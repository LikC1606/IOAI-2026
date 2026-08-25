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
    6: (55357080, 75.0154),
}

FINAL_RESULTS = {
    1: {
        "source_sha256": "922375f34f447965c28bf7d7d089427376cac9e00afee2e739360f6275b60c04",
        "counts": (30, 15, 15),
        "refs": [55267333, 55267368],
        "public": 0.77751,
        "private": 0.80474,
        "latest": (55300144, 0.81854, 0.82775),
    },
    2: {
        "source_sha256": "cd78ff77983ad75afb301ee1bdf7bc79962ff9dc5a7efa91d19110e3dee740b2",
        "counts": (16, 5, 11),
        "refs": [55261432],
        "public": 0.63583,
        "private": 0.625,
        "latest": (55280319, 0.65888, 0.66166),
    },
    3: {
        "source_sha256": "b1492e3213fad6ae0c77a2a97f02e4e39542f18b9aee950af1349d55cd60588e",
        "counts": (27, 11, 16),
        "refs": [55289569, 55289823],
        "public": 58.51666,
        "private": 51.61666,
        "latest": (55306794, 41.16666, 41.15),
    },
    4: {
        "source_sha256": "8afbfb3ad2a6a6fd0711b03e92db38fb6a46fb038ac2a106a4bb4356a9b94038",
        "counts": (3, 3, 0),
        "refs": [55316818],
        "public": 98.41,
        "private": 98.32,
        "latest": (55316818, 98.41, 98.32),
    },
    5: {
        "source_sha256": "d72861924dd58ad649c70bca45cdcda276253d88a5dcd2a51cb8da402b5b5820",
        "counts": (7, 6, 1),
        "refs": [55320296],
        "public": 95.39,
        "private": 96.06,
        "latest": (55320652, 94.17, 96.31),
    },
    6: {
        "source_sha256": "220c181eafc7be3db00a8bc1a955c7af351d62e3e73384fb0adfbf941221b50f",
        "counts": (6, 4, 2),
        "refs": [55357080],
        "public": 75.0154,
        "private": 73.36234,
        "latest": (55358739, 76.41428, 73.74666),
    },
}

