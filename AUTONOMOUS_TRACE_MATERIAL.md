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

For Tasks 1 and 2, the original run records were unavailable after a
school-server restart; the selected traces are later fresh reproductions
using the same configured solver/system and organizer constraints.

| Task | Trace files | Events | User prompts | Logical calls | Tokens | Boundary (exclusive UTC) |
|---|---:|---:|---:|---:|---:|---|
| task1 | 1 | 1398 | 3 | 17 | 40933816 | 2026-08-05T18:25:50.634Z |
| task2 | 1 | 1067 | 2 | 40 | 29205639 | 2026-08-05T18:20:08.972Z |
| task3 | 4 | 2427 | 8 | 135 | 56373300 | 2026-08-06T05:46:19.450Z |
| task4 | 5 | 2717 | 20 | 75 | 109119898 | 2026-08-07T06:18:25.517Z |
| task5 | 14 | 4705 | 28 | 131 | 160243108 | 2026-08-07T09:04:20.519Z |
| task6 | 3 | 1868 | 6 | 54 | 41371859 | 2026-08-08T18:09:48.833Z |

Exact prompt hashes, per-trace SHA-256 values, tool-call counts, message
counts, and token counters are in
[`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json). Costs and
GPU runtimes are in [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json).
Verify the complete selected set with
[`AUTONOMOUS_MATERIAL_MANIFEST.sha256`](AUTONOMOUS_MATERIAL_MANIFEST.sha256).

## task1

Boundary: later two-hour reproduction deadline; no live human method/target prompt was delivered.

Record recovery note: The original Task 1 run record was unavailable after a school-server restart. The canonical trace is a later fresh reproduction using the same configured solver/system, official competition bundle, and organizer constraints; it is not the original run record.

Strict exact organizer prompt text: **no**.
Prompt audit note: The reproduction starter contains a user-requested fresh-run-isolation appendix. Its custom continuation occurs after the selected submission, final Agent answer, and task_complete event, but the custom starter still prevents an exact-prompt-only claim.

Included trace files:

- [`rollout.jsonl`](task1/evidence/reproduction-120m/rollout.jsonl) — 1398 events

Explicitly excluded:

- events at or after the later two-hour reproduction deadline
- the official account's earlier deadline and all post-deadline scores are outside official-ranking scope
- the older formal-run prefix remains under task1/evidence/rollouts as historical audit material

## task2

Boundary: later two-hour reproduction deadline; no live human method/target prompt was delivered.

Record recovery note: The original Task 2 run record was unavailable after a school-server restart. The canonical trace is a later fresh reproduction using the same configured solver/system, official competition bundle, and organizer constraints; it is not the original run record.

Strict exact organizer prompt text: **no**.
Prompt audit note: The reproduction starter contains a user-requested fresh-run-isolation appendix; there is no continuation event in this reproduction.

Included trace files:

- [`rollout.jsonl`](task2/evidence/reproduction-120m/rollout.jsonl) — 1067 events

Explicitly excluded:

- events at or after the later two-hour reproduction deadline
- the official account's earlier deadline and all post-deadline scores are outside official-ranking scope
- the older formal-run prefix remains under task2/evidence/rollouts as historical audit material

## task3

Boundary: first non-read-only supervisory instruction received by the controlling session.

Strict exact organizer prompt text: **yes**.
Prompt audit note: All starter/continuation prompt events match the exact organizer text; no continuation was needed where none is present.

Included trace files:

- [`rollout-2026-08-06T12-34-49-019fd55a-3edf-7801-b6a1-f1313393ff34.jsonl`](task3/evidence/rollouts/rollout-2026-08-06T12-34-49-019fd55a-3edf-7801-b6a1-f1313393ff34.jsonl) — 990 events
- [`rollout-2026-08-06T12-40-25-019fd55f-61f3-74c2-a87f-66ce5288dc56.jsonl`](task3/evidence/rollouts/rollout-2026-08-06T12-40-25-019fd55f-61f3-74c2-a87f-66ce5288dc56.jsonl) — 690 events
- [`rollout-2026-08-06T12-41-11-019fd560-1290-7bb1-af1d-8fd44c84aad5.jsonl`](task3/evidence/rollouts/rollout-2026-08-06T12-41-11-019fd560-1290-7bb1-af1d-8fd44c84aad5.jsonl) — 385 events
- [`rollout-2026-08-06T12-41-42-019fd560-8eec-78c1-92c9-3ab2e67b1bd8.jsonl`](task3/evidence/rollouts/rollout-2026-08-06T12-41-42-019fd560-8eec-78c1-92c9-3ab2e67b1bd8.jsonl) — 362 events

Explicitly excluded:

- all events at or after the supervision boundary at 05:46:19.450Z

## task4

Boundary: run deadline; no live human method or target prompt was delivered to the solver.

Strict exact organizer prompt text: **no**.
Prompt audit note: The injected starter has formatting changes and the six main-runtime continuation events use a substantive generic workflow template rather than the exact organizer Continuation Prompt. The final selected submission is downstream of those events.

Included trace files:

- [`rollout-2026-08-07T12-18-29-019fda71-a6a2-7a22-8c18-22e99f127422.jsonl`](task4/evidence/rollouts/rollout-2026-08-07T12-18-29-019fda71-a6a2-7a22-8c18-22e99f127422.jsonl) — 1549 events
- [`rollout-2026-08-07T12-18-41-019fda71-d4eb-70a3-9b66-e0fb3b2d0e66.jsonl`](task4/evidence/rollouts/rollout-2026-08-07T12-18-41-019fda71-d4eb-70a3-9b66-e0fb3b2d0e66.jsonl) — 229 events
- [`rollout-2026-08-07T12-18-47-019fda71-effd-7321-8ce9-2a4a57fcaa48.jsonl`](task4/evidence/rollouts/rollout-2026-08-07T12-18-47-019fda71-effd-7321-8ce9-2a4a57fcaa48.jsonl) — 239 events
- [`rollout-2026-08-07T13-21-43-019fdaab-8d94-76a0-b625-078c838b5227.jsonl`](task4/evidence/rollouts/rollout-2026-08-07T13-21-43-019fdaab-8d94-76a0-b625-078c838b5227.jsonl) — 351 events
- [`rollout-2026-08-07T13-21-51-019fdaab-ace4-7b51-93b2-244d9517423a.jsonl`](task4/evidence/rollouts/rollout-2026-08-07T13-21-51-019fdaab-ace4-7b51-93b2-244d9517423a.jsonl) — 349 events

Explicitly excluded:

- events at or after the run deadline

## task5

Boundary: run deadline; controller status questions were not solver inputs.

Strict exact organizer prompt text: **yes**.
Prompt audit note: All starter/continuation prompt events match the exact organizer text; no continuation was needed where none is present.

Included trace files:

- [`rollout-2026-08-07T15-04-23-019fdb09-8b16-7032-82e1-21be10be17c0.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-04-23-019fdb09-8b16-7032-82e1-21be10be17c0.jsonl) — 1230 events
- [`rollout-2026-08-07T15-10-16-019fdb0e-ece5-75f1-a919-0cf4bc532838.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-10-16-019fdb0e-ece5-75f1-a919-0cf4bc532838.jsonl) — 167 events
- [`rollout-2026-08-07T15-10-32-019fdb0f-2ccc-7d80-b97f-3e6891df20be.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-10-32-019fdb0f-2ccc-7d80-b97f-3e6891df20be.jsonl) — 153 events
- [`rollout-2026-08-07T15-10-46-019fdb0f-641d-71f1-aad9-71a76ad14bb3.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-10-46-019fdb0f-641d-71f1-aad9-71a76ad14bb3.jsonl) — 202 events
- [`rollout-2026-08-07T15-23-21-019fdb1a-e97c-7542-b5b9-eb65046b1e4c.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-23-21-019fdb1a-e97c-7542-b5b9-eb65046b1e4c.jsonl) — 221 events
- [`rollout-2026-08-07T15-35-11-019fdb25-bcda-76b3-aa61-bf745122bb27.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-35-11-019fdb25-bcda-76b3-aa61-bf745122bb27.jsonl) — 256 events
- [`rollout-2026-08-07T15-35-25-019fdb25-f27d-7fc0-a235-ef2d4e1b9e14.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-35-25-019fdb25-f27d-7fc0-a235-ef2d4e1b9e14.jsonl) — 226 events
- [`rollout-2026-08-07T15-36-47-019fdb27-333f-7002-84f3-83c19536e1a2.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-36-47-019fdb27-333f-7002-84f3-83c19536e1a2.jsonl) — 241 events
- [`rollout-2026-08-07T15-58-45-019fdb3b-4f7e-70b2-b652-940314651df4.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-58-45-019fdb3b-4f7e-70b2-b652-940314651df4.jsonl) — 337 events
- [`rollout-2026-08-07T15-58-59-019fdb3b-85ff-7f63-9981-952915290c13.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-58-59-019fdb3b-85ff-7f63-9981-952915290c13.jsonl) — 253 events
- [`rollout-2026-08-07T15-59-18-019fdb3b-d220-74b3-9fce-c89b25442543.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T15-59-18-019fdb3b-d220-74b3-9fce-c89b25442543.jsonl) — 264 events
- [`rollout-2026-08-07T16-05-40-019fdb41-a587-7410-8926-ba38fb7da71d.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T16-05-40-019fdb41-a587-7410-8926-ba38fb7da71d.jsonl) — 402 events
- [`rollout-2026-08-07T16-23-09-019fdb51-a930-7953-9c40-be02d0c93136.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T16-23-09-019fdb51-a930-7953-9c40-be02d0c93136.jsonl) — 396 events
- [`rollout-2026-08-07T16-23-36-019fdb52-12da-7931-b44c-82fe30560795.jsonl`](task5/evidence/rollouts/rollout-2026-08-07T16-23-36-019fdb52-12da-7931-b44c-82fe30560795.jsonl) — 357 events

