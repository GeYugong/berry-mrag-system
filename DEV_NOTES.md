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
