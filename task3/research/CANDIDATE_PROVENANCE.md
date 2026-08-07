# Pre-Boundary Candidate Provenance

The files under `research/candidates` were copied during the audit from the formal
project. Inclusion was based on the original filesystem modification time being
strictly earlier than the 2026-08-06 13:46:19.450 CST supervision boundary, then
cross-checked against pre-boundary rollout tool/patch evidence. Copying changed
their visible mtimes inside this package, so the table below records the relevant
original chronology at lane level.

| Original time range (CST) | Lane | Preserved evidence |
|---|---|---|
| 12:40:16 | deployable baseline | official starter source |
| 12:41:59-13:35:43 | soft belief | evaluators, synthetic-shift probes, multiple executable belief variants, `RESULTS.md` |
| 12:50:35-13:07:48 | robust rank | robustness experiment, bounded-rank implementation, `RESULTS.md` |
| 12:56:46-13:11:29 | query balance | acquisition implementation, evaluator, `RESULTS.md` |
| 13:03:39-13:42:55 | prior/likelihood | initial route, v2/v4/v7/v8/v9 candidates, penalty probes, and pre-boundary v10 source |
| 13:09:54 | rank-prior integration | executable integrated source |
| 13:30:39 | online calibration | executable integrated source |

The exact scored sources are not inferred from these working candidates. They are
decoded independently from remote CSVs into `solutions/v1.py` through `v8.py`.
Candidate artifacts show the autonomous research breadth and implementation
process; remote payloads and Kaggle records establish what was actually submitted.

`lane_prior/v10_soft15.py` is the only preserved working candidate that did not
produce an included scored result. It was created at 13:42:55 CST and is retained
as research-process evidence only.

No file first created at or after the boundary is copied into this candidate
snapshot. Later Task 3 routes are outside this package and are not inspected.
