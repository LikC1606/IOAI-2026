# =============================================================================
# IOAI 2026 - AI Models Track - Ghost of the Machine
# TECHNICAL REPORT
# =============================================================================
#
# 1. SUMMARY
#    This solution fine-tunes the permitted local bge-base-en-v1.5 encoder on all
#    official labels, then decodes one human-to-machine transition. Its train-only
#    predecessor scored 94.56 Public; this refit's Public score is pending.
#
# 2. APPROACH
#    Each feasible sentence start receives the sum of neural machine-origin
#    logits over its suffix plus a fixed Gaussian position prior. This enforces
#    the known single human-prefix/machine-suffix structure end to end.
#
# 3. TEXT REPRESENTATION
#    Sentences are split after terminal punctuation, tokenized to 96 tokens, and
#    represented by the CLS state of the local bge-base-en-v1.5 encoder. This is
#    the only pretrained model used, and it is loaded by local directory only.
#
# 4. TRAINING
#    The full encoder and a binary linear head are trained for one epoch on
#    43,590 sentences from all 1,601 labeled train and dev passages. Encoder/head
#    LRs are 2e-5/1e-4, batch 96, AdamW decay 0.01, and 10% warmup.
#
# 5. FROM MODEL OUTPUT TO A CHARACTER INDEX
#    Reverse cumulative neural logits score candidates with at least 180 words
#    on each side, plus `-0.5*((fraction-mean)/sd)^2`. The best candidate's
#    original character offset is emitted as a range-checked integer.
#
# 6. RESULTS
#    Before refitting, honest remote dev was 95.688 and a fixed train hash holdout
#    scored 94.557 versus 94.324 for the paired sparse baseline. That version
#    scored 94.56 Public. Refit dev is in-sample and is not selection evidence.
#
# 7. ERROR ANALYSIS
#    Honest train-only dev exact-match was 94.2% remotely, MAE 13.03 characters,
#    and error through P90 was zero. The holdout exact rate was 93.33% with MAE
#    20.28, so the refit's in-sample dev output is treated only as a check.
#
# 8. WHAT WAS TRIED AND DROPPED
#    Frozen bge emissions scored 86.82 dev. Sparse cumulative sequence reached
#    93.56 remote dev / 92.48 Public; all-label refitting reached 92.73 Public.
#    Local transitions, pair seams, context windows, and NB were less robust.
#
# 9. LIMITATIONS AND NEXT STEPS
#    It assumes the hidden generator and stitching match labeled data. All 1,601
#    known labels satisfy the sentence and 180-word constraints, but the fixed
#    single epoch has not been ensembled and neural training can vary by device.
#
# 10. RUNTIME
#    All-label training plus test inference took 24.8s on one H100 with 5.05GB
#    peak VRAM. A conservative T4 projection including setup and the dev check is
#    below 330s. The notebook exposes and uses only `cuda:0` under the 600s cap.
#
# =============================================================================

# ─── IOAI 2026 — environment setup. Keep this at the VERY TOP of your script. ───
# Installs the competition's pinned packages from the mounted wheel files.
# No internet is used. It must run BEFORE you import any of those packages:
# pip cannot change a module that Python has already loaded.
#
# Attach the wheel dataset to your notebook first:
#     Add data -> Datasets -> "ioai-2026-wheel-dataset"
# (or fork the official starter, which already has it attached).
#
# Two steps, because it makes the difference between 40 seconds and 6 minutes:
#   1. install `uv` (a fast installer) with pip — one small wheel, ~6s
#   2. use `uv` to install everything else                        — ~34s
import os
import re
import subprocess
import sys
from pathlib import Path

# torch ships as e.g. torch-2.13.0+cu126-...whl. Kaggle strips the "+" from
# uploaded filenames, leaving torch-2.13.0cu126-... — which is not a parseable
# version, so pip and uv do not recognise the file as torch at all. Normalising
# the name to torch-2.13.0-... fixes that, but then the filename disagrees with
# the wheel's internal metadata, which uv rejects unless told the mismatch is
# intentional. Hence both the rename and UV_SKIP_WHEEL_FILENAME_CHECK below.
WHEEL_DATASET = "ioai-2026-wheel-dataset"

