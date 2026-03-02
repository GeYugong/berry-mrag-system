# berry-mrag-system

berry-mrag-system/
├── data/                  # 存放原始数据和处理后的数据（记得在 .gitignore 中忽略大文件）
├── docs/                  # 团队知识库、需求文档、开题报告等
├── visual_module/         # A工作区：YOLOv8 训练、推理与 OpenCV 处理脚本
├── rag_module/            # B工作区：文本切块（chunks）、CLIP 编码、MLLM 交互 [cite: 22, 28, 31]
├── backend/               # C工作区：FastAPI/Flask 应用，FAISS/Milvus 数据库交互 [cite: 33, 36]
├── frontend/              # D工作区：Web 前端代码 
├── requirements.txt       # 项目核心依赖包
└── README.md              # 项目简介与快速启动指南