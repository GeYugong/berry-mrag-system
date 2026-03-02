from typing import Dict, List, Union


def rerank(
    items: List[Dict[str, Union[str, float]]], pest_type: str
) -> List[Dict[str, Union[str, float]]]:
    boosted: List[Dict[str, Union[str, float]]] = []
    pest_hint = pest_type.replace("_", "")
    for item in items:
        title = str(item["title"]).replace(" ", "").lower()
        boost = 0.08 if pest_hint and pest_hint[:2] in title else 0.0
        boosted.append({**item, "score": round(float(item["score"]) + boost, 4)})

    boosted.sort(key=lambda x: x["score"], reverse=True)
    return boosted
