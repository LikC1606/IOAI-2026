# Official Submission Instructions

Source: authenticated `Kaggle CLI Submission` page, accessed 2026-08-06 12:39
CST. This competition is notebook-only. A kernel push is free; each accepted
competition submit consumes one of 15 scored submissions, and a notebook version
may be submitted at most once.

The notebook directory must contain exactly `script.py` and
`kernel-metadata.json`. Metadata attaches only competition source
`ioai-2026-task-3-westlake-nlp-48`, with empty dataset/kernel/model sources,
`enable_gpu: false`, `enable_internet: false`, and `machine_shape: ""`.

Exact flow:

```bash
kaggle kernels push -p submission/
kaggle kernels status researai/ioai-2026-task-3-westlake-nlp-48-solution
kaggle kernels output researai/ioai-2026-task-3-westlake-nlp-48-solution -p out/
kaggle competitions submit ioai-2026-task-3-westlake-nlp-48 \
  -k researai/ioai-2026-task-3-westlake-nlp-48-solution \
  -v <version-number> \
  -f submission.csv \
  -m "short description"
kaggle competitions submissions ioai-2026-task-3-westlake-nlp-48
```

Do not pass `--timeout` to `kaggle kernels push`. `-f submission.csv` names the
completed notebook output; it is not a local upload. The submit command must be
sent before 2026-08-06T06:26:44.395Z. Scoring may finish later. Validate locally,
download and inspect the remote CSV, and confirm identical payloads before every
scored submission.
