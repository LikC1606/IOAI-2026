# =============================================================================
# IOAI 2026 - AI Models Track - Double Agent Dilemma
# TECHNICAL REPORT
# =============================================================================
#
# 1. SUMMARY
#    This submission loads the two supplied frozen ImageNet classifiers and
#    generates one raw-resolution Type A and one Type B perturbation for every
#    leaderboard image. On the 100-image labeled confirmation split, the local
#    exact-transform check reached 100/100 successes for both types; the
#    unlabeled leaderboard-image consensus proxy also reached 100/100 for both.
#    The first two remote versions scored 98.23 and 98.36. Both scores are
#    consistent with all public attack conditions succeeding; this version
#    combines the finer quantizer from version 2 with norm refinement.
#
# 2. APPROACH
#    The task is treated as constrained per-image optimization rather than
#    training a new predictor. The clean R/V consensus supplies the class y.
#    Type A minimizes the ViT true-class margin while protecting the ResNet
#    margin; Type B swaps the models. This directly matches the evaluator's
#    binary condition and uses no information beyond the permitted checkpoints
#    and image.
#
# 3. ATTACK DETAILS
#    Each attack starts with zero delta and runs at most 100 normalized
#    gradient steps. The step is 1e-4 RMS pixel amplitude, with a 1e-2 RMS
#    projection radius. The loss is the attacked-model true-vs-best-other
#    logit margin plus 2.0 times a hinge on the protected margin below 0.02.
#    Once a valid flip is found, a ten-iteration scalar backtrack finds a
#    smaller point on that direction. Eight norm-shrink/linearized-projection
#    refinement steps then rotate it toward a lower-norm feasible point. A
#    fine power-of-two quantizer (2^-14 through 2^-24) retains a 0.01
#    attacked-margin buffer.
#
# 4. NORM CONTROL
#    Updates are normalized by the raw tensor RMS and projected in an RMS ball,
#    then clipped through the same [0,1] operation used by the evaluator. The
#    resulting confirmation RMS averages were about 4.8e-4 (Type A) and 5.7e-4
#    (Type B). Per-image quantization retained all 400 leaderboard-proxy attack
#    conditions and reduced the local CSV from 644 MB to 74 MB. On the full
#    labeled confirmation cell, refinement retained 200/200 conditions while
#    reducing mean RMS by about 2-3% for Type A and 1-2% for Type B. Version 2
#    established that fine quantization improves the remote norm score. The
#    complete candidate measured mean L2/N 6.5833e-7 and a corrected public
#    penalty proxy of 98.40.
#
# 5. RESOLUTION HANDLING
#    The optimization variable has shape 3 x H x W from the original PNG. Every
#    forward and backward pass applies differentiable bilinear Resize(256) and
#    CenterCrop(224) before normalization. The final tensor is never resized to
#    224 for output; it is encoded in its original shape.
#
# 6. VALIDATION
#    I measured exact argmax conditions and per-tensor RMS on train and
#    test_public, keeping the public labels only for validation. Both models
#    were clean-correct and agreeing. I also ran a separate development proxy
#    on both unlabeled leaderboard folders using their clean model consensus;
#    it is evidence of interface/shift transfer, not a hidden-label score. The
#    98.23 public score revealed that the evaluator sums the two per-image norm
#    terms before averaging; version 2 then improved to 98.36 with finer
#    quantization. Neither result implies a public attack failure.
#
# 7. WHAT DID NOT WORK
#    The starter's constant noise was only an interface sanity check and did
#    not create model-specific flips. Untargeted projected gradients without a
#    protected-model hinge could invalidate both conditions, so that route was
#    dropped in favor of the dual-margin objective and boundary backtracking.
#    A top-5 linearized DeepFool probe preserved success but used larger norms.
#
# 8. KNOWN WEAKNESSES
#    The hidden labels are unavailable, so the method relies on the organizer's
#    stated clean 100% accuracy and consensus. A rare clean disagreement or a
#    different evaluator interpolation implementation would reduce transfer;
#    the protected-margin buffer is the mitigation. The refinement is a local
#    linear approximation and therefore stops whenever it cannot verify a
#    smaller feasible point. Private labels remain unavailable.
#
# 9. RUNTIME
#    The first T4 notebook completed in about 213 seconds. The complete refined
#    body took 161 seconds on one local H100, including fine quantization and
#    writing its 190 MB output. Eight refinement steps keep the extrapolated
#    one-cuda:0 T4 path below the 600-second cap, including offline setup.
#
# 10. REPRODUCIBILITY
#    Seeds are fixed at 42 for Python/NumPy/PyTorch. There are no random attack
#    operations; cuDNN benchmark mode is used for runtime, so low-level floating
#    point order may vary by device. Every candidate is rechecked before output.
#    Models come only from competition data; no network/external artifacts exist.
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

