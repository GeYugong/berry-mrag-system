import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


SECTION_PATTERN = re.compile(r"^##\s*(.+)$")
TITLE_META_PATTERN = re.compile(r"^\s*(?:\d+\.)?\s*([^\(]+?)(?:\s*\(([^)]+)\))?\s*$")
INTERVAL_PATTERN = re.compile(r"(\d+\s*[-~]\s*\d+\s*天|\d+\s*天)")
DOSE_PATTERN = re.compile(r"(\d+\s*%\s*[^，。；]*?\d+\s*倍液)")

KNOWN_CROPS = ["草莓", "蓝莓", "覆盆子", "树莓", "黑莓"]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build structured RAG chunks from berry manual markdown."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="docs/berry_manual.md",
        help="Input manual markdown path.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/chunks/berry_manual_chunks.jsonl",
        help="Output chunks jsonl path.",
    )
    return parser.parse_args()


def _split_sections(md_text: str) -> List[Tuple[str, List[str]]]:
    sections: List[Tuple[str, List[str]]] = []
    current_title: Optional[str] = None
    current_lines: List[str] = []

    for line in md_text.splitlines():
        section_match = SECTION_PATTERN.match(line.strip())
        if section_match:
            if current_title is not None:
                sections.append((current_title, current_lines))
            current_title = section_match.group(1).strip()
            current_lines = []
            continue
        if current_title is not None:
            current_lines.append(line.rstrip())

    if current_title is not None:
        sections.append((current_title, current_lines))
    return sections


def _extract_title_meta(title: str) -> Tuple[str, str, str]:
    match = TITLE_META_PATTERN.match(title.strip())
    if not match:
        return title.strip(), "", ""

    disease_cn = match.group(1).strip()
    disease_en = (match.group(2) or "").strip().lower().replace(" ", "_")
    crop = ""
    for name in KNOWN_CROPS:
        if disease_cn.startswith(name):
            crop = name
            break
    return disease_cn, disease_en, crop


def _extract_field(prefix: str, lines: List[str]) -> str:
    for line in lines:
        line = line.strip()
        if line.startswith(prefix):
            return line.split(":", 1)[-1].strip()
    return ""


def _extract_treatments(lines: List[str]) -> List[str]:
    treatments: List[str] = []
    capture = False
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- **防治方案**"):
            capture = True
            continue
        if capture and line.startswith("- "):
            treatments.append(line[2:].strip())
    return treatments


def _extract_interval(text: str) -> str:
    match = INTERVAL_PATTERN.search(text)
    return match.group(1).replace(" ", "") if match else ""


def _extract_dose(treatments: List[str]) -> str:
    for line in treatments:
        match = DOSE_PATTERN.search(line)
        if match:
            return match.group(1).replace(" ", "")
    return ""


def _extract_pesticide(treatments: List[str]) -> str:
    # Heuristic for common lines like "使用 15% 三唑酮可湿性粉剂 1500 倍液喷雾。"
    for line in treatments:
        for key in ["可湿性粉剂", "悬浮剂", "水分散粒剂", "乳油"]:
            if key in line:
                left = line.split(key, 1)[0]
                left = (
                    left.replace("药剂推荐", "")
                    .replace("推荐使用", "")
                    .replace("使用", "")
                    .replace("喷施", "")
                    .strip(" ，。:：")
                )
                return f"{left}{key}".strip()
    return ""


def _build_chunk(idx: int, title: str, lines: List[str], source_path: str) -> Dict[str, object]:
    disease_cn, disease_en, crop = _extract_title_meta(title)
    symptom = _extract_field("- **病征**", lines)
    treatments = _extract_treatments(lines)
    treatments_text = "；".join(treatments)
    interval = _extract_interval("\n".join(lines))
    dose = _extract_dose(treatments)
    pesticide = _extract_pesticide(treatments)

    content_parts = []
    if symptom:
        content_parts.append(f"病征：{symptom}")
    if treatments:
        content_parts.append(f"防治方案：{treatments_text}")
    content = "\n".join(content_parts).strip()

    chunk: Dict[str, object] = {
        "id": f"manual-{idx:03d}",
        "title": disease_cn or title.strip(),
        "content": content,
        "source": source_path,
        "crop": crop,
        "disease_cn": disease_cn,
        "disease_en": disease_en,
        "symptom": symptom,
        "treatments": treatments,
        "pesticide": pesticide,
        "dose": dose,
        "interval_days": interval,
        "keywords": [x for x in [crop, disease_cn, disease_en] if x],
    }
    return chunk


def build_chunks(input_path: Path) -> List[Dict[str, object]]:
    text = input_path.read_text(encoding="utf-8")
    sections = _split_sections(text)
    chunks: List[Dict[str, object]] = []
    for idx, (title, lines) in enumerate(sections, start=1):
        chunk = _build_chunk(idx=idx, title=title, lines=lines, source_path=input_path.as_posix())
        if str(chunk.get("content", "")).strip():
            chunks.append(chunk)
    return chunks


def save_jsonl(chunks: List[Dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for item in chunks:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def main() -> None:
    args = _parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.exists():
        raise FileNotFoundError(f"Input markdown not found: {input_path}")

    chunks = build_chunks(input_path)
    save_jsonl(chunks, output_path)
    print(f"Built chunks: {len(chunks)} -> {output_path}")


if __name__ == "__main__":
    main()
