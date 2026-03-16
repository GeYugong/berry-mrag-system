import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "berry-mrag-backend")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    top_k: int = int(os.getenv("TOP_K", "3"))
    yolo_model_path: str = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")
    yolo_device: str = os.getenv("YOLO_DEVICE", "cpu")
    yolo_conf: float = float(os.getenv("YOLO_CONF", "0.25"))
    yolo_iou: float = float(os.getenv("YOLO_IOU", "0.45"))


settings = Settings()
