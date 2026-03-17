import shutil
import time
import uuid
import logging
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
logger = logging.getLogger("berry_mrag.api")


def _process_diagnosis(
    request_id: str,
    query: str,
    image_path: Optional[str] = None,
    crop: Optional[str] = None,
    disease_hint: Optional[str] = None,
) -> DiagnoseResponse:
    started = time.perf_counter()
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
    reranked = rerank(
        retrieved,
        pest_type=str(detection["pest_type"]),
        crop=crop,
        disease_hint=effective_hint,
    )
    answer = generate_markdown_report(query, detection, reranked)

    resp = DiagnoseResponse(
        detection=detection,  # type: ignore[arg-type]
        retrieved=reranked,  # type: ignore[arg-type]
        answer_markdown=answer,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    logger.info(
        "diagnose_ok request_id=%s elapsed_ms=%.2f pest_type=%s retrieved=%d crop=%s hint=%s",
        request_id,
        elapsed_ms,
        detection.get("pest_type"),
        len(reranked),
        crop or "",
        effective_hint,
    )
    return resp


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(req: DiagnoseRequest) -> DiagnoseResponse:
    request_id = uuid.uuid4().hex[:12]
    logger.info("diagnose_start request_id=%s source=json", request_id)
    try:
        return _process_diagnosis(
            request_id=request_id,
            query=req.query,
            image_path=req.image_path,
            crop=req.crop,
            disease_hint=req.disease_hint,
        )
    except Exception:
        logger.exception("diagnose_failed request_id=%s source=json", request_id)
        raise


@router.post("/diagnose/upload", response_model=DiagnoseResponse)
async def diagnose_upload(
    query: str = Form(...),
    file: Optional[UploadFile] = File(None),
    crop: Optional[str] = Form(None),
    disease_hint: Optional[str] = Form(None),
) -> DiagnoseResponse:
    request_id = uuid.uuid4().hex[:12]
    logger.info("diagnose_start request_id=%s source=upload", request_id)
    image_path = None
    if file:
        save_dir = Path("data/raw")
        save_dir.mkdir(parents=True, exist_ok=True)
        image_path = str(save_dir / file.filename) if file.filename else None
        if image_path:
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

    try:
        return _process_diagnosis(
            request_id=request_id,
            query=query,
            image_path=image_path,
            crop=crop,
            disease_hint=disease_hint,
        )
    except Exception:
        logger.exception("diagnose_failed request_id=%s source=upload", request_id)
        raise
