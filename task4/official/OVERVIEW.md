# Official Overview

URL: https://www.kaggle.com/competitions/ioai-2026-task-4-westlake-nlp-24
Retrieved: 2026-08-07 UTC via `kaggle competitions pages ... list --content`.

## Description

Competition title: Double Agent Dilemma. Two frozen ImageNet-1K classifiers are
provided: torchvision `resnet18` (Model R) and timm
`vit_tiny_patch16_224` (Model V). Both are 100% accurate on the supplied labeled
splits and are expected to agree on clean scored images. For each scored image,
emit two additive perturbations at the original raw RGB resolution. Type A must
leave R correct while making V incorrect. Type B must leave V correct while
making R incorrect. The evaluator adds delta to the raw [0,1] image, clips to
[0,1], then applies `Resize(256) -> CenterCrop(224) -> Normalize` with mean
`[0.485,0.456,0.406]` and std `[0.229,0.224,0.225]`.

Only competition data and the two mounted checkpoints may be used. Solutions
may be algorithmic; no external data, models, weights, APIs, or runtime
downloads are allowed. Notebook Internet is disabled. At most one GPU is used
(`cuda:0`) on the allowed `NvidiaTeslaT4` machine shape.

## Data

Competition files mount below `/kaggle/input/` (nesting may vary):

```
data/dataset/train/images/*.png              100 labeled images
data/dataset/train/labels.json
data/dataset/test_public/images/*.png        100 labeled development images
data/dataset/test_public/labels.json
data/dataset/test_leaderboard_a/images/*.png 100 public-scored images
data/dataset/test_leaderboard_b/images/*.png 100 private-scored images
data/models/resnet18.pth
data/models/vit_tiny_patch16_224.safetensors
ioai-starter.py
```

PNG images are RGB and have varying original dimensions. Leaderboard folders
intentionally contain no labels. IDs use the zero-based filename index.

## Evaluation / Scoring

Each output tensor is shape `3 x H x W` for its image and is encoded as a
base64-encoded zlib stream of contiguous little-endian float32 bytes. The CSV
must be named `submission.csv`, have columns `id,delta_a,delta_b`, and contain
exactly 200 rows in order `a_0` through `a_99`, then `b_0` through `b_99`.
Malformed or wrong-shape tensors are treated as zero.

With M=100 images per scored split, `S_pure=(Score_A+Score_B)/(2M)`. Let
`mean(||delta||_2/N)` be the mean over all submitted tensors, where N is the
number of tensor elements. The penalty is
`PF=1.5-sigmoid(50000*mean(||delta||_2/N))`, bounded in [0.5,1], and the
reported score is `100*S_pure*PF`, rounded to two decimals. Public score uses
`test_leaderboard_a`; private score uses `test_leaderboard_b`.

## Rules / Resources

Notebook-only submissions are required; direct prediction-file uploads are not
permitted. Final notebooks have no Internet. The run limit is 600 seconds and
the competition permits at most 20 notebook versions, with each kernel push
counting even on failure. Concurrent limits are 5 CPU sessions and 2 GPU
sessions. The official offline wheel dataset is
`kamalkhan/ioai-2026-wheel-dataset`.

## Starter

`ioai-starter.py` contains the required `setup_ioai_env()` block, dynamic data
path discovery, checkpoint loading, exact preprocessing, and the CSV adapter.
The setup block must execute before importing installed packages. Pushes must
use the exact command and timeout in `official/SUBMISSION.md`; score a completed
notebook version with the competition submission command rather than uploading
a local file.
