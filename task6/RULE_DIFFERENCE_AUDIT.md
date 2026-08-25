# Task 6 Rule-Difference Audit

The final result is trace-aligned and the submission envelope satisfies the
mechanical contract. The decisive unresolved issue is that the submitted model
uses other evaluator query points as features. This is classified as a serious
Jury-interpretation risk, not as an organizer-confirmed violation.

| Rule area | Status | Evidence-backed conclusion |
|---|---|---|
| `result.trace_alignment` | `evidence_supported_compliant` | Final submission `55357080` and v3 source/output are present before the autonomous boundary. |
| `prompt.exact_text` | `evidence_supported_compliant` | The selected main and worker traces contain exact organizer Starter Prompt text and no continuation. |
| `submission.notebook_only` | `evidence_supported_compliant` | The final result names Kernel version 3 and the exact remote output is preserved. |
| `submission.deadline` | `evidence_supported_compliant` | v3 was accepted 449.92 seconds before the official deadline. |
| `submission.version_budget` | `evidence_supported_compliant` | The extraction captured eight versions, below the limit of 20. |
| `submission.timeout` | `evidence_supported_compliant` | Trace evidence records `--timeout 600`; v3 completed in about 75.09 remote seconds. |
| `resources.remote_metadata` | `evidence_supported_compliant` | Exact metadata has Internet disabled, one T4, only the competition source, and no attached datasets/models/kernels. |
| `model.envelope_and_parameters` | `evidence_supported_compliant` | Two identical payload rows decode to a loadable 13,426-parameter model source/state dict pair. |
| `model.dropout_randomness` | `evidence_supported_compliant` | Training-mode stochasticity comes from `nn.Dropout`; the eight-unit equal-scale output remains within `[-2000,2000]`. |
| `model.evaluator_batch_dependence` | `serious_jury_interpretation_risk` | `torch.cdist(x,x)`, global mean and lane means make outputs depend on unrelated evaluator query points. The deterministic test changes final predictions for 5/100 fixed coordinates. |
| `protected_field.hidden_geometry` | `serious_jury_interpretation_risk` | The evaluator explicitly randomizes batches to avoid exposing region-block structure, while the solution intentionally uses batch density/context to infer geometry. Whether this crosses the protected-field rule requires a Jury ruling. |
| `source.technical_report` | `disclosed_factual_error` | The immutable report describes seven differently scaled dropout bits and `[-1016,1016]`; code implements eight equal-scale bits and can reach `[-2000,2000]`. |
| `resources.external_web_research` | `evidence_supported_no_search_found` | No external webpage search was found in the selected autonomous Task 6 traces. |
| `hardware.local_development` | `jury_interpretation_risk_and_accounting_incomplete` | Final Kaggle execution used one T4, while local work used H100 hardware and exhaustive local GPU seconds are unavailable. |
| `cost.total_usd` | `unavailable_not_complete_numeric_total` | Token and observed T4 runtime are known; API/GPU USD and exhaustive local GPU runtime are unavailable. |

Run `python3 tools/verify_v3_artifacts.py` to verify hashes, envelope, decoded
source identity, parameter count, batch dependence, and the preserved report
discrepancy. The organizer evaluator source is not redistributed; its exact
digest, `_predict_model_random_batches` locator, and call-site facts are in
`evidence/EVALUATOR_BATCHING_PROVENANCE.json`.
