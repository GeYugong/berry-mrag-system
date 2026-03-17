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
            f"[{idx}] title={item.get('title','')} score={item.get('score','')} content={item.get('content','')}"
        )

    context_block = "\n".join(context_lines) if context_lines else "无可用检索上下文"
    return (
        "你是农业病虫害诊断助手。请基于提供的检索证据生成中文 Markdown 报告。\n"
        "要求：\n"
        "1) 只能依据给定证据，不确定就明确说明。\n"
        "2) 输出结构必须包含：诊断结果、检索依据、建议方案、注意事项。\n"
        "3) 建议方案要可执行，包含优先级与复查建议。\n"
        "4) 如涉及药剂，提醒按标签剂量与安全间隔期执行。\n\n"
        f"用户问题：{user_query}\n"
        f"视觉结果：pest_type={detection.get('pest_type')} confidence={detection.get('confidence')} bbox={detection.get('bbox')}\n"
        f"检索证据：\n{context_block}\n"
    )


def _call_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is empty")

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    base_url = os.getenv(
        "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
    ).rstrip("/")
    timeout_sec = float(os.getenv("GEMINI_TIMEOUT_SEC", "20"))
    temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.4"))

    url = f"{base_url}/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
        },
    }
    resp = requests.post(url, json=payload, timeout=timeout_sec)
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
    if provider == "gemini":
        try:
            prompt = _build_prompt(user_query, detection, contexts)
            return _call_gemini(prompt)
        except Exception:
            return _fallback_markdown(user_query, detection, contexts)
    return _fallback_markdown(user_query, detection, contexts)
