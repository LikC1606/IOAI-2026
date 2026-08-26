# Organizer review guide — Tasks 1–6

This page is a short audit route for the organizer or Jury. It is a request
for determinations, not a self-issued compliance certificate. The preserved
artifacts and hashes are authoritative; this guide only points to them and
separates supported facts from questions that require organizer judgment.

For the shortest one-page hand-off of scores, trace scope, cost accounting,
and unresolved decisions, see [`AUDIT_STATUS.md`](AUDIT_STATUS.md).
For the same unresolved questions in a compact, numbered decision register,
see [`OPEN_REVIEW_ITEMS.md`](OPEN_REVIEW_ITEMS.md).

The fastest field-by-field route is the
[`REQUIREMENT_EVIDENCE_MATRIX.md`](REQUIREMENT_EVIDENCE_MATRIX.md) (11 rows per
task: autonomy, trace alignment, prompt, notebook flow, budget, runtime,
resources, hardware, output, report, and deadline). This index is deliberately
scope-labeled and is not a self-issued compliance certificate.

Before sharing, check [`ACCESS_CONTROL_AUDIT.md`](ACCESS_CONTROL_AUDIT.md): the
GitHub repository is Private, while the external Drive extraction has its own
link-access scope and a separately documented content scan.
For the exact runtime instruction context, use
[`STARTUP_INSTRUCTION_INDEX.md`](STARTUP_INSTRUCTION_INDEX.md) and its
machine-readable companion [`STARTUP_INSTRUCTION_INDEX.json`](STARTUP_INSTRUCTION_INDEX.json),
which link and hash the six `AGENTS-ACTUALLY-INJECTED.md` payloads.

## Fast verification route

From the repository root, run:

```bash
# This read-only route works from the checked-in package alone:
python3 verify_repository.py
for t in 1 2 3 4 5 6; do (cd task$t && sha256sum -c MANIFEST.sha256); done
sha256sum -c AUTONOMOUS_MATERIAL_MANIFEST.sha256
sha256sum -c REPRODUCTION_MATERIAL_MANIFEST.sha256
# Optional refresh, only when the preserved private historical sources exist:
python3 tools/build_reproduction_trace_material.py
python3 tools/build_execution_trace_index.py
python3 tools/build_autonomous_trace_material.py
python3 verify_repository.py
for t in 1 2 3 4 5 6; do (cd task$t && sha256sum -c MANIFEST.sha256); done
sha256sum -c AUTONOMOUS_MATERIAL_MANIFEST.sha256
sha256sum -c REPRODUCTION_MATERIAL_MANIFEST.sha256
# Optional, after downloading the Drive archive:
python3 tools/verify_extraction_bindings.py --archive /path/to/ioai-kaggle-fetch-researai-20260813.tar.gz
```

`verify_repository.py` checks the six task packages, score records, selected
trace boundaries, prompt classifications, event-type coverage, exact Task 6
artifacts, Task 4/5 provenance chains, Task 4 rule-status classifications,
Task 5 historical-source limitation, Task 6 measured-behavior disclosures,
extraction metadata, all advertised checklist paths, and all material hashes.
The separate `SUBMISSION_VERSION_AUDIT.json` checks exact extracted
`script_version_id` reuse and literal task-budget counts; it is intentionally
not reduced to a green check when the published wording is contradicted.
It also runs the Task 1 package/provenance verifier and all eight Task 3
source/output replays, and scans tracked text for common unredacted
credentials and private endpoints. It should print `"all_ok": true`.
The repository must remain private while the restricted Task 3 competition
bundle is present; see `task3/DATA_PROVENANCE.md`.

In the verifier output, `package_positive_claim` is deliberately scope-labeled
and is separate from `final_account_result`. In particular, Task 1's positive
claim is the separately disclosed post-supervision/post-deadline Agent-executed
result, while Task 2's is the bounded pre-boundary formal result; neither field
is presented as those accounts' official final or as the later reproduction.

The extraction cross-check is deliberately explicit: each `taskN/SUMMARY.json`
contains an `extraction_summary_binding` with the source hash, competition
slug, deadline, account submission count, post-deadline count, captured
version count, and kernel count. The verifier compares those bindings with
`KAGGLE_EXTRACTION_SUMMARY.json` and with each task's
`remote/FINAL_ACCOUNT_RESULTS.json`; a green result means these records agree,
not that the account history is automatically rule-compliant.
Each task summary also carries a `submission_version_audit` binding with the
applicable budget kind/limit, observed count, duplicate-version count, and
combined literal status. The verifier cross-checks those fields against the
complete extracted ref/version audit.

