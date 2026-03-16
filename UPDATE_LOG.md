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

## 2026-03-16 第 6 次更新

- 执行者：Codex
- 更新类型：YOLOv8 本地推理接入与配置文档补全

### 更新内容
1. 将视觉推理从纯占位逻辑升级为“YOLOv8 优先 + 占位回退”：
   - 更新 `visual_module/inference.py`，新增本地 YOLOv8 推理流程。
   - 支持从检测结果中提取最高置信度目标并返回 `pest_type/confidence/bbox`。
   - 当 `ultralytics` 不可用、模型推理失败或图片不存在时，自动回退到文件名关键词占位逻辑，保证接口可用性。

2. 新增后端 YOLO 配置项并接入诊断接口：
   - 更新 `backend/config.py`，新增 `YOLO_MODEL_PATH/YOLO_DEVICE/YOLO_CONF/YOLO_IOU`。
   - 更新 `backend/api_routes.py`，`/api/diagnose` 调用 `run_inference` 时传入上述配置。

3. 更新工程依赖与使用说明：
   - 更新 `requirements.txt`，新增 `ultralytics`、`opencv-python`。
   - 更新 `README.md`，新增“YOLOv8 本地推理（无需外部 API）”章节和 PowerShell 配置示例。
   - 同步修正流程图边界说明，标注已支持本地 YOLOv8 推理。

### 涉及文件/模块
- `visual_module/inference.py`
- `backend/config.py`
- `backend/api_routes.py`
- `requirements.txt`
- `README.md`
- `UPDATE_LOG.md`

### 验证结果
- 语法检查通过（不落盘编译）：
  - `backend/config.py`
  - `backend/api_routes.py`
  - `visual_module/inference.py`

### 已知问题
- 当前尚未在本环境完成 `ultralytics` 安装与真实权重推理实测；仍需在可安装依赖的机器上进行运行级验证。
- 返回类别名依赖模型 `names` 映射，需与最终自训练数据集类别规范保持一致。

### 下一步任务
1. 新增 `visual_module/train_yolo.py`，提供本地训练脚本（含数据集 YAML、训练参数、导出 best.pt 说明）。
2. 在 `backend` 增加一个最小集成测试，覆盖 YOLO 正常推理与回退逻辑两条路径。

---

## 2026-03-16 第 7 次更新

- 执行者：Codex
- 更新类型：YOLO 训练脚本与数据配置模板落地

### 更新内容
1. 新增 `visual_module/train_yolo.py`：
   - 支持 YOLOv8 训练参数管理（`data/model/device/epochs/batch/imgsz` 等）。
   - 支持训练后自动验证（可关闭）。
   - 支持导出模型（默认 `onnx`，可选 `none/torchscript/openvino/engine`）。
   - 训练完成后输出 `save_dir` 与 `best.pt` 路径，便于直接接入后端推理。

2. 新增数据集配置模板：
   - 新增 `docs/berry_yolo_data.example.yaml`（用于复制到 `data/processed/berry_yolo_data.yaml`）。
   - 提供标准目录结构示例与默认类别映射：`powdery_mildew/aphid/gray_mold`。

3. 文档同步：
   - 更新 `README.md`，新增“YOLOv8 本地训练（产出 best.pt）”章节与执行命令。
   - 更新 `DEV_NOTES.md`，将 YOLO 推理接入与 `train_yolo.py` 项标记为已完成。

### 涉及文件/模块
- `visual_module/train_yolo.py`
- `docs/berry_yolo_data.example.yaml`
- `README.md`
- `DEV_NOTES.md`
- `UPDATE_LOG.md`

### 验证结果
- 语法检查通过（不落盘编译）：
  - `visual_module/train_yolo.py`
  - `visual_module/inference.py`
  - `backend/api_routes.py`
  - `backend/config.py`

### 已知问题
- 当前尚未在真实标注数据上执行训练，`best.pt` 仍需用户按数据集完成训练后生成。
- 推理类别仍依赖当前加载权重，若继续使用 COCO 预训练权重会出现非农业类别。

### 下一步任务
1. 以 `berry_yolo_data.yaml` + 标注数据实际跑完一次训练，产出并接入 `best.pt`。
2. 增加类别映射与低置信度兜底策略，避免非农业类别直接传入 RAG。

---

## 2026-03-16 第 8 次更新

- 执行者：Codex
- 更新类型：RAG 检索模块升级（本地 chunks + 可持久化索引）

### 更新内容
1. 重写 `rag_module/retriever.py`：
   - 检索数据源优先读取 `data/chunks/*.json|*.jsonl`。
   - 若本地 chunks 不存在，自动回退读取 `docs/berry_manual.md`。
   - 若仍无可用数据，回退到内置最小知识库，确保服务不中断。

2. 检索索引与缓存：
   - 启动检索时自动构建向量并缓存。
   - 向量与元数据持久化到 `data/vector_store/`。
   - 若环境安装了 `faiss`，优先使用 FAISS `IndexFlatIP` 检索；未安装时自动回退余弦相似度检索。

