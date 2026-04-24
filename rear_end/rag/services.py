from __future__ import annotations

import os
import time
import logging
from functools import lru_cache
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from django.conf import settings

from knowledge.models import DocumentChunk, KnowledgeBase
from knowledge.vectorstore import embed_texts, load_faiss_index, load_faiss_meta, save_faiss_meta

logger = logging.getLogger(__name__)


class RagError(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


@dataclass(frozen=True)
class RagConfig:
    top_k: int
    max_context_chars: int


def _get_rag_config() -> RagConfig:
    top_k = int(os.getenv("RAG_TOP_K", "4"))
    max_context_chars = int(os.getenv("RAG_MAX_CONTEXT_CHARS", "6000"))
    if top_k <= 0:
        top_k = 1
    if max_context_chars <= 0:
        max_context_chars = 1000
    return RagConfig(top_k=top_k, max_context_chars=max_context_chars)


def _truncate(text: str, max_chars: int) -> str:
    if max_chars <= 0:
        return ""
    text = text or ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars]


def _build_prompt(question: str, contexts: list[str], max_context_chars: int) -> str:
    context_text = "\n\n---\n\n".join([c for c in contexts if (c or "").strip()])
    context_text = _truncate(context_text, max_context_chars)
    return (
        "你是一个检索增强问答助手。请只基于“资料”回答问题；如果资料不足以回答，请明确说明不知道。\n\n"
        f"资料：\n{context_text}\n\n"
        f"问题：{(question or '').strip()}\n\n"
        "回答："
    )


@dataclass(frozen=True)
class LlmConfig:
    model: str
    base_url: str


def _get_llm_config() -> LlmConfig:
    model = os.getenv("OPENAI_CHAT_MODEL", "") or os.getenv("OPENAI_MODEL", "")
    base_url = getattr(settings, "OPENAI_BASE_URL", "") or os.getenv("OPENAI_BASE_URL", "")
    if not model:
        if base_url and ("dashscope" in base_url.lower() or "aliyuncs" in base_url.lower()):
            model = "qwen-plus"
        else:
            model = "gpt-4o-mini"
    return LlmConfig(model=model, base_url=base_url)


@lru_cache(maxsize=4)
def _get_chat_openai_llm(model: str, base_url: str, api_key: str, streaming: bool):
    from langchain_openai import ChatOpenAI

    kwargs: dict = {"model": model, "api_key": api_key, "temperature": 0}
    if base_url:
        kwargs["base_url"] = base_url
    if streaming:
        kwargs["streaming"] = True
    return ChatOpenAI(**kwargs)

 
@dataclass(frozen=True)
class TokenUsage:
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None


def _to_int_or_none(v):
    try:
        if v is None:
            return None
        return int(v)
    except Exception:
        return None


def _extract_token_usage(resp) -> TokenUsage:
    prompt_tokens = None
    completion_tokens = None
    total_tokens = None

    usage = getattr(resp, "usage_metadata", None)
    if isinstance(usage, dict):
        prompt_tokens = _to_int_or_none(usage.get("input_tokens") or usage.get("prompt_tokens"))
        completion_tokens = _to_int_or_none(
            usage.get("output_tokens") or usage.get("completion_tokens")
        )
        total_tokens = _to_int_or_none(usage.get("total_tokens"))

    if prompt_tokens is None and completion_tokens is None and total_tokens is None:
        meta = getattr(resp, "response_metadata", None)
        if isinstance(meta, dict):
            u = meta.get("token_usage") or meta.get("usage")
            if isinstance(u, dict):
                prompt_tokens = _to_int_or_none(u.get("prompt_tokens"))
                completion_tokens = _to_int_or_none(u.get("completion_tokens"))
                total_tokens = _to_int_or_none(u.get("total_tokens"))

    if prompt_tokens is None and completion_tokens is None and total_tokens is None:
        kw = getattr(resp, "additional_kwargs", None)
        if isinstance(kw, dict):
            u = kw.get("token_usage") or kw.get("usage")
            if isinstance(u, dict):
                prompt_tokens = _to_int_or_none(u.get("prompt_tokens"))
                completion_tokens = _to_int_or_none(u.get("completion_tokens"))
                total_tokens = _to_int_or_none(u.get("total_tokens"))

    if total_tokens is None and prompt_tokens is not None and completion_tokens is not None:
        total_tokens = int(prompt_tokens) + int(completion_tokens)

    return TokenUsage(
        prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens
    )


def _generate_answer_fake(question: str, contexts: list[str]) -> str:
    first_ctx = (contexts[0] if contexts else "").strip()
    first_ctx = _truncate(first_ctx, 200)
    q = (question or "").strip()
    if first_ctx:
        return f"（fake）基于资料：{first_ctx}\n\n对问题“{q}”的回答：请参考上述资料。"
    return f"（fake）资料不足，无法回答问题“{q}”。"


def _generate_answer_openai(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "") or os.getenv("DASHSCOPE_API_KEY", "")
    if not api_key:
        raise RagError(500, "模型 API Key 未配置")

    cfg = _get_llm_config()
    llm = _get_chat_openai_llm(cfg.model, cfg.base_url, api_key, streaming=False)
    resp = llm.invoke(prompt)
    usage = _extract_token_usage(resp)
    content = getattr(resp, "content", None)
    if not content:
        raise RagError(500, "模型未返回有效内容")
    return str(content).strip(), usage


def _stream_answer_openai(prompt: str):
    api_key = os.getenv("OPENAI_API_KEY", "") or os.getenv("DASHSCOPE_API_KEY", "")
    if not api_key:
        raise RagError(500, "模型 API Key 未配置")

    cfg = _get_llm_config()
    llm = _get_chat_openai_llm(cfg.model, cfg.base_url, api_key, streaming=True)
    for chunk in llm.stream(prompt):
        delta = getattr(chunk, "content", None)
        if isinstance(delta, str) and delta:
            yield delta


