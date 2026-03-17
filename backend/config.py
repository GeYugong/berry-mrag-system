import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "berry-mrag-backend")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    top_k: int = int(os.getenv("TOP_K", "3"))
    yolo_model_path: str = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")
    yolo_device: str = os.getenv("YOLO_DEVICE", "cpu")
    yolo_conf: float = float(os.getenv("YOLO_CONF", "0.25"))
    yolo_iou: float = float(os.getenv("YOLO_IOU", "0.45"))
    yolo_business_conf: float = float(os.getenv("YOLO_BUSINESS_CONF", "0.45"))
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")
    embedding_dim: int = int(os.getenv("EMBEDDING_DIM", "1024"))
    gen_provider: str = os.getenv("GEN_PROVIDER", "template")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.0-flash")


settings = Settings()
