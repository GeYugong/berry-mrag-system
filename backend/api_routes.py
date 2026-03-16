import shutil
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from backend.config import settings
from backend.schemas import DiagnoseRequest, DiagnoseResponse
from rag_module.embedder import embed_text
from rag_module.mllm_generator import generate_markdown_report
from rag_module.reranker import rerank
from rag_module.retriever import search
from visual_module.inference import run_inference

router = APIRouter(prefix="/api", tags=["berry-mrag"])


def _process_diagnosis(
    query: str,
    image_path: Optional[str] = None,
    crop: Optional[str] = None,
    disease_hint: Optional[str] = None,
) -> DiagnoseResponse:
    detection = run_inference(
        image_path,
        model_path=settings.yolo_model_path,
        device=settings.yolo_device,
        conf=settings.yolo_conf,
        iou=settings.yolo_iou,
        business_conf=settings.yolo_business_conf,
    )
    query_text = f"{query} {detection['pest_type']}"
    query_vector = embed_text(query_text)
    effective_hint = disease_hint or str(detection["pest_type"])
    retrieved = search(
        query_vector,
        top_k=settings.top_k,
        crop=crop,
        disease_hint=effective_hint,
    )
    reranked = rerank(retrieved, pest_type=str(detection["pest_type"]))
    answer = generate_markdown_report(query, detection, reranked)

    return DiagnoseResponse(
        detection=detection,  # type: ignore[arg-type]
        retrieved=reranked,  # type: ignore[arg-type]
        answer_markdown=answer,
    )


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(req: DiagnoseRequest) -> DiagnoseResponse:
    return _process_diagnosis(req.query, req.image_path, req.crop, req.disease_hint)


@router.post("/diagnose/upload", response_model=DiagnoseResponse)
async def diagnose_upload(
    query: str = Form(...),
    file: Optional[UploadFile] = File(None),
    crop: Optional[str] = Form(None),
    disease_hint: Optional[str] = Form(None),
) -> DiagnoseResponse:
    image_path = None
    if file:
        save_dir = Path("data/raw")
        save_dir.mkdir(parents=True, exist_ok=True)
        image_path = str(save_dir / file.filename) if file.filename else None
        if image_path:
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

    return _process_diagnosis(query, image_path, crop, disease_hint)
