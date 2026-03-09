from fastapi import APIRouter

from backend.config import settings
from backend.schemas import DiagnoseRequest, DiagnoseResponse
from rag_module.embedder import embed_text
from rag_module.mllm_generator import generate_markdown_report
from rag_module.reranker import rerank
from rag_module.retriever import search
from visual_module.inference import run_inference

router = APIRouter(prefix="/api", tags=["berry-mrag"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(req: DiagnoseRequest) -> DiagnoseResponse:
    detection = run_inference(
        req.image_path,
        mode=settings.yolo_mode,
        api_url=settings.yolo_api_url or None,
        api_token=settings.yolo_api_token or None,
        api_timeout=settings.yolo_api_timeout,
        api_send_image_base64=settings.yolo_api_send_image_base64,
        api_include_image_path=settings.yolo_api_include_image_path,
        model_path=settings.yolo_weights_path or None,
        conf_threshold=settings.yolo_conf_threshold,
        iou_threshold=settings.yolo_iou_threshold,
    )
    query_text = f"{req.query} {detection['pest_type']}"
    query_vector = embed_text(
        query_text,
        enabled=settings.embedding_enabled,
        model=settings.embedding_model,
        api_url=settings.embedding_api_url or None,
        api_key=settings.embedding_api_key or None,
        timeout=settings.embedding_timeout,
    )
    retrieved = search(
        query_vector,
        top_k=settings.top_k,
        embedding_enabled=settings.embedding_enabled,
        embedding_model=settings.embedding_model,
        embedding_api_url=settings.embedding_api_url,
        embedding_api_key=settings.embedding_api_key,
        embedding_timeout=settings.embedding_timeout,
    )
    reranked = rerank(retrieved, pest_type=str(detection["pest_type"]))
    answer = generate_markdown_report(
        req.query,
        detection,
        reranked,
        llm_enabled=settings.llm_enabled,
        llm_model=settings.llm_model,
        llm_api_key=settings.llm_api_key,
        llm_api_url=settings.llm_api_url,
        llm_timeout=settings.llm_timeout,
        llm_temperature=settings.llm_temperature,
    )

    return DiagnoseResponse(
        detection=detection,  # type: ignore[arg-type]
        retrieved=reranked,  # type: ignore[arg-type]
        answer_markdown=answer,
    )
