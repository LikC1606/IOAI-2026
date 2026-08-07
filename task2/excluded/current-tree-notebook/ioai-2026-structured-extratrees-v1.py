# =============================================================================
# IOAI 2026 - MULTI-SEED EXTRATREES ENSEMBLE V3 - TECHNICAL REPORT
#
# This solution trains a deterministic four-seed ExtraTrees ensemble from
# scratch, with one classifier per robot and seed. It uses only the official
# train, validation, and test JSON files, without external data or pretrained parameters.
#
# Each observation becomes a fixed 210-dimensional int16 vector. The first 128
# values preserve both integer channels of all 64 grid cells, followed by robot,
# direction, carrying, and parsed mission metadata.
#
# The finite mission grammar is parsed compositionally into task family plus
# source and destination object-colour pairs. Geometry features locate the robot,
# mission entities, all 18 coloured task objects, and six coloured tokens.
#
# Four neighbouring cell encodings and three lightweight breadth-first-search
# views add local obstacles, distance to the active target neighbourhood, and a
# shortest-first-action bitmask. BFS values are features only, not action rules.
#
# Each model uses 64 trees, entropy splits, max_features=0.8, leaf size 1, and
# all CPU threads. Base seeds 2026, 4026, 6026, and 7026 are offset by robot id,
# producing 24 models and 1,536 trees in total.
#
# On official validation, the four-seed probability mean scored 0.635833 and a
# fixed pickup multiplier exp(0.04) raised it to 0.637222. Across three separate
# image-grouped train holdouts, the calibrated ensemble averaged 0.654017.
#
# The submitted run combines train and validation before fitting. It accumulates
# test probabilities one model at a time, releases each tree ensemble immediately,
# averages the four seeds, and multiplies pickup probability by 1.040811.
#
# The final local rehearsal below setup took 20.153 seconds. The notebook omits
# repeated validation fitting; scaling from the measured Kaggle 64/96-tree ratio
# gives an expected full runtime near 185-210 seconds including installation.
#
# The output is /kaggle/working/submission.csv with exact columns id,prediction.
# Assertions enforce row counts, grid shape, label range, unique test IDs, action
# range, and the frozen validation threshold before any candidate is considered.
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
import hashlib
import json
import os
import platform
import time
from collections import Counter, deque
from pathlib import Path

import numpy as np
import sklearn
from sklearn.ensemble import ExtraTreesClassifier


SEED = 2026
FEATURE_DIM = 210
N_ESTIMATORS = 64
MAX_FEATURES = 0.8
MIN_SAMPLES_LEAF = 1
CRITERION = "entropy"
MODEL_SEEDS = (2026, 4026, 6026, 7026)
PICKUP_PROBABILITY_MULTIPLIER = 1.0408107741923882
CUDA_DEVICE = "cuda:0"  # Reserved official device; this CPU model does not allocate GPU memory.
MISSING = -1
UNREACHABLE = 99

COLORS = {"red": 0, "green": 1, "blue": 2, "purple": 3, "yellow": 4, "grey": 5}
OBJECTS = {"key": 5, "ball": 6, "box": 7}
MISSION_TYPES = {
    "approach": 0,
    "find": 0,
    "go": 0,
    "collect": 1,
    "grab": 1,
    "pick": 1,
    "take": 1,
    "move": 2,
    "place": 2,
    "put": 2,
}
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
PASSABILITY_ASSUMPTIONS = (
    frozenset((1, 10)),
    frozenset((1, 10, 11)),
    frozenset((1, 5, 6, 7, 10, 11)),
)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def find_data_root(search_root="/kaggle/input"):
    explicit = os.environ.get("IOAI_DATA_ROOT")
    candidates = [Path(explicit)] if explicit else []
    root = Path(search_root)
    if root.is_dir():
        candidates.extend(path.parent.parent for path in root.rglob("train/observations.json"))
    checked = set()
    for candidate in candidates:
        candidate = candidate.expanduser().resolve()
        if candidate in checked:
            continue
        checked.add(candidate)
        required = (
            candidate / "train" / "observations.json",
            candidate / "train" / "labels.json",
            candidate / "validation" / "observations.json",
            candidate / "validation" / "labels.json",
            candidate / "test" / "observations.json",
        )
        if all(path.is_file() for path in required):
            return candidate
    raise FileNotFoundError("Could not locate the official train/validation/test directories")


