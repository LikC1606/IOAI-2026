# Task 6 — IOAI Field

Competition: `ioai-2026-task-6-westlake-nlp-60`<br>
Kaggle account: `researai`<br>
Agent run: 2026-08-08 16:23:20.951Z–18:23:20.943Z<br>
Model: `gpt-5.6-sol`, reasoning effort `xhigh`

Start with [`COMPLIANCE.md`](COMPLIANCE.md),
[`RULE_DIFFERENCE_AUDIT.md`](RULE_DIFFERENCE_AUDIT.md), and
[`ARTIFACT_PROVENANCE.json`](ARTIFACT_PROVENANCE.json). The official result is
trace-aligned. The v3 model's use of evaluator-batch context is measured and
documented as a technical behavior for reproducibility; it is not treated as a
violation or compliance blocker.

The solver approximated a protected procedural 2-D field with a trained
`torch.nn.Module`. The official evaluator scores five equally weighted regions
(`I`, `O`, `A`, `I_entropy`, and background), requires dropout-derived inference
stochasticity for `I_entropy`, and applies a 0.5 penalty at 20,260 parameters or
more. The exact rules and submission envelope are preserved in
[`official/OVERVIEW.md`](official/OVERVIEW.md) and
[`official/SUBMISSION.md`](official/SUBMISSION.md).

## Autonomous result and final account reconciliation

Before the first live human intervention, version 3 was the autonomous incumbent:
submission `55357080`, Public `75.01540`, Private `73.36234`. This is a score on
Kaggle's 0–100 display scale; it is not a 0–1 score. A later target instruction
was received only after the autonomous boundary and its body and causal suffix
are not published as organizer-facing trace material.

| Version | Mechanism | Public LB | Private LB | Remote runtime |
|---:|---|---:|---:|---:|
| 1 | public-config routed sine + bounded dropout | 47.15536 | 46.71642 | 72.563943906 s |
| 2 | seed-randomized routed sine | 70.95502 | 69.14383 | 96.065099238 s |
| 3 | lane-density context + routed sine | **75.01540** | **73.36234** | 75.092360389 s |

The candidate frontier and validation evidence are in
[`records/CANDIDATES.md`](records/CANDIDATES.md) and
[`records/TASK_KNOWLEDGE.md`](records/TASK_KNOWLEDGE.md). The chronological
experiment and submission ledgers are retained as JSONL in `records/`.

## Exact v3 artifacts

The historical notebook and metadata are preserved at `notebooks/v3/`. The
exact remote `submission.csv` and its decoded submitted `custom_model.py` are
under `remote/v3/`. The decoded CSV source is byte-identical to the preserved
source, the safetensors weights load into it, and the model has 13,426
parameters. Verify with:

```bash
python3 tools/verify_v3_artifacts.py
sha256sum -c MANIFEST.sha256
```

The same verifier demonstrates that the model is not pointwise: changing the
other coordinates in a batch changes internal outputs for 100/100 fixed test
points and final predictions for 5/100 in the deterministic fixture. This
measured batch behavior is disclosed in the rule audit and is not treated as a
compliance issue. The non-redistributed official evaluator source is bound by hash and
function/call-site locators in
[`evidence/EVALUATOR_BATCHING_PROVENANCE.json`](evidence/EVALUATOR_BATCHING_PROVENANCE.json).

## Execution trace

The published autonomous trace set has a bounded main trace in
[`evidence/autonomous-only/`](evidence/autonomous-only/) and two pre-boundary
worker traces in [`evidence/rollouts/`](evidence/rollouts/). They retain
startup/organizer user context, developer prompts, visible assistant messages,
logical tool-call envelopes, tool outputs, timestamps, and cumulative token telemetry.
Opaque encrypted reasoning is replaced by a marker; it is not interpreted or
claimed as an output. The raw `codex-home` trace files and SQLite state are not
copied into this repository.

See the cross-task [execution trace index](../EXECUTION_TRACE_INDEX.json),
[trace guide](../EXECUTION_TRACES.md), and [cost manifest](../COSTS.json).

The main trace stops
strictly before `2026-08-08T18:09:48.833Z`, the first human-triggered resume
prompt. The later human target-score prompt, every downstream event, and the two
workers spawned after that resume are excluded from the repository; only their
timestamps and hashes are retained in
[`evidence/SUPERVISED_EXCLUSIONS.json`](evidence/SUPERVISED_EXCLUSIONS.json).
The authoritative trace selection is the root
[`AUTONOMOUS_TRACE_INDEX.json`](../AUTONOMOUS_TRACE_INDEX.json). Versions v1-v3
and their scores were already produced before this boundary.

## Remote provenance

`remote/v1-kernel.log` through `remote/v3-kernel.log` are the compact logs for
the three autonomous versions. `remote/kernel-metadata.json`
records the T4, Internet-off, competition-only notebook configuration. The
Kaggle extraction found six account submissions in total: v1-v3 before the
autonomy boundary, `55357740` after that boundary but before both run and
competition deadlines, and `55358042`/`55358739` after the official deadline.
All three later submissions are excluded from the autonomous claim. The
chronological last and all-account numerical best is `55358739`, Public
`76.41428`, Private `73.74666`; it is post-deadline and non-autonomous. See
[`remote/FINAL_ACCOUNT_RESULTS.json`](remote/FINAL_ACCOUNT_RESULTS.json) and
[`remote/POST_RUN_SUBMISSIONS_NOTE.json`](remote/POST_RUN_SUBMISSIONS_NOTE.json).

The extraction does not expose a selected-for-final flag, so no final placement
is inferred. Latest, all-account best, official-deadline, and autonomous scopes
are reported separately.

## Historical report correction

The exact v3 report says the entropy branch uses seven differently scaled
dropout bits with range `[-1016,1016]`. The submitted source actually uses eight
equal-scale centered dropout units and can reach `[-2000,2000]`, still inside
the official `[-2026,2026]` bound. The historical notebook remains immutable;
the discrepancy is disclosed in `COMPLIANCE.md`.
