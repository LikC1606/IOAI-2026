# Robust rank screen

experiment.py keeps the player on the public matrix and changes only the judge
matrix (or flips judge outcomes), so the comparison isolates public/private
disagreement. It is CPU-only and uses only the competition files.

The bounded sign-likelihood policy (SoftBelief(..., rank_only=True,
reliability=0.65, champion_weight=3)) preserves the exact public practice
score at 92.50 (119/120) versus the starter's 92.583 (119/120). Under
deterministic public-judge outcome flips, it is materially more robust:

| flip probability | hard starter | bounded rank |
| ---: | ---: | ---: |
| 0.00 | 92.583 | 92.500 |
| 0.02 | 82.367 | 89.167 |
| 0.05 | 72.300 | 88.333 |
| 0.10 | 55.200 | 79.117 |
| 0.15 | 39.583 | 66.017 |
| 0.20 | 33.100 | 55.733 |

The same direction appears in embedding-space perturbations. With a coherent
low-rank private shift (sigma=.03/.06), bounded rank scored 86.067/64.517
versus hard 83.050/60.250 on the 120 practice secrets. With independent
row-noise sigma=.01 it scored 75.367 versus hard 74.350. A nearest-family
median smoother was not competitive: its best small grid entry had public
89.10 and low-rank .03/.06 83.98/66.33. The family signal alone is therefore
not a promotion candidate, while bounded rank evidence is.

Runtime for the rank policy is about 0.2s for all 120 practice games after
loading the pairwise matrix. The full grid's balanced information policy was
much slower (about 3s for practice, 40s for all 1602 synthetic secrets), so it
is a research baseline only.

As a geometry sanity check, public/private nearest-neighbor overlap remained
high for coherent shifts: excluding self, top-8 recall was 0.924 at low-rank
sigma=.03 and 0.758 at sigma=.06 (0.832 for row-noise sigma=.01). This supports
using rank/neighborhood evidence while avoiding irreversible exact half-space
cuts.
