import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


def _disease_specs() -> List[Dict[str, object]]:
    return [
        {
            "key": "powdery_mildew",
            "name_cn": "白粉病",
            "crops": ["草莓", "蓝莓", "覆盆子"],
            "symptoms": [
                "叶片表面出现白色粉末状霉层，后期叶片卷曲",
                "幼叶与果梗出现粉状斑，通风不良时快速扩展",
                "果面有白粉覆盖，商品果率下降",
            ],
            "measures": [
                "优先改善棚内通风并降低夜间湿度",
                "清除重病叶并带出田间集中处理",
                "发病初期轮换使用三唑类与硫制剂，避免单一药剂连续使用",
            ],
            "pesticides": [
                ("15%三唑酮可湿性粉剂", "1500倍液", "7-10天"),
                ("25%戊唑醇悬浮剂", "2000倍液", "7天"),
                ("40%腈菌唑乳油", "3000倍液", "7-10天"),
            ],
        },
        {
            "key": "aphid",
            "name_cn": "蚜虫",
            "crops": ["草莓", "蓝莓", "黑莓"],
            "symptoms": [
                "嫩叶背面聚集绿色小虫并伴随蜜露",
                "新梢卷缩，生长点发育迟缓",
                "叶片发黏，后续易诱发煤污病",
            ],
            "measures": [
                "优先用黄板监测与诱杀，降低虫口基数",
                "保护瓢虫、草蛉等天敌，减少广谱药冲击",
                "若虫高峰期分区施药并轮换作用机制",
            ],
            "pesticides": [
                ("10%吡虫啉可湿性粉剂", "2000倍液", "5-7天"),
                ("22.4%螺虫乙酯悬浮剂", "4000倍液", "7天"),
                ("50%抗蚜威可湿性粉剂", "2500倍液", "5天"),
            ],
        },
        {
            "key": "gray_mold",
            "name_cn": "灰霉病",
            "crops": ["草莓", "蓝莓", "覆盆子"],
            "symptoms": [
                "果面出现灰色霉层并逐步软腐",
                "花器与幼果先发病，阴雨后扩展明显",
                "采后短时间内出现腐烂和水渍状病斑",
            ],
            "measures": [
                "花期前后控制湿度并加强通风",
                "及时清除病残花和病果，减少再侵染源",
                "开花前至坐果期进行预防性用药并轮换药剂",
            ],
            "pesticides": [
                ("50%腐霉利可湿性粉剂", "1000倍液", "7天"),
                ("40%嘧霉胺悬浮剂", "1200倍液", "7天"),
                ("25%啶酰菌胺水分散粒剂", "1500倍液", "7-10天"),
            ],
        },
    ]


def _chunk_record(
    idx: int,
    disease_key: str,
    disease_name: str,
    crop: str,
    symptom: str,
    measure: str,
    pesticide: str,
    dose: str,
    interval: str,
    variant: int,
) -> Dict[str, object]:
    return {
        "id": f"exp-{disease_key}-{idx:03d}",
        "title": f"{crop}{disease_name}防治要点V{variant}",
        "content": (
            f"病征：{symptom}。"
            f"\n管理措施：{measure}。"
            f"\n推荐药剂：{pesticide}，{dose}，安全间隔期{interval}。"
        ),
        "source": "synthetic_expansion_v1",
        "crop": crop,
        "disease_cn": disease_name,
        "disease_en": disease_key,
        "symptom": symptom,
        "treatments": [measure, f"{pesticide} {dose}"],
        "pesticide": pesticide,
        "dose": f"{pesticide}{dose}",
        "interval_days": interval,
        "keywords": [crop, disease_name, disease_key, "病害防治", "剂量", "安全间隔期"],
    }


def _query_templates() -> List[str]:
    return [
        "{crop}{disease_name}怎么防治",
        "{crop}出现{symptom}怎么办",
        "{disease_name}推荐药剂和剂量",
        "{crop}{disease_name}安全间隔期多久",
        "{crop}棚里{disease_name}反复发生怎么处理",
        "请给出{crop}{disease_name}综合治理方案",
        "{disease_name}高湿天气下怎么控",
        "{crop}{disease_name}早期识别与应对",
        "{crop}果面异常，疑似{disease_name}，如何处理",
        "{disease_name}要不要马上打药",
    ]


def build_dataset() -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    chunks: List[Dict[str, object]] = []
    eval_queries: List[Dict[str, object]] = []

    q_templates = _query_templates()
    for spec in _disease_specs():
        disease_key = str(spec["key"])
        disease_name = str(spec["name_cn"])
        crops = list(spec["crops"])
        symptoms = list(spec["symptoms"])
        measures = list(spec["measures"])
        pesticides = list(spec["pesticides"])

        # 生成 chunk：每个病害 30 条（3作物 * 10变体）
        local_idx = 1
        for crop in crops:
            for variant in range(1, 11):
                symptom = symptoms[(variant - 1) % len(symptoms)]
                measure = measures[(variant - 1) % len(measures)]
                pesticide, dose, interval = pesticides[(variant - 1) % len(pesticides)]
                rec = _chunk_record(
                    idx=local_idx,
                    disease_key=disease_key,
                    disease_name=disease_name,
                    crop=str(crop),
                    symptom=str(symptom),
                    measure=str(measure),
                    pesticide=str(pesticide),
                    dose=str(dose),
                    interval=str(interval),
                    variant=variant,
                )
                chunks.append(rec)
                local_idx += 1

        # 评测问句：每病害 60 条（3作物 * 10模板 * 2轮）
        qid = 1
        gold_doc_id = f"exp-{disease_key}-001"
        for repeat in range(2):
            for crop in crops:
                for i, tpl in enumerate(q_templates):
                    symptom = symptoms[(i + repeat) % len(symptoms)]
                    eval_queries.append(
                        {
                            "id": f"eq-{disease_key}-{qid:03d}",
                            "query": tpl.format(
                                crop=crop, disease_name=disease_name, symptom=symptom
                            ),
                            "crop": crop,
                            "disease_hint": disease_key,
                            "gold_doc_ids": [gold_doc_id],
                        }
                    )
                    qid += 1

    return chunks, eval_queries


def save_jsonl(rows: List[Dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate expanded synthetic RAG dataset.")
    parser.add_argument(
        "--chunks-out",
        default="data/chunks/rag_chunks_expanded.jsonl",
        help="Output path for expanded chunk dataset.",
    )
    parser.add_argument(
        "--eval-out",
        default="docs/eval_queries.expanded.jsonl",
        help="Output path for expanded eval queries.",
    )
    parser.add_argument(
        "--docs-chunks-copy",
        default="docs/rag_chunks_expanded.jsonl",
        help="Tracked copy of chunks under docs.",
    )
    args = parser.parse_args()

    chunks, eval_queries = build_dataset()
    save_jsonl(chunks, Path(args.chunks_out))
    save_jsonl(eval_queries, Path(args.eval_out))
    save_jsonl(chunks, Path(args.docs_chunks_copy))
    print(
        f"Expanded dataset generated: chunks={len(chunks)}, eval_queries={len(eval_queries)}"
    )
    print(f"chunks -> {args.chunks_out}")
    print(f"eval_queries -> {args.eval_out}")


if __name__ == "__main__":
    main()