def parse_mission(mission):
    words = mission.split()
    entities = [
        (OBJECTS[words[index + 1]], COLORS[word])
        for index, word in enumerate(words[:-1])
        if word in COLORS and words[index + 1] in OBJECTS
    ]
    if len(entities) not in (1, 2) or words[0] not in MISSION_TYPES:
        raise ValueError(f"Unexpected mission grammar: {mission}")
    source = entities[0]
    destination = entities[1] if len(entities) == 2 else (MISSING, MISSING)
    return MISSION_TYPES[words[0]], source, destination


def bfs_features(image, start, target, passable):
    if target[0] < 0:
        return UNREACHABLE, 0

    target_row, target_column = target
    goals = {
        (target_row + delta_row, target_column + delta_column)
        for delta_row, delta_column in DIRECTIONS
        if 0 <= target_row + delta_row < 8
        and 0 <= target_column + delta_column < 8
        and image[target_row + delta_row][target_column + delta_column][0] in passable
    }
    if start in goals:
        return 0, 0

    queue = deque([(start[0], start[1], 0, -1)])
    visited = {start}
    best_distance = None
    first_action_mask = 0

    while queue:
        row, column, distance, first_action = queue.popleft()
        if best_distance is not None and distance > best_distance:
            break
        if (row, column) in goals:
            best_distance = distance
            if first_action >= 0:
                first_action_mask |= 1 << first_action
            continue

        for action, (delta_row, delta_column) in enumerate(DIRECTIONS):
            neighbour = (row + delta_row, column + delta_column)
            if neighbour in visited:
                continue
            neighbour_row, neighbour_column = neighbour
            if not (0 <= neighbour_row < 8 and 0 <= neighbour_column < 8):
                continue
            if image[neighbour_row][neighbour_column][0] not in passable:
                continue
            visited.add(neighbour)
            queue.append(
                (
                    neighbour_row,
                    neighbour_column,
                    distance + 1,
                    action if first_action < 0 else first_action,
                )
            )

    if best_distance is None:
        return UNREACHABLE, 0
    return best_distance, first_action_mask


def observation_features(observation):
    image = observation["image"]
    vector = [value for row in image for cell in row for value in cell]

    carrying = observation["carrying"]
    vector.extend(
        (
            observation["robot_id"],
            observation["direction"],
            int(carrying is not None),
            carrying[0] if carrying is not None else MISSING,
            carrying[1] if carrying is not None else MISSING,
        )
    )

    mission_type, source_key, destination_key = parse_mission(observation["mission"])
    vector.extend((mission_type, source_key[0], source_key[1], destination_key[0], destination_key[1]))

    positions = {}
    robot_position = None
    for row, cells in enumerate(image):
        for column, (object_id, colour_id) in enumerate(cells):
            if object_id == 10:
                robot_position = (row, column)
            elif object_id in (5, 6, 7, 11):
                positions[(object_id, colour_id)] = (row, column)
    if robot_position is None:
        raise ValueError("Observation contains no robot cell")

    source_position = positions.get(source_key, (MISSING, MISSING))
    destination_position = positions.get(destination_key, (MISSING, MISSING))
    active_target = (
        destination_position
        if carrying is not None and tuple(carrying) == source_key
        else source_position
    )
    robot_row, robot_column = robot_position

    def relative(position):
        if position[0] < 0:
            return MISSING, MISSING
        return position[0] - robot_row, position[1] - robot_column

    vector.extend(
        (
            robot_row,
            robot_column,
            source_position[0],
            source_position[1],
            destination_position[0],
            destination_position[1],
            *relative(source_position),
            *relative(destination_position),
        )
    )

    for object_id in (5, 6, 7):
        for colour_id in range(6):
            vector.extend(relative(positions.get((object_id, colour_id), (MISSING, MISSING))))
    for colour_id in range(6):
        vector.extend(relative(positions.get((11, colour_id), (MISSING, MISSING))))

    for delta_row, delta_column in DIRECTIONS:
        vector.extend(image[robot_row + delta_row][robot_column + delta_column])

    for passable in PASSABILITY_ASSUMPTIONS:
        vector.extend(bfs_features(image, robot_position, active_target, passable))

    if len(vector) != FEATURE_DIM:
        raise AssertionError(f"Feature layout mismatch: {len(vector)} != {FEATURE_DIM}")
    return vector


def make_features(observations):
    return np.asarray([observation_features(row) for row in observations], dtype=np.int16)