# Kaggle imports Pillow while starting its notebook kernel. The exact
# IOAI header above replaces Pillow on disk, so the official solution must
# run in a fresh interpreter to load one consistent native-library version.
_RUNTIME_PATH = Path('/kaggle/working/ioai_double_agent_runtime.py')
_RUNTIME_PATH.write_text('# ─── Double Agent competition path discovery ───\n# Kaggle mounts competition files below /kaggle/input, while the original\n# Yandex notebook expects DATA_DIR and MODELS_DIR. This changes paths only;\n# dependency initialization above is copied verbatim from the example starter.\nimport os\nfrom pathlib import Path\n\n\ndef _configure_double_agent_paths(search_root="/kaggle/input"):\n    roots = []\n    for checkpoint in sorted(Path(search_root).rglob("data/models/resnet18.pth")):\n        root = checkpoint.parent.parent\n        if (\n            (root / "dataset").is_dir()\n            and (root / "models" / "vit_tiny_patch16_224.safetensors").is_file()\n        ):\n            roots.append(root)\n    if len(roots) != 1:\n        raise FileNotFoundError(f"Expected one Double Agent data root, found {roots}")\n    os.environ["DATA_DIR"] = str(roots[0] / "dataset")\n    os.environ["MODELS_DIR"] = str(roots[0] / "models")\n    print(f"Double Agent data root: {roots[0]}")\n\n\n_configure_double_agent_paths()\n# ───────────────────────────────────────────────\n\n# ─── Original solution.ipynb implementation cells ───\n\nimport sys\nfrom pathlib import Path\nimport numpy as np\nimport torch\nimport torchvision.transforms as T\nimport torchvision.transforms.functional as TF\nfrom PIL import Image\nfrom tqdm.auto import tqdm\nimport os\n\n\n### PLEASE DO NOT CHANGE THESE VARIABLES ###\nTRAIN_SPLIT = os.environ.get("TRAIN_SPLIT", "train")\nTEST_SPLIT = os.environ.get("TEST_SPLIT", "test_public")\nMODELS_ROOT = Path(os.environ.get("MODELS_DIR", "models"))\nDATASET_ROOT = Path(os.environ.get("DATA_DIR", "dataset"))\n\nSEED = 42\nnp.random.seed(SEED)\ntorch.manual_seed(SEED)\nDEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")\nprint("Device:", DEVICE)\n\nimport json\n\ndef load_split(split: str):\n    """Load a dataset split (e.g. \'train\', \'test_public.\').\n\n    Reads from dataset/<split>/ if present, otherwise extracts dataset/<split>.tar.gz.\n    """\n    split_dir = DATASET_ROOT / split\n    if not split_dir.exists():\n        raise FileNotFoundError(\n            f"Dataset split \'{split}\' not found in {DATASET_ROOT}. "\n            "Please make sure to extract the dataset first."\n        )\n\n    labels_path = split_dir / "labels.json"\n    if not labels_path.exists():\n        raise FileNotFoundError(\n            f"labels.json not found in {split_dir}."\n        )\n\n    with open(labels_path) as f:\n        labels = json.load(f)\n\n    images_dir = split_dir / "images"\n    items = []\n    for idx_str, label in sorted(labels.items(), key=lambda x: int(x[0])):\n        idx = int(idx_str)\n        image_path = images_dir / f"{idx:04d}.png"\n        items.append({"idx": idx, "image_path": image_path, "label": label})\n\n    return items\n\ntrain_data = load_split(TRAIN_SPLIT)\ntest_data = load_split(TEST_SPLIT)\n\nprint(f"train : {len(train_data)} images")\nprint(f"test  : {len(test_data)} images")\n\nsample = train_data[0]\nimg0 = Image.open(sample["image_path"]).convert("RGB")\nprint(f"\\nExample item: idx={sample[\'idx\']}  label={sample[\'label\']}  size={img0.size} (W×H)")\n\nimport timm\nimport torch\nfrom torchvision import models\n\nresnet = models.resnet18(weights=None)\nresnet.load_state_dict(torch.load(MODELS_ROOT / "resnet18.pth", map_location="cpu"))\nresnet = resnet.to(DEVICE).eval()\n\n# custom_load=False is required: this cfg has custom_load=True (the augreg\n# weights were originally JAX .npz) and on the file= path timm honours it,\n# feeding our safetensors to np.load. Plain pretrained=True escapes this only\n# because the hf-hub path checks for custom_load == \'hf\' instead.\nvit = timm.create_model(\n    "vit_tiny_patch16_224",\n    pretrained=True,\n    pretrained_cfg_overlay=dict(\n        file=MODELS_ROOT / "vit_tiny_patch16_224.safetensors",\n        custom_load=False,\n    ),\n).to(DEVICE).eval()\n\nfor p in list(resnet.parameters()) + list(vit.parameters()):\n    p.requires_grad = False\n\n_MEAN = torch.tensor([0.485, 0.456, 0.406], device=DEVICE).view(3, 1, 1)\n_STD = torch.tensor([0.229, 0.224, 0.225], device=DEVICE).view(3, 1, 1)\n\ndef preprocess(img_tensor):\n    """Raw [0,1] CxHxW tensor -> normalized 3x224x224 (matches the grader transform)."""\n    img = TF.resize(img_tensor, size=256, interpolation=T.InterpolationMode.BILINEAR)\n    img = TF.center_crop(img, output_size=224)\n    return (img - _MEAN) / _STD\n\n@torch.no_grad()\ndef predict(img_tensor):\n    inp = preprocess(img_tensor).unsqueeze(0)\n    return int(resnet(inp).argmax(1)), int(vit(inp).argmax(1))\n\nimg_t = TF.to_tensor(img0).to(DEVICE)\nr_pred, v_pred = predict(img_t)\nprint(f"True label     : {sample[\'label\']}")\nprint(f"ResNet18 (Rex) : {r_pred}  {\'✓\' if r_pred == sample[\'label\'] else \'✗\'}")\nprint(f"ViT-Tiny (Vita): {v_pred}  {\'✓\' if v_pred == sample[\'label\'] else \'✗\'}")\n\nimport torch\nimport torchvision.transforms as T\nfrom PIL import Image\nfrom tqdm import tqdm\n\nimport random\nimport numpy as np\n\nseed = 42\n\nrandom.seed(seed)\nnp.random.seed(seed)\ntorch.manual_seed(seed)\ntorch.cuda.manual_seed(seed)\ntorch.cuda.manual_seed_all(seed)\n\n# Ensures deterministic behavior\ntorch.backends.cudnn.deterministic = True\ntorch.backends.cudnn.benchmark = False\n\nEPSILON = 0.0001\n\n\nclass Solution:\n    """Baseline solution: naive constant-noise perturbation."""\n\n    def __init__(self):\n        pass\n\n    def _generate_naive_noise(self, img_tensor):\n        mean_rgb = img_tensor.mean()\n        return torch.full_like(img_tensor, mean_rgb * EPSILON)\n\n    def run(self, data):\n        """Return (preds, targets).\n\n        preds:   list of (delta_a, delta_b) tensors\n        targets: data (list of {\'idx\', \'image_path\', \'label\'})\n        """\n        preds = []\n        for item in tqdm(data, desc="Generating naive perturbations"):\n            img = Image.open(item["image_path"]).convert("RGB")\n            img_tensor = T.functional.to_tensor(img)\n            delta = self._generate_naive_noise(img_tensor)\n            preds.append((delta, delta))\n        return preds, data\n\n# ─── Kaggle submission adapter ───────────────────────────────────────────────\n# The Yandex runner accepted submission.zip. This Kaggle Code Competition uses\n# a standard submission.csv. Each payload is zlib-compressed contiguous float32\n# tensor bytes encoded as base64; the trusted metric derives the expected shape\n# from the clean image and recomputes every prediction and norm itself.\nimport base64\nimport csv\nimport zlib\n\n\ndef load_unlabeled_split(split):\n    images_dir = DATASET_ROOT / split / "images"\n    if not images_dir.is_dir():\n        raise FileNotFoundError(f"Leaderboard images not found: {images_dir}")\n    items = []\n    for image_path in sorted(images_dir.glob("*.png")):\n        try:\n            idx = int(image_path.stem)\n        except ValueError as exc:\n            raise ValueError(f"Invalid leaderboard image name: {image_path.name}") from exc\n        items.append({"idx": idx, "image_path": image_path, "label": None})\n    if not items or len({item["idx"] for item in items}) != len(items):\n        raise ValueError(f"Leaderboard split {split!r} is empty or has duplicate ids")\n    return items\n\n\ndef encode_delta(delta, expected_shape, row_id, tag):\n    if not isinstance(delta, torch.Tensor) or tuple(delta.shape) != tuple(expected_shape):\n        raise ValueError(\n            f"{row_id} {tag} has shape {getattr(delta, \'shape\', None)}, "\n            f"expected {tuple(expected_shape)}"\n        )\n    delta = delta.detach().to(device="cpu", dtype=torch.float32).contiguous()\n    if not bool(torch.isfinite(delta).all()):\n        raise ValueError(f"{row_id} {tag} contains NaN or infinity")\n    raw = delta.numpy().tobytes(order="C")\n    return base64.b64encode(zlib.compress(raw, level=6)).decode("ascii")\n\n\nsolver = Solution()\nsubmission_rows = []\nfor split_code, split_name in (\n    ("a", "test_leaderboard_a"),\n    ("b", "test_leaderboard_b"),\n):\n    split_items = load_unlabeled_split(split_name)\n    split_predictions, returned_items = solver.run(split_items)\n    if len(split_predictions) != len(split_items) or len(returned_items) != len(split_items):\n        raise ValueError(f"Solution returned the wrong row count for {split_name}")\n    for (delta_a, delta_b), item in zip(split_predictions, returned_items):\n        with Image.open(item["image_path"]) as image:\n            width, height = image.convert("RGB").size\n        expected_shape = (3, height, width)\n        row_id = f"{split_code}_{item[\'idx\']}"\n        submission_rows.append(\n            (\n                row_id,\n                encode_delta(delta_a, expected_shape, row_id, "delta_a"),\n                encode_delta(delta_b, expected_shape, row_id, "delta_b"),\n            )\n        )\n\nexpected_ids = [f"a_{idx}" for idx in range(100)] + [f"b_{idx}" for idx in range(100)]\nactual_ids = [row[0] for row in submission_rows]\nif actual_ids != expected_ids:\n    raise ValueError(f"Unexpected leaderboard ids: {actual_ids[:5]} ... {actual_ids[-5:]}")\n\nSUBMISSION = Path("/kaggle/working/submission.csv")\nSUBMISSION.parent.mkdir(parents=True, exist_ok=True)\ntemporary = SUBMISSION.with_suffix(".csv.tmp")\nwith temporary.open("w", newline="") as handle:\n    writer = csv.writer(handle)\n    writer.writerow(["id", "delta_a", "delta_b"])\n    writer.writerows(submission_rows)\ntemporary.replace(SUBMISSION)\n\nassert SUBMISSION.is_file() and SUBMISSION.stat().st_size > 0\nprint(\n    f"wrote {SUBMISSION} with {len(submission_rows)} rows "\n    f"({SUBMISSION.stat().st_size / 2**20:.2f} MiB)"\n)\n# ─────────────────────────────────────────────────────────────────────────────\n')
# Replace the illustrative starter body above with the submitted solver.  The
# fresh interpreter is retained because Kaggle preloads Pillow before setup.
_RUNTIME_PATH.write_text(r'''
import base64
import csv
import os
import random
import zlib
from pathlib import Path

import numpy as np
import torch
import torchvision.transforms as T
import torchvision.transforms.functional as TF
from PIL import Image
from torchvision import models
import timm


def locate_data_root(search_root="/kaggle/input"):
    roots = []
    for checkpoint in sorted(Path(search_root).rglob("data/models/resnet18.pth")):
        root = checkpoint.parent.parent
        if ((root / "dataset").is_dir()
                and (root / "models" / "vit_tiny_patch16_224.safetensors").is_file()):
            roots.append(root)
    if len(roots) != 1:
        raise FileNotFoundError("expected one competition data root, found %s" % roots)
    return roots[0]


ROOT = locate_data_root()
DATASET_ROOT = ROOT / "dataset"
MODELS_ROOT = ROOT / "models"
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.deterministic = False
torch.backends.cudnn.benchmark = True
print("Double Agent root:", ROOT)
print("Device:", DEVICE)


R = models.resnet18(weights=None)
R.load_state_dict(torch.load(MODELS_ROOT / "resnet18.pth", map_location="cpu"))
R = R.to(DEVICE).eval()
V = timm.create_model(
    "vit_tiny_patch16_224",
    pretrained=True,
    pretrained_cfg_overlay=dict(
        file=MODELS_ROOT / "vit_tiny_patch16_224.safetensors",
        custom_load=False,
    ),
).to(DEVICE).eval()
for parameter in list(R.parameters()) + list(V.parameters()):
    parameter.requires_grad_(False)

MEAN = torch.tensor([0.485, 0.456, 0.406], device=DEVICE).view(1, 3, 1, 1)
STD = torch.tensor([0.229, 0.224, 0.225], device=DEVICE).view(1, 3, 1, 1)
MAX_STEPS = 100
STEP_RMS = 1.0e-4
RADIUS_RMS = 1.0e-2
PROTECT_WEIGHT = 2.0
PROTECT_FLOOR = 2.0e-2
ATTACK_FLOOR = 1.0e-2
LINE_STEPS = 10
REFINE_STEPS = 8
QUANTA = [2.0 ** -power for power in range(14, 25)]
QUANT_SCALES = [1.0, 1.03125, 1.0625, 1.125, 1.25]


def preprocess(image):
    if image.ndim == 3:
        image = image.unsqueeze(0)
    image = TF.resize(image, size=256, interpolation=T.InterpolationMode.BILINEAR)
    image = TF.center_crop(image, output_size=224)
    return (image - MEAN) / STD


def class_margin(logits, label):
    true_logit = logits[:, label]
    other = logits.clone()
    other[:, label] = -torch.inf
    return true_logit - other.max(dim=1).values


@torch.no_grad()
def evaluate_margins(image, label):
    logits_r = R(preprocess(image))
    logits_v = V(preprocess(image))
    return float(class_margin(logits_r, label)), float(class_margin(logits_v, label))


def infer_label(image):
    with torch.no_grad():
        z = preprocess(image)
        pred_r = int(R(z).argmax(dim=1).item())
        pred_v = int(V(z).argmax(dim=1).item())
    # The competition guarantees clean agreement/correctness. Keeping a
    # deterministic fallback avoids aborting the whole notebook on a malformed
    # outlier while preserving the stated inference boundary.
    if pred_r != pred_v:
        print("WARNING: clean model disagreement", pred_r, pred_v)
    return pred_r


def make_attack(image, label, kind):
    """Return a finite raw-resolution delta satisfying one type, or zero."""
    delta = torch.zeros_like(image, requires_grad=True)
    for iteration in range(MAX_STEPS):
        transformed = preprocess((image + delta).clamp(0.0, 1.0))
        logits_r = R(transformed)
        logits_v = V(transformed)
        margin_r = class_margin(logits_r, label)
        margin_v = class_margin(logits_v, label)
        if kind == "A":
            attacked, protected = margin_v, margin_r
        else:
            attacked, protected = margin_r, margin_v
        objective = attacked + PROTECT_WEIGHT * torch.relu(PROTECT_FLOOR - protected)
        (gradient,) = torch.autograd.grad(objective, delta)
        with torch.no_grad():
            gradient_scale = gradient.square().mean().sqrt().clamp_min(1.0e-12)
            delta -= STEP_RMS * gradient / gradient_scale
            current_rms = delta.square().mean().sqrt()
            if current_rms > RADIUS_RMS:
                delta.mul_(RADIUS_RMS / current_rms)
            delta.copy_((image + delta).clamp(0.0, 1.0) - image)
            new_r, new_v = evaluate_margins((image + delta).clamp(0.0, 1.0), label)
            new_attacked, new_protected = ((new_v, new_r) if kind == "A"
                                           else (new_r, new_v))
            if new_attacked < -ATTACK_FLOOR and new_protected > PROTECT_FLOOR:
                # A scalar line search along the found direction removes PGD
                # overshoot and is cheap compared with another backward pass.
                direction = delta.detach().clone()
                lo, hi = 0.0, 1.0
                for _ in range(LINE_STEPS):
                    mid = (lo + hi) * 0.5
                    trial = (image + mid * direction).clamp(0.0, 1.0)
                    tr, tv = evaluate_margins(trial, label)
                    ta, tp = ((tv, tr) if kind == "A" else (tr, tv))
                    if ta < -ATTACK_FLOOR and tp > PROTECT_FLOOR:
                        hi = mid
                    else:
                        lo = mid
                result = (image + hi * direction).clamp(0.0, 1.0) - image
                rr, vv = evaluate_margins((image + result).clamp(0.0, 1.0), label)
                if ((vv < -ATTACK_FLOOR and rr > PROTECT_FLOOR) if kind == "A"
                        else (rr < -ATTACK_FLOOR and vv > PROTECT_FLOOR)):
                    return result.detach()
                break
        delta.grad = None
    return torch.zeros_like(image)


def refine_attack(image, label, kind, initial):
    """Reduce RMS by shrinking and projecting onto linearized constraints."""
    if not bool(initial.any()):
        return initial
    best = initial.detach().clone()
    best_rms = float(best.square().mean().sqrt())
    for _ in range(REFINE_STEPS):
        delta = (0.98 * best).detach().requires_grad_(True)
        for _ in range(2):
            transformed = preprocess((image + delta).clamp(0.0, 1.0))
            margin_r = class_margin(R(transformed), label)
            margin_v = class_margin(V(transformed), label)
            attacked, protected = ((margin_v, margin_r) if kind == "A"
                                   else (margin_r, margin_v))
            corrections = []
            if float(attacked.detach()) > -ATTACK_FLOOR:
                (gradient,) = torch.autograd.grad(attacked, delta, retain_graph=True)
                violation = attacked.detach() + ATTACK_FLOOR
                corrections.append(
                    -1.05 * violation * gradient /
                    gradient.square().sum().clamp_min(1.0e-20))
            if float(protected.detach()) < PROTECT_FLOOR:
                (gradient,) = torch.autograd.grad(protected, delta)
                violation = PROTECT_FLOOR - protected.detach()
                corrections.append(
                    1.05 * violation * gradient /
                    gradient.square().sum().clamp_min(1.0e-20))
            if not corrections:
                break
            with torch.no_grad():
                candidate = delta.detach() + sum(corrections)
                candidate = (image + candidate).clamp(0.0, 1.0) - image
            delta = candidate.detach().requires_grad_(True)
        candidate = delta.detach()
        margin_r, margin_v = evaluate_margins(
            (image + candidate).clamp(0.0, 1.0), label)
        attacked, protected = ((margin_v, margin_r) if kind == "A"
                               else (margin_r, margin_v))
        candidate_rms = float(candidate.square().mean().sqrt())
        if (attacked < -ATTACK_FLOOR and protected > PROTECT_FLOOR
                and candidate_rms < best_rms):
            best, best_rms = candidate, candidate_rms
        else:
            break
    return best


@torch.no_grad()
def quantize_attack(image, label, kind, delta):
    """Choose the coarsest low-entropy delta that remains evaluator-valid."""
    if not bool(delta.any()):
        return delta
    for quantum in QUANTA:
        levels = torch.round(delta / quantum)
        if not bool(levels.any()):
            continue
        for scale in QUANT_SCALES:
            candidate = levels * (quantum * scale)
            margin_r, margin_v = evaluate_margins(
                (image + candidate).clamp(0.0, 1.0), label)
            if kind == "A":
                valid = margin_v < -ATTACK_FLOOR and margin_r > PROTECT_FLOOR
            else:
                valid = margin_r < -ATTACK_FLOOR and margin_v > PROTECT_FLOOR
            if valid:
                return candidate
    return delta


def load_unlabeled(split):
    images_dir = DATASET_ROOT / split / "images"
    paths = sorted(images_dir.glob("*.png"))
    if len(paths) != 100:
        raise ValueError("expected 100 images in %s, found %d" % (split, len(paths)))
    items = []
    for path in paths:
        if int(path.stem) != len(items):
            raise ValueError("non-contiguous image ids in %s" % split)
        with Image.open(path) as image:
            tensor = TF.to_tensor(image.convert("RGB")).to(DEVICE)
        items.append((int(path.stem), tensor))
    return items


def encode_delta(delta, shape, row_id, tag):
    if tuple(delta.shape) != tuple(shape):
        raise ValueError("%s %s has shape %s, expected %s" %
                         (row_id, tag, tuple(delta.shape), tuple(shape)))
    delta = delta.detach().to(device="cpu", dtype=torch.float32).contiguous()
    if not bool(torch.isfinite(delta).all()):
        raise ValueError("%s %s is non-finite" % (row_id, tag))
    return base64.b64encode(zlib.compress(delta.numpy().tobytes(order="C"), 6)).decode("ascii")


rows = []
for split_code, split_name in (("a", "test_leaderboard_a"), ("b", "test_leaderboard_b")):
    for index, image in load_unlabeled(split_name):
        label = infer_label(image)
        delta_a = make_attack(image, label, "A")
        delta_b = make_attack(image, label, "B")
        delta_a = refine_attack(image, label, "A", delta_a)
        delta_b = refine_attack(image, label, "B", delta_b)
        delta_a = quantize_attack(image, label, "A", delta_a)
        delta_b = quantize_attack(image, label, "B", delta_b)
        shape = tuple(image.shape)
        row_id = "%s_%d" % (split_code, index)
        rows.append((row_id, encode_delta(delta_a, shape, row_id, "delta_a"),
                     encode_delta(delta_b, shape, row_id, "delta_b")))
        if len(rows) % 10 == 0:
            print("completed", len(rows), "of 200 rows", flush=True)

expected = ["a_%d" % i for i in range(100)] + ["b_%d" % i for i in range(100)]
if [row[0] for row in rows] != expected:
    raise ValueError("leaderboard IDs are not in required order")
output = Path("/kaggle/working/submission.csv")
output.parent.mkdir(parents=True, exist_ok=True)
temporary = output.with_suffix(".csv.tmp")
with temporary.open("w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["id", "delta_a", "delta_b"])
    writer.writerows(rows)
temporary.replace(output)
print("wrote", output, "with", len(rows), "rows", output.stat().st_size, "bytes")
''')
subprocess.check_call([sys.executable, str(_RUNTIME_PATH)])
