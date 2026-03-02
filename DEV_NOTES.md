### 一、 系统整体技术架构

整个系统围绕“感知 - 认知 - 生成”的混合式 AI 工作流展开：

1. 
**感知层**：通过 OpenCV 进行图像标准化处理，送入微调后的 YOLOv8 模型，提取病虫害类别和位置坐标。


2. 
**认知层（MRAG）**：利用 CLIP 模型对多模态数据进行高维向量化，在 FAISS/Milvus 中进行高效 Top-K 检索召回。


3. 
**生成层**：将检索到的精准多模态知识块打包，通过 Prompt 输入 LLaVA 等大模型，输出综合诊断与防治方案。



---

### 二、 完整项目目录结构

建立清晰的工程目录，能够让四名成员互不干扰地进行并行开发。推荐采用如下基于 Python 的标准后端应用结构：

```text
berry-mrag-system/
├── data/                         # 数据集与持久化存储 (需在 .gitignore 中忽略)
│   ├── raw_images/               # 原始采集的浆果图像
│   ├── processed_images/         # 预处理后的标准化图像
│   ├── raw_documents/            # 原始农业手册、论文 (PDF/Word)
│   ├── chunks/                   # 切分后的文本块数据 (JSON/CSV)
│   └── vector_db_storage/        # FAISS/Milvus 向量库本地持久化文件
│
├── docs/                         # 项目文档与团队知识库
│   ├── api_specs/                # 前后端 API 接口文档
│   └── knowledge_base/           # 团队技术沉淀 (支持使用 Markdown 编写，同步管理)
│
├── src/                          # 核心源代码目录
│   ├── vision_module/            # 【模块 1】高精度视觉诊断模块
│   │   ├── preprocessing.py      # 图像清洗、尺度标定、色彩校正与精准分割脚本
│   │   ├── dataset_builder.py    # YOLOv8 格式数据集自动生成脚本
│   │   ├── train_yolo.py         # YOLOv8 微调训练脚本
│   │   └── inference.py          # YOLOv8 推理接口封装，输出类别、置信度、坐标
│   │
│   ├── rag_module/               # 【模块 2】多模态检索增强生成模块
│   │   ├── document_parser.py    # 文本提取与 chunk 切块逻辑
│   │   ├── embedding.py          # 调用 CLIP 将文本/图像/视频关键帧编码为高维向量
│   │   ├── vector_store.py       # 封装 FAISS/Milvus 的增删改查与相似度搜索
│   │   ├── reranker.py           # 检索结果二次重排模型逻辑
│   │   └── mllm_generator.py     # Prompt 组装及 LLaVA 等多模态大模型 API 对接
│   │
│   ├── backend_api/              # 【模块 3】后端服务 API 集成
│   │   ├── main.py               # FastAPI/Flask 主程序入口
│   │   ├── routers/              # 路由分发 (诊断接口、问答接口等)
│   │   └── schemas.py            # Pydantic 数据校验模型 (定义请求体和响应体格式)
│   │
│   └── utils/                    # 通用工具类
│       ├── config.py             # 全局配置读取 (加载 .env 文件)
│       └── logger.py             # 统一日志记录工具
│
├── frontend_app/                 # 【模块 4】前端交互界面
│   ├── public/                   # 静态资源
│   └── src/                      # Vue/React 或 Streamlit 应用源码
│       ├── components/           # UI 组件 (图片上传框、聊天气泡、报告渲染)
│       └── api_client.js         # 与后端交互的请求逻辑
│
├── weights/                      # 存放训练好的模型权重 (.pt, .safetensors 等)
├── .env.example                  # 环境变量配置模板 (API Keys, 数据库 URL)
├── .gitignore                    # Git 忽略清单
├── requirements.txt              # Python 环境依赖包列表
└── README.md                     # 项目入口说明文档

```

---

### 三、 核心模块内容与开发要点

在工程化落地时，各个模块需要明确输入输出，方便团队成员对接：

#### 1. 视觉预处理与检测 ( `src/vision_module/` )

* **工作内容**：构建自动化流水线，读取原始图像进行预处理。利用 OpenCV 脚本确保输入模型前的图片在尺度和色彩上保持一致，必要时进行病叶的精准分割以排除复杂背景干扰。随后，将处理好的数据转换为 YOLO 格式进行训练。
* 
**交付物**：一个 `inference.py` 脚本，接收一张图片路径，返回一个包含边界框坐标、置信度和“如：草莓白粉病”标签的结构化字典。



#### 2. 知识库构建与向量化 ( `src/rag_module/` )

* 
**工作内容**：将收集到的文献解析，严格切分成适合 LLM 阅读的“知识块”（chunks）。使用 CLIP 模型统一处理图像和这些文本块，生成跨模态特征向量。


* 
**交付物**：稳定运行的 FAISS/Milvus 实例，提供一个 `search(query_vector, top_k=5)` 方法，能在一秒内极速召回相关的图文语料。



#### 3. 大模型生成核心 ( `src/rag_module/mllm_generator.py` )

* **工作内容**：这是整个系统的大脑。它需要将视觉模块输出的“病害标签”、向量数据库召回的“防治手册知识块”以及“用户原始提问”拼接成一个高质量的 Prompt，然后调用大模型生成答案。
* 
**交付物**：一个流式输出生成器，输出格式化良好的 Markdown 防治方案文本（包含农药、剂量等）。



#### 4. RESTful API 服务端 ( `src/backend_api/` )

* 
**工作内容**：负责把上面所有的底层算法封装成 Web 接口。前端只需要向后端发送带有图片的 HTTP 请求，后端统筹视觉诊断和 MRAG 流程后，将结果通过 JSON 返回。



