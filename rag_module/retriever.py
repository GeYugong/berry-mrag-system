import math
from typing import Dict, List, Union

from rag_module.embedder import embed_text


KNOWLEDGE_BASE: List[Dict[str, str]] = [
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


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def search(
    query_vector: List[float],
    top_k: int = 3,
    embedding_enabled: bool = True,
    embedding_model: str = "qwen3-vl-embedding",
    embedding_api_url: str = "",
    embedding_api_key: str = "",
    embedding_timeout: float = 20.0,
) -> List[Dict[str, Union[str, float]]]:
    scored: List[Dict[str, Union[str, float]]] = []
    for item in KNOWLEDGE_BASE:
        item_vec = embed_text(
            item["title"] + item["content"],
            dim=len(query_vector),
            enabled=embedding_enabled,
            model=embedding_model,
            api_url=embedding_api_url or None,
            api_key=embedding_api_key or None,
            timeout=embedding_timeout,
        )
        score = _cosine_similarity(query_vector, item_vec)
        scored.append({**item, "score": round(score, 4)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
