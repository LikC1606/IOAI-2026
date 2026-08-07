# Task Knowledge

## Objective And Task Map

Solve `ioai-2026-task-5-westlake-nlp-24` by producing a rule-legal Kaggle notebook that predicts the single human-to-machine character boundary for all 760 test passages, submits it through the exact notebook CLI flow before 2026-08-07T09:04:20.519Z, and continues leaderboard-driven improvement while preserving a deployable incumbent. The user specifically requires local dev self-scoring, the unchanged offline setup block, local-only bge loading, one `cuda:0` GPU at most, 600-second pushes, and a technical report.

Classification: supervised structured prediction/change-point detection over one document sequence. ML is likely useful because the boundary is defined by a latent author/style transition, but ML is not inherently required: candidate-boundary constraints and deterministic stylistic discontinuities may carry signal.

Prediction unit: one passage. Target: exact character offset where the human prefix ends and machine suffix starts. Labels use Python slicing semantics: `text[:t]` is human and `text[t:].lstrip()` is machine. There is exactly one switch; each side is at least 180 words.

## Mechanism Brief

The likely generator chooses a human excerpt/prefix and asks an LLM to continue it. Sufficient evidence should combine (1) legal candidate cut points, likely sentence/paragraph starts; (2) local distributional/style change around a cut; (3) whether the full prefix looks more human and full suffix more machine; and (4) the empirical boundary-position prior. Dominant loss is assigning the correct transition neighborhood because the metric scale is only 100 characters. Removable headroom over the global fraction baseline should come from passage-specific evidence. Cheapest falsification: measure whether true boundaries are concentrated at structural offsets and whether supervised local/sequence features rank their neighborhoods on untouched dev.

## Task Decomposition Gate

| Subproblem | Question / expected contribution | Evidence boundary and cheapest falsification | Cost / dependencies | Owner |
|---|---|---|---|---|
| Candidate generation | Which character offsets can be true boundaries, and can structure alone shrink the search space? High impact because 100-char metric scale. | Train structural hit rate and distance; confirm unchanged on dev. | Seconds, CPU; no model dependency. | `classical_forensics` |
| Local style seam | Which local lexical, punctuation, rhythm, or bge embedding changes distinguish the switch? Expected to rank nearby candidates. | Train-only fit, untouched dev score/error quantiles and hard cases. | Minutes CPU or one local GPU; depends on candidates. | `classical_forensics`, `bge_changepoint` |
| Sequence aggregation | Does enforcing one human prefix plus machine suffix beat independent local seam scoring? Potentially largest robustness gain. | Document-held-out dev likelihood/score versus local and prior baselines. | Minutes CPU/GPU; depends on per-segment features. | `sequence_route` |
| Deployment/output | Can the exact method reproduce under offline T4, one device, setup, 600s, source/output rules? Required for any incumbent. | Local unchanged-body check, conservative scale estimate, then one meaningful Kernel run. | Up to 600s remote; depends on selected candidate. | primary |

## Hidden-Boundary Model

Officially train, dev, Public, and Private consist of disjoint ids drawn from the same distribution; test membership is hidden and no row-level feedback is available at inference. Plausible remaining shifts are random corpus/generator mixture imbalance and passage-length/boundary-position variation, not entity or time leakage. Evidence distinguishing them: train-vs-dev structural/style slice stability, confirmation on separate dev partitions, and paired full-dev/Public scores. Do not treat matched train fit or the known official baseline score as candidate-ranking evidence.

## Validation Matrix

- `development_proxy`: fixed dev halves by deterministic id hash, used for route construction and slice analysis.
- `confirmation_proxy`: the other dev half and full untouched dev only when implementation-complete; report mean metric, half-to-half dispersion, worst half, median/P75/P90 absolute error, and length/boundary-fraction slices.
- Stress cell: dev rows in extreme passage-length and boundary-fraction quartiles.
- `public_lb`: separate 380-row evidence after a legal completed notebook submission.
- `hidden_lb`: final 380 rows, unavailable before deadline.

Dev represents the stated test distribution but repeated dev reuse can overfit route selection. Public score can test broad transfer but cannot identify test rows or justify tuning repeated minor variants.

## Hard Constraints And Output Contract

Metric: `100 * mean(exp(-abs(p-t)/100))`, higher is better. Output path `/kaggle/working/submission.csv`, header `id,boundary_char_index`, exactly 760 test ids, integer predictions within passage bounds. Notebook-only exact CLI flow; unchanged setup block first; wheel dataset plus competition source; internet false; only local `bge-base-en-v1.5`; 15 pushes total; 600 seconds per push; CPU or one T4 via `cuda:0`; source <=1 MB.

