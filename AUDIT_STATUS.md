# Final audit status — Tasks 1–6

This page is a compact hand-off for an organizer or Jury reviewer. It is an
index of preserved evidence and machine checks, not a compliance certificate.
The authoritative detailed records remain in the linked task packages and in
the root JSON ledgers.

## At-a-glance scope

| Task | Official final (Public / Private) | Published no-live-human trace | Exact organizer prompt text | Main qualification |
|---|---:|---|---|---|
| [1](task1/) | 0.77751 / 0.80474 (`55267333`, `55267368`) | Later 120-minute reproduction; 1 canonical prefix | No | Original run lost after school-server restart; later trace is post-deadline and non-ranking. Exact-prompt formal prefix is separate and has no scored submission. |
| [2](task2/) | 0.63583 / 0.62500 (`55261432`) | Later 120-minute reproduction; full trace | No | Original run lost after school-server restart; later trace is post-deadline and non-ranking. Exact-prompt formal prefix and eligible `55260695` are separate evidence. |
| [3](task3/) | 58.51666 / 51.61666 (`55289569`, `55289823`) | 4 traces covering 8 scored submissions | Yes | Account/version-budget interpretation and report/timeline fields remain for Jury determination. |
| [4](task4/) | 98.41 / 98.32 (`55316818`) | 12 traces | No | Formatting-modified Starter and substantive non-exact continuation are disclosed; final artifact chain is verified. |
| [5](task5/) | 95.39 / 96.06 (`55320296`) | 14 traces | Yes | Historical v6 source pull returned HTTP 403; byte identity limitation is disclosed. |
| [6](task6/) | 75.01540 / 73.36234 (`55357080`) | 3 traces | Yes | Exact v3 artifact chain is verified; historical report corrections and measured evaluator batching are disclosed. |

“Official final” means the extracted account result under the preserved
automatic highest-Public-before-deadline rule. It is intentionally separated
from the selected trace result; in particular, Tasks 1–2 do not claim that the
later reproductions caused their earlier official finals.

## What is preserved

The selected trace package contains observable startup/organizer prompts,
visible Agent messages, worker assignments, tool-call envelopes, and tool
outputs within each declared boundary. The machine-readable index reports 35
trace files, 17,331 events, and 572,189,803 cumulative tokens. The separate
Task 1/2 reproduction package retains the complete later raw streams (2 files,
2,465 events, 70,139,455 tokens). Startup instruction payloads are indexed and
hash-bound in [`STARTUP_INSTRUCTION_INDEX.md`](STARTUP_INSTRUCTION_INDEX.md).
The Task 1/2 official-ref mapping is further disambiguated in
[`KERNEL_VERSION_MAPPING_AUDIT.md`](KERNEL_VERSION_MAPPING_AUDIT.md): the
account's internal `scriptVersionId` is exact, while the archive `vN` folder
and submitted bytes remain explicitly candidate-level where Kaggle did not
provide a confirming digest.

Credential material, private endpoints, hidden chain-of-thought, encrypted
opaque reasoning, and the bodies of excluded live-human prompts are not
published. Boundary records retain timestamps, classifications, and hashes so
the omission is auditable without exposing those contents.

## Cost and compute accounting

[`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json) is the machine-readable source
for model, reasoning effort, token vectors, and observed Kaggle runtime per
task. All selected traces use `ioai_allowed / gpt-5.6-sol`; Tasks 1–4 use
`max`, and Tasks 5–6 use `xhigh`. Exact API USD is `null` because no provider
invoice or applicable rate card was captured. Kaggle T4 runtime is reported for
the selected scope; exhaustive overlapping local H100 development time for
Tasks 4–6 and GPU USD are not reconstructable, so they remain explicitly
unavailable rather than estimated.

## Remaining organizer decisions

The evidence package deliberately leaves these questions open:

- whether a later post-deadline reproduction or a bounded formal prefix can
  satisfy the requested historical trace deliverable for Tasks 1–2;
- whether Task 4’s prompt/formatting and local-development deviations are
  acceptable;
- how the submission/version budget and repeated Notebook versions are scoped
  for Tasks 1–3;
- whether Task 6’s historical report errors are material.

The cross-task findings and exact evidence paths are in
[`RULE_COMPLIANCE_AUDIT.md`](RULE_COMPLIANCE_AUDIT.md),
[`PROMPT_CONFORMANCE_AUDIT.md`](PROMPT_CONFORMANCE_AUDIT.md),
[`SUBMISSION_VERSION_AUDIT.md`](SUBMISSION_VERSION_AUDIT.md), and the
11-row-per-task [`REQUIREMENT_EVIDENCE_MATRIX.md`](REQUIREMENT_EVIDENCE_MATRIX.md).

## Verification route

From the repository root:

```bash
python3 tools/build_execution_trace_index.py
python3 tools/build_autonomous_trace_material.py
python3 verify_repository.py
for t in 1 2 3 4 5 6; do (cd task$t && sha256sum -c MANIFEST.sha256); done
sha256sum -c AUTONOMOUS_MATERIAL_MANIFEST.sha256
sha256sum -c REPRODUCTION_MATERIAL_MANIFEST.sha256
```

The current local verifier result is `all_ok: true`; that result means the
published files are internally consistent. Final eligibility and recognition
remain solely with the organizer/Jury.
