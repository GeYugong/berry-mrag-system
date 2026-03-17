from typing import Dict, List, Optional

_DISEASE_ALIASES = {
    "powdery mildew": "powdery_mildew",
    "powdery-mildew": "powdery_mildew",
    "gray mold": "gray_mold",
    "grey mold": "gray_mold",
    "grey_mold": "gray_mold",
    "botrytis": "gray_mold",
}


def _norm(s: str) -> str:
    return s.strip().lower().replace("-", "_")


def _norm_disease(s: Optional[str]) -> str:
    if not s:
        return ""
    key = _norm(s)
    return _DISEASE_ALIASES.get(key, key)


def rerank(
    items: List[Dict[str, object]],
    pest_type: str,
    crop: Optional[str] = None,
    disease_hint: Optional[str] = None,
) -> List[Dict[str, object]]:
    boosted: List[Dict[str, object]] = []
    disease_q = _norm_disease(disease_hint or pest_type)
    crop_q = _norm(crop or "")

    for item in items:
        title = _norm(str(item.get("title", "")))
        content = _norm(str(item.get("content", "")))
        item_crop = _norm(str(item.get("crop", "")))
        item_disease = _norm_disease(str(item.get("disease_en", "")))
        keywords = " ".join(_norm(str(x)) for x in item.get("keywords", [])) if isinstance(item.get("keywords"), list) else ""

        boost = 0.0
        if disease_q and disease_q != "unknown_leaf_issue":
            if disease_q in item_disease:
                boost += 0.20
            if disease_q in title or disease_q in keywords:
                boost += 0.15
            if disease_q in content:
                boost += 0.05

        if crop_q:
            if crop_q in item_crop or crop_q in title or crop_q in keywords:
                boost += 0.10

        if str(item.get("dose", "")).strip():
            boost += 0.02
        if str(item.get("interval_days", "")).strip():
            boost += 0.02

        boosted.append({**item, "score": round(float(item["score"]) + boost, 4)})

    boosted.sort(key=lambda x: float(x["score"]), reverse=True)
    return boosted
