import hashlib
from typing import List


def embed_text(text: str, dim: int = 16) -> List[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = []
    for i in range(dim):
        byte_val = digest[i]
        values.append((byte_val / 255.0) * 2 - 1)
    return values
