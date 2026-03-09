# 更新日志（Codex）

说明：
- 本文件由 Codex 维护。
- 每次更新必须追加新记录，不覆盖历史记录。
- 记录包含：时间、执行者、更新内容、验证结果、已知问题。

---

## 2026-03-02 第 1 次更新

- 执行者：Codex
- 更新类型：项目初始化骨架实现（MVP）

### 更新内容
1. 新增后端基础框架（FastAPI）
   - 新增 `backend/main.py`（应用入口）
   - 新增 `backend/api_routes.py`（`/api/health`、`/api/diagnose`）
   - 新增 `backend/config.py`（应用配置）
   - 新增 `backend/schemas.py`（请求/响应数据模型）

2. 新增视觉模块占位推理
   - 新增 `visual_module/inference.py`
   - 支持根据图片文件名关键词做规则化病虫害判断（占位逻辑）

3. 新增 RAG 模块骨架
   - 新增 `rag_module/embedder.py`（哈希向量占位）
   - 新增 `rag_module/retriever.py`（内置知识库 + 相似度检索）
   - 新增 `rag_module/reranker.py`（重排占位）
   - 新增 `rag_module/mllm_generator.py`（Markdown 诊断报告生成）

4. 工程与文档更新
   - 更新 `requirements.txt`（`fastapi`、`uvicorn`、`pydantic`）
   - 更新 `README.md`，补充当前 MVP 启动与调用说明
   - 新增包标识文件：`backend/__init__.py`、`rag_module/__init__.py`、`visual_module/__init__.py`
   - 新建数据目录：`data/raw`、`data/processed`、`data/chunks`、`data/vector_store`

5. 兼容性修复
   - 将 `|` 联合类型改为 `typing.Optional/Union` 写法，兼容 Python 3.8+

### 验证结果
- `python -m compileall backend rag_module visual_module`：通过
- 模块级联调（视觉 -> 检索 -> 重排 -> 生成）：通过

### 已知问题
- 当前环境 `pip install -r requirements.txt` 受代理/网络限制，`fastapi` 无法下载，未完成 `uvicorn` 运行级验证。

---

## 2026-03-02 第 2 次更新

- 执行者：Codex
- 更新类型：文档一致性检查与修复

### 更新内容
1. 修复 `README.md` 中错误引用
   - 将不存在的 `backend/.env.example` 引用改为现状说明，避免误导。
   - 同步修正“项目结构”目录树，改为当前真实目录与 `data` 子目录。

2. 修复 `PROJECT_SPEC.md` 中目录结构错误
   - 将末尾文件 `AI_CONTEXT.md` 更正为 `PROJECT_SPEC.md`。
   - 将 `backend/` 结构补齐为实际存在的 `schemas.py` 与 `config.py`。
   - 删除当前仓库未落地的 `visual_module/preprocessor.py`、`visual_module/train_yolo.py` 误导项（可后续新增时再补回）。

3. 重写 `DEV_NOTES.md` 为“当前已落地结构”
   - 移除与现仓库冲突的 `src/`、`frontend_app/`、`backend_api/` 等旧路径描述。
   - 统一为当前真实目录：`backend/`、`visual_module/`、`rag_module/`、`data/{raw,processed,chunks,vector_store}`。
   - 保留模块职责与 API 说明，明确本文件描述的是已落地状态。

### 验证结果
- 全文检索确认以下错误引用已清除：
  - `backend/.env.example`
  - `AI_CONTEXT.md`
  - `src/vision_module`
  - `src/rag_module`
  - `src/backend_api`
  - `frontend_app`

### 已知问题
- `requirements.txt` 中依赖安装仍受当前环境网络/代理限制影响，运行级验证需在可联网环境完成。

### 下一步任务
1. 在 `UPDATE_LOG.md` 的后续每条记录中固定增加“下一步任务”小节并保持可执行、可验证。

---

## 2026-03-02 第 3 次更新

- 执行者：Codex
- 更新类型：规范调整（更新日志约定）

### 更新内容
1. 更新 `PROJECT_SPEC.md` 中 `Update Log Policy`：
   - 在“Entry content requirement”中新增强制项：`next-step task for the following update cycle`。
   - 要求每次更新日志都必须包含下一步任务说明。

### 涉及文件/模块
- `PROJECT_SPEC.md`
- `UPDATE_LOG.md`

### 验证结果
- 文档内容检查通过：`PROJECT_SPEC.md` 已包含“next-step task”要求。
- 本次日志记录已按新规范写入“下一步任务”。

### 已知问题
- 暂无新增问题。

### 下一步任务
1. 后续代码变更完成后，继续按新规范记录日志并明确下一次可执行任务。

---

## 2026-03-02 第 4 次更新

- 执行者：Codex
- 更新类型：环境依赖安装与运行级接口验证

### 更新内容
1. 在当前终端会话配置代理并安装依赖：
   - `HTTP_PROXY=http://127.0.0.1:7897`
   - `HTTPS_PROXY=http://127.0.0.1:7897`
   - 执行 `pip install -r requirements.txt` 成功安装 `fastapi/uvicorn/pydantic` 及依赖。
