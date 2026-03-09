import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple
from urllib import request
from urllib.error import HTTPError, URLError

_EMBED_CACHE: Dict[Tuple[str, str, str], List[float]] = {}


def _fallback_embed(text: str, dim: int) -> List[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values: List[float] = []
    for i in range(dim):
        byte_val = digest[i % len(digest)]
        values.append((byte_val / 255.0) * 2 - 1)
    return values


def _clip_or_pad(vec: List[float], dim: int) -> List[float]:
    if len(vec) == dim:
        return vec
    if len(vec) > dim:
        return vec[:dim]
    return vec + [0.0] * (dim - len(vec))


def _extract_embedding(resp: Dict[str, Any]) -> Optional[List[float]]:
    data = resp.get("data")
    if isinstance(data, list) and data:
        emb = data[0].get("embedding")
        if isinstance(emb, list):
            return [float(v) for v in emb]

    output = resp.get("output")
    if isinstance(output, dict):
        embeddings = output.get("embeddings")
        if isinstance(embeddings, list) and embeddings:
            first = embeddings[0]
            if isinstance(first, dict):
                emb = first.get("embedding")
                if isinstance(emb, list):
                    return [float(v) for v in emb]
    return None


def embed_text(
    text: str,
    dim: int = 16,
    enabled: bool = True,
    model: str = "qwen3-vl-embedding",
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: float = 20.0,
) -> List[float]:
    if not enabled or not api_url or not api_key:
        return _fallback_embed(text, dim)

    cache_key = (text, model, api_url)
    cached = _EMBED_CACHE.get(cache_key)
    if cached is not None:
        return _clip_or_pad(cached, dim)

    payload = {"model": model, "input": text}
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    req = request.Request(url=api_url, data=body, headers=headers, method="POST")

    try:
        with request.urlopen(req, timeout=float(timeout)) as resp:
            raw = resp.read().decode("utf-8")
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            return _fallback_embed(text, dim)

        emb = _extract_embedding(parsed)
        if not emb:
            return _fallback_embed(text, dim)

        _EMBED_CACHE[cache_key] = emb
        return _clip_or_pad(emb, dim)
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return _fallback_embed(text, dim)
