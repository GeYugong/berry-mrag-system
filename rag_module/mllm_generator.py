import os
from typing import Dict, List, Union

import requests


def _fallback_markdown(
    user_query: str,
    detection: Dict[str, Union[str, float, list]],
    contexts: List[Dict[str, object]],
) -> str:
    lines = [
        "# 浆果病虫害诊断建议",
        "",
        "## 诊断结果",
        f"- 疑似问题：`{detection['pest_type']}`",
        f"- 置信度：`{detection['confidence']}`",
        f"- 目标框：`{detection['bbox']}`",
        "",
        "## 用户问题",
        f"> {user_query}",
        "",
        "## 检索依据",
    ]

    for idx, item in enumerate(contexts, start=1):
        lines.append(
            f"{idx}. **{item['title']}** (score={item['score']}) - {item['content']}"
        )

    lines.extend(
        [
            "",
            "## 建议方案",
            "1. 先做田间复查，确认发病范围与进展速度。",
            "2. 优先执行农业与生物防治措施，化学药剂按标签剂量与安全间隔期使用。",
            "3. 3-5 天后复查并记录，必要时调整防治策略。",
        ]
    )
    return "\n".join(lines)


def _build_prompt(
    user_query: str,
    detection: Dict[str, Union[str, float, list]],
    contexts: List[Dict[str, object]],
) -> str:
    context_lines: List[str] = []
    for idx, item in enumerate(contexts, start=1):
        context_lines.append(
            f"[{idx}] 标题：{item.get('title','')} (相关性: {item.get('score','')})\n内容：{item.get('content','')}"
        )

    context_block = "\n---\n".join(context_lines) if context_lines else "未发现直接相关的历史防治手册。"
    
    return (
        "你是一名资深的智慧农业植物保护专家。请基于视觉诊断结果和检索到的知识库证据，为浆果种植户生成一份详尽、专业的中文 Markdown 诊断报告。\n\n"
        "### 写作约束：\n"
        "1. **结构化呈现**：必须严格遵循下方的[报告结构规范]。\n"
        "2. **依据为本**：所有防治药剂和剂量必须优先参考检索证据中的内容。若证据不足，请结合农业常识提供建议并注明‘专家经验补充’。\n"
        "3. **语气专业**：语气要冷静、严谨且充满人文关怀。使用专业的农技术语，但要配以通俗的解释。\n"
        "4. **排版精美**：充分利用 Markdown 特性（加粗、列表、表格、Emoji）。\n\n"
        "### [报告结构规范]：\n"
        "## 📊 诊断综合概要\n"
        "> (用一句话总结当前病害识别结果及其对作物的潜在威胁程度。)\n\n"
        "## 🩺 视觉与症状解析\n"
        "* **识别结果**：识别到 {pest_type}，视觉置信度为 {confidence}。\n"
        "* **用户描述反馈**：针对用户提到的‘{user_query}’进行专业解读。\n"
        "* **病理分析**：简述该病害的发病机理与当前症状的关联。\n\n"
        "## 🛡️ 核心防治体系\n"
        "### 1. 紧急处理方案 (Priority A)\n"
        "(侧重于快速阻断蔓延的措施。)\n"
        "### 2. 农业调控与生物防治 (Priority B)\n"
        "(侧重于环境控制，如通风、湿度调节等。)\n\n"
        "## 💊 推荐药剂与剂量参考\n"
        "| 推荐药剂 | 建议剂量/倍数 | 安全间隔期 | 使用要点 |\n"
        "| :--- | :--- | :--- | :--- |\n"
        "(基于检索证据填充表格，若证据中无详细参数则保留空白并提醒查阅药剂说明书。)\n\n"
        "## 🕒 后续管理与复查建议\n"
        "(明确告知农户 3-7 天内应观察的特征及下一步动作。)\n\n"
        "## ⚠️ 农业安全温馨提示\n"
        "(强调农药混配禁忌、施药防护及环境保护要求。)\n\n"
        "### [输入数据]：\n"
        f"1. 用户问题：{user_query}\n"
        f"2. 视觉指纹：pest_type={detection.get('pest_type')} confidence={detection.get('confidence')}\n"
        f"3. 知识库检索证据：\n{context_block}\n"
    ).format(
        pest_type=detection.get('pest_type'),
        confidence=f"{float(detection.get('confidence',0))*100:.1f}%",
        user_query=user_query
    )


def _call_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is empty")

    model = os.getenv("GEMINI_MODEL", "gemini-3.0-flash")
    base_url = os.getenv(
        "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
    ).rstrip("/")
    timeout_sec = float(os.getenv("GEMINI_TIMEOUT_SEC", "20"))
    temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.4"))

    # 支持从环境变量读取代理
    proxy_url = os.getenv("GEMINI_PROXY", "").strip()
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

    url = f"{base_url}/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
        },
    }

    # 使用代理进行请求
    resp = requests.post(url, json=payload, timeout=timeout_sec, proxies=proxies)
    resp.raise_for_status()
    data = resp.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini empty candidates")
    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(str(p.get("text", "")) for p in parts).strip()
    if not text:
        raise RuntimeError("Gemini empty text")
    return text


def generate_markdown_report(
    user_query: str,
    detection: Dict[str, Union[str, float, list]],
    contexts: List[Dict[str, object]],
) -> str:
    provider = os.getenv("GEN_PROVIDER", "template").strip().lower()
    print(f"[DEBUG] Current GEN_PROVIDER: {provider}")
    
    if provider == "gemini":
        try:
            prompt = _build_prompt(user_query, detection, contexts)
            print("[DEBUG] Calling Gemini API...")
            result = _call_gemini(prompt)
            print("[DEBUG] Gemini call successful.")
            return result
        except Exception as e:
            print(f"[DEBUG] Gemini Error: {str(e)}")
            print("[DEBUG] Falling back to template...")
            return _fallback_markdown(user_query, detection, contexts)
    
    print("[DEBUG] Using default template...")
    return _fallback_markdown(user_query, detection, contexts)
