import os
from pathlib import Path

from django.conf import settings


def ensure_dir(path: Path) -> None:
    # 确保目录存在（并发下也安全）
    path.mkdir(parents=True, exist_ok=True)


def build_kb_index_path(user_id: int, kb_id: int) -> Path:
    # 将索引文件按 user 目录隔离，避免不同用户之间的文件混用
    root = Path(settings.FAISS_INDEX_ROOT)
    return root / f"user_{user_id}" / f"kb_{kb_id}.index"


def create_empty_index_file(file_path: Path) -> None:
    # 创建空索引文件：已存在则不覆盖
    ensure_dir(file_path.parent)
    try:
        file_path.open("xb").close()
    except FileExistsError:
        return


def safe_remove_file(file_path: str | os.PathLike) -> None:
    # 删除文件：不存在则忽略
    try:
        Path(file_path).unlink()
    except FileNotFoundError:
        return


def build_upload_path(user_id: int, kb_id: int, filename: str) -> Path:
    # 上传文件按用户/知识库隔离，且仅取 basename 防止路径穿越。
    root = Path(settings.KB_UPLOAD_ROOT)
    safe_name = Path(filename).name
    return root / f"user_{user_id}" / f"kb_{kb_id}" / safe_name


def save_uploaded_file(upload_path: Path, file_obj) -> None:
    # 以流式方式落盘，避免一次性把大文件读入内存。
    ensure_dir(upload_path.parent)
    with upload_path.open("wb") as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
