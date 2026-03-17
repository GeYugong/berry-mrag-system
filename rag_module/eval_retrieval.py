import argparse
import json
import math
import statistics
import time
from pathlib import Path
from typing import Dict, List, Sequence

from rag_module.embedder import embed_text
from rag_module.reranker import rerank
from rag_module.retriever import search


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Offline retrieval evaluation for berry RAG module."
    )
    parser.add_argument(
        "--eval-file",
        type=str,
        default="docs/eval_queries.example.jsonl",
        help="Path to eval queries jsonl.",
    )
    parser.add_argument("--top-k", type=int, default=3, help="Top-K for retrieval metrics.")
    parser.add_argument(
        "--mode",
        type=str,
        default="both",
        choices=["filtered", "unfiltered", "both"],
        help="Evaluate with metadata filter, without filter, or both.",
    )
    parser.add_argument(
        "--use-rerank",
        action="store_true",
        help="Apply reranker after retrieval before metrics.",
    )
    parser.add_argument(
        "--out-json",
        type=str,
        default="data/vector_store/eval_report.json",
        help="Output json report path.",
    )
    parser.add_argument(
        "--out-md",
        type=str,
        default="docs/eval_report.md",
        help="Output markdown report path.",
    )
    return parser.parse_args()


def _load_eval_data(path: Path) -> List[Dict[str, object]]:
    if not path.exists():
        raise FileNotFoundError(f"Eval file not found: {path}")

    rows: List[Dict[str, object]] = []
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSONL at line {idx}: {e}") from e
            if not isinstance(item, dict):
                continue
            if not item.get("query"):
                continue
            gold = item.get("gold_doc_ids", [])
            if not isinstance(gold, list):
                gold = []
            item["gold_doc_ids"] = [str(x) for x in gold]
            rows.append(item)

    if not rows:
        raise ValueError("Eval dataset is empty.")
    return rows


def _recall_at_k(retrieved_ids: Sequence[str], gold_ids: Sequence[str], k: int) -> float:
    if not gold_ids:
        return 0.0
    hit = len(set(retrieved_ids[:k]) & set(gold_ids))
    return hit / len(set(gold_ids))


def _mrr_at_k(retrieved_ids: Sequence[str], gold_ids: Sequence[str], k: int) -> float:
    gold = set(gold_ids)
    for idx, doc_id in enumerate(retrieved_ids[:k], start=1):
        if doc_id in gold:
            return 1.0 / idx
    return 0.0


def _ndcg_at_k(retrieved_ids: Sequence[str], gold_ids: Sequence[str], k: int) -> float:
    gold = set(gold_ids)
    dcg = 0.0
    for i, doc_id in enumerate(retrieved_ids[:k], start=1):
        rel = 1.0 if doc_id in gold else 0.0
        if rel > 0:
            dcg += rel / math.log2(i + 1)
    ideal_hits = min(len(gold), k)
    if ideal_hits == 0:
        return 0.0
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
    return dcg / idcg if idcg > 0 else 0.0


def _percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    vals = sorted(values)
    if len(vals) == 1:
        return vals[0]
    rank = (p / 100.0) * (len(vals) - 1)
    low = int(math.floor(rank))
    high = int(math.ceil(rank))
    if low == high:
        return vals[low]
    w = rank - low
    return vals[low] * (1 - w) + vals[high] * w


