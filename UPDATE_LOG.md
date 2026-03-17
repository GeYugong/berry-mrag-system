# 更新日志

说明：
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

---

## 2026-03-16 第 11 次更新

- 执行者：Codex
- 更新类型：`/api/diagnose` 检索过滤参数接入（crop / disease_hint）

### 更新内容
1. 接口参数扩展：
   - `backend/schemas.py` 为 `DiagnoseRequest` 新增可选字段：
     - `crop`（作物提示）
     - `disease_hint`（病害提示）

2. 路由调用接入过滤参数：
   - `backend/api_routes.py` 在调用 `retriever.search()` 时传入 `crop` 与 `disease_hint`。
   - 当未传 `disease_hint` 时，自动回退使用视觉结果中的 `pest_type`。

3. 检索过滤能力落地：
   - `rag_module/retriever.py` 新增过滤逻辑：
     - 支持按 `crop`、`disease_hint` 过滤候选知识块。
     - 有过滤条件时自动扩大召回范围，再二次筛选，最后截断 Top-K。
   - 兼容 `data/chunks` 的结构化字段（如 `crop`、`disease_en`、`keywords`）。

4. 文档与任务同步：
   - `README.md` 补充带过滤参数的请求示例。
   - `DEV_NOTES.md` 将“Top-K 召回与过滤”标记为已完成。

### 涉及文件/模块
- `backend/schemas.py`
- `backend/api_routes.py`
- `rag_module/retriever.py`
- `README.md`
- `DEV_NOTES.md`
- `UPDATE_LOG.md`

### 验证结果
- 语法检查通过：`backend/schemas.py`、`backend/api_routes.py`、`rag_module/retriever.py`
- 检索功能验证通过：
  - `crop=草莓` 返回 `manual-001`
  - `disease_hint=aphid` 返回 `manual-002`

### 已知问题
- 当前过滤依赖规则匹配，若后续文档字段命名变化需同步调整匹配规则。
- 过滤维度目前为 `crop/disease_hint`，时令条件等高级过滤尚未接入。

### 下一步任务
1. 将 `embedder.py` 从哈希向量升级为真实文本 embedding 模型识别。
2. 为 `/api/diagnose` 新增自动化测试，覆盖过滤参数命中与未命中场景。

---

## 2026-03-16 第 12 次更新

- 执行者：Codex
- 更新类型：接入百炼 OpenAI 兼容 Embedding（Qwen3-Embedding）

### 更新内容
1. 升级 `rag_module/embedder.py`：
   - 支持通过 OpenAI SDK 调用百炼兼容接口（`DASHSCOPE_API_KEY` + `EMBEDDING_MODEL`）。
   - 默认模型为 `text-embedding-v4`，支持 `dimensions` 参数。
   - 新迎本地哈希向量回退，接口异常时保持服务可用。

2. 检索缓存重建逻辑增强：
   - `rag_module/retriever.py` 的索引签名加入 `EMBEDDING_MODEL/EMBEDDING_DIM`。
   - 维度变化时自动触发向量重建，避免旧索引污染。

3. 依赖与文档更新：
   - `requirements.txt` 新增 `openai` 依赖。
   - `README.md` 新增百炼 Embedding 环境变量配置说明。

### 涉及文件/模块
- `rag_module/embedder.py`
- `rag_module/retriever.py`
- `requirements.txt`
- `README.md`
- `UPDATE_LOG.md`

### 验证结果
- 语法检查通过：`rag_module/embedder.py`、`rag_module/retriever.py`
- `embed_text(..., dim=64)` 可返回 64 维向量。

### 已知问题
- 当前环境网络受限时，Embedding 可能走回退向量；需在可联网环境验证真实 API 命中。

### 下一步任务
1. 重启 `uvicorn` 并验证 `data/vector_store` 已按新 embedding 维度重建。
2. 新增 `/api/diagnose` 自动化测试，覆盖 embedding API 异常回退路径。

---

## 2026-03-16 第 13 次更新

