# Organizer submission — Tasks 1–6

This is the single entry point for every requested deliverable. The
machine-readable checklist is [`ORGANIZER_SUBMISSION.json`](ORGANIZER_SUBMISSION.json),
and `python3 verify_repository.py` validates the paths, hashes, score records,
trace coverage, model/cost fields, and extraction metadata.

For the shortest organizer/Jury audit route, start with
[`ORGANIZER_REVIEW_GUIDE.md`](ORGANIZER_REVIEW_GUIDE.md). It lists the exact
verification commands, evidence map, and the few determinations that cannot be
resolved from the preserved historical records.

The compact current-status hand-off is [`AUDIT_STATUS.md`](AUDIT_STATUS.md).
It summarizes the six official account results, selected trace scope, prompt
qualification, cost accounting, and remaining Jury decisions without replacing
the detailed evidence.

The numbered [`OPEN_REVIEW_ITEMS.md`](OPEN_REVIEW_ITEMS.md) register gathers
those remaining decisions in one place, with a direct evidence link for each
item.

For a requirement-by-requirement view, use the
[`REQUIREMENT_EVIDENCE_MATRIX.md`](REQUIREMENT_EVIDENCE_MATRIX.md) table or its
machine-readable [`REQUIREMENT_EVIDENCE_MATRIX.json`](REQUIREMENT_EVIDENCE_MATRIX.json).
It explicitly separates official-account scope, selected-trace scope,
artifact scope, known deviations, and Jury-interpretation risks.

> **Restricted-data notice:** `task3/input/competition/` contains
> organizer-provided data for authorized review. Keep this repository private
> and follow [`task3/DATA_PROVENANCE.md`](task3/DATA_PROVENANCE.md) before
> sharing or publishing any copy.

The separate repository/Drive distinction is documented in
[`ACCESS_CONTROL_AUDIT.md`](ACCESS_CONTROL_AUDIT.md). GitHub Private status does
not automatically apply to the external Google Drive extraction link.

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

- Tasks 1–2 later reproductions: [`REPRODUCTION_TRACE_MATERIAL.md`](REPRODUCTION_TRACE_MATERIAL.md), [`REPRODUCTION_TRACE_INDEX.json`](REPRODUCTION_TRACE_INDEX.json), [`REPRODUCTION_COSTS.json`](REPRODUCTION_COSTS.json), and the integrity [`REPRODUCTION_MATERIAL_MANIFEST.sha256`](REPRODUCTION_MATERIAL_MANIFEST.sha256).
- Tasks 1–2 bounded formal prefixes: [`FORMAL_PREFIX_AUDIT.md`](FORMAL_PREFIX_AUDIT.md) and [`FORMAL_PREFIX_AUDIT.json`](FORMAL_PREFIX_AUDIT.json).
- Startup instruction payloads actually injected into each run: [`STARTUP_INSTRUCTION_INDEX.md`](STARTUP_INSTRUCTION_INDEX.md), machine-readable [`STARTUP_INSTRUCTION_INDEX.json`](STARTUP_INSTRUCTION_INDEX.json), and the six linked `taskN/environment/AGENTS-ACTUALLY-INJECTED.md` files.
- Read-only extraction member verifier: [`tools/verify_extraction_bindings.py`](tools/verify_extraction_bindings.py), which checks the candidate source/output/log hashes against the downloaded Drive archive without upgrading any exact-version-confidence claim.
- Tasks 1–2 external final-result candidates: [`task1/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json`](task1/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json) and [`task2/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json`](task2/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json). These are kernel-linked candidates from the Kaggle extraction; neither has byte-confirmed exact-version binding to the official final ref.
- Task 1/2 version mapping clarification: [`KERNEL_VERSION_MAPPING_AUDIT.md`](KERNEL_VERSION_MAPPING_AUDIT.md) records the exact internal `scriptVersionId` values, the strongest archive `vN` candidates, the Task 1 byte-equivalent v5/v6 class, and the remaining no-submitted-digest limitation.
- Startup instruction lineage: [`AGENT_INSTRUCTION_LINEAGE.md`](AGENT_INSTRUCTION_LINEAGE.md) explains why the six task-scoped `AGENTS-ACTUALLY-INJECTED.md` payloads are the authoritative runtime records rather than a single shared `AGENT.md`.
- Submission/version budget audit: [`SUBMISSION_VERSION_AUDIT.md`](SUBMISSION_VERSION_AUDIT.md) and [`SUBMISSION_VERSION_AUDIT.json`](SUBMISSION_VERSION_AUDIT.json). This explicitly checks the published budget and the one-submission-per-Notebook-version rule, including repeated `scriptVersionId` values.
- Task 4 supplemental trace provenance: [`task4/evidence/SUPPLEMENTAL_ROLLOUT_PROVENANCE.json`](task4/evidence/SUPPLEMENTAL_ROLLOUT_PROVENANCE.json) and [`task4/RULE_DIFFERENCE_AUDIT.md`](task4/RULE_DIFFERENCE_AUDIT.md).
- Task 6 exact v3 artifact chain and corrected report supplement: [`task6/ARTIFACT_PROVENANCE.json`](task6/ARTIFACT_PROVENANCE.json), [`task6/RULE_DIFFERENCE_AUDIT.md`](task6/RULE_DIFFERENCE_AUDIT.md), [`task6/SUPPLEMENTARY_TECHNICAL_REPORT.md`](task6/SUPPLEMENTARY_TECHNICAL_REPORT.md), and [`task6/evidence/EVALUATOR_BATCHING_PROVENANCE.json`](task6/evidence/EVALUATOR_BATCHING_PROVENANCE.json).

