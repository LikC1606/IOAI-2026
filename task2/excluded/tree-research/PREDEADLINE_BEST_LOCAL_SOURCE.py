# =============================================================================
# IOAI 2026 - Chasing the Robot - TECHNICAL REPORT
#
# This submission performs supervised next-action imitation from the 60,000
# labeled training snapshots. It treats each row independently, matching the
# competition data boundary, and trains all learned parameters from scratch.
#
# Mission text is parsed into one of three task families and one or two typed,
# colored targets. This removes dependence on exact wording while preserving
# the compositional color-object combinations that can change at test time.
#
# Each grid becomes 532 deterministic features. They include symbolic cell
# channels, robot identity and direction, carrying state, target-relative
# geometry, adjacent-cell contents, pickup/drop conditions, and BFS distances.
#
# Two BFS views are used for each target: one treats unnamed tokens as blockers
# and one permits them. This lets the model infer each robot's learned handling
# of obstacles instead of forcing a single shortest-path assumption.
#
# The classifier is an ExtraTrees ensemble. A 220-tree shared policy learns
# behavior common to all robots, while six 180-tree experts learn stable robot-
# specific deviations. Their class probabilities are blended 0.35/0.65.
#
# Models use unweighted multiclass training because train, validation, and test
# contain equal row counts per robot and the official metric averages robot
# accuracies. No validation or test row is used to fit any learned operation.
#
# On the organizer validation split, the exact model scored 0.546944 mean
# per-robot accuracy, equivalent to 54.6944 on the leaderboard's 0-100 scale.
# Its measured local end-to-end candidate runtime was 39.4 seconds.
#
# A per-robot-majority baseline scored 0.218056. Published BabyAI-style FiLM
# models were considered, but this first artifact uses structured tree features
# for lower runtime and stronger explicit compositional grounding.
#
# The final script fits on train only, predicts all 7,200 test ids, checks that
# predictions are integer actions 0-5 and ids are unique, then atomically writes
# /kaggle/working/submission.csv with the exact id,prediction header.
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
from collections import deque

import numpy as np
from sklearn.ensemble import ExtraTreesClassifier


COLORS = {"red": 0, "green": 1, "blue": 2, "purple": 3, "yellow": 4, "grey": 5}
OBJECTS = {"key": 5, "ball": 6, "box": 7}
OBJECT_VALUES = (1, 2, 5, 6, 7, 10, 11)
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def load_json(path):
    with path.open() as handle:
        return json.load(handle)


def resolve_data_root(payload):
    data_roots = []
    project_roots = []

    def visit(value, key=""):
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                visit(child_value, str(child_key))
        elif isinstance(value, list):
            for child in value:
                visit(child, key)
        elif isinstance(value, str):
            lowered = key.lower()
            if lowered == "data_root" or lowered.endswith("_data_root"):
                data_roots.append(Path(value))
            elif lowered == "project_root" or lowered.endswith("_project_root"):
                project_roots.append(Path(value))

    visit(payload)
    candidates = []
    for data_root in data_roots:
        candidates.extend([data_root, data_root / "data"])
        for project_root in project_roots:
            candidates.extend([project_root / data_root, project_root / data_root / "data"])
    for project_root in project_roots:
        candidates.append(project_root / "data" / "official" / "data")

    for candidate in candidates:
        if (candidate / "train" / "observations.json").is_file():
            return candidate
    raise FileNotFoundError("attempt input did not provide a usable official data root")


def parse_mission(mission):
    if mission.startswith(("put ", "place ", "move the ")):
        family = 2
    elif mission.startswith(("pick up ", "grab ", "take ", "collect ")):
        family = 1
    else:
        family = 0

    tokens = mission.split()
    pairs = []
    for index, token in enumerate(tokens[:-1]):
        if token in COLORS and tokens[index + 1] in OBJECTS:
            pairs.append((OBJECTS[tokens[index + 1]], COLORS[token]))
    if not pairs:
        raise ValueError(f"could not parse mission: {mission}")
    first = pairs[0]
    second = pairs[1] if len(pairs) > 1 else (-1, -1)

    prefixes = (
        "go to ", "approach ", "move toward ", "find ",
        "pick up ", "grab ", "take ", "collect ",
        "put ", "place ", "move the ",
    )
    template = next((i for i, prefix in enumerate(prefixes) if mission.startswith(prefix)), len(prefixes))
    connector = int(" beside " in mission)
    return family, first, second, template, connector


def one_hot(value, size):
    return [float(value == index) for index in range(size)]