_LOCAL_VER = re.compile(r"^(?P<name>[^-]+)-(?P<ver>\d[\d.]*)(?:\+?cu\d+)-(?P<rest>.+\.whl)$")


def _find_wheels(search_root="/kaggle/input", depth=7):
    """Locate the wheel directory by looking for the meta-wheel.

    Never hard-code the path: Kaggle mounts competition data under
    /kaggle/input/competitions/<slug>/ and datasets under
    /kaggle/input/datasets/<owner>/<slug>/, and the nesting can change.
    """
    base = Path(search_root)
    for d in range(depth):
        hits = sorted(base.glob("/".join(["*"] * d + ["ioai_env-*.whl"])))
        if hits:
            return hits[0].parent
    present = sorted(str(p.relative_to(base)) for p in base.glob("*"))[:20]
    raise FileNotFoundError(
        f"IOAI wheels not found under {base}.\n"
        f"  {base} currently contains: {present or '<nothing>'}\n\n"
        f"  Add the wheel dataset to this notebook:\n"
        f"    Add data -> Datasets -> search '{WHEEL_DATASET}'\n"
        f"  (or fork the official starter notebook, which already has it attached)."
    )


def _normalise(wheels):
    """Return a directory whose wheel filenames all parse.

    Symlinks only — nothing is copied, so this costs no disk and no time.
    If every name is already fine, the original directory is used as-is.
    """
    needs_fix = [w for w in wheels.glob("*.whl") if _LOCAL_VER.match(w.name)]
    if not needs_fix:
        return wheels
    work = Path("/kaggle/working/_ioai_wheels")
    work.mkdir(parents=True, exist_ok=True)
    for stale in work.glob("*"):
        stale.unlink()
    for w in sorted(wheels.glob("*.whl")):
        m = _LOCAL_VER.match(w.name)
        name = f"{m['name']}-{m['ver']}-{m['rest']}" if m else w.name
        (work / name).symlink_to(w)
    print(f"normalised {len(needs_fix)} wheel filename(s) into {work}")
    return work


def setup_ioai_env(search_root="/kaggle/input"):
    """Install the pinned environment offline. Returns the wheel directory."""
    wheels = _normalise(_find_wheels(search_root))
    common = ["--no-index", f"--find-links={wheels}"]

    # Step 1 — bootstrap uv itself with pip. One wheel, no dependencies.
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
                           *common, "uv"])

    # Step 2 — let uv do the heavy lifting. `-m uv` rather than the `uv`
    # executable, so this does not depend on PATH inside the kernel.
    env = dict(os.environ, UV_SKIP_WHEEL_FILENAME_CHECK="1")
    try:
        subprocess.check_call([sys.executable, "-m", "uv", "pip", "install",
                               "--system", *common, "ioai-env"], env=env)
    except subprocess.CalledProcessError:
        # Falling back is deliberate: a slow run beats a failed submission.
        print("WARNING: uv failed — falling back to pip. This takes ~6 minutes "
              "instead of ~35 seconds, but it will work.", flush=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
                               "--only-binary=:all:", *common, "ioai-env"])

    print(f"IOAI environment ready (wheels from {wheels})")
    return wheels


setup_ioai_env()
# ───────────────────────────────────────────────────────────────────────────────

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import csv
import json
import math
import random
import time

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModel, AutoTokenizer

TARGET_COLUMN = "boundary_char_index"
SENTENCE_BREAK = re.compile(r"(?<=[.!?])[\"']?\s+")


def find_input(name, search_root="/kaggle/input"):
    matches = sorted(Path(search_root).rglob(name))
    if not matches:
        raise FileNotFoundError(f"{name} not found under {search_root}")
    return matches[0]


def read_jsonl(path):
    rows = []
    with Path(path).open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def answer_map(path):
    return {row["id"]: int(row[TARGET_COLUMN]) for row in read_jsonl(path)}


def sentence_units(text):
    starts = [0] + [match.end() for match in SENTENCE_BREAK.finditer(text)]
    ends = starts[1:] + [len(text)]
    units = [text[start:end].strip() or "." for start, end in zip(starts, ends)]
    return starts, units


