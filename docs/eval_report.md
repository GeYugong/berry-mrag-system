# RAG 离线评测报告

- 生成时间：2026-03-17 10:22:59

## 模式：filtered

- Query 数：5
- Top-K：3
- Recall@K：1.0
- MRR@K：1.0
- nDCG@K：1.0
- 平均延迟(ms)：11999.57
- P95 延迟(ms)：25626.54

| id | Recall@K | MRR@K | nDCG@K | Latency(ms) | Retrieved | Gold |
|---|---:|---:|---:|---:|---|---|
| q-001 | 1.0 | 1.0 | 1.0 | 30146.23 | manual-001 | manual-001 |
| q-002 | 1.0 | 1.0 | 1.0 | 7345.69 | manual-002 | manual-002 |
| q-003 | 1.0 | 1.0 | 1.0 | 7547.79 | manual-003 | manual-003 |
| q-004 | 1.0 | 1.0 | 1.0 | 7517.49 | manual-001 | manual-001 |
| q-005 | 1.0 | 1.0 | 1.0 | 7440.65 | manual-002 | manual-002 |

## 模式：unfiltered

- Query 数：5
- Top-K：3
- Recall@K：1.0
- MRR@K：0.6333
- nDCG@K：0.7262
- 平均延迟(ms)：7484.02
- P95 延迟(ms)：7637.16

| id | Recall@K | MRR@K | nDCG@K | Latency(ms) | Retrieved | Gold |
|---|---:|---:|---:|---:|---|---|
| q-001 | 1.0 | 1.0 | 1.0 | 7352.82 | manual-001, manual-003, manual-002 | manual-001 |
| q-002 | 1.0 | 0.3333 | 0.5 | 7332.3 | manual-003, manual-001, manual-002 | manual-002 |
| q-003 | 1.0 | 0.5 | 0.6309 | 7656.08 | manual-002, manual-003, manual-001 | manual-003 |
| q-004 | 1.0 | 1.0 | 1.0 | 7561.46 | manual-001, manual-002, manual-003 | manual-001 |
| q-005 | 1.0 | 0.3333 | 0.5 | 7517.45 | manual-003, manual-001, manual-002 | manual-002 |
