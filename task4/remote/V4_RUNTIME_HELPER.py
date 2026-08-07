
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