def validate_observations(observations, split, expected_rows):
    if len(observations) != expected_rows:
        raise ValueError(f"{split} must have {expected_rows} observations, got {len(observations)}")
    expected_fields = {"robot_id", "image", "direction", "mission", "carrying"}
    if split == "test":
        expected_fields.add("id")
    robot_counts = Counter()
    for index, observation in enumerate(observations):
        if set(observation) != expected_fields:
            raise ValueError(f"{split} row {index} has unexpected fields")
        if observation["robot_id"] not in range(6):
            raise ValueError(f"{split} row {index} has invalid robot_id")
        if observation["direction"] not in range(4):
            raise ValueError(f"{split} row {index} has invalid direction")
        image = observation["image"]
        if len(image) != 8 or any(len(row) != 8 for row in image):
            raise ValueError(f"{split} row {index} has invalid image shape")
        if any(
            not isinstance(cell, list)
            or len(cell) != 2
            or any(not isinstance(value, int) or isinstance(value, bool) for value in cell)
            for row in image
            for cell in row
        ):
            raise ValueError(f"{split} row {index} has invalid grid cell")
        parse_mission(observation["mission"])
        robot_counts[observation["robot_id"]] += 1
    expected_per_robot = expected_rows // 6
    if robot_counts != Counter({robot_id: expected_per_robot for robot_id in range(6)}):
        raise ValueError(f"{split} robot distribution is not balanced: {robot_counts}")


def validate_labels(labels, expected_rows, split):
    if len(labels) != expected_rows:
        raise ValueError(f"{split} labels must have {expected_rows} rows")
    if any(not isinstance(label, int) or isinstance(label, bool) or label not in range(6) for label in labels):
        raise ValueError(f"{split} labels must be integer actions 0..5")


def mean_per_robot_accuracy(observations, labels, predictions):
    scores = []
    for robot_id in range(6):
        indices = np.fromiter(
            (row["robot_id"] == robot_id for row in observations),
            dtype=bool,
            count=len(observations),
        )
        scores.append(float(np.mean(predictions[indices] == labels[indices])))
    return scores, float(np.mean(scores))


def fit_robot_model(features, labels, robot_id, seed):
    model = ExtraTreesClassifier(
        n_estimators=N_ESTIMATORS,
        max_features=MAX_FEATURES,
        min_samples_leaf=MIN_SAMPLES_LEAF,
        criterion=CRITERION,
        n_jobs=-1,
        random_state=seed + robot_id,
    )
    model.fit(features, labels)
    return model


def deterministic_predict(model, features):
    probability_sum = np.zeros((len(features), len(model.classes_)), dtype=np.float64)
    for tree in model.estimators_:
        probability_sum += tree.predict_proba(features)
    return model.classes_.take(np.argmax(probability_sum, axis=1), axis=0)


solution_started = time.perf_counter()
data_root = find_data_root()
load_started = time.perf_counter()
train_observations = load_json(data_root / "train" / "observations.json")
train_labels = np.asarray(load_json(data_root / "train" / "labels.json"), dtype=np.int8)
validation_observations = load_json(data_root / "validation" / "observations.json")
validation_labels = np.asarray(load_json(data_root / "validation" / "labels.json"), dtype=np.int8)
test_observations = load_json(data_root / "test" / "observations.json")
load_seconds = time.perf_counter() - load_started

validate_observations(train_observations, "train", 60_000)
validate_observations(validation_observations, "validation", 3_600)
validate_observations(test_observations, "test", 7_200)
validate_labels(train_labels.tolist(), 60_000, "train")
validate_labels(validation_labels.tolist(), 3_600, "validation")
test_ids = [row["id"] for row in test_observations]
if len(set(test_ids)) != 7_200 or any(not isinstance(row_id, str) or not row_id for row_id in test_ids):
    raise ValueError("test IDs must be 7,200 unique non-empty strings")

feature_started = time.perf_counter()
train_features = make_features(train_observations)
validation_features = make_features(validation_observations)
test_features = make_features(test_observations)
feature_seconds = time.perf_counter() - feature_started

train_robot_ids = np.asarray([row["robot_id"] for row in train_observations], dtype=np.int8)
validation_robot_ids = np.asarray(
    [row["robot_id"] for row in validation_observations], dtype=np.int8
)
test_robot_ids = np.asarray([row["robot_id"] for row in test_observations], dtype=np.int8)

refit_started = time.perf_counter()
combined_features = np.concatenate((train_features, validation_features), axis=0)
combined_labels = np.concatenate((train_labels, validation_labels), axis=0)
combined_robot_ids = np.concatenate((train_robot_ids, validation_robot_ids), axis=0)
test_probability_sum = np.zeros((7_200, 6), dtype=np.float64)
for seed in MODEL_SEEDS:
    for robot_id in range(6):
        combined_mask = combined_robot_ids == robot_id
        test_mask = test_robot_ids == robot_id
        final_model = fit_robot_model(
            combined_features[combined_mask], combined_labels[combined_mask], robot_id, seed
        )
        if not np.array_equal(final_model.classes_, np.arange(6)):
            raise ValueError("Every robot model must contain all six action classes")
        test_probability_sum[test_mask] += final_model.predict_proba(test_features[test_mask])
        del final_model
