#!/usr/bin/env python3
"""Prefix-constrained identity-order baseline for the public validation split."""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path


PROJECT_ROOT = Path(
    os.environ.get(
        "IOAI_PROJECT_ROOT",
        "/workspace/IOAI/next-task/ioai-2026-task-1-westlake-nlp-24/project",
    )
)


def chunk_count(dialogue_dir: Path) -> int:
    indices = sorted(
        int(path.stem.removeprefix("chunk_"))
        for path in dialogue_dir.glob("chunk_*.wav")
    )
    if indices != list(range(len(indices))):
        raise ValueError(f"invalid chunk set: {dialogue_dir}")
    return len(indices)


def predict(split_dir: Path) -> dict[str, list[int]]:
    predictions = {}
    with (split_dir / "prefix.csv").open(newline="") as handle:
        for row in csv.DictReader(handle):
            filename = str(row["filename"])
            prefix = json.loads(row["prefix"])
            n = chunk_count(split_dir / filename)
            order = prefix + [idx for idx in range(n) if idx not in prefix]
            ranks = [0] * n
            for rank, chunk_idx in enumerate(order):
                ranks[chunk_idx] = rank
            predictions[filename] = ranks
    return predictions


def measured_score(split_dir: Path, predictions: dict[str, list[int]]) -> float:
    scores = []
    with (split_dir / "answers.csv").open(newline="") as handle:
        for row in csv.DictReader(handle):
            answer = json.loads(row["answer"])
            prediction = predictions[str(row["filename"])]
            n = len(answer)
            pairs = n * (n - 1) // 2
            correct = sum(
                (prediction[left] < prediction[right]) == (answer[left] < answer[right])
                for left in range(n)
                for right in range(left + 1, n)
            )
            scores.append(correct / pairs)
    return sum(scores) / len(scores)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.input) as handle:
        attempt_input = json.load(handle)
    case_ids = [case["case_id"] for case in attempt_input["cases"]]
    split_dir = PROJECT_ROOT / "data/official/test_public"
    predictions = predict(split_dir)
    candidate = {"score": measured_score(split_dir, predictions)}
    payload = {
        "schema": "deepscientist.ioai.competition.attempt-output.v2",
        "cases": [
            {"case_id": case_id, "candidate": candidate}
            for case_id in case_ids
        ],
    }

    output = Path(args.output)
    temporary = output.with_name(output.name + ".tmp")
    with temporary.open("w") as handle:
        json.dump(payload, handle, separators=(",", ":"))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, output)


if __name__ == "__main__":
    main()
