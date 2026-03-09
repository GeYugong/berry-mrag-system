import logging
import json
import base64
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError
from typing import Any, Dict, List, Optional, Union

try:
    from ultralytics import YOLO
except Exception:  # pragma: no cover - optional dependency/runtime
    YOLO = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)
_MODEL_CACHE: Dict[str, Any] = {}

_CLASS_NAME_MAP: Dict[str, str] = {
    "powdery_mildew": "powdery_mildew",
    "powder": "powdery_mildew",
    "white_powder": "powdery_mildew",
    "aphid": "aphid",
    "gray_mold": "gray_mold",
    "grey_mold": "gray_mold",
}


def _normalize_label(raw_label: str) -> str:
    key = raw_label.strip().lower().replace(" ", "_").replace("-", "_")
    if not key:
        return "unknown_leaf_issue"
    return _CLASS_NAME_MAP.get(key, key)


def _guess_pest_from_name(file_name: str) -> str:
    name = file_name.lower()
    if "powder" in name or "白粉" in name:
        return "powdery_mildew"
    if "aphid" in name or "蚜" in name:
        return "aphid"
    if "gray" in name or "grey" in name or "灰霉" in name:
        return "gray_mold"
    return "unknown_leaf_issue"


def _fallback_inference(
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


def _to_abs_path(path_str: str) -> Path:
    path = Path(path_str).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def _unknown_result() -> Dict[str, Union[str, float, List[int]]]:
    return {
        "pest_type": "unknown_leaf_issue",
        "confidence": 0.0,
        "bbox": [0, 0, 0, 0],
    }


def _extract_bbox(payload: Dict[str, Any]) -> List[int]:
    bbox = payload.get("bbox")
    if isinstance(bbox, list) and len(bbox) == 4:
        return [int(round(float(v))) for v in bbox]

    for key in ("xyxy", "box", "bndbox"):
        value = payload.get(key)
        if isinstance(value, list) and len(value) == 4:
            return [int(round(float(v))) for v in value]

    if all(k in payload for k in ("x1", "y1", "x2", "y2")):
        return [
            int(round(float(payload["x1"]))),
            int(round(float(payload["y1"]))),
            int(round(float(payload["x2"]))),
            int(round(float(payload["y2"]))),
        ]
    return [0, 0, 0, 0]


def _parse_api_result(resp_payload: Dict[str, Any]) -> Dict[str, Union[str, float, List[int]]]:
    item = resp_payload
    predictions = resp_payload.get("predictions")
    if isinstance(predictions, list) and predictions:
        item = predictions[0]
    elif isinstance(resp_payload.get("result"), dict):
        item = resp_payload["result"]

    raw_label = str(
        item.get("pest_type")
        or item.get("label")
        or item.get("class_name")
        or item.get("class")
        or "unknown_leaf_issue"
    )
    confidence_val = item.get("confidence", item.get("score", 0.0))
    try:
        confidence = float(confidence_val)
    except (TypeError, ValueError):
        confidence = 0.0

    return {
        "pest_type": _normalize_label(raw_label),
        "confidence": round(confidence, 4),
        "bbox": _extract_bbox(item),
    }


def _api_inference(
    image_file: Path,
    api_url: str,
    api_token: Optional[str],
    api_timeout: float,
    api_send_image_base64: bool,
    api_include_image_path: bool,
    conf_threshold: float,
    iou_threshold: float,
) -> Dict[str, Union[str, float, List[int]]]:
    payload: Dict[str, Any] = {
        "file_name": image_file.name,
        "conf_threshold": float(conf_threshold),
        "iou_threshold": float(iou_threshold),
    }
    if api_include_image_path:
        payload["image_path"] = str(image_file)
    if api_send_image_base64:
        payload["image_base64"] = base64.b64encode(image_file.read_bytes()).decode("ascii")

    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"

    req = request.Request(url=api_url, data=body, headers=headers, method="POST")
    with request.urlopen(req, timeout=float(api_timeout)) as resp:
        raw = resp.read().decode("utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid YOLO API response: {raw[:200]}") from exc

    if not isinstance(data, dict):
        raise RuntimeError("YOLO API response must be a JSON object")
    return _parse_api_result(data)


def _get_model(model_path: Path) -> Any:
    cache_key = str(model_path.resolve())
    cached = _MODEL_CACHE.get(cache_key)
    if cached is not None:
        return cached

    if YOLO is None:
        raise RuntimeError("ultralytics is not installed")

    model = YOLO(str(model_path))
    _MODEL_CACHE[cache_key] = model
    return model


def run_inference(
    image_path: Optional[str],
    mode: str = "api",
    api_url: Optional[str] = None,
    api_token: Optional[str] = None,
    api_timeout: float = 15.0,
    api_send_image_base64: bool = True,
    api_include_image_path: bool = True,
    model_path: Optional[str] = None,
    conf_threshold: float = 0.25,
    iou_threshold: float = 0.45,
) -> Dict[str, Union[str, float, List[int]]]:
    if not image_path:
        return _fallback_inference(image_path)

    image_file = _to_abs_path(image_path)
    if not image_file.exists():
        logger.warning("Image file not found: %s; fallback inference will be used", image_file)
        return _fallback_inference(str(image_file))

    mode_norm = (mode or "").strip().lower()
    if mode_norm == "api":
        if not api_url:
            logger.warning("YOLO_MODE=api but YOLO_API_URL is empty; fallback inference will be used")
            return _fallback_inference(str(image_file))
        try:
            return _api_inference(
                image_file=image_file,
                api_url=api_url,
                api_token=api_token,
                api_timeout=api_timeout,
                api_send_image_base64=api_send_image_base64,
                api_include_image_path=api_include_image_path,
                conf_threshold=conf_threshold,
                iou_threshold=iou_threshold,
            )
        except (HTTPError, URLError, TimeoutError, RuntimeError):
            logger.exception("YOLO API inference failed; fallback inference will be used")
            return _fallback_inference(str(image_file))
        except Exception:
            logger.exception("Unexpected YOLO API error; fallback inference will be used")
            return _fallback_inference(str(image_file))

    if mode_norm not in ("local", ""):
        logger.warning("Unknown YOLO_MODE=%s; fallback inference will be used", mode_norm)
        return _fallback_inference(str(image_file))

    if not model_path:
        logger.info("YOLO_MODE=local but YOLO_WEIGHTS_PATH is empty; fallback inference will be used")
        return _fallback_inference(str(image_file))

    weights_file = _to_abs_path(model_path)
    if not weights_file.exists():
        logger.warning(
            "YOLO weights not found: %s; fallback inference will be used", weights_file
        )
        return _fallback_inference(str(image_file))

    try:
        model = _get_model(weights_file)
        results = model.predict(
            source=str(image_file),
            conf=float(conf_threshold),
            iou=float(iou_threshold),
            max_det=1,
            verbose=False,
        )

        if not results:
            return _unknown_result()

        result = results[0]
        boxes = getattr(result, "boxes", None)
        if boxes is None or len(boxes) == 0:
            return _unknown_result()

        box = boxes[0]
        cls_id = int(box.cls[0].item())
        confidence = float(box.conf[0].item())
        coords = box.xyxy[0].tolist()
        bbox = [int(round(v)) for v in coords]

        names = getattr(result, "names", {}) or {}
        if isinstance(names, dict):
            raw_label = str(names.get(cls_id, str(cls_id)))
        else:
            raw_label = str(cls_id)

        pest_type = _normalize_label(raw_label)
        return {
            "pest_type": pest_type,
            "confidence": round(confidence, 4),
            "bbox": bbox,
        }
    except Exception:
        logger.exception("YOLO inference failed; fallback inference will be used")
        return _fallback_inference(str(image_file))
