# Rollout Provenance and Redaction

The formal solver used an isolated Codex home inside the formal run directory.
The private originals below are not copied into this shareable package because
session metadata and tool output can contain credentials or private transport
configuration. Their SHA-256 hashes were taken before redaction:

| Role | Original filename | Original SHA-256 |
|---|---|---|
| Main solver | `rollout-2026-08-06T12-34-49-019fd55a-3edf-7801-b6a1-f1313393ff34.jsonl` | `86122f5e248c14a6ec8a767d5510d3dcb3e84c84e7cd47b487d23734bb2e785c` |
| Worker 1 | `rollout-2026-08-06T12-40-25-019fd55f-61f3-74c2-a87f-66ce5288dc56.jsonl` | `a9b518a97df12a376e3633859b92d7a8a20dedbfa8123e4f453a122131f11404` |
| Worker 2 | `rollout-2026-08-06T12-41-11-019fd560-1290-7bb1-af1d-8fd44c84aad5.jsonl` | `8585adfffd4b3064ef66a6f66f63787ddd8fc73b1f570945eef122e1c0fd94b6` |
| Worker 3 | `rollout-2026-08-06T12-41-42-019fd560-8eec-78c1-92c9-3ab2e67b1bd8.jsonl` | `1735693100b38bcd4c64b3d2e631d2a2d67b2de3581dd22ec0353628bbdef980` |

Original directory:

`/workspace/IOAI/ioai2-competition-runs-task3-formal-deadline-20260806T123442CST/ioai-2026-task-3-westlake-nlp-48/codex-home/sessions/2026/08/06`

`evidence/redact_rollouts.py` retains events whose top-level timestamp is no later
than `2026-08-06T05:46:19.450Z`, then redacts Kaggle/API credentials, known
private endpoints, and secret-valued metadata fields. The main copy contains 990
events and ends at 05:46:08.146Z. The three worker copies contain 690, 385, and
362 events and all end before the boundary.

The controlling conversation is distinct from the formal solver. A frozen
private copy used to extract the boundary event is stored outside this package at:

`/workspace/IOAI/_private-audit-raw/task3-20260806/controller-at-extraction.jsonl`

Its extraction-time SHA-256 is
`696149a81972717bcb066cdb60e5c7bad235bb83d6ddfdf4598d0852b8b67226`.
Only the exact redacted boundary message is exported into this package as
`SUPERVISION_BOUNDARY_EVENT.json`. The controlling conversation is not evidence
of what the solver received; the formal solver rollout is.

Because redaction changes bytes, verify the shareable copies against
`MANIFEST.sha256`, not against the private-original hashes above.
