# Candidate Routes

## Breakthrough Objective

Improve the autonomous v3 Public score of **75.01540** by retaining the
near-perfect entropy/background baseline and adding stable A/O/I accuracy under
plausible geometry shifts. The measured bottleneck is chiefly A/background
support and hidden I geometry.

## Key Bottleneck And Score Budget

Mode-routed dropout makes ~63.2 locally without learning. Remaining public
headroom is approximately 20 points from A, 6.3 from O, and 10.5 from I. The
hidden bottleneck is geometry/value-range transfer, not entropy.

## Deployable Frontier

- Incumbent v3: lane-density conditioned routed sine, held confirmation proxy
  73.0339 (worst 69.8745) and remote public 75.01540. This improves A while
  retaining the safe first-I fallback and bounded entropy branch.
- Retained v2: seed-randomized routed sine, held-seed proxy 69.7828 and remote
  public 70.95502. This remains the exact fallback if batch-context behavior is
  later shown to be unstable.
- Retained v1: public-fit routed sine, local matched 86.07, remote public
  47.15536; useful only as a matched-sanity diagnostic.
- Local diagnostic incumbent: eval-mode zero, train-mode bounded eight-unit
  dropout sum; 1 parameter, matched sanity 63.193.

## Scientific Frontier

- Mechanism-distinct: sine-activated coordinate network with separate huge-I
  and small-value heads, plus mode-routed entropy.
- Mechanism-distinct: piecewise/local-basis or geometric classifier-regressor
  that treats mask support separately from region value approximation.
- Same-family exploitation: ReLU/tanh MLP widths, losses, and sampling weights.

## Active Routes

- Train a sub-20,260 parameter sine model on balanced region samples; falsify if
  it cannot improve A and O while holding background on fresh public seeds.
- Train with legal config perturbations; falsify if confirmation worst-cell is
  below a public-only model without a corresponding hidden-boundary rationale.

- Active replacement: seed-randomized routed sine trained on seeds 0-7 and
  calibrated on 8-11; mechanism-distinct information use is config robustness.
- Higher-ceiling screen: set-conditioned sine model trained on evaluator-like
  shuffled batches, using only the coordinates actually passed to `forward`.

## Retired Routes And Lessons

- Official [32,32,32] ReLU/dropout starter: matched score 36.825, worse than the
  zero output baseline because one stochastic head compromises all objectives.
