"""Verify task manifests, core score claims, and autonomous trace material."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
import sys
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

PACKAGE_POSITIVE_CLAIM_SCOPES = {
    1: "separately_disclosed_agent_executed_after_supervision_and_official_deadline",
    2: "supplemental_exact_prompt_preboundary_formal_result_not_official_final",
    3: "trace_aligned_exact_prompt_official_final",
    4: "trace_aligned_non_exact_prompt_official_final",
    5: "trace_aligned_exact_prompt_official_final",
    6: "trace_aligned_exact_prompt_official_final",
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
    "task1": {
        "custom_starter_prompt": 1,
        "startup_instructions": 1,
    },
    "task2": {
        "custom_starter_prompt": 1,
        "startup_instructions": 1,
    },
    "task3": {
        "exact_organizer_starter_prompt": 1,
        "inherited_exact_organizer_starter_prompt": 3,
        "startup_instructions": 4,
    },
    "task4": {
        "custom_continuation_prompt": 10,
        "custom_starter_prompt": 2,
        "inherited_custom_continuation_prompt": 16,
        "inherited_custom_starter_prompt": 10,
        "startup_instructions": 12,
    },
    "task5": {
        "exact_organizer_starter_prompt": 1,
        "inherited_exact_organizer_starter_prompt": 13,
        "startup_instructions": 14,
    },
    "task6": {
        "exact_organizer_starter_prompt": 1,
        "inherited_exact_organizer_starter_prompt": 2,
        "startup_instructions": 3,
    },
}
STRICT_EXACT_PROMPT_TASKS = {"task3", "task5", "task6"}
TOKEN_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)


def verify_token_vector(tokens: dict[str, int], context: str) -> None:
    """Check the arithmetic and monotonicity invariants of token telemetry."""
    assert all(
        isinstance(tokens[field], int) and tokens[field] >= 0 for field in TOKEN_FIELDS
    ), context
    assert tokens["cached_input_tokens"] <= tokens["input_tokens"], context
    assert tokens["reasoning_output_tokens"] <= tokens["output_tokens"], context
    assert tokens["total_tokens"] == tokens["input_tokens"] + tokens["output_tokens"], context


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def verify_publication_safety() -> dict[str, int]:
    """Reject common unredacted credential and private-endpoint patterns."""
    patterns = {
        "kaggle_token": re.compile(r"KGAT_[A-Za-z0-9_-]{12,}"),
        "openai_key": re.compile(r"(?<![A-Za-z0-9_-])sk-(?:proj-)?[A-Za-z0-9_]{24,}"),
        "private_endpoint": re.compile(
            r"https?://(?:codex\.aiswing\.fun|api\.smilecodex\.space|127\.0\.0\.1:\d+)",
            re.IGNORECASE,
        ),
    }
    scanned = 0
    binary = 0
    findings: list[tuple[str, str]] = []
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\0")
    for raw_path in tracked:
        if not raw_path:
            continue
        path = ROOT / raw_path.decode("utf-8")
        try:
            content = path.read_bytes()
        except OSError:
            continue
        if b"\0" in content[:8192]:
            binary += 1
            continue
        scanned += 1
        text = content.decode("utf-8", errors="replace")
        for name, pattern in patterns.items():
            if pattern.search(text):
                findings.append((str(path.relative_to(ROOT)), name))
    assert not findings, findings
    return {"tracked_text_files": scanned, "tracked_binary_files": binary}


def verify_markdown_links() -> dict[str, int]:
    """Ensure every tracked Markdown link to a local path resolves.

    External links are intentionally not fetched here: network availability is
    not a repository-integrity property.  Local links, including links with an
    anchor fragment, must resolve so an organizer can follow every advertised
    evidence path from the published Markdown.
    """
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\0")
    local_links = 0
    external_links = 0
    missing: list[tuple[str, str]] = []
    for raw_path in tracked:
        if not raw_path or not raw_path.decode("utf-8").endswith(".md"):
            continue
        relative_path = raw_path.decode("utf-8")
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8", errors="replace")
        for raw_target in pattern.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if target.startswith(("http://", "https://", "mailto:")):
                external_links += 1
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            local_links += 1
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(ROOT.resolve()) or not resolved.exists():
                missing.append((relative_path, raw_target))
    assert not missing, missing
    return {
        "tracked_markdown_files": sum(
            1
            for raw_path in tracked
            if raw_path and raw_path.decode("utf-8").endswith(".md")
        ),
        "local_links": local_links,
        "external_links_not_fetched": external_links,
    }


def verify_manifest(root: Path) -> int:
    checked = 0
    manifest = root / "MANIFEST.sha256"
    listed_paths: set[str] = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        relative = relative.removeprefix("*").removeprefix("./")
        listed_paths.add(relative)
        assert sha256(root / relative) == expected, f"{root.name}/{relative}"
        checked += 1
    tracked_raw = subprocess.check_output(
        ["git", "ls-files", "-z", "--", f"{root.name}/"], cwd=ROOT
    )
    tracked_paths = {
        item.decode("utf-8").removeprefix(f"{root.name}/")
        for item in tracked_raw.split(b"\0")
        if item and item.decode("utf-8") != f"{root.name}/MANIFEST.sha256"
    }
    assert listed_paths == tracked_paths, {
        "task": root.name,
        "listed_not_tracked": sorted(listed_paths - tracked_paths),
        "tracked_not_listed": sorted(tracked_paths - listed_paths),
    }
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
        canonical = summary["canonical_autonomous_rollout"]
        assert canonical["trace_path"] == "evidence/canonical/rollout-solution-prefix.jsonl"
        assert canonical["full_raw_trace_path"] == "evidence/reproduction-120m/rollout.jsonl"
        assert canonical["autonomy_status"] == "fully_autonomous_no_live_human_intervention"
        assert canonical["submission_id"] == 55277782
        assert canonical["public_score"] == 0.74121
        assert canonical["post_deadline"] is True
        assert canonical["ranking_eligible"] is False
        assert canonical["manual_human_prompt_events_included"] == 0
        assert canonical["strict_exact_organizer_prompt_text_conformance"] is False
        assert canonical["user_prompt_classes"] == {
            "startup_instructions": 1,
            "custom_starter_prompt": 1,
        }
        formal_prefix = summary["supplemental_formal_prefix"]
        assert (ROOT / "task1" / formal_prefix["audit_path"]).resolve() == (
            ROOT / "FORMAL_PREFIX_AUDIT.json"
        ).resolve()
        assert formal_prefix == {
            "audit_path": "../FORMAL_PREFIX_AUDIT.json",
            "trace_path": "evidence/rollouts/rollout-2026-08-05T17-20-55-019fd139-d180-7171-ac0b-c037e11866eb.jsonl",
            "trace_sha256": "bcfb0c6ffca945638aedd4b3771915bc88abf72ca29843b457e966427684eb89",
            "event_count": 350,
            "boundary_utc_exclusive": "2026-08-05T10:16:52.222Z",
            "strict_exact_organizer_prompt_text_conformance": True,
            "preboundary_submission_ref": None,
            "scope": "bounded_preboundary_historical_audit_only; not the later reproduction and not trace evidence for the official final refs",
        }
    elif task == 2:
        assert result["autonomous_result"]["submission_ref"] == 55260695
        canonical = summary["canonical_autonomous_rollout"]
        assert canonical["trace_path"] == "evidence/reproduction-120m/rollout.jsonl"
        assert canonical["autonomy_status"] == "fully_autonomous_no_live_human_intervention"
        assert canonical["submission_id"] == 55277682
        assert canonical["public_score"] == 0.675
        assert canonical["post_deadline"] is True
        assert canonical["ranking_eligible"] is False
        assert canonical["manual_human_prompt_events_included"] == 0
        assert canonical["strict_exact_organizer_prompt_text_conformance"] is False
        assert canonical["user_prompt_classes"] == {
            "startup_instructions": 1,
            "custom_starter_prompt": 1,
        }
        formal_prefix = summary["supplemental_formal_prefix"]
        assert (ROOT / "task2" / formal_prefix["audit_path"]).resolve() == (
            ROOT / "FORMAL_PREFIX_AUDIT.json"
        ).resolve()
        assert formal_prefix == {
            "audit_path": "../FORMAL_PREFIX_AUDIT.json",
            "trace_path": "evidence/rollouts/rollout-2026-08-05T13-30-31-019fd066-e338-71a0-9d8e-6e1d154c5a79.jsonl",
            "trace_sha256": "a7dc48c7a837b3536d835c17fdee63db6fe27b79cd1cc577cbf4e15672f45014",
            "event_count": 705,
            "boundary_utc_exclusive": "2026-08-05T06:24:47.549Z",
            "strict_exact_organizer_prompt_text_conformance": True,
            "preboundary_submission_ref": 55260695,
            "preboundary_public_score": 0.55416,
            "preboundary_private_score": 0.54833,
            "scope": "bounded_preboundary_historical_audit_only; exact-prompt eligible v2 artifact chain; not the later reproduction or the official final",
        }
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
    manifest_paths: set[str] = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        assert relative not in manifest_paths, relative
        manifest_paths.add(relative)
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
        assert data["strict_exact_organizer_prompt_text_conformance"] == (
            task in STRICT_EXACT_PROMPT_TASKS
        ), task
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
            assert trace["path"] in manifest_paths, trace["path"]
            assert sha256(path) == trace["sha256"], trace["path"]
            assert trace["last_timestamp"] < boundary, trace["path"]
            if task in {"task1", "task2"}:
                expected_scope = (
                    "/evidence/canonical/"
                    if task == "task1"
                    else "/evidence/reproduction-120m/"
                )
                assert expected_scope in trace["path"], task
                assert trace["message_counts"].get("user", 0) == len(data["user_prompt_audit"]), task
                assert set(data["user_prompt_classes"]).issubset(
                    {
                        "startup_instructions",
                        "exact_organizer_starter_prompt",
                        "exact_organizer_continuation_prompt",
                        "custom_starter_prompt",
                        "custom_continuation_prompt",
                    }
                ), task
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
    assert costs["schema"] == "ioai.autonomous-execution-costs.v1"
    assert costs["known_token_total_all_tasks"] == tokens
    assert costs["api_cost_total_status"] == (
        "unavailable_no_provider_invoice_or_applicable_public_rate"
    )
    assert costs["api_cost_usd_total"] is None
    assert costs["gpu_compute_accounting_status"] == (
        "remote_kaggle_runtime_complete_selected_scope_local_development_incomplete"
    )
    assert costs["gpu_cost_total_status"] == (
        "incomplete_local_runtime_and_unavailable_rate"
    )
    assert costs["gpu_cost_usd_total"] is None
    observed_t4_seconds = sum(
        float(costs["tasks"][task]["gpu"]["runtime_seconds"])
        for task in costs["tasks"]
        if costs["tasks"][task]["gpu"]["accelerator"] == "NvidiaTeslaT4"
    )
    assert math.isclose(
        costs["known_t4_runtime_seconds"], observed_t4_seconds, rel_tol=0, abs_tol=1e-9
    )
    assert math.isclose(
        costs["known_t4_runtime_hours"], costs["known_t4_runtime_seconds"] / 3600,
        rel_tol=0, abs_tol=1e-12,
    )
    for task in ("task4", "task5", "task6"):
        gpu = costs["tasks"][task]["gpu"]
        assert gpu["local_development_runtime_seconds"] is None, task
        assert gpu["local_development_gpu_cost_usd"] is None, task
    for task, data in index["tasks"].items():
        aggregate = data["token_usage_cumulative_sum_across_traces"]
        assert aggregate is not None, task
        verify_token_vector(aggregate, task)
        assert costs["tasks"][task]["token_usage"] == {
            field: aggregate[field] for field in TOKEN_FIELDS
        }, task
    prompt_audit = json.loads(
        (ROOT / "PROMPT_CONFORMANCE_AUDIT.json").read_text(encoding="utf-8")
    )
    assert prompt_audit["strict_exact_prompt_tasks"] == ["task3", "task5", "task6"]
    assert prompt_audit["non_exact_prompt_tasks"] == ["task1", "task2", "task4"]
    for task, data in prompt_audit["tasks"].items():
        assert data["trace_prompt_classes"] == index["tasks"][task]["user_prompt_classes"]
        assert data["strict_exact_organizer_prompt_text_conformance"] == (
            task in STRICT_EXACT_PROMPT_TASKS
        )
        assert data["live_kaggle_page_matches_repository_source"] is True
    task4_rule_audit = json.loads(
        (ROOT / "task4/RULE_DIFFERENCE_AUDIT.json").read_text(encoding="utf-8")
    )
    assert task4_rule_audit["audited_final_submission"]["submission_ref"] == 55316818
    assert len(task4_rule_audit["findings"]) == 14
    statuses = {item["rule_id"]: item["status"] for item in task4_rule_audit["findings"]}
    assert statuses["prompt.exact_text"] == "disclosed_deviation"
    assert statuses["submission.folder_two_files"] == "disclosed_process_deviation_remote_artifact_unaffected"
    assert statuses["resources.external_web_research"] == (
        "informational_method_background_not_a_compliance_issue"
    )
    assert len(index["tasks"]["task4"]["trace_files"]) == 12
    supplemental = json.loads(
        (ROOT / "task4/evidence/SUPPLEMENTAL_ROLLOUT_PROVENANCE.json").read_text(encoding="utf-8")
    )
    assert len(supplemental["traces"]) == 7
    return {
        "manifest_files": checked,
        "trace_files": trace_files,
        "events": events,
        "tokens": tokens,
    }


def verify_task6_artifacts() -> dict[str, object]:
    """Run the exact v3 verifier and bind its result to the provenance audit."""
    expected = {
        "notebooks/v3/script.py": "f9a8fbdcbcf2be4b327ca3961726feebe19a2d4d54c6a257bca5e6f60a45e267",
        "notebooks/v3/kernel-metadata.json": "3e9aeeba013f32d01e54b9e65f233573285c40fe34d1021d0d043683fe2676d8",
        "remote/v3/custom_model.py": "f325541e9ec0df6b4e286528c46070976407a66003912477f05d38134c80822a",
        "remote/v3/submission.csv": "6695d583492eae631f778f6f7846fe498836f250ae47c585a770b1073c79e53c",
    }
    task_root = ROOT / "task6"
    for relative, digest in expected.items():
        assert sha256(task_root / relative) == digest, f"task6/{relative}"

    completed = subprocess.run(
        [sys.executable, str(task_root / "tools/verify_v3_artifacts.py")],
        cwd=task_root,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["all_ok"] is True
    assert result["rows"] == 2
    assert result["payloads_identical"] is True
    assert result["decoded_source_exact_match"] is True
    assert result["parameter_count"] == 13_426
    assert result["batch_dependence"] == {
        "test_points": 100,
        "component_changes": 100,
        "final_prediction_changes": 5,
        "max_final_change": 1.0,
    }
    assert result["historical_report_discrepancy_present"] is True

    provenance = json.loads(
        (task_root / "ARTIFACT_PROVENANCE.json").read_text(encoding="utf-8")
    )
    assert provenance["submission_ref"] == 55357080
    assert provenance["cross_checks"]["parameter_count"] == 13_426
    for key, relative in {
        "notebook_source": "notebooks/v3/script.py",
        "kernel_metadata": "notebooks/v3/kernel-metadata.json",
        "decoded_submitted_source": "remote/v3/custom_model.py",
        "remote_submission_output": "remote/v3/submission.csv",
    }.items():
        artifact = provenance["artifacts"][key]
        assert artifact["path"] == relative
        assert artifact["sha256"] == expected[relative]

    rule_audit = json.loads(
        (task_root / "RULE_DIFFERENCE_AUDIT.json").read_text(encoding="utf-8")
    )
    summary = json.loads((task_root / "SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["official_final_submission_refs"] == [provenance["submission_ref"]]
    assert summary["official_final_public_score"] == provenance["public_score"]
    assert summary["official_final_private_score"] == provenance["private_score"]
    assert summary["strict_exact_organizer_prompt_text_conformance"] is True
    assert summary["exact_v3_artifacts"]["provenance"] == "ARTIFACT_PROVENANCE.json"
    assert summary["rule_difference_audit"] == "RULE_DIFFERENCE_AUDIT.json"
    assert summary["batch_dependence_fixture"] == result["batch_dependence"]
    assert summary["historical_report_factual_error_disclosed"] is True
    assert summary["local_gpu_accounting_status"] == (
        "v3_candidate_31.03_seconds_known_exhaustive_total_unavailable"
    )
    assert rule_audit["statuses"]["result.trace_alignment"] == (
        "evidence_supported_compliant"
    )
    assert rule_audit["statuses"]["prompt.exact_text"] == (
        "evidence_supported_compliant"
    )
    assert rule_audit["statuses"]["model.evaluator_batch_dependence"] == (
        "measured_technical_behavior_not_treated_as_compliance_issue"
    )
    assert rule_audit["statuses"]["protected_field.hidden_geometry"] == (
        "measured_technical_behavior_not_treated_as_compliance_issue"
    )
    assert rule_audit["statuses"]["source.technical_report"] == (
        "disclosed_factual_error"
    )
    evaluator = json.loads(
        (task_root / "evidence/EVALUATOR_BATCHING_PROVENANCE.json").read_text(
            encoding="utf-8"
        )
    )
    assert evaluator["logical_source_path"] == "field/metrics/field_score.py"
    assert evaluator["source_sha256"] == (
        "a26781f14ac47eddf71aa320888b8d28c454cf13c3bba95b011ad8e827f8eb1d"
    )
    assert evaluator["source_in_repository"] is False
    assert evaluator["observed_function"]["name"] == "_predict_model_random_batches"
    assert evaluator["observed_function"]["definition_line_in_preserved_copy"] == 196
    assert rule_audit["official_evaluator_batching_provenance"] == (
        "evidence/EVALUATOR_BATCHING_PROVENANCE.json"
    )
    return result


def verify_task1_package() -> dict[str, object]:
    """Run the full Task 1 provenance/package verifier without writing files."""
    completed = subprocess.run(
        [sys.executable, "tools/verify_package.py", "--no-write-report"],
        cwd=ROOT / "task1",
        check=True,
        capture_output=True,
        text=True,
        timeout=600,
    )
    result = json.loads(completed.stdout)
    assert result["all_ok"] is True
    assert result["checks"]["official_prompts"]["starter_sha256"]
    assert result["checks"]["official_prompts"]["continue_sha256"]
    assert result["checks"]["boundary"]["hash_only"] is True
    assert result["checks"]["secrets"]["plaintext_secret_findings"] == 0
    return {
        "all_ok": result["all_ok"],
        "checks": sorted(result["checks"]),
    }


def verify_task3_package() -> dict[str, object]:
    """Replay all eight preserved Task 3 sources against the supplied data."""
    completed = subprocess.run(
        [sys.executable, "evidence/verify_artifacts.py"],
        cwd=ROOT / "task3",
        check=True,
        capture_output=True,
        text=True,
        timeout=600,
    )
    result = json.loads(completed.stdout)
    assert result["all_ok"] is True
    assert len(result["results"]) == 8
    assert all(
        item["csv_contract_ok"]
        and item["decoded_source_matches"]
        and item["local_contract_ok"]
        and item["starter_executable_outside_player_preserved"]
        for item in result["results"]
    )
    return {
        "all_ok": result["all_ok"],
        "versions": len(result["results"]),
        "source_csv_contracts": all(item["csv_contract_ok"] for item in result["results"]),
        "local_contracts": all(item["local_contract_ok"] for item in result["results"]),
    }


def verify_formal_prefix_audit() -> dict[str, object]:
    """Verify the supplemental bounded formal Task 1/2 prefixes.

    These prefixes are deliberately separate from the requested later
    reproduction selection.  Checking them here prevents a reviewer-facing
    audit from silently losing the exact-prompt formal evidence that remains
    after the complete original records became unavailable.
    """
    audit = json.loads((ROOT / "FORMAL_PREFIX_AUDIT.json").read_text(encoding="utf-8"))
    assert audit["schema"] == "ioai.formal-prefix-audit.v1"
    assert (ROOT / "FORMAL_PREFIX_AUDIT.md").is_file()
    expected = {
        "task1": {
            "events": 350,
            "boundary": "2026-08-05T10:16:52.222Z",
            "trace_sha256": "bcfb0c6ffca945638aedd4b3771915bc88abf72ca29843b457e966427684eb89",
            "prompt_count": 2,
            "starter": "task1/official/STARTER_PROMPT.md",
            "continuation": None,
        },
        "task2": {
            "events": 705,
            "boundary": "2026-08-05T06:24:47.549Z",
            "trace_sha256": "a7dc48c7a837b3536d835c17fdee63db6fe27b79cd1cc577cbf4e15672f45014",
            "prompt_count": 3,
            "starter": "task2/official/STARTER_PROMPT.md",
            "continuation": "task2/official/CONTINUE_PROMPT.md",
        },
    }
    for task, spec in expected.items():
        item = audit["tasks"][task]
        path = ROOT / item["trace_path"]
        assert path.is_file()
        assert sha256(path) == spec["trace_sha256"]
        events = []
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    events.append(json.loads(line))
        assert len(events) == spec["events"]
        assert item["event_count"] == len(events)
        timestamps = [str(event.get("timestamp")) for event in events if event.get("timestamp")]
        assert timestamps
        assert min(timestamps) == item["first_timestamp_utc"]
        assert max(timestamps) == item["last_timestamp_utc"]
        assert all(timestamp < spec["boundary"] for timestamp in timestamps)
        assert item["boundary_exclusive_utc"] == spec["boundary"]

        user_messages: list[str] = []
        for event in events:
            payload = event.get("payload", {})
            if event.get("type") != "response_item" or payload.get("role") != "user":
                continue
            user_messages.append(
                "\n".join(
                    str(part.get("text") or part.get("input_text") or "")
                    for part in payload.get("content") or []
                    if isinstance(part, dict)
                )
            )
        assert len(user_messages) == spec["prompt_count"]
        assert user_messages[0].startswith("# AGENTS.md instructions")
        starter = (ROOT / spec["starter"]).read_text(encoding="utf-8")
        assert user_messages[1] == starter
        if spec["continuation"] is None:
            assert len(user_messages) == 2
            assert item["prompt_conformance"]["continuation_prompt_events_before_boundary"] == 0
        else:
            continuation = (ROOT / spec["continuation"]).read_text(encoding="utf-8")
            assert user_messages[2] == continuation
            assert item["prompt_conformance"]["continuation_prompt_sha256"] == sha256(
                ROOT / spec["continuation"]
            )
        assert item["prompt_conformance"]["strict_exact_organizer_prompt_text"] is True
        assert item["prompt_conformance"]["starter_prompt_sha256"] == sha256(
            ROOT / spec["starter"]
        )
        assert item["provenance_file"] == f"{task}/ROLLOUT_PROVENANCE.json"
        provenance = json.loads(
            (ROOT / item["provenance_file"]).read_text(encoding="utf-8")
        )
        if task == "task1":
            provenance_rollout = provenance["formal_solver"]
            assert provenance["supervising_controller"]["prompt_body_in_repository"] is False
        else:
            assert provenance["provenance"]["boundary_prompt_body_in_repository"] is False
            assert provenance["provenance"]["causal_suffix_in_repository"] is False
            provenance_rollout = provenance["provenance"]["rollouts"][0]
        assert provenance_rollout["filename"] == path.name
        assert provenance_rollout["redacted_sha256"] == spec["trace_sha256"]
        assert provenance_rollout["kept_events"] == spec["events"]
        assert provenance_rollout["last_timestamp"] == item["last_timestamp_utc"]
        assert provenance_rollout["first_timestamp"] == item["first_timestamp_utc"]
        if task == "task1":
            assert provenance_rollout["boundary_utc_exclusive"] == spec["boundary"]
            assert provenance_rollout["excluded_post_boundary_suffix"]["content_in_repository"] is False
        else:
            assert provenance["provenance"]["boundary_utc"] == spec["boundary"]

    task2_result = audit["tasks"]["task2"]["preboundary_submission"]
    assert task2_result == {
        "submission_ref": 55260695,
        "kernel_version": 2,
        "submitted_at_utc": "2026-08-05T06:19:10.890Z",
        "public_score": 0.55416,
        "private_score": 0.54833,
        "trace_alignment": True,
        "artifact_chain": "task2/remote/rotation-cnn-v2/",
    }
    task2_summary = json.loads((ROOT / "task2/SUMMARY.json").read_text(encoding="utf-8"))
    assert task2_summary["best_submission_ref"] == task2_result["submission_ref"]
    assert task2_summary["best_public_score"] == task2_result["public_score"]
    assert task2_summary["best_private_score"] == task2_result["private_score"]
    assert audit["tasks"]["task1"]["preboundary_submission"] is None
    return {"all_ok": True, "formal_prefixes": 2, "task2_trace_aligned_submission": 55260695}


def _verify_gpu_notebook_metadata(
    metadata: dict[str, object], competition: str, kernel: str
) -> None:
    assert metadata["id"] == kernel
    assert metadata["is_private"] is True
    assert metadata["enable_gpu"] is True
    assert metadata["enable_internet"] is False
    assert metadata["machine_shape"] == "NvidiaTeslaT4"
    assert metadata["dataset_sources"] == ["kamalkhan/ioai-2026-wheel-dataset"]
    assert metadata["competition_sources"] == [competition]
    assert metadata["kernel_sources"] == []
    assert metadata["model_sources"] == []


def verify_task4_artifacts() -> dict[str, object]:
    """Verify the archived Task 4 source/log and hash-only large-output chain."""
    root = ROOT / "task4"
    source = root / "notebooks/REMOTE_CURRENT_V4.py"
    local_source = root / "notebooks/script.py"
    log_path = root / "remote/V4_KERNEL.log"
    provenance = json.loads(
        (root / "remote/V4_OUTPUT_PROVENANCE.json").read_text(encoding="utf-8")
    )
    final = json.loads(
        (root / "remote/FINAL_ACCOUNT_RESULTS.json").read_text(encoding="utf-8")
    )
    assert source.read_bytes() == local_source.read_bytes()
    assert sha256(source) == "d467bc5a1e7c83ae7da780aaf01fb6ac001fd326e514495cae3a9279b7b6301b"
    assert sha256(log_path) == "bc7cfde1adb09278a12c9d623422d07039f3bdac3afe22c5041ea5653832b535"
    # Keep the compact-package provenance contract strict while allowing the
    # separately documented extraction-archive binding block to evolve.  The
    # archive block is intentionally checked below rather than silently
    # discarded by a whole-dict equality assertion.
    expected_provenance = {
        "competition": "ioai-2026-task-4-westlake-nlp-24",
        "kernel": "researai/ioai-2026-task-4-westlake-nlp-24-solution",
        "version": 4,
        "submission_ref": 55316818,
        "remote_filename": "submission.csv",
        "size_bytes": 190117536,
        "sha256": "bdb202711d6494bc94c331d549b0fa7956aa1d9eb585c247ae0dfce723f76542",
        "rows": 200,
        "columns": ["id", "delta_a", "delta_b"],
        "remote_runtime_seconds": 316,
        "public_score": 98.41,
        "stored_in_compact_package": False,
    }
    assert set(provenance) == set(expected_provenance) | {
        "reason_not_stored", "extraction_archive"
    }
    for key, value in expected_provenance.items():
        assert provenance[key] == value
    assert isinstance(provenance["reason_not_stored"], str)
    extraction = provenance["extraction_archive"]
    assert extraction["archive"] == "ioai-kaggle-fetch-researai-20260813.tar.gz"
    assert extraction["archive_sha256"] == (
        "eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c"
    )
    assert extraction["archive_source_sha256"] == sha256(source)
    assert extraction["archive_output_sha256"] == provenance["sha256"]
    assert extraction["archive_source_size_bytes"] == source.stat().st_size
    assert extraction["archive_output_size_bytes"] == provenance["size_bytes"]
    assert extraction["archive_metadata_size_bytes"] == 3494
    assert extraction["archive_log_gzip_size_bytes"] == 4002
    assert extraction["archive_metadata_sha256"] == (
        "3da88345f245f7b46fadb08385c29b8999da7299cb1513013b002f33431735cc"
    )
    assert extraction["archive_log_gzip_sha256"] == (
        "3fddd4688f831d7f68d671f63db4058884233f26bb4310028075384d8f7f1bd2"
    )
    assert extraction["archive_output_path"].endswith(
        "/ioai-2026-task-4-westlake-nlp-24-solution/v4/submission.csv"
    )
    assert extraction["archive_source_path"].endswith(
        "/ioai-2026-task-4-westlake-nlp-24-solution/v4/kernel-source.py"
    )
    assert extraction["archive_metadata_path"].endswith(
        "/ioai-2026-task-4-westlake-nlp-24-solution/v4/kernel-version-metadata.json"
    )
    assert extraction["archive_log_path"].endswith(
        "/ioai-2026-task-4-westlake-nlp-24-solution/v4/run.log.json.gz"
    )
    observation = extraction["archive_metadata_observation"]
    assert observation == {
        "kernel_version_directory": 4,
        "matched_kernel_confidence": [55316818, 55316194, 55315359],
        "matched_version_confidence": [],
        "enable_gpu": True,
        "machine_shape": "NvidiaTeslaT4",
        "enable_internet": False,
        "cuda_device_strings": ["cuda:0"],
        "observed_runtime_seconds": 321.609419295,
        "produced_output_file": True,
        "reused_from_disk": False,
    }
    summary = json.loads((root / "SUMMARY.json").read_text(encoding="utf-8"))
    rule_audit = json.loads((root / "RULE_DIFFERENCE_AUDIT.json").read_text(encoding="utf-8"))
    rule_statuses = {
        item["rule_id"]: item["status"] for item in rule_audit["findings"]
    }
    audited = rule_audit["audited_final_submission"]
    assert rule_statuses["prompt.exact_text"] == "disclosed_deviation"
    assert rule_statuses["submission.folder_two_files"] == (
        "disclosed_process_deviation_remote_artifact_unaffected"
    )
    assert rule_statuses["resources.external_web_research"] == (
        "informational_method_background_not_a_compliance_issue"
    )
    assert rule_statuses["hardware.local_development"] == "jury_interpretation_risk"
    assert audited["submission_ref"] == provenance["submission_ref"]
    assert audited["kernel_version"] == provenance["version"] == 4
    assert audited["source_sha256"] == sha256(source)
    assert audited["output_sha256"] == provenance["sha256"]
    assert audited["public_score"] == provenance["public_score"]
    assert audited["private_score"] == final["official_final_result"]["private_score"]
    version_finding = next(
        item for item in rule_audit["findings"] if item["rule_id"] == "submission.version_budget"
    )
    assert "SUBMISSION_VERSION_AUDIT.json: tasks.task4" in version_finding["evidence"]
    assert "four captured Task 4 notebook versions" in version_finding["conclusion"]
    # Organizer-facing evidence locators must be directly followable.  Reject
    # abbreviated filenames and verify that every cited timestamp is present
    # in the cited local record.
    timestamp_pattern = re.compile(
        r"20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z"
    )
    for finding in rule_audit["findings"]:
        assert finding["evidence"], finding["rule_id"]
        for locator in finding["evidence"]:
            assert "..." not in locator, (finding["rule_id"], locator)
            relative = locator.split(": ", 1)[0]
            evidence_path = (ROOT / relative).resolve()
            assert evidence_path.is_relative_to(ROOT.resolve()), locator
            assert evidence_path.is_file(), locator
            timestamps = timestamp_pattern.findall(locator)
            if timestamps:
                evidence_text = evidence_path.read_text(encoding="utf-8", errors="replace")
                assert all(timestamp in evidence_text for timestamp in timestamps), locator
    assert summary["official_final_submission_refs"] == [provenance["submission_ref"]]
    assert summary["official_final_public_score"] == provenance["public_score"]
    assert summary["official_final_private_score"] == provenance.get("private_score", audited["private_score"])
    assert summary["official_final_trace_alignment"] is True
    assert summary["strict_exact_organizer_prompt_text_conformance"] is False
    assert summary["rule_difference_audit"] == "RULE_DIFFERENCE_AUDIT.json"
    assert final["official_final_result"]["submission_refs"] == [provenance["submission_ref"]]
    assert final["official_final_result"]["public_score"] == provenance["public_score"]
    assert final["autonomous_and_official_deadline_best"]["seconds_before_official_deadline"] > 0
    local_metadata = json.loads(
        (root / "notebooks/kernel-metadata.json").read_text(encoding="utf-8")
    )
    remote_metadata = json.loads(
        (root / "notebooks/REMOTE_CURRENT_METADATA.json").read_text(encoding="utf-8")
    )
    for metadata in (local_metadata, remote_metadata):
        _verify_gpu_notebook_metadata(
            metadata,
            "ioai-2026-task-4-westlake-nlp-24",
            "researai/ioai-2026-task-4-westlake-nlp-24-solution",
        )
    log = json.loads(log_path.read_text(encoding="utf-8"))
    messages = "".join(str(item.get("data", "")) for item in log)
    assert "Device: cuda:0" in messages
    assert "completed 200 of 200 rows" in messages
    assert "wrote /kaggle/working/submission.csv with 200 rows 190117536 bytes" in messages
    max_time = max(float(item["time"]) for item in log)
    assert max_time < 600
    return {
        "all_ok": True,
        "source_exact": True,
        "metadata_contract": True,
        "remote_log_runtime_seconds": max_time,
        "remote_output_in_repository": False,
        "remote_output_provenance_sha256": provenance["sha256"],
        "limitation": "exact 190117536-byte CSV is hash-only in this compact repository",
    }


def verify_task2_artifacts() -> dict[str, object]:
    """Verify the autonomous eligible Task 2 v2 notebook artifact chain."""
    root = ROOT / "task2"
    source = root / "notebooks/rotation-cnn-v2/ioai-task2-westlake-rotation-cnn-v2.py"
    remote_source = root / "notebooks/rotation-v2-remote/ioai-task2-westlake-rotation-cnn-v2.py"
    csv_path = root / "remote/rotation-cnn-v2/submission.csv"
    log_path = root / "remote/rotation-cnn-v2/ioai-task2-westlake-rotation-cnn-v2.log"
    expected_source_sha256 = "942c8b7b33247ae7117ae1f008e704bf17672bb9c75559cdd7a0bac7cb35ef43"
    expected_csv_sha256 = "19cfbca1f4bdede69bb03a77b862e2a4a9495710dde92d31d0da595eb9ac09ba"
    expected_log_sha256 = "070fe51ea6a142b36fd28ca9a251708e4616fc4093b52d90fcfd5bc0f3dd5293"
    assert source.read_bytes() == remote_source.read_bytes()
    assert sha256(source) == expected_source_sha256
    assert sha256(csv_path) == expected_csv_sha256
    assert sha256(log_path) == expected_log_sha256
    metadata = json.loads(
        (root / "notebooks/rotation-cnn-v2/kernel-metadata.json").read_text(encoding="utf-8")
    )
    _verify_gpu_notebook_metadata(
        metadata,
        "ioai-2026-task-2-westlake-nlp-24",
        "researai/ioai-task2-westlake-rotation-cnn-v2",
    )
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == ["id", "prediction"]
        rows = list(reader)
    assert len(rows) == 7200
    ids = [row["id"] for row in rows]
    assert len(set(ids)) == 7200
    assert all(row["prediction"].isdigit() and 0 <= int(row["prediction"]) <= 5 for row in rows)
    log = json.loads(log_path.read_text(encoding="utf-8"))
    messages = "".join(str(item.get("data", "")) for item in log)
    assert "IOAI environment ready (wheels from /kaggle/input/datasets/kamalkhan/ioai-2026-wheel-dataset)" in messages
    assert "best_epoch=13 validation=54.8056 wrote=/kaggle/working/submission.csv rows=7200" in messages
    max_time = max(float(item["time"]) for item in log)
    assert max_time < 300
    eligible = json.loads(
        (root / "remote/KAGGLE_SUBMISSIONS_ELIGIBLE.json").read_text(encoding="utf-8")
    )
    eligible_v2 = next(item for item in eligible if item["ref"] == 55260695)
    assert eligible_v2["publicScore"] == "0.55416"
    assert eligible_v2["status"] == "SubmissionStatus.COMPLETE"
    final = json.loads((root / "remote/FINAL_ACCOUNT_RESULTS.json").read_text(encoding="utf-8"))
    summary = json.loads((root / "SUMMARY.json").read_text(encoding="utf-8"))
    assert final["autonomous_result"] == {
        "submission_ref": 55260695,
        "submitted_at_utc": "2026-08-05T06:19:10.890Z",
        "public_score": 0.55416,
        "private_score": 0.54833,
    }
    assert summary["best_submission_ref"] == 55260695
    assert summary["best_public_score"] == 0.55416
    assert summary["best_private_score"] == 0.54833
    assert summary["official_final_trace_alignment"] is False
    return {
        "all_ok": True,
        "source_exact": True,
        "csv_hash_and_contract": True,
        "rows": 7200,
        "metadata_contract": True,
        "remote_log_runtime_seconds": max_time,
        "autonomous_submission_ref": 55260695,
        "autonomous_public_score": 0.55416,
    }


def verify_task5_artifacts() -> dict[str, object]:
    """Verify exact archived Task 5 v6 output/log and trace-preserved source."""
    root = ROOT / "task5"
    provenance = json.loads((root / "V6_SOURCE_PROVENANCE.json").read_text(encoding="utf-8"))
    source = root / provenance["source"]["path"]
    csv_path = root / provenance["remote_result"]["output_path"]
    log_path = root / provenance["remote_result"]["log_path"]
    assert source.stat().st_size == provenance["source"]["size_bytes"]
    assert sha256(source) == provenance["source"]["sha256"]
    assert provenance["preserved_run_copy"]["byte_identical_to_packaged_source"] is True
    assert provenance["preserved_run_copy"]["sha256_at_package_audit"] == sha256(source)
    assert sha256(csv_path) == provenance["remote_result"]["output_sha256"]
    assert sha256(log_path) == provenance["remote_result"]["log_sha256"]
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == ["id", "boundary_char_index"]
        rows = list(reader)
    assert len(rows) == 760
    assert len({row["id"] for row in rows}) == 760
    assert all(
        row["boundary_char_index"].lstrip("-").isdigit()
        and int(row["boundary_char_index"]) >= 0
        for row in rows
    )
    final = json.loads(
        (root / "remote/FINAL_ACCOUNT_RESULTS.json").read_text(encoding="utf-8")
    )
    summary = json.loads((root / "SUMMARY.json").read_text(encoding="utf-8"))
    compliance = (root / "COMPLIANCE.md").read_text(encoding="utf-8")
    assert provenance["classification"] == (
        "preserved formal-run source; not independently redownloaded historical source"
    )
    assert summary["historical_remote_source_retrievable"] is False
    assert summary["historical_remote_output_included"] is True
    assert "HTTP 403" in provenance["limitation"]
    assert "independent post-run source download" in provenance["limitation"]
    assert "HTTP 403" in compliance
    assert "preserved from the formal run" in compliance
    assert "source is\ntherefore classified as the source preserved from the formal run" in compliance
    assert summary["official_final_submission_refs"] == [provenance["submission_ref"]]
    assert summary["official_final_public_score"] == provenance["remote_result"]["public_score"]
    assert summary["official_final_trace_alignment"] is True
    assert final["official_final_result"]["submission_refs"] == [provenance["submission_ref"]]
    assert final["official_final_result"]["public_score"] == provenance["remote_result"]["public_score"]
    assert final["official_deadline_best_public_and_private"]["submitted_at_utc"] == (
        provenance["remote_result"]["submitted_at_utc"]
    )
    for metadata_path in (
        root / "notebooks/kernel-metadata.json",
        root / "notebooks/REMOTE_CURRENT_METADATA.json",
    ):
        _verify_gpu_notebook_metadata(
            json.loads(metadata_path.read_text(encoding="utf-8")),
            "ioai-2026-task-5-westlake-nlp-24",
            "researai/ioai-2026-ghost-of-the-machine-solution",
        )
    log = json.loads(log_path.read_text(encoding="utf-8"))
    messages = "".join(str(item.get("data", "")) for item in log)
    assert "device=cuda:0 gpu=Tesla T4" in messages
    assert "wrote /kaggle/working/submission.csv with 760 rows" in messages
    max_time = max(float(item["time"]) for item in log)
    assert max_time < 600
    return {
        "all_ok": True,
        "source_hash_and_trace_provenance": True,
        "csv_hash_and_contract": True,
        "rows": 760,
        "metadata_contract": True,
        "remote_log_runtime_seconds": max_time,
        "limitation": provenance["limitation"],
    }


def verify_cross_task_rule_audit() -> dict[str, object]:
    audit = json.loads((ROOT / "RULE_COMPLIANCE_AUDIT.json").read_text(encoding="utf-8"))
    assert audit["all_six_strictly_compliant_claim_supported"] is False
    tasks = audit["tasks"]
    prompt_audit = json.loads(
        (ROOT / "PROMPT_CONFORMANCE_AUDIT.json").read_text(encoding="utf-8")
    )
    for task_number in range(1, 7):
        task = f"task{task_number}"
        summary = json.loads((ROOT / task / "SUMMARY.json").read_text(encoding="utf-8"))
        rule = tasks[task]
        for relative in rule.get("evidence", []):
            target = (ROOT / relative).resolve()
            assert target.is_relative_to(ROOT.resolve()), (task, relative)
            assert target.is_file(), (task, relative)
        formal_prefix = rule.get("formal_prefix")
        if formal_prefix:
            for key in ("path", "audit"):
                target = (ROOT / formal_prefix[key]).resolve()
                assert target.is_relative_to(ROOT.resolve()), (task, formal_prefix[key])
                assert target.is_file(), (task, formal_prefix[key])
        prompt = prompt_audit["tasks"][task]
        assert summary["official_final_submission_refs"] == rule["official_final_submission_refs"]
        assert summary["official_final_trace_alignment"] is rule["official_final_trace_alignment"]
        assert summary["official_final_trace_alignment"] is (
            task_number >= 3
        ), task
        summary_prompt_status = summary.get("strict_exact_organizer_prompt_text_conformance")
        if summary_prompt_status is None:
            summary_prompt_status = summary["canonical_autonomous_rollout"][
                "strict_exact_organizer_prompt_text_conformance"
            ]
        assert summary_prompt_status is rule["strict_exact_organizer_prompt_text_conformance"]
        assert prompt["strict_exact_organizer_prompt_text_conformance"] is (
            rule["strict_exact_organizer_prompt_text_conformance"]
        )
        assert prompt["live_kaggle_page_matches_repository_source"] is True
        assert prompt["no_live_human_prompt_events_included"] is True
        if task_number == 3:
            official_pages = json.loads(
                (ROOT / "task3/official/OFFICIAL_PAGES_FULL.json").read_text(encoding="utf-8")
            )
            continuation = next(
                item["content"]
                for item in official_pages
                if item.get("name") == "Continuation Prompt"
            )
            assert (
                ROOT / "task3/official/CONTINUE_PROMPT_EXACT.md"
            ).read_text(encoding="utf-8") == continuation

    assert tasks["task1"]["official_final_trace_alignment"] is False
    assert tasks["task2"]["official_final_trace_alignment"] is False
    assert tasks["task3"]["official_final_trace_alignment"] is True
    assert tasks["task3"]["submission_counts"] == {
        "all_account": 27,
        "before_official_deadline": 11,
        "after_official_deadline": 16,
        "published_limit": 15,
    }
    task3_summary = json.loads((ROOT / "task3/SUMMARY.json").read_text(encoding="utf-8"))
    assert task3_summary["submissions_before_autonomy_boundary"] == 8
    task3_final = json.loads(
        (ROOT / "task3/remote/FINAL_ACCOUNT_RESULTS.json").read_text(encoding="utf-8")
    )
    task3_session = json.loads(
        (ROOT / "task3/environment/session.json").read_text(encoding="utf-8")
    )
    task3_submission_copy = (
        ROOT / "task3/official/SUBMISSION_WORKING_COPY.md"
    ).read_text(encoding="utf-8")
    assert task3_session["deadlineAt"] == "2026-08-06T06:26:44.395Z"
    assert task3_final["official_competition_deadline_utc"] == "2026-08-06T06:30:00Z"
    assert "official Kaggle\ndeadline was `2026-08-06T06:30:00Z`" in task3_submission_copy
    assert "run deadline `2026-08-06T06:26:44.395Z`" in task3_submission_copy
    assert task3_final["submission_counts"]["before_autonomy_boundary"] == (
        task3_summary["submissions_before_autonomy_boundary"]
    )
    assert {
        "all_account": task3_summary["account_submission_count"],
        "before_official_deadline": task3_summary["submissions_before_official_deadline"],
        "after_official_deadline": task3_summary["submissions_after_official_deadline"],
        "published_limit": task3_summary["published_scored_submission_limit"],
    } == tasks["task3"]["submission_counts"]
    assert tasks["task4"]["strict_exact_organizer_prompt_text_conformance"] is False
    assert tasks["task4"]["selected_trace_files"] == 12
    task4_summary = json.loads((ROOT / "task4/SUMMARY.json").read_text(encoding="utf-8"))
    task4_rule = json.loads((ROOT / "task4/RULE_DIFFERENCE_AUDIT.json").read_text(encoding="utf-8"))
    task4_provenance = json.loads(
        (ROOT / "task4/remote/V4_OUTPUT_PROVENANCE.json").read_text(encoding="utf-8")
    )
    task4_extraction = task4_provenance["extraction_archive"]
    assert task4_extraction["archive_sha256"] == (
        "eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c"
    )
    assert task4_extraction["archive_source_sha256"] == sha256(
        ROOT / "task4/notebooks/REMOTE_CURRENT_V4.py"
    )
    assert task4_extraction["archive_output_sha256"] == task4_provenance["sha256"]
    assert task4_extraction["archive_source_size_bytes"] == (
        ROOT / "task4/notebooks/REMOTE_CURRENT_V4.py"
    ).stat().st_size
    assert task4_extraction["archive_output_size_bytes"] == task4_provenance[
        "size_bytes"
    ]
    assert task4_extraction["archive_metadata_observation"]["matched_version_confidence"] == []
    assert task4_extraction["archive_metadata_observation"]["kernel_version_directory"] == 4
    task4_final = json.loads(
        (ROOT / "task4/remote/FINAL_ACCOUNT_RESULTS.json").read_text(encoding="utf-8")
    )
    assert task4_summary["canonical_trace_files"] == tasks["task4"]["selected_trace_files"]
    assert task4_summary["rule_difference_audit"] == "RULE_DIFFERENCE_AUDIT.json"
    assert task4_rule["audited_final_submission"]["submission_ref"] == task4_summary[
        "official_final_submission_refs"
    ][0]
    assert task4_summary["official_final_submission_refs"][0] == task4_provenance[
        "submission_ref"
    ]
    assert task4_provenance["submission_ref"] == task4_final["official_final_result"][
        "submission_refs"
    ][0]
    assert task4_rule["audited_final_submission"]["source_sha256"] == sha256(
        ROOT / "task4/notebooks/REMOTE_CURRENT_V4.py"
    )
    assert task4_rule["audited_final_submission"]["output_sha256"] == task4_provenance[
        "sha256"
    ]
    assert task4_rule["audited_final_submission"]["public_score"] == task4_provenance[
        "public_score"
    ]
    assert task4_rule["audited_final_submission"]["private_score"] == task4_final[
        "official_final_result"
    ]["private_score"]
    task4_statuses = {item["rule_id"]: item["status"] for item in task4_rule["findings"]}
    assert task4_statuses["prompt.exact_text"] == "disclosed_deviation"
    assert task4_statuses["submission.folder_two_files"] == (
        "disclosed_process_deviation_remote_artifact_unaffected"
    )
    assert task4_statuses["resources.external_web_research"] == (
        "informational_method_background_not_a_compliance_issue"
    )
    assert task4_statuses["hardware.local_development"] == "jury_interpretation_risk"
    assert {
        "substantive_non_exact_continuation",
        "transient_local_push_folder_pycache",
        "two_arxiv_searches_retained_as_provenance_not_a_method_research_violation",
        "local_h100_hardware_scope_interpretation",
    }.issubset(set(tasks["task4"]["disclosures"]))
    assert tasks["task5"]["official_final_trace_alignment"] is True
    assert tasks["task6"]["batch_dependence_fixture"]["final_prediction_changes"] == 5
    task5_summary = json.loads((ROOT / "task5/SUMMARY.json").read_text(encoding="utf-8"))
    task5_provenance = json.loads((ROOT / "task5/V6_SOURCE_PROVENANCE.json").read_text(encoding="utf-8"))
    task5_compliance = (ROOT / "task5/COMPLIANCE.md").read_text(encoding="utf-8")
    assert task5_provenance["classification"] == (
        "preserved formal-run source; not independently redownloaded historical source"
    )
    assert task5_summary["historical_remote_source_retrievable"] is False
    assert "HTTP 403" in task5_provenance["limitation"]
    assert "HTTP 403" in task5_compliance
    assert {
        "external_literature_used_as_method_background_not_treated_as_compliance_issue",
        "historical_v6_source_preserved_from_trace_but_not_independently_redownloaded",
        "exhaustive_local_h100_runtime_unavailable",
    }.issubset(set(tasks["task5"]["disclosures"]))
    task6_summary = json.loads((ROOT / "task6/SUMMARY.json").read_text(encoding="utf-8"))
    task6_rule = json.loads((ROOT / "task6/RULE_DIFFERENCE_AUDIT.json").read_text(encoding="utf-8"))
    assert task6_summary["batch_dependence_fixture"] == tasks["task6"]["batch_dependence_fixture"]
    assert task6_summary["rule_difference_audit"] == "RULE_DIFFERENCE_AUDIT.json"
    assert task6_summary["historical_report_factual_error_disclosed"] is True
    assert task6_rule["statuses"]["result.trace_alignment"] == "evidence_supported_compliant"
    assert task6_rule["statuses"]["prompt.exact_text"] == "evidence_supported_compliant"
    assert task6_rule["statuses"]["model.evaluator_batch_dependence"] == (
        "measured_technical_behavior_not_treated_as_compliance_issue"
    )
    assert task6_rule["statuses"]["protected_field.hidden_geometry"] == (
        "measured_technical_behavior_not_treated_as_compliance_issue"
    )
    assert task6_rule["statuses"]["source.technical_report"] == "disclosed_factual_error"
    assert {
        "evaluator_batch_dependent_predictions_measured_not_treated_as_violation",
        "hidden_geometry_batch_context_measured_not_treated_as_compliance_issue",
        "historical_report_dropout_and_range_error",
        "exhaustive_local_h100_runtime_unavailable",
    }.issubset(set(tasks["task6"]["disclosures"]))
    for task in ("task1", "task2", "task3"):
        assert audit["tasks"][task]["informational_disclosures"] == [
            "method_background_research_not_treated_as_compliance_issue"
        ]
    assert audit["tasks"]["task1"]["formal_prefix"] == {
        "path": "task1/evidence/rollouts/rollout-2026-08-05T17-20-55-019fd139-d180-7171-ac0b-c037e11866eb.jsonl",
        "audit": "FORMAL_PREFIX_AUDIT.json",
        "strict_exact_organizer_prompt_text_conformance": True,
        "preboundary_submission": None,
    }
    assert audit["tasks"]["task2"]["formal_prefix"] == {
        "path": "task2/evidence/rollouts/rollout-2026-08-05T13-30-31-019fd066-e338-71a0-9d8e-6e1d154c5a79.jsonl",
        "audit": "FORMAL_PREFIX_AUDIT.json",
        "strict_exact_organizer_prompt_text_conformance": True,
        "preboundary_submission": 55260695,
    }
    assert audit["cost_accounting"]["local_gpu_runtime"] == "incomplete_tasks_4_to_6"
    return {
        "tasks": len(tasks),
        "all_six_strictly_compliant_claim_supported": False,
    }


def verify_requirement_evidence_matrix() -> dict[str, object]:
    """Check the rule-by-rule navigation index without certifying eligibility."""
    path = ROOT / "REQUIREMENT_EVIDENCE_MATRIX.json"
    matrix = json.loads(path.read_text(encoding="utf-8"))
    assert matrix["schema"] == "ioai.requirement-evidence-matrix.v1"
    assert matrix["overall"]["strict_all_six_claim"] is False
    assert set(matrix["tasks"]) == {f"task{i}" for i in range(1, 7)}
    expected_requirements = {
        "trace_no_live_human", "final_trace_alignment", "exact_prompt_text",
        "notebook_only", "version_budget", "runtime_cap", "internet_resources",
        "hardware", "output_artifacts", "technical_report", "official_deadline",
    }
    competitions = {
        1: "ioai-2026-task-1-westlake-nlp-24",
        2: "ioai-2026-task-2-westlake-nlp-24",
        3: "ioai-2026-task-3-westlake-nlp-48",
        4: "ioai-2026-task-4-westlake-nlp-24",
        5: "ioai-2026-task-5-westlake-nlp-24",
        6: "ioai-2026-task-6-westlake-nlp-60",
    }
    for task, data in matrix["tasks"].items():
        assert set(data["requirements"]) == expected_requirements, task
        number = int(task.removeprefix("task"))
        assert data["competition"] == competitions[number]
        for requirement, item in data["requirements"].items():
            assert item["requirement"] and item["official_source"] and item["scope"]
            assert item["evidence"] and item["note"]
            assert all((ROOT / evidence).exists() for evidence in item["evidence"]), (task, requirement)

    # Task 1/2 extraction records are candidates, not silently upgraded final
    # artifacts.  Check the provenance records' explicit uncertainty and the
    # metadata observations used by the matrix.
    expected_candidate_refs = {1: [55267333, 55267368], 2: 55261432}
    for number in (1, 2):
        candidate = json.loads(
            (ROOT / f"task{number}/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json").read_text(
                encoding="utf-8"
            )
        )
        assert candidate["schema"] == "ioai.extracted-official-final-artifact-candidate.v1"
        assert candidate["confidence"] == "kernel_linked_candidate_not_byte_confirmed_exact_version"
        assert candidate["archive_sha256"] == (
            "eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c"
        )
        refs = candidate.get("official_submission_refs", candidate.get("official_submission_ref"))
        assert refs == expected_candidate_refs[number]
        metadata = candidate["candidate_metadata_summary"]
        assert metadata["enable_internet"] is False
        assert metadata["machine_shape"] == "NvidiaTeslaT4"
        assert metadata["cuda_device_strings"] == ["cuda:0"]
        assert metadata["multi_device_suspicion"] is False
        output = candidate["candidate_output_observation"]
        assert output["produced_output_file"] is True
        assert output["reused_from_disk"] is False
        assert output["data_row_count"] in {200, 7200}

    # Exact prompt snapshots must be byte-equal to the stored page bodies.
    for task in (4, 5, 6):
        pages = json.loads(
            (ROOT / f"task{task}/official/OFFICIAL_PAGES_FULL.json").read_text(encoding="utf-8")
        )
        for page_name, filename in (
            ("Starter Prompt", "STARTER_PROMPT_EXACT.md"),
            ("Continuation Prompt", "CONTINUE_PROMPT_EXACT.md"),
        ):
            expected = next(item["content"] for item in pages if item.get("name") == page_name)
            actual = (ROOT / f"task{task}/official/{filename}").read_text(encoding="utf-8")
            assert actual == expected, (task, filename)
    return {
        "all_ok": True,
        "tasks": {task: len(data["requirements"]) for task, data in matrix["tasks"].items()},
        "strict_all_six_claim": matrix["overall"]["strict_all_six_claim"],
    }


def verify_submission_version_audit() -> dict[str, object]:
    """Verify literal budget/version-reuse findings without greenwashing them."""
    audit = json.loads((ROOT / "SUBMISSION_VERSION_AUDIT.json").read_text(encoding="utf-8"))
    assert audit["schema"] == "ioai.submission-version-audit.v1"
    assert audit["source_archive_sha256"] == (
        "eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c"
    )
    assert audit["extraction_summary_sha256"] == sha256(
        ROOT / "KAGGLE_EXTRACTION_SUMMARY.json"
    )
    assert set(audit["tasks"]) == {f"task{i}" for i in range(1, 7)}
    assert audit["overall"] == {
        "tasks_with_literal_budget_excess": ["task1", "task3"],
        "tasks_with_repeated_script_version_submission": ["task1", "task2", "task3"],
        "strict_all_six_budget_and_version_reuse_claim_supported": False,
    }
    expected_budget = {
        "task1": (20, 38, "known_deviation_under_published_wording"),
        "task2": (20, 18, "evidence_supported_account_extraction_scope"),
        "task3": (15, 27, "known_deviation_under_published_wording"),
        "task4": (20, 4, "evidence_supported_account_extraction_scope"),
        "task5": (15, 7, "evidence_supported_account_extraction_scope"),
        "task6": (20, 8, "evidence_supported_account_extraction_scope"),
    }
    expected_duplicates = {
        "task1": {
            340342513: [55267333, 55267368],
            340345171: [55267587, 55267607, 55267647],
        },
        "task2": {340290308: [55260462, 55260695]},
        "task3": {340521169: [55290807, 55290810]},
        "task4": {},
        "task5": {},
        "task6": {},
    }
    for task, item in audit["tasks"].items():
        limit, observed, status = expected_budget[task]
        assert item["official_budget_limit"] == limit
        assert item["observed_budget_count"] == observed
        assert item["budget_literal_status"] == status
        assert item["submission_status_counts"] == {
            "COMPLETE": item["submission_record_count"]
        }
        groups = {
            group["script_version_id"]: group["submission_refs"]
            for group in item["duplicate_script_version_groups"]
        }
        assert groups == expected_duplicates[task]
        for group in item["duplicate_script_version_groups"]:
            for observation in group["observations"]:
                assert observation["submitted_at_utc"].endswith("Z")
        pages = json.loads(
            (ROOT / f"{task}/official/OFFICIAL_PAGES_FULL.json").read_text(encoding="utf-8")
        )
        rules = next(page["content"] for page in pages if page.get("name") == "rules")
        assert item["one_submission_per_version_rule"] in rules
        summary = json.loads((ROOT / f"{task}/SUMMARY.json").read_text(encoding="utf-8"))
        summary_audit = summary["submission_version_audit"]
        assert summary_audit["path"] == "../SUBMISSION_VERSION_AUDIT.json"
        assert summary_audit["task_key"] == task
        assert summary_audit["official_budget_kind"] == item["official_budget_kind"]
        assert summary_audit["official_budget_limit"] == item["official_budget_limit"]
        assert summary_audit["observed_budget_count"] == item["observed_budget_count"]
        assert summary_audit["literal_budget_conflict"] is (
            item["observed_budget_count"] > item["official_budget_limit"]
        )
        assert summary_audit["literal_version_reuse_conflict"] is bool(
            item["duplicate_script_version_groups"]
        )
        assert summary_audit["duplicate_script_version_group_count"] == len(
            item["duplicate_script_version_groups"]
        )
        assert summary_audit["combined_literal_status"] == item[
            "combined_budget_and_reuse_status"
        ]
        if task == "task1":
            assert summary_audit["official_final_refs_share_script_version_id"] == 340342513
        elif task in {"task2", "task3"}:
            repeated_group = item["duplicate_script_version_groups"][0]
            assert summary_audit["reused_script_version_id"] == repeated_group[
                "script_version_id"
            ]
            assert summary_audit["reused_submission_refs"] == repeated_group[
                "submission_refs"
            ]
        final_refs = summary["official_final_submission_refs"]
        assert item["official_final_submission_refs"] == final_refs
    assert audit["tasks"]["task1"]["official_final_refs_affected_by_version_reuse"] == [
        55267333, 55267368
    ]
    assert audit["tasks"]["task2"]["official_final_refs_affected_by_version_reuse"] == []
    assert audit["tasks"]["task3"]["unknown_script_version_id_records"] == 2
    assert (ROOT / "SUBMISSION_VERSION_AUDIT.md").is_file()
    assert (ROOT / "tools/build_submission_version_audit.py").is_file()
    return {
        "all_ok": True,
        "literal_budget_excess_tasks": ["task1", "task3"],
        "repeated_version_tasks": ["task1", "task2", "task3"],
        "official_final_version_reuse_tasks": ["task1"],
        "compliance_certificate": False,
    }


def verify_kaggle_extraction_summary() -> dict[str, object]:
    """Bind the external extraction summary to every task package.

    The extraction summary and the task packages are independently useful
    records. This cross-check makes their shared account counts, deadlines,
    competition slugs, and captured-version totals auditable instead of
    relying on a reviewer to notice drift between files.
    """
    extraction_path = ROOT / "KAGGLE_EXTRACTION_SUMMARY.json"
    extraction = json.loads(extraction_path.read_text(encoding="utf-8"))
    assert extraction["tool_version"] == "1.0.0"
    assert extraction["username"] == "researai"
    assert len(extraction["competitions"]) == 6
    extraction_sha = sha256(extraction_path)
    by_competition = {item["competition"]: item for item in extraction["competitions"]}
    assert len(by_competition) == 6

    checked: list[dict[str, object]] = []
    for number in range(1, 7):
        task = f"task{number}"
        task_summary = json.loads((ROOT / task / "SUMMARY.json").read_text(encoding="utf-8"))
        binding = task_summary["extraction_summary_binding"]
        competition = task_summary["competition"]
        source = by_competition[competition]
        assert binding["source_path"] == "../KAGGLE_EXTRACTION_SUMMARY.json", task
        assert binding["source_sha256"] == extraction_sha, task
        assert binding["competition"] == competition, task
        assert binding["deadline_utc"] == source["deadline_utc"].replace(" ", "T") + "Z", task
        assert task_summary["official_competition_deadline_utc"] == binding["deadline_utc"], task
        for field in ("submissions", "submissions_after_deadline", "versions_captured", "kernels"):
            assert binding[field] == source[field], (task, field)
        if "captured_account_notebook_versions" in task_summary:
            assert task_summary["captured_account_notebook_versions"] == source["versions_captured"], task

        final = json.loads(
            (ROOT / task / "remote" / "FINAL_ACCOUNT_RESULTS.json").read_text(encoding="utf-8")
        )
        assert final["competition"] == competition, task
        assert final["official_competition_deadline_utc"] == binding["deadline_utc"], task
        counts = final["submission_counts"]
        assert counts["all_account"] == source["submissions"], task
        assert counts["after_official_deadline"] == source["submissions_after_deadline"], task
        assert task_summary["account_submission_count"] == source["submissions"], task
        assert task_summary["submissions_after_official_deadline"] == source[
            "submissions_after_deadline"
        ], task
        checked.append(
            {
                "task": task,
                "competition": competition,
                "submissions": source["submissions"],
                "submissions_after_deadline": source["submissions_after_deadline"],
                "versions_captured": source["versions_captured"],
                "kernels": source["kernels"],
            }
        )
    return {"all_ok": True, "source_sha256": extraction_sha, "tasks": checked}


def verify_execution_accounting() -> dict[str, int]:
    index = json.loads((ROOT / "EXECUTION_TRACE_INDEX.json").read_text(encoding="utf-8"))
    costs = json.loads((ROOT / "COSTS.json").read_text(encoding="utf-8"))
    assert index["schema"] == "ioai.execution-trace-index.v1"
    assert costs["schema"] == "ioai.execution-costs.v1"
    assert costs["api_cost_total_status"] == (
        "unavailable_no_provider_invoice_or_applicable_public_rate"
    )
    assert costs["api_cost_usd_total"] is None
    assert costs["gpu_compute_accounting_status"] == (
        "remote_kaggle_runtime_complete_selected_scope_local_development_incomplete"
    )
    assert costs["gpu_cost_total_status"] == (
        "incomplete_local_runtime_and_unavailable_rate"
    )
    assert costs["gpu_cost_usd_total"] is None
    tokens = 0
    traces = 0
    for task, data in index["tasks"].items():
        cost_task = costs["tasks"][task]
        task_summary = json.loads(
            (ROOT / task / "SUMMARY.json").read_text(encoding="utf-8")
        )
        assert cost_task["competition"] == task_summary["competition"], task
        assert cost_task["model_provider"] == "ioai_allowed", task
        assert cost_task["model"] == "gpt-5.6-sol", task
        assert cost_task["reasoning_effort"] in {"max", "xhigh"}, task
        assert cost_task["api_cost_usd"] is None, task
        token_usage = cost_task["token_usage"]
        assert set(token_usage) >= set(TOKEN_FIELDS), task
        verify_token_vector(token_usage, task)
        assert token_usage == {
            field: data["token_usage_cumulative_sum_across_traces"][field]
            for field in TOKEN_FIELDS
        }, task
        gpu = cost_task["gpu"]
        assert "accelerator" in gpu and "runtime_seconds" in gpu, task
        assert float(gpu["runtime_seconds"]) >= 0, task
        assert math.isclose(
            float(gpu["runtime_hours"]), float(gpu["runtime_seconds"]) / 3600,
            rel_tol=0, abs_tol=1e-12,
        ), task
        assert gpu["gpu_cost_usd"] is None or gpu["gpu_cost_usd"] == 0, task
        task_tokens = data["token_usage_cumulative_sum_across_traces"]["total_tokens"]
        assert costs["tasks"][task]["token_usage"]["total_tokens"] == task_tokens, task
        # COSTS.json is the public execution-accounting view.  Keep its
        # per-task model and complete token vector in lockstep with the
        # autonomous index so a stale summary cannot silently pass on total
        # tokens alone.
        public_cost_task = costs["tasks"][task]
        assert public_cost_task["competition"] == cost_task["competition"], task
        assert public_cost_task["model_provider"] == cost_task["model_provider"], task
        assert public_cost_task["model"] == cost_task["model"], task
        assert public_cost_task["reasoning_effort"] == cost_task["reasoning_effort"], task
        assert public_cost_task["token_usage"] == token_usage, task
        public_gpu = public_cost_task["gpu"]
        assert float(public_gpu["runtime_seconds"]) >= 0, task
        assert math.isclose(
            float(public_gpu["runtime_hours"]), float(public_gpu["runtime_seconds"]) / 3600,
            rel_tol=0, abs_tol=1e-12,
        ), task
        if task in {"task4", "task5", "task6"}:
            gpu = costs["tasks"][task]["gpu"]
            assert gpu["local_development_runtime_seconds"] is None, task
            assert gpu["local_development_gpu_cost_usd"] is None, task
        tokens += task_tokens
        traces += len(data["trace_files"])
    assert costs["known_token_total_all_tasks"] == tokens
    assert len(index["tasks"]["task6"]["trace_files"]) == 3
    assert index["tasks"]["task6"]["token_usage_cumulative_sum_across_traces"]["total_tokens"] == 41371859
    return {"trace_files": traces, "tokens": tokens}


def verify_reproduction_material() -> dict[str, int]:
    """Verify the separately scoped later Task 1/2 reproduction package."""
    manifest = ROOT / "REPRODUCTION_MATERIAL_MANIFEST.sha256"
    checked = 0
    manifest_paths: set[str] = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        assert relative not in manifest_paths, relative
        manifest_paths.add(relative)
        target = (ROOT / relative).resolve()
        assert target.is_relative_to(ROOT.resolve()), relative
        assert sha256(target) == expected, relative
        checked += 1

    index = json.loads((ROOT / "REPRODUCTION_TRACE_INDEX.json").read_text(encoding="utf-8"))
    costs = json.loads((ROOT / "REPRODUCTION_COSTS.json").read_text(encoding="utf-8"))
    assert costs["schema"] == "ioai.later-reproduction-costs.v1"
    assert costs["api_cost_usd_total"] is None
    assert costs["gpu_cost_usd_total"] is None
    assert index["schema"] == "ioai.later-reproduction-trace-material.v1"
    events = 0
    tokens = 0
    traces = 0
    allowed_prompt_classes = {
        "startup_instructions",
        "exact_organizer_starter_prompt",
        "exact_organizer_continuation_prompt",
        "custom_starter_prompt",
        "custom_continuation_prompt",
    }
    for task in ("task1", "task2"):
        data = index["tasks"][task]
        cost_task = costs["tasks"][task]
        assert cost_task["competition"] == data["competition"], task
        assert cost_task["model_provider"] == "ioai_allowed", task
        assert cost_task["model"] == "gpt-5.6-sol", task
        assert cost_task["reasoning_effort"] == "max", task
        assert cost_task["api_cost_usd"] is None, task
        trace_tokens = data["trace_file"]["token_usage_cumulative_final"]
        verify_token_vector(trace_tokens, task)
        assert cost_task["trace_token_usage"] == {
            field: trace_tokens[field] for field in TOKEN_FIELDS
        }, task
        assert cost_task["gpu"]["gpu_cost_usd"] is None, task
        assert data["post_deadline"] is True
        assert data["ranking_eligible"] is False
        assert data["strict_exact_organizer_prompt_text_conformance"] is False
        assert data["canonical_autonomous_trace"] is (task == "task2")
        if task == "task1":
            assert data["canonical_solution_prefix"] == "task1/evidence/canonical/rollout-solution-prefix.jsonl"
        trace = data["trace_file"]
        path = ROOT / trace["path"]
        assert trace["path"] in manifest_paths, trace["path"]
        assert sha256(path) == trace["published_sha256"], trace["path"]
        line_count = 0
        max_tokens = None
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                line_count += 1
                event = json.loads(line)
                payload = event.get("payload", {})
                if event.get("type") == "event_msg" and payload.get("type") == "token_count":
                    total = payload.get("info", {}).get("total_token_usage", {})
                    if isinstance(total.get("total_tokens"), int):
                        max_tokens = max(max_tokens or 0, total["total_tokens"])
        assert line_count == trace["event_count"], task
        assert max_tokens == trace["token_usage_cumulative_final"]["total_tokens"], task
        assert trace["manual_human_prompt_events_included"] == 0, task
        assert set(trace["user_prompt_classes"]).issubset(allowed_prompt_classes), task
        assert sum(trace["user_prompt_classes"].values()) == trace["message_counts"]["user"], task
        events += line_count
        tokens += max_tokens
        traces += 1
    return {"manifest_files": checked, "trace_files": traces, "events": events, "tokens": tokens}


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
        expected_alignment = task >= 3
        assert summary["official_final_trace_alignment"] is expected_alignment, task
        if task == 3:
            assert summary["account_submission_count"] == 27
            assert summary["published_scored_submission_limit"] == 15
            assert summary["historical_report_status"] == (
                "nonconforming_length_and_v8_local_score_error_disclosed"
            )
        task_report = {
            "manifest_files": verify_manifest(root),
            "package_positive_claim": {
                "scope": PACKAGE_POSITIVE_CLAIM_SCOPES[task],
                "submission_refs": submission if isinstance(submission, list) else [submission],
                "public_score": score,
            },
        }
        task_report["final_account_result"] = verify_final_account_result(task, summary)
        report["tasks"][f"task{task}"] = task_report
    report["autonomous_material"] = verify_autonomous_material()
    report["published_execution_accounting"] = verify_execution_accounting()
    report["later_reproduction_material"] = verify_reproduction_material()
    report["task1_package_replay"] = verify_task1_package()
    report["task2_artifact_chain"] = verify_task2_artifacts()
    report["task3_package_replay"] = verify_task3_package()
    report["formal_prefix_audit"] = verify_formal_prefix_audit()
    report["task4_artifact_chain"] = verify_task4_artifacts()
    report["task5_artifact_chain"] = verify_task5_artifacts()
    report["task6_exact_artifacts"] = verify_task6_artifacts()
    report["cross_task_rule_audit"] = verify_cross_task_rule_audit()
    report["requirement_evidence_matrix"] = verify_requirement_evidence_matrix()
    report["submission_version_audit"] = verify_submission_version_audit()
    report["kaggle_extraction_summary_crosscheck"] = verify_kaggle_extraction_summary()
    report["publication_safety"] = verify_publication_safety()
    report["markdown_links"] = verify_markdown_links()
    delivery = json.loads((ROOT / "KAGGLE_EXTRACTION_DELIVERY.json").read_text(encoding="utf-8"))
    assert delivery["archive"]["size_bytes"] == 496870419
    assert delivery["archive"]["entry_count"] == 1401
    assert delivery["archive"]["sha256"] == "eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c"
    assert delivery["google_drive"]["file_id"] == "1c9yRn5SUo6LOPDrHLrAVjj-9JLFti9Vz"
    live_drive = delivery["google_drive"]["live_head_check"]
    assert live_drive["view_http_status"] == 200
    assert live_drive["download_get_http_status"] == 200
    assert live_drive["download_head_http_status"] == 200
    assert live_drive["content_length_bytes"] == delivery["archive"]["size_bytes"]
    assert live_drive["content_disposition_filename"] == delivery["archive"]["filename"]
    assert live_drive["accept_ranges"] == "bytes"
    checklist = json.loads((ROOT / "ORGANIZER_SUBMISSION.json").read_text(encoding="utf-8"))
    assert checklist["status"] == (
        "complete_evidence_package_with_known_compliance_and_cost_limits"
    )
    assert checklist["organizer_review_guide"] == "ORGANIZER_REVIEW_GUIDE.md"
    assert (ROOT / checklist["organizer_review_guide"]).is_file()
    assert checklist["requirement_evidence_matrix"] == {
        "json": "REQUIREMENT_EVIDENCE_MATRIX.json",
        "markdown": "REQUIREMENT_EVIDENCE_MATRIX.md",
        "builder": "tools/build_requirement_evidence_matrix.py",
        "status": "complete_scope_labeled_rule_by_rule_index_not_a_compliance_certificate",
    }
    submission_limits = checklist["requirements"]["submission_version_limits"]
    assert submission_limits["task_summary_paths"] == [
        f"task{i}/SUMMARY.json" for i in range(1, 7)
    ]
    for relative in submission_limits["task_summary_paths"]:
        assert (ROOT / relative).is_file()
    assert (ROOT / checklist["requirement_evidence_matrix"]["json"]).is_file()
    assert (ROOT / checklist["requirement_evidence_matrix"]["markdown"]).is_file()
    assert checklist["access_control"] == {
        "repository_visibility": "private_authorized_review_only_while_restricted_data_is_present",
        "restricted_path": "task3/input/competition/",
        "handling_instructions": "task3/DATA_PROVENANCE.md",
        "audit": "ACCESS_CONTROL_AUDIT.json",
        "audit_markdown": "ACCESS_CONTROL_AUDIT.md",
    }
    access_audit = json.loads((ROOT / "ACCESS_CONTROL_AUDIT.json").read_text(encoding="utf-8"))
    assert access_audit["schema"] == "ioai.access-control-audit.v1"
    assert access_audit["repository"]["visibility"] == "PRIVATE"
    assert access_audit["repository"]["restricted_path"] == "task3/input/competition/"
    assert access_audit["external_drive_archive"]["sha256"] == (
        "eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c"
    )
    assert access_audit["archive_content_audit"]["data_like_path_heuristic_matches"] == 0
    assert (ROOT / "ACCESS_CONTROL_AUDIT.md").is_file()
    assert set(checklist["task_packages"]) == {f"task{i}" for i in range(1, 7)}
    expected_official_sources = {
        "task1": [
            "task1/official/OFFICIAL_PAGES_FULL.json",
            "task1/official/STARTER_PROMPT.md",
            "task1/official/CONTINUE_PROMPT.md",
        ],
        "task2": [
            "task2/official/OFFICIAL_PAGES_FULL.json",
            "task2/official/STARTER_PROMPT.md",
            "task2/official/CONTINUE_PROMPT.md",
        ],
        "task3": [
            "task3/official/OFFICIAL_PAGES_FULL.json",
            "task3/official/STARTER_PROMPT_SUBSTITUTED.md",
            "task3/official/CONTINUE_PROMPT_EXACT.md",
            "task3/official/OVERVIEW_WORKING_COPY.md",
            "task3/official/SUBMISSION_WORKING_COPY.md",
            "task3/official/README.md",
        ],
        "task4": [
            "task4/official/OFFICIAL_PAGES_FULL.json",
            "task4/official/OVERVIEW.md",
            "task4/official/SUBMISSION.md",
            "task4/official/STARTER_PROMPT_EXACT.md",
            "task4/official/CONTINUE_PROMPT_EXACT.md",
            "task4/official/README.md",
        ],
        "task5": [
            "task5/official/OFFICIAL_PAGES_FULL.json",
            "task5/official/OVERVIEW.md",
            "task5/official/SUBMISSION.md",
            "task5/official/STARTER_PROMPT_EXACT.md",
            "task5/official/CONTINUE_PROMPT_EXACT.md",
            "task5/official/README.md",
        ],
        "task6": [
            "task6/official/OFFICIAL_PAGES_FULL.json",
            "task6/official/OVERVIEW.md",
            "task6/official/SUBMISSION.md",
            "task6/official/STARTER_PROMPT_EXACT.md",
            "task6/official/CONTINUE_PROMPT_EXACT.md",
            "task6/official/README.md",
        ],
    }
    for task, paths in checklist["task_packages"].items():
        number = task.removeprefix("task")
        assert paths == {
            "readme": f"task{number}/README.md",
            "official_sources": expected_official_sources[task],
            "summary": f"task{number}/SUMMARY.json",
            "compliance": f"task{number}/COMPLIANCE.md",
            "manifest": f"task{number}/MANIFEST.sha256",
        }
        assert all(
            (ROOT / path).is_file()
            for value in paths.values()
            for path in (value if isinstance(value, list) else [value])
        ), task
    assert checklist["special_evidence"] == {
        "tasks1_2_reproductions": [
            "REPRODUCTION_TRACE_MATERIAL.md",
            "REPRODUCTION_TRACE_INDEX.json",
            "REPRODUCTION_COSTS.json",
        ],
        "tasks1_2_formal_prefix_audit": [
            "FORMAL_PREFIX_AUDIT.md",
            "FORMAL_PREFIX_AUDIT.json",
        ],
        "tasks1_2_official_final_extraction_candidates": [
            "task1/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json",
            "task2/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json",
        ],
        "submission_version_budget_audit": [
            "SUBMISSION_VERSION_AUDIT.json",
            "SUBMISSION_VERSION_AUDIT.md",
        ],
        "task4_supplemental_trace_and_rule_audit": [
            "task4/evidence/SUPPLEMENTAL_ROLLOUT_PROVENANCE.json",
            "task4/RULE_DIFFERENCE_AUDIT.md",
        ],
        "task6_exact_artifact_chain": [
            "task6/ARTIFACT_PROVENANCE.json",
            "task6/RULE_DIFFERENCE_AUDIT.md",
            "task6/evidence/EVALUATOR_BATCHING_PROVENANCE.json",
        ],
    }
    assert all(
        (ROOT / path).is_file()
        for paths in checklist["special_evidence"].values()
        for path in paths
    )
    requirements = checklist["requirements"]
    expected_requirement_statuses = {
        "execution_traces_all_six_tasks": "complete_selected_observable_prefixes_with_provenance_limits",
        "later_two_hour_reproduction_traces_task1_task2": "complete_separately_scoped_post_deadline_reference",
        "prompts_and_visible_outputs": "complete_for_selected_observable_trace_scope",
        "exact_organizer_prompt_conformance": "audited_with_non_exact_tasks",
        "cross_task_rule_compliance": "audited_known_deviations_and_evidence_limits_remain",
        "submission_version_limits": "complete_literal_audit_with_known_deviations_and_organizer_scope_questions",
        "task4_rule_difference_audit": "complete_with_disclosed_prompt_process_and_hardware_limits",
        "task6_exact_artifact_and_rule_audit": "exact_v3_artifacts_complete_measured_batch_behavior_disclosed_not_a_compliance_blocker",
        "tool_calls_and_outputs": "complete_for_selected_observable_trace_scope",
        "llms_used": "complete",
        "api_costs": "token_accounting_complete_usd_unavailable",
        "gpu_compute_and_costs_per_task": "remote_selected_scope_complete_local_h100_and_usd_incomplete",
        "kaggle_extraction": "complete_external_archive",
        "official_final_submission_results": "complete_score_reconciliation_not_all_results_trace_bound",
        "human_intervention_exclusion": "complete_for_selected_scope",
    }
    assert set(requirements) == set(expected_requirement_statuses)
    for name, expected_status in expected_requirement_statuses.items():
        assert requirements[name]["status"] == expected_status, name

    # Every path advertised in the organizer-facing requirements must resolve
    # to a repository file. This prevents a green verifier when the checklist
    # has drifted to a renamed, omitted, or mistyped deliverable.
    for name, requirement in requirements.items():
        advertised_paths: list[str] = []
        if "path" in requirement:
            advertised_paths.append(requirement["path"])
        advertised_paths.extend(requirement.get("paths", []))
        for key in ("selection_path", "manifest_path"):
            if key in requirement:
                advertised_paths.append(requirement[key])
        assert advertised_paths, f"requirement has no evidence path: {name}"
        for relative in advertised_paths:
            target = (ROOT / relative).resolve()
            assert target.is_relative_to(ROOT.resolve()), (name, relative)
            assert target.is_file(), (name, relative)

    assert requirements["execution_traces_all_six_tasks"]["paths"] == [
        "AUTONOMOUS_TRACE_MATERIAL.md",
        "AUTONOMOUS_TRACE_INDEX.json",
    ]
    assert requirements["later_two_hour_reproduction_traces_task1_task2"]["paths"] == [
        "REPRODUCTION_TRACE_MATERIAL.md",
        "REPRODUCTION_TRACE_INDEX.json",
        "REPRODUCTION_COSTS.json",
    ]
    prompt_requirement = requirements["exact_organizer_prompt_conformance"]
    assert prompt_requirement["strict_exact_prompt_tasks"] == ["task3", "task5", "task6"]
    assert prompt_requirement["non_exact_prompt_tasks"] == ["task1", "task2", "task4"]
    assert prompt_requirement["supplemental_formal_prefix_exact_prompt_tasks"] == [
        "task1",
        "task2",
    ]
    assert requirements["cross_task_rule_compliance"][
        "all_six_strictly_compliant_claim_supported"
    ] is False
    tool_requirement = requirements["tool_calls_and_outputs"]
    assert tool_requirement["event_types"] == [
        "function_call",
        "function_call_output",
        "custom_tool_call",
        "custom_tool_call_output",
    ]
    llm_requirement = requirements["llms_used"]
    assert llm_requirement["model"] == "gpt-5.6-sol"
    assert llm_requirement["provider"] == "ioai_allowed"
    assert llm_requirement["reasoning_effort"] == {
        "task1": "max",
        "task2": "max",
        "task3": "max",
        "task4": "max",
        "task5": "xhigh",
        "task6": "xhigh",
    }
    assert requirements["api_costs"]["usd_total"] is None
    assert requirements["human_intervention_exclusion"]["selection_path"] == (
        "AUTONOMOUS_TRACE_INDEX.json"
    )
    assert requirements["human_intervention_exclusion"]["manifest_path"] == (
        "AUTONOMOUS_MATERIAL_MANIFEST.sha256"
    )
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
