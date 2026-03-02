from typing import List, Optional

from pydantic import BaseModel, Field


class DiagnoseRequest(BaseModel):
    query: str = Field(..., description="用户文本问题")
    image_path: Optional[str] = Field(
        default=None, description="本地图片路径（演示阶段使用）"
    )


class DetectionResult(BaseModel):
    pest_type: str
    confidence: float
    bbox: List[int]


class RetrievalItem(BaseModel):
    id: str
    title: str
    content: str
    score: float


class DiagnoseResponse(BaseModel):
    detection: DetectionResult
    retrieved: List[RetrievalItem]
    answer_markdown: str
