# =============================================================================
# IOAI 2026 - AI Models Track - Find the Order
# TECHNICAL REPORT
# =============================================================================
#
# 1. SUMMARY
#    This submission transcribes every turn with whisper-small, identifies the
#    two speakers with balanced MFCC clustering, and orders turns using bundled
#    Qwen2.5-0.5B transition likelihood. Public validation scores 0.785577.
#
# 2. APPROACH
#    Ordering is a maximum-coherence path problem. Directed next-turn scores
#    feed a prefix-constrained beam search of width 128, while a hard alternating
#    speaker constraint removes paths that cannot be two-party conversations.
#
# 3. AUDIO AND TEXT FEATURES
#    The allowed whisper-small checkpoint performs zero-shot English ASR.
#    Nineteen MFCC means and standard deviations plus spectral centroid and
#    bandwidth describe voice timbre. Qwen2.5-0.5B is used zero-shot in FP16.
#
# 4. USE OF PREFIX INFORMATION
#    The two supplied indices are fixed at ranks 0 and 1, seed the two MFCC
#    speaker centroids, and determine even/odd speaker parity. Every decoded
#    permutation is asserted to preserve this prefix exactly.
#
# 5. TRAINING
#    No neural weights are trained. Per-dialogue two-cluster K-means uses only
#    that dialogue's hidden-test audio, fixed prefix seeds, one initialization,
#    at most 30 iterations, and an exact balanced speaker-count projection.
#
# 6. INFERENCE AND PERMUTATION CONSTRUCTION
#    Qwen scores target tokens in "A: previous / B: reply" pairs. Log-likelihood
#    sums are divided by token_count**0.75. Beam width 128 selects an alternating
#    path, which is inverted to ranks and checked for uniqueness and completeness.
#
# 7. RESULTS
#    Mean pairwise accuracy is 0.785577 on all 100 test_public dialogues.
#    Balanced speaker parity is 98.893% per chunk and perfect for 97 dialogues.
#    Public LB is pending because this is the first submission of this approach.
#
# 8. WHAT WAS TRIED AND DROPPED
#    Prefix-index baselines scored 0.682710 and 0.699420. Unconstrained Qwen
#    transition beams peaked at 0.758831; plain/reply templates, greedy beams,
#    antisymmetric scores, and other length normalizations were weaker.
#
# 9. LIMITATIONS AND NEXT STEPS
#    Pair-local likelihood does not model full dialogue history, ASR errors can
#    break references, and 0.5B Qwen sometimes favors generic replies. The
#    monotonic cutoff falls back to a valid prefix-aware order if time is short.
#
# 10. RUNTIME
#    The notebook uses one T4 through cuda:0 and FP16 inference. Public ASR took
#    14.69 seconds and complete public Qwen scoring 6.84 seconds on a local H100;
#    the script reserves a conservative buffer under Kaggle's 600-second cap.
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

# ─── Your solution below ───────────────────────────────────────────────────────
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import csv
import gc
import json
import math
import time

import librosa
import numpy as np
import torch
from sklearn.cluster import KMeans
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    WhisperForConditionalGeneration,
    WhisperProcessor,
)


STARTED = time.monotonic()
DEADLINE = STARTED + 500.0
DEVICE = "cuda:0"
ASR_BATCH = 16
LM_BATCH = 32
BEAM_WIDTH = 128
LENGTH_ALPHA = 0.75


def find_split(name, search_root="/kaggle/input"):
    matches = [
        path for path in Path(search_root).rglob(name)
        if path.is_dir() and (path / "prefix.csv").is_file()
    ]
    if not matches:
        raise FileNotFoundError(f"{name} split not found under {search_root}")
    return sorted(matches)[0]


def find_model(name, search_root="/kaggle/input"):
    matches = [
        path for path in Path(search_root).rglob(name)
        if path.is_dir() and (path / "config.json").is_file()
    ]
    if not matches:
        raise FileNotFoundError(f"model {name} not found under {search_root}")
    return sorted(matches)[0]


def chunk_index(path):
    return int(path.stem.removeprefix("chunk_"))


