# IOAI 2026 Evidence Records

Organizer-review materials for IOAI 2026 Tasks 1-6. Start with
[`ORGANIZER_SUBMISSION.md`](ORGANIZER_SUBMISSION.md), which maps every requested
deliverable to its exact evidence path and machine-verifiable status. The
shortest audit route is [`ORGANIZER_REVIEW_GUIDE.md`](ORGANIZER_REVIEW_GUIDE.md).
For a one-page hand-off of the current scope, scores, costs, and unresolved
decisions, see [`AUDIT_STATUS.md`](AUDIT_STATUS.md).
For a compact numbered register of the remaining organizer/Jury questions, see
[`OPEN_REVIEW_ITEMS.md`](OPEN_REVIEW_ITEMS.md).
For a single-table coverage view of every requested trace, prompt, output,
model, cost, and result field, see
[`PACKAGE_COMPLETENESS.md`](PACKAGE_COMPLETENESS.md). It is generated from the
checked-in ledgers and independently checked by `verify_repository.py`.
The cross-task [`RULE_COMPLIANCE_AUDIT.md`](RULE_COMPLIANCE_AUDIT.md) separates
known deviations, Jury-interpretation risks, and unavailable evidence; the
current record does not support a claim that all six tasks are strictly
compliant.
The field-by-field [`REQUIREMENT_EVIDENCE_MATRIX.md`](REQUIREMENT_EVIDENCE_MATRIX.md)
indexes the same limits against 11 concrete requirements per task.
The channel/access distinction is recorded in
[`ACCESS_CONTROL_AUDIT.md`](ACCESS_CONTROL_AUDIT.md).

> **Access note:** `task3/input/competition/` contains organizer data that is
> restricted to authorized reviewers. Keep this repository private and follow
> [`task3/DATA_PROVENANCE.md`](task3/DATA_PROVENANCE.md) before sharing or
> publishing any copy.

## Recommended review order

1. [`ORGANIZER_REVIEW_GUIDE.md`](ORGANIZER_REVIEW_GUIDE.md) — shortest audit
   route, verification commands, evidence map, and unresolved determinations.
2. [`ORGANIZER_SUBMISSION.md`](ORGANIZER_SUBMISSION.md) — complete deliverable
   checklist and evidence links.
3. [`OPEN_REVIEW_ITEMS.md`](OPEN_REVIEW_ITEMS.md) — compact decision register
   for the remaining organizer/Jury questions.
4. [`ORIGINAL_SESSION_RECOVERY.md`](ORIGINAL_SESSION_RECOVERY.md) — recovered
   private raw-session hashes/counts for the Task 1/2 formal runs and the
   causal reason their human-influenced suffixes are not published.
5. [`STARTUP_INSTRUCTION_INDEX.md`](STARTUP_INSTRUCTION_INDEX.md) and
   [`STARTUP_INSTRUCTION_INDEX.json`](STARTUP_INSTRUCTION_INDEX.json) — the
   actual startup `AGENTS.md` payload and hash for each Task run.
6. [`AGENT_INSTRUCTION_LINEAGE.md`](AGENT_INSTRUCTION_LINEAGE.md) — explains
   the task-scoped startup payload families; there was no single literal
   `AGENT.md` shared by all six runs.
7. [`KERNEL_VERSION_MAPPING_AUDIT.md`](KERNEL_VERSION_MAPPING_AUDIT.md) —
   separates exact Kaggle `scriptVersionId` evidence from the unresolved
   archive version/byte mapping for the Task 1/2 official refs.
8. [`FINAL_SUBMISSION_RESULTS.md`](FINAL_SUBMISSION_RESULTS.md) — official
   account results separated from autonomous and later reproduction results.
9. [`RULE_COMPLIANCE_AUDIT.md`](RULE_COMPLIANCE_AUDIT.md) and
   [`PROMPT_CONFORMANCE_AUDIT.md`](PROMPT_CONFORMANCE_AUDIT.md) — cross-task
   scope, exact-prompt, provenance, budget, hardware, and reporting audits.
10. [`REQUIREMENT_EVIDENCE_MATRIX.md`](REQUIREMENT_EVIDENCE_MATRIX.md) — one
   row per rule field with scope-labeled status and direct evidence paths.
11. [`SUBMISSION_VERSION_AUDIT.md`](SUBMISSION_VERSION_AUDIT.md) — exact
   account-level budget and repeated Notebook-version submission audit.
12. [`ACCESS_CONTROL_AUDIT.md`](ACCESS_CONTROL_AUDIT.md) — GitHub Private,
   external Drive delivery, and archive-content handling scope.
