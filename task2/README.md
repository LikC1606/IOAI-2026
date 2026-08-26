# Task 2 Autonomous Evidence

Competition: `ioai-2026-task-2-westlake-nlp-24`.

For the cross-task checklist and official-result reconciliation, start with
`../ORGANIZER_SUBMISSION.md` and `../FINAL_SUBMISSION_RESULTS.md`. For this
task's evidence, start with `COMPLIANCE.md`, `SUMMARY.json`, and
`AUTONOMY_BOUNDARY.md`.

## Record recovery note

The complete raw formal Task 2 session was subsequently located in a private
local archive after a school-server restart. Because its 662-event suffix
starts with a modified human continuation, the public package intentionally
retains only the bounded 705-event pre-boundary formal prefix under
`evidence/rollouts/`; its provenance hashes are recorded in
`ROLLOUT_PROVENANCE.json` and the root
[`ORIGINAL_SESSION_RECOVERY.md`](../ORIGINAL_SESSION_RECOVERY.md). The canonical trace in
`evidence/reproduction-120m/` is a later fresh reproduction using the same
configured solver/system, official competition bundle, and organizer
constraints. It is a reproduction record, not a replacement for the recovered
private formal session, and its post-deadline status remains explicit below.

The canonical published no-live-human rollout is
the complete later two-hour trace under `evidence/reproduction-120m/`; the
earlier formal run is retained as separate historical audit material.
The machine-readable cross-task audit is
[`../FORMAL_PREFIX_AUDIT.md`](../FORMAL_PREFIX_AUDIT.md): it records 705
events, exact Starter and Continuation Prompt conformance, the exclusive
`2026-08-05T06:24:47.549Z` boundary, and the eligible pre-boundary v2
submission `55260695` (Public `0.55416`, Private `0.54833`).

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
`55277682` (Public LB `0.675`). This is the canonical no-live-human autonomous
rollout for Task 2, but it is post-deadline and non-ranking; it does not replace
the official account result.

Prompt-text qualification: the reproduction starter appends a custom
fresh-run-isolation section, and no continuation occurs in that trace. The run
is disclosed as no-live-human but not strict exact-organizer-prompt text; see
`../PROMPT_CONFORMANCE_AUDIT.md`.