2. 完成真实 HTTP 运行级验证：
   - 通过 Python 子进程启动 `uvicorn backend.main:app`。
   - 调用 `GET /api/health` 与 `POST /api/diagnose` 验证成功。
   - 诊断链路返回 `powdery_mildew` 检测结果与检索列表。

### 涉及文件/模块
- 无代码文件改动（本次为环境与运行验证）
- 日志文件：`UPDATE_LOG.md`

### 验证结果
- 依赖安装：成功。
- 接口验证：成功。
  - `/api/health` 返回 `status=ok`
  - `/api/diagnose` 返回诊断结果与 3 条检索结果

### 已知问题
- 当前测试为占位逻辑，尚未接入真实 YOLOv8、FAISS/Milvus、MLLM。

### 下一步任务
1. 将 `rag_module/retriever.py` 从内置知识库升级为基于本地 `data/chunks` 的可持久化检索实现（优先 FAISS）。

---

## 2026-03-02 第 5 次更新

- 执行者：Codex
- 更新类型：开发清单完善（To-Do）

### 更新内容
1. 在 `DEV_NOTES.md` 新增“完整 To-Do List（执行清单）”章节。
2. To-Do 按优先级与模块拆分，覆盖：
   - P0 主链路打通
   - 数据工程
   - YOLO 专项（重点，含训练/评估/推理/性能）
   - RAG 专项
   - 后端工程化
   - 前端交互
   - 质量与交付
3. 补充“下一次开发建议（短期）”，便于直接进入执行。

### 涉及文件/模块
- `DEV_NOTES.md`
- `UPDATE_LOG.md`

### 验证结果
- 文档更新完成，`DEV_NOTES.md` 已包含完整 To-Do 清单。
- 清单与当前仓库结构保持一致，未引入不存在的路径引用。

### 已知问题
- To-Do 中多项能力依赖真实数据与模型资源，当前仍为占位实现阶段。

### 下一步任务
1. 开始执行 To-Do 的第一项工程任务：新增 `visual_module/train_yolo.py` 并接入真实 YOLO 推理流程。

---

## 2026-03-09 第 6 次更新

- 执行者：Codex
- 更新类型：接入 YOLOv8 推理（含降级兜底）

### 更新内容
1. 升级视觉推理模块，新增真实 YOLOv8 推理路径：
   - `visual_module/inference.py` 支持通过 `model_path/conf_threshold/iou_threshold` 参数执行 `ultralytics.YOLO.predict`。
   - 统一输出结构仍为 `pest_type/confidence/bbox`，保持 `POST /api/diagnose` 协议不变。
   - 新增模型对象缓存，避免重复加载权重。
2. 增加健壮性与降级策略：
   - 权重未配置、权重文件不存在、依赖缺失、推理异常等场景会自动降级到原占位规则推理，保证接口可用。
   - 图片不存在时记录 warning 并降级处理。
3. 后端配置与路由联动：
   - `backend/config.py` 新增 `YOLO_WEIGHTS_PATH`、`YOLO_CONF_THRESHOLD`、`YOLO_IOU_THRESHOLD` 配置项。
   - `backend/api_routes.py` 在调用 `run_inference` 时传入上述配置。
4. 依赖更新：
   - `requirements.txt` 新增 `ultralytics>=8.3,<9.0`。

### 涉及文件/模块
- `visual_module/inference.py`
- `backend/config.py`
- `backend/api_routes.py`
- `requirements.txt`
- `UPDATE_LOG.md`

### 验证结果
- 语法级验证：使用 `compile(source, file, "exec")` 对 `backend/config.py`、`backend/api_routes.py`、`visual_module/inference.py` 进行无落盘编译检查，结果通过。
- 接口协议检查：`/api/diagnose` 返回字段未变更（`detection/retrieved/answer_markdown`）。

### 已知问题
- 当前仓库尚未提供实际 YOLO 权重文件；未配置 `YOLO_WEIGHTS_PATH` 时会走降级逻辑。
- 未执行真实模型运行级验证（需本地存在可用权重并安装对应推理依赖）。

### 下一步任务
1. 新增 `.env.example` 并补充 YOLO 配置项示例。
2. 准备一份可用权重与测试图片，完成 `/api/diagnose` 的真实推理回归测试。

---

## 2026-03-09 第 7 次更新

- 执行者：Codex
- 更新类型：视觉推理改为 API 模式（支持本地兜底）

### 更新内容
1. 新增 API 推理配置项：
   - `backend/config.py` 增加 `YOLO_MODE`、`YOLO_API_URL`、`YOLO_API_TOKEN`、`YOLO_API_TIMEOUT`。
2. 路由接线调整：
   - `backend/api_routes.py` 调用 `run_inference` 时传入 API 模式与相关参数。
3. 视觉推理逻辑升级：
   - `visual_module/inference.py` 新增 YOLO API 调用逻辑（HTTP POST JSON）。
   - 默认 `mode=api`，当 API 成功时直接使用 API 返回结果。
   - 支持多种响应字段解析（`pest_type/label/class_name/class`、`bbox/xyxy/x1y1x2y2`）。
   - 当 API 未配置、请求失败、响应非法时自动降级到占位规则推理。
   - 保留 `mode=local` 本地权重推理路径作为兜底能力。

