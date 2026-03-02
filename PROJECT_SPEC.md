# Project Context for AI Agent: Berry-MRAG-System

> **Note to Agent**: This document serves as the primary system architecture and context reference for the "面向浆果种植的多模态RAG系统" (Multi-modal RAG System for Berry Planting) project. When generating code, suggesting completions, or refactoring, strictly adhere to the architecture, data flows, and technology stack defined below.

## 1. Project Overview
The objective is to build a multi-modal Retrieval-Augmented Generation (RAG) system that utilizes text, image, and video data to provide precise and efficient intelligent decision support for berry planting. The system will help farmers obtain knowledge, reduce risks, and improve yield and quality.

## 2. System Architecture
The system follows a "Perception - Cognition - Generation" (感知 - 认知 - 生成) hybrid AI workflow.

### 2.1 Core Modules
1. **Multi-modal Knowledge Base (多模态知识库)**: 
   * **Data Sources**: High-resolution images, video clips, scientific papers, control manuals, and structured tabular data (e.g., pesticide dosages, safety intervals).
   * **Processing**: Strict cleaning, filtering, and standardization. Text is parsed and split into vectorizable "chunks". Image processing requires high standards, including scale calibration, color consistency checks, and precise segmentation using Python and OpenCV to ensure dataset quality for model training.
2. **High-Precision Visual Diagnosis (高精度视觉诊断模块 - Stage 1)**:
   * **Model**: Fine-tuned YOLOv8.
   * **Input**: User-uploaded images of berry plants.
   * **Output**: Disease/pest category labels, confidence scores, and bounding box coordinates.
3. **Multi-modal RAG (多模态检索增强生成模块 - Stage 2)**:
   * **Embedding**: Uses models like CLIP to encode text chunks, images, and video keyframes into high-dimensional vectors.
   * **Vector DB**: Stores vectors for efficient similarity search.
   * **Retrieval**: Uses the visual diagnosis result as a precise query to perform vector similarity search, recalling the Top-K relevant multi-modal knowledge blocks.
   * **Reranking**: A secondary sorting model filters the initial recall results to ensure core accuracy.
   * **Generation**: The filtered context and original query are packaged as a Prompt for a Multi-modal Large Language Model (MLLM, e.g., LLaVA) to generate comprehensive, text-and-image solutions.
4. **System Integration & UI (系统集成与用户界面)**:
   * **Backend**: APIs encapsulating the AI modules.
   * **Frontend**: A clean Web application (and future App) for image upload and report display.

## 3. Technology Stack (Enforce these in code generation)
* **Computer Vision / Image Processing**: Python, OpenCV, Ultralytics (YOLOv8).
* **Multi-modal Embeddings / MLLM**: HuggingFace Transformers, CLIP, LLaVA.
* **Vector Database**: FAISS or Milvus.
* **Backend Framework**: FastAPI (Recommended for async AI API wrapping) or Flask.
* **Knowledge Management**: Markdown-based knowledge base architecture, synchronized via Git.

## 4. Expected Directory Structure
AI should use this structure to resolve relative imports and file paths:

```text
berry-mrag-system/
├── data/
│   ├── raw/                 # Unprocessed images, PDFs, videos
│   ├── processed/           # OpenCV-processed images, cleaned text
│   ├── chunks/              # Text chunks ready for embedding
│   └── vector_store/        # FAISS index or Milvus config
├── docs/                    # System documentation and Obsidian Markdown notes
├── visual_module/
│   └── inference.py         # YOLOv8 inference returning labels and boxes
├── rag_module/
│   ├── embedder.py          # CLIP encoding logic
│   ├── retriever.py         # FAISS/Milvus Top-K search logic
│   ├── reranker.py          # Secondary sorting logic
│   └── mllm_generator.py    # LLaVA prompt building and generation
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── api_routes.py        # Endpoints for frontend integration
│   ├── schemas.py           # Request/response data models
│   └── config.py            # App runtime settings
├── frontend/                # Web UI components
├── requirements.txt
└── PROJECT_SPEC.md          # This file

```

## 5. Data Flow execution (Example: User uploads an image)

1. **Frontend**: Sends image to `backend/api_routes.py`.
2. **Backend -> Visual Module**: Image is passed to `visual_module/inference.py` (YOLOv8). Returns `{"pest_type": "powdery_mildew", "confidence": 0.92, "bbox": [...]}`.


3. **Backend -> RAG Module**:
* The visual output is formatted into a query string.


* 
`rag_module/embedder.py` vectorizes the query.


* 
`rag_module/retriever.py` queries the Vector DB for Top-K relevant knowledge.


* 
`rag_module/reranker.py` sorts the Top-K results.


* 
`rag_module/mllm_generator.py` constructs a prompt with the Top results and sends it to the MLLM.




4. 
**Backend -> Frontend**: MLLM generates the final structured report (pesticide recommendation, dosage, alternative methods) and sends it back to the UI.

## 6. Update Log Policy (Mandatory)

All implementation updates completed by agent must be recorded in a persistent changelog file.

- **Changelog file**: `UPDATE_LOG.md` at repository root.
- **Author requirement**: each entry must explicitly state it was written by **who**.
- **Append-only rule**: new updates must be appended; do **not** overwrite, delete, or rewrite previous entries.
- **Entry content requirement**: each update entry should include at least:
  - date/time
  - executor
  - summary of changes
  - touched files/modules
  - validation/test results
  - known issues or follow-up items
  - next-step task for the following update cycle

When agent finishes a coding change, updating `UPDATE_LOG.md` is part of the definition of done.