## Suggested adjudication order

The package intentionally separates mechanical evidence from decisions that
cannot be reconstructed from the preserved records. A reviewer can therefore
make the minimum factual findings first and defer only the policy questions:

1. Confirm the six task manifests, the autonomous/reproduction manifests, the
   formal-prefix audit, and `python3 verify_repository.py`.
2. Treat Tasks 3, 5, and 6 as the exact-prompt, trace-aligned positive set
   supported by the preserved artifacts. Their task-specific report, budget,
   and technical disclosures remain part of the record.
3. For Task 4, decide whether the disclosed formatting-modified Starter,
   substantive generic continuation, transient local `__pycache__`, and local
   H100 development are acceptable under the competition wording. The final
   v4 source, T4 output provenance, deadline timestamp, and remote metadata are
   independently verified.
4. For Tasks 1 and 2, keep three scopes separate: the bounded exact-prompt
   formal prefix, the requested later two-hour no-live-human reproduction, and
   the account's automatic official final. The extraction also provides a
   kernel-linked source/output candidate for each official final, but neither
   candidate has byte-confirmed exact-version binding. The formal prefix is not
   silently promoted to a complete historical run, and the reproduction is not
   used as causal evidence for the official final.
5. For Tasks 1–3, review `SUBMISSION_VERSION_AUDIT.md`: Task 1's official
   final refs reuse one Notebook version; Task 2's eligible v2 pair reuses one
   version; Task 3 has a repeated version immediately before the deadline.
   Task 1 and Task 3 also exceed the literal account-wide extracted budget
   counts. The package separately shows the deadline-scoped Task 3 count (11
   before the deadline, within the published 15) and the account-wide count
   (27), without selecting an interpretation. Any exception or enforcement
   scope for pre-deadline version reuse and post-deadline activity remains for
   organizer adjudication.
6. For Task 3, decide whether the published 15-submission rule is applied to
   the 11 deadline-eligible submissions under the timeline clause or to all 27
   account records, including the 16 post-deadline submissions.
7. Record any exception or interpretation in writing. The repository's
   `all_ok` result means internal evidence consistency, not organizer
   acceptance.

## Six-task adjudication matrix

| Task | Evidence-supported positive finding | Open organizer/Jury determination |
|---|---|---|
| 1 | A complete observable, no-live-human later 120-minute reproduction is preserved, with a canonical prefix through `task_complete`; a bounded exact-prompt formal prefix is also retained after the complete original record became unavailable following a school-server restart. | Whether the later reproduction or supplemental formal prefix may satisfy the requested trace deliverable; whether the custom starter appendix is acceptable; and whether the literal 38/20 version count and duplicate official-final version receive an exception. Neither reproduction is causal evidence for official final refs `55267333`/`55267368`. |
| 2 | A complete observable, no-live-human later 120-minute reproduction is preserved; the exact-prompt formal prefix and eligible v2 submission `55260695` are separately recorded. | Whether the later reproduction may satisfy the requested trace deliverable despite being post-deadline and custom-starter based, and whether the duplicate use of scriptVersionId `340290308` is excused. Official final `55261432` is downstream of the modified formal boundary and is not attributed to the later reproduction. |
| 3 | Eight scored submissions, including the tied official Public-best refs `55289569`/`55289823`, are in exact-prompt autonomous scope before the supervision boundary. | The account history has 27 submissions (11 before and 16 after deadline). The deadline-scoped count is within 15, while the account-wide count exceeds 15; the package records both readings. It also repeats scriptVersionId `340521169` immediately before the deadline. The count interpretation and pre-deadline version reuse remain organizer decisions. |
| 4 | Final submission `55316818` is trace-aligned, before deadline, notebook-only, one-T4, and has exact output/artifact evidence; all 12 selected solver traces are indexed. | Whether the formatting-modified starter and substantive generic continuation are acceptable operational deviations; whether the transient local `__pycache__` affects the two-file folder rule. |
| 5 | Final v6 submission `55320296` is trace-aligned, exact-prompt, before deadline, notebook-only, one-T4, and its output/log are preserved. | Whether the trace-preserved v6 source is sufficient when Kaggle now returns 403 for the historical source pull, and whether the historical report-format limitations are material. |
| 6 | Final v3 submission `55357080` is trace-aligned and exact-prompt; notebook metadata, decoded source, weights, CSV, parameter count, and hashes verify exactly. The evaluator-batch dependence is retained as a measured technical disclosure and is not classified as a compliance issue. | Whether the historical report's factual range/dropout errors are material to eligibility. The evaluator behavior is not an open compliance determination in this package; it remains documented for reproducibility. |