def flatten_rows(rows, truth=None):
    metadata, texts, labels, raw_weights = [], [], [], []
    for row in rows:
        starts, units = sentence_units(row["text"])
        offset = len(texts)
        texts.extend(units)
        metadata.append((starts, slice(offset, len(texts))))
        if truth is not None:
            boundary = truth[row["id"]]
            if boundary not in starts:
                raise ValueError(f"{row['id']}: truth is not a sentence start")
            boundary_unit = starts.index(boundary)
            labels.extend([0] * boundary_unit + [1] * (len(starts) - boundary_unit))
            raw_weights.extend([1.0 / len(starts)] * len(starts))
    if truth is None:
        return texts, metadata, None, None
    labels = np.asarray(labels, dtype=np.float32)
    weights = np.asarray(raw_weights, dtype=np.float32)
    for value in (0.0, 1.0):
        weights[labels == value] *= 0.5 / weights[labels == value].sum()
    weights *= len(weights) / weights.sum()
    return texts, metadata, labels, weights


class TextDataset(Dataset):
    def __init__(self, texts, labels=None, weights=None):
        self.texts = texts
        self.labels = labels
        self.weights = weights

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        if self.labels is None:
            return self.texts[index]
        return self.texts[index], self.labels[index], self.weights[index]


class Collator:
    def __init__(self, tokenizer, max_length=96):
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __call__(self, examples):
        labelled = isinstance(examples[0], tuple)
        texts = [item[0] for item in examples] if labelled else examples
        tokens = self.tokenizer(
            texts, padding=True, truncation=True, max_length=self.max_length,
            pad_to_multiple_of=8, return_tensors="pt",
        )
        if labelled:
            tokens["labels"] = torch.tensor([item[1] for item in examples])
            tokens["weights"] = torch.tensor([item[2] for item in examples])
        return tokens


class OriginModel(nn.Module):
    def __init__(self, model_dir):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_dir, local_files_only=True)
        self.classifier = nn.Linear(self.encoder.config.hidden_size, 1)
        nn.init.normal_(self.classifier.weight, mean=0.0, std=0.02)
        nn.init.zeros_(self.classifier.bias)

    def forward(self, **tokens):
        cls = self.encoder(**tokens).last_hidden_state[:, 0]
        return self.classifier(cls).squeeze(-1)


