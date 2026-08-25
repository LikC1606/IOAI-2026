# Cross-task rule-compliance audit

This audit answers a different question from whether the repository contains a
well-formed trace package. A selected observable trace can be complete within
its stated boundary while the corresponding competition result still fails an
exact-prompt rule, is not trace-bound, or carries another disclosed rule risk.

## Bottom line

The current evidence does **not** support a claim that all six tasks satisfy
every organizer verification rule. The repository is suitable for transparent
Jury review because the recoverable evidence is published and the remaining
problems are classified, but Jury recognition is not self-certified.

The classifications used here are:

- **Known deviation**: repository evidence directly conflicts with a stated
  requirement or with the scope needed for the requested claim.
- **Jury-interpretation risk**: the facts are established, but the published
  wording does not resolve how the Jury applies the rule.
- **Evidence unavailable**: a historical fact cannot be reconstructed from the
  retained records and is not replaced with a post-run assertion.

## Six-task matrix

| Task | Official final bound to selected trace? | Exact organizer prompt? | Evidence-backed assessment |
|---|:---:|:---:|---|
| 1 | **No** | **No** | **Strict claim not supported.** The original run record was lost after a school-server restart. The selected two-hour run is a later post-deadline reproduction with a custom starter and a different submission. The official final refs are therefore not trace-bound. External-method research and 38 captured notebook versions versus the published limit of 20 are separately disclosed risks. |
| 2 | **No** | **No** | **Strict claim not supported.** The official final is downstream of the formal supervision boundary; the selected two-hour run is a different post-deadline reproduction with a custom starter. Its potentially causal BabyAI/FiLM/MiniGrid/noisy-demonstration research is a Jury-interpretation risk. The captured version count is 18/20. |
| 3 | **Yes** | **Yes** | The result and exact prompt are supported, but this is **not a clean self-certification**. Potentially causal research on noisy GBS, Bayesian active learning, dueling bandits, and entropy pursuit is disclosed. The account has 27 scored submissions against a published limit of 15: 11 before and 16 after the official deadline. Historical report length and score statements also deviate. |
| 4 | **Yes** | **No** | **Known exact-prompt deviation.** The final is downstream of a substantive generic continuation template. The corrected package contains all 12 selected solver traces. A transient local `__pycache__`, two apparently noncausal arXiv searches, and local H100 development under a one-T4 notebook rule remain disclosed process/interpretation risks. |
| 5 | **Yes** | **Yes** | The final and exact prompt are supported. External literature was explicitly used to justify the selected sequence/context route, so the broad external-information rule remains a **Jury-interpretation risk**. The exact v6 output/log are retained; its source is the trace-preserved copy because Kaggle now rejects the historical source pull. |
| 6 | **Yes** | **Yes** | The exact v3 notebook, metadata, submitted CSV, decoded source, weights envelope, and trace are present. The model is evaluator-batch-dependent: changing unrelated batch points changes 5/100 final predictions in the deterministic fixture. The non-redistributed official evaluator's batching behavior is bound by file hash and function/call-site locators. This is a **serious Jury-interpretation risk**, not an asserted Jury ruling. The historical report also misdescribes the dropout construction and range. |

## Trace and artifact scope

The selected JSONL files retain observable startup/organizer prompts, inherited
context, Agent outputs, worker assignments, tool calls, and tool outputs within
their declared causal boundaries. Credentials and private endpoints are
redacted; hidden or encrypted chain-of-thought is not published. Those limits
are provenance limits, not missing observable tool envelopes.

Tasks 1 and 2 are special cases: their original run records are unavailable.
Their selected traces are later fresh two-hour reproductions using the same
configured solver/system, official competition bundle, and organizer
constraints. They demonstrate a no-live-human reproduction, but cannot prove
the provenance of the earlier official final results and do not use the exact
organizer starter text.

Tasks 3–6 have official-final/selected-trace alignment. That alignment does not
erase the task-specific prompt, external-information, report, budget, hardware,
or method risks listed above.

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
- Costs: `AUTONOMOUS_COSTS.json` and `COSTS.json`

`RULE_COMPLIANCE_AUDIT.json` is the machine-readable version. The organizer or
Jury remains the final authority on every interpretation-risk item.
