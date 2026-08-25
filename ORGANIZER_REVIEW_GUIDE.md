# Organizer review guide — Tasks 1–6

This page is a short audit route for the organizer or Jury. It is a request
for determinations, not a self-issued compliance certificate. The preserved
artifacts and hashes are authoritative; this guide only points to them and
separates supported facts from questions that require organizer judgment.

## Fast verification route

From the repository root, run:

```bash
python3 tools/build_execution_trace_index.py
python3 tools/build_autonomous_trace_material.py
python3 verify_repository.py
for t in 1 2 3 4 5 6; do (cd task$t && sha256sum -c MANIFEST.sha256); done
sha256sum -c AUTONOMOUS_MATERIAL_MANIFEST.sha256
sha256sum -c REPRODUCTION_MATERIAL_MANIFEST.sha256
```

`verify_repository.py` checks the six task packages, score records, selected
trace boundaries, prompt classifications, event-type coverage, exact Task 6
artifacts, extraction metadata, all advertised checklist paths, and all
material hashes. It also runs the Task 1 package/provenance verifier and all
eight Task 3 source/output replays, and scans tracked text for common
unredacted credentials and private endpoints. It should print `"all_ok": true`.
The repository must remain private while the restricted Task 3 competition
bundle is present; see `task3/DATA_PROVENANCE.md`.

## Six-task adjudication matrix

| Task | Evidence-supported positive finding | Open organizer/Jury determination |
|---|---|---|
| 1 | A complete observable, no-live-human later 120-minute reproduction is preserved, with a canonical prefix through `task_complete`; the original run record was lost after a school-server restart. | Whether this later reproduction may substitute for the lost original trace; whether its custom starter appendix is acceptable. It must not be treated as causal evidence for official final refs `55267333`/`55267368`. |
| 2 | A complete observable, no-live-human later 120-minute reproduction is preserved; the formal pre-boundary submission `55260695` is separately recorded. | Whether the later reproduction may satisfy the requested trace deliverable despite being post-deadline and custom-starter based. Official final `55261432` is downstream of the formal boundary and is not attributed to that trace. |
| 3 | Eight scored submissions, including the tied official Public-best refs `55289569`/`55289823`, are in exact-prompt autonomous scope before the supervision boundary. | Whether the 27 captured account submissions (16 after the deadline) count against the published 15-submission rule, or whether enforcement is limited to scored competition-window submissions. The package does not decide this. |
| 4 | Final submission `55316818` is trace-aligned, before deadline, notebook-only, one-T4, and has exact output/artifact evidence; all 12 selected solver traces are indexed. | Whether the formatting-modified starter and substantive generic continuation are acceptable operational deviations; whether the transient local `__pycache__` affects the two-file folder rule. |
| 5 | Final v6 submission `55320296` is trace-aligned, exact-prompt, before deadline, notebook-only, one-T4, and its output/log are preserved. | Whether the trace-preserved v6 source is sufficient when Kaggle now returns 403 for the historical source pull, and whether the historical report-format limitations are material. |
| 6 | Final v3 submission `55357080` is trace-aligned and exact-prompt; notebook metadata, decoded source, weights, CSV, parameter count, and hashes verify exactly. | Whether the measured evaluator-batch dependence and the historical report's factual range/dropout errors affect eligibility. They are disclosed technical/report facts, not silently removed or declared harmless by this package. |

## Evidence map

- Trace selection and causal boundaries: `AUTONOMOUS_TRACE_MATERIAL.md`,
  `AUTONOMOUS_TRACE_INDEX.json`, and `AUTONOMOUS_MATERIAL_MANIFEST.sha256`.
- Official rules, Starter Prompts, and Continuation Prompts: the
  `official_sources` arrays in `ORGANIZER_SUBMISSION.json` point to the exact
  per-task snapshots; these are checked by `verify_repository.py`.
- Later Task 1/2 reproductions: `REPRODUCTION_TRACE_MATERIAL.md`,
  `REPRODUCTION_TRACE_INDEX.json`, and `REPRODUCTION_COSTS.json`.
- Exact prompt comparison: `PROMPT_CONFORMANCE_AUDIT.md` and
  `PROMPT_CONFORMANCE_AUDIT.json`.
- Cross-task findings: `RULE_COMPLIANCE_AUDIT.md` and
  `RULE_COMPLIANCE_AUDIT.json`.
- Official account reconciliation: `FINAL_SUBMISSION_RESULTS.md` and each
  `taskN/remote/FINAL_ACCOUNT_RESULTS.json`.
- Task 4 detailed audit: `task4/RULE_DIFFERENCE_AUDIT.md` and
  `task4/RULE_DIFFERENCE_AUDIT.json`.
- Task 6 artifact and evaluator evidence: `task6/ARTIFACT_PROVENANCE.json`,
  `task6/RULE_DIFFERENCE_AUDIT.md`, `task6/RULE_DIFFERENCE_AUDIT.json`, and
  `task6/evidence/EVALUATOR_BATCHING_PROVENANCE.json`.
- Extraction archive: `KAGGLE_EXTRACTION_DELIVERY.json` and the linked Drive
  archive. Its archive hash and size are recorded there and in the verifier.
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
