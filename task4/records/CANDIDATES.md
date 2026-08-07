# Candidate Routes

Objective: maximize the official success-rate times norm penalty while retaining
an exact, reproducible notebook path. No numeric LB target was supplied; the
breakthrough objective is to remove the measured failure bottleneck (type
specific flips at the lowest mean L2 per pixel).

## Breakthrough Objective

Find a mechanism that raises both Type A and Type B success on fresh public
images without increasing the mean norm enough to lower the final score. A
route is promising when its success and norm profile is stable across train and
test_public and its runtime is T4-feasible.

## Key Bottleneck And Score Budget

Public LB calibration supports complete attack success: version 1's 98.23 is
exactly its evaluator-side norm penalty. The dominant measured loss is therefore
perturbation norm, not missed crossings or clean classification.

## Deployable Frontier

- **Fallback: version-2 fine-quantized dual-margin raw PGD.** Up to 100
  RMS-normalized steps (`1e-4` step, `1e-2` radius), protected-margin hinge
  weight 2/floor 0.02, ten-step backtracking, 0.03 attack buffer, and fine
  `2^-14..2^-24` quantization. It scored **98.36 public**, passed 400/400 local
  proxy conditions, and has a verified notebook-only one-T4 path.
- **Deployable incumbent: version-4 refined fine-quantized PGD.** Eight
  shrink/projection steps follow the same feasible attack, then the proven fine
  quantizer is applied with a 0.01 attack buffer. The remote notebook completed
  in 316 seconds, its 190,117,536-byte output passed independent 400/400 replay,
  and its exactly calibrated public proxy was 98.4084. Submission `55316818`
  scored **98.41 public**, a +0.05 gain, and was accepted before the deadline.
  The submissions API contains that result, while the active-team/leaderboard
  endpoint still shows version 2 during post-deadline finalization.

## Scientific Frontier

- **Dual-objective PGD (mechanism-distinct optimization):** directly optimize
  one model's untargeted loss with a protected-model margin hinge through the
  exact raw-resolution transform. Screen step size, steps, and norm projection
  on train/test_public; cheapest falsification is zero type-specific flips.
- **Targeted boundary search:** choose a low-margin rival class and minimize
  perturbation with a CW-style margin objective, then reject any protected-model
  flip. Tests whether targeted directions are materially smaller than untargeted
  PGD.
- **Input-space low-rank parameterization:** optimize a 224/256-grid perturbation
  and resize it back to raw resolution, testing whether interpolation-aware
  spreading lowers the global norm while preserving flips.
- **Feasible minimum-norm refinement:** after PGD, alternate 2% shrinkage with
  linearized projection back onto attacked/protected margin constraints. The
  full labeled confirmation cell retained 200/200 and reduced RMS about 3% for
  Type A and 1-2% for Type B with eight steps. A complete encoded-artifact norm
  and success replay is the selection gate; expected full remote cost is below
  600 seconds.

## Active Routes

Version 4 is the scored deployable incumbent and version 2 is the fallback.
Targeted boundary search remains scientific upside, but the deadline has passed.
The only live check is private transfer against the locked 98.3194 proxy.

## Retired Routes And Lessons

- Constant noise is retired as an interface-only sanity check because it does
  not cause architecture-specific flips.
- Dense raw-gradient encoding is retired for deployment despite identical model
  behavior: its 644 MB artifact wastes runtime and output bandwidth. Adaptive
  power-of-two quantization preserves all checked conditions at about 74 MiB.
- A top-5 linearized DeepFool screen is retired after a bounded 30-image test:
  it reached 30/30 for both types but mean RMS was `6.05e-4` (A) and `8.55e-4`
  (B), worse than the dual-margin PGD incumbent. The local boundary is too
  nonlinear/protected-model-sensitive for that one-step geometry to pay back
  its extra gradients.
- Lowering the quantizer scale below 1.0 was screened on the complete artifact.
  It retained 400/400 conditions but slightly increased mean `L2/N` to
  `7.293e-7` (from `7.279e-7`), so the original scale list remains incumbent.
- A diagnostic enforcing both `antialias=True` and `False` with a 0.03 buffer
  produced a 197.6 MB artifact whose corrected public penalty proxy was 98.30,
  below version 2's observed 98.36. It is retired because robustness cost more
  norm than the public evidence justifies.