def balanced_speaker_labels(features, prefix):
    values = np.asarray(features, dtype=np.float32)
    values = (values - values.mean(0)) / (values.std(0) + 1e-5)
    first, second = prefix
    clustering = KMeans(
        n_clusters=2,
        init=np.stack([values[first], values[second]]),
        n_init=1,
        max_iter=30,
        random_state=0,
    ).fit(values)
    centers = clustering.cluster_centers_
    if np.linalg.norm(values[first] - centers[0]) > np.linalg.norm(values[first] - centers[1]):
        centers = centers[::-1]
    margin = (
        np.linalg.norm(values - centers[0], axis=1)
        - np.linalg.norm(values - centers[1], axis=1)
    )
    margin[first], margin[second] = -1e9, 1e9
    even_count = (len(values) + 1) // 2
    even_indices = set(np.argsort(margin)[:even_count].tolist())
    labels = [0 if index in even_indices else 1 for index in range(len(values))]
    assert labels[first] == 0 and labels[second] == 1
    assert labels.count(0) == even_count
    return labels


def fallback_order(n, prefix, parities):
    remaining = set(range(n)).difference(prefix)
    order = list(prefix)
    while remaining:
        parity = len(order) % 2
        choices = sorted(index for index in remaining if parities[index] == parity)
        chosen = choices[0] if choices else min(remaining)
        order.append(chosen)
        remaining.remove(chosen)
    return order


def beam_decode(n, prefix, parities, edges):
    beams = [(0.0, tuple(prefix), frozenset(prefix))]
    while len(beams[0][1]) < n:
        expanded = []
        for score, path, used in beams:
            expected_parity = len(path) % 2
            for nxt in range(n):
                if nxt not in used and parities[nxt] == expected_parity:
                    expanded.append(
                        (score + edges[path[-1], nxt], path + (nxt,), used | {nxt})
                    )
        if not expanded:
            return fallback_order(n, prefix, parities)
        expanded.sort(key=lambda item: item[0], reverse=True)
        beams = expanded[:BEAM_WIDTH]
    return list(beams[0][1])


test_dir = find_split("test")
whisper_dir = find_model("whisper-small")
qwen_dir = find_model("qwen2.5-0.5b")
with (test_dir / "prefix.csv").open(newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 200

prefixes = {str(row["filename"]): json.loads(row["prefix"]) for row in rows}
audio_items = []
speaker_features = {}
chunk_counts = {}
for row in rows:
    filename = str(row["filename"])
    paths = sorted((test_dir / filename).glob("chunk_*.wav"), key=chunk_index)
    indices = [chunk_index(path) for path in paths]
    assert indices == list(range(len(indices)))
    chunk_counts[filename] = len(paths)
    speaker_features[filename] = []
    for path in paths:
        audio, sr = librosa.load(path, sr=16000, mono=True)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)
        feature = np.r_[
            mfcc[1:].mean(1),
            mfcc[1:].std(1),
            librosa.feature.spectral_centroid(y=audio, sr=sr).mean() / 1000,
            librosa.feature.spectral_bandwidth(y=audio, sr=sr).mean() / 1000,
        ]
        speaker_features[filename].append(feature)
        audio_items.append((filename, chunk_index(path), audio))

parities = {
    filename: balanced_speaker_labels(features, prefixes[filename])
    for filename, features in speaker_features.items()
}
print(f"loaded {len(audio_items)} chunks; feature seconds={time.monotonic() - STARTED:.1f}")

transcripts = {
    filename: [""] * chunk_counts[filename]
    for filename in prefixes
}
processor = WhisperProcessor.from_pretrained(whisper_dir, local_files_only=True)
whisper = WhisperForConditionalGeneration.from_pretrained(
    whisper_dir, dtype=torch.float16, local_files_only=True
).to(DEVICE).eval()
for start in range(0, len(audio_items), ASR_BATCH):
    batch = audio_items[start : start + ASR_BATCH]
    encoded = processor(
        [item[2] for item in batch],
        sampling_rate=16000,
        return_tensors="pt",
        return_attention_mask=True,
    )
    with torch.inference_mode():
        token_ids = whisper.generate(
            encoded.input_features.to(DEVICE, dtype=torch.float16),
            attention_mask=encoded.attention_mask.to(DEVICE),
            language="en",
            task="transcribe",
            max_new_tokens=96,
            num_beams=1,
            do_sample=False,
        )
    decoded = processor.batch_decode(token_ids, skip_special_tokens=True)
    for (filename, index, _), text in zip(batch, decoded, strict=True):
        transcripts[filename][index] = text.strip()
    if start % (ASR_BATCH * 20) == 0:
        print(f"ASR {min(start + len(batch), len(audio_items))}/{len(audio_items)}", flush=True)

