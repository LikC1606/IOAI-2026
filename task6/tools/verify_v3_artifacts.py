#!/usr/bin/env python3
"""Verify the exact autonomous Task 6 v3 submission and its batch dependence."""

from __future__ import annotations

import base64
import csv
import hashlib
import json
from pathlib import Path

import torch
from safetensors.torch import load


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/v3/script.py"
METADATA = ROOT / "notebooks/v3/kernel-metadata.json"
SOURCE = ROOT / "remote/v3/custom_model.py"
SUBMISSION = ROOT / "remote/v3/submission.csv"

EXPECTED = {
    NOTEBOOK: "f9a8fbdcbcf2be4b327ca3961726feebe19a2d4d54c6a257bca5e6f60a45e267",
    METADATA: "3e9aeeba013f32d01e54b9e65f233573285c40fe34d1021d0d043683fe2676d8",
    SOURCE: "f325541e9ec0df6b4e286528c46070976407a66003912477f05d38134c80822a",
    SUBMISSION: "6695d583492eae631f778f6f7846fe498836f250ae47c585a770b1073c79e53c",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for path, expected in EXPECTED.items():
        assert sha256(path) == expected, path

    with SUBMISSION.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        assert reader.fieldnames == ["id", "model_b64", "code_b64"]
    assert [row["id"] for row in rows] == ["leaderboard-a", "leaderboard-b"]
    assert rows[0]["model_b64"] == rows[1]["model_b64"]
    assert rows[0]["code_b64"] == rows[1]["code_b64"]

    decoded_source = base64.b64decode(rows[0]["code_b64"])
    decoded_weights = base64.b64decode(rows[0]["model_b64"])
    assert decoded_source == SOURCE.read_bytes()

    namespace: dict[str, object] = {}
    exec(compile(decoded_source, "submitted_custom_model.py", "exec"), namespace)
    model = namespace["build_model"]()
    model.load_state_dict(load(decoded_weights))
    model.eval()
    parameter_count = sum(parameter.numel() for parameter in model.parameters())
    assert parameter_count == 13_426

    generator = torch.Generator().manual_seed(20_260_825)
    points = torch.rand((100, 2), generator=generator)
    context_a = torch.rand((100, 199, 2), generator=generator)
    context_b = torch.rand((100, 199, 2), generator=generator)
    component_changes = 0
    final_prediction_changes = 0
    max_final_change = 0.0
    with torch.no_grad():
        for index, point in enumerate(points):
            batch_a = torch.cat((point[None], context_a[index]), dim=0)
            batch_b = torch.cat((point[None], context_b[index]), dim=0)
            components_a = model.components(batch_a)
            components_b = model.components(batch_b)
            if any(
                not torch.equal(left[0], right[0])
                for left, right in zip(components_a, components_b)
            ):
                component_changes += 1
            prediction_a = model(batch_a)[0]
            prediction_b = model(batch_b)[0]
            difference = float(torch.max(torch.abs(prediction_a - prediction_b)))
            if difference > 0:
                final_prediction_changes += 1
            max_final_change = max(max_final_change, difference)

    assert component_changes == 100
    assert final_prediction_changes > 0
    assert max_final_change > 0

    report = NOTEBOOK.read_text(encoding="utf-8")
    assert "seven independent centered" in report
    assert "expand(-1, 8)" in decoded_source.decode("utf-8")

    print(
        json.dumps(
            {
                "all_ok": True,
                "rows": len(rows),
                "payloads_identical": True,
                "decoded_source_exact_match": True,
                "parameter_count": parameter_count,
                "batch_dependence": {
                    "test_points": len(points),
                    "component_changes": component_changes,
                    "final_prediction_changes": final_prediction_changes,
                    "max_final_change": max_final_change,
                },
                "historical_report_discrepancy_present": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
