"""Deterministic local evaluator for dialogue rank permutations."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_answers(path: Path) -> dict[str, list[int]]:
    with path.open(newline="") as handle:
        rows = csv.DictReader(handle)
        return {str(row["filename"]): json.loads(row["answer"]) for row in rows}


def _valid_permutation(values: object, n: int) -> bool:
    return (
        isinstance(values, list)
        and len(values) == n
        and all(isinstance(value, int) and not isinstance(value, bool) for value in values)
        and sorted(values) == list(range(n))
    )


def _dialogue_score(prediction: object, answer: list[int]) -> float:
    n = len(answer)
    if not _valid_permutation(prediction, n):
        return 0.0
    pairs = n * (n - 1) // 2
    if pairs == 0:
        return 1.0
    correct = 0
    for left in range(n):
        for right in range(left + 1, n):
            correct += ((prediction[left] < prediction[right]) ==
                        (answer[left] < answer[right]))
    return correct / pairs


def score(candidate: dict, fixture: dict) -> float:
    """Return mean per-dialogue pairwise ordering accuracy."""
    if set(candidate) == {"score"}:
        return float(candidate["score"])

    predictions = candidate.get("predictions")
    if not isinstance(predictions, dict):
        return 0.0

    answers_path = PROJECT_ROOT / fixture["answers_path"]
    answers = _load_answers(answers_path)
    scores = [
        _dialogue_score(predictions.get(filename), answer)
        for filename, answer in answers.items()
    ]
    return sum(scores) / len(scores) if scores else 0.0
