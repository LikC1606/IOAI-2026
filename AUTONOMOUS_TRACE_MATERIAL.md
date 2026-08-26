# Autonomous competition trace material

This is the organizer-facing trace set for Tasks 1–6. It contains only
observable competition-agent execution before any live human intervention
prompt. Exclusion is causal: once a disallowed prompt arrives, that prompt
and every later event are omitted rather than deleting only the message.

Startup instructions, organizer prompts, inherited context, custom runtime
prompt text, and observable worker assignments are retained and classified.
No-live-human autonomy is not treated as proof of the separate exact-prompt
rule. Tasks 1, 2, and 4 contain custom prompt text and are disclosed as
non-exact; organizer/Jury recognition is not assumed. Hidden chain-of-thought
is not published.
The actual startup instruction payload for each task is indexed and hash-bound
in [`STARTUP_INSTRUCTION_INDEX.md`](STARTUP_INSTRUCTION_INDEX.md) and the
machine-readable [`STARTUP_INSTRUCTION_INDEX.json`](STARTUP_INSTRUCTION_INDEX.json).

Completeness here means completeness of the selected observable prefix, not
proof of competition-rule compliance. Tasks 1 and 2 do not bind the official
final result to an original autonomous trace. Method research is retained as
background provenance, and Task 6's evaluator-batch dependence is retained as
a measured technical behavior; neither is treated as a compliance blocker. See
`RULE_COMPLIANCE_AUDIT.md/json`.

For Tasks 1 and 2, complete raw formal sessions were subsequently recovered
in private local archives after a school-server restart. Their human-influenced
suffixes are intentionally unpublished; bounded formal prefixes remain separate
historical audit material, while the selected traces are later fresh reproductions
using the same configured solver/system and organizer constraints. See
`ORIGINAL_SESSION_RECOVERY.md/json`.

| Task | Trace files | Events | User prompts | Logical calls | Unfinished calls | Tokens | Boundary (exclusive UTC) |
|---|---:|---:|---:|---:|---:|---:|---|
| task1 | 1 | 1383 | 2 | 17 | 0 | 40830176 | 2026-08-05T18:25:04.940Z |
| task2 | 1 | 1067 | 2 | 40 | 0 | 29205639 | 2026-08-05T18:20:08.972Z |
| task3 | 4 | 2427 | 8 | 135 | 0 | 56373300 | 2026-08-06T05:46:19.450Z |
| task4 | 12 | 5881 | 50 | 198 | 2 | 244165721 | 2026-08-07T06:18:25.517Z |
| task5 | 14 | 4705 | 28 | 131 | 0 | 160243108 | 2026-08-07T09:04:20.519Z |
| task6 | 3 | 1868 | 6 | 54 | 0 | 41371859 | 2026-08-08T18:09:48.833Z |

Call-envelope audit found 2 call(s) whose output is absent
because the trace ends on that call at the declared capture boundary. Each
call ID and timestamp is recorded below and in the JSON index; orphan outputs,
duplicate IDs, out-of-order outputs, or unmatched calls away from the final
event are rejected by `verify_repository.py`.

