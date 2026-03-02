from pathlib import Path
from typing import Dict, List, Optional, Union


def _guess_pest_from_name(file_name: str) -> str:
    name = file_name.lower()
    if "powder" in name or "白粉" in name:
        return "powdery_mildew"
    if "aphid" in name or "蚜" in name:
        return "aphid"
    if "gray" in name or "灰霉" in name:
        return "gray_mold"
    return "unknown_leaf_issue"


def run_inference(
    image_path: Optional[str],
) -> Dict[str, Union[str, float, List[int]]]:
    if not image_path:
        return {
            "pest_type": "unknown_leaf_issue",
            "confidence": 0.51,
            "bbox": [0, 0, 100, 100],
        }

    file_name = Path(image_path).name
    pest_type = _guess_pest_from_name(file_name)
    confidence = 0.88 if pest_type != "unknown_leaf_issue" else 0.63

    return {
        "pest_type": pest_type,
        "confidence": confidence,
        "bbox": [42, 56, 260, 300],
    }
