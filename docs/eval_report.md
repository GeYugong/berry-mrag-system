# RAG 离线评测报告

- 生成时间：2026-03-17 10:30:48

## 模式：filtered

- Query 数：5
- Top-K：3
- Use Rerank：True
- Recall@K：1.0
- MRR@K：1.0
- nDCG@K：1.0
- 平均延迟(ms)：11926.84
- P95 延迟(ms)：25426.6

| id | Recall@K | MRR@K | nDCG@K | Latency(ms) | Retrieved | Gold |
|---|---:|---:|---:|---:|---|---|
| q-001 | 1.0 | 1.0 | 1.0 | 29898.21 | manual-001 | manual-001 |
| q-002 | 1.0 | 1.0 | 1.0 | 7400.35 | manual-002 | manual-002 |
| q-003 | 1.0 | 1.0 | 1.0 | 7540.16 | manual-003 | manual-003 |
| q-004 | 1.0 | 1.0 | 1.0 | 7362.35 | manual-001 | manual-001 |
| q-005 | 1.0 | 1.0 | 1.0 | 7433.12 | manual-002 | manual-002 |

## 模式：unfiltered

- Query 数：5
- Top-K：3
- Use Rerank：True
- Recall@K：1.0
- MRR@K：0.8667
- nDCG@K：0.9
- 平均延迟(ms)：7442.85
- P95 延迟(ms)：7546.4

| id | Recall@K | MRR@K | nDCG@K | Latency(ms) | Retrieved | Gold |
|---|---:|---:|---:|---:|---|---|
| q-001 | 1.0 | 1.0 | 1.0 | 7552.63 | manual-001, manual-003, manual-002 | manual-001 |
| q-002 | 1.0 | 1.0 | 1.0 | 7347.82 | manual-002, manual-003, manual-001 | manual-002 |
| q-003 | 1.0 | 1.0 | 1.0 | 7309.61 | manual-003, manual-002, manual-001 | manual-003 |
| q-004 | 1.0 | 1.0 | 1.0 | 7482.75 | manual-001, manual-002, manual-003 | manual-001 |
| q-005 | 1.0 | 0.3333 | 0.5 | 7521.47 | manual-003, manual-001, manual-002 | manual-002 |
