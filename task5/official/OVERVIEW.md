# Official Overview

Source: https://www.kaggle.com/competitions/ioai-2026-task-5-westlake-nlp-24/overview
Accessed: 2026-08-07 15:09 Asia/Chongqing with authenticated Kaggle CLI 2.2.4.

## Task

"Ghost of the Machine" is supervised text change-point detection. Each English passage begins with human-written text and switches exactly once to a language-model continuation conditioned on the human prefix. Predict the character offset at which the machine continuation begins. Both sides contain at least 180 words and passages are roughly 500-800 words.

The only permitted pretrained model is the supplied local `bge-base-en-v1.5` encoder (110M parameters). It may be frozen or fine-tuned on competition data. No other pretrained weights, external data, external embeddings, external AI services, or internet access are allowed. Classical/statistical and non-ML methods are permitted.

## Data

- `dataset/train`: 1,221 labeled passages.
- `dataset/dev`: 380 labeled, disjoint passages for free self-scoring.
- `dataset/test_public`: 760 unlabeled passages, split invisibly into 380 Public and 380 Private leaderboard rows.
- `models/bge-base-en-v1.5`: the only allowed pretrained encoder; load from its local directory.
- `solution.py`: official starter and required offline setup block.
- `sample_submission.csv`: exact output schema.

All splits are stated to be drawn from the same distribution. Find `dataset` and `bge-base-en-v1.5` by recursively searching under `/kaggle/input`; do not hard-code mount paths.

## Evaluation

For prediction `p` and truth `t`, the per-row score is `exp(-abs(p-t)/100)`. The competition score is 100 times the mean per-row score, rounded to two decimals; higher is better. Output `/kaggle/working/submission.csv` with exactly `id,boundary_char_index`, one row per 760 test ids. Values must be Python-`int`-compatible integers in `[0, len(text)]`. Missing, duplicate, unknown, invalid, or out-of-range rows score zero.

Official mean-boundary-fraction baseline: 28.60 Public / 32.68 Private.

## Hard Rules And Resources

- Notebook-generated submissions only; direct file upload is forbidden.
- Maximum 15 Kaggle notebook versions; every `kaggle kernels push`, including failures/timeouts, spends one. Each version may be submitted at most once.
- Every push must use `--timeout 600`; this covers offline install, training, and inference.
- Internet disabled. The official setup block from `solution.py` must remain unchanged and run above every other installed-package import.
- Attach both competition data and `kamalkhan/ioai-2026-wheel-dataset`.
- CPU or `NvidiaTeslaT4`; never P100. T4 provisioning exposes two devices but the solution may use only `cuda:0`.
- Source size at most 1 MB; team size 1; five concurrent CPU sessions and two GPU sessions.
- `kaggle competitions submit` must be sent before the deadline; scoring may finish later.
- Final submissions are auto-selected by Public score; do not manually select them.

## Technical Report

Each submitted script must begin with an 8-10 paragraph comment report above the setup block. It must describe the submitted solution, framing, representation, training, character-index decoding, dev/Public results, absolute-error distribution, dropped methods, limitations, and runtime. It carries no score.
