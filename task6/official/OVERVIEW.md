# Official Overview

Retrieved 2026-08-09 with the authenticated Kaggle CLI from competition
`ioai-2026-task-6-westlake-nlp-60` (IOAI 2026 - IOAI Field).

## Task And Data

Approximate a procedural spatial field `F(x, y, W)` on `[0,1]^2` with a trained
`torch.nn.Module`. The public configuration is loaded from
`ioai-field/data/train_config/field_config.json`; the test configurations are
hidden and vary letter scale/incline and the first-I value range. Training data
must be generated only through the published competition APIs (`field_value`,
`field_masks`, and `make_batch`). The protected runtime must not be inspected,
reverse engineered, patched, or used to reveal hidden evaluation state.

The five equally weighted regions are: first `I` (large linear-gradient values),
`O` (spiral values), `A` (constant -1), last `I` / `I_entropy` (output
variability), and background (constant 0).

## Metric

For `I`, `O`, `A`, and background, 512 points per region are scored by
`1 - min(MAE / scale, 1)`. The shipped evaluator uses the target p1-p99 range
for the letter scales and 0.1 for background. For `I_entropy`, the model is run
10 times with training mode enabled; a point scores zero if any prediction is
outside `[-2026, 2026]`, otherwise it scores the clipped standard deviation
divided by `sqrt(1/12)`. Region scores are averaged and multiplied by 100.

A model with `>= 20,260` parameters has its total score multiplied by 0.5.
Persistent tensors must be `nn.Parameter` values; buffers, raw tensor module
attributes, and NumPy module attributes are rejected.

## Rules And Resources

Only competition data and permitted installed packages may be used. No external
data or pretrained models are permitted. Final notebooks have Internet disabled.
Stochasticity must come from dropout during inference; direct `rand*` and
`_uniform` randomness is prohibited. Runs may use CPU or one T4 via `cuda:0`.
There are at most 20 notebook versions and every push consumes one, including
failed runs. Each run must be explicitly capped at 600 seconds.

The official starter trains a 2,241-parameter ReLU/dropout MLP for 100 batches.
It must be read end-to-end and locally evaluated before replacing it.
