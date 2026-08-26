# Open review items — decision register

This is a compact register of the questions that cannot be settled by a
repository hash or a replay. It is intended to keep an organizer/Jury review
focused: the facts are preserved in the linked evidence, while the requested
disposition remains with the organizer. An item listed here is not an
admission beyond the scope stated in its evidence, and the repository does not
issue a compliance certificate.

| ID | Scope | Evidence-backed fact | Requested organizer/Jury disposition |
|---|---|---|---|
| R1 | Task 1 | The complete raw formal session was subsequently recovered privately after the school-server restart. Its 350-event exact-prompt prefix and a separate later 120-minute no-live-human reproduction are preserved publicly; the 425-event human-influenced suffix is intentionally withheld, and neither public selection is the historical official-final trace. | Decide whether either separately labeled record satisfies the requested trace deliverable, and whether the custom appendix in the later reproduction is acceptable. See [`FORMAL_PREFIX_AUDIT.md`](FORMAL_PREFIX_AUDIT.md), [`ORIGINAL_SESSION_RECOVERY.md`](ORIGINAL_SESSION_RECOVERY.md), [`task1/COMPLIANCE.md`](task1/COMPLIANCE.md). |
| R2 | Task 2 | The complete raw formal session was subsequently recovered privately after the school-server restart. Its 705-event exact-prompt prefix (with eligible v2 result) and a separate later reproduction are preserved publicly; the 662-event suffix begins with a modified continuation and is intentionally withheld. | Decide how the formal prefix and later reproduction should be recognized, and whether the custom appendix in the later reproduction is acceptable. See [`FORMAL_PREFIX_AUDIT.md`](FORMAL_PREFIX_AUDIT.md), [`ORIGINAL_SESSION_RECOVERY.md`](ORIGINAL_SESSION_RECOVERY.md), [`task2/COMPLIANCE.md`](task2/COMPLIANCE.md). |
| R3 | Task 1 | The extracted account proves the official refs and linked `scriptVersionId`, but the archive candidate is not byte-confirmed as the exact scored source/output for either tied ref. | Decide whether the candidate-level provenance is sufficient or whether an exact-version artifact is required. See [`KERNEL_VERSION_MAPPING_AUDIT.md`](KERNEL_VERSION_MAPPING_AUDIT.md), [`task1/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json`](task1/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json). |
| R4 | Task 2 | The extracted account proves the official ref and linked kernel candidate, but the exact scored source/output bytes are not byte-confirmed. | Decide whether candidate-level provenance is sufficient. See [`KERNEL_VERSION_MAPPING_AUDIT.md`](KERNEL_VERSION_MAPPING_AUDIT.md), [`task2/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json`](task2/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json). |
| R5 | Task 1 | The extraction records 38 captured notebook versions against the published 20-version wording, and `scriptVersionId=340342513` was used for both official-final refs. | Decide the applicable post-deadline scope and any exception for repeated-version submission. See [`SUBMISSION_VERSION_AUDIT.md`](SUBMISSION_VERSION_AUDIT.md). |
| R6 | Task 2 | The extraction records 18 versions (within the count) but `scriptVersionId=340290308` was submitted twice before the deadline. | Decide whether the one-submission-per-version conflict is excused. See [`SUBMISSION_VERSION_AUDIT.md`](SUBMISSION_VERSION_AUDIT.md). |
| R7 | Task 3 | The account has 27 submissions: 11 before and 16 after the deadline. The deadline-scoped count is within 15, while the account-wide count is not; one version was also submitted twice immediately before the deadline. | Decide whether the limit is deadline-scoped or account-wide and how repeated-version use is treated. See [`SUBMISSION_VERSION_AUDIT.md`](SUBMISSION_VERSION_AUDIT.md). |
| R8 | Task 3 | Historical v1–v8 reports are shorter than the requested 8–10 paragraphs; v8 also has a score/distribution documentation discrepancy. Exact source and output files are preserved unchanged, with a separate correction supplement. | Decide whether these report-format and factual issues are material. See [`task3/REPORT_COMPLIANCE.md`](task3/REPORT_COMPLIANCE.md), [`task3/SUPPLEMENTARY_TECHNICAL_REPORT.md`](task3/SUPPLEMENTARY_TECHNICAL_REPORT.md). |
| R9 | Task 4 | The selected trace contains a formatting-modified Starter and substantive generic continuation; a transient local `__pycache__` was present, and local development mentions an H100 although the submitted notebook used one T4. | Decide whether these process, folder, and local-development differences affect eligibility. See [`task4/RULE_DIFFERENCE_AUDIT.md`](task4/RULE_DIFFERENCE_AUDIT.md). |
| R10 | Task 5 | Kaggle currently returns HTTP 403 for the historical v6 source pull. The trace-preserved source is hash-bound to the v6 push; output, log, metadata, score, and submission record are retained. | Decide whether the preserved source plus independent remote artifacts is sufficient. See [`task5/COMPLIANCE.md`](task5/COMPLIANCE.md), [`task5/V6_SOURCE_PROVENANCE.json`](task5/V6_SOURCE_PROVENANCE.json). |
| R11 | Task 6 | The historical report has dropout/range value errors; the exact v3 source, weights, CSV, and decoded model verify. Evaluator-batch dependence is measured and disclosed as a technical property, not classified as a rule violation. | Decide whether the report errors are material. See [`task6/RULE_DIFFERENCE_AUDIT.md`](task6/RULE_DIFFERENCE_AUDIT.md), [`task6/SUPPLEMENTARY_TECHNICAL_REPORT.md`](task6/SUPPLEMENTARY_TECHNICAL_REPORT.md). |
| R12 | All tasks | Token totals and selected Kaggle runtime are recorded. Actual provider/GPU USD cannot be reconstructed from invoices. A separate budget estimate applies official GPT-5.6 Sol rates and the requested 2-H100 × 2-hour-per-Task assumption, with a public H100 median/range. | Decide whether the labeled estimates are sufficient for the cost deliverable or request an external invoice/runtime record. See [`COST_ESTIMATE.md`](COST_ESTIMATE.md), [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json), [`COSTS.json`](COSTS.json). |
| R13 | Repository access | `task3/input/competition/` contains restricted organizer data; the GitHub repository must remain private while it is present. The large Kaggle extraction is delivered separately on Google Drive with a recorded archive hash. | Confirm reviewer access and handling scope before redistribution. See [`ACCESS_CONTROL_AUDIT.md`](ACCESS_CONTROL_AUDIT.md), [`KAGGLE_EXTRACTION_DELIVERY.json`](KAGGLE_EXTRACTION_DELIVERY.json). |

## Findings intentionally not escalated as rule violations

Development-time literature searches are retained as method-background
provenance and are not runtime inputs. Task 6's measured evaluator batching
dependence is disclosed for technical reproducibility and is not classified as
a compliance blocker in this package. These classifications remain reviewable
by the organizer; they are not claims of organizer acceptance.

## Mechanical checks

The open items above do not change the historical artifacts. Verify the
published package with:

```bash
python3 verify_repository.py
for t in 1 2 3 4 5 6; do (cd task$t && sha256sum -c MANIFEST.sha256); done
sha256sum -c AUTONOMOUS_MATERIAL_MANIFEST.sha256
sha256sum -c REPRODUCTION_MATERIAL_MANIFEST.sha256
```

These checks establish internal consistency only. They do not resolve any
item in this register.