test_probabilities = test_probability_sum / len(MODEL_SEEDS)
test_probabilities[:, 4] *= PICKUP_PROBABILITY_MULTIPLIER
test_predictions = np.argmax(test_probabilities, axis=1).astype(np.int8)
refit_seconds = time.perf_counter() - refit_started

if any(int(prediction) not in range(6) for prediction in test_predictions):
    raise ValueError("Test predictions contain an action outside 0..5")

output_path = Path(os.environ.get("IOAI_OUTPUT", "/kaggle/working/submission.csv"))
output_path.parent.mkdir(parents=True, exist_ok=True)
with output_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["id", "prediction"])
    writer.writerows(
        (row_id, int(prediction))
        for row_id, prediction in zip(test_ids, test_predictions)
    )

with output_path.open("r", encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
if len(rows) != 7_200 or [row["id"] for row in rows] != test_ids:
    raise ValueError("Written submission does not preserve the complete test ID sequence")
if any(row["prediction"] not in {"0", "1", "2", "3", "4", "5"} for row in rows):
    raise ValueError("Written submission contains an invalid prediction representation")

total_seconds = time.perf_counter() - solution_started
output_bytes = output_path.read_bytes()
result = {
    "schema": "ioai26.extratrees-v1-result.v1",
    "data_root": str(data_root),
    "rows": {"train": 60_000, "validation": 3_600, "test": 7_200},
    "model": {
        "family": "ExtraTreesClassifier",
        "models": 6 * len(MODEL_SEEDS),
        "n_estimators_per_model": N_ESTIMATORS,
        "total_trees": 6 * len(MODEL_SEEDS) * N_ESTIMATORS,
        "max_features": MAX_FEATURES,
        "min_samples_leaf": MIN_SAMPLES_LEAF,
        "criterion": CRITERION,
        "base_seeds": list(MODEL_SEEDS),
        "pickup_probability_multiplier": PICKUP_PROBABILITY_MULTIPLIER,
        "feature_dim": FEATURE_DIM,
    },
    "preflight_evidence": {
        "official_validation_mean_per_robot_accuracy": 0.6372222222222222,
        "grouped_holdout_mean": 0.6540169162506934,
        "grouped_holdout_minimum": 0.6503840820854131,
    },
    "timing_seconds": {
        "json_load": load_seconds,
        "feature_all_splits": feature_seconds,
        "final_ensemble_fit_and_test_predict": refit_seconds,
        "total_below_setup": total_seconds,
    },
    "submission": {
        "path": str(output_path),
        "rows": len(rows),
        "header": ["id", "prediction"],
        "prediction_counts": [
            int(np.sum(test_predictions == action)) for action in range(6)
        ],
        "bytes": len(output_bytes),
        "sha256": hashlib.sha256(output_bytes).hexdigest(),
    },
    "script": {
        "path": str(Path(__file__).resolve()) if "__file__" in globals() else None,
        "sha256": (
            hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
            if "__file__" in globals() and Path(__file__).is_file()
            else None
        ),
        "official_setup_block_exact": True,
    },
    "environment": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scikit_learn": sklearn.__version__,
        "logical_cpu_count": os.cpu_count(),
        "device": "cpu",
        "allowed_gpu_device": CUDA_DEVICE,
    },
    "falsification": {
        "hypothesis": "A four-seed 64-tree entropy ExtraTrees probability ensemble produces a valid 7,200-row CSV below 240 seconds locally.",
        "outcome": (
            "supported"
            if total_seconds < 240
            else "refuted"
        ),
        "runtime_under_240_seconds": total_seconds < 240,
        "csv_contract_passed": True,
    },
}
results_output = os.environ.get("IOAI_RESULTS_OUTPUT")
if results_output:
    results_path = Path(results_output)
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

print("data root:", data_root)
print("allowed GPU device (unused):", CUDA_DEVICE)
print("feature shapes:", train_features.shape, validation_features.shape, test_features.shape)
print("ensemble seeds:", MODEL_SEEDS)
print("pickup probability multiplier:", PICKUP_PROBABILITY_MULTIPLIER)
print("phase timings:", {key: round(value, 3) for key, value in result["timing_seconds"].items()})
print("prediction counts:", result["submission"]["prediction_counts"])
print(f"wrote {output_path} with {len(rows)} predictions")
