# Pre-Boundary Research Summary (Reconstructed Audit)

This file was written after the run from evidence that itself predates the
2026-08-06 13:46:19.450 CST autonomy boundary. It is an audit summary, not an
original timestamped research file. The later-mutated live `TASK_KNOWLEDGE.md`,
`RESEARCH.md`, and `CANDIDATES.md` are deliberately not copied as historical
snapshots.

## Task understanding reached autonomously

The agent identified the task as sequential noisy preference search over 1,602
legal words. Each verdict compares the retained champion with a proposal in an
unavailable private embedding space. The supplied public embedding therefore
provides useful neighborhood geometry but its pairwise ordering cannot be treated
as a hard hidden-judge constraint. The 600-second budget and 120 games make a
precomputed 1,602-by-1,602 similarity matrix feasible.

The starter's 92.58 public self-score but 32.50 LB made the public/private mismatch
the dominant bottleneck. The agent stopped treating public self-score as an LB
estimator and used it mainly for contract, coverage, and runtime checks. It built
synthetic row-noise, low-rank, anisotropic, random-mixture, and verdict-flip
screens to test robustness hypotheses while acknowledging that none identifies
the true private generator.

## Independent lanes executed

- Deployable baseline: exact official starter, contract-valid and remotely
  submitted as v1.
- Query balance: evaluated information/partition-aware acquisition while holding
  the starter-style belief update fixed.
- Robust rank: bounded sign evidence retained more wins than irreversible hard
  masks under controlled verdict flips and embedding shifts.
- Soft belief: maintained probability mass over all candidates with a logistic
  public-margin likelihood plus mismatch floor; entropy-aware shortlist proposal
  selection improved robustness screens and became the main deployable route.
- Practice/sampling prior: tested weak centroid priors, explicit practice-secret
  penalties, stronger/no prior ablations, and showed through v8 that the centroid
  did not explain the best LB gain.
- Online calibration: used solved-game comparisons to fit later-game likelihood
  settings; v6 regressed from v4 on LB.

Runnable pre-boundary artifacts and result notes are preserved under
`research/candidates`. The selection was reconstructed from source filesystem
modification times no later than the boundary and corroborated by the included
rollouts. The directory includes `v10_soft15.py` because its source was created at
13:42:55 CST; its post-boundary remote submission/result remains excluded.

## Autonomous evidence loop

The platform feedback established: hard starter 32.50; first soft posterior 45.70;
bounded sign 40.75; calibrated soft likelihood 58.51666; practice penalty 45.70;
online calibration 55.01666; intermediate likelihood 54.11666; and no-prior v8
58.51666. The v4/v8 tie isolated the meaningful gain to robust comparison
likelihood and acquisition rather than the practice centroid.

The pre-boundary main rollout then began a broader softening candidate (v10) after
recognizing the v5-v7 plateau. The source existed before supervision, but the
scored action did not, so it is research evidence only. No centered, tail,
dynamic-embedding, external-embedding, or user-specified semantic method is part
of this summary's positive claim.

## Provenance cautions

The contemporaneous JSONL records are useful for hypotheses and reflections, but
they were manually written by the agent and are not a platform clock. Kaggle
timestamps/status/scores and exact remote payloads take precedence. Candidate
copy times in this package reflect audit copying, not original creation; original
times and patch/tool evidence remain in the pre-boundary rollouts.
