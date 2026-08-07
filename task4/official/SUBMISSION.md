# Official Submission Instructions

URL: https://www.kaggle.com/competitions/ioai-2026-task-4-westlake-nlp-24
Retrieved: 2026-08-07T06:10Z via Kaggle CLI immediately before the version-4 scoring action. Refresh this page immediately before each remote
action.

The competition is notebook-only. Direct prediction-file upload is forbidden;
the notebook version must create `/kaggle/working/submission.csv` on Kaggle.
Every kernel run must be capped at 600 seconds, and every push must include:

```bash
kaggle kernels push -p <folder>/ --timeout 600
```

There are at most 20 notebook versions; every push spends one even if the run
errors or times out. A single GPU may be used (`cuda:0`) with metadata
`enable_gpu: true`, `machine_shape: "NvidiaTeslaT4"`; notebook Internet must be
disabled. Attach both the wheel dataset and competition data:

```json
{
  "id": "<username>/<notebook-slug>",
  "title": "<title>",
  "code_file": "script.py",
  "language": "python",
  "kernel_type": "script",
  "is_private": true,
  "enable_gpu": true,
  "enable_internet": false,
  "machine_shape": "NvidiaTeslaT4",
  "dataset_sources": ["kamalkhan/ioai-2026-wheel-dataset"],
  "competition_sources": ["ioai-2026-task-4-westlake-nlp-24"],
  "kernel_sources": [],
  "model_sources": []
}
```

`script.py` must begin with the required 8-10 paragraph technical report
comment block, followed by the starter's environment setup block unchanged.
The setup block runs before imports and installs pinned packages offline from
the mounted wheel files. Locate competition files by name under
`/kaggle/input`; do not hard-code the mount nesting. Load only the supplied
ResNet-18 and ViT-Tiny checkpoints.

Before scoring, poll the pushed notebook and inspect its output:

```bash
kaggle kernels status <username>/<notebook-slug>
kaggle kernels output <username>/<notebook-slug> -p out/
```

Once the run is complete and its output contains the required file, submit that
remote output using the exact command:

```bash
kaggle competitions submit ioai-2026-task-4-westlake-nlp-24 \
  -k <username>/<notebook-slug> \
  -v <version-number> \
  -f submission.csv \
  -m "short description"
```

`-f submission.csv` names the file produced by the completed notebook; it is
not a local path. Submitting does not rerun the notebook. Read results with:

```bash
kaggle competitions leaderboard ioai-2026-task-4-westlake-nlp-24 --show
kaggle competitions submissions ioai-2026-task-4-westlake-nlp-24
```

The output must have exact header `id,delta_a,delta_b` and exactly 200 rows in
order `a_0..a_99` followed by `b_0..b_99`. Each delta is a base64-encoded zlib
stream of contiguous little-endian float32 bytes with shape `3 x H x W` at the
original image resolution. Write finite values and validate the full output,
runtime, and memory locally before spending a kernel version. A first meaningful
legal baseline may establish the remote reference; later pushes need a
validated improvement or an explicit mechanism-distinct hidden-boundary probe.
