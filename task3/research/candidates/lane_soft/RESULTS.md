# Soft Belief Lane Result

## Finding

The hypothesis is supported on the available proxies. Replacing irreversible
half-space masks with a bounded logistic likelihood, retaining a posterior over
all untried words, and using posterior-predictive comparison entropy improves
both exact-public search and robustness to controlled public/private order
inversions.

The frozen defaults in `soft_belief.py` are `tau=0.01`, random-verdict mixture
`0.10`, comparison tempering `1.0`, champion weight `2.0`, information weight
`2.0`, information-posterior temperature `1.5`, and a 64-word posterior
shortlist.

## Evidence

Exact public, all 120 official practice secrets:

| Player | Score | Solved | Mean turn | Last win |
|---|---:|---:|---:|---:|
| official hard-mask starter | 92.58 | 119/120 | 12.15 | 28 |
| frozen soft belief | 96.02 | 120/120 | 10.99 | 23 |

Five seeded row-wise Gaussian perturbations of the normalized embeddings:

| Row noise | Sampled comparison agreement | Starter score | Soft score | Delta |
|---:|---:|---:|---:|---:|
| 0.005 | 0.961 | 82.29 +/- 2.03 | 94.63 +/- 0.44 | +12.34 |
| 0.010 | 0.917 | 70.86 +/- 1.95 | 91.03 +/- 1.56 | +20.17 |
| 0.015 | 0.865 | 60.61 +/- 3.92 | 80.40 +/- 3.49 | +19.79 |
| 0.020 | 0.810 | 51.06 +/- 5.49 | 66.11 +/- 2.62 | +15.05 |

Three seeded stochastic-comparison probes also favored soft belief. For
logistic comparison-noise scales `0.005`, `0.010`, and `0.020`, mean scores were
`79.59 -> 94.61`, `70.84 -> 91.64`, and `48.16 -> 74.15` respectively.

Structured shift probes were directionally consistent. On one fixed seed,
anisotropic dimension scaling with log-scale standard deviation `0.6` scored
`75.48 -> 88.58`; a 40% blend with independent normalized row vectors scored
`62.13 -> 82.73`. A signed coordinate permutation/reflection produced exactly
the public scores for both players, as expected: a shared orthogonal transform
preserves every cosine and therefore is not a genuine private-space shift.

As a distribution check beyond the 120 public labels, a fixed random sample of
120 vocabulary secrets scored `93.12 -> 94.53` in exact public geometry,
`64.12 -> 84.97` at row noise `0.01`, and `32.38 -> 48.70` at row noise `0.02`.
This confirms that the main robustness signal is not confined to the official
practice list.

## Runtime And Risks

The contract check passes. Exact-public evaluation of 120 games takes about
0.9 seconds of wall time after data loading on this machine; the starter takes
about 0.06 seconds. The `(1602, 1602)` public cosine matrix dominates memory at
roughly 10 MB as float32. This is far inside the 600-second round limit.

No synthetic transformation identifies the real private generator. Row noise,
anisotropic scaling, and stochastic flips cover order inversion rates but not
all semantic model changes. The environment-variable knobs are only local
probe aids; grader behavior uses the checked-in defaults. The experimental
`ensemble_belief.py`, `vote_belief.py`, `scheduled_belief.py`, and
`mutual_belief.py` did not beat the frozen single soft model across the proxy
portfolio and should not be promoted.

## Recommended Decision

Promote `soft_belief.py` as the next scored candidate after copying only its
`PotatoPlayer` body into the official submission artifact and rerunning the
official local contract/self-score. It gives a +3.43 exact-public gain, repairs
the `kettle` miss, and has large, repeated gains under controlled comparison
inversions; this is sufficient evidence for one leaderboard test, while the
starter remains the deployable fallback until the LB result returns.
