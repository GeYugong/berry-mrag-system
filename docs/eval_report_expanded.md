# RAG 离线评测报告

- 生成时间：2026-03-17 13:39:39

## 模式：filtered

- Query 数：30
- Top-K：3
- Use Rerank：True
- Recall@K：0.0333
- MRR@K：0.0167
- nDCG@K：0.021
- 平均延迟(ms)：30548.41
- P95 延迟(ms)：7549.55

| id | Recall@K | MRR@K | nDCG@K | Latency(ms) | Retrieved | Gold |
|---|---:|---:|---:|---:|---|---|
| eq-powdery_mildew-001 | 0.0 | 0.0 | 0.0 | 700897.37 | exp-powdery_mildew-009, exp-powdery_mildew-010, exp-powdery_mildew-002 | exp-powdery_mildew-001 |
| eq-powdery_mildew-002 | 0.0 | 0.0 | 0.0 | 7488.23 | exp-powdery_mildew-005, exp-powdery_mildew-010, exp-powdery_mildew-009 | exp-powdery_mildew-001 |
| eq-powdery_mildew-003 | 0.0 | 0.0 | 0.0 | 7350.6 | exp-powdery_mildew-008, exp-powdery_mildew-007, exp-powdery_mildew-010 | exp-powdery_mildew-001 |
| eq-powdery_mildew-004 | 0.0 | 0.0 | 0.0 | 7443.89 | exp-powdery_mildew-005, exp-powdery_mildew-009, exp-powdery_mildew-008 | exp-powdery_mildew-001 |
| eq-powdery_mildew-005 | 0.0 | 0.0 | 0.0 | 7500.32 | exp-powdery_mildew-009, exp-powdery_mildew-004, exp-powdery_mildew-010 | exp-powdery_mildew-001 |
| eq-powdery_mildew-006 | 0.0 | 0.0 | 0.0 | 7385.48 | exp-powdery_mildew-009, exp-powdery_mildew-007, exp-powdery_mildew-004 | exp-powdery_mildew-001 |
| eq-powdery_mildew-007 | 1.0 | 0.5 | 0.6309 | 7546.93 | exp-powdery_mildew-004, exp-powdery_mildew-001, exp-powdery_mildew-008 | exp-powdery_mildew-001 |
| eq-powdery_mildew-008 | 0.0 | 0.0 | 0.0 | 7288.84 | exp-powdery_mildew-005, exp-powdery_mildew-007, exp-powdery_mildew-004 | exp-powdery_mildew-001 |
| eq-powdery_mildew-009 | 0.0 | 0.0 | 0.0 | 7425.08 | exp-powdery_mildew-006, exp-powdery_mildew-010, exp-powdery_mildew-007 | exp-powdery_mildew-001 |
| eq-powdery_mildew-010 | 0.0 | 0.0 | 0.0 | 7541.78 | exp-powdery_mildew-004, manual-001, exp-powdery_mildew-008 | exp-powdery_mildew-001 |
| eq-powdery_mildew-011 | 0.0 | 0.0 | 0.0 | 7377.85 | exp-powdery_mildew-012, exp-powdery_mildew-016, exp-powdery_mildew-017 | exp-powdery_mildew-001 |
| eq-powdery_mildew-012 | 0.0 | 0.0 | 0.0 | 7359.01 | exp-powdery_mildew-017, exp-powdery_mildew-019, exp-powdery_mildew-015 | exp-powdery_mildew-001 |
| eq-powdery_mildew-013 | 0.0 | 0.0 | 0.0 | 7338.14 | exp-powdery_mildew-014, exp-powdery_mildew-013, exp-powdery_mildew-011 | exp-powdery_mildew-001 |
| eq-powdery_mildew-014 | 0.0 | 0.0 | 0.0 | 7518.35 | exp-powdery_mildew-011, exp-powdery_mildew-019, exp-powdery_mildew-018 | exp-powdery_mildew-001 |
| eq-powdery_mildew-015 | 0.0 | 0.0 | 0.0 | 7476.35 | exp-powdery_mildew-014, exp-powdery_mildew-017, exp-powdery_mildew-015 | exp-powdery_mildew-001 |
| eq-powdery_mildew-016 | 0.0 | 0.0 | 0.0 | 7507.28 | exp-powdery_mildew-013, exp-powdery_mildew-014, exp-powdery_mildew-012 | exp-powdery_mildew-001 |
| eq-powdery_mildew-017 | 0.0 | 0.0 | 0.0 | 7382.51 | exp-powdery_mildew-014, exp-powdery_mildew-017, exp-powdery_mildew-015 | exp-powdery_mildew-001 |
| eq-powdery_mildew-018 | 0.0 | 0.0 | 0.0 | 7369.79 | exp-powdery_mildew-012, exp-powdery_mildew-013, exp-powdery_mildew-016 | exp-powdery_mildew-001 |
| eq-powdery_mildew-019 | 0.0 | 0.0 | 0.0 | 7471.96 | exp-powdery_mildew-014, exp-powdery_mildew-018, exp-powdery_mildew-016 | exp-powdery_mildew-001 |
| eq-powdery_mildew-020 | 0.0 | 0.0 | 0.0 | 7459.4 | exp-powdery_mildew-014, exp-powdery_mildew-011, exp-powdery_mildew-020 | exp-powdery_mildew-001 |
| eq-powdery_mildew-021 | 0.0 | 0.0 | 0.0 | 7429.02 | exp-powdery_mildew-023, exp-powdery_mildew-021, exp-powdery_mildew-025 | exp-powdery_mildew-001 |
| eq-powdery_mildew-022 | 0.0 | 0.0 | 0.0 | 7507.69 | exp-powdery_mildew-030, exp-powdery_mildew-028, exp-powdery_mildew-024 | exp-powdery_mildew-001 |
| eq-powdery_mildew-023 | 0.0 | 0.0 | 0.0 | 7343.16 | exp-powdery_mildew-023, exp-powdery_mildew-024, exp-powdery_mildew-030 | exp-powdery_mildew-001 |
| eq-powdery_mildew-024 | 0.0 | 0.0 | 0.0 | 7529.84 | exp-powdery_mildew-025, exp-powdery_mildew-023, exp-powdery_mildew-021 | exp-powdery_mildew-001 |
| eq-powdery_mildew-025 | 0.0 | 0.0 | 0.0 | 7397.71 | exp-powdery_mildew-026, exp-powdery_mildew-024, exp-powdery_mildew-025 | exp-powdery_mildew-001 |
| eq-powdery_mildew-026 | 0.0 | 0.0 | 0.0 | 7376.9 | exp-powdery_mildew-028, exp-powdery_mildew-023, exp-powdery_mildew-029 | exp-powdery_mildew-001 |
| eq-powdery_mildew-027 | 0.0 | 0.0 | 0.0 | 7463.17 | exp-powdery_mildew-027, exp-powdery_mildew-030, exp-powdery_mildew-024 | exp-powdery_mildew-001 |
| eq-powdery_mildew-028 | 0.0 | 0.0 | 0.0 | 7551.7 | exp-powdery_mildew-024, exp-powdery_mildew-027, exp-powdery_mildew-026 | exp-powdery_mildew-001 |
| eq-powdery_mildew-029 | 0.0 | 0.0 | 0.0 | 7365.97 | exp-powdery_mildew-028, exp-powdery_mildew-030, exp-powdery_mildew-022 | exp-powdery_mildew-001 |
| eq-powdery_mildew-030 | 0.0 | 0.0 | 0.0 | 7358.07 | exp-powdery_mildew-021, exp-powdery_mildew-023, exp-powdery_mildew-025 | exp-powdery_mildew-001 |

