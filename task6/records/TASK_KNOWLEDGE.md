# Task Knowledge

## Task Map

This is procedural supervised 2D function approximation with a stochastic
sub-objective. The prediction unit is one coordinate `(x,y)`. Machine learning
is useful for the unknown geometric masks and O spiral; explicit output routing
is useful because deterministic and stochastic regions are evaluated in
different module modes.

Subproblems:

| Question | Score upside | Evidence / cheapest test | Cost / dependency | Owner |
|---|---:|---|---|---|
| Can mode routing isolate entropy variability? | 20 | zero accuracy head plus bounded dropout probe | seconds; evaluator contract | forensics |
| Can a compact net learn I/O/A/bg on the public field? | up to 80 | fresh-seed evaluator cells | minutes; published samples | primary |
| Which representation preserves sharp masks and O oscillation? | 10-30 | matched SIREN vs ReLU/RBF screen | minutes; same data | mechanisms |
| Does config randomization help unseen geometry? | hidden transfer | held-out scale/rotation configurations | minutes; valid config construction | primary |

## Task Understanding And Validation

`evaluate_model` samples 512 points from each of `I`, `O`, `A`, `I_entropy`,
and background. Accuracy predictions use `model.eval()`; entropy predictions
use `model.train()` for 10 dropout-enabled passes. Batches are shuffled and
irregular, so solutions must be pointwise and cannot depend on batch position.
The output contract is a rebuilt architecture plus safetensors weights, not
predictions or a pickled module.

## Mechanism Brief

Letter location is the sufficient coordinate information. The binding limits
are sharp mask boundaries, the 20,259 safe parameter maximum, the extreme first-I
dynamic range, and hidden geometry shift. The intended stochastic source is
dropout. A mode-specific forward path can separate the entropy objective from
accuracy without using region order or hidden state. The cheapest falsifier is
the official evaluator: a bounded eight-unit dropout branch should score near
one for entropy while leaving eval-mode outputs unchanged.

## Hard Constraints

- Competition data and published field API only; no external data/pretraining.
- Do not inspect or reverse engineer the protected runtime or hidden config.
- Model must be `torch.nn.Module`; persistent tensors must be parameters.
- Keep parameters below 20,260; use dropout as the only inference randomness.
- Notebook-only submission, Internet off, one GPU at `cuda:0`, 600 seconds.
- At most 20 pushes; use official `write_submission` and CLI flow.

## Validation Protocol And Subgroups

`matched_sanity`: exact public config with official seed, used for interface and
upper-bound checks only. `development_proxy`: fresh evaluator seeds on the public
config and several independently constructed plausible scale/rotation variants.
`confirmation_proxy`: untouched config variants/seeds chosen after route
implementation. Report mean, worst configuration, and each region. Public LB is
one hidden configuration; private LB averages several.

## Runtime And Deployment Evidence

Local host: 128 CPUs, ~1.8 TiB available RAM, and two H100 80GB devices. Remote
candidate must train on CPU or one T4 within 600 seconds. Official starter ran in
29.5 seconds locally, scored 36.825, verified its envelope, and failed only when
trying to create the Kaggle-only `/kaggle/working` path.

## Evidence And Unknowns

Public dense grid areas: I 1.46%, O 7.89%, A 2.52%, entropy-I 2.34%, background
85.78%; evaluator balancing makes region-aware sampling essential. Zero output
scores about 47.4% I, 68.5% O, 0% A, 100% background. A bounded eight-unit
dropout branch with zero deterministic output scores 100% entropy and about
63.19 total. Unknown: distribution/range of hidden rotations and scales.

## Validation-LB Lessons

Version 1 public score was 47.15536 while matched local score was 86.0722. The
sign and magnitude agree with the published-API seed-shift proxy (roughly
50-56), so the hidden boundary is materially different geometry rather than a
remote preprocessing mismatch. Public-fit first-I and A gates do not transfer;
seed-randomized training is now the active replacement hypothesis.

Version 2 seed-randomized public score was 70.95502 versus a 69.7828 held-seed
proxy, matching within 1.17 points and preserving the proxy ordering. Version
3 added within-batch density and lane context, scored 73.0339 on held
confirmation (worst 69.8745), and reached 75.01540 publicly. This transfer
supports density as a useful but evaluator-batch-dependent signal. Pointwise
pooling appears near its information ceiling because O phase and first-I
amplitude are not identifiable from one coordinate; set-conditioned inference
remains a mechanism-distinct research route, but its fresh diagnostic scored
only 71.018 and is below the incumbent.
