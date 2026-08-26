# Cross-task rule-compliance audit

This audit answers a different question from whether the repository contains a
well-formed trace package. A selected observable trace can be complete within
its stated boundary while the corresponding competition result still fails an
exact-prompt rule or is not trace-bound.

## Bottom line

The current evidence does **not** support a claim that all six tasks satisfy
every organizer verification rule. Task 1/2 provenance, Task 4 prompt text,
and the literal submission/version conflicts documented for Tasks 1–3 remain
different from an all-green official-final claim. Method research and the Task
6 evaluator batching behavior are retained as factual disclosures, but are
**not treated as compliance problems** in this audit.

The classifications used here are:

- **Known deviation**: repository evidence directly conflicts with a stated
  requirement or with the scope needed for the requested claim.
- **Informational disclosure**: a technically relevant fact is retained for
  reproducibility but is not classified as a rule problem.
- **Jury-interpretation risk**: the facts are established but the published
  wording does not resolve how the organizer/Jury applies a remaining prompt,
  hardware, or provenance rule.
- **Evidence unavailable**: a historical fact cannot be reconstructed from the
  retained records and is not replaced with a post-run assertion.

## Six-task matrix

| Task | Official final bound to selected trace? | Exact organizer prompt? | Evidence-backed assessment |
|---|:---:|:---:|---|
| 1 | **No** | **No for the canonical reproduction** | **Strict claim not supported.** The complete raw formal session was recovered privately after a school-server restart, but its human-influenced suffix is withheld; a bounded exact-prompt formal prefix is preserved as supplemental evidence. The selected two-hour run is a later post-deadline reproduction with a custom starter and a different submission. The official final refs are therefore not trace-bound. The extraction also records 38 captured notebook versions against the literal 20-version wording, and `scriptVersionId=340342513` was submitted twice as the two official-final refs; these are disclosed in `SUBMISSION_VERSION_AUDIT.json`. The official-final version reuse is a separate pre-deadline literal conflict; any post-deadline exception scope is for the organizer. |
| 2 | **No** | **No for the canonical reproduction** | **Strict claim not supported for the official final.** The complete raw formal session was recovered privately after a school-server restart, but its modified-continuation suffix is withheld; a bounded exact-prompt formal prefix and eligible v2 artifact chain are preserved as supplemental evidence. The official final is downstream of the formal supervision boundary; the selected two-hour run is a different post-deadline reproduction with a custom starter. The account has 18 captured versions within the 20-version count, but `scriptVersionId=340290308` was submitted twice as refs `55260462` and `55260695`, including the eligible v2 result. The BabyAI/FiLM/MiniGrid/noisy-demonstration material was method background only. |
| 3 | **Yes** | **Yes** | The result and exact prompt are supported. The account extraction has 27 submissions in total, of which 11 were sent before and 16 after the official deadline. Under the timeline clause's deadline-scoped reading, the 11 pre-deadline submissions are within the published limit of 15; under an account-wide reading, 27 exceeds it. Separately, `scriptVersionId=340521169` was submitted twice as refs `55290807` and `55290810` immediately before the deadline. Historical report length and score statements also deviate. The full ref/version evidence and both count interpretations are in `SUBMISSION_VERSION_AUDIT.json`; the organizer decides the applicable scope. |
| 4 | **Yes** | **No** | **Known exact-prompt deviation.** The final is downstream of a substantive generic continuation template. The corrected package contains all 12 selected solver traces. The two arXiv searches are retained for provenance and are not treated as a method-research violation; the transient local `__pycache__` and local H100 accounting remain separately disclosed. |
| 5 | **Yes** | **Yes** | The final and exact prompt are supported. The sentence-level detection/stylometry literature is retained as method background and is not treated as a compliance problem. The exact v6 output/log are retained; its source is the trace-preserved copy because Kaggle now rejects the historical source pull. |
| 6 | **Yes** | **Yes** | The exact v3 notebook, metadata, submitted CSV, decoded source, weights envelope, and trace are present. The model's evaluator-batch dependence is a measured technical property: changing unrelated batch points changes 5/100 final predictions in the deterministic fixture. The non-redistributed official evaluator's batching behavior is bound by file hash and function/call-site locators. This is **not treated as a compliance blocker or violation**; the historical report's dropout construction and range error remain disclosed. |

## Trace and artifact scope

The selected JSONL files retain observable startup/organizer prompts, inherited
context, Agent outputs, worker assignments, tool calls, and tool outputs within
their declared causal boundaries. Credentials and private endpoints are
redacted; hidden or encrypted chain-of-thought is not published. Those limits
are provenance limits, not missing observable tool envelopes.

Tasks 1 and 2 are special cases: their complete raw formal sessions were
recovered in private local archives, while bounded pre-boundary formal prefixes
remain as supplemental historical evidence and the human-influenced suffixes
are intentionally withheld. Their selected traces are later fresh two-hour
reproductions using the same configured solver/system, official competition
bundle, and organizer constraints. They demonstrate no-live-human
reproduction, but cannot prove the provenance of the earlier official final
results; the later reproductions do not use the exact organizer Starter text.
See `FORMAL_PREFIX_AUDIT.md/json` and `ORIGINAL_SESSION_RECOVERY.md/json` for
the separate formal-prefix and recovery scopes.

Tasks 3–6 have official-final/selected-trace alignment. That alignment does not
erase the task-specific prompt, report, budget, hardware, or provenance limits
listed above. Method research and evaluator batching are retained as
informational facts, not compliance blockers.

## Cost completeness

Per-task token counters, provider/model attribution, and selected Kaggle remote
runtime are recorded. API USD is unavailable because no applicable
`ioai_allowed` / `gpt-5.6-sol` rate card or invoice was captured. GPU USD is
also unavailable. Tasks 4–6 used local H100 development; selected observations
are recorded where available, but exhaustive non-overlapping local GPU runtime
cannot be reconstructed. Cost accounting is therefore complete for tokens and
the stated selected remote scope, not a complete numeric USD or all-local-GPU
total.

## Evidence entry points

- Exact prompt comparison: `PROMPT_CONFORMANCE_AUDIT.md/json`
- Selected trace inventory: `AUTONOMOUS_TRACE_MATERIAL.md` and
  `AUTONOMOUS_TRACE_INDEX.json`
- Official-result reconciliation: `FINAL_SUBMISSION_RESULTS.md`
- Task-specific facts: `task1/COMPLIANCE.md` through `task6/COMPLIANCE.md`
- Detailed method audits: `task4/RULE_DIFFERENCE_AUDIT.md/json` and
  `task6/RULE_DIFFERENCE_AUDIT.md/json`
- Task 6 evaluator batching provenance:
  `task6/evidence/EVALUATOR_BATCHING_PROVENANCE.json`
- Submission/version budget and one-version-one-submission audit:
  `SUBMISSION_VERSION_AUDIT.md` and `SUBMISSION_VERSION_AUDIT.json`
- Costs: `AUTONOMOUS_COSTS.json` and `COSTS.json`

`RULE_COMPLIANCE_AUDIT.json` is the machine-readable version. The organizer or
Jury remains the final authority on the remaining provenance and prompt issues.
