import hashlib
import os
from typing import List, Optional

try:
    from openai import OpenAI  # type: ignore
except Exception:
    OpenAI = None  # type: ignore[assignment]

_CLIENT: Optional["OpenAI"] = None


def _hash_embed(text: str, dim: int) -> List[float]:
    # Local fallback to keep service available when API is unavailable.
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values: List[float] = []
    for i in range(dim):
        byte_val = digest[i % len(digest)]
        values.append((byte_val / 255.0) * 2 - 1)
    return values


def _get_client() -> Optional["OpenAI"]:
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT

    if OpenAI is None:
        return None

    api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        return None

    _CLIENT = OpenAI(
        api_key=api_key,
        base_url=os.getenv(
            "EMBEDDING_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
        ),
    )
    return _CLIENT


def embed_text(text: str, dim: int = 1024) -> List[float]:
    client = _get_client()
    if client is None:
        return _hash_embed(text, dim)

    model = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")
    try:
        resp = client.embeddings.create(model=model, input=text, dimensions=dim)
        return list(resp.data[0].embedding)
    except Exception:
        return _hash_embed(text, dim)
