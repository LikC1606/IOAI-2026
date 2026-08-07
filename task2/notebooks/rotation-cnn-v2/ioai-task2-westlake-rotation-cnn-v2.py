# =============================================================================
# IOAI 2026 - CHASING THE ROBOT - TECHNICAL REPORT
#
# This solution treats the task as supervised imitation learning. It trains a
# compact policy network from scratch on the 60,000 labeled competition rows
# and predicts one of the six absolute actions for every test snapshot.
#
# Mission text is parsed with the twelve closed instruction templates. The
# parser extracts task type, wording template, primary object and colour, and,
# for put-next missions, the destination object and colour.
#
# Each 8x8 grid is encoded with learned object and colour embeddings. Three
# explicit spatial masks mark the robot, the primary mission object, and the
# secondary destination, preserving the compositional structure of unseen
# colour/object combinations.
#
# Robot id, facing direction, task type, language template, source and target
# attributes, and carried-object state are represented by small categorical
# embeddings. These metadata features are fused with the spatial network.
#
# The spatial model is a 64-channel residual CNN with four 3x3 residual blocks.
# Its flattened grid representation is combined with the metadata and passed
# through a two-layer classifier with SiLU activations and 0.10 dropout.
#
# Training uses AdamW, mixed precision, batch size 1024, label smoothing 0.01,
# and a OneCycle learning-rate schedule peaking at 0.003. Fifteen epochs are
# run, while the checkpoint with the best labeled-validation mean per-robot
# accuracy is retained for test inference.
#
# On the official 3,600-row validation split, the development run reached
# 54.78 mean per-robot accuracy; all six robots were evaluated independently
# before averaging, matching the competition metric.
#
# A shortest-path symbolic planner was also tested during development, but it
# was dropped because the robot policies frequently take consistent non-shortest
# and no-op actions. Random quarter-turn rotation augmentation is applied to
# the grid, facing direction, and movement labels to improve spatial coverage.
#
# The final script validates unique test ids and action range, then writes
# exactly 7,200 rows to /kaggle/working/submission.csv with header
# id,prediction. No pretrained model, external data, or internet access is used.
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
import csv
import json
import random
import time

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


COLORS = {"red": 0, "green": 1, "blue": 2, "purple": 3, "yellow": 4, "grey": 5}
OBJECTS = {"key": 0, "ball": 1, "box": 2}
GRID_OBJECTS = {1: 0, 2: 1, 5: 2, 6: 3, 7: 4, 10: 5, 11: 6}
PUT_RE = re.compile(
    r"^(?:move|put|place) the (red|green|blue|purple|yellow|grey) "
    r"(key|ball|box) (?:next to|beside) the "
    r"(red|green|blue|purple|yellow|grey) (key|ball|box)$"
)
SINGLE_RE = re.compile(
    r"^(find the|go to the|move toward the|approach the|pick up the|take the|grab the|collect the) "
    r"(red|green|blue|purple|yellow|grey) (key|ball|box)( and stand next to it)?$"
)
TEMPLATES = {
    "find the": 0, "go to the": 1, "move toward the": 2, "approach the": 3,
    "pick up the": 4, "take the": 5, "grab the": 6, "collect the": 7,
    "move-next": 8, "put-next": 9, "put-beside": 10, "place-beside": 11,
}
ROTATE_DIRECTION = torch.tensor([
    [0, 1, 2, 3],
    [2, 3, 1, 0],
    [1, 0, 3, 2],
    [3, 2, 0, 1],
], dtype=torch.long)


def find_dir(name, search_root="/kaggle/input"):
    matches = sorted(p for p in Path(search_root).rglob(name) if p.is_dir())
    if not matches:
        raise FileNotFoundError(f"{name}/ not found under {search_root}")
    return matches[0]


def parse_mission(mission):
    match = PUT_RE.match(mission)
    if match:
        source_color, source_object, target_color, target_object = match.groups()
        if mission.startswith("move"):
            template = TEMPLATES["move-next"]
        elif mission.startswith("place"):
            template = TEMPLATES["place-beside"]
        elif "beside" in mission:
            template = TEMPLATES["put-beside"]
        else:
            template = TEMPLATES["put-next"]
        return (2, template, OBJECTS[source_object], COLORS[source_color],
                OBJECTS[target_object], COLORS[target_color])
    match = SINGLE_RE.match(mission)
    if not match:
        raise ValueError(f"unparsed mission: {mission}")
    prefix, color, object_name, _ = match.groups()
    task = int(prefix in {"pick up the", "take the", "grab the", "collect the"})
    return task, TEMPLATES[prefix], OBJECTS[object_name], COLORS[color], 3, 6