## Runtime And Deployment Evidence

Local host: 128 CPUs, about 1.5 TiB available RAM, two H100 80GB devices visible through PyTorch. Local allocation: primary uses CPU for baseline/integration; bge lane uses logical GPU 0 only; sequence/classical lanes use CPU unless their method benefits from the other local GPU. Remote feasibility is judged independently against one T4 and 600 seconds including roughly 40 seconds of setup.

## Evidence And Unknowns

Resolved structural mechanism: every one of 1,221 train and 380 dev targets is exactly a punctuation-plus-space sentence start; the classical candidate set averages 24.2 offsets per document. Train/dev/test passage lengths align, train/dev boundary fractions are 0.5952/0.5962, and no full-text cross-split duplicates exist. Machine continuations have strong reusable lexical/style markers, while uncommon continuation starter words are the weakest dev slice.

Frozen bge sequence emissions confirm that authorship information exists beyond the position prior (86.82 dev; grouped-CV worst 85.31), but competition-trained word/character representations are stronger. The one-transition lexical sequence route scores 93.76 dev with three held-out train folds 93.02/94.37/92.67. The current leading local-transition plus onset classifier scores 94.62 dev and 92.87 on a late-id 20% train confirmation block.

## Validation-LB Lessons

Remote version 1 reproduced the matched baseline: 28.57 dev, 63.5-second CPU notebook, 28.60 Public. Version 2 classical change-point scored 94.615 dev and 90.86 Public. The improvement sign/rank transfers (+62.26 Public over baseline), but the -3.755 absolute gap shows that full dev is optimistic for the error tail or selected route. Exact Kaggle/local predictions and dev parity rule out output/preprocessing mismatch.

Classical route reflection: versus baseline, full-dev delta is +66.05 points, exact boundaries rise from 0.3% to 92.9%, and MAE falls from 201.84 to 15.82 characters. A frozen five-fold audit gives 91.451 mean, 89.073 worst and 1.379 SD; contiguous-ID folds give 91.499 mean/91.202 worst. Source-clustered folds give 91.515 and no exact prefix/suffix duplicates exist, so source leakage does not explain dev. Public 90.86 is consistent with the OOF range and shows dev was an easier/optimistic cell.

Updated candidate decision: cumulative sequence likelihood has lower full dev (93.758 local / 93.563 remote) but stronger held-out evidence (93.02/94.37/92.67) and better OOF tail than the local-transition incumbent. It scores 92.48 Public, +1.62 over the dev-leading local model, and its Public calibration gap is only -1.083. Thus train passage OOF, not the reused full-dev aggregate, is the valid primary selector. Train-only caps and confidence fusion were explicitly falsified on confirmation. Direct pair-seam and frozen-bge screens also failed to beat the cumulative sequence route.

The standard data-coverage refit of the unchanged selected mechanism on all 1,601 official labeled train+dev passages scores 92.73 Public, +0.25 over train-only version 3. This uses only competition data and does not use Public row identities or feedback. The all-label fit's 100 in-sample dev score remains only a pipeline check.

A representation-level route cleared the gate: one fixed one-epoch full fine-tune of the permitted local BGE encoder scored 94.557 on a 195-passage train hash holdout versus 94.324 for the paired lexical sequence baseline. Version 5 produced 95.688 remote dev and 94.56 Public (+1.83 over sparse v4) in 244.4 seconds on one T4/cuda:0 at 5.00GB. A second predeclared seed gave 94.463 on the same holdout, confirming stability while warning that dev tails vary.

The all-label neural refit keeps the complete v5 mechanism fixed, fits 43,590 sentences from 1,601 official labeled passages, and changed only 9/760 remote neural decisions. Version 6 completed in 289.3 seconds, passed every output/device/setup gate, and scored 95.39 Public, +0.83 over v5. Its 97.384 in-sample dev remains matched-sanity only; the Public gain supports variance reduction from extra official labels but cannot reveal which changed rows were beneficial. Version 6 is the deployable incumbent and v5 remains the fallback.

A final local-transition decoder improved the fixed holdout 94.557 to 96.041 and untouched dev 95.160 to 96.246, but version 7 scored only 94.17 Public, -1.22 versus v6. Thus adjacent-sentence neural jumps do not transfer despite local tail gains; the hidden evaluator rewards the more robust cumulative suffix-state evidence. This paired contradiction invalidates the transition proxy for hidden selection. Automatic Public-score selection preserves version 6 as the final incumbent.
