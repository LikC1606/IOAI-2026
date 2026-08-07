import argparse
import json
from collections import deque
from pathlib import Path

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


def requested_case_ids(payload):
    cases = payload.get("cases", [])
    ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
    ids = [case_id for case_id in ids if case_id]
    if not ids and payload.get("case_id"):
        ids = [payload["case_id"]]
    return ids or ["validation"]


def validation_diagnostics(observations, labels, predictions):
    correct_by_robot = [0] * 6
    total_by_robot = [0] * 6
    correct_by_family = [0] * 3
    total_by_family = [0] * 3
    anchor_correct = 0
    anchor_total = 0
    seen_by_robot = [0] * 6
    for observation, label, prediction in zip(observations, labels, predictions):
        robot_id = observation["robot_id"]
        family = parse_mission(observation["mission"])[0]
        is_correct = int(label == prediction)
        correct_by_robot[robot_id] += is_correct
        total_by_robot[robot_id] += 1
        correct_by_family[family] += is_correct
        total_by_family[family] += 1
        if seen_by_robot[robot_id] % 5 == 0:
            anchor_correct += is_correct
            anchor_total += 1
        seen_by_robot[robot_id] += 1
    per_robot = [c / n for c, n in zip(correct_by_robot, total_by_robot)]
    per_family = [c / n for c, n in zip(correct_by_family, total_by_family)]
    return {
        "score": sum(per_robot) / 6,
        "per_robot_accuracy": per_robot,
        "per_family_accuracy": per_family,
        "anchor_accuracy": anchor_correct / anchor_total,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.input) as handle:
        payload = json.load(handle)
    data = resolve_data_root(payload)
    train_observations = load_json(data / "train" / "observations.json")
    train_labels = load_json(data / "train" / "labels.json")
    validation_observations = load_json(data / "validation" / "observations.json")
    validation_labels = load_json(data / "validation" / "labels.json")
    predictions, feature_count = train_predict(train_observations, train_labels, validation_observations)
    candidate = validation_diagnostics(validation_observations, validation_labels, predictions)
    candidate.update({
        "validation_predictions": predictions,
        "model": "shared-plus-per-robot-extra-trees",
        "feature_count": feature_count,
    })
    output = {
        "schema": "deepscientist.ioai.competition.attempt-output.v2",
        "cases": [
            {"case_id": case_id, "candidate": candidate}
            for case_id in requested_case_ids(payload)
        ],
    }
    destination = Path(args.output)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    with temporary.open("w") as handle:
        json.dump(output, handle, separators=(",", ":"))
    temporary.replace(destination)


if __name__ == "__main__":
    main()
