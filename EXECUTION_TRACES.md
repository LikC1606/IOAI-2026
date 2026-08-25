# Agent execution traces: Tasks 1–6

This package records the observable execution of the six competition agents.
The machine-readable index is [`EXECUTION_TRACE_INDEX.json`](EXECUTION_TRACE_INDEX.json);
the individual JSONL files are under each `taskN/evidence/rollouts/` directory.
Task 6 was imported from a local capture with
[`tools/build_execution_trace_index.py`](tools/build_execution_trace_index.py),
then redacted before it was added to the repository.

## What is represented

Each JSONL line is one timestamped event. In `response_item` events:

- `role=user` and `role=developer` contain the prompts/context injected into the
  agent session; `role=assistant` contains visible assistant messages.
- `type=function_call` is the logical tool call emitted by the model (for
  example `spawn_agent`, `wait`, or `send_message`).
- `type=custom_tool_call` is the outer `exec` wrapper used by this runtime. Its
  paired `custom_tool_call_output` contains the visible command/tool output.
- `event_msg` records lifecycle events and cumulative token telemetry.

The traces do not publish hidden chain-of-thought. Task 6's opaque
`encrypted_content` fields are replaced with `[OMITTED_OPAQUE_REASONING]`; all
observable prompts, outputs, and tool-call envelopes remain available. Kaggle,
OAuth, proxy, and API credentials/private endpoints are redacted. Raw Task 6
SQLite state and the original `codex-home` traces are not included.

## Cross-task accounting

All six runs identify the same canonical LLM, `gpt-5.6-sol`, under the
`ioai_allowed` provider. The `models_observed` field in the JSON index is a
textual audit of model-name strings in context; incidental names in injected
instructions are not evidence that another model executed the run.

| Task | Trace files | Events | User / assistant messages | Logical function calls | Outer `exec` calls | Final cumulative tokens |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 775 | 5 / 40 | 16 (`wait` ×16) | 133 | 30,380,753 |
| 2 | 1 | 705 | 3 / 27 | 4 (`wait` ×4) | 128 | 14,457,808 |
| 3 | 4 | 2,427 | 8 / 48 | 135 | 373 | unavailable — redacted |
| 4 | 5 | 2,717 | 20 / 62 | 75 | 387 | 109,119,898 |
| 5 | 14 | 4,705 | 28 / 140 | 131 | 409 | 160,243,108 |
| 6 | 5 | 2,871 | 14 / 67 | 63 | 341 | 104,143,733 |

The token column is the sum of the final cumulative counters from each trace in
that task. It is not a sum of every intermediate `token_count` event. Task 3's
redaction removed those counters, so its API cost cannot be reconstructed from
the repository without inventing data.

## Observable tool-call mix

The logical call names are preserved in each file and summarized in the index.
The most useful cross-task view is:

| Task | Logical calls visible in the trace |
|---|---|
| 1 | `wait` ×16 (3 formal + 13 post-boundary agent-execution) |
| 2 | `wait` ×4 |
| 3 | `wait` ×106, `send_message` ×20, `list_agents` ×5, `spawn_agent` ×3, `wait_agent` ×1 |
| 4 | `wait` ×65, `send_message` ×4, `spawn_agent` ×4, `list_agents` ×2 |
| 5 | `wait` ×60, `send_message` ×35, `spawn_agent` ×13, `wait_agent` ×12, `list_agents` ×7, `followup_task` ×4 |
| 6 | `wait` ×35, `send_message` ×13, `list_agents` ×6, `spawn_agent` ×4, `followup_task` ×3, `wait_agent` ×2 |

For full prompts and outputs, search the JSONL rather than relying on this
summary. For example, the following shows visible user prompts and assistant
messages without printing tool payloads:

```bash
jq 'select(.type == "response_item" and (.payload.role == "user" or .payload.role == "assistant")) |
    {timestamp, role: .payload.role, content: .payload.content}' \
  task6/evidence/rollouts/rollout-*.jsonl
```

The index also contains a SHA-256 for every trace file so an organizer can
verify that the documented copy has not changed.

## Cost and compute limitations

Exact token counters are in [`COSTS.json`](COSTS.json). Exact USD API prices
are intentionally `null`: `ioai_allowed`/`gpt-5.6-sol` has no applicable public
rate in the available pricing page, and no invoice or provider rate card was
captured. GPU entries report Kaggle T4/CPU notebook wall-clock runtime, not GPU
utilization or a billable amount; monetary GPU cost is likewise `null` without a
cloud invoice/rate. A reproducible token-price formula is included in the JSON
manifest for later completion if the provider supplies rates.

## Per-task evidence map

- [Task 1](task1/): formal rollout plus the separate
  `evidence/submission-execution/` post-boundary trace, including the
  agent-executed scored submission.
- [Task 2](task2/): single main trace plus eligible remote CNN records.
- [Task 3](task3/): [direct trace and cost entry point](task3/EXECUTION_AND_COSTS.md),
  main and subagent traces; token telemetry is redacted.
- [Task 4](task4/): main and four worker/resume traces.
- [Task 5](task5/): main trace and thirteen worker/resume traces.
- [Task 6](task6/): main trace and four redacted subagent traces, plus the
  official prompts, experiment/submission ledgers, and v1–v3 remote logs.
