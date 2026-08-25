# Organizer submission — Tasks 1–6

This is the single entry point for every requested deliverable. The
machine-readable checklist is [`ORGANIZER_SUBMISSION.json`](ORGANIZER_SUBMISSION.json),
and `python3 verify_repository.py` validates the paths, hashes, score records,
trace coverage, model/cost fields, and extraction metadata.

For the shortest organizer/Jury audit route, start with
[`ORGANIZER_REVIEW_GUIDE.md`](ORGANIZER_REVIEW_GUIDE.md). It lists the exact
verification commands, evidence map, and the few determinations that cannot be
resolved from the preserved historical records.

> **Restricted-data notice:** `task3/input/competition/` contains
> organizer-provided data for authorized review. Keep this repository private
> and follow [`task3/DATA_PROVENANCE.md`](task3/DATA_PROVENANCE.md) before
> sharing or publishing any copy.

## Task-package entry points

| Task | Package README | Official-page snapshots | Machine-readable summary | Compliance note | Integrity manifest |
|---|---|---|---|---|---|
| 1 | [`task1/README.md`](task1/README.md) | [`task1/official/`](task1/official/) | [`task1/SUMMARY.json`](task1/SUMMARY.json) | [`task1/COMPLIANCE.md`](task1/COMPLIANCE.md) | [`task1/MANIFEST.sha256`](task1/MANIFEST.sha256) |
| 2 | [`task2/README.md`](task2/README.md) | [`task2/official/`](task2/official/) | [`task2/SUMMARY.json`](task2/SUMMARY.json) | [`task2/COMPLIANCE.md`](task2/COMPLIANCE.md) | [`task2/MANIFEST.sha256`](task2/MANIFEST.sha256) |
| 3 | [`task3/README.md`](task3/README.md) | [`task3/official/`](task3/official/) | [`task3/SUMMARY.json`](task3/SUMMARY.json) | [`task3/COMPLIANCE.md`](task3/COMPLIANCE.md) | [`task3/MANIFEST.sha256`](task3/MANIFEST.sha256) |
| 4 | [`task4/README.md`](task4/README.md) | [`task4/official/`](task4/official/) | [`task4/SUMMARY.json`](task4/SUMMARY.json) | [`task4/COMPLIANCE.md`](task4/COMPLIANCE.md) | [`task4/MANIFEST.sha256`](task4/MANIFEST.sha256) |
| 5 | [`task5/README.md`](task5/README.md) | [`task5/official/`](task5/official/) | [`task5/SUMMARY.json`](task5/SUMMARY.json) | [`task5/COMPLIANCE.md`](task5/COMPLIANCE.md) | [`task5/MANIFEST.sha256`](task5/MANIFEST.sha256) |
| 6 | [`task6/README.md`](task6/README.md) | [`task6/official/`](task6/official/) | [`task6/SUMMARY.json`](task6/SUMMARY.json) | [`task6/COMPLIANCE.md`](task6/COMPLIANCE.md) | [`task6/MANIFEST.sha256`](task6/MANIFEST.sha256) |

Special evidence is linked here for quick review:

- Tasks 1–2 later reproductions: [`REPRODUCTION_TRACE_MATERIAL.md`](REPRODUCTION_TRACE_MATERIAL.md), [`REPRODUCTION_TRACE_INDEX.json`](REPRODUCTION_TRACE_INDEX.json), and [`REPRODUCTION_COSTS.json`](REPRODUCTION_COSTS.json).
- Task 4 supplemental trace provenance: [`task4/evidence/SUPPLEMENTAL_ROLLOUT_PROVENANCE.json`](task4/evidence/SUPPLEMENTAL_ROLLOUT_PROVENANCE.json) and [`task4/RULE_DIFFERENCE_AUDIT.md`](task4/RULE_DIFFERENCE_AUDIT.md).
- Task 6 exact v3 artifact chain: [`task6/ARTIFACT_PROVENANCE.json`](task6/ARTIFACT_PROVENANCE.json), [`task6/RULE_DIFFERENCE_AUDIT.md`](task6/RULE_DIFFERENCE_AUDIT.md), and [`task6/evidence/EVALUATOR_BATCHING_PROVENANCE.json`](task6/evidence/EVALUATOR_BATCHING_PROVENANCE.json).

## Deliverable checklist

