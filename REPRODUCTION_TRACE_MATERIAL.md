# Later two-hour reproduction traces

These are full, credential-redacted traces from the later fresh 120-minute
reproduction runs for Tasks 1 and 2. They are post-deadline, non-ranking
reference material. The official account results and the autonomous-only
prefix package remain separate and are not overwritten by this material.

The JSONL retains startup/organizer prompts, visible Agent messages, tool
calls, tool outputs, lifecycle events, and cumulative token telemetry.
Opaque encrypted reasoning is replaced by a placeholder; secrets and private
endpoints are redacted. The Task 1 final continuation is a preconfigured
runtime-resume template, not a human method or target-score instruction.

| Task | Trace events | User / assistant | Logical calls | `exec` calls | Tokens | Result |
|---|---:|---:|---:|---:|---:|---|
| task1 | 1398 | 3 / 72 | 17 | 264 | 40933816 | `55277782` / Public 0.74121 |
| task2 | 1067 | 2 / 61 | 40 | 176 | 29205639 | `55277682` / Public 0.675 |

## Scope and result separation

Do not use the scores in this table as the official final scores. They are
results produced by later fresh runs and were submitted after the official
competition deadline. For official account reconciliation, use
[`FINAL_SUBMISSION_RESULTS.md`](FINAL_SUBMISSION_RESULTS.md). For the strict
human-intervention-free material, use [`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json).

## task1

Competition: `ioai-2026-task-1-westlake-nlp-24`; account: `researai`.
Run window: `2026-08-05T16:25:50.693Z` to `2026-08-05T18:25:50.634Z`.
Official Kaggle deadline: `2026-08-05T10:50:00Z` (the run starts after it).
Trace: [`rollout.jsonl`](task1/evidence/reproduction-120m/rollout.jsonl) — 1398 events; SHA-256 `ee1f08c710402e2db9408eb6ec122b17ef1c8f8dd8d2b1aab21af71c0f9deb84`.

Prompt classes:

- `organizer_starter_prompt`: 1
- `preconfigured_runtime_resume_template`: 1
- `startup_instructions`: 1

Selected reproduction result: submission `55277782`, candidate `balanced_edge_fallback_v5`, Public LB `0.74121`, local CV `0.7676212811096714`.
Observed compute: {"accelerator": "NvidiaTeslaT4", "notebook_versions": 6, "observed_notebook_runtime_seconds": 1946.54, "observed_notebook_runtime_note": "Sum of the six recorded remote runtime fields: 62.48 + 83.02 + 315.35 + 600 + 285.69 + 600.", "gpu_cost_usd": null, "cost_status": "unavailable_no_invoice_or_rate"}

## task2

Competition: `ioai-2026-task-2-westlake-nlp-24`; account: `researai`.
Run window: `2026-08-05T16:20:09.021Z` to `2026-08-05T18:20:08.972Z`.
Official Kaggle deadline: `2026-08-05T07:35:00Z` (the run starts after it).
Trace: [`rollout.jsonl`](task2/evidence/reproduction-120m/rollout.jsonl) — 1067 events; SHA-256 `429c4a133ea7c661f48fdf4f547baf481a0fd12c209449d5804df662ee95d3a8`.

Prompt classes:

- `organizer_starter_prompt`: 1
- `startup_instructions`: 1

Selected reproduction result: submission `55277682`, candidate `tree_film_blend_65_35_full_labels`, Public LB `0.675`, local CV `0.6713888889`.
Observed compute: {"accelerator": "NvidiaTeslaT4", "gpu_versions": [2], "observed_gpu_runtime_seconds": 263.17, "cpu_versions": [1, 3], "observed_cpu_runtime_seconds": 441.25, "gpu_cost_usd": null, "cost_status": "unavailable_no_invoice_or_rate"}