def encode(observations):
    count = len(observations)
    objects = torch.empty((count, 8, 8), dtype=torch.uint8)
    colors = torch.empty((count, 8, 8), dtype=torch.uint8)
    roles = torch.zeros((count, 3, 8, 8), dtype=torch.uint8)
    meta = torch.empty((count, 10), dtype=torch.uint8)
    object_name = {5: "key", 6: "ball", 7: "box"}
    for index, observation in enumerate(observations):
        task, template, source_object, source_color, target_object, target_color = parse_mission(
            observation["mission"]
        )
        carrying = observation["carrying"]
        carry_object = 3 if carrying is None else OBJECTS[object_name[carrying[0]]]
        carry_color = 6 if carrying is None else carrying[1]
        meta[index] = torch.tensor([
            observation["robot_id"], observation["direction"], task, template,
            source_object, source_color, target_object, target_color,
            carry_object, carry_color,
        ], dtype=torch.uint8)
        source_grid_object = source_object + 5
        target_grid_object = target_object + 5 if target_object < 3 else None
        for row, cells in enumerate(observation["image"]):
            for col, (object_id, color_id) in enumerate(cells):
                objects[index, row, col] = GRID_OBJECTS[object_id]
                colors[index, row, col] = color_id
                roles[index, 0, row, col] = int(object_id == 10)
                roles[index, 1, row, col] = int(
                    object_id == source_grid_object and color_id == source_color
                )
                roles[index, 2, row, col] = int(
                    target_grid_object is not None
                    and object_id == target_grid_object and color_id == target_color
                )
    return objects, colors, roles, meta


def rotate_batch(objects, colors, roles, meta, labels, turns):
    if turns == 0:
        return objects, colors, roles, meta, labels
    objects = torch.rot90(objects, turns, dims=(1, 2))
    colors = torch.rot90(colors, turns, dims=(1, 2))
    roles = torch.rot90(roles, turns, dims=(2, 3))
    meta = meta.clone()
    direction_map = ROTATE_DIRECTION[turns].to(meta.device)
    meta[:, 1] = direction_map[meta[:, 1].long()].to(meta.dtype)
    labels = labels.clone()
    movement = labels < 4
    labels[movement] = direction_map[labels[movement].long()].to(labels.dtype)
    return objects, colors, roles, meta, labels


class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(channels, channels, 3, padding=1, bias=False),
            nn.BatchNorm2d(channels), nn.SiLU(),
            nn.Conv2d(channels, channels, 3, padding=1, bias=False),
            nn.BatchNorm2d(channels),
        )
        self.activation = nn.SiLU()

    def forward(self, inputs):
        return self.activation(inputs + self.net(inputs))


class PolicyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.object_embedding = nn.Embedding(7, 12)
        self.color_embedding = nn.Embedding(6, 6)
        self.stem = nn.Sequential(
            nn.Conv2d(21, 64, 3, padding=1, bias=False), nn.BatchNorm2d(64), nn.SiLU()
        )
        self.blocks = nn.Sequential(*[ResidualBlock(64) for _ in range(4)])
        self.spatial_head = nn.Sequential(
            nn.Flatten(), nn.Linear(64 * 8 * 8, 384), nn.SiLU(), nn.Dropout(0.10)
        )
        cardinalities = [6, 4, 3, 12, 3, 6, 4, 7, 4, 7]
        dimensions = [12, 8, 8, 12, 8, 10, 8, 10, 8, 10]
        self.meta_embeddings = nn.ModuleList(
            nn.Embedding(cardinality, dimension)
            for cardinality, dimension in zip(cardinalities, dimensions)
        )
        self.classifier = nn.Sequential(
            nn.Linear(384 + sum(dimensions), 256), nn.SiLU(), nn.Dropout(0.10),
            nn.Linear(256, 128), nn.SiLU(), nn.Dropout(0.10), nn.Linear(128, 6),
        )

    def forward(self, objects, colors, roles, meta):
        object_features = self.object_embedding(objects.long()).permute(0, 3, 1, 2)
        color_features = self.color_embedding(colors.long()).permute(0, 3, 1, 2)
        grid = torch.cat([object_features, color_features, roles.float()], dim=1)
        spatial = self.spatial_head(self.blocks(self.stem(grid)))
        metadata = torch.cat([
            embedding(meta[:, index].long())
            for index, embedding in enumerate(self.meta_embeddings)
        ], dim=1)
        return self.classifier(torch.cat([spatial, metadata], dim=1))