def generate_answer(question: str, contexts: list[str], max_context_chars: int) -> str:
    backend = (os.getenv("RAG_LLM_BACKEND", "") or "openai").lower()
    if backend == "fake":
        return _generate_answer_fake(question, contexts)

    prompt = _build_prompt(question, contexts, max_context_chars=max_context_chars)
    answer, _usage = _generate_answer_openai(prompt)
    return answer


def generate_answer_with_usage(question: str, contexts: list[str], max_context_chars: int) -> tuple[str, TokenUsage]:
    backend = (os.getenv("RAG_LLM_BACKEND", "") or "openai").lower()
    if backend == "fake":
        return _generate_answer_fake(question, contexts), TokenUsage(None, None, None)

    prompt = _build_prompt(question, contexts, max_context_chars=max_context_chars)
    return _generate_answer_openai(prompt)


def stream_answer(question: str, contexts: list[str], max_context_chars: int):
    backend = (os.getenv("RAG_LLM_BACKEND", "") or "openai").lower()
    if backend == "fake":
        yield _generate_answer_fake(question, contexts)
        return

    prompt = _build_prompt(question, contexts, max_context_chars=max_context_chars)
    yield from _stream_answer_openai(prompt)


def retrieve_contexts(kb: KnowledgeBase, question: str, top_k: int) -> list[str]:
    index_path = Path(kb.faiss_path)
    index = load_faiss_index(index_path)
    if index is None:
        raise RagError(400, "知识库索引不可用")

    q_vec = embed_texts([(question or "").strip()])
    q_vec = np.asarray(q_vec, dtype=np.float32)
    if q_vec.ndim != 2 or q_vec.shape[0] != 1:
        raise RagError(500, "问题向量化失败")

    if int(getattr(index, "d", -1)) != int(q_vec.shape[1]):
        raise RagError(500, "索引维度与 embedding 不一致，请重建索引")

    _, idx = index.search(q_vec, int(top_k))
    idx_list = [int(i) for i in idx[0].tolist() if int(i) >= 0]
    contexts: list[str] = []
    chunk_ids = load_faiss_meta(index_path)
    if chunk_ids is None:
        ids = list(
            DocumentChunk.objects.filter(document__kb=kb)
            .order_by("document_id", "chunk_index")
            .values_list("id", flat=True)
        )
        if ids and int(getattr(index, "ntotal", 0)) == int(len(ids)):
            save_faiss_meta(index_path, ids)
            chunk_ids = ids
    if chunk_ids and int(getattr(index, "ntotal", 0)) == int(len(chunk_ids)):
        selected_ids = [chunk_ids[i] for i in idx_list if 0 <= i < len(chunk_ids)]
        rows = DocumentChunk.objects.filter(id__in=selected_ids).values_list("id", "text")
        text_by_id = {int(i): (t or "") for i, t in rows}
        for cid in selected_ids:
            t = (text_by_id.get(int(cid), "") or "").strip()
            if t:
                contexts.append(t)
        if contexts:
            return contexts

    texts = list(
        DocumentChunk.objects.filter(document__kb=kb)
        .order_by("document_id", "chunk_index")
        .values_list("text", flat=True)
    )
    if not texts:
        raise RagError(400, "知识库暂无可检索内容")
    for i in idx_list:
        if 0 <= i < len(texts):
            t = (texts[i] or "").strip()
            if t:
                contexts.append(t)
    return contexts


def rag_chat(kb: KnowledgeBase, question: str) -> str:
    cfg = _get_rag_config()
    t0 = time.perf_counter()
    contexts = retrieve_contexts(kb, question, top_k=cfg.top_k)
    t1 = time.perf_counter()
    answer, usage = generate_answer_with_usage(question, contexts, max_context_chars=cfg.max_context_chars)
    t2 = time.perf_counter()
    answer = (answer or "").strip()
    if not answer:
        raise RagError(500, "生成回答失败")
    if (os.getenv("RAG_LOG_TIMINGS", "") or "").strip() == "1":
        logger.info(
            "rag_chat kb=%s retrieve_ms=%.1f generate_ms=%.1f total_ms=%.1f",
            getattr(kb, "id", None),
            (t1 - t0) * 1000.0,
            (t2 - t1) * 1000.0,
            (t2 - t0) * 1000.0,
        )
    elapsed_ms = int(max(0.0, (t2 - t0) * 1000.0))
    return {
        "answer": answer,
        "elapsed_ms": elapsed_ms,
        "token_usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        },
    }


def rag_chat_stream(kb: KnowledgeBase, question: str):
    cfg = _get_rag_config()
    t0 = time.perf_counter()
    contexts = retrieve_contexts(kb, question, top_k=cfg.top_k)
    t1 = time.perf_counter()

    # 生成完整回答以保存到数据库
    answer, usage = generate_answer_with_usage(question, contexts, max_context_chars=cfg.max_context_chars)
    answer = (answer or "").strip()
    t2 = time.perf_counter()
    elapsed_ms = int(max(0.0, (t2 - t0) * 1000.0))

    def gen():
        try:
            yield from stream_answer(question, contexts, max_context_chars=cfg.max_context_chars)
        finally:
            if (os.getenv("RAG_LOG_TIMINGS", "") or "").strip() == "1":
                logger.info(
                    "rag_chat_stream kb=%s retrieve_ms=%.1f generate_ms=%.1f total_ms=%.1f",
                    getattr(kb, "id", None),
                    (t1 - t0) * 1000.0,
                    (t2 - t1) * 1000.0,
                    (t2 - t0) * 1000.0,
                )

    return gen(), answer, {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
    }, elapsed_ms
