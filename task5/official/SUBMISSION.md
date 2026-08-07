# Official Submission Instructions

Source: https://www.kaggle.com/competitions/ioai-2026-task-5-westlake-nlp-24/overview/kaggle-cli-submission
Accessed: 2026-08-07 17:02 Asia/Chongqing with authenticated Kaggle CLI 2.2.4; content length 10,661 characters, SHA-256 `2bd744c668604aa08e108768a342c632e4ea9bf215fdb7b562986530ff27791c`, and terminal line verified unchanged immediately before scoring the neural-transition candidate.

The text below is copied from the current `Kaggle CLI Submission` page.

---

This competition is **notebook-only**: predictions cannot be uploaded as a file. Every submission must come from a notebook that ran on Kaggle's servers. The steps below do that entirely from the command line.

## Limits for this competition

| Limit | Value |
|---|---|
| Notebook versions | **15 maximum** |
| Kernel runtime | **600 seconds (10 minutes) maximum** |
| Concurrent CPU sessions | 5 |
| Concurrent GPU sessions | 2 |
| GPUs usable per run | **1** (set your device to `cuda:0`) |
| Internet in the notebook | Disabled |
| Solution source size | 1 MB |
| Team size | 1 |

### Capping the runtime at 600 seconds

You must cap every run at **600 seconds**. Kaggle does not enforce this for you, so pass `--timeout` on every push:

```bash
kaggle kernels push -p my-solution/ --timeout 600
```

`--timeout` takes **seconds**, so `600` is the 10-minute cap. The budget covers everything in the run: the offline package install, any training or fine-tuning you do, and inference on all 760 test passages.

A run killed at the timeout produces no usable `submission.csv`, so write the output file before the budget runs out. A long run is also a bad trade: with only 2 concurrent GPU sessions, a slow notebook buys you fewer iterations.

## The deadline rule

`kaggle competitions submit` must be **sent before the competition deadline**.

- Submit before the deadline, scoring finishes after it: **counts**.
- Notebook finished in time but you submit after the deadline: does not count.
- Notebook still running at the deadline: does not count.

Late submissions are still accepted and still produce a score you can see, but they never appear on the leaderboard. Aim to submit a few minutes early.

## Before you start

Accept the competition rules in your browser. There is no CLI equivalent, and data download fails until you do:

```text
https://www.kaggle.com/competitions/<competition-slug>/rules
```

Then install and authenticate the CLI:

```bash
pip install kaggle
export KAGGLE_API_TOKEN="KGAT_..."   # kaggle.com -> Settings -> API
```

## Step 1: Create the notebook folder

A notebook is a folder holding exactly two files:

```text
my-solution/
├── script.py
└── kernel-metadata.json
```

## Step 2: Attach the data in `kernel-metadata.json`

Your notebook has **no internet access**, so every input must be declared up front. There are two separate lists and you need both:

```json
{
  "id": "<your-kaggle-username>/<your-notebook-slug>",
  "title": "My Solution",
  "code_file": "script.py",
  "language": "python",
  "kernel_type": "script",
  "is_private": true,
  "enable_gpu": true,
  "enable_internet": false,
  "machine_shape": "NvidiaTeslaT4",
  "dataset_sources": ["kamalkhan/ioai-2026-wheel-dataset"],
  "competition_sources": ["<competition-slug>"],
  "kernel_sources": [],
  "model_sources": []
}
```

| Field | What it does |
|---|---|
| `dataset_sources` | Mounts the wheel dataset, which is how packages get installed offline |
| `competition_sources` | Mounts `dataset/`, `models/`, and the starter |
| `enable_internet` | Must stay `false` |
| `enable_gpu` + `machine_shape` | Both are needed for a GPU run. Use `NvidiaTeslaT4` |

For a CPU-only run, set `"enable_gpu": false` and `"machine_shape": ""`.

Selecting `NvidiaTeslaT4` provisions two T4 GPUs. Use only **one**, by setting your device to `cuda:0`. `NvidiaTeslaP100` must not be used; Kaggle's PyTorch build does not support it.

## Step 3: Write `script.py`

Start from the supplied `solution.py` in the competition data. Keep two things from it: the environment-setup block at the very top, unchanged, and the two helper functions `find_input` and `read_jsonl` that are defined below it. Replace only `predict_boundaries` and `main` with your own solution.

```python
# =============================================================================
# IOAI 2026 - Ghost of the Machine - TECHNICAL REPORT
# (8-10 paragraphs; see the "Report Generation Prompt" tab for the template)
# =============================================================================

# -- keep the starter setup block here, unchanged --
setup_ioai_env()

# -- keep these two helpers from solution.py --
# def find_input(name, search_root="/kaggle/input"): ...
# def read_jsonl(path): ...

# -- your solution below --
import csv, json
from pathlib import Path

dataset = find_input("dataset")
model_dir = find_input("bge-base-en-v1.5")   # the only allowed pretrained model

test_rows = read_jsonl(dataset / "test_public" / "data.jsonl")
print(f"passages to predict: {len(test_rows)}")

# ... build your model, predict one boundary index per passage ...


def predict(text):
    """Return the predicted boundary, an int in [0, len(text)]."""
    raise NotImplementedError("your model goes here")


out = Path("/kaggle/working/submission.csv")
with out.open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "boundary_char_index"])
    for row in test_rows:
        p = int(predict(row["text"]))
        if not 0 <= p <= len(row["text"]):
            raise ValueError("prediction out of range for " + row["id"])
        w.writerow([row["id"], p])

print(f"wrote {out} with {len(test_rows)} rows")
```

