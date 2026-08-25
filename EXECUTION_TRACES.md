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
[`REPRODUCTION_TRACE_MATERIAL.md`](REPRODUCTION_TRACE_MATERIAL.md) and are now
the canonical no-live-human autonomous rollout selection for those two tasks.
They remain post-deadline, non-ranking traces for official-score purposes and
must not be read as the official account result.

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
| 1 | 1 | 1,398 | 3 / 72 | 17 | 264 | 40,933,816 |
| 2 | 1 | 1,067 | 2 / 61 | 40 | 176 | 29,205,639 |
| 3 | 4 | 2,427 | 8 / 48 | 135 | 373 | 56,373,300 |
| 4 | 5 | 2,717 | 20 / 62 | 75 | 387 | 109,119,898 |
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

- [Task 1](task1/): complete later no-live-human reproduction rollout,
  post-deadline result, and historical formal-prefix audit material.
- [Task 2](task2/): complete later no-live-human reproduction rollout,
  post-deadline result, and historical formal-prefix audit material.
- [Task 3](task3/): direct trace, recovered token aggregate, and official result.
- [Task 4](task4/): main and four worker/resume traces, with official result.
- [Task 5](task5/): main and worker/resume traces, with late-submission fields
  explicitly separated from official result.
- [Task 6](task6/): bounded main trace, two pre-boundary worker traces, and
  post-boundary exclusions by hash.

Run `python3 verify_repository.py` from the repository root to validate all
task manifests, trace hashes, score reconciliations, cost accounting, and the
organizer material manifest.
