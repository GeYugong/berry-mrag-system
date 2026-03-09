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
    embedding_enabled: bool = _as_bool("EMBEDDING_ENABLED", "true")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "qwen3-vl-embedding").strip()
    embedding_api_url: str = os.getenv(
        "EMBEDDING_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings"
    ).strip()
    embedding_api_key: str = os.getenv(
        "EMBEDDING_API_KEY", os.getenv("DASHSCOPE_API_KEY", "")
    ).strip()
    embedding_timeout: float = float(os.getenv("EMBEDDING_API_TIMEOUT", "20"))
    llm_enabled: bool = _as_bool("LLM_ENABLED", "true")
    llm_model: str = os.getenv("LLM_MODEL", "gemini-2.0-flash").strip()
    llm_api_key: str = os.getenv("LLM_API_KEY", os.getenv("GEMINI_API_KEY", "")).strip()
    llm_api_url: str = os.getenv("LLM_API_URL", "").strip()
    llm_timeout: float = float(os.getenv("LLM_API_TIMEOUT", "30"))
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))


settings = Settings()