13. [`AUTONOMOUS_TRACE_MATERIAL.md`](AUTONOMOUS_TRACE_MATERIAL.md) and
   [`EXECUTION_TRACES.md`](EXECUTION_TRACES.md) — selected traces, event
   envelopes, boundaries, and token accounting; see also
   [`COSTS.json`](COSTS.json) for compute/accounting fields.
14. `task1/` through `task6/` — task-specific source, outputs, reports, and
   compliance notes.
15. [`KAGGLE_EXTRACTION_DELIVERY.json`](KAGGLE_EXTRACTION_DELIVERY.json) — the
   complete external Kaggle extraction archive and Drive delivery record.
16. [`EXTRACTION_BINDING_RECEIPT.json`](EXTRACTION_BINDING_RECEIPT.json) — the
   latest full archive hash and cited-member verification receipt; rerun the
   read-only checker when independently reviewing the Drive download.

## Scope labels used throughout

| Label | Meaning |
|---|---|
| **Official final** | The result reconciled from the extracted Kaggle account under the competition's automatic highest-Public-before-deadline rule. |
| **Canonical autonomous rollout** | The selected no-live-human trace and result for the package's stated boundary; for Tasks 1–2 it is a later post-deadline reproduction, separate from the recovered private formal session. |
| **Historical/reproduction evidence** | Other preserved submissions, reports, source copies, or later runs retained for audit context but not substituted for the official result. |

## Official result and scope summary

| Task | Competition | Official final Public LB | Status |
|---|---|---:|---|
| [Task 1](task1/) | `ioai-2026-task-1-westlake-nlp-24` | 0.77751 | Private 0.80474; tied refs `55267333` / `55267368`; final not trace-bound |
| [Task 2](task2/) | `ioai-2026-task-2-westlake-nlp-24` | 0.63583 | Private 0.62500; `55261432`; final not trace-bound |
| [Task 3](task3/) ([trace + costs](task3/EXECUTION_AND_COSTS.md)) | `ioai-2026-task-3-westlake-nlp-48` | 58.51666 | Private 51.61666; trace-aligned; budget/report disclosures |
| [Task 4](task4/) | `ioai-2026-task-4-westlake-nlp-24` | 98.41 | Private 98.32; `55316818`; trace-aligned, non-exact continuation |
| [Task 5](task5/) | `ioai-2026-task-5-westlake-nlp-24` | 95.39 | Private 96.06; `55320296`; v7 was late; source provenance disclosed |
| [Task 6](task6/) | `ioai-2026-task-6-westlake-nlp-60` | 75.01540 | Private 73.36234; `55357080`; batch behavior measured, not a blocker |

No final leaderboard placement is claimed. The final-score rows apply the
preserved automatic highest-Public-before-deadline rule to the extracted account
records; extracted Private scores remain historical submission fields, not
placement claims. For Tasks 1–6,
[`FINAL_SUBMISSION_RESULTS.md`](FINAL_SUBMISSION_RESULTS.md) separates the
official result, autonomous scope, chronological last account submission, and
all-account numerical maxima.

## Similar-looking index files

