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
    query_vector = embed_text(query_text)
    retrieved = search(query_vector, top_k=settings.top_k)
    reranked = rerank(retrieved, pest_type=str(detection["pest_type"]))
    answer = generate_markdown_report(req.query, detection, reranked)

    return DiagnoseResponse(
        detection=detection,  # type: ignore[arg-type]
        retrieved=reranked,  # type: ignore[arg-type]
        answer_markdown=answer,
    )
