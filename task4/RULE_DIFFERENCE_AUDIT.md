# Task 4 rule-difference audit

The final Kaggle notebook/output is close to the competition's operational hard rules, not a large artifact-format or model/data deviation. The large difference is prompt provenance: the continuation text is substantively non-exact. Separate disclosures cover the transient local __pycache__ and the interpretation of local H100 development under the Hardware clause; the two arXiv searches are retained as method-background provenance and are not treated as a compliance issue.

This is an evidence classification, not a self-issued compliance certificate.
The organizer/Jury decides whether disclosed deviations and interpretation
risks affect recognition.

| Rule area | Status | Evidence-backed conclusion |
|---|---|---|
| `prompt.exact_text` | `disclosed_deviation` | The starter differences are formatting-only in substance, but the continuation is a substantive generic workflow template. The final result is downstream of it; strict exact-prompt conformance is false. |
| `trace.complete_solver_set` | `evidence_supported_compliant_after_correction` | The canonical set now contains the five formal-run traces and seven separate parallel-solver traces that produced versions 2/3 and the comparison evidence used by version 4: 12 traces and 5,881 events. |
| `submission.notebook_only` | `evidence_supported_compliant` | Submission 55316818 names Kernel version 4 output submission.csv; no local-file upload path was used. |
| `submission.folder_two_files` | `disclosed_process_deviation_remote_artifact_unaffected` | A pre-v4 trace listing shows submission/__pycache__/script.cpython-311.pyc in the local folder; the v3 command itself ran py_compile immediately before push. Thus the local folder was not strictly two-file at those moments. Kaggle's remote source record still consists of the declared script/metadata artifact, and the final source hash matches the pulled version 4. |
| `submission.timeout` | `evidence_supported_compliant` | Direct tool-call evidence records --timeout 600 for versions 1, 2, 3, and 4. Version 4 wrote submission.csv at 315.957934901 seconds and the recorded remote runtime is 316 seconds. |
| `submission.version_budget` | `evidence_supported_compliant` | Four versions were created; versions 1, 2, and 4 were submitted once and version 3 was not submitted. |
| `submission.deadline_and_final_selection` | `evidence_supported_compliant` | Submission 55316818 was accepted 251.077 seconds before 06:15:00Z and was the highest-Public eligible result. No manual final-selection action appears in the trace. |
| `resources.remote_metadata` | `evidence_supported_compliant` | Local and pulled remote metadata show Internet disabled, the official wheel dataset and Task 4 competition as the only sources, empty kernel/model sources, and one T4 configuration. The run log confirms Device: cuda:0. |
| `resources.models_and_data` | `evidence_supported_compliant_for_final_notebook` | The final source dynamically locates the competition mount, constructs only ResNet-18 and ViT-Tiny, and loads both local mounted checkpoints. timm's pretrained=True is paired with a local file overlay and custom_load=False; the Internet-disabled remote run completed without a download. |
| `resources.external_web_research` | `informational_method_background_not_a_compliance_issue` | A parallel solver issued two arXiv search queries at 05:55:29.993Z and 05:56:02.175Z. Both occurred after version 3 was pushed, in a separate solver directory, and no evidence shows the results entering the formal version-4 source path. The final notebook itself has no network code or external resource. The searches are retained as method-background provenance and are not treated as a compliance issue. |
| `hardware.local_development` | `jury_interpretation_risk` | The submitted notebook ran on one T4/cuda:0, but local development and validation records explicitly mention one local H100. If the Hardware clause is interpreted as governing only Kaggle submission notebooks, the final run complies; if interpreted as a global development-compute restriction, this is a material deviation. |
| `source.setup_and_report` | `evidence_supported_compliant` | The final source begins with ten numbered report sections. Its setup block hash is 4a9f323d5e28991bd6ba65bb3f7161fe1ad9a637b0aaca343afe77e951bf672c, matching the official starter block captured during the run. |
| `output.contract` | `evidence_supported_compliant` | The recorded remote artifact has 200 rows and the exact header; independent replay recorded 400 finite original-resolution tensors. The exact 190,117,536-byte CSV is represented by SHA-256 but not duplicated in GitHub. |
| `participation.account_team_sharing` | `evidence_partially_unavailable` | All captured Task 4 actions use account researai and autonomous subagents under the same participant. Repository evidence cannot independently prove the absence of every other account, human team relationship, or off-trace private sharing. |

## Practical conclusion

The final remote artifact does not show a large mismatch in notebook workflow,
deadline, version budget, timeout, T4/cuda:0 use, Internet setting, attached
resources, allowed models, setup block, report, runtime, or output contract.

The decisive non-exact item is the Continuation Prompt. It is substantive and
pre-result, so Task 4 must not be presented as an exact-organizer-prompt trace.
The external-search item is preserved as method-background provenance and is not
treated as a compliance issue. The local-H100 accounting/scope question remains
separately disclosed. Full structured evidence locators are in
[`RULE_DIFFERENCE_AUDIT.json`](RULE_DIFFERENCE_AUDIT.json).