Exact prompt hashes, per-trace SHA-256 values, tool-call counts, message
counts, and token counters are in
[`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json). Costs and
GPU runtimes are in [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json).
Verify the complete selected set with
[`AUTONOMOUS_MATERIAL_MANIFEST.sha256`](AUTONOMOUS_MATERIAL_MANIFEST.sha256).

## task1

Boundary: canonical causal solution prefix ends at task_complete; the complete later reproduction remains in the separate reproduction audit package.

Record recovery note: The complete raw formal Task 1 session was subsequently located in a private local archive after a school-server restart. Its human-influenced suffix is not published; a bounded pre-boundary formal prefix remains under task1/evidence/rollouts. The canonical trace is a later fresh reproduction using the same configured solver/system, official competition bundle, and organizer constraints. See ORIGINAL_SESSION_RECOVERY.md/json.

Strict exact organizer prompt text: **no**.
Prompt audit note: The reproduction starter contains a user-requested fresh-run-isolation appendix. The canonical solution prefix ends at task_complete and contains no continuation event, but the custom starter still prevents an exact-prompt-only claim. The full raw reproduction preserves the later post-solution continuation separately.

Included trace files:

- [`rollout-solution-prefix.jsonl`](task1/evidence/canonical/rollout-solution-prefix.jsonl) — 1383 events; call pairing `complete`; unfinished calls: none

Explicitly excluded:

- the 15-event suffix after task_complete, beginning with the post-solution custom continuation
- the complete 1,398-event reproduction remains available under task1/evidence/reproduction-120m and REPRODUCTION_TRACE_INDEX.json
- the official account's earlier deadline and all post-deadline scores are outside official-ranking scope
- the older formal-run prefix remains under task1/evidence/rollouts as historical audit material

## task2

Boundary: later two-hour reproduction deadline; no live human method/target prompt was delivered.

Record recovery note: The complete raw formal Task 2 session was subsequently located in a private local archive after a school-server restart. Its human-influenced suffix is not published; a bounded pre-boundary formal prefix remains under task2/evidence/rollouts. The canonical trace is a later fresh reproduction using the same configured solver/system, official competition bundle, and organizer constraints. See ORIGINAL_SESSION_RECOVERY.md/json.

Strict exact organizer prompt text: **no**.
Prompt audit note: The reproduction starter contains a user-requested fresh-run-isolation appendix; there is no continuation event in this reproduction.

Included trace files:

- [`rollout.jsonl`](task2/evidence/reproduction-120m/rollout.jsonl) — 1067 events; call pairing `complete`; unfinished calls: none

Explicitly excluded:

- events at or after the later two-hour reproduction deadline
- the official account's earlier deadline and all post-deadline scores are outside official-ranking scope
- the older formal-run prefix remains under task2/evidence/rollouts as historical audit material

## task3

Boundary: first non-read-only supervisory instruction received by the controlling session.

Strict exact organizer prompt text: **yes**.
Prompt audit note: All starter/continuation prompt events match the exact organizer text; no continuation was needed where none is present.

Included trace files:

- [`rollout-2026-08-06T12-34-49-019fd55a-3edf-7801-b6a1-f1313393ff34.jsonl`](task3/evidence/rollouts/rollout-2026-08-06T12-34-49-019fd55a-3edf-7801-b6a1-f1313393ff34.jsonl) — 990 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-06T12-40-25-019fd55f-61f3-74c2-a87f-66ce5288dc56.jsonl`](task3/evidence/rollouts/rollout-2026-08-06T12-40-25-019fd55f-61f3-74c2-a87f-66ce5288dc56.jsonl) — 690 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-06T12-41-11-019fd560-1290-7bb1-af1d-8fd44c84aad5.jsonl`](task3/evidence/rollouts/rollout-2026-08-06T12-41-11-019fd560-1290-7bb1-af1d-8fd44c84aad5.jsonl) — 385 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-06T12-41-42-019fd560-8eec-78c1-92c9-3ab2e67b1bd8.jsonl`](task3/evidence/rollouts/rollout-2026-08-06T12-41-42-019fd560-8eec-78c1-92c9-3ab2e67b1bd8.jsonl) — 362 events; call pairing `complete`; unfinished calls: none

Explicitly excluded:

- all events at or after the supervision boundary at 05:46:19.450Z

## task4

Boundary: run deadline; no live human method or target prompt was delivered to the solver.

Strict exact organizer prompt text: **no**.
Prompt audit note: The injected starter has formatting changes and the main-runtime continuation events use a substantive generic workflow template rather than the exact organizer Continuation Prompt. The final selected submission is downstream of those events; the complete selection includes the supplemental parallel-solver traces.

Included trace files:

- [`rollout-2026-08-07T12-18-29-019fda71-a6a2-7a22-8c18-22e99f127422.jsonl`](task4/evidence/rollouts/rollout-2026-08-07T12-18-29-019fda71-a6a2-7a22-8c18-22e99f127422.jsonl) — 1549 events; call pairing `incomplete_at_capture_boundary`; unfinished calls: `call_WBf0RTIKAETcSi6JGnKXfF9S` (custom_tool_call)
- [`rollout-2026-08-07T12-18-41-019fda71-d4eb-70a3-9b66-e0fb3b2d0e66.jsonl`](task4/evidence/rollouts/rollout-2026-08-07T12-18-41-019fda71-d4eb-70a3-9b66-e0fb3b2d0e66.jsonl) — 229 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T12-18-47-019fda71-effd-7321-8ce9-2a4a57fcaa48.jsonl`](task4/evidence/rollouts/rollout-2026-08-07T12-18-47-019fda71-effd-7321-8ce9-2a4a57fcaa48.jsonl) — 239 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T13-21-43-019fdaab-8d94-76a0-b625-078c838b5227.jsonl`](task4/evidence/rollouts/rollout-2026-08-07T13-21-43-019fdaab-8d94-76a0-b625-078c838b5227.jsonl) — 351 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T13-21-51-019fdaab-ace4-7b51-93b2-244d9517423a.jsonl`](task4/evidence/rollouts/rollout-2026-08-07T13-21-51-019fdaab-ace4-7b51-93b2-244d9517423a.jsonl) — 349 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T13-04-06-019fda9b-6b63-7031-a6dd-52db684209be.jsonl`](task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-06-019fda9b-6b63-7031-a6dd-52db684209be.jsonl) — 997 events; call pairing `incomplete_at_capture_boundary`; unfinished calls: `call_eNISCiGsdfwyEhbSnydlqGCc` (function_call)
- [`rollout-2026-08-07T13-04-23-019fda9b-ade0-7912-868f-a922606fd40f.jsonl`](task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-23-019fda9b-ade0-7912-868f-a922606fd40f.jsonl) — 449 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T13-04-30-019fda9b-c906-70a0-8f5c-99fc2f25fafa.jsonl`](task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-30-019fda9b-c906-70a0-8f5c-99fc2f25fafa.jsonl) — 460 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T13-04-39-019fda9b-ed93-7473-96c5-f8c030d3e4bc.jsonl`](task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-39-019fda9b-ed93-7473-96c5-f8c030d3e4bc.jsonl) — 255 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T13-57-14-019fdacc-1073-7f03-ac6e-346ad63c0c4f.jsonl`](task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-57-14-019fdacc-1073-7f03-ac6e-346ad63c0c4f.jsonl) — 297 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T13-57-22-019fdacc-2e9c-78a2-b037-135a4b172944.jsonl`](task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-57-22-019fdacc-2e9c-78a2-b037-135a4b172944.jsonl) — 377 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T13-57-28-019fdacc-47fe-7bc3-8cac-d77f25b124e1.jsonl`](task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-57-28-019fdacc-47fe-7bc3-8cac-d77f25b124e1.jsonl) — 329 events; call pairing `complete`; unfinished calls: none

Explicitly excluded:

- events at or after the run deadline

## task5

Boundary: run deadline; controller status questions were not solver inputs.

Strict exact organizer prompt text: **yes**.
Prompt audit note: All starter/continuation prompt events match the exact organizer text; no continuation was needed where none is present.

Included trace files:

- [`rollout-2026-08-07T15-04-23-019fdb09-8b16-7032-82e1-21be10be17c0.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-04-23-019fdb09-8b16-7032-82e1-21be10be17c0.jsonl) — 1230 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T15-10-16-019fdb0e-ece5-75f1-a919-0cf4bc532838.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-10-16-019fdb0e-ece5-75f1-a919-0cf4bc532838.jsonl) — 167 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T15-10-32-019fdb0f-2ccc-7d80-b97f-3e6891df20be.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-10-32-019fdb0f-2ccc-7d80-b97f-3e6891df20be.jsonl) — 153 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T15-10-46-019fdb0f-641d-71f1-aad9-71a76ad14bb3.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-10-46-019fdb0f-641d-71f1-aad9-71a76ad14bb3.jsonl) — 202 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T15-23-21-019fdb1a-e97c-7542-b5b9-eb65046b1e4c.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-23-21-019fdb1a-e97c-7542-b5b9-eb65046b1e4c.jsonl) — 221 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T15-35-11-019fdb25-bcda-76b3-aa61-bf745122bb27.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-35-11-019fdb25-bcda-76b3-aa61-bf745122bb27.jsonl) — 256 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T15-35-25-019fdb25-f27d-7fc0-a235-ef2d4e1b9e14.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-35-25-019fdb25-f27d-7fc0-a235-ef2d4e1b9e14.jsonl) — 226 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T15-36-47-019fdb27-333f-7002-84f3-83c19536e1a2.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-36-47-019fdb27-333f-7002-84f3-83c19536e1a2.jsonl) — 241 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T15-58-45-019fdb3b-4f7e-70b2-b652-940314651df4.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-58-45-019fdb3b-4f7e-70b2-b652-940314651df4.jsonl) — 337 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T15-58-59-019fdb3b-85ff-7f63-9981-952915290c13.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-58-59-019fdb3b-85ff-7f63-9981-952915290c13.jsonl) — 253 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T15-59-18-019fdb3b-d220-74b3-9fce-c89b25442543.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-59-18-019fdb3b-d220-74b3-9fce-c89b25442543.jsonl) — 264 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T16-05-40-019fdb41-a587-7410-8926-ba38fb7da71d.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T16-05-40-019fdb41-a587-7410-8926-ba38fb7da71d.jsonl) — 402 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T16-23-09-019fdb51-a930-7953-9c40-be02d0c93136.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T16-23-09-019fdb51-a930-7953-9c40-be02d0c93136.jsonl) — 396 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-07T16-23-36-019fdb52-12da-7931-b44c-82fe30560795.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T16-23-36-019fdb52-12da-7931-b44c-82fe30560795.jsonl) — 357 events; call pairing `complete`; unfinished calls: none