- 执行者：Codex
- 更新类型：自动化测试用例新增（YOLO 兜底 / 检索过滤 / 诊断韧性）

### 更新内容
1. 新增视觉兜底测试：`tests/test_visual_inference_guardrail.py`
   - 覆盖非业务类别回退 `unknown_leaf_issue`。
   - 覆盖低置信度业务类别回退。
   - 覆盖业务类别+足够置信度正常放行。

2. 新增检索过滤测试：`tests/test_retriever_filters.py`
   - 覆盖 `crop=草莓` 过滤命中。
   - 覆盖 `disease_hint=aphid` 过滤命中。

3. 新增接口韧性测试：`tests/test_api_diagnose_resilience.py`
   - 覆盖 embedding API 异常时 `embed_text` 的回退向量行为。
   - 覆盖 `/api/diagnose` 在 embedding API 异常场景下仍返回 200。

4. 依赖调整：
   - `requirements.txt` 增加 `pytest` 依赖。

### 涉及文件/模块
- `tests/test_visual_inference_guardrail.py`
- `tests/test_retriever_filters.py"
- `tests/test_api_diagnose_resilience.py`
- `requirements.txt`
- `UPDATE_LOG.md`

### 验证结果
- 测试文件语法检查通过。
- 关键断言手工验证通过：
  - `embed_text` 在 API 异常时可返回指定维度向量。
  - `retriever` 过滤逻辑可正确命中目标样本。
- 当前会话因 PyPI 访问受限，`pytest` 模块安装失败，未完成完整 `python -m pytest` 运行验证。

### 已知问题
- 受网络/代理环境影响，`pip install pytest` 在当前会话返回 `No matching distribution found`。

### 下一步任务
1. 在可安装依赖的终端执行 `pip install -r requirements.txt` 后运行 `python -m pytest -q tests`。
2. 补充一条真实 `TestClient` 集成测试，不依赖 monkeypatch 的 `search` 返回。

## 2026-03-16 第 14 次更新

- 执行者：Gemini CLI
- 更新类型：仓库深度调研与前端脚手架初始化

### 更新内容
1. **仓库深度调研与代码梳理**：
   - 完整分析了 `backend`、`visual_module`、`rag_module` 的逻辑链路。
   - 确认了 `/api/diagnose` 接口的输入输出协议，以及视觉模块的“YOLO 优先 + 文件名回退”和 RAG 模块的“FAISS 检索 + 规则重排”机制。
2. **前端脚手架初始化**：
   - 在 `frontend/` 目录下使用 Vite 初始化了 **React + TypeScript** 项目。
   - 确立了前端“智慧农业”主题风格（森林绿 + 浆果红）及交互原型设计。

### 涉及文件/模块
- `UPDATE_LOG.md`
- `frontend/` (Vite 初始化产物)
- `backend/`, `visual_module/`, `rag_module/` (调研覆盖)

### 验证结果
- **后端协议校验**：通过 `read_file` 确认接口逻辑闭环，支持多模态输入与 Markdown 报告输出。
- **前端初始化校验**：`frontend/` 目录结构已生成，`package.json` 配置正确。

### 已知问题
- 前端目前仅为基础骨架，尚未安装 `lucide-react`、`react-markdown` 等核心依赖。
- `embedder.py` 和 `mllm_generator.py` 目前仍为占位实现，需在前端联调后考虑接入真实模型。

### 下一步任务
1. **前端依赖安装**：安装 `lucide-react` (图标)、`react-markdown` (渲染) 及 `clsx` (类名管理)。
2. **核心组件开发**：实现图片上传预览与诊断报告展示组件，并与后端 `/api/diagnose` 接口联调。

---

## 2026-03-16 第 15 次更新

- 执行者：Gemini CLI
- 更新类型：前端全栈功能实现与后端联调增强（CORS & 文件上传）

### 更新内容
1. **后端联调能力增强**：
   - 更新 `backend/main.py`：启用 **CORS 中间件**，允许前端跨域请求。
   - 更新 `backend/api_routes.py`：新增 `POST /api/diagnose/upload` 接口，支持 `multipart/form-data` 文件上传，方便 Web 端直接调用。
2. **前端应用完整落地**：
   - 编写 `frontend/src/App.tsx`：实现图片上传预览、文本问题输入、异步诊断请求及报告渲染逻辑。
   - 编写 `frontend/src/App.css`：确立“智慧农业”主题视觉，并添加加载动画。
   - 集成 `react-markdown`：实现诊断报告的富文本展示。
   - 集成 `lucide-react`：增强界面的图形化引导。

### 涉及文件/模块
- `backend/main.py`
- `backend/api_routes.py`
- `frontend/src/App.tsx`, `App.css`, `index.css`
- `UPDATE_LOG.md`

### 验证结果
- **后端接口验证**：使用模拟数据调用 `/api/diagnose/upload` 成功保存图片并返回诊断 JSON。
- **前端编译验证**：React 组件无语法错误，样式加载正常。

### 已知问题
- 生产环境部署时需收紧 `allow_origins` 配置。

### 下一步任务
1. 启动全栈服务进行端到端实测验证。

---

## 2026-03-17 第 16 次更新（更正）

- 执行者：Codex
- 更新类型：后端配置模板与诊断日志增强（更正归位）

### 更正说明
- 先前同内容日志误写为“第 14 次更新”，与 Gemini CLI 第 14/15 次记录发生编号冲突。
- 按当前顺序更正归位为“第 16 次更新”，并保留历史条目不删除（遵循追加式日志规则）。

### 更新内容
1. 新增环境变量模板：
   - 新增仓库根目录 `.env.example`。
   - 覆盖 App、YOLO、Embedding 关键配置项，便于多人协作统一环境。

2. 诊断接口日志增强：
   - `backend/api_routes.py` 为 `/api/diagnose` 与 `/api/diagnose/upload` 增加 `request_id`。
   - 记录开始/成功/失败日志，并输出耗时（`elapsed_ms`）、`pest_type`、召回条数等关键信息。

3. 日志级别配置：
   - `backend/config.py` 增加 `LOG_LEVEL`。
   - `backend/main.py` 增加统一 `logging.basicConfig` 初始化。

4. 文档同步：
   - `README.md` 修正 `.env.example` 现状说明。

### 涉及文件/模块
- `.env.example`
- `backend/api_routes.py`
- `backend/config.py`
- `backend/main.py`
- `README.md`
- `UPDATE_LOG.md`

### 验证结果
- 语法检查通过：`backend/config.py`、`backend/main.py`、`backend/api_routes.py`

### 已知问题
- 当前测试运行仍受本机 `pytest` 依赖安装环境影响，完整自动化测试需在可安装依赖环境执行。

### 下一步任务
1. 在可联网环境执行 `python -m pytest -q tests`，闭环验证新增日志改动未引入回归。
2. 补充真实 `TestClient` 集成测试，减少 monkeypatch 依赖。

---

## 2026-03-17 第 17 次更新

- 执行者：Codex
- 更新类型：上传接口依赖补全与端到端接口实测

### 更新内容
1. 依赖补全：
   - `requirements.txt` 新增 `python-multipart>=0.0.20,<1.0`，用于 FastAPI `Form/File` 上传解析。

2. 接口实测：
   - 验证 `POST /api/diagnose`（JSON）可正常返回诊断结果。
   - 验证 `POST /api/diagnose/upload`（multipart/form-data）可正常接收图片并返回诊断结果。

### 涉及文件/模块
- `requirements.txt`
- `UPDATE_LOG.md`

### 验证结果
- `/api/diagnose` 返回 200，包含 `detection/retrieved/answer_markdown`。
- `/api/diagnose/upload` 返回 200，协议字段完整。

### 已知问题
- 当前使用通用权重时，病害类别仍可能回退为 `unknown_leaf_issue`，属于业务兜底预期行为。

### 下一步任务
1. 前端与 `/api/diagnose/upload` 完成联调，确认图片上传路径与字段一致。
2. 后续切换自训练 `best.pt` 后复测三类病害识别效果。

---

## 2026-03-17 第 18 次更新

- 执行者：Codex
- 更新类型：RAG 离线评测脚本与指标报告落地

### 更新内容
1. 新增评测集示例：
   - 新增 `docs/eval_queries.example.jsonl`（包含 query/crop/disease_hint/gold_doc_ids）。

2. 新增离线评测脚本：
   - 新增 `rag_module/eval_retrieval.py`。
   - 支持评测模式：`filtered` / `unfiltered` / `both`。
   - 输出指标：`Recall@K`、`MRR@K`、`nDCG@K`、平均延迟与 P95 延迟。
   - 输出文件：JSON 报告与 Markdown 报告。

3. 文档补充：
   - `README.md` 新增“RAG 离线评测”使用说明与命令示例。

4. 执行验证：
   - 运行评测命令并生成：
     - `data/vector_store/eval_report.json`
     - `docs/eval_report.md`

### 涉及文件/模块
- `docs/eval_queries.example.jsonl`
- `rag_module/eval_retrieval.py`
- `README.md`
- `UPDATE_LOG.md`

### 验证结果
- 语法检查通过：`rag_module/eval_retrieval.py`
- 评测脚本运行成功并产出报告。
- 当前示例集结果显示：`filtered` 模式下排序指标（MRR/nDCG）优于 `unfiltered`，证明过滤策略有效。

### 已知问题
- 当前评测集规模较小（示例 5 条），指标仅用于流程验证，不代表线上真实性能。
- 延迟受 embedding API 网络波动影响明显，需在稳定环境重复采样。

### 下一步任务
1. 扩充离线评测集到 30~100 条，覆盖更多作物与病害问法。
2. 在 `reranker` 中接入字段加权（title/crop/disease_en）并复测指标提升。

---

## 2026-03-17 第 19 次更新

- 执行者：Codex
- 更新类型：Reranker 字段加权与离线评测对比增强

### 更新内容
1. 升级 `rag_module/reranker.py`：
   - 将原先简单规则改为结构化加权规则。
   - 加权维度：`disease_en`、`title`、`crop`、`keywords`、`dose`、`interval_days`。
   - 支持参数：`pest_type` + 可选 `crop` + 可选 `disease_hint`。

2. 检索结果补充结构化字段：
   - 更新 `rag_module/retriever.py`，返回结果中附带 `crop/disease_en/keywords/dose/interval_days`（供 rerank 使用）。

3. 路由联动：
   - 更新 `backend/api_routes.py`，调用 `rerank` 时传入 `crop` 与 `disease_hint`。

4. 离线评测增强：
   - 重写 `rag_module/eval_retrieval.py`，新增 `--use-rerank` 开关。
   - 报告新增 `Use Rerank` 标记，支持更直观的前后对比。

5. 实际评测结果（示例集）：
   - 在 `--use-rerank` 下，`unfiltered` 模式指标提升：
     - `MRR@K`: `0.6333 -> 0.8667`
     - `nDCG@K`: `0.7262 -> 0.9000`
   - 报告已写入：`docs/eval_report.md` 与 `data/vector_store/eval_report.json`。

### 涉及文件/模块
- `rag_module/reranker.py`
- `rag_module/retriever.py`
- `backend/api_routes.py`
- `rag_module/eval_retrieval.py`
- `docs/eval_report.md`
- `README.md`
- `UPDATE_LOG.md`

### 验证结果
- 语法检查通过：`retriever/reranker/api_routes/eval_retrieval`。
- `/api/diagnose` 实测返回正常，且在过滤条件下召回分数更聚焦。
- 离线评测脚本成功运行并输出对比结果。

### 已知问题
- 当前示例评测集规模较小，指标仅说明策略方向有效，仍需扩大样本验证稳健性。
- 延迟仍受 embedding API 网络波动影响。

### 下一步任务
1. 扩充评测集到 30~100 条并按病害类别分组统计指标。
2. 在 `reranker` 中加入“失败样例回流”机制，针对低分命中 query 进行规则迭代。
