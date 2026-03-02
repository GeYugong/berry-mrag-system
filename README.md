# 面向浆果种植的多模态RAG系统 (Berry-MRAG-System)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![YOLOv8](https://img.shields.io/badge/YOLO-v8-green.svg)](https://github.com/ultralytics/ultralytics)

> **大连理工大学大学生创新创业训练计划**
> 
> **项目编号**：20261014110987 

## 📖 项目简介

本项目旨在构建一个能够综合利用文本、图像、视频等多模态数据的检索增强生成（MRAG）系统，为浆果种植提供精准、高效的智能决策支持 。

通过创新的“感知 - 认知 - 生成”混合式 AI 工作流 ，系统将帮助浆果种植户有效获取和利用农业知识，降低种植风险，推动智慧农业的发展与数字化转型 。

## ✨ 核心功能与预期指标

* **📸 多模态交互**：支持农户通过文本提问（如“草莓叶子有白色粉末怎么办”）或上传拍摄的病虫害部位图像进行交互 。
* **🩺 高精度视觉诊断**：采用微调的 YOLOv8 模型，病虫害诊断准确率预期 ≥85% 。
* **🧠 智能决策与生成**：结合多模态大语言模型（MLLM），生成图文并茂的防治方案（含推荐农药、剂量、安全间隔期等），并可结合环境数据生成个性化水肥管理方案 。
* **⚡ 高效跨模态检索**：实现文本匹配图像、图像关联文本的高效检索，检索延迟预期 ≤1 秒，结果相关性达标率预期 ≥90% 。

## 🛠️ 技术栈选型

* **视觉检测基础模型**：YOLOv8 
* **多模态处理与生成**：CLIP / LLaVA 
* **向量存储与检索引擎**：FAISS / Milvus 
* **数据预处理**：Python, OpenCV (用于构建高质量视觉数据集) 

## 📂 项目结构

```text
berry-mrag-system/
├── data/                  # 多模态数据集（视觉图像、文本知识块 chunks、传感器数据等）
├── docs/                  # 团队知识库（支持通过 Obsidian 结合 GitHub 进行 Markdown 知识同步）与项目文档
├── visual_module/         # 第一阶段：高精度视觉诊断模块 (YOLOv8 微调与推理代码) 
├── rag_module/            # 第二阶段：多模态检索增强生成模块 (CLIP 编码、向量召回、重排、MLLM 交互) 
├── backend/               # 后端服务 API 集成 
├── frontend/              # 简洁直观的 Web 前端应用程序 
├── requirements.txt       # 环境依赖
└── README.md              # 项目说明文档

```

## 🚀 快速启动

### 1. 克隆仓库

```bash
git clone [https://github.com/Berry-MRAG-Team/berry-mrag-system.git](https://github.com/Berry-MRAG-Team/berry-mrag-system.git)
cd berry-mrag-system

```

### 2. 配置环境

建议使用 Conda 创建虚拟环境：

```bash
conda create -n berry-mrag python=3.10
conda activate berry-mrag
pip install -r requirements.txt

```

*(注：API 密钥及数据库配置请参考 `backend/.env.example` 文件进行本地设置)*





## 📅 项目开发进度规划

* **第一阶段：多模态数据处理与基础流水线搭建**
  * 编写 Python 脚本进行视觉数据的清洗、尺寸缩放与标准化，构建高质量的 YOLOv8 训练数据集。
  * 开发文本解析模块，将科学论文、技术规程等文档自动化切分并转化为标准化的“知识块”（chunks）。
  * 提取并结构化农药使用剂量、安全间隔期等表格化数据。

* **第二阶段：高精度视觉诊断模块开发**
  * 编写模型训练脚本，完成 YOLOv8 模型的定制化微调与验证。
  * 实现视觉诊断推理接口，确保能够准确输出病虫害类别标签、置信度以及位置坐标。

* **第三阶段：多模态检索增强生成（MRAG）核心逻辑开发**
  * 编写代码集成 CLIP 等多模态嵌入模型，将文本块、图像统一编码为高维向量。
  * 部署并配置 FAISS 或 Milvus 向量数据库，开发向量存储与高效相似性检索（Top-K 召回）的核心代码。
  * 开发二次重排（Rerank）逻辑，并构建 Prompt 工程模块，将多模态上下文信息与用户查询打包，与多模态大语言模型（MLLM）进行接口对接与结果生成。

* **第四阶段：全栈系统集成与交互界面开发**
  * 后端开发：使用相关框架将视觉诊断模块和 MRAG 模块封装为稳定、高效的 API 服务。
  * 前端开发：构建 Web 前端应用程序，开发图像上传、文本交互以及图文并茂诊断报告渲染的用户界面。
  * 开发极简交互模式与离线功能，确保系统在离线状态下仍能调用本地核心知识库。

* **第五阶段：系统调优、测试与自动化迭代**
  * 针对复杂场景编写多维度检索过滤的代码逻辑，优化多模态语义对齐，提升检索精准度。
  * 进行系统级性能测试与并发调优，确保跨模态检索延迟控制在 1 秒以内。
  * 开发知识库自动更新接口，支持后续新文档和方案的动态接入。







berry-mrag-system/
├── data/                  # 存放原始数据和处理后的数据（记得在 .gitignore 中忽略大文件）
├── docs/                  # 团队知识库、需求文档、开题报告等
├── visual_module/         # A工作区：YOLOv8 训练、推理与 OpenCV 处理脚本
├── rag_module/            # B工作区：文本切块（chunks）、CLIP 编码、MLLM 交互 
├── backend/               # C工作区：FastAPI/Flask 应用，FAISS/Milvus 数据库交互 
├── frontend/              # D工作区：Web 前端代码 
├── requirements.txt       # 项目核心依赖包
└── README.md              # 项目简介与快速启动指南