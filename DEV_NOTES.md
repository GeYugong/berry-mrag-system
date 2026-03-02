### 一、系统整体技术架构

系统围绕“感知 - 认知 - 生成”流程构建：

1. 感知层：视觉模块输出病虫害类别、置信度、目标框。
2. 认知层：RAG 模块完成向量化、召回、重排。
3. 生成层：基于检索上下文输出结构化诊断建议。

---

### 二、当前仓库实际目录结构（已落地）

```text
berry-mrag-system/
├── backend/
│   ├── main.py               # FastAPI 入口
│   ├── api_routes.py         # /api/health 与 /api/diagnose
│   ├── schemas.py            # 请求/响应模型
│   └── config.py             # 运行配置
├── visual_module/
│   └── inference.py          # 视觉诊断占位推理
├── rag_module/
│   ├── embedder.py           # 向量化占位实现
│   ├── retriever.py          # 检索逻辑（内置知识库）
│   ├── reranker.py           # 重排逻辑
│   └── mllm_generator.py     # Markdown 报告生成
├── data/
│   ├── raw/                  # 原始数据目录（预留）
│   ├── processed/            # 处理后数据目录（预留）
│   ├── chunks/               # 文本块目录（预留）
│   └── vector_store/         # 向量库目录（预留）
├── frontend/                 # 前端目录（预留）
├── docs/                     # 文档目录
├── PROJECT_SPEC.md           # 项目规范与约束
├── UPDATE_LOG.md             # Codex 追加式更新日志
└── README.md                 # 项目说明
```

---

### 三、模块职责与最小交付

#### 1. 视觉模块（`visual_module/`）

- 输入：图片路径（演示阶段可为空）。
- 输出：`pest_type`、`confidence`、`bbox`。

#### 2. RAG 模块（`rag_module/`）

- 输入：用户问题 + 视觉结果。
- 处理：向量化 -> Top-K 检索 -> 重排 -> 生成。
- 输出：可直接展示的 Markdown 建议文本。

#### 3. 后端 API（`backend/`）

- `GET /api/health`：健康检查。
- `POST /api/diagnose`：端到端诊断链路。

---

### 四、说明

- 本文件描述的是“当前已落地结构”，不是未来理想结构草案。
- 若未来新增 `train_yolo.py`、真实 FAISS/Milvus、前端页面等，请在实现后同步更新本文件与 `PROJECT_SPEC.md`。

---

### 五、完整 To-Do List（执行清单）

#### P0：先打通可评估主链路

- [ ] 建立最小可用数据集（图片 + 文本 chunks）并完成目录落盘。
- [ ] 接入真实 YOLO 推理，替换 `visual_module/inference.py` 占位逻辑。
- [ ] 接入真实检索（优先 FAISS），替换 `rag_module/retriever.py` 内置知识库。
- [ ] 保持 `/api/diagnose` 输出协议稳定（`detection/retrieved/answer_markdown`）。
- [ ] 增加最小回归测试，覆盖 `/api/health` 与 `/api/diagnose`。

#### 数据工程（Data）

- [ ] 明确病虫害类别体系（中文名、英文 key、同义词映射）。
- [ ] 建立标注规范文档（框选规则、遮挡/重叠处理、难例定义）。
- [ ] 采集并清洗原始图像，去除重复、严重模糊、错误样本。
- [ ] 划分训练/验证/测试集，防止同场景泄漏。
- [ ] 建立文本知识块生产流程（解析、切块、去重、元数据）。
- [ ] 补充结构化字段（农药、剂量、安全间隔期、适用作物阶段）。

#### YOLO 专项（重点）

- [ ] 新建 `visual_module/train_yolo.py`（训练入口与参数管理）。
- [ ] 新建 `visual_module/preprocessor.py`（尺寸/色彩/增强预处理）。
- [ ] 准备 YOLO 数据配置（类别、路径、训练参数）。
- [ ] 训练基线模型（记录输入尺寸、batch、epoch、lr、augment）。
- [ ] 评估指标落库：mAP50、mAP50-95、Precision、Recall、每类指标。
- [ ] 输出误检/漏检样本清单并建立回流机制。
- [ ] 完成模型版本化（权重、配置、数据版本、评估报告绑定）。
- [ ] 在 `inference.py` 增加真实模型加载、阈值控制、NMS 参数配置。
- [ ] 统一推理输出 schema（类别映射、置信度、bbox 坐标系说明）。
- [ ] 增加推理性能测试（单张延迟、吞吐、CPU/GPU 对比）。

#### RAG 专项

- [ ] 将 `embedder.py` 升级为真实 embedding（CLIP/文本模型二选一先落地）。
- [ ] 使用 `data/chunks` 构建向量索引并持久化到 `data/vector_store`。
- [ ] 完成 Top-K 召回与过滤（按病虫害类别、作物阶段、时令条件）。
- [ ] 优化 `reranker.py`（规则+模型混合，先规则后模型）。
- [ ] 在 `mllm_generator.py` 增加引用依据与安全提示模板。

#### 后端与工程化

- [ ] 增加统一错误码与异常处理中间件。
- [ ] 增加配置管理（`.env.example`、环境区分、必填项校验）。
- [ ] 增加日志与追踪字段（request_id、耗时、模块阶段耗时）。
- [ ] 增加接口文档示例（成功/失败样例、字段解释）。
- [ ] 补充单元测试与集成测试（pytest + 接口测试）。

#### 前端与交互

- [ ] 实现图片上传 + 文本提问页面。
- [ ] 展示检测框信息、检索依据、最终建议报告。
- [ ] 增加加载状态、失败重试、输入校验提示。
- [ ] 增加移动端适配。

#### 质量与交付

- [ ] 建立验收指标看板：YOLO 准确率、检索相关性、接口延迟。
- [ ] 形成周迭代节奏：数据回流 -> 再训练 -> 回归测试。
- [ ] 完成部署文档（本地、服务器、依赖与端口说明）。
- [ ] 完成演示脚本与答辩材料（流程图、案例、指标对比）。

#### 下一次开发建议（短期）

- [ ] 先实现 `visual_module/train_yolo.py` 与真实 `inference.py` 接入。
- [ ] 同步将 `rag_module/retriever.py` 切换为 FAISS 本地索引。
- [ ] 为 `/api/diagnose` 增加一条端到端自动化测试用例。
