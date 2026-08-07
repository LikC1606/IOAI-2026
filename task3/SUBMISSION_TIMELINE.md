# Autonomous Submission Timeline

Platform timestamps below come from `remote/KAGGLE_SUBMISSIONS_CURRENT.json`;
scores and statuses come from Kaggle, not from the agent's handwritten records.
All times are UTC on 2026-08-06. Add eight hours for CST.

| Kernel version | Submission ID | UTC submitted | Candidate | Local score recorded/reproduced | Public LB | Status |
|---:|---:|---|---|---:|---:|---|
| 1 | 55288941 | 04:46:56.707 | official starter | 92.58 | 32.50000 | COMPLETE |
| 2 | 55289364 | 05:08:22.643 | soft posterior + practice prior | 99.20 | 45.70000 | COMPLETE |
| 3 | 55289414 | 05:11:54.600 | bounded-sign posterior | 99.05 | 40.75000 | COMPLETE |
| 4 | 55289569 | 05:21:32.723 | calibrated soft posterior | 98.63 | **58.51666** | COMPLETE |
| 5 | 55289661 | 05:26:08.787 | practice-secret penalty | 90.72 | 45.70000 | COMPLETE |
| 6 | 55289751 | 05:32:01.070 | online likelihood calibration | 99.05 | 55.01666 | COMPLETE |
| 7 | 55289779 | 05:33:35.703 | interpolated soft likelihood | 98.95 | 54.11666 | COMPLETE |
| 8 | 55289823 | 05:35:41.457 | v4 likelihood without practice prior | 96.62 current reproduction | **58.51666** | COMPLETE |

The autonomy boundary is 05:46:19.450 UTC, more than ten minutes after v8 was
sent and scored. The filtered platform subset is stored at
`remote/KAGGLE_SUBMISSIONS_AUTONOMOUS_V1_V8.json`.

For every version, `remote/vN/submission.csv` was downloaded from the completed
remote Kernel. Verification confirms exactly two IDs (`leaderboard-a`,
`leaderboard-b`), identical base64 payloads, and byte-for-byte equality between
the decoded payload and `solutions/vN.py`. `remote/vN/kernel.log` confirms the
remote contract check and output generation.

v4 and v8 are two distinct source payloads with different SHA-256 hashes. Both
score 58.51666. v8 removes the practice-centroid initial prior while otherwise
retaining the calibrated soft-comparison route, supporting the autonomous
conclusion that the main gain came from robust likelihood/acquisition rather
than that prior.

The internal `research/records/submissions-before-supervision.jsonl` is included
as a contemporaneous decision/reflection log. It is secondary evidence: where a
manual log timestamp, local score, or status differs from a later mechanical
reproduction or platform record, the remote Kaggle record and exact artifact
control.
