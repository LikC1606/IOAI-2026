# Task Knowledge

## Task Map

This is an algorithmic/optimization task, not a conventional learned-predictor
problem. The decision unit is one raw RGB image. For each of 100 images in each
unlabeled leaderboard split, the solution emits two raw-resolution tensors:
Type A must leave Model R correct and make Model V wrong; Type B must leave V
correct and make R wrong. The evaluator applies the submitted tensor before
`Resize(256) -> CenterCrop(224) -> Normalize` and recomputes both predictions.
The clean class is not supplied for leaderboard images, but both frozen models
are specified to be correct and agree, so their clean consensus is the legal
inference-time label proxy.

## Task Understanding And Validation

The official score is directional: `S_pure=(Score_A+Score_B)/(2*100)` and the
reported score is `100*S_pure*PF`, where
`PF=1.5-sigmoid(50000*mean(||delta||_2/N))`. Smaller perturbations therefore
trade against binary success. A row is valid only when its base64/zlib payload
decodes to contiguous little-endian float32 with shape `3 x H x W`; IDs must be
`a_0..a_99,b_0..b_99` in that order.

Remote evidence resolved an implementation detail not explicit in the prose:
the evaluator averages the *sum* of the two normalized tensor norms per image.
For version 1, the public mean was `1.41910146e-6`, whose penalty-only score is
exactly 98.23. Thus its public result supports 200/200 successes and a factor-two
norm aggregation versus the earlier local estimate; it does not support attack
failures or label shift.

The hidden-boundary model is that leaderboard images are drawn from the same
ImageNet-style source and are evaluated by the exact supplied checkpoints and
transform, while labels remain hidden. Potential shifts are image aspect ratio,
resolution/interpolation sensitivity, and class/visual-margin mix; there is no
feedback during inference. Development validation uses the labeled `train` and
`test_public` splits with untouched confirmation subsets, and a separate
unlabeled self-consistency check uses clean R/V consensus on leaderboard images.
Those checks establish attack transfer/interface parity, not an independent
estimate of private labels; a remote LB result is kept separate.

## Mechanism Brief

The target mechanism is local decision-boundary geometry of two frozen,
architecturally different ImageNet classifiers. A differentiable raw-to-224
resize/crop lets gradients find a small image perturbation. Type A changes the
ViT margin while adding a hinge barrier for the ResNet true-vs-best-competitor
margin; Type B swaps those roles. The main bottleneck is finding a boundary
crossing at low mean L2 per pixel without crossing the protected model. A cheap
falsification test is a short untargeted projected-gradient run on each labeled
image followed by exact prediction checks. If gradients do not produce a
stable type-specific flip, try a targeted or boundary-search objective rather
than tuning the same step size.

## Current Decomposition

- **Attack feasibility:** cross only the attacked boundary while protecting the
  other model. It contributes the binary success term; exact argmax replay is
  the cheapest falsification test. The dual-margin PGD route is supported.
- **Minimum-norm geometry:** reduce each feasible delta without losing either
  inequality. It controls all remaining public headroom; paired norm/success
  replay is the cheapest test. Linearized shrink/projection is active.
- **Representation and parity:** encode original-resolution float32 tensors with
  enough precision for the evaluator. Fine power-of-two quantization improved
  public LB from 98.23 to 98.36; malformed-shape and decode checks remain gates.
- **Hidden boundary:** private labels and image mix are held out. Clean consensus
  and private-image model replay are only development proxies; private LB stays
  separate until released.

## Hard Constraints

- Only the competition data and the provided `resnet18` and
  `vit_tiny_patch16_224` checkpoints may be used.
- Notebook-only submissions; notebook Internet disabled; offline wheel setup
  must run before package imports.
- One GPU maximum (`cuda:0`), Kaggle machine shape `NvidiaTeslaT4`, and every
  pushed kernel capped with `--timeout 600`; at most 20 versions.
- Perturbations stay at each image's original `3 x H x W` resolution and are
  clipped after addition. Output is `/kaggle/working/submission.csv` with 200
  ordered rows and exact header/encoding.

## Validation Protocol And Subgroups

The first development cell is `train`; confirmation is `test_public`. For each
cell, report Type A/Type B success, mean and lower-quantile norm, penalty factor,
and protected-model failures, with per-resolution/aspect-ratio slices where
sample size permits. A candidate is selection-ready only when the same attack
mechanism works on both cells and the local submission adapter decodes exactly.
Leaderboard self-checks are marked `development_proxy` only for model behavior;
they cannot prove hidden labels or private-LB transfer.

## Runtime And Deployment Evidence

The final notebook must include the starter's verbatim setup/path discovery and
load checkpoints from the mounted competition data. Runtime is dominated by
per-image gradient optimization over 200 images; the submitted candidate must
finish comfortably below 600 seconds on one T4. Before each push, run the same
script locally, verify all 200 IDs/shapes/finite float32 payloads, and estimate
full-scale memory/runtime. Preserve the strongest verified implementation as
the deployable incumbent.

Version 1 completed remotely in about 213 seconds. Version 2 used finer
power-of-two quantization and scored 98.36 publicly. Version 4 adds eight
shrink/projection steps after PGD; its T4 notebook completed in 316 seconds and
its remote artifact passed independent 400/400 replay. The exact corrected
public proxy was 98.4084 and the observed public LB is 98.41.

## Evidence And Unknowns

Known: clean R/V predictions agree and match labels on all 200 labeled images;
raw resolutions vary widely; labels for leaderboard images are private.
Unknowns: exact private image-generation shift and whether all hidden clean
predictions are correct as promised. The evaluator's norm aggregation is now
calibrated from public LB. Private-image consensus remains a proxy and is not
combined numerically with public or private leaderboard evidence.

## Validation-LB Lessons

Version 1 scored 98.23 public versus an incorrectly calibrated local 99.11. An
audit of target, ordering, decoding, model replay, and exact norms showed the LB
equals the penalty from summing both per-image norm terms, with no missing
successes needed. Version 2's finer quantization scored 98.36. Version 4's
minimum-norm refinement then predicted 98.4084 and scored 98.41, establishing
exact public proxy/LB calibration and a +0.05 gain. Private LB is still blank.
The next falsifiable action is to compare the private result with the locked
98.3194 remote-artifact proxy; no post-deadline tuning is eligible. Immediately
after the deadline, the submissions API reports version 4 complete at 98.41 but
the active team-submission endpoint still lists version 2 at 98.36. This is kept
as finalization-state evidence rather than treated as a modeling result.
