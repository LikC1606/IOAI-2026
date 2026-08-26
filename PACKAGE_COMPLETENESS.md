# Package completeness and evidence coverage

This page is a compact join of the checked-in trace, prompt, result, and
cost ledgers. It answers **where each requested deliverable is and what
qualification travels with it**; it is not a compliance certificate.
The machine-readable form is [`PACKAGE_COMPLETENESS.json`](PACKAGE_COMPLETENESS.json).

## Global coverage

| Scope | Trace files | Events | Cumulative tokens |
|---|---:|---:|---:|
| Selected human-intervention-free material | 35 | 17331 | 572,189,803 |
| Later Task 1/2 reproduction material | 2 | 2465 | 70,139,455 |

All selected traces include zero live-human prompt events. Observable
startup/organizer prompts, visible Agent messages, worker assignments,
tool-call envelopes, tool outputs, timestamps, and token telemetry are
retained within each declared boundary. Hidden chain-of-thought, opaque
encrypted reasoning, credentials, private endpoints, and excluded human
prompt bodies are not published.

## Requested deliverables by task

| Task | Trace and prompt coverage | Observable outputs/tool calls | Model and tokens | Official result binding | GPU/runtime and USD | Main qualification |
|---|---|---|---|---|---|---|
| [task1](task1/README.md) | 1 files / 1383 events; non-exact/custom disclosed; 0 live-human events | assistant 70; logical calls 17; tool calls 262 (+ outputs) | `ioai_allowed / gpt-5.6-sol` / `max`; 40,830,176 total tokens | `[55267333, 55267368]`: Public 0.77751, Private 0.80474; Account result is reconciled, but neither public trace selection is causal evidence for the official final | NvidiaTeslaT4, 1946.54 s; GPU USD null (unavailable_no_rate_or_invoice); local: not applicable | Custom starter in reproduction; recovered formal human-influenced suffix withheld; 38 captured versions vs literal 20 and repeated official version |
| [task2](task2/README.md) | 1 files / 1067 events; non-exact/custom disclosed; 0 live-human events | assistant 61; logical calls 40; tool calls 176 (+ outputs) | `ioai_allowed / gpt-5.6-sol` / `max`; 29,205,639 total tokens | `[55261432]`: Public 0.63583, Private 0.625; Account result is reconciled, but the official final is downstream of the modified formal continuation and not bound to the later reproduction | NvidiaTeslaT4, 263.17 s; GPU USD null (unavailable_no_rate_or_invoice); local: not applicable | Custom starter in reproduction; recovered formal modified-continuation suffix withheld; repeated pre-deadline version |
| [task3](task3/README.md) | 4 files / 2427 events; exact; 0 live-human events | assistant 48; logical calls 135; tool calls 373 (+ outputs) | `ioai_allowed / gpt-5.6-sol` / `max`; 56,373,300 total tokens | `[55289569, 55289823]`: Public 58.51666, Private 51.61666; Official final refs and selected trace are aligned | CPU, 0 s; GPU USD 0 (no_gpu_allocated); local: not applicable | Account-wide count and repeated version conflict remain for organizer interpretation; historical reports are short and v8 contains factual score/distribution errors |
| [task4](task4/README.md) | 12 files / 5881 events; non-exact/custom disclosed; 0 live-human events | assistant 118; logical calls 198; tool calls 753 (+ outputs) | `ioai_allowed / gpt-5.6-sol` / `max`; 244,165,721 total tokens | `[55316818]`: Public 98.41, Private 98.32; Official final ref and selected trace are aligned | NvidiaTeslaT4, 1120.720551504 s; GPU USD null (unavailable_no_rate_or_invoice); local: unavailable_non_exhaustive_overlapping_approximate_records | Starter formatting differs and continuation is substantively non-exact; local __pycache__ and H100-development scope are disclosed |
| [task5](task5/README.md) | 14 files / 4705 events; exact; 0 live-human events | assistant 140; logical calls 131; tool calls 409 (+ outputs) | `ioai_allowed / gpt-5.6-sol` / `xhigh`; 160,243,108 total tokens | `[55320296]`: Public 95.39, Private 96.06; Official v6 final ref and selected trace are aligned | NvidiaTeslaT4, 837.27460599 s; GPU USD null (unavailable_no_rate_or_invoice); local: unavailable_multiple_overlapping_runs | Source is the trace-preserved formal-run copy rather than an independently redownloaded historical v6 file; exhaustive local H100 runtime is unavailable |
| [task6](task6/README.md) | 3 files / 1868 events; exact; 0 live-human events | assistant 54; logical calls 54; tool calls 309 (+ outputs) | `ioai_allowed / gpt-5.6-sol` / `xhigh`; 41,371,859 total tokens | `[55357080]`: Public 75.0154, Private 73.36234; Official v3 final ref and selected trace are aligned | NvidiaTeslaT4, 243.721403533 s; GPU USD null (unavailable_no_rate_or_invoice); local: unavailable_multiple_experiment_records_not_exhaustively_allocated | Historical report has dropout/range errors; evaluator batching dependence and incomplete local H100 accounting are explicitly disclosed |

## Cost interpretation

Token vectors and the selected remote runtime are recorded per task.
API USD is `null` for every task because no provider invoice or
applicable `ioai_allowed / gpt-5.6-sol` rate was captured. GPU USD is
also `null` except the explicit zero for the CPU-only Task 3 scope.
Tasks 4–6 additionally contain local H100 development observations
whose exhaustive non-overlapping runtime is unavailable; no estimate
is substituted.

## Where to verify

- Trace inventory and event-level coverage: [`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json) and [`AUTONOMOUS_TRACE_MATERIAL.md`](AUTONOMOUS_TRACE_MATERIAL.md).
- Prompt exactness and custom/inherited prompt classes: [`PROMPT_CONFORMANCE_AUDIT.md`](PROMPT_CONFORMANCE_AUDIT.md).
- Official account reconciliation: [`FINAL_SUBMISSION_RESULTS.md`](FINAL_SUBMISSION_RESULTS.md) and each task's `remote/FINAL_ACCOUNT_RESULTS.json`.
- Model/token/remote-runtime accounting: [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json) and [`COSTS.json`](COSTS.json).
- Remaining organizer/Jury decisions: [`OPEN_REVIEW_ITEMS.md`](OPEN_REVIEW_ITEMS.md).
- Integrity route: `python3 verify_repository.py` plus the six task manifests and the two root material manifests.

The current package deliberately keeps `strict_all_six_claim_supported` false.
A green verifier result proves internal consistency only; it does not
establish organizer acceptance.
