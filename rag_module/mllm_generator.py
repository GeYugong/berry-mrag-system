from typing import Dict, List, Union


def generate_markdown_report(
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
    return "\n".join(lines)#AFAF