del whisper, processor, audio_items
gc.collect()
torch.cuda.empty_cache()
print(f"ASR complete; elapsed seconds={time.monotonic() - STARTED:.1f}")

tokenizer = AutoTokenizer.from_pretrained(qwen_dir, local_files_only=True)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
qwen = AutoModelForCausalLM.from_pretrained(
    qwen_dir, dtype=torch.float16, local_files_only=True
).to(DEVICE).eval()


def score_edges(turns):
    examples = []
    for left, left_text in enumerate(turns):
        for right, right_text in enumerate(turns):
            if left == right:
                continue
            context = f"A: {left_text.strip()}\nB:"
            target = " " + right_text.strip() + "\n"
            context_ids = tokenizer(context, add_special_tokens=False).input_ids
            target_ids = tokenizer(target, add_special_tokens=False).input_ids
            examples.append((left, right, context_ids, target_ids))
    edges = {}
    for start in range(0, len(examples), LM_BATCH):
        if time.monotonic() > DEADLINE - 25:
            raise TimeoutError("Qwen scoring cutoff reached")
        batch = examples[start : start + LM_BATCH]
        max_len = max(len(item[2]) + len(item[3]) for item in batch)
        ids = torch.full(
            (len(batch), max_len), tokenizer.pad_token_id,
            dtype=torch.long, device=DEVICE,
        )
        attention = torch.zeros_like(ids)
        target_mask = torch.zeros_like(ids, dtype=torch.bool)
        for row_index, item in enumerate(batch):
            sequence = item[2] + item[3]
            ids[row_index, :len(sequence)] = torch.tensor(sequence, device=DEVICE)
            attention[row_index, :len(sequence)] = 1
            target_mask[row_index, len(item[2]):len(sequence)] = True
        with torch.inference_mode():
            logits = qwen(input_ids=ids, attention_mask=attention).logits[:, :-1]
            log_probs = torch.log_softmax(logits.float(), dim=-1)
            token_log_probs = log_probs.gather(2, ids[:, 1:].unsqueeze(-1)).squeeze(-1)
            scored_mask = target_mask[:, 1:]
            sums = (token_log_probs * scored_mask).sum(1).cpu().tolist()
            counts = scored_mask.sum(1).cpu().tolist()
        for item, total, count in zip(batch, sums, counts, strict=True):
            edges[item[0], item[1]] = total / (count ** LENGTH_ALPHA)
        del logits, log_probs, token_log_probs
    return edges


orders = {}
fallback_count = 0
for row_number, row in enumerate(rows):
    filename = str(row["filename"])
    n = chunk_counts[filename]
    try:
        if time.monotonic() > DEADLINE - 25:
            raise TimeoutError("global cutoff reached")
        edges = score_edges(transcripts[filename])
        order = beam_decode(n, prefixes[filename], parities[filename], edges)
    except TimeoutError:
        order = fallback_order(n, prefixes[filename], parities[filename])
        fallback_count += 1
    assert len(order) == n and sorted(order) == list(range(n))
    assert order[:2] == prefixes[filename]
    orders[filename] = order
    if row_number % 20 == 0:
        print(f"ordered {row_number + 1}/{len(rows)}", flush=True)

submission_path = Path("/kaggle/working/submission.csv")
with submission_path.open("w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["filename", "prediction"])
    for row in rows:
        filename = str(row["filename"])
        order = orders[filename]
        ranks = [0] * len(order)
        for rank, index in enumerate(order):
            ranks[index] = rank
        assert sorted(ranks) == list(range(len(order)))
        assert ranks[prefixes[filename][0]] == 0
        assert ranks[prefixes[filename][1]] == 1
        writer.writerow([filename, json.dumps(ranks, separators=(",", ":"))])

assert submission_path.is_file() and submission_path.stat().st_size > 0
print(
    f"wrote {submission_path} with {len(rows)} rows; "
    f"fallback_dialogues={fallback_count}; elapsed_seconds={time.monotonic() - STARTED:.1f}"
)
