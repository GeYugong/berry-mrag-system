import json
from typing import Any, Dict, List, Union
from urllib import parse, request
from urllib.error import HTTPError, URLError


def _fallback_markdown_report(
    user_query: str,
    detection: Dict[str, Union[str, float, list]],
    contexts: List[Dict[str, Union[str, float]]],
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
    contexts: List[Dict[str, Union[str, float]]],
) -> str:
    refs = []
    for idx, item in enumerate(contexts, start=1):
        refs.append(f"{idx}. {item['title']} (score={item['score']}): {item['content']}")

    return "\n".join(
        [
            "你是浆果病虫害诊断助手。请输出中文 Markdown，内容务必可执行、简洁、专业。",
            "结构必须包含：",
            "1) 诊断结论 2) 处置步骤 3) 用药与安全间隔提醒 4) 复查计划 5) 依据引用",
            "",
            f"用户问题：{user_query}",
            f"视觉检测：pest_type={detection.get('pest_type')}, confidence={detection.get('confidence')}, bbox={detection.get('bbox')}",
            "检索依据：",
            "\n".join(refs) if refs else "无检索依据",
        ]
    )


def _extract_gemini_text(resp: Dict[str, Any]) -> str:
    candidates = resp.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        return ""
    first = candidates[0]
    content = first.get("content", {})
    parts = content.get("parts", [])
    if not isinstance(parts, list):
        return ""
    texts: List[str] = []
    for part in parts:
        text = part.get("text")
        if isinstance(text, str) and text.strip():
            texts.append(text)
    return "\n".join(texts).strip()


def _generate_with_gemini(
    prompt: str,
    model: str,
    api_key: str,
    api_url: str,
    timeout: float,
    temperature: float,
) -> str:
    final_url = api_url.strip() or (
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    )
    if "?" in final_url:
        final_url = f"{final_url}&key={parse.quote(api_key)}"
    else:
        final_url = f"{final_url}?key={parse.quote(api_key)}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": float(temperature)},
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    req = request.Request(url=final_url, data=body, headers=headers, method="POST")

    with request.urlopen(req, timeout=float(timeout)) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        return ""
    return _extract_gemini_text(data)


def generate_markdown_report(
    user_query: str,
    detection: Dict[str, Union[str, float, list]],
    contexts: List[Dict[str, Union[str, float]]],
    llm_enabled: bool = True,
    llm_model: str = "gemini-2.0-flash",
    llm_api_key: str = "",
    llm_api_url: str = "",
    llm_timeout: float = 30.0,
    llm_temperature: float = 0.2,
) -> str:
    if not llm_enabled or not llm_api_key:
        return _fallback_markdown_report(user_query, detection, contexts)

    prompt = _build_prompt(user_query, detection, contexts)
    try:
        answer = _generate_with_gemini(
            prompt=prompt,
            model=llm_model,
            api_key=llm_api_key,
            api_url=llm_api_url,
            timeout=llm_timeout,
            temperature=llm_temperature,
        )
        if answer:
            return answer
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        pass

    return _fallback_markdown_report(user_query, detection, contexts)
