import json
import math
import os
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

DEFAULT_KNOWLEDGE_BASE: List[Dict[str, object]] = [
    {
        "id": "kb-001",
        "title": "草莓白粉病防治",
        "content": "加强通风，降低湿度；发病初期可使用三唑类药剂，按标签剂量喷施。",
        "crop": "草莓",
        "disease_en": "powdery_mildew",
    },
    {
        "id": "kb-002",
        "title": "蚜虫综合治理",
        "content": "优先生物防治与黄板诱杀，必要时轮换低抗性风险杀虫剂。",
        "disease_en": "aphid",
    },
    {
        "id": "kb-003",
        "title": "灰霉病管理要点",
        "content": "清理病残体，控制棚内湿度，开花期注意预防性用药。",
        "disease_en": "gray_mold",
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
    items: List[Dict[str, object]]
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
    parts.append(f"emb_model:{os.getenv('EMBEDDING_MODEL', 'text-embedding-v4')}")
    parts.append(f"emb_dim:{os.getenv('EMBEDDING_DIM', '1024')}")
    return "|".join(parts)


def _load_chunks_from_files() -> List[Dict[str, object]]:
    chunks: List[Dict[str, object]] = []
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
            normalized: Dict[str, object] = dict(item)
            normalized["id"] = str(item.get("id", f"{jf.stem}-{idx}"))
            normalized["title"] = title or "未命名知识块"
            normalized["content"] = content
            chunks.append(normalized)

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
                normalized: Dict[str, object] = dict(item)
                normalized["id"] = str(item.get("id", f"{jlf.stem}-{idx}"))
                normalized["title"] = title or "未命名知识块"
                normalized["content"] = content
                chunks.append(normalized)
    return chunks


def _load_chunks_from_manual() -> List[Dict[str, object]]:
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

    chunks: List[Dict[str, object]] = []
    for idx, (title, body_lines) in enumerate(sections, start=1):
        content = "\n".join(x for x in body_lines if x).strip()
        if not content:
            continue
        chunks.append(
            {
                "id": f"manual-{idx:03d}",
                "title": title,
                "content": content,
                "crop": "草莓" if "草莓" in title else ("蓝莓" if "蓝莓" in title else ""),
                "disease_en": (
                    "powdery_mildew"
                    if "白粉" in title
                    else ("aphid" if "蚜虫" in title else ("gray_mold" if "灰霉" in title else ""))
                ),
            }
        )
    return chunks


def _load_items() -> List[Dict[str, object]]:
    items = _load_chunks_from_files()
    if items:
        return items

    manual_items = _load_chunks_from_manual()
    if manual_items:
        return manual_items

    return DEFAULT_KNOWLEDGE_BASE.copy()


def _build_vectors(items: List[Dict[str, object]], dim: int) -> List[List[float]]:
    return [embed_text(f"{x['title']}\n{x['content']}", dim=dim) for x in items]


def _to_float32_array(vectors: List[List[float]]):  # type: ignore[no-untyped-def]
    if np is None:
        return None
    arr = np.array(vectors, dtype="float32")
    if arr.ndim != 2 or arr.shape[0] == 0:
        return None
    return arr


def _persist_cache(items: List[Dict[str, object]], vectors: List[List[float]]) -> None:
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    signature = _source_signature()
    dim = len(vectors[0]) if vectors else 0
    META_CACHE_FILE.write_text(
        json.dumps(
            {
                "count": len(items),
                "dim": dim,
                "signature": signature,
                "items": items,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    VECTORS_CACHE_FILE.write_text(
        json.dumps(vectors, ensure_ascii=False), encoding="utf-8"
    )


def _load_cached_items_vectors(
    signature: str, dim: int
) -> Optional[Tuple[List[Dict[str, object]], List[List[float]]]]:
    if not META_CACHE_FILE.exists() or not VECTORS_CACHE_FILE.exists():
        return None
    try:
        meta = json.loads(META_CACHE_FILE.read_text(encoding="utf-8"))
        vectors = json.loads(VECTORS_CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None

    if not isinstance(meta, dict) or not isinstance(vectors, list):
        return None
    if str(meta.get("signature", "")) != signature:
        return None
    if int(meta.get("dim", 0)) != dim:
        return None

    items = meta.get("items", [])
    if not isinstance(items, list):
        return None
    if len(items) != len(vectors):
        return None
    if vectors and (not isinstance(vectors[0], list) or len(vectors[0]) != dim):
        return None
    return items, vectors


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

    if (
        _INDEX_CACHE
        and _INDEX_CACHE.signature == signature
        and _INDEX_CACHE.vectors
        and len(_INDEX_CACHE.vectors[0]) == dim
    ):
        return _INDEX_CACHE

    cached = _load_cached_items_vectors(signature=signature, dim=dim)
    if cached is not None:
        items, vectors = cached
        faiss_index = _build_faiss_index(vectors)
        _INDEX_CACHE = _IndexCache(
            items=items,
            vectors=vectors,
            signature=signature,
            faiss_index=faiss_index,
        )
        return _INDEX_CACHE

    items = _load_items()
    vectors = _build_vectors(items, dim=dim)
    _persist_cache(items, vectors)
    faiss_index = _build_faiss_index(vectors)
    _INDEX_CACHE = _IndexCache(
        items=items, vectors=vectors, signature=signature, faiss_index=faiss_index
    )
    return _INDEX_CACHE


def _pack_item(item: Dict[str, object], score: float) -> Dict[str, object]:
    keywords_val = item.get("keywords", [])
    keywords = keywords_val if isinstance(keywords_val, list) else []
    return {
        "id": str(item.get("id", "")),
        "title": str(item.get("title", "")),
        "content": str(item.get("content", "")),
        "score": round(float(score), 4),
        "crop": str(item.get("crop", "")),
        "disease_en": str(item.get("disease_en", "")),
        "keywords": [str(x) for x in keywords],
        "dose": str(item.get("dose", "")),
        "interval_days": str(item.get("interval_days", "")),
    }


def _search_with_faiss(
    query_vector: List[float], top_k: int, cache: _IndexCache
) -> List[Dict[str, object]]:
    if cache.faiss_index is None or np is None:
        return []

    q = np.array([query_vector], dtype="float32")
    faiss.normalize_L2(q)
    scores, indices = cache.faiss_index.search(q, top_k)

    out: List[Dict[str, object]] = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(cache.items):
            continue
        item = cache.items[int(idx)]
        out.append(_pack_item(item, score=float(score)))
    return out


def _search_with_cosine(
    query_vector: List[float], top_k: int, cache: _IndexCache
) -> List[Dict[str, object]]:
    scored: List[Dict[str, object]] = []
    for item, item_vec in zip(cache.items, cache.vectors):
        score = _cosine_similarity(query_vector, item_vec)
        scored.append(_pack_item(item, score=score))
    scored.sort(key=lambda x: float(x["score"]), reverse=True)
    return scored[:top_k]


def _normalize_hint(value: Optional[str]) -> str:
    if not value:
        return ""
    return value.strip().lower().replace("-", "_")


def _item_matches_filter(
    item: Dict[str, object], crop: Optional[str], disease_hint: Optional[str]
) -> bool:
    crop_q = (crop or "").strip().lower()
    disease_q = _normalize_hint(disease_hint)
    if disease_q == "unknown_leaf_issue":
        disease_q = ""

    title = str(item.get("title", "")).lower()
    content = str(item.get("content", "")).lower()
    item_crop = str(item.get("crop", "")).lower()
    item_disease = _normalize_hint(str(item.get("disease_en", "")))
    keywords = " ".join(str(x).lower() for x in item.get("keywords", [])) if isinstance(item.get("keywords"), list) else ""

    if crop_q:
        if crop_q not in item_crop and crop_q not in title and crop_q not in content and crop_q not in keywords:
            return False

    if disease_q:
        if disease_q not in item_disease and disease_q not in title and disease_q not in content and disease_q not in keywords:
            return False
    return True


def search(
    query_vector: List[float],
    top_k: int = 3,
    crop: Optional[str] = None,
    disease_hint: Optional[str] = None,
) -> List[Dict[str, object]]:
    if top_k <= 0:
        return []

    cache = _ensure_index(dim=len(query_vector))
    if not cache.items:
        return []

    need_filter = bool((crop or "").strip() or _normalize_hint(disease_hint))
    top_n = len(cache.items) if need_filter else min(top_k, len(cache.items))

    faiss_result = _search_with_faiss(query_vector, top_k=top_n, cache=cache)
    base_result = faiss_result if faiss_result else _search_with_cosine(query_vector, top_k=top_n, cache=cache)

    if need_filter:
        item_map = {str(x.get("id", "")): x for x in cache.items}
        filtered = [
            r
            for r in base_result
            if _item_matches_filter(item_map.get(str(r.get("id", "")), {}), crop=crop, disease_hint=disease_hint)
        ]
        if filtered:
            return filtered[:top_k]
    return base_result[:top_k]
