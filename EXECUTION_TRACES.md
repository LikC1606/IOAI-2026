# Agent execution traces: Tasks 1–6

This is the published organizer-facing execution package. It selects the
observable trace prefix for each task before the first live human intervention
prompt. The single entry point is
[`ORGANIZER_SUBMISSION.md`](ORGANIZER_SUBMISSION.md).

The machine-readable index is [`EXECUTION_TRACE_INDEX.json`](EXECUTION_TRACE_INDEX.json);
individual credential-redacted JSONL files are under each task's evidence
directory. The autonomous-specific classification, prompt hashes, boundaries,
and exclusion records are in [`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json).

The requested later fresh two-hour Task 1/2 runs are published in
[`REPRODUCTION_TRACE_MATERIAL.md`](REPRODUCTION_TRACE_MATERIAL.md). Task 1's
canonical solution selection is its exact prefix through `task_complete`, while
the full raw stream remains in the reproduction package; Task 2 uses its full
later trace.
They remain post-deadline, non-ranking traces for official-score purposes and
must not be read as the official account result.
The complete raw formal Task 1 and Task 2 sessions were subsequently recovered
in private local archives after a school-server restart. Their human-influenced
suffixes are intentionally withheld; bounded pre-boundary formal prefixes remain
as separate historical audit evidence. Those two selected traces are later fresh
reproductions using the same configured solver/system, official competition
bundle, and organizer constraints, not replacements for the incomplete
original records. See [`FORMAL_PREFIX_AUDIT.md`](FORMAL_PREFIX_AUDIT.md).

## Supplemental formal prefixes for Tasks 1–2

These are intentionally listed separately from the canonical selected trace
set above:

| Task | Prefix | Exact prompt evidence | Scored result in prefix | Scope |
|---|---:|---|---|---|
| 1 | 350 events | Exact Starter Prompt; no continuation | None before the boundary | Historical bounded audit only |
| 2 | 705 events | Exact Starter and Continuation Prompts | `55260695`, Public `0.55416`, Private `0.54833` | Historical bounded audit plus eligible v2 artifact chain |

The complete raw formal sessions for Tasks 1 and 2 are available only in the
private local archives recorded in `ORIGINAL_SESSION_RECOVERY.json`; their
human-influenced suffixes are not published. A prefix is not silently expanded into a complete
historical trace, and neither prefix is used to claim causal provenance for the
account's later automatic official final. Hashes, timestamps, prompt checks,
and boundary definitions are in [`FORMAL_PREFIX_AUDIT.json`](FORMAL_PREFIX_AUDIT.json).

## What is represented

Each JSONL line is one timestamped event. In `response_item` events:

- `role=user` and `role=developer` contain injected prompts/context;
  `role=assistant` contains visible Agent messages.
- `type=function_call` and `function_call_output` are logical tool calls and
  returned outputs.
- `type=custom_tool_call` and `custom_tool_call_output` are the outer `exec`
  wrapper and visible command/tool output.
- `event_msg` records lifecycle events and cumulative token telemetry.

The index explicitly reports prompt messages, assistant outputs, logical calls,
logical call outputs, outer tool calls, and outer tool outputs. Hidden
chain-of-thought is not published. Opaque `encrypted_content` is replaced with
`[OMITTED_OPAQUE_REASONING]`; credentials, private endpoints, and secret
metadata are redacted.

Call envelopes are paired by `call_id` during verification. Three published
audit streams end exactly on an in-flight call (the full later Task 1
reproduction and two Task 4 boundary traces); those call IDs and timestamps are
marked `incomplete_at_capture_boundary` in the machine index. No orphan output,
duplicate call ID, out-of-order output, or unmatched call away from the final
captured event is accepted.

The first excluded human prompt and all events causally downstream of it are
outside this package. Boundary records contain timestamp, classification, and
cryptographic hashes only; they do not reproduce human prompt bodies. The older
formal Task 1 run's later supervised submission suffix is retained only as hash
provenance, not as organizer-facing trace material.

## Cross-task accounting

All six runs identify the same canonical LLM, `gpt-5.6-sol`, under provider
`ioai_allowed`. Tasks 1–4 used reasoning effort `max`; Tasks 5–6 used `xhigh`.

| Task | Trace files | Events | User / assistant messages | Logical calls | Outer `exec` calls | Final cumulative tokens |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1,383 | 2 / 70 | 17 | 262 | 40,830,176 |
| 2 | 1 | 1,067 | 2 / 61 | 40 | 176 | 29,205,639 |
| 3 | 4 | 2,427 | 8 / 48 | 135 | 373 | 56,373,300 |
| 4 | 12 | 5,881 | 50 / 118 | 198 | 753 | 244,165,721 |
| 5 | 14 | 4,705 | 28 / 140 | 131 | 409 | 160,243,108 |
| 6 | 3 | 1,868 | 6 / 54 | 54 | 309 | 41,371,859 |

The token column sums the final cumulative counter from each selected trace; it
does not add intermediate snapshots twice. Task 3's exact aggregate was
recovered from matching private originals whose hashes are recorded in the
task evidence, while raw originals remain unpublished.

## Cost and compute limitations

Exact token counters and per-task accelerator runtimes are in
[`COSTS.json`](COSTS.json) and [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json).
Exact USD API prices remain `null`: no invoice or applicable
`ioai_allowed`/`gpt-5.6-sol` rate card was captured, and another model's public
price is not substituted. GPU monetary costs remain `null` where no billable
rate or invoice exists; CPU/no-GPU tasks are recorded as zero GPU allocation.

## Per-task evidence map

- [Task 1](task1/): canonical later solution prefix through `task_complete`,
  full raw reproduction audit, post-deadline result, and historical formal prefix.
- [Task 2](task2/): complete later no-live-human reproduction rollout,
  post-deadline result, and historical formal-prefix audit material.
- [Task 3](task3/): direct trace, recovered token aggregate, and official result.
- [Task 4](task4/): formal and supplemental parallel-solver traces (12 total),
  rule-difference audit, and official result.
- [Task 5](task5/): main and worker/resume traces, with late-submission fields
  explicitly separated from official result.
- [Task 6](task6/): bounded main trace, two pre-boundary worker traces, and
  post-boundary exclusions by hash.

Run `python3 verify_repository.py` from the repository root to validate all
task manifests, trace hashes, score reconciliations, cost accounting, and the
organizer material manifest.
