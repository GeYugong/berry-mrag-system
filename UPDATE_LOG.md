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