def positions_matching(objects, colors, target):
    object_id, color_id = target
    if object_id < 0:
        return []
    return [
        (row, column)
        for row in range(1, 7)
        for column in range(1, 7)
        if objects[row, column] == object_id and colors[row, column] == color_id
    ]


def distance_map(objects, goals, allow_tokens):
    distance = np.full((8, 8), 99, dtype=np.int16)
    queue = deque()
    for row, column in goals:
        if distance[row, column] != 0:
            distance[row, column] = 0
            queue.append((row, column))
    while queue:
        row, column = queue.popleft()
        next_distance = int(distance[row, column]) + 1
        for dr, dc in DIRECTIONS:
            nr, nc = row + dr, column + dc
            value = int(objects[nr, nc])
            walkable = value in (1, 10) or (allow_tokens and value == 11)
            if walkable and next_distance < distance[nr, nc]:
                distance[nr, nc] = next_distance
                queue.append((nr, nc))
    return distance


def adjacent_walkable(objects, targets, allow_tokens):
    goals = set()
    for row, column in targets:
        for dr, dc in DIRECTIONS:
            nr, nc = row + dr, column + dc
            value = int(objects[nr, nc])
            if value in (1, 10) or (allow_tokens and value == 11):
                goals.add((nr, nc))
    return sorted(goals)


def target_geometry(robot, targets):
    if not targets:
        return [0.0] * 13
    rr, rc = robot
    relative = [(row - rr, column - rc) for row, column in targets]
    nearest = min(relative, key=lambda pair: (abs(pair[0]) + abs(pair[1]), abs(pair[0]), pair[0], pair[1]))
    distances = [abs(dr) + abs(dc) for dr, dc in relative]
    return [
        float(len(targets)), float(nearest[0]), float(nearest[1]),
        float(abs(nearest[0])), float(abs(nearest[1])), float(sum(map(abs, nearest))),
        float(nearest[0] < 0), float(nearest[0] > 0),
        float(nearest[1] < 0), float(nearest[1] > 0),
        float(min(distances)), float(max(distances)), float(sum(distances) / len(distances)),
    ]


def directional_distances(distance, robot):
    rr, rc = robot
    values = [float(distance[rr, rc])]
    for dr, dc in DIRECTIONS:
        values.append(float(distance[rr + dr, rc + dc]))
    return values


def extract_features(observation):
    image = np.asarray(observation["image"], dtype=np.int16)
    objects = image[:, :, 0]
    colors = image[:, :, 1]
    robot_location = np.argwhere(objects == 10)
    if len(robot_location) != 1:
        raise ValueError("each grid must contain one robot")
    robot = tuple(int(value) for value in robot_location[0])
    rr, rc = robot

    family, target_a, target_b, template, connector = parse_mission(observation["mission"])
    targets_a = positions_matching(objects, colors, target_a)
    targets_b = positions_matching(objects, colors, target_b)

    carrying = observation["carrying"]
    carry_object, carry_color = carrying if carrying is not None else (-1, -1)
    features = []
    features += one_hot(observation["robot_id"], 6)
    features += one_hot(observation["direction"], 4)
    features += one_hot(family, 3)
    features += one_hot(template, 12)
    features += [float(connector), float(rr), float(rc), float(carrying is not None)]
    features += one_hot(carry_object - 5, 3) if carry_object in (5, 6, 7) else [0.0] * 3
    features += one_hot(carry_color, 6) if carry_color >= 0 else [0.0] * 6
    features += one_hot(target_a[0] - 5, 3) + one_hot(target_a[1], 6)
    features += one_hot(target_b[0] - 5, 3) + one_hot(target_b[1], 6) if target_b[0] >= 0 else [0.0] * 9
    features += target_geometry(robot, targets_a)
    features += target_geometry(robot, targets_b)

    target_a_set = set(targets_a)
    target_b_set = set(targets_b)
    for direction, (dr, dc) in enumerate(DIRECTIONS):
        nr, nc = rr + dr, rc + dc
        object_id = int(objects[nr, nc])
        color_id = int(colors[nr, nc])
        features += one_hot(OBJECT_VALUES.index(object_id), len(OBJECT_VALUES))
        features += [
            float(color_id), float((nr, nc) in target_a_set), float((nr, nc) in target_b_set),
            float(object_id == 1), float(object_id == 11),
            float(direction == observation["direction"]),
        ]

    for targets in (targets_a, targets_b):
        for allow_tokens in (False, True):
            goals = adjacent_walkable(objects, targets, allow_tokens)
            features += directional_distances(distance_map(objects, goals, allow_tokens), robot)

    valid_drop_directions = [0.0] * 4
    drop_stands = set()
    for target_row, target_column in targets_b:
        for drop_dr, drop_dc in DIRECTIONS:
            drop_row, drop_column = target_row + drop_dr, target_column + drop_dc
            if objects[drop_row, drop_column] != 1:
                continue
            for stand_dr, stand_dc in DIRECTIONS:
                stand = (drop_row + stand_dr, drop_column + stand_dc)
                if objects[stand] in (1, 10):
                    drop_stands.add(stand)
            for direction, (dr, dc) in enumerate(DIRECTIONS):
                if (rr + dr, rc + dc) == (drop_row, drop_column):
                    valid_drop_directions[direction] = 1.0
    features += valid_drop_directions
    features += directional_distances(distance_map(objects, sorted(drop_stands), False), robot)

    front_dr, front_dc = DIRECTIONS[observation["direction"]]
    front = (rr + front_dr, rc + front_dc)
    front_object = int(objects[front])
    front_color = int(colors[front])
    features += [
        float(front in target_a_set), float(front in target_b_set),
        float(front_object == 1), float(front_object == 2), float(front_object == 11),
        float(front_object in (5, 6, 7)),
        float((front_object, front_color) == target_a),
        float((front_object, front_color) == target_b),
        float(valid_drop_directions[observation["direction"]]),
    ]

    interior_objects = objects[1:7, 1:7].reshape(-1)
    interior_colors = colors[1:7, 1:7].reshape(-1)
    for object_id in OBJECT_VALUES:
        features.extend((interior_objects == object_id).astype(np.float32).tolist())
    features.extend((interior_colors / 5.0).astype(np.float32).tolist())
    features.extend([
        float((row, column) in target_a_set)
        for row in range(1, 7) for column in range(1, 7)
    ])
    features.extend([
        float((row, column) in target_b_set)
        for row in range(1, 7) for column in range(1, 7)
    ])
    return features


