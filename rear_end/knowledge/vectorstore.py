from __future__ import annotations

"""
文档入库向量化与 FAISS 索引读写。

- embed_texts：统一向量化入口（支持 openai / fake 两种后端）
- add_vectors_to_index：追加写入向量
- rebuild_index：按文本集合重建索引（用于删除文档后的同步）
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
from django.conf import settings


@dataclass(frozen=True)
class EmbeddingConfig:
    model: str
    base_url: str


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be < chunk_size")

    text = (text or "").strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - chunk_overlap
        if start < 0:
            start = 0
        if end == len(text):
            break
    return chunks


def _get_embedding_config() -> EmbeddingConfig:
    model = getattr(settings, "OPENAI_EMBEDDING_MODEL", "") or os.getenv("OPENAI_EMBEDDING_MODEL", "")
    base_url = getattr(settings, "OPENAI_BASE_URL", "") or os.getenv("OPENAI_BASE_URL", "")
    return EmbeddingConfig(model=model, base_url=base_url)


def _embed_texts_fake(texts: list[str]) -> np.ndarray:
    # 测试用假向量：避免在 CI/本地跑测试时依赖真实外部 API。
    dim = 8
    vectors = np.zeros((len(texts), dim), dtype=np.float32)
    for i, t in enumerate(texts):
        h = abs(hash(t)) % 10_000_000
        for j in range(dim):
            vectors[i, j] = float((h >> (j * 3)) & 0x7) / 7.0
    return vectors


def embed_texts(texts: list[str]) -> np.ndarray:
    # 通过环境变量切换向量化后端：默认 openai，测试可用 fake。
    backend = (os.getenv("KB_EMBEDDING_BACKEND", "") or "openai").lower()
    if backend == "fake":
        return _embed_texts_fake(texts)
    return embed_texts_langchain_openai(texts)


def embed_texts_langchain_openai(texts: list[str]) -> np.ndarray:
    api_key = os.getenv("OPENAI_API_KEY", "") or os.getenv("DASHSCOPE_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 或 DASHSCOPE_API_KEY 未配置")

    cfg = _get_embedding_config()
    if not cfg.model:
        raise RuntimeError("OPENAI_EMBEDDING_MODEL 未配置")

    from langchain_openai import OpenAIEmbeddings

    kwargs = {"model": cfg.model, "api_key": api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url

    # DashScope 的 OpenAI 兼容 embeddings 接口不接受 token ids 列表作为 input，
    # 关闭长度安全逻辑以确保按 list[str] 直接发送。
    embeddings = OpenAIEmbeddings(check_embedding_ctx_length=False, **kwargs)
    vectors = embeddings.embed_documents(texts)
    return np.asarray(vectors, dtype=np.float32)


def _faiss():
    import faiss

    return faiss


def load_faiss_index(index_path: Path):
    faiss = _faiss()
    if not index_path.exists() or index_path.stat().st_size == 0:
        return None
    try:
        return faiss.read_index(str(index_path))
    except Exception:
        return None


def save_faiss_index(index, index_path: Path) -> None:
    faiss = _faiss()
    index_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(index_path))


def add_vectors_to_index(index_path: Path, texts: list[str]) -> int:
    if not texts:
        return 0
    vectors = embed_texts(texts)
    dim = int(vectors.shape[1])

    index = load_faiss_index(index_path)
    if index is None or int(index.d) != dim:
        faiss = _faiss()
        index = faiss.IndexFlatL2(dim)

    index.add(vectors)
    save_faiss_index(index, index_path)
    return int(vectors.shape[0])


def rebuild_index(index_path: Path, texts: Iterable[str]) -> int:
    texts_list = [t for t in texts if (t or "").strip()]
    if not texts_list:
        try:
            index_path.unlink()
        except FileNotFoundError:
            pass
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.open("wb").close()
        return 0

    vectors = embed_texts(texts_list)
    dim = int(vectors.shape[1])
    faiss = _faiss()
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    save_faiss_index(index, index_path)
    return int(vectors.shape[0])


def count_vectors(index_path: Path) -> int:
    index = load_faiss_index(index_path)
    if index is None:
        return 0
    return int(index.ntotal)