Four rules that cause most first-time failures:

- `setup_ioai_env()` must run **before** you import `torch`, `transformers`, or anything else it installs. `pip` cannot replace a module Python has already loaded, so an import above it silently keeps the old version.
- Write the output to `/kaggle/working/submission.csv` with the exact header `id,boundary_char_index`.
- Include **exactly one row per test id** (760 rows). Row order does not matter; rows are matched by `id`.
- Load `bge-base-en-v1.5` from its local directory. A hub id such as `"BAAI/bge-base-en-v1.5"` triggers a download and fails, because the notebook has no internet.

## Step 4: Run the notebook on Kaggle

```bash
kaggle kernels push -p my-solution/ --timeout 600
```

Each push prints a version number. Record it; you need it to submit:

```text
Kernel version 3 successfully pushed.
```

Then wait for the run to finish:

```bash
kaggle kernels status <your-kaggle-username>/<your-notebook-slug>
```

Statuses go `QUEUED -> RUNNING -> COMPLETE` (or `ERROR`). Poll every ~15 seconds.

Concurrency limits apply across all your notebooks at once: **5** CPU sessions, **2** GPU sessions. Exceeding them rejects the push with `Maximum batch GPU session count of 2 reached`.

## Step 5: Check the output (optional but recommended)

```bash
kaggle kernels output <your-kaggle-username>/<your-notebook-slug> -p out/
```

This downloads `submission.csv` and the run log. Verify the row count (760) and the header before spending a submission. The log is also where you confirm the offline install worked:

```text
IOAI environment ready (wheels from /kaggle/input/datasets/...)
```

## Step 6: Submit

```bash
kaggle competitions submit <competition-slug> \
  -k <your-kaggle-username>/<your-notebook-slug> \
  -v <version-number> \
  -f submission.csv \
  -m "short description"
```

`-f submission.csv` is **not** a local file path. It names an output file that already exists in the completed notebook version on Kaggle. Nothing is uploaded from your machine.

Submitting does **not** re-run your notebook. It scores the `submission.csv` your run already produced. To change your predictions, push a new version and submit that.

## Step 7: Read your score

```bash
kaggle competitions leaderboard <competition-slug> --show
kaggle competitions submissions <competition-slug>
```

## Submission limits

**Your budget is 15 notebook versions.**

Every `kaggle kernels push` creates one version and spends one of the 15, even if the run fails, errors, or is stopped at the 600-second cap. Each version may be submitted to the competition at most once.

### `submission-limits` does not track your budget

`kaggle competitions submission-limits` reports a different quantity from the one that is limited here. It counts **submissions to the competition**; your budget is **notebook versions**. The two diverge in both directions:

```bash
kaggle kernels push -p my-solution/ --timeout 600
# creates a version, spends 1 of your 15
# submission-limits: UNCHANGED

kaggle competitions submit <competition-slug> -k <owner>/<slug> -v 3 -f submission.csv -m "..."
# submission-limits: decrements
```

So the counter can read a large remaining number while you have already spent most of your 15 versions. Track your own usage from the version numbers printed by each push.

Kaggle does not enforce the version limit. The competition organizers do.

Practical consequences:

- Do not push speculatively. A failed push is a spent version.
- Validate your script before pushing: check that it writes `/kaggle/working/submission.csv`, that the header is `id,boundary_char_index`, and that every prediction is an integer inside the passage.
- Self-score on `dataset/dev/` first. It is labelled, disjoint from the test set, and costs you nothing.
- Kaggle occasionally starts a run before the competition data has finished mounting, which fails with `FileNotFoundError`. Pushing again resolves it, but the retry spends another version. Locating files by name rather than by a hard-coded path avoids failures that merely look like this one.

## Report requirement

The script you submit should carry a short technical report in a comment block at the very top. See the **Report Generation Prompt** tab for the template. The report carries no score.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Data download returns 403 or 404 | The account has not accepted the rules. Open the competition in a browser and click **Join competition**. There is no CLI equivalent. |
| `FileNotFoundError` on the first push after attaching the competition | The data mount was not ready. Pushing again resolves it, but costs another notebook version. |
| Old package versions despite the setup block | Something was imported above `setup_ioai_env()`. Move all such imports below it. |
| `Maximum batch GPU session count of 2 reached` | Wait for a running GPU session to finish, or use a CPU notebook. |
| Model fails to load / tries to download | Load `bge-base-en-v1.5` from the local path returned by `find_input`, not by hub id. |
| Score of 0 on some rows | The id was missing, duplicated, unknown, or the value was not an integer in range. |
| Submission accepted but absent from the leaderboard | It was sent after the deadline. Submit earlier next time. |
| Run stopped early with no `submission.csv` | It hit the 600-second cap. Reduce training time and write the output file before the budget runs out. |