def make_matrix(observations):
    return np.asarray([extract_features(row) for row in observations], dtype=np.float32)


def train_predict(train_observations, train_labels, evaluation_observations):
    x_train = make_matrix(train_observations)
    x_evaluation = make_matrix(evaluation_observations)
    y_train = np.asarray(train_labels, dtype=np.int64)
    robot_train = np.asarray([row["robot_id"] for row in train_observations])
    robot_evaluation = np.asarray([row["robot_id"] for row in evaluation_observations])

    shared = ExtraTreesClassifier(
        n_estimators=220,
        max_features=0.65,
        min_samples_leaf=1,
        n_jobs=-1,
        random_state=20260805,
    )
    shared.fit(x_train, y_train)
    probabilities = 0.35 * shared.predict_proba(x_evaluation)

    for robot_id in range(6):
        train_mask = robot_train == robot_id
        evaluation_mask = robot_evaluation == robot_id
        expert = ExtraTreesClassifier(
            n_estimators=180,
            max_features=0.75,
            min_samples_leaf=1,
            n_jobs=-1,
            random_state=20260815 + robot_id,
        )
        expert.fit(x_train[train_mask], y_train[train_mask])
        probabilities[evaluation_mask] += 0.65 * expert.predict_proba(x_evaluation[evaluation_mask])
    return probabilities.argmax(axis=1).astype(int).tolist(), x_train.shape[1]


def find_split(name, search_root="/kaggle/input"):
    matches = []
    for path in Path(search_root).rglob(name):
        if path.is_dir() and (path / "observations.json").is_file():
            matches.append(path)
    if not matches:
        raise FileNotFoundError(f"{name}/ with observations.json not found")
    return sorted(matches)[0]


train_dir = find_split("train")
test_dir = find_split("test")
train_observations = load_json(train_dir / "observations.json")
train_labels = load_json(train_dir / "labels.json")
test_observations = load_json(test_dir / "observations.json")
assert len(train_observations) == len(train_labels) == 60000
assert len(test_observations) == 7200

predictions, feature_count = train_predict(train_observations, train_labels, test_observations)
ids = [row["id"] for row in test_observations]
assert len(ids) == len(set(ids)) == 7200
assert len(predictions) == 7200
assert all(isinstance(value, int) and 0 <= value < 6 for value in predictions)

submission = Path("/kaggle/working/submission.csv")
temporary = submission.with_suffix(".tmp")
with temporary.open("w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["id", "prediction"])
    writer.writerows(zip(ids, predictions))
temporary.replace(submission)
print(f"wrote {submission} with {len(predictions)} rows and {feature_count} features")
