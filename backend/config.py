import os
from dataclasses import dataclass


def _as_bool(env_name: str, default: str = "false") -> bool:
    return os.getenv(env_name, default).strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "berry-mrag-backend")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    top_k: int = int(os.getenv("TOP_K", "3"))
    yolo_mode: str = os.getenv("YOLO_MODE", "api").strip().lower()
    yolo_api_url: str = os.getenv("YOLO_API_URL", "").strip()
    yolo_api_token: str = os.getenv("YOLO_API_TOKEN", "").strip()
    yolo_api_timeout: float = float(os.getenv("YOLO_API_TIMEOUT", "15"))
    yolo_api_send_image_base64: bool = _as_bool("YOLO_API_SEND_IMAGE_BASE64", "true")
    yolo_api_include_image_path: bool = _as_bool("YOLO_API_INCLUDE_IMAGE_PATH", "true")
    yolo_weights_path: str = os.getenv("YOLO_WEIGHTS_PATH", "").strip()
    yolo_conf_threshold: float = float(os.getenv("YOLO_CONF_THRESHOLD", "0.25"))
    yolo_iou_threshold: float = float(os.getenv("YOLO_IOU_THRESHOLD", "0.45"))


settings = Settings()
