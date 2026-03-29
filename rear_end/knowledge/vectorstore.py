from __future__ import annotations

"""
文档入库向量化与 FAISS 索引读写。

- embed_texts：统一向量化入口（支持 openai / fake 两种后端）
- add_vectors_to_index：追加写入向量
- rebuild_index：按文本集合重建索引（用于删除文档后的同步）
"""

import os
import json
import threading
from dataclasses import dataclass
from functools import lru_cache
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

    embeddings = _get_openai_embeddings(cfg.model, cfg.base_url, api_key)
    vectors = embeddings.embed_documents(texts)
    return np.asarray(vectors, dtype=np.float32)


@lru_cache(maxsize=4)
def _get_openai_embeddings(model: str, base_url: str, api_key: str):
    from langchain_openai import OpenAIEmbeddings

    kwargs = {"model": model, "api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAIEmbeddings(check_embedding_ctx_length=False, **kwargs)


def _faiss():
    import faiss

    return faiss


_INDEX_CACHE_LOCK = threading.Lock()
_INDEX_CACHE: dict[str, tuple[float, object]] = {}

_META_CACHE_LOCK = threading.Lock()
_META_CACHE: dict[str, tuple[float, list[int]]] = {}


def _meta_path(index_path: Path) -> Path:
    return index_path.with_name(f"{index_path.name}.meta.json")


def load_faiss_index(index_path: Path):
    faiss = _faiss()
    if not index_path.exists() or index_path.stat().st_size == 0:
        return None
    key = str(index_path.resolve())
    mtime = float(index_path.stat().st_mtime)
    with _INDEX_CACHE_LOCK:
        cached = _INDEX_CACHE.get(key)
        if cached and cached[0] == mtime:
            return cached[1]
    try:
        index = faiss.read_index(str(index_path))
        with _INDEX_CACHE_LOCK:
            _INDEX_CACHE[key] = (mtime, index)
        return index
    except Exception:
        return None


def save_faiss_index(index, index_path: Path) -> None:
    faiss = _faiss()
    index_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(index_path))


def load_faiss_meta(index_path: Path) -> list[int] | None:
    mp = _meta_path(index_path)
    if not mp.exists() or mp.stat().st_size == 0:
        return None
    key = str(mp.resolve())
    mtime = float(mp.stat().st_mtime)
    with _META_CACHE_LOCK:
        cached = _META_CACHE.get(key)
        if cached and cached[0] == mtime:
            return list(cached[1])
    try:
        data = json.loads(mp.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            return None
        ids = [int(x) for x in data]
        with _META_CACHE_LOCK:
            _META_CACHE[key] = (mtime, ids)
        return list(ids)
    except Exception:
        return None


def save_faiss_meta(index_path: Path, chunk_ids: list[int]) -> None:
    mp = _meta_path(index_path)
    mp.parent.mkdir(parents=True, exist_ok=True)
    tmp = mp.with_name(f"{mp.name}.tmp")
    tmp.write_text(json.dumps([int(x) for x in chunk_ids], ensure_ascii=False), encoding="utf-8")
    os.replace(str(tmp), str(mp))
    key = str(mp.resolve())
    mtime = float(mp.stat().st_mtime)
    with _META_CACHE_LOCK:
        _META_CACHE[key] = (mtime, list(chunk_ids))


def add_vectors_to_index(index_path: Path, texts: list[str], chunk_ids: list[int] | None = None) -> int:
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
    if chunk_ids is not None:
        existing = load_faiss_meta(index_path) or []
        existing.extend([int(x) for x in chunk_ids])
        save_faiss_meta(index_path, existing)
    return int(vectors.shape[0])


def rebuild_index(index_path: Path, texts: Iterable[str], chunk_ids: Iterable[int] | None = None) -> int:
    texts_list: list[str] = []
    ids_list: list[int] = []
    if chunk_ids is None:
        texts_list = [t for t in texts if (t or "").strip()]
    else:
        for cid, t in zip(chunk_ids, texts):
            if (t or "").strip():
                texts_list.append(t)
                ids_list.append(int(cid))
    if not texts_list:
        try:
            index_path.unlink()
        except FileNotFoundError:
            pass
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.open("wb").close()
        mp = _meta_path(index_path)
        try:
            mp.unlink()
        except FileNotFoundError:
            pass
        return 0

    vectors = embed_texts(texts_list)
    dim = int(vectors.shape[1])
    faiss = _faiss()
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    save_faiss_index(index, index_path)
    if chunk_ids is not None:
        save_faiss_meta(index_path, ids_list)
    return int(vectors.shape[0])


def count_vectors(index_path: Path) -> int:
    index = load_faiss_index(index_path)
    if index is None:
        return 0
    return int(index.ntotal)