## 模式：unfiltered

- Query 数：30
- Top-K：3
- Use Rerank：True
- Recall@K：0.0333
- MRR@K：0.0333
- nDCG@K：0.0333
- 平均延迟(ms)：7467.93
- P95 延迟(ms)：7602.87

| id | Recall@K | MRR@K | nDCG@K | Latency(ms) | Retrieved | Gold |
|---|---:|---:|---:|---:|---|---|
| eq-powdery_mildew-001 | 0.0 | 0.0 | 0.0 | 7517.19 | exp-aphid-021, exp-gray_mold-024, exp-aphid-029 | exp-powdery_mildew-001 |
| eq-powdery_mildew-002 | 0.0 | 0.0 | 0.0 | 7337.31 | exp-powdery_mildew-019, exp-powdery_mildew-013, manual-002 | exp-powdery_mildew-001 |
| eq-powdery_mildew-003 | 0.0 | 0.0 | 0.0 | 7310.86 | exp-powdery_mildew-014, exp-gray_mold-002, exp-gray_mold-004 | exp-powdery_mildew-001 |
| eq-powdery_mildew-004 | 0.0 | 0.0 | 0.0 | 7503.34 | exp-powdery_mildew-013, exp-gray_mold-029, exp-gray_mold-015 | exp-powdery_mildew-001 |
| eq-powdery_mildew-005 | 0.0 | 0.0 | 0.0 | 7498.6 | exp-aphid-004, exp-gray_mold-018, exp-gray_mold-023 | exp-powdery_mildew-001 |
| eq-powdery_mildew-006 | 0.0 | 0.0 | 0.0 | 7408.07 | exp-aphid-003, exp-aphid-026, exp-aphid-015 | exp-powdery_mildew-001 |
| eq-powdery_mildew-007 | 0.0 | 0.0 | 0.0 | 7598.93 | exp-powdery_mildew-004, exp-gray_mold-007, exp-aphid-012 | exp-powdery_mildew-001 |
| eq-powdery_mildew-008 | 0.0 | 0.0 | 0.0 | 7353.91 | exp-aphid-012, exp-aphid-009, exp-aphid-015 | exp-powdery_mildew-001 |
| eq-powdery_mildew-009 | 0.0 | 0.0 | 0.0 | 7606.09 | exp-powdery_mildew-020, exp-aphid-009, exp-gray_mold-026 | exp-powdery_mildew-001 |
| eq-powdery_mildew-010 | 0.0 | 0.0 | 0.0 | 7485.66 | exp-powdery_mildew-021, exp-gray_mold-002, exp-aphid-025 | exp-powdery_mildew-001 |
| eq-powdery_mildew-011 | 0.0 | 0.0 | 0.0 | 7439.22 | exp-powdery_mildew-012, exp-gray_mold-012, exp-gray_mold-021 | exp-powdery_mildew-001 |
| eq-powdery_mildew-012 | 0.0 | 0.0 | 0.0 | 7492.86 | exp-powdery_mildew-017, exp-aphid-003, manual-002 | exp-powdery_mildew-001 |
| eq-powdery_mildew-013 | 0.0 | 0.0 | 0.0 | 7524.57 | exp-powdery_mildew-014, exp-gray_mold-002, exp-gray_mold-004 | exp-powdery_mildew-001 |
| eq-powdery_mildew-014 | 0.0 | 0.0 | 0.0 | 7528.0 | exp-powdery_mildew-011, exp-powdery_mildew-010, exp-gray_mold-019 | exp-powdery_mildew-001 |
| eq-powdery_mildew-015 | 0.0 | 0.0 | 0.0 | 7528.45 | exp-powdery_mildew-014, exp-powdery_mildew-017, exp-gray_mold-029 | exp-powdery_mildew-001 |
| eq-powdery_mildew-016 | 0.0 | 0.0 | 0.0 | 7366.7 | exp-gray_mold-005, exp-aphid-026, exp-aphid-001 | exp-powdery_mildew-001 |
| eq-powdery_mildew-017 | 0.0 | 0.0 | 0.0 | 7382.92 | exp-powdery_mildew-004, exp-aphid-012, exp-gray_mold-007 | exp-powdery_mildew-001 |
| eq-powdery_mildew-018 | 0.0 | 0.0 | 0.0 | 7634.06 | exp-aphid-022, exp-aphid-030, exp-aphid-028 | exp-powdery_mildew-001 |
| eq-powdery_mildew-019 | 0.0 | 0.0 | 0.0 | 7473.67 | exp-powdery_mildew-027, exp-aphid-013, exp-aphid-021 | exp-powdery_mildew-001 |
| eq-powdery_mildew-020 | 0.0 | 0.0 | 0.0 | 7447.45 | exp-powdery_mildew-021, exp-aphid-025, exp-gray_mold-002 | exp-powdery_mildew-001 |
| eq-powdery_mildew-021 | 0.0 | 0.0 | 0.0 | 7513.36 | exp-powdery_mildew-023, exp-gray_mold-012, exp-aphid-019 | exp-powdery_mildew-001 |
| eq-powdery_mildew-022 | 0.0 | 0.0 | 0.0 | 7362.8 | exp-powdery_mildew-012, exp-gray_mold-016, exp-gray_mold-019 | exp-powdery_mildew-001 |
| eq-powdery_mildew-023 | 0.0 | 0.0 | 0.0 | 7537.44 | exp-powdery_mildew-014, exp-gray_mold-002, exp-gray_mold-004 | exp-powdery_mildew-001 |
| eq-powdery_mildew-024 | 0.0 | 0.0 | 0.0 | 7566.64 | exp-powdery_mildew-015, exp-gray_mold-028, exp-aphid-003 | exp-powdery_mildew-001 |
| eq-powdery_mildew-025 | 0.0 | 0.0 | 0.0 | 7305.74 | exp-powdery_mildew-026, exp-aphid-017, exp-aphid-001 | exp-powdery_mildew-001 |
| eq-powdery_mildew-026 | 0.0 | 0.0 | 0.0 | 7550.92 | exp-powdery_mildew-028, exp-gray_mold-014, exp-aphid-009 | exp-powdery_mildew-001 |
| eq-powdery_mildew-027 | 0.0 | 0.0 | 0.0 | 7380.71 | exp-powdery_mildew-004, exp-aphid-012, exp-gray_mold-007 | exp-powdery_mildew-001 |
| eq-powdery_mildew-028 | 1.0 | 1.0 | 1.0 | 7382.67 | exp-powdery_mildew-001, exp-gray_mold-011, exp-gray_mold-018 | exp-powdery_mildew-001 |
| eq-powdery_mildew-029 | 0.0 | 0.0 | 0.0 | 7428.88 | exp-powdery_mildew-012, exp-powdery_mildew-003, exp-gray_mold-021 | exp-powdery_mildew-001 |
| eq-powdery_mildew-030 | 0.0 | 0.0 | 0.0 | 7570.94 | exp-powdery_mildew-021, exp-aphid-025, exp-gray_mold-002 | exp-powdery_mildew-001 |
