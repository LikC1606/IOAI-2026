# Task 6 post-run supplementary technical report

This is a post-run explanatory supplement for organizer review. It corrects
factual details in the immutable v3 source header; it is not the historical
report that Kaggle received and must not be substituted for
`notebooks/v3/script.py`.

## 1. Summary

The submitted solution trains a compact routed sine network on balanced samples
from eight public-API seed configurations, then serializes its model and code
through the required two-row envelope. The exact v3 submission scored Public
`75.01540` and Private `73.36234`.

## 2. Architecture

The decoded model is a `3 -> 48 -> 48 -> 72 -> 6` network. Its inputs are
`x`, `y`, and a four-neighbor batch-density feature; global and four-lane
contexts are concatenated before the final sine layer. It has four region
logits, an O-value head, an I-value head, four fixed scalar thresholds, and
exactly 13,426 parameters, below the 20,260-parameter penalty edge.

## 3. Accuracy regions

Training is balanced over I, O, A, and background samples from eight seed
configurations. The I target is normalized by the supplied `i_grad_max` before
the sigmoid head and rescaled at inference. O uses a tanh head, A routes to
exact `-1`, and low-confidence predictions fall back to zero.

## 4. I-entropy

Training-mode inference returns eight equal-scale centered `Dropout(0.5)` units,
not seven differently scaled units. Each unit contributes `250 * (dropout(1) -
1)`, so the total support is `[-2000, 2000]`; this keeps all ten evaluator runs
inside the official `[-2026, 2026]` range while producing nonzero variability.

## 5. Background

The classifier has a dedicated background route whose deterministic output is
exactly zero. The final v3 thresholds are `i=1.1`, `o=0.999`, and `a=0.9`;
the intentionally conservative I threshold avoids catastrophic large-value
false positives on background points.

## 6. Training

For each of eight configurations, the script samples 4,096 points for each of
I, O, A, I-entropy, and background. Adam uses learning rate `1e-3` for 3,000
mixed-batch steps, with cross-entropy for routing and SmoothL1 losses for the I
and O heads. The selected local candidate path took about 31.03 seconds on an
H100; the submitted notebook uses only `cuda:0` in Kaggle's
`NvidiaTeslaT4` environment.

## 7. Hidden-configuration generalisation

The model trains on `secret_seed` values 0–7 and is checked on held values 8–15.
It derives its scale from the supplied configuration rather than hard-coding
the public field. Density and lane-context features were chosen because the
hidden evaluator shuffles points and changes the field geometry; they are
computed from the current evaluator batch and are documented as a technical
behavior below.

## 8. Results

The exact v3 public-config proxy reported I=`0.447459`, O=`0.690749`, A=`0.726562`,
I-entropy=`1.000000`, and background=`0.765625`, for a weighted total of
`72.6079`. Held seeds 8–15 averaged I=`0.462457`, O=`0.689510`, A=`0.777832`,
I-entropy=`1.000000`, background=`0.733887`, total=`73.2737`; the later Public
Leaderboard result was `75.01540`.

## 9. Alternatives

The official starter scored 36.8251 locally, a routed zero-accuracy baseline
scored 63.1931, and a public-only sine route scored 47.15536 remotely. Broad
72-configuration pooling scored 69.7038 on held variants; multi-scale density
and set-context diagnostics were retained as experiments but were not more
robust than the selected lane-density v3 route.

## 10. Limitations and runtime

The model is not pointwise: changing unrelated coordinates in a deterministic
fixture changed internal components for 100/100 points and final predictions
for 5/100. This measured evaluator-batch dependence is disclosed for
reproducibility. The remote v3 run completed in 75.092 seconds end-to-end,
Internet was disabled, and no external data or model was attached; exhaustive
local H100 development time and USD cost remain unavailable.