Explicitly excluded:

- events at or after the run deadline

## task6

Boundary: first human-triggered resume prompt delivered after the autonomous start.

Strict exact organizer prompt text: **yes**.
Prompt audit note: All starter/continuation prompt events match the exact organizer text; no continuation was needed where none is present.

Included trace files:

- [`rollout-2026-08-09T00-23-24-019fe22f-b2b8-7191-a6ec-39dea000da9f-autonomous-prefix.jsonl`](task6/evidence/autonomous-only/rollout-2026-08-09T00-23-24-019fe22f-b2b8-7191-a6ec-39dea000da9f-autonomous-prefix.jsonl) — 1173 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-09T00-23-42-019fe22f-f897-7d10-b27c-2c6586c55a27.jsonl`](task6/evidence/rollouts/rollout-2026-08-09T00-23-42-019fe22f-f897-7d10-b27c-2c6586c55a27.jsonl) — 346 events; call pairing `complete`; unfinished calls: none
- [`rollout-2026-08-09T00-30-10-019fe235-e3a2-7173-bac5-0ba0451f279f.jsonl`](task6/evidence/rollouts/rollout-2026-08-09T00-30-10-019fe235-e3a2-7173-bac5-0ba0451f279f.jsonl) — 349 events; call pairing `complete`; unfinished calls: none

Explicitly excluded:

- main-trace events at or after 18:09:48.833Z
- the later human target-score prompt at 18:14:21.148Z and everything after it
- two worker traces spawned after the human-triggered resume