## Evidence map

- Trace selection and causal boundaries: `AUTONOMOUS_TRACE_MATERIAL.md`,
  `AUTONOMOUS_TRACE_INDEX.json`, and `AUTONOMOUS_MATERIAL_MANIFEST.sha256`.
- Startup instruction context: `STARTUP_INSTRUCTION_INDEX.md/json` and the six
  `taskN/environment/AGENTS-ACTUALLY-INJECTED.md` files, each covered by its
  Task manifest.
- Drive archive member bindings: `tools/verify_extraction_bindings.py` checks
  the hashes cited by the Task 1/2 candidate and Task 4 extraction provenance.
- Official rules, Starter Prompts, and Continuation Prompts: the
  `official_sources` arrays in `ORGANIZER_SUBMISSION.json` point to the exact
  per-task snapshots; these are checked by `verify_repository.py`. Task 3's
  exact continuation is also available directly at
  `task3/official/CONTINUE_PROMPT_EXACT.md`, with byte equality checked against
  the full official-page snapshot.
- Later Task 1/2 reproductions: `REPRODUCTION_TRACE_MATERIAL.md`,
  `REPRODUCTION_TRACE_INDEX.json`, and `REPRODUCTION_COSTS.json`.
- Supplemental bounded formal prefixes for Tasks 1–2:
  `FORMAL_PREFIX_AUDIT.md` and `FORMAL_PREFIX_AUDIT.json`.
- Exact prompt comparison: `PROMPT_CONFORMANCE_AUDIT.md` and
  `PROMPT_CONFORMANCE_AUDIT.json`.
- Cross-task findings: `RULE_COMPLIANCE_AUDIT.md` and
  `RULE_COMPLIANCE_AUDIT.json`.
- Submission/version limits: `SUBMISSION_VERSION_AUDIT.md` and
  `SUBMISSION_VERSION_AUDIT.json`.
- Official account reconciliation: `FINAL_SUBMISSION_RESULTS.md` and each
  `taskN/remote/FINAL_ACCOUNT_RESULTS.json`.
- Task 1/2 external final-result candidates (not exact-version claims):
  `task1/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json` and
  `task2/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json`.
- Task 4 detailed audit: `task4/RULE_DIFFERENCE_AUDIT.md` and
  `task4/RULE_DIFFERENCE_AUDIT.json`.
- Task 6 artifact and evaluator evidence: `task6/ARTIFACT_PROVENANCE.json`,
  `task6/RULE_DIFFERENCE_AUDIT.md`, `task6/RULE_DIFFERENCE_AUDIT.json`, and
  `task6/evidence/EVALUATOR_BATCHING_PROVENANCE.json`.
- Extraction archive: `KAGGLE_EXTRACTION_DELIVERY.json` and the linked Drive
  archive. Its archive hash and size are recorded there and in the verifier;
  the delivery record also contains a live HTTP 200 HEAD check with matching
  `Content-Length`, filename, and byte-range support. For this approximately
  474 MiB file, Drive may show a virus-scan warning first; use **Download
  anyway** to reach the archive.
- Extraction/account cross-check: `KAGGLE_EXTRACTION_SUMMARY.json` and the
  `extraction_summary_binding` blocks in the six task summaries. This binds
  the six competition slugs, deadlines, submission totals, late-submission
  totals, captured-version totals, and kernel counts to the per-task account
  result records.
- Final notebook/output chains: Task 2 is verified from the autonomous eligible
  v2 source, exact 7,200-row CSV, metadata, log, and score record. Task 4 is
  verified from its exact source,
  metadata, log, and hash-only 190 MB output provenance; Task 5 is verified
  from the trace-preserved v6 source, exact archived CSV/log, metadata, and
  hashes; Task 6 is replayed from the exact v3 envelope and decoded source.

## Scope and cost notes

The selected traces retain observable prompts, Agent outputs, worker
assignments, tool-call envelopes, and tool outputs within each declared causal
boundary. Hidden chain-of-thought, encrypted opaque reasoning, credentials,
private endpoints, and excluded live-human prompt bodies are intentionally not
published. A complete selected trace is therefore not a claim that every
historical official result is trace-bound.

Token totals and selected remote Kaggle runtime are recorded. Exact API USD,
exhaustive local H100 runtime for Tasks 4–6, and GPU USD are unavailable; the
cost ledgers leave those fields null rather than inventing rates or invoices.

The final eligibility decision remains with the organizer/Jury. This guide is
intended to make the remaining decisions explicit and quickly verifiable.