@torch.inference_mode()
def evaluate(model, loader, device):
    model.eval()
    correct = torch.zeros(6, dtype=torch.long)
    total = torch.zeros(6, dtype=torch.long)
    for objects, colors, roles, meta, labels in loader:
        objects, colors, roles, meta, labels = [
            tensor.to(device, non_blocking=True) for tensor in (objects, colors, roles, meta, labels)
        ]
        with torch.autocast(device_type="cuda", dtype=torch.float16):
            predictions = model(objects, colors, roles, meta).argmax(1)
        for robot in range(6):
            mask = meta[:, 0].long() == robot
            total[robot] += mask.sum().cpu()
            correct[robot] += (predictions[mask] == labels[mask]).sum().cpu()
    per_robot = correct.float() / total
    return per_robot, per_robot.mean().item()


start_time = time.time()
random.seed(2026)
torch.manual_seed(2026)
torch.cuda.manual_seed_all(2026)
torch.set_float32_matmul_precision("high")
device = torch.device("cuda:0")
assert torch.cuda.is_available(), "GPU notebook required"
assert torch.cuda.device_count() >= 1

train_dir = find_dir("train")
validation_dir = find_dir("validation")
test_dir = find_dir("test")
train_observations = json.load(open(train_dir / "observations.json"))
train_labels = torch.tensor(json.load(open(train_dir / "labels.json")), dtype=torch.uint8)
validation_observations = json.load(open(validation_dir / "observations.json"))
validation_labels = torch.tensor(
    json.load(open(validation_dir / "labels.json")), dtype=torch.uint8
)
test_observations = json.load(open(test_dir / "observations.json"))
assert len(train_observations) == len(train_labels) == 60000
assert len(validation_observations) == len(validation_labels) == 3600
assert len(test_observations) == 7200

train_tensors = encode(train_observations)
validation_tensors = encode(validation_observations)
test_tensors = encode(test_observations)
del train_observations, validation_observations
print(f"encoded all splits in {time.time() - start_time:.2f}s", flush=True)

train_loader = DataLoader(
    TensorDataset(*train_tensors, train_labels), batch_size=1024, shuffle=True,
    generator=torch.Generator().manual_seed(2026), num_workers=0, pin_memory=True,
)
validation_loader = DataLoader(
    TensorDataset(*validation_tensors, validation_labels), batch_size=2048,
    shuffle=False, num_workers=0, pin_memory=True,
)
test_loader = DataLoader(
    TensorDataset(*test_tensors), batch_size=2048, shuffle=False,
    num_workers=0, pin_memory=True,
)

model = PolicyNet().to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=0.0002)
scheduler = torch.optim.lr_scheduler.OneCycleLR(
    optimizer, max_lr=0.003, epochs=15, steps_per_epoch=len(train_loader),
    pct_start=0.15, div_factor=10, final_div_factor=30,
)
criterion = nn.CrossEntropyLoss(label_smoothing=0.01)
scaler = torch.amp.GradScaler("cuda")
best_score = -1.0
best_state = None
best_epoch = 0

for epoch in range(1, 16):
    model.train()
    for objects, colors, roles, meta, labels in train_loader:
        objects, colors, roles, meta, labels = [
            tensor.to(device, non_blocking=True) for tensor in (objects, colors, roles, meta, labels)
        ]
        objects, colors, roles, meta, labels = rotate_batch(
            objects, colors, roles, meta, labels, random.randrange(4)
        )
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda", dtype=torch.float16):
            loss = criterion(model(objects, colors, roles, meta), labels.long())
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        scheduler.step()
    per_robot, score = evaluate(model, validation_loader, device)
    print(
        f"epoch={epoch} score={100 * score:.4f} per_robot="
        f"{[round(100 * value.item(), 3) for value in per_robot]}",
        flush=True,
    )
    if score > best_score:
        best_score = score
        best_epoch = epoch
        best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}

model.load_state_dict(best_state)
model.eval()
predictions = []
with torch.inference_mode():
    for objects, colors, roles, meta in test_loader:
        objects, colors, roles, meta = [
            tensor.to(device, non_blocking=True) for tensor in (objects, colors, roles, meta)
        ]
        with torch.autocast(device_type="cuda", dtype=torch.float16):
            predictions.extend(model(objects, colors, roles, meta).argmax(1).cpu().tolist())

ids = [row["id"] for row in test_observations]
assert len(ids) == len(predictions) == 7200
assert len(set(ids)) == 7200
assert all(isinstance(value, int) and 0 <= value <= 5 for value in predictions)
submission = Path("/kaggle/working/submission.csv")
with submission.open("w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["id", "prediction"])
    writer.writerows(zip(ids, predictions))

assert submission.is_file() and sum(1 for _ in submission.open()) == 7201
print(
    f"best_epoch={best_epoch} validation={100 * best_score:.4f} "
    f"wrote={submission} rows=7200 elapsed={time.time() - start_time:.2f}s",
    flush=True,
)