| File | Use it for |
|---|---|
| [`EXECUTION_TRACE_INDEX.json`](EXECUTION_TRACE_INDEX.json) / [`EXECUTION_TRACE_INDEX.md`](EXECUTION_TRACE_INDEX.md) | One inventory of the 35 selected redacted trace files, event counts, tool-call counts, and token totals. |
| [`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json) / [`AUTONOMOUS_TRACE_MATERIAL.md`](AUTONOMOUS_TRACE_MATERIAL.md) | The authoritative autonomous-scope classification: boundaries, prompt classes, exclusions, and exact-prompt status. |
| [`REPRODUCTION_TRACE_INDEX.json`](REPRODUCTION_TRACE_INDEX.json) / [`REPRODUCTION_TRACE_MATERIAL.md`](REPRODUCTION_TRACE_MATERIAL.md) | The separate full later two-hour Task 1/2 reproductions; these are post-deadline reference material. |
| [`COSTS.json`](COSTS.json) / [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json) | Token, model, accelerator-runtime, actual-charge fields, and labeled public-rate estimates for the selected 35-trace scope. |
| [`COST_ESTIMATE.md`](COST_ESTIMATE.md) | Per-task API estimate using official GPT-5.6 Sol rates and the requested 2×H100 × 2-hour server assumption, with survey range and formulas. |
| [`REPRODUCTION_COSTS.json`](REPRODUCTION_COSTS.json) / [`REPRODUCTION_MATERIAL_MANIFEST.sha256`](REPRODUCTION_MATERIAL_MANIFEST.sha256) | Cost/token fields and integrity hashes for the separate full Task 1/2 reproduction traces. |

## Generated material and safe refresh order

The trace indexes, trace guide, cost summary, prompt audit, Task 4 rule audit,
requirement matrix, and their SHA-256 material manifest are generated from the
preserved evidence.
The canonical full refresh is `build_autonomous_trace_material.py`; it rebuilds
the autonomous index/material, cost ledger, both audit reports, and the
autonomous material manifest in one consistent pass. The other builders remain
available as standalone diagnostic/regeneration tools when investigating one
component. Their roles are:

| Generated material | Refresh tool |
|---|---|
| `AUTONOMOUS_TRACE_INDEX.json`, `AUTONOMOUS_TRACE_MATERIAL.md`, `AUTONOMOUS_COSTS.json`, `PROMPT_CONFORMANCE_AUDIT.json/.md`, `task4/RULE_DIFFERENCE_AUDIT.json/.md`, `REQUIREMENT_EVIDENCE_MATRIX.json/.md`, `STARTUP_INSTRUCTION_INDEX.json/.md`, and `AUTONOMOUS_MATERIAL_MANIFEST.sha256` | `python3 tools/build_autonomous_trace_material.py` (canonical full refresh) |
| `EXECUTION_TRACE_INDEX.json/.md` | `python3 tools/build_execution_trace_index.py` (standalone execution inventory) |
| `REPRODUCTION_TRACE_INDEX.json`, `REPRODUCTION_TRACE_MATERIAL.md`, `REPRODUCTION_COSTS.json`, and `REPRODUCTION_MATERIAL_MANIFEST.sha256` | `python3 tools/build_reproduction_trace_material.py` (later Task 1/2 reproduction package; requires the preserved private historical source paths) |
| `PROMPT_CONFORMANCE_AUDIT.json/.md` | `python3 tools/build_prompt_conformance_audit.py` (standalone prompt diagnostic) |
| `task4/RULE_DIFFERENCE_AUDIT.json/.md` | `python3 tools/build_task4_rule_audit.py` (standalone Task 4 diagnostic) |
| `REQUIREMENT_EVIDENCE_MATRIX.json/.md` | Included in the canonical full refresh; `python3 tools/build_requirement_evidence_matrix.py` remains a standalone scope-labeled rule-index refresh |
| `PACKAGE_COMPLETENESS.json/.md` | `python3 tools/build_package_completeness.py` (coverage join; checked by `verify_repository.py`) |
| Extraction candidate member checks | [`EXTRACTION_BINDING_RECEIPT.json`](EXTRACTION_BINDING_RECEIPT.json) records the latest completed check; rerun `python3 tools/verify_extraction_bindings.py --archive /path/to/ioai-kaggle-fetch-researai-20260813.tar.gz` (read-only, after downloading the Drive archive) |

Recommended refresh order is: first run the read-only verifier and checked-in
manifest checks. If the preserved private historical source paths are
available, refresh the later-reproduction package, then the execution
inventory and canonical autonomous-material builder, and run the checks again.
If those private paths are unavailable, do not run the reproduction builder;
verify the checked-in reproduction manifest instead. After any refresh, run
`python3 verify_repository.py` and all manifest checks.
Do not hand-edit the JSONL traces, exact submission artifacts, or generated
hashes; make a source/evidence change first, then regenerate and verify.

```bash
# Always works from the checked-in package:
python3 verify_repository.py
for t in 1 2 3 4 5 6; do (cd task$t && sha256sum -c MANIFEST.sha256); done
sha256sum -c AUTONOMOUS_MATERIAL_MANIFEST.sha256
sha256sum -c REPRODUCTION_MATERIAL_MANIFEST.sha256

# Optional refresh, only when the preserved private historical sources exist:
python3 tools/build_reproduction_trace_material.py
python3 tools/build_execution_trace_index.py
python3 tools/build_autonomous_trace_material.py
python3 tools/build_package_completeness.py
python3 verify_repository.py
for t in 1 2 3 4 5 6; do (cd task$t && sha256sum -c MANIFEST.sha256); done
sha256sum -c AUTONOMOUS_MATERIAL_MANIFEST.sha256
sha256sum -c REPRODUCTION_MATERIAL_MANIFEST.sha256
```

The organizer-facing, human-intervention-free execution package starts at
[AUTONOMOUS_TRACE_MATERIAL.md](AUTONOMOUS_TRACE_MATERIAL.md), with the
machine-readable [AUTONOMOUS_TRACE_INDEX.json](AUTONOMOUS_TRACE_INDEX.json) and
[AUTONOMOUS_COSTS.json](AUTONOMOUS_COSTS.json), verified by
[AUTONOMOUS_MATERIAL_MANIFEST.sha256](AUTONOMOUS_MATERIAL_MANIFEST.sha256). It retains startup/organizer
prompts, Agent outputs, worker assignments, tool calls, and tool outputs, but
causally excludes every live human intervention prompt and all later events.

Each directory contains its own README, official prompts/pages, environment
record, solver evidence, solution artifacts, remote records, and summary.
All six tasks maintain task-specific SHA-256 manifests. Task 6 includes the
bounded main trace, two pre-boundary worker traces, exact final v3 notebook,
metadata, submitted CSV and decoded model source, plus compact v1-v3 remote
logs; raw `codex-home` databases, post-intervention traces, intermediate model
artifacts, and competition inputs are excluded. Task-specific
limitations are disclosed in the corresponding README, `COMPLIANCE.md`,
`EXCLUSIONS.md`, or boundary documents.

The published trace overview is [EXECUTION_TRACES.md](EXECUTION_TRACES.md),
with machine-readable [EXECUTION_TRACE_INDEX.json](EXECUTION_TRACE_INDEX.json)
and [EXECUTION_TRACE_INDEX.md](EXECUTION_TRACE_INDEX.md). Token counters,
provider/model attribution, API-cost limitations, and GPU runtime accounting are
in [COSTS.json](COSTS.json). Both trace indexes now use the same
human-intervention-free selection. USD API/GPU amounts are left `null` where no
applicable rate or invoice exists.

For Task 1, the canonical solution selection is the later two-hour rollout
prefix through `task_complete`; the complete raw trace remains under
[REPRODUCTION_TRACE_MATERIAL.md](REPRODUCTION_TRACE_MATERIAL.md). Task 2 uses
its full later trace. Neither contains a live human method/target prompt, and
both scores remain post-deadline and non-ranking. The complete raw formal Task 1
and Task 2 sessions were subsequently located in private local archives after a
school-server restart; their human-influenced suffixes are intentionally not
published, while bounded pre-boundary formal prefixes remain separate
historical audit evidence. These are later fresh reproductions using the same
configured solver/system, official competition bundle, and organizer
constraints, not replacements for the recovered private formal sessions. See
[FORMAL_PREFIX_AUDIT.md](FORMAL_PREFIX_AUDIT.md).
Recovery metadata is in [ORIGINAL_SESSION_RECOVERY.md](ORIGINAL_SESSION_RECOVERY.md).

Task 4's full rule classification and corrected 12-trace solver inventory are
in [task4/RULE_DIFFERENCE_AUDIT.md](task4/RULE_DIFFERENCE_AUDIT.md). Task 6's
exact v3 artifact audit and measured evaluator-batch behavior disclosure are in
[task6/RULE_DIFFERENCE_AUDIT.md](task6/RULE_DIFFERENCE_AUDIT.md).

The complete 496,870,419-byte Kaggle extraction archive is delivered through
the verified Google Drive record in
[`KAGGLE_EXTRACTION_DELIVERY.json`](KAGGLE_EXTRACTION_DELIVERY.json); its
six-competition summary is
[`KAGGLE_EXTRACTION_SUMMARY.json`](KAGGLE_EXTRACTION_SUMMARY.json).
Each task summary also carries an `extraction_summary_binding` (source hash,
competition, deadline, submission totals, captured versions, and kernel count)
and a `submission_version_audit` binding (budget kind/limit, observed count,
duplicate-version count, and literal status). `verify_repository.py`
cross-checks these bindings against the extracted account-result records and
the complete ref/version audit. This is an integrity check between evidence
files, not an organizer compliance decision.

These files are evidence for organizer review, not a self-issued compliance
certificate. The organizer or Jury remains the final authority.

Run the repository verifier from the root:

```bash
python verify_repository.py
```

## Data handling

Task 3 retains the organizer's competition archive and extracted inputs for
authorized reproducibility review. Those files total about 25 MB and are not
owned or licensed for unrestricted redistribution. While they remain in
`task3/input/competition/`, this repository must remain private and access must
be limited to people authorized under the competition rules. See
`task3/DATA_PROVENANCE.md` for exact hashes and public-release instructions.

The other task packages do not duplicate bulk competition datasets or model
checkpoints. Before making any part of this repository public, remove all
restricted competition data, regenerate the affected manifest, and re-run the
repository verifier.
