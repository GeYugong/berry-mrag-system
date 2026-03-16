import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from rag_module.embedder import embed_text

try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # type: ignore[assignment]

try:
    import faiss  # type: ignore
except Exception:
    faiss = None  # type: ignore[assignment]

DEFAULT_KNOWLEDGE_BASE: List[Dict[str, str]] = [
    {
        "id": "kb-001",
        "title": "草莓白粉病防治",
        "content": "加强通风，降低湿度；发病初期可使用三唑类药剂，按标签剂量喷施。",
    },
    {
        "id": "kb-002",
        "title": "蚜虫综合治理",
        "content": "优先生物防治与黄板诱杀，必要时轮换低抗性风险杀虫剂。",
    },
    {
        "id": "kb-003",
        "title": "灰霉病管理要点",
        "content": "清理病残体，控制棚内湿度，开花期注意预防性用药。",
    },
]

CHUNKS_DIR = Path("data/chunks")
VECTOR_STORE_DIR = Path("data/vector_store")
VECTORS_CACHE_FILE = VECTOR_STORE_DIR / "retriever_vectors.json"
META_CACHE_FILE = VECTOR_STORE_DIR / "retriever_meta.json"
FAISS_INDEX_FILE = VECTOR_STORE_DIR / "retriever.index"
MANUAL_MD_FILE = Path("docs/berry_manual.md")


@dataclass
class _IndexCache:
    items: List[Dict[str, str]]
    vectors: List[List[float]]
    signature: str
    faiss_index: Optional[object] = None


_INDEX_CACHE: Optional[_IndexCache] = None


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _source_signature() -> str:
    tracked: List[Path] = []
    if CHUNKS_DIR.exists():
        tracked.extend(sorted(CHUNKS_DIR.glob("*.json")))
        tracked.extend(sorted(CHUNKS_DIR.glob("*.jsonl")))
    if MANUAL_MD_FILE.exists():
        tracked.append(MANUAL_MD_FILE)

    if not tracked:
        return "default"

    parts: List[str] = []
    for p in tracked:
        st = p.stat()
        parts.append(f"{p.as_posix()}:{int(st.st_mtime)}:{st.st_size}")
    return "|".join(parts)


