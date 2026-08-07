# Task 2 Compliance and Reproduction Note

This post-run note consolidates the positive claim and known limitations. It
does not modify the historical notebook source or include any post-boundary
method as support for the claimed result.

## Eligible scope

The formal run began at `2026-08-05T05:30:32Z`. Its conservative autonomy
boundary is `2026-08-05T06:24:47.549Z`, when the first modified Continuation
Prompt arrived. Submission `55260695` was sent at `06:19:10.890Z`, before that
boundary and the `07:00:00Z` competition deadline. Its Public LB is `0.55416`;
no Private/final LB is present in the captured records.

The later ExtraTrees score `0.63583` is excluded. It cannot be used to support
this autonomous claim even though it is higher. See `EXCLUSIONS.md`.

## Submission and resource audit

- The result came from private Kaggle Kernel
  `researai/ioai-task2-westlake-rotation-cnn-v2` and the notebook-only
  competition submission flow.
- Metadata records one `NvidiaTeslaT4`, Internet disabled, the competition
  source and official wheel dataset, and no attached model or Kernel sources.
- The source preserves the official offline setup block, trains from scratch,
  uses `cuda:0`, and does not load a pretrained model or external data.
- The remote output has exactly 7,200 rows and columns `id,prediction`.
- Remote runtime was 204.02 seconds, within the 300-second cap.

Artifact hashes:

| Artifact | SHA-256 |
|---|---|
| `notebooks/rotation-cnn-v2/ioai-task2-westlake-rotation-cnn-v2.py` | `942c8b7b33247ae7117ae1f008e704bf17672bb9c75559cdd7a0bac7cb35ef43` |
| `remote/rotation-cnn-v2/submission.csv` | `19cfbca1f4bdede69bb03a77b862e2a4a9495710dde92d31d0da595eb9ac09ba` |
| `remote/rotation-cnn-v2/ioai-task2-westlake-rotation-cnn-v2.log` | `070fe51ea6a142b36fd28ca9a251708e4616fc4093b52d90fcfd5bc0f3dd5293` |

## Historical report correction

The source begins with nine logical report paragraphs and states validation
`54.78`. The exact remote log reports best epoch 13 validation `54.8056`. The
source also could not include its later-known Public LB `0.55416`. These are
documentation gaps, disclosed here rather than repaired in the historical
source. No Private score is claimed.

## Reproduce

From `task2/`:

```bash
sha256sum -c MANIFEST.sha256
python -m py_compile notebooks/rotation-cnn-v2/ioai-task2-westlake-rotation-cnn-v2.py
kaggle kernels push -p notebooks/rotation-cnn-v2/ --timeout 300
```

The final command creates a new Kernel version and consumes a version allowance;
it is shown for authorized reproduction, not as a request to resubmit. The
historical source, output, remote log, submission ledger, prompt snapshot, and
bounded rollout are already included for offline review.