def _evaluate(dataset: List[Dict[str, object]], top_k: int, use_filter: bool, use_rerank: bool) -> Dict[str, object]:
    per_query: List[Dict[str, object]] = []
    recalls: List[float] = []
    mrrs: List[float] = []
    ndcgs: List[float] = []
    latencies_ms: List[float] = []

    for i, row in enumerate(dataset, start=1):
        query = str(row.get("query", ""))
        crop = str(row.get("crop", "")) if row.get("crop") is not None else ""
        disease_hint = str(row.get("disease_hint", "")) if row.get("disease_hint") is not None else ""
        gold_ids = [str(x) for x in row.get("gold_doc_ids", [])]  # type: ignore[arg-type]
        query_id = str(row.get("id", f"q-{i:03d}"))

        t0 = time.perf_counter()
        query_vec = embed_text(query)
        if use_filter:
            retrieved = search(query_vec, top_k=top_k, crop=crop or None, disease_hint=disease_hint or None)
        else:
            retrieved = search(query_vec, top_k=top_k)

        if use_rerank:
            retrieved = rerank(
                retrieved,
                pest_type=disease_hint or "unknown_leaf_issue",
                crop=crop or None,
                disease_hint=disease_hint or None,
            )[:top_k]

        latency_ms = (time.perf_counter() - t0) * 1000
        latencies_ms.append(latency_ms)

        retrieved_ids = [str(x.get("id", "")) for x in retrieved]
        recall = _recall_at_k(retrieved_ids, gold_ids, top_k)
        mrr = _mrr_at_k(retrieved_ids, gold_ids, top_k)
        ndcg = _ndcg_at_k(retrieved_ids, gold_ids, top_k)

        recalls.append(recall)
        mrrs.append(mrr)
        ndcgs.append(ndcg)

        per_query.append(
            {
                "id": query_id,
                "query": query,
                "crop": crop,
                "disease_hint": disease_hint,
                "gold_doc_ids": gold_ids,
                "retrieved_doc_ids": retrieved_ids,
                "recall_at_k": round(recall, 4),
                "mrr_at_k": round(mrr, 4),
                "ndcg_at_k": round(ndcg, 4),
                "latency_ms": round(latency_ms, 2),
            }
        )

    summary = {
        "queries": len(dataset),
        "top_k": top_k,
        "use_rerank": use_rerank,
        "recall_at_k": round(statistics.mean(recalls), 4) if recalls else 0.0,
        "mrr_at_k": round(statistics.mean(mrrs), 4) if mrrs else 0.0,
        "ndcg_at_k": round(statistics.mean(ndcgs), 4) if ndcgs else 0.0,
        "latency_ms_avg": round(statistics.mean(latencies_ms), 2) if latencies_ms else 0.0,
        "latency_ms_p95": round(_percentile(latencies_ms, 95), 2),
    }
    return {"summary": summary, "per_query": per_query}


def _render_markdown(report: Dict[str, object], out_path: Path) -> None:
    generated_at = time.strftime("%Y-%m-%d %H:%M:%S")
    lines: List[str] = [
        "# RAG 离线评测报告",
        "",
        f"- 生成时间：{generated_at}",
        "",
    ]

    for mode_name in ["filtered", "unfiltered"]:
        if mode_name not in report:
            continue
        data = report[mode_name]
        summary = data["summary"]
        lines.extend(
            [
                f"## 模式：{mode_name}",
                "",
                f"- Query 数：{summary['queries']}",
                f"- Top-K：{summary['top_k']}",
                f"- Use Rerank：{summary['use_rerank']}",
                f"- Recall@K：{summary['recall_at_k']}",
                f"- MRR@K：{summary['mrr_at_k']}",
                f"- nDCG@K：{summary['ndcg_at_k']}",
                f"- 平均延迟(ms)：{summary['latency_ms_avg']}",
                f"- P95 延迟(ms)：{summary['latency_ms_p95']}",
                "",
                "| id | Recall@K | MRR@K | nDCG@K | Latency(ms) | Retrieved | Gold |",
                "|---|---:|---:|---:|---:|---|---|",
            ]
        )
        for row in data["per_query"]:
            lines.append(
                f"| {row['id']} | {row['recall_at_k']} | {row['mrr_at_k']} | "
                f"{row['ndcg_at_k']} | {row['latency_ms']} | "
                f"{', '.join(row['retrieved_doc_ids'])} | {', '.join(row['gold_doc_ids'])} |"
            )
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = _parse_args()
    dataset = _load_eval_data(Path(args.eval_file))

    report: Dict[str, object] = {}
    if args.mode in ("filtered", "both"):
        report["filtered"] = _evaluate(dataset, top_k=args.top_k, use_filter=True, use_rerank=args.use_rerank)
    if args.mode in ("unfiltered", "both"):
        report["unfiltered"] = _evaluate(dataset, top_k=args.top_k, use_filter=False, use_rerank=args.use_rerank)

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    _render_markdown(report, Path(args.out_md))
    print(f"Eval done. JSON -> {out_json}, Markdown -> {args.out_md}")


if __name__ == "__main__":
    main()