def train_one_epoch(model, loader, device):
    optimizer = torch.optim.AdamW([
        {"params": model.encoder.parameters(), "lr": 2e-5},
        {"params": model.classifier.parameters(), "lr": 1e-4},
    ], weight_decay=0.01)
    steps = len(loader)
    warmup = max(1, int(0.1 * steps))

    def schedule(step):
        if step < warmup:
            return (step + 1) / warmup
        return max(0.0, (steps - step) / max(1, steps - warmup))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, schedule)
    scaler = torch.amp.GradScaler("cuda")
    model.train()
    started = time.perf_counter()
    for step, batch in enumerate(loader):
        labels = batch.pop("labels").to(device, non_blocking=True)
        weights = batch.pop("weights").to(device, non_blocking=True)
        batch = {key: value.to(device, non_blocking=True) for key, value in batch.items()}
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda", dtype=torch.float16):
            logits = model(**batch)
            losses = nn.functional.binary_cross_entropy_with_logits(logits, labels, reduction="none")
            loss = (losses * weights).sum() / weights.sum()
        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()
        scheduler.step()
        if step in {0, steps // 2, steps - 1}:
            print(f"train step {step + 1}/{steps} loss={float(loss.detach()):.5f} "
                  f"elapsed={time.perf_counter() - started:.1f}s", flush=True)


@torch.inference_mode()
def infer(model, texts, collator, device):
    loader = DataLoader(TextDataset(texts), batch_size=256, shuffle=False,
                        collate_fn=collator, num_workers=0, pin_memory=True)
    model.eval()
    output = []
    for batch in loader:
        batch = {key: value.to(device, non_blocking=True) for key, value in batch.items()}
        with torch.autocast(device_type="cuda", dtype=torch.float16):
            output.append(model(**batch).float().cpu().numpy())
    return np.concatenate(output)


def valid_candidates(text, starts):
    valid = []
    for index in range(1, len(starts)):
        start = starts[index]
        if len(text[:start].split()) >= 180 and len(text[start:].split()) >= 180:
            valid.append(index)
    if valid:
        return np.asarray(valid, dtype=np.int64)
    return np.arange(1, len(starts), dtype=np.int64)


def decode(rows, metadata, logits, prior_mean, prior_sd):
    predictions = []
    for row, (starts, unit_slice) in zip(rows, metadata):
        if len(starts) < 2:
            predictions.append(int(prior_mean * len(row["text"])))
            continue
        sentence_logits = logits[unit_slice]
        candidates = valid_candidates(row["text"], starts)
        emission = np.cumsum(sentence_logits[::-1])[::-1]
        fractions = np.asarray(starts, dtype=np.float64) / len(row["text"])
        log_prior = -0.5 * np.square((fractions - prior_mean) / prior_sd)
        best = int(candidates[int(np.argmax(emission[candidates] + log_prior[candidates]))])
        predictions.append(int(starts[best]))
    return predictions


def main():
    overall_started = time.perf_counter()
    random.seed(2026)
    np.random.seed(2026)
    torch.manual_seed(2026)
    if not torch.cuda.is_available():
        raise RuntimeError("cuda:0 is required")
    torch.cuda.manual_seed_all(2026)
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    device = torch.device("cuda:0")

    dataset = find_input("dataset")
    model_dir = find_input("bge-base-en-v1.5")
    train_rows = read_jsonl(dataset / "train" / "data.jsonl")
    train_answers = answer_map(dataset / "train" / "answers.jsonl")
    dev_rows = read_jsonl(dataset / "dev" / "data.jsonl")
    dev_answers = answer_map(dataset / "dev" / "answers.jsonl")
    test_rows = read_jsonl(dataset / "test_public" / "data.jsonl")
    fit_rows = train_rows + dev_rows
    fit_answers = {**train_answers, **dev_answers}
    train_texts, _, train_labels, train_weights = flatten_rows(fit_rows, fit_answers)
    dev_texts, dev_metadata, _, _ = flatten_rows(dev_rows)
    test_texts, test_metadata, _, _ = flatten_rows(test_rows)
    fractions = np.asarray([fit_answers[row["id"]] / len(row["text"]) for row in fit_rows])
    prior_mean, prior_sd = float(fractions.mean()), float(fractions.std(ddof=1))

    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    collator = Collator(tokenizer, max_length=96)
    loader = DataLoader(
        TextDataset(train_texts, train_labels, train_weights), batch_size=96,
        shuffle=True, generator=torch.Generator().manual_seed(2026),
        collate_fn=collator, num_workers=0, pin_memory=True,
    )
    model = OriginModel(model_dir).to(device)
    print(f"device={device} gpu={torch.cuda.get_device_name(0)} "
          f"train_sentences={len(train_texts)}", flush=True)
    torch.cuda.reset_peak_memory_stats()
    train_one_epoch(model, loader, device)
    dev_logits = infer(model, dev_texts, collator, device)
    test_logits = infer(model, test_texts, collator, device)
    dev_predictions = decode(dev_rows, dev_metadata, dev_logits, prior_mean, prior_sd)
    predictions = decode(test_rows, test_metadata, test_logits, prior_mean, prior_sd)

    if len(predictions) != 760 or len({row["id"] for row in test_rows}) != 760:
        raise RuntimeError("expected exactly 760 unique test ids")
    out = Path("/kaggle/working/submission.csv")
    with out.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", TARGET_COLUMN])
        for row, prediction in zip(test_rows, predictions):
            prediction = int(prediction)
            if not 0 <= prediction <= len(row["text"]):
                raise ValueError("prediction out of range for " + row["id"])
            writer.writerow([row["id"], prediction])
    print(f"wrote {out} with {len(test_rows)} rows")

    errors = [abs(p - dev_answers[row["id"]]) for row, p in zip(dev_rows, dev_predictions)]
    score = 100.0 * sum(math.exp(-error / 100.0) for error in errors) / len(errors)
    print(f"in-sample refit dev check: {score:.3f} | exact: "
          f"{sum(e == 0 for e in errors)}/{len(errors)} "
          f"| MAE: {sum(errors) / len(errors):.2f} | total: "
          f"{time.perf_counter() - overall_started:.1f}s | peak_vram_gb: "
          f"{torch.cuda.max_memory_allocated() / 2**30:.2f}")


main()
