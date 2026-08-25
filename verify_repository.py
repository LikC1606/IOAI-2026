"""Verify task manifests, core score claims, and autonomous trace material."""
from __future__ import annotations

import hashlib
import json
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
    for task in ("task4", "task5", "task6"):
        gpu = costs["tasks"][task]["gpu"]
        assert gpu["local_development_runtime_seconds"] is None, task
        assert gpu["local_development_gpu_cost_usd"] is None, task
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


def verify_cross_task_rule_audit() -> dict[str, object]:
    audit = json.loads((ROOT / "RULE_COMPLIANCE_AUDIT.json").read_text(encoding="utf-8"))
    assert audit["all_six_strictly_compliant_claim_supported"] is False
    tasks = audit["tasks"]
    assert tasks["task1"]["official_final_trace_alignment"] is False
    assert tasks["task2"]["official_final_trace_alignment"] is False
    assert tasks["task3"]["official_final_trace_alignment"] is True
    assert tasks["task3"]["submission_counts"] == {
        "all_account": 27,
        "before_official_deadline": 11,
        "after_official_deadline": 16,
        "published_limit": 15,
    }
    assert tasks["task4"]["strict_exact_organizer_prompt_text_conformance"] is False
    assert tasks["task4"]["selected_trace_files"] == 12
    assert tasks["task5"]["official_final_trace_alignment"] is True
    assert tasks["task6"]["batch_dependence_fixture"]["final_prediction_changes"] == 5
    for task in ("task1", "task2", "task3"):
        assert audit["tasks"][task]["informational_disclosures"] == [
            "method_background_research_not_treated_as_compliance_issue"
        ]
    assert audit["cost_accounting"]["local_gpu_runtime"] == "incomplete_tasks_4_to_6"
    return {
        "tasks": len(tasks),
        "all_six_strictly_compliant_claim_supported": False,
    }


def verify_execution_accounting() -> dict[str, int]:
    index = json.loads((ROOT / "EXECUTION_TRACE_INDEX.json").read_text(encoding="utf-8"))
    costs = json.loads((ROOT / "COSTS.json").read_text(encoding="utf-8"))
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
        task_tokens = data["token_usage_cumulative_sum_across_traces"]["total_tokens"]
        assert costs["tasks"][task]["token_usage"]["total_tokens"] == task_tokens, task
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
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        target = (ROOT / relative).resolve()
        assert target.is_relative_to(ROOT.resolve()), relative
        assert sha256(target) == expected, relative
        checked += 1

    index = json.loads((ROOT / "REPRODUCTION_TRACE_INDEX.json").read_text(encoding="utf-8"))
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
        assert data["post_deadline"] is True
        assert data["ranking_eligible"] is False
        assert data["strict_exact_organizer_prompt_text_conformance"] is False
        assert data["canonical_autonomous_trace"] is (task == "task2")
        if task == "task1":
            assert data["canonical_solution_prefix"] == "task1/evidence/canonical/rollout-solution-prefix.jsonl"
        trace = data["trace_file"]
        path = ROOT / trace["path"]
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
            "recorded_score": score,
        }
        task_report["final_account_result"] = verify_final_account_result(task, summary)
        report["tasks"][f"task{task}"] = task_report
    report["autonomous_material"] = verify_autonomous_material()
    report["published_execution_accounting"] = verify_execution_accounting()
    report["later_reproduction_material"] = verify_reproduction_material()
    report["task6_exact_artifacts"] = verify_task6_artifacts()
    report["cross_task_rule_audit"] = verify_cross_task_rule_audit()
    delivery = json.loads((ROOT / "KAGGLE_EXTRACTION_DELIVERY.json").read_text(encoding="utf-8"))
    assert delivery["archive"]["size_bytes"] == 496870419
    assert delivery["archive"]["entry_count"] == 1401
    assert delivery["archive"]["sha256"] == "eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c"
    assert delivery["google_drive"]["file_id"] == "1c9yRn5SUo6LOPDrHLrAVjj-9JLFti9Vz"
    checklist = json.loads((ROOT / "ORGANIZER_SUBMISSION.json").read_text(encoding="utf-8"))
    assert checklist["status"] == (
        "complete_evidence_package_with_known_compliance_and_cost_limits"
    )
    assert checklist["organizer_review_guide"] == "ORGANIZER_REVIEW_GUIDE.md"
    assert (ROOT / checklist["organizer_review_guide"]).is_file()
    assert checklist["access_control"] == {
        "repository_visibility": "private_authorized_review_only_while_restricted_data_is_present",
        "restricted_path": "task3/input/competition/",
        "handling_instructions": "task3/DATA_PROVENANCE.md",
    }
    assert set(checklist["task_packages"]) == {f"task{i}" for i in range(1, 7)}
    for task, paths in checklist["task_packages"].items():
        number = task.removeprefix("task")
        assert paths == {
            "readme": f"task{number}/README.md",
            "summary": f"task{number}/SUMMARY.json",
            "compliance": f"task{number}/COMPLIANCE.md",
            "manifest": f"task{number}/MANIFEST.sha256",
        }
        assert all((ROOT / path).is_file() for path in paths.values()), task
    assert checklist["special_evidence"] == {
        "tasks1_2_reproductions": [
            "REPRODUCTION_TRACE_MATERIAL.md",
            "REPRODUCTION_TRACE_INDEX.json",
            "REPRODUCTION_COSTS.json",
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
    assert checklist["requirements"]["cross_task_rule_compliance"][
        "all_six_strictly_compliant_claim_supported"
    ] is False
    assert checklist["requirements"]["api_costs"]["status"] == (
        "token_accounting_complete_usd_unavailable"
    )
    assert checklist["requirements"]["gpu_compute_and_costs_per_task"]["status"] == (
        "remote_selected_scope_complete_local_h100_and_usd_incomplete"
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
