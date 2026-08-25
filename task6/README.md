# Task 6 — IOAI Field

Competition: `ioai-2026-task-6-westlake-nlp-60`<br>
Kaggle account: `researai`<br>
Agent run: 2026-08-08 16:23:20.951Z–18:23:20.943Z<br>
Model: `gpt-5.6-sol`, reasoning effort `xhigh`

The solver approximated a protected procedural 2-D field with a trained
`torch.nn.Module`. The official evaluator scores five equally weighted regions
(`I`, `O`, `A`, `I_entropy`, and background), requires dropout-derived inference
stochasticity for `I_entropy`, and applies a 0.5 penalty at 20,260 parameters or
more. The exact rules and submission envelope are preserved in
[`official/OVERVIEW.md`](official/OVERVIEW.md) and
[`official/SUBMISSION.md`](official/SUBMISSION.md).

## Run result

The user-requested target was 86.5 public LB (0.865 normalized). The run stopped
at its deadline with version 3 as the in-run incumbent: submission `55357080`,
public `75.01540`, private `73.36234`. This is a score on Kaggle's 0–100 display
scale; it is not a 0–1 score. The target was not reached.

| Version | Mechanism | Public LB | Private LB | Remote runtime |
|---:|---|---:|---:|---:|
| 1 | public-config routed sine + bounded dropout | 47.15536 | 46.71642 | 72.563943906 s |
| 2 | seed-randomized routed sine | 70.95502 | 69.14383 | 96.065099238 s |
| 3 | lane-density context + routed sine | **75.01540** | **73.36234** | 75.092360389 s |

The candidate frontier and validation evidence are in
[`records/CANDIDATES.md`](records/CANDIDATES.md) and
[`records/TASK_KNOWLEDGE.md`](records/TASK_KNOWLEDGE.md). The chronological
experiment and submission ledgers are retained as JSONL in `records/`.

## Execution trace

The five JSONL files in [`evidence/rollouts/`](evidence/rollouts/) are
credential-redacted copies of the main agent and four subagent traces. They
retain observable user/developer prompts, visible assistant messages, logical
tool-call envelopes, tool outputs, timestamps, and cumulative token telemetry.
Opaque encrypted reasoning is replaced by a marker; it is not interpreted or
claimed as an output. The raw `codex-home` trace files and SQLite state are not
copied into this repository.

See the cross-task [execution trace index](../EXECUTION_TRACE_INDEX.json),
[trace guide](../EXECUTION_TRACES.md), and [cost manifest](../COSTS.json).

## Remote provenance

`remote/v1-kernel.log` through `remote/v3-kernel.log` are the compact logs for
the three versions that belong to this agent run. `remote/kernel-metadata.json`
records the T4, Internet-off, competition-only notebook configuration. The
Kaggle extraction performed later found additional post-deadline submissions;
they are intentionally excluded from the autonomous-run claim (see
[`remote/POST_RUN_SUBMISSIONS_NOTE.json`](remote/POST_RUN_SUBMISSIONS_NOTE.json)).

No private/final leaderboard claim is made beyond the scores explicitly recorded
above.
