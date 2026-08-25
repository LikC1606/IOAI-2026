#!/usr/bin/env python3
"""Publish the parallel Task 4 solver traces omitted from the first index.

The parallel solver produced notebook versions 2 and 3 and supplied the
version-2 comparison baseline used by the final version-4 solver.  These traces
are therefore causally relevant Task 4 execution evidence, even though they
live in a separate historical run directory.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import build_execution_trace_index as trace_tools


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(
    "/workspace/IOAI/runs/historical/"
    "ioai2-competition-runs-task4-fastbaseline-real-subagents-20260807T1304CST/"
    "ioai-2026-task-4-westlake-nlp-24/codex-home/sessions/2026/08/07"
)
DESTINATION_ROOT = ROOT / "task4/evidence/supplemental-rollouts"
PROVENANCE = ROOT / "task4/evidence/SUPPLEMENTAL_ROLLOUT_PROVENANCE.json"
BOUNDARY_UTC_EXCLUSIVE = "2026-08-07T06:18:25.517Z"
FILENAMES = (
    "rollout-2026-08-07T13-04-06-019fda9b-6b63-7031-a6dd-52db684209be.jsonl",
    "rollout-2026-08-07T13-04-23-019fda9b-ade0-7912-868f-a922606fd40f.jsonl",
    "rollout-2026-08-07T13-04-30-019fda9b-c906-70a0-8f5c-99fc2f25fafa.jsonl",
    "rollout-2026-08-07T13-04-39-019fda9b-ed93-7473-96c5-f8c030d3e4bc.jsonl",
    "rollout-2026-08-07T13-57-14-019fdacc-1073-7f03-ac6e-346ad63c0c4f.jsonl",
    "rollout-2026-08-07T13-57-22-019fdacc-2e9c-78a2-b037-135a4b172944.jsonl",
    "rollout-2026-08-07T13-57-28-019fdacc-47fe-7bc3-8cac-d77f25b124e1.jsonl",
)


def publish_one(source: Path, destination: Path) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    encoded: list[str] = []
    for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL {source}:{line_number}") from exc
        timestamp = str(event.get("timestamp", ""))
        if timestamp and timestamp >= BOUNDARY_UTC_EXCLUSIVE:
            raise ValueError(f"post-boundary supplemental Task 4 event: {source}:{line_number}")
        encoded.append(
            json.dumps(trace_tools.redact(event), ensure_ascii=False, separators=(",", ":"))
        )
    destination.write_text("\n".join(encoded) + "\n", encoding="utf-8")
    relative = destination.relative_to(ROOT).as_posix()
    record = trace_tools.trace_record(destination, relative)
    return {
        "filename": source.name,
        "role": record["role"],
        "private_original_path": str(source),
        "private_original_sha256": trace_tools.sha256(source),
        "published_path": relative,
        "published_sha256": trace_tools.sha256(destination),
        "event_count": record["event_count"],
        "first_timestamp": record["first_timestamp"],
        "last_timestamp": record["last_timestamp"],
        "token_usage_cumulative_final": record["token_usage_cumulative_final"],
    }


def build() -> dict[str, Any]:
    missing = [SOURCE_ROOT / name for name in FILENAMES if not (SOURCE_ROOT / name).is_file()]
    if missing:
        if all((DESTINATION_ROOT / name).is_file() for name in FILENAMES) and PROVENANCE.is_file():
            return json.loads(PROVENANCE.read_text(encoding="utf-8"))
        raise FileNotFoundError(f"missing Task 4 supplemental trace source(s): {missing}")
    records = [
        publish_one(SOURCE_ROOT / name, DESTINATION_ROOT / name)
        for name in FILENAMES
    ]
    payload = {
        "schema": "ioai.supplemental-rollout-provenance.v1",
        "task": 4,
        "competition": "ioai-2026-task-4-westlake-nlp-24",
        "selection_reason": (
            "Parallel autonomous solver execution produced versions 2 and 3 and "
            "the version-2 evidence used by the final version-4 path; the first "
            "organizer index omitted this separate historical run directory."
        ),
        "boundary_utc_exclusive": BOUNDARY_UTC_EXCLUSIVE,
        "live_human_prompt_events_included": 0,
        "redaction": (
            "credentials, private endpoints, secret metadata, and opaque encrypted "
            "reasoning are redacted using tools/build_execution_trace_index.py"
        ),
        "traces": records,
    }
    PROVENANCE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return payload


def main() -> None:
    payload = build()
    print(json.dumps({"trace_files": len(payload["traces"]), "events": sum(x["event_count"] for x in payload["traces"])}))


if __name__ == "__main__":
    main()
