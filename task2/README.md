# Task 2 Autonomous Evidence

Competition: `ioai-2026-task-2-westlake-nlp-24`.

For the consolidated rule, artifact, report-correction, and reproduction audit,
start with `COMPLIANCE.md`.

The formal solver began at 05:30:32 UTC. Before the conservative autonomy
boundary it received only the injected startup instructions, the organizer
Starter Prompt once, and the exact organizer Continuation Prompt once. The first
modified Continue arrived at 06:24:47.549 UTC. That input, its unpublished body,
and every later action are excluded.

The submission timeline around the boundary is:

| Submission | UTC | Candidate | Public LB |
|---:|---|---|---:|
| 55260462 | 06:09:48.697 | rotation CNN v1 | 0.55055 |
| 55260695 | 06:19:10.890 | rotation CNN v2 | 0.55416 |
| 55261432 | 06:46:18.437 | structured ExtraTrees v1 | 0.63583 (official final; outside autonomous scope) |

`remote/KAGGLE_SUBMISSIONS_ELIGIBLE.json` is the platform-derived positive set.
The best eligible result is rotation CNN v2 at **0.55416**. Its exact remote
source, log, metadata, and 7,200-row output were re-downloaded with Kaggle CLI.
The later tree research is retained only under the excluded snapshot area.

Separately, the organizer-requested Kaggle extraction establishes the account's
official final result as `55261432`, Public 0.63583 / Private 0.62500, before
the official `07:35:00Z` Kaggle deadline. It is not attributed to the bounded
human-intervention-free trace.

Kaggle now exposes a still later post-boundary tree version as the current
private Kernel but returns HTTP 403 for a historical `/1` pull. That snapshot
and the frozen pre-submit tree sources are isolated as excluded evidence. They
are not used to support the eligible 0.55416 claim.

The excluded tree submission description says validation 0.625833, while its
preserved candidate receipt reports 0.546944. The discrepancy remains disclosed
for audit but has no bearing on the positive score claim.

All modified/custom prompts at or after the boundary and every causally
downstream event are outside this autonomous claim. Their bodies are not part
of the organizer-facing trace material.

## Later 120-minute reproduction

The requested later fresh run is preserved separately at
[`evidence/reproduction-120m/rollout.jsonl`](evidence/reproduction-120m/rollout.jsonl),
with counts, prompt classification, token telemetry, runtime, and result in the
root [`REPRODUCTION_TRACE_INDEX.json`](../REPRODUCTION_TRACE_INDEX.json). Its
best scored candidate was `tree_film_blend_65_35_full_labels`, submission
`55277682` (Public LB `0.675`). This run is post-deadline and non-ranking; it
does not replace the bounded autonomous trace or the official account result.
