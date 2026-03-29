# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Summary

Berry-MRAG-System（面向浆果种植的多模态RAG系统）— a multi-modal Retrieval-Augmented Generation system for berry crop disease/pest diagnosis. Follows a **Perception → Cognition → Generation** pipeline: YOLOv8 visual detection → embedding + FAISS retrieval + reranking → Gemini/template report generation.

## Commands

### Backend
```bash
# Start dev server
uvicorn backend.main:app --reload --port 8000

# Run all tests
pytest tests/

# Run a single test file
pytest tests/test_retriever_filters.py -v

# Build RAG chunks from knowledge base
python -m rag_module.build_chunks --input docs/berry_manual.md --output data/chunks/berry_manual_chunks.jsonl

# Offline RAG evaluation
python -m rag_module.eval_retrieval --eval-file docs/eval_queries.expanded.jsonl --top-k 3 --mode both --use-rerank --out-md docs/eval_report.md

# YOLO training
python -m visual_module.train_yolo --data data/processed/berry_yolo_data.yaml --model yolov8n.pt --epochs 100 --batch 16
```

### Frontend
```bash
cd frontend
npm run dev      # Vite dev server with HMR
npm run build    # TypeScript compile + Vite production build
npm run lint     # ESLint
npm run preview  # Preview production build
```

## Architecture

### Pipeline flow (single diagnosis request)
```
POST /api/diagnose/upload
  → visual_module/inference.py   (YOLOv8 → pest_type, confidence, bbox)
  → rag_module/embedder.py       (DashScope text-embedding-v4 → query vector)
  → rag_module/retriever.py      (FAISS cosine search over chunks → top-K)
  → rag_module/reranker.py       (rule-based score boost by crop/disease match)
  → rag_module/mllm_generator.py (Gemini API → markdown report; template fallback)
  → JSON response {detection, retrieved, answer_markdown}
```

### Backend (Python / FastAPI)
- `backend/main.py` — FastAPI app init, CORS middleware
- `backend/api_routes.py` — `/api/health`, `/api/diagnose`, `/api/diagnose/upload`; orchestrates the full pipeline in `_process_diagnosis()`
- `backend/schemas.py` — Pydantic v2 request/response models
- `backend/config.py` — `Settings` dataclass loaded from `.env` via `python-dotenv`

### Visual Module
- `visual_module/inference.py` — `run_inference()`: tries real YOLO, falls back to filename guessing. Normalizes labels against a business whitelist (powdery_mildew, aphid, gray_mold). Applies business confidence threshold.

### RAG Module
- `rag_module/embedder.py` — `embed_text()`: calls DashScope (OpenAI-compatible), falls back to SHA256 hash-based embedding
- `rag_module/retriever.py` — `search()`: loads chunks from `data/chunks/` (JSON/JSONL) + `docs/berry_manual.md` + built-in defaults. Builds FAISS index with vector caching. Supports crop/disease filtering.
- `rag_module/reranker.py` — `rerank()`: rule-based score adjustments (+0.08 disease match, +0.05 crop match)
- `rag_module/mllm_generator.py` — `generate_markdown_report()`: Gemini via OpenAI-compatible client, template fallback

### Frontend (React 19 + TypeScript + Vite 8)
- `frontend/src/App.tsx` — single-page app: image upload, query input, API call, result display with markdown rendering, PDF export (html2canvas + jsPDF)

## Key Design Decisions

- **Graceful degradation everywhere**: each module has fallbacks (YOLO → filename guess, DashScope → hash embedding, Gemini → template). The system always returns a response.
- **OpenAI-compatible clients**: both DashScope embedding and Gemini generation use the `openai` Python SDK with custom `base_url`.
- **Environment-driven config**: all model paths, API keys, thresholds, and provider selection via `.env` (see `.env.example`). The `Settings` dataclass in `backend/config.py` is the single source of truth.
- **RAG chunks as JSONL**: each chunk has `id`, `title`, `content`, `crop`, `disease_en` fields. Stored in `data/chunks/`.

## Environment Setup

Copy `.env.example` to `.env` and fill in:
- `DASHSCOPE_API_KEY` — required for real embeddings (Aliyun)
- `GEMINI_API_KEY` — required for LLM report generation
- `GEMINI_PROXY` — optional, for network proxy
- `YOLO_MODEL_PATH` — defaults to `yolov8n.pt` (pretrained nano model in repo root)
- `GEN_PROVIDER` — `gemini` or `template`

Python deps: `pip install -r requirements.txt` (dev: `pip install -r requirements-dev.txt`)
Frontend deps: `cd frontend && npm install`