def _load_chunks_from_files() -> List[Dict[str, str]]:
    chunks: List[Dict[str, str]] = []
    if not CHUNKS_DIR.exists():
        return chunks

    json_files = sorted(CHUNKS_DIR.glob("*.json"))
    jsonl_files = sorted(CHUNKS_DIR.glob("*.jsonl"))

    for jf in json_files:
        with jf.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            continue
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                continue
            title = str(item.get("title", "")).strip()
            content = str(item.get("content", "")).strip()
            if not content:
                continue
            chunks.append(
                {
                    "id": str(item.get("id", f"{jf.stem}-{idx}")),
                    "title": title or "未命名知识块",
                    "content": content,
                }
            )

    for jlf in jsonl_files:
        with jlf.open("r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(item, dict):
                    continue
                title = str(item.get("title", "")).strip()
                content = str(item.get("content", "")).strip()
                if not content:
                    continue
                chunks.append(
                    {
                        "id": str(item.get("id", f"{jlf.stem}-{idx}")),
                        "title": title or "未命名知识块",
                        "content": content,
                    }
                )
    return chunks


def _load_chunks_from_manual() -> List[Dict[str, str]]:
    if not MANUAL_MD_FILE.exists():
        return []

    lines = MANUAL_MD_FILE.read_text(encoding="utf-8").splitlines()
    sections: List[Tuple[str, List[str]]] = []
    current_title = ""
    current_body: List[str] = []

    for line in lines:
        if line.startswith("## "):
            if current_title and current_body:
                sections.append((current_title, current_body))
            current_title = line.replace("## ", "", 1).strip()
            current_body = []
            continue
        if current_title:
            current_body.append(line.strip())

    if current_title and current_body:
        sections.append((current_title, current_body))

    chunks: List[Dict[str, str]] = []
    for idx, (title, body_lines) in enumerate(sections, start=1):
        content = "\n".join(x for x in body_lines if x).strip()
        if not content:
            continue
        chunks.append(
            {
                "id": f"manual-{idx:03d}",
                "title": title,
                "content": content,
            }
        )
    return chunks


def _load_items() -> List[Dict[str, str]]:
    items = _load_chunks_from_files()
    if items:
        return items

    manual_items = _load_chunks_from_manual()
    if manual_items:
        return manual_items

    return DEFAULT_KNOWLEDGE_BASE.copy()


def _build_vectors(items: List[Dict[str, str]], dim: int) -> List[List[float]]:
    return [embed_text(f"{x['title']}\n{x['content']}", dim=dim) for x in items]


def _to_float32_array(vectors: List[List[float]]):  # type: ignore[no-untyped-def]
    if np is None:
        return None
    arr = np.array(vectors, dtype="float32")
    if arr.ndim != 2 or arr.shape[0] == 0:
        return None
    return arr


def _persist_cache(items: List[Dict[str, str]], vectors: List[List[float]]) -> None:
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    META_CACHE_FILE.write_text(
        json.dumps({"count": len(items), "items": items}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    VECTORS_CACHE_FILE.write_text(
        json.dumps(vectors, ensure_ascii=False), encoding="utf-8"
    )


def _build_faiss_index(vectors: List[List[float]]) -> Optional[object]:
    if faiss is None or np is None:
        return None
    if not vectors:
        return None

    arr = _to_float32_array(vectors)
    if arr is None:
        return None

    faiss.normalize_L2(arr)
    index = faiss.IndexFlatIP(arr.shape[1])
    index.add(arr)
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_INDEX_FILE))
    return index


def _ensure_index(dim: int) -> _IndexCache:
    global _INDEX_CACHE
    signature = _source_signature()

    if _INDEX_CACHE and _INDEX_CACHE.signature == signature:
        return _INDEX_CACHE

    items = _load_items()
    vectors = _build_vectors(items, dim=dim)
    _persist_cache(items, vectors)
    faiss_index = _build_faiss_index(vectors)
    _INDEX_CACHE = _IndexCache(
        items=items, vectors=vectors, signature=signature, faiss_index=faiss_index
    )
    return _INDEX_CACHE


def _search_with_faiss(
    query_vector: List[float], top_k: int, cache: _IndexCache
) -> List[Dict[str, Union[str, float]]]:
    if cache.faiss_index is None or np is None:
        return []

    q = np.array([query_vector], dtype="float32")
    faiss.normalize_L2(q)
    scores, indices = cache.faiss_index.search(q, top_k)

    out: List[Dict[str, Union[str, float]]] = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(cache.items):
            continue
        out.append({**cache.items[int(idx)], "score": round(float(score), 4)})
    return out


def _search_with_cosine(
    query_vector: List[float], top_k: int, cache: _IndexCache
) -> List[Dict[str, Union[str, float]]]:
    scored: List[Dict[str, Union[str, float]]] = []
    for item, item_vec in zip(cache.items, cache.vectors):
        score = _cosine_similarity(query_vector, item_vec)
        scored.append({**item, "score": round(score, 4)})
    scored.sort(key=lambda x: float(x["score"]), reverse=True)
    return scored[:top_k]


def search(query_vector: List[float], top_k: int = 3) -> List[Dict[str, Union[str, float]]]:
    if top_k <= 0:
        return []

    cache = _ensure_index(dim=len(query_vector))
    if not cache.items:
        return []

    top_k = min(top_k, len(cache.items))
    faiss_result = _search_with_faiss(query_vector, top_k=top_k, cache=cache)
    if faiss_result:
        return faiss_result
    return _search_with_cosine(query_vector, top_k=top_k, cache=cache)