EXPECTED_PROMPT_CLASSES = {
    "task3": {
        "inherited_organizer_starter_prompt": 3,
        "organizer_starter_prompt": 1,
        "startup_instructions": 4,
    },
    "task4": {
        "inherited_organizer_starter_prompt": 4,
        "inherited_preconfigured_runtime_resume_template": 4,
        "organizer_starter_prompt": 1,
        "preconfigured_runtime_resume_template": 6,
        "startup_instructions": 5,
    },
    "task5": {
        "inherited_organizer_starter_prompt": 13,
        "organizer_starter_prompt": 1,
        "startup_instructions": 14,
    },
    "task6": {
        "inherited_organizer_starter_prompt": 2,
        "organizer_starter_prompt": 1,
        "startup_instructions": 3,
    },
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


def verify_final_account_result(task: int, summary: dict) -> dict[str, object]:
    expected = FINAL_RESULTS[task]
    path = ROOT / f"task{task}/remote/FINAL_ACCOUNT_RESULTS.json"
    result = json.loads(path.read_text(encoding="utf-8"))
    assert result["task"] == task
    assert result["account"] == "researai"
    assert result["extraction_source_sha256"] == expected["source_sha256"]

    counts = result["submission_counts"]
    assert (
        counts["all_account"],
        counts["before_official_deadline"],
        counts["after_official_deadline"],
    ) == expected["counts"]

    official = result["official_final_result"]
    assert official["submission_refs"] == expected["refs"]
    assert official["public_score"] == expected["public"]
    assert official["private_score"] == expected["private"]
    assert summary["official_final_submission_refs"] == expected["refs"]
    assert summary["official_final_public_score"] == expected["public"]
    assert summary["official_final_private_score"] == expected["private"]

    latest_key = {
        1: "latest_account_and_best_private",
        2: "latest_account_submission",
        3: "latest_account_submission",
        4: "latest_account_submission",
        5: "latest_account_and_best_private",
        6: "latest_account_and_all_account_best",
    }[task]
    latest = result[latest_key]
    assert (
        latest["submission_ref"],
        latest["public_score"],
        latest["private_score"],
    ) == expected["latest"]

    if task == 1:
        assert result["separately_disclosed_agent_executed_result"]["submission_ref"] == 55267607
        assert result["official_prompt_only_autonomous_result"]["scored_submission"] is None
    elif task == 2:
        assert result["autonomous_result"]["submission_ref"] == 55260695
    elif task == 3:
        assert result["official_deadline_best_private"] == {
            "score": 55.48333,
            "submission_ref": 55290027,
            "public_score": 53.43333,
            "submitted_at_utc": "2026-08-06T05:47:27.213Z",
            "autonomous": False,
        }
    elif task == 5:
        assert latest["seconds_after_official_deadline"] == 121.927
        assert latest["official_deadline_eligible"] is False
    elif task == 6:
        excluded = result["excluded_post_autonomy_pre_run_deadline_submission"]
        assert (
            excluded["submission_ref"],
            excluded["public_score"],
            excluded["private_score"],
        ) == (55357740, 58.15133, 57.05126)
        assert [item["submission_ref"] for item in result["post_official_deadline_submissions"]] == [
            55358042,
            55358739,
        ]

    return {
        "submission_refs": official["submission_refs"],
        "public_score": official["public_score"],
        "private_score": official["private_score"],
        "account_submission_count": counts["all_account"],
    }


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
        assert data["canonical_model"] == "gpt-5.6-sol", task
        assert data["model_provider"] == "ioai_allowed", task
        assert data["reasoning_effort"] in {"max", "xhigh"}, task
        for field in (
            "prompt_message_events",
            "assistant_output_events",
            "function_call_events",
            "function_call_output_events",
            "custom_tool_call_events",
            "custom_tool_call_output_events",
        ):
            assert field in data["organizer_required_event_coverage"], (task, field)
        task_tokens = 0
        for trace in data["trace_files"]:
            path = ROOT / trace["path"]
            assert sha256(path) == trace["sha256"], trace["path"]
            assert trace["last_timestamp"] < boundary, trace["path"]
            task_tokens += trace["token_usage_cumulative_final"]["total_tokens"]
            trace_files += 1
            events += trace["event_count"]
        assert task_tokens == data["token_usage_cumulative_sum_across_traces"]["total_tokens"], task
        if task in EXPECTED_PROMPT_CLASSES:
            assert data["user_prompt_classes"] == EXPECTED_PROMPT_CLASSES[task], task
        tokens += task_tokens

    assert len(index["tasks"]["task6"]["trace_files"]) == 3
    task3_boundary = json.loads(
        (ROOT / "task3/evidence/SUPERVISION_BOUNDARY_EVENT.json").read_text(encoding="utf-8")
    )
    assert task3_boundary["content_in_repository"] is False
    assert "content" not in task3_boundary
    task1_boundary = json.loads(
        (ROOT / "task1/evidence/SUPERVISION_BOUNDARY_EVENT.json").read_text(encoding="utf-8")
    )
    assert task1_boundary["content_in_repository"] is False
    assert "content" not in task1_boundary and "payload" not in task1_boundary
    task6_exclusions = json.loads(
        (ROOT / "task6/evidence/SUPERVISED_EXCLUSIONS.json").read_text(encoding="utf-8")
    )
    assert task6_exclusions["excluded_prompt_bodies_in_repository"] is False
    for item in task6_exclusions["excluded_trace_sources"]:
        assert not (ROOT / item["former_repository_path"]).exists()
    assert not (ROOT / "task6/official/continue.md").exists()

    costs = json.loads((ROOT / "AUTONOMOUS_COSTS.json").read_text(encoding="utf-8"))
    assert costs["known_token_total_all_tasks"] == tokens
    return {
        "manifest_files": checked,
        "trace_files": trace_files,
        "events": events,
        "tokens": tokens,
    }


def verify_execution_accounting() -> dict[str, int]:
    index = json.loads((ROOT / "EXECUTION_TRACE_INDEX.json").read_text(encoding="utf-8"))
    costs = json.loads((ROOT / "COSTS.json").read_text(encoding="utf-8"))
    tokens = 0
    traces = 0
    for task, data in index["tasks"].items():
        task_tokens = data["token_usage_cumulative_sum_across_traces"]["total_tokens"]
        assert costs["tasks"][task]["token_usage"]["total_tokens"] == task_tokens, task
        tokens += task_tokens
        traces += len(data["trace_files"])
    assert costs["known_token_total_all_tasks"] == tokens
    assert len(index["tasks"]["task6"]["trace_files"]) == 3
    assert index["tasks"]["task6"]["token_usage_cumulative_sum_across_traces"]["total_tokens"] == 41371859
    return {"trace_files": traces, "tokens": tokens}


def main() -> None:
    report = {"tasks": {}}
    for task in range(1, 7):
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
        task_report = {
            "manifest_files": verify_manifest(root) if task <= 5 else 0,
            "recorded_score": score,
        }
        task_report["final_account_result"] = verify_final_account_result(task, summary)
        report["tasks"][f"task{task}"] = task_report
    report["autonomous_material"] = verify_autonomous_material()
    report["published_execution_accounting"] = verify_execution_accounting()
    delivery = json.loads((ROOT / "KAGGLE_EXTRACTION_DELIVERY.json").read_text(encoding="utf-8"))
    assert delivery["archive"]["size_bytes"] == 496870419
    assert delivery["archive"]["entry_count"] == 1401
    assert delivery["archive"]["sha256"] == "eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c"
    assert delivery["google_drive"]["file_id"] == "1c9yRn5SUo6LOPDrHLrAVjj-9JLFti9Vz"
    checklist = json.loads((ROOT / "ORGANIZER_SUBMISSION.json").read_text(encoding="utf-8"))
    assert checklist["status"] == "complete_with_explicit_cost_limits"
    forbidden = ("你让他继续优化 找到高分了再提交", "Extend this run by 35 minutes")
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path == Path(__file__):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        assert not any(marker in text for marker in forbidden), path
    report["all_ok"] = True
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