## Deliverable checklist

| Organizer requirement | Status | Evidence |
|---|---|---|
| Execution traces for Tasks 1–6 | Complete selected observable prefixes; provenance limits disclosed | [`AUTONOMOUS_TRACE_MATERIAL.md`](AUTONOMOUS_TRACE_MATERIAL.md), [`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json) |
| Later two-hour reproduction traces for Tasks 1–2 | Complete, separately scoped post-deadline reproductions; not the lost originals | [`REPRODUCTION_TRACE_MATERIAL.md`](REPRODUCTION_TRACE_MATERIAL.md), [`REPRODUCTION_TRACE_INDEX.json`](REPRODUCTION_TRACE_INDEX.json), [`REPRODUCTION_COSTS.json`](REPRODUCTION_COSTS.json), [`REPRODUCTION_MATERIAL_MANIFEST.sha256`](REPRODUCTION_MATERIAL_MANIFEST.sha256) |
| Prompts and visible Agent outputs | Complete within selected observable trace scope | Full payloads are in every indexed JSONL trace; prompt classes and hashes are in the index |
| Startup `AGENTS.md` payloads | Indexed and hash-bound per Task | [`STARTUP_INSTRUCTION_INDEX.md`](STARTUP_INSTRUCTION_INDEX.md), [`STARTUP_INSTRUCTION_INDEX.json`](STARTUP_INSTRUCTION_INDEX.json); each payload is also covered by its Task manifest |
| Task 1/2 official-ref version mapping | Exact internal `scriptVersionId` evidence with candidate/byte limits clearly separated | [`KERNEL_VERSION_MAPPING_AUDIT.md`](KERNEL_VERSION_MAPPING_AUDIT.md) and the two task-level extraction provenance JSON files |
| Drive archive member bindings | Read-only verifier available for authorized archive copy | [`tools/verify_extraction_bindings.py`](tools/verify_extraction_bindings.py); candidate provenance records and archive delivery hash |
| Exact organizer prompt conformance | Audited; canonical Task 1/2 reproductions and Task 4 are non-exact, while the supplemental Task 1/2 formal prefixes are exact-prompt bounded evidence | [`PROMPT_CONFORMANCE_AUDIT.md`](PROMPT_CONFORMANCE_AUDIT.md), [`PROMPT_CONFORMANCE_AUDIT.json`](PROMPT_CONFORMANCE_AUDIT.json), [`FORMAL_PREFIX_AUDIT.md`](FORMAL_PREFIX_AUDIT.md) |
| Cross-task rule compliance | Audited; known deviations and evidence/interpretation limits remain | [`RULE_COMPLIANCE_AUDIT.md`](RULE_COMPLIANCE_AUDIT.md), [`RULE_COMPLIANCE_AUDIT.json`](RULE_COMPLIANCE_AUDIT.json) |
| Submission/version limits | Audited against extracted `script_version_id`, deadline offset, task budget fields, and per-task summary bindings | [`SUBMISSION_VERSION_AUDIT.md`](SUBMISSION_VERSION_AUDIT.md), [`SUBMISSION_VERSION_AUDIT.json`](SUBMISSION_VERSION_AUDIT.json), `task1/SUMMARY.json` through `task6/SUMMARY.json` |
| Rule-by-rule evidence map | Complete, scope-labeled for 11 requirements per Task | [`REQUIREMENT_EVIDENCE_MATRIX.md`](REQUIREMENT_EVIDENCE_MATRIX.md), [`REQUIREMENT_EVIDENCE_MATRIX.json`](REQUIREMENT_EVIDENCE_MATRIX.json) |
| Open organizer/Jury decisions | Centralized numbered register; facts and requested dispositions kept separate | [`OPEN_REVIEW_ITEMS.md`](OPEN_REVIEW_ITEMS.md) |
| Access-control and delivery scope | Audited separately for Private GitHub, external Drive, and archive content limits | [`ACCESS_CONTROL_AUDIT.md`](ACCESS_CONTROL_AUDIT.md), [`ACCESS_CONTROL_AUDIT.json`](ACCESS_CONTROL_AUDIT.json) |
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

Because the archive is approximately 474 MiB, Google Drive may first show its
standard virus-scan warning page. Choose **Download anyway**; the delivery
record below preserves the archive hash, byte length, filename, and byte-range
support for the resulting download.

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
The complete original Task 1 and Task 2 run records were unavailable after a
school-server restart; bounded pre-boundary formal prefixes remain as separate
historical audit evidence. These are later fresh reproductions using the same
configured solver/system, official competition bundle, and organizer
constraints, not replacements for the incomplete original records. See
[`FORMAL_PREFIX_AUDIT.md`](FORMAL_PREFIX_AUDIT.md).
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