| Organizer requirement | Status | Evidence |
|---|---|---|
| Execution traces for Tasks 1–6 | Complete selected observable prefixes; provenance limits disclosed | [`AUTONOMOUS_TRACE_MATERIAL.md`](AUTONOMOUS_TRACE_MATERIAL.md), [`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json) |
| Later two-hour reproduction traces for Tasks 1–2 | Complete, separately scoped post-deadline reproductions; not the lost originals | [`REPRODUCTION_TRACE_MATERIAL.md`](REPRODUCTION_TRACE_MATERIAL.md), [`REPRODUCTION_TRACE_INDEX.json`](REPRODUCTION_TRACE_INDEX.json) |
| Prompts and visible Agent outputs | Complete within selected observable trace scope | Full payloads are in every indexed JSONL trace; prompt classes and hashes are in the index |
| Exact organizer prompt conformance | Audited; Tasks 1, 2, and 4 are non-exact | [`PROMPT_CONFORMANCE_AUDIT.md`](PROMPT_CONFORMANCE_AUDIT.md), [`PROMPT_CONFORMANCE_AUDIT.json`](PROMPT_CONFORMANCE_AUDIT.json) |
| Cross-task rule compliance | Audited; known deviations and evidence/interpretation limits remain | [`RULE_COMPLIANCE_AUDIT.md`](RULE_COMPLIANCE_AUDIT.md), [`RULE_COMPLIANCE_AUDIT.json`](RULE_COMPLIANCE_AUDIT.json) |
| Task 4 competition-rule differences | Audited with disclosed prompt, process, and hardware limits | [`task4/RULE_DIFFERENCE_AUDIT.md`](task4/RULE_DIFFERENCE_AUDIT.md), [`task4/RULE_DIFFERENCE_AUDIT.json`](task4/RULE_DIFFERENCE_AUDIT.json) |
| Task 6 exact artifacts and rule differences | Exact v3 artifacts complete; evaluator batch behavior measured and disclosed, not treated as a compliance blocker | [`task6/ARTIFACT_PROVENANCE.json`](task6/ARTIFACT_PROVENANCE.json), [`task6/RULE_DIFFERENCE_AUDIT.md`](task6/RULE_DIFFERENCE_AUDIT.md) |
| Read-only artifact replay | Task 1 provenance/package verifier, Task 2 eligible v2 exact source/output chain, all eight Task 3 source/output replays, Task 4 hash-only output chain, Task 5 exact v6 output chain, and Task 6 exact v3 replay pass | [`task1/tools/verify_package.py`](task1/tools/verify_package.py), Task 2 `remote/rotation-cnn-v2/`, [`task3/evidence/verify_artifacts.py`](task3/evidence/verify_artifacts.py), `task4/remote/V4_OUTPUT_PROVENANCE.json`, `task5/V6_SOURCE_PROVENANCE.json`, and `python3 verify_repository.py` |
| Tool calls and tool outputs | Complete within selected observable trace scope | Per-task and per-file counts cover `function_call`, `function_call_output`, `custom_tool_call`, and `custom_tool_call_output` |
| LLM(s) used | Complete | [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json): `ioai_allowed` / `gpt-5.6-sol`; Tasks 1–4 `max`, Tasks 5–6 `xhigh` |
| Total API costs | Token accounting complete; USD unavailable | Exact per-task tokens and total are provided; USD is `null` because no invoice or exact provider/model rate was captured |
| GPU compute/cost per task | Kaggle remote selected scope complete; local H100 accounting and USD incomplete | Observed remote accelerator seconds/hours and known local observations are provided; exhaustive local runtime and USD are unavailable |
| Kaggle extraction results | Complete | [`KAGGLE_EXTRACTION_DELIVERY.json`](KAGGLE_EXTRACTION_DELIVERY.json), [`KAGGLE_EXTRACTION_SUMMARY.json`](KAGGLE_EXTRACTION_SUMMARY.json), and the linked Drive archive |
| Final submitted results matching Kaggle | Score reconciliation complete; Tasks 1–2 are not final-trace-bound | [`FINAL_SUBMISSION_RESULTS.md`](FINAL_SUBMISSION_RESULTS.md) and six task-level `FINAL_ACCOUNT_RESULTS.json` files |

## Human-intervention-free trace scope

The organizer trace selection contains the observable prefix before the first
live human intervention for each task. It retains startup/organizer prompts,
inherited context, Agent-generated worker assignments, visible outputs, tool
calls, and tool outputs. The first excluded human prompt and its entire causal
suffix are not part of the selected material. Boundary records expose only
timestamp, classification, and cryptographic hashes; they do not reproduce the
human prompt bodies.

Hidden chain-of-thought and opaque encrypted reasoning are not published.
Credentials, private endpoints, and secret metadata are redacted. These
omissions do not remove observable prompts, Agent responses, or tool envelopes.

No-live-human autonomy is not treated as proof of exact-organizer-prompt
conformance. Live Kaggle prompt pages were checked for all six tasks. Tasks 3,
5, and 6 match the exact organizer prompt text in the selected traces. Tasks 1,
2, and 4 contain custom prompt text and are disclosed as non-exact; this
repository does not self-certify Jury acceptance.

Trace-package completeness is not a compliance certificate. Task 1 and Task 2
do not bind their official final result to an original autonomous trace; Task 4
has a known exact-continuation deviation; and the remaining task-specific
prompt, budget, hardware, report, and provenance limits are summarized in
[`RULE_COMPLIANCE_AUDIT.md`](RULE_COMPLIANCE_AUDIT.md).

## Kaggle extraction archive

The complete organizer-requested extraction archive for account `researai` is
496,870,419 bytes and contains 1,401 archive entries. Its SHA-256 is
`eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c`.
It exceeds GitHub's single-file limit and is therefore delivered on Google
Drive:

<https://drive.google.com/file/d/1c9yRn5SUo6LOPDrHLrAVjj-9JLFti9Vz/view?usp=drivesdk>

## Verification

```bash
python3 tools/build_execution_trace_index.py
python3 tools/build_autonomous_trace_material.py
python3 verify_repository.py
sha256sum -c AUTONOMOUS_MATERIAL_MANIFEST.sha256
sha256sum -c REPRODUCTION_MATERIAL_MANIFEST.sha256
```

The USD cost fields deliberately remain `null` rather than pricing
`gpt-5.6-sol` with a different model's public rate or inventing a Kaggle GPU
invoice. The local H100 total is also incomplete for Tasks 4–6; the cost files
record only supported observations and do not extrapolate a total.

## Later two-hour reproduction scope

At the request to use the later fresh two-hour runs for Tasks 1 and 2, the full
credential-redacted traces are published separately under
[`task1/evidence/reproduction-120m/`](task1/evidence/reproduction-120m/) and
[`task2/evidence/reproduction-120m/`](task2/evidence/reproduction-120m/).
The original Task 1 and Task 2 run records were unavailable after a
school-server restart; these are later fresh reproductions using the same
configured solver/system, official competition bundle, and organizer
constraints, not the lost original run records.
They preserve the complete observable event streams and the corresponding
candidate/submission outcomes. Both runs contain no live human method/target
prompt. Task 1's canonical solution material is the immutable prefix through
`task_complete`; its complete raw stream remains in the reproduction package.
Task 2 uses its full reproduction as the canonical selection.
Both reproduction starter messages append a custom fresh-run-isolation section,
so neither is claimed to satisfy the strict exact Starter Prompt rule. Task 1's
canonical solution prefix has no continuation. Its full raw trace preserves a
later custom continuation after the selected submission, final Agent answer,
and `task_complete`; the 15-event suffix is outside the canonical selection.
See [`PROMPT_CONFORMANCE_AUDIT.md`](PROMPT_CONFORMANCE_AUDIT.md).

Task 4 now includes seven supplemental parallel-solver traces that were omitted
from the first trace index. The rule audit also discloses the substantive
non-exact continuation, a transient local `__pycache__` in the push folder, the
method-background arXiv searches (not treated as a compliance issue), and the
interpretation question around local H100 development versus the final one-T4
notebook. No organizer acceptance is self-certified. The final Task 4
submission was accepted at `06:10:48.923Z`, before the `06:15:00Z` official
deadline; the selected trace itself continues to the later agent-run boundary,
but no post-deadline submission is used to replace the official result. Exact
token, runtime, and unavailable-USD disclosures are in
[`REPRODUCTION_COSTS.json`](REPRODUCTION_COSTS.json), with hashes in
[`REPRODUCTION_MATERIAL_MANIFEST.sha256`](REPRODUCTION_MATERIAL_MANIFEST.sha256).