### 涉及文件/模块
- `backend/config.py`
- `backend/api_routes.py`
- `visual_module/inference.py`
- `UPDATE_LOG.md`

### 验证结果
- 语法级验证：使用 `compile(source, file, "exec")` 对改动文件进行无落盘编译检查，结果通过。
- 接口协议检查：`/api/diagnose` 返回字段保持不变（`detection/retrieved/answer_markdown`）。

### 已知问题
- 当前未内置 YOLO 远程服务端实现；需外部 API 按约定返回检测结果。
- API 返回字段若与约定差异过大，可能触发降级逻辑。

### 下一步任务
1. 新增 `.env.example`，明确 API 模式必填配置与示例。
2. 增加一个本地 mock YOLO API 用于端到端回归测试。

---

## 2026-03-09 第 8 次更新

- 执行者：Codex
- 更新类型：YOLO API 接入增强（支持传输图片内容）

### 更新内容
1. 新增 API 传图配置：
   - `backend/config.py` 新增 `YOLO_API_SEND_IMAGE_BASE64`（默认 true）。
   - `backend/config.py` 新增 `YOLO_API_INCLUDE_IMAGE_PATH`（默认 true）。
2. 路由参数透传：
   - `backend/api_routes.py` 调用 `run_inference` 时传入上述两个开关。
3. API 请求体增强：
   - `visual_module/inference.py` 的 `_api_inference` 支持在请求中携带 `image_base64` 与 `file_name`。
   - 可按开关决定是否同时携带 `image_path`，兼容同机/跨机部署两种 YOLO API。
   - 维持现有响应解析与降级策略不变。

### 涉及文件/模块
- `backend/config.py`
- `backend/api_routes.py`
- `visual_module/inference.py`
- `UPDATE_LOG.md`

### 验证结果
- 语法级验证：使用 `compile(source, file, "exec")` 对改动文件进行无落盘编译检查，结果通过。
- 协议检查：`/api/diagnose` 输出结构未变。

### 已知问题
- `image_base64` 会增大请求体，超大图片建议在调用前压缩。
- YOLO API 需实现对应字段解析（`image_base64`/`file_name`）。

### 下一步任务
1. 新增 `.env.example` 并写入 API 传图开关说明。
2. 提供一个最小 YOLO API mock 示例，便于快速联调。

---

## 2026-03-09 第 9 次更新

- 执行者：Codex
- 更新类型：接入外部 Embedding 与 LLM API（Qwen + Gemini）

### 更新内容
1. 新增全局配置项（`backend/config.py`）：
   - Embedding：`EMBEDDING_ENABLED`、`EMBEDDING_MODEL`、`EMBEDDING_API_URL`、`EMBEDDING_API_KEY`、`EMBEDDING_API_TIMEOUT`。
   - LLM：`LLM_ENABLED`、`LLM_MODEL`、`LLM_API_KEY`、`LLM_API_URL`、`LLM_API_TIMEOUT`、`LLM_TEMPERATURE`。
2. 接入阿里 Embedding API（`rag_module/embedder.py`）：
   - 新增 HTTP 调用逻辑（OpenAI-compatible 响应优先，兼容 DashScope `output.embeddings` 结构）。
   - 新增内存缓存，减少重复文本的 API 调用。
   - 未配置 key/url 或 API 异常时自动回退到哈希向量占位逻辑。
3. 检索链路接线（`rag_module/retriever.py` + `backend/api_routes.py`）：
   - `search` 新增 embedding 参数透传，使 query 与知识条目向量使用同一模型配置。
4. 接入 Gemini 生成（`rag_module/mllm_generator.py`）：
   - 新增 Gemini `generateContent` 调用逻辑。
   - 构造结构化 Prompt（诊断结论、处置步骤、用药与安全、复查计划、依据引用）。
   - API 异常或未配置 key 时自动回退模板生成。

### 涉及文件/模块
- `backend/config.py`
- `backend/api_routes.py`
- `rag_module/embedder.py`
- `rag_module/retriever.py`
- `rag_module/mllm_generator.py`
- `UPDATE_LOG.md`

### 验证结果
- 语法级验证：对上述 Python 文件执行无落盘编译检查，通过。
- 最小链路验证：在无 API key 场景调用 `diagnose`，服务可返回结果（走兜底逻辑）。

### 已知问题
- 当前知识库仍为内置 3 条样例，外部 embedding/LLM 接入后效果受语料规模限制明显。
- 若设置 `EMBEDDING_MODEL=qwen3-vl-embedding`，需确保你的 DashScope 账号已开通该模型权限。

### 下一步任务
1. 新增 `.env.example` 并补充 Qwen/Gemini 配置模板。
2. 增加 API 连通性与响应结构校验日志，便于排障。
3. 将 `data/chunks` 落地并替换内置知识库，实现真实检索。
