# Task 6 Compliance and Artifact Note

This is an evidence report, not a self-issued compliance certificate. The
official final result and autonomous trace are aligned. The submitted v3 model
has measured evaluator-batch dependence, which is retained as a technical
property and is not treated here as a competition-compliance issue.

## Result and autonomy

Submission `55357080` (Kernel version 3) scored Public `75.01540` and Private
`73.36234`. It was created and submitted before the first live-human boundary
at `2026-08-08T18:09:48.833Z` and before the official deadline. The selected
main and worker traces contain the exact organizer Starter Prompt and no
Continuation Prompt or live-human method instruction.

The complete account extraction captures 8 notebook versions against the
published limit of 20 and finds no repeated `scriptVersionId` among the six
Task 6 submissions. The per-task binding and source records are in
[`../SUBMISSION_VERSION_AUDIT.json`](../SUBMISSION_VERSION_AUDIT.json) and
`SUMMARY.json`.

## Exact submitted artifacts

The exact v3 notebook source and metadata are under `notebooks/v3/`. The exact
remote `submission.csv` and its decoded `custom_model.py` are under
`remote/v3/`. Mechanical verification establishes:

- two rows with ids `leaderboard-a` and `leaderboard-b`;
- identical model and code payloads in both rows;
- decoded source SHA-256
  `f325541e9ec0df6b4e286528c46070976407a66003912477f05d38134c80822a`;
- decoded source byte identity with `remote/v3/custom_model.py`;
- a loadable safetensors state dict and 13,426 parameters.

Run `python3 tools/verify_v3_artifacts.py` from this directory. Full hashes and
sizes are in `ARTIFACT_PROVENANCE.json` and `MANIFEST.sha256`.

## Operational rules supported by evidence

The final notebook used the notebook-only workflow, Internet-disabled metadata,
only the Task 6 competition source, one T4 through `cuda:0`, the required
`--timeout 600` push, eight captured account versions against the 20-version
limit, and the required three-column/two-row submission envelope. The model is
below the parameter penalty edge, defines `build_model()`, carries weights as a
safetensors state dict, and uses `nn.Dropout` as its stochastic source.

## Evaluator batching: technical disclosure, not a compliance finding

The submitted source computes `torch.cdist(x, x)`, nearest-neighbour density,
a full-batch mean, and lane-conditioned batch means. Therefore a coordinate's
prediction can change when unrelated coordinates in the same evaluator batch
change. The deterministic verification fixture changes the internal component
output for 100/100 fixed points and the final output for 5/100 points, with a
maximum change of 1.0.

The official evaluator deliberately shuffles points and uses irregular batches
to avoid exposing region-block structure. The official starter also forbids
recovering or inferring the protected field or hidden configuration outside the
published API. The formal rule text does not state a general ban on every
permutation-invariant batch statistic, so this audit does not classify the
behavior as a violation or a compliance blocker. The evaluator source digest,
function name, line locators, and observed batching behavior are recorded
without redistributing the competition file in
`evidence/EVALUATOR_BATCHING_PROVENANCE.json`.

## Historical report correction

The immutable submitted report says the entropy branch uses seven differently
scaled dropout bits and lies in `[-1016,1016]`. The exact source instead expands
eight equal-scale units and returns `250 * sum(dropout(z) - z)`, whose support
can reach `[-2000,2000]`. The actual range still lies inside the official
`[-2026,2026]` bound. This is a report-value error; the historical source is
preserved rather than silently rewritten. A corrected ten-section explanatory
supplement is available in
[`SUPPLEMENTARY_TECHNICAL_REPORT.md`](SUPPLEMENTARY_TECHNICAL_REPORT.md); it is
not represented as part of the historical submission.

## Compute accounting limit

The three autonomous Kaggle versions consumed 243.721403533 observed T4
seconds. The final v3 local candidate record reports 31.03 seconds on the local
H100 path, but multiple additional H100 experiments were run and their total
allocation is not exhaustively reconstructable. GPU USD remains unavailable
without a rate or invoice.