3. 文档同步：
   - 更新 `README.md`，新增 “RAG 检索数据接入（本地 chunks）” 章节。
   - 更新 `DEV_NOTES.md`，将“真实检索接入”任务标记为已完成。

### 涉及文件/模块
- `rag_module/retriever.py`
- `README.md`
- `DEV_NOTES.md`
- `UPDATE_LOG.md`

### 验证结果
- 语法检查通过（不落盘编译）：`rag_module/retriever.py`
- 代码路径检查通过：`/api/diagnose` 调用路径不变，兼容现有接口协议。

### 已知问题
- `data/*` 在仓库中默认被 `.gitignore` 忽略，chunks 与 vector_store 需要在本地环境准备与验证。
- 当前 embedding 仍为哈希占位实现，后续可替换为真实文本 embedding 模型以提升召回质量。

### 下一步任务
1. 新增 `chunks` 生产脚本（从 `docs/berry_manual.md` 自动切块并落盘 `data/chunks`）。
2. 将 `embedder.py` 从哈希向量升级为真实 embedding 模型。

---

## 2026-03-16 第 9 次更新

- 执行者：Codex
- 更新类型：视觉类别映射与低置信度兜底策略

### 更新内容
1. 更新 `visual_module/inference.py`：
   - 新增业务类别白名单：`powdery_mildew`、`aphid`、`gray_mold`。
   - 新增类别别名映射（如 `powdery mildew` -> `powdery_mildew`、`botrytis` -> `gray_mold`）。
   - YOLO 检测结果若类别不在业务白名单，或置信度低于业务阈值，则统一回退为 `unknown_leaf_issue`。

2. 新增业务置信度配置：
   - `backend/config.py` 新增 `YOLO_BUSINESS_CONF`（默认 `0.45`）。
   - `backend/api_routes.py` 将该参数传入 `run_inference`。

3. 文档同步：
   - `README.md` 增加 `YOLO_BUSINESS_CONF` 说明与 PowerShell 配置示例。
   - 补充“仅放行业务类别，其余自动回退”的行为说明。
   - `DEV_NOTES.md` 将“统一推理输出 schema（类别映射等）”标记为已完成。

### 涉及文件/模块
- `visual_module/inference.py`
- `backend/config.py`
- `backend/api_routes.py`
- `README.md`
- `DEV_NOTES.md`
- `UPDATE_LOG.md`

### 验证结果
- 语法检查通过：`visual_module/inference.py`、`backend/config.py`、`backend/api_routes.py`
- 映射函数快速校验通过：`frisbee -> None`、`Powdery Mildew -> powdery_mildew`、`aphid -> aphid`

### 已知问题
- 当前仍使用通用权重时，可能频繁回退为 `unknown_leaf_issue`，属于预期行为。
- 真实效果仍取决于后续农业数据训练得到的 `best.pt`。

### 下一步任务
1. 产出并接入农业病虫害 `best.pt`，验证三类业务标签的端到端稳定识别。
2. 新增 `/api/diagnose` 自动化测试，覆盖“非业务类别回退”和“低置信度回退”。

---

## 2026-03-16 第 10 次更新

- 执行者：Codex
- 更新类型：RAG chunks 自动构建脚本与结构化字段落地

### 更新内容
1. 新增 `rag_module/build_chunks.py`：
   - 从 `docs/berry_manual.md` 自动解析章节并生成 `jsonl` 知识块。
   - 支持提取结构化字段：`crop`、`disease_cn`、`disease_en`、`symptom`、`treatments`、`pesticide`、`dose`、`interval_days`、`keywords`。
   - 提供 CLI 参数：`--input` 与 `--output`，可复用到后续手册版本。

2. 本地执行生成：
   - 运行 `python -m rag_module.build_chunks --input docs/berry_manual.md --output data/chunks/berry_manual_chunks.jsonl`。
   - 产出 3 条结构化 chunks，供 `retriever` 直接读取。

3. 文档与任务状态同步：
   - `README.md` 新增“从手册自动生成 chunks”章节与命令示例。
   - `DEV_NOTES.md` 将“文本知识块生产流程”“结构化字段补充”标记为已完成。

### 涉及文件/模块
- `rag_module/build_chunks.py`
- `README.md`
- `DEV_NOTES.md`
- `UPDATE_LOG.md`

### 验证结果
- 脚本运行成功：`Built chunks: 3 -> data/chunks/berry_manual_chunks.jsonl`
- 检索验证通过：`rag_module.retriever.search()` 已可直接命中新生成 chunks。

### 已知问题
- 当前结构化抽取采用规则法，适配 `berry_manual.md` 现有格式；后续文档格式变化时可能需要补充规则。
- `data/*` 默认被 `.gitignore` 忽略，chunks 需在本地运行脚本生成。

### 下一步任务
1. 在 `retriever` 中接入基于 `disease/crop` 的元数据过滤参数，降低不相关召回。
2. 将 `embedder.py` 从哈希向量替换为真实 embedding 模型（先文本 embedding）。
