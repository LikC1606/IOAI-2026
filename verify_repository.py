"""Verify task manifests, core score claims, and autonomous trace material."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = {
    1: (55267607, 0.78049),
    2: (55260695, 0.55416),
    3: ([55289569, 55289823], 58.51666),
    4: (55316818, 98.41),
    5: (55320296, 95.39),
}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def verify_manifest(root: Path) -> int:
    checked = 0
    manifest = root / "MANIFEST.sha256"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        relative = relative.removeprefix("*").removeprefix("./")
        assert sha256(root / relative) == expected, f"{root.name}/{relative}"
        checked += 1
    return checked


def verify_autonomous_material() -> dict[str, int]:
    checked = 0
    manifest = ROOT / "AUTONOMOUS_MATERIAL_MANIFEST.sha256"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        target = (ROOT / relative).resolve()
        assert target.is_relative_to(ROOT.resolve()), relative
        assert sha256(target) == expected, relative
        checked += 1

    index = json.loads((ROOT / "AUTONOMOUS_TRACE_INDEX.json").read_text(encoding="utf-8"))
    trace_files = 0
    events = 0
    tokens = 0
    for task, data in index["tasks"].items():
        assert data["manual_human_prompt_events_included"] == 0, task
        assert len(data["user_prompt_audit"]) == data["message_counts"].get("user", 0), task
        boundary = data["boundary"]["exclusive_utc"]
        task_tokens = 0
        for trace in data["trace_files"]:
            path = ROOT / trace["path"]
            assert sha256(path) == trace["sha256"], trace["path"]
            assert trace["last_timestamp"] < boundary, trace["path"]
            task_tokens += trace["token_usage_cumulative_final"]["total_tokens"]
            trace_files += 1
            events += trace["event_count"]
        assert task_tokens == data["token_usage_cumulative_sum_across_traces"]["total_tokens"], task
        tokens += task_tokens

    costs = json.loads((ROOT / "AUTONOMOUS_COSTS.json").read_text(encoding="utf-8"))
    assert costs["known_token_total_all_tasks"] == tokens
    return {
        "manifest_files": checked,
        "trace_files": trace_files,
        "events": events,
        "tokens": tokens,
    }


def main() -> None:
    report = {"tasks": {}}
    for task in range(1, 6):
        root = ROOT / f"task{task}"
        assert root.is_dir()
        summary = json.loads((root / "SUMMARY.json").read_text(encoding="utf-8"))
        submission, score = EXPECTED[task]
        if task == 1:
            assert summary["positive_claim"]["agent_executed_submission"] == submission
            assert summary["positive_claim"]["agent_executed_public_score"] == score
        elif task == 3:
            assert summary["best_submission_refs"] == submission
            assert summary["best_public_score"] == score
        else:
            assert summary["best_submission_ref"] == submission
            assert summary["best_public_score"] == score
        report["tasks"][f"task{task}"] = {
            "manifest_files": verify_manifest(root),
            "recorded_score": score,
        }
    report["autonomous_material"] = verify_autonomous_material()
    report["all_ok"] = True
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