Explicitly excluded:

- events at or after the run deadline

## task6

Boundary: first human-triggered resume prompt delivered after the autonomous start.

Strict exact organizer prompt text: **yes**.
Prompt audit note: All starter/continuation prompt events match the exact organizer text; no continuation was needed where none is present.

Included trace files:

- [`rollout-2026-08-09T00-23-24-019fe22f-b2b8-7191-a6ec-39dea000da9f-autonomous-prefix.jsonl`](task6/evidence/autonomous-only/rollout-2026-08-09T00-23-24-019fe22f-b2b8-7191-a6ec-39dea000da9f-autonomous-prefix.jsonl) — 1173 events
- [`rollout-2026-08-09T00-23-42-019fe22f-f897-7d10-b27c-2c6586c55a27.jsonl`](task6/evidence/rollouts/rollout-2026-08-09T00-23-42-019fe22f-f897-7d10-b27c-2c6586c55a27.jsonl) — 346 events
- [`rollout-2026-08-09T00-30-10-019fe235-e3a2-7173-bac5-0ba0451f279f.jsonl`](task6/evidence/rollouts/rollout-2026-08-09T00-30-10-019fe235-e3a2-7173-bac5-0ba0451f279f.jsonl) — 349 events

Explicitly excluded:

- main-trace events at or after 18:09:48.833Z
- the later human target-score prompt at 18:14:21.148Z and everything after it
- two worker traces spawned after the human-triggered resume
