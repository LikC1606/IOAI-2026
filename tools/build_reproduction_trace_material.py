#!/usr/bin/env python3
"""Publish the later two-hour Task 1/2 reproduction traces.

The source JSONL files live in the private historical run archive.  This
builder copies only their observable event envelopes after applying the same
credential/private-endpoint/opaque-reasoning redaction used by the published
autonomous package.  These runs are deliberately a separate, post-deadline,
non-ranking scope; they must not replace the official or autonomous result
records.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import build_execution_trace_index as trace_tools


ROOT = Path(__file__).resolve().parents[1]

RUNS: dict[str, dict[str, Any]] = {
    "task1": {
        "competition": "ioai-2026-task-1-westlake-nlp-24",
        "account": "researai",
        "run_kind": "later_reproduction_120m",
        "post_deadline": True,
        "ranking_eligible": False,
        "source": Path(
            "/workspace/IOAI/runs/historical/"
            "ioai2-competition-runs-task1-fresh-120m-20260806T002520CST/"
            "ioai-2026-task-1-westlake-nlp-24/codex-home/sessions/2026/08/06/"
            "rollout-2026-08-06T00-25-54-019fd2be-e734-7dd1-9a9c-823dee341dc6.jsonl"
        ),
        "destination": ROOT / "task1/evidence/reproduction-120m/rollout.jsonl",
        "project": Path(
            "/workspace/IOAI/runs/historical/"
            "ioai2-competition-runs-task1-fresh-120m-20260806T002520CST/"
            "ioai-2026-task-1-westlake-nlp-24/project"
        ),
        "window": {
            "start_utc": "2026-08-05T16:25:50.693Z",
            "deadline_utc": "2026-08-05T18:25:50.634Z",
            "trace_first_event_utc": "2026-08-05T16:25:54.368Z",
            "trace_last_event_utc": "2026-08-05T18:25:46.003Z",
        },
        "official_deadline_utc": "2026-08-05T10:50:00Z",
        "official_deadline_basis": "The competition account's official deadline predates this fresh reproduction; it is not an official-ranking run.",
        "result": {
            "selected_submission": {
                "submission_id": "55277782",
                "kernel": "researai/ioai-task1-fresh-20260806-002520",
                "version": 5,
                "candidate": "balanced_edge_fallback_v5",
                "public_lb": 0.74121,
                "local_cv": 0.7676212811096714,
                "runtime_seconds": 285.69,
                "status": "COMPLETE",
            },
            "other_versions": [
                {"version": 1, "candidate": "edge_explicit_speaker_v1", "status": "ERROR", "runtime_seconds": 62.48},
                {"version": 2, "candidate": "edge_explicit_speaker_v2_official_env", "status": "ERROR", "runtime_seconds": 83.02},
                {"version": 3, "candidate": "edge_explicit_speaker_v3_mount_retry", "status": "ERROR", "runtime_seconds": 315.35},
                {"version": 4, "candidate": "global_reranker_production_b8_v4", "status": "TIMEOUT", "runtime_seconds": 600.0},
                {"version": 6, "candidate": "reduced_global_plain_conversation_v6", "status": "TIMEOUT", "runtime_seconds": 600.0},
            ],
        },
        "gpu": {
            "accelerator": "NvidiaTeslaT4",
            "notebook_versions": 6,
            "observed_notebook_runtime_seconds": 1946.54,
            "observed_notebook_runtime_note": "Sum of the six recorded remote runtime fields: 62.48 + 83.02 + 315.35 + 600 + 285.69 + 600.",
            "gpu_cost_usd": None,
            "cost_status": "unavailable_no_invoice_or_rate",
        },
    },
    "task2": {
        "competition": "ioai-2026-task-2-westlake-nlp-24",
        "account": "researai",
        "run_kind": "later_reproduction_120m",
        "post_deadline": True,
        "ranking_eligible": False,
        "source": Path(
            "/workspace/IOAI/runs/historical/"
            "ioai2-competition-runs-task2-fresh-120m-20260806T001936CST/"
            "ioai-2026-task-2-westlake-nlp-24/codex-home/sessions/2026/08/06/"
            "rollout-2026-08-06T00-20-11-019fd2b9-ac0f-7d11-a60a-bf5b586b736e.jsonl"
        ),
        "destination": ROOT / "task2/evidence/reproduction-120m/rollout.jsonl",
        "project": Path(
            "/workspace/IOAI/runs/historical/"
            "ioai2-competition-runs-task2-fresh-120m-20260806T001936CST/"
            "ioai-2026-task-2-westlake-nlp-24/project"
        ),
        "window": {
            "start_utc": "2026-08-05T16:20:09.021Z",
            "deadline_utc": "2026-08-05T18:20:08.972Z",
            "trace_first_event_utc": "2026-08-05T16:20:11.567Z",
            "trace_last_event_utc": "2026-08-05T18:20:07.628Z",
        },
        "official_deadline_utc": "2026-08-05T07:35:00Z",
        "official_deadline_basis": "The competition account's official deadline predates this fresh reproduction; it is not an official-ranking run.",
        "result": {
            "selected_submission": {
                "submission_id": "55277682",
                "kernel": "researai/ioai-2026-task-2-westlake-nlp-24-solution",
                "version": 2,
                "candidate": "tree_film_blend_65_35_full_labels",
                "public_lb": 0.675,
                "local_cv": 0.6713888889,
                "runtime_seconds": 263.17,
                "status": "COMPLETE_SCORED",
            },
            "other_versions": [
                {"version": 1, "candidate": "structured_lgbm_v2_per_robot_full_labels", "submission_id": "55276740", "public_lb": 0.66944, "status": "COMPLETE_SCORED", "runtime_seconds": 220.27},
                {"version": 3, "candidate": "soft_pooled_robot_tree_full_labels", "submission_id": "55277932", "public_lb": 0.67, "status": "COMPLETE_SCORED", "runtime_seconds": 220.98},
            ],
        },
        "gpu": {
            "accelerator": "NvidiaTeslaT4",
            "gpu_versions": [2],
            "observed_gpu_runtime_seconds": 263.17,
            "cpu_versions": [1, 3],
            "observed_cpu_runtime_seconds": 441.25,
            "gpu_cost_usd": None,
            "cost_status": "unavailable_no_invoice_or_rate",
        },
    },
}


def message_text(payload: dict[str, Any]) -> str:
    return "\n".join(
        str(item.get("text") or item.get("input_text") or "")
        for item in payload.get("content") or []
        if isinstance(item, dict)
    )


def prompt_class(task: str, text: str) -> str:
    run = RUNS[task]
    project = run["project"]
    if text.startswith("# AGENTS.md instructions"):
        return "startup_instructions"
    if text == (project / "official/start.md").read_text(encoding="utf-8"):
        return "organizer_starter_prompt"
    continuation = project / "official/continue.md"
    if continuation.is_file() and text == continuation.read_text(encoding="utf-8"):
        return "preconfigured_runtime_resume_template"
    return "unclassified_user_prompt"


def publish_trace(task: str, run: dict[str, Any]) -> dict[str, Any]:
    source = run["source"]
    destination = run["destination"]
    if not source.is_file():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open(encoding="utf-8") as source_handle, destination.open("w", encoding="utf-8") as out:
        for line_number, line in enumerate(source_handle, 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid source JSONL {source}:{line_number}") from exc
            out.write(json.dumps(trace_tools.redact(event), ensure_ascii=False, separators=(",", ":")) + "\n")

    relative = destination.relative_to(ROOT).as_posix()
    record = trace_tools.trace_record(destination, relative, role_hint="main")
    prompt_audit = []
    for event in trace_tools.jsonl_events(destination):
        payload = event.get("payload", {})
        if event.get("type") != "response_item" or payload.get("role") != "user":
            continue
        text = message_text(payload)
        prompt_audit.append(
            {
                "timestamp": str(event.get("timestamp")),
                "class": prompt_class(task, text),
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            }
        )
    unknown = [item for item in prompt_audit if item["class"] == "unclassified_user_prompt"]
    if unknown:
        raise ValueError(f"unclassified user prompt(s) in {task}: {unknown}")
    run["trace"] = {
        **record,
        "source_sha256": trace_tools.sha256(source),
        "published_sha256": trace_tools.sha256(destination),
        "user_prompt_audit": prompt_audit,
        "user_prompt_classes": dict(sorted(Counter(item["class"] for item in prompt_audit).items())),
        "manual_human_prompt_events_included": 0,
        "redaction": "same credential/private-endpoint/opaque-reasoning redaction as the autonomous package",
    }
    return run


def main() -> None:
    tasks = {task: publish_trace(task, run) for task, run in RUNS.items()}
    index: dict[str, Any] = {
        "schema": "ioai.later-reproduction-trace-material.v1",
        "scope": "full later two-hour reproduction traces for Tasks 1 and 2",
        "status": "post-deadline non-ranking reference material",
        "important_boundary": "These traces do not replace AUTONOMOUS_TRACE_INDEX.json or FINAL_SUBMISSION_RESULTS.md and must not be represented as official-ranking autonomous results.",
        "included_prompt_types": [
            "injected startup instructions",
            "organizer Starter Prompt",
            "preconfigured runtime resume template without a human method or target",
        ],
        "redaction": "credentials, private endpoints, secret metadata, and encrypted_content are redacted or replaced by an opaque placeholder",
        "tasks": {},
    }
    for task, run in tasks.items():
        trace = run["trace"]
        index["tasks"][task] = {
            "competition": run["competition"],
            "account": run["account"],
            "run_kind": run["run_kind"],
            "post_deadline": run["post_deadline"],
            "ranking_eligible": run["ranking_eligible"],
            "window": run["window"],
            "official_deadline_utc": run["official_deadline_utc"],
            "official_deadline_basis": run["official_deadline_basis"],
            "trace_file": {
                "path": trace["path"],
                "source_sha256": trace["source_sha256"],
                "published_sha256": trace["published_sha256"],
                "event_count": trace["event_count"],
                "first_timestamp": trace["first_timestamp"],
                "last_timestamp": trace["last_timestamp"],
                "event_types": trace["event_types"],
                "response_item_types": trace["response_item_types"],
                "message_counts": trace["message_counts"],
                "organizer_required_event_coverage": trace["organizer_required_event_coverage"],
                "logical_function_calls": trace["logical_function_calls"],
                "logical_function_call_names": trace["logical_function_call_names"],
                "exec_wrapper_custom_tool_calls": trace["exec_wrapper_custom_tool_calls"],
                "custom_tool_call_names": trace["custom_tool_call_names"],
                "models_observed": trace["models_observed"],
                "reasoning_efforts_observed": trace["reasoning_efforts_observed"],
                "token_usage_cumulative_final": trace["token_usage_cumulative_final"],
                "user_prompt_audit": trace["user_prompt_audit"],
                "user_prompt_classes": trace["user_prompt_classes"],
                "manual_human_prompt_events_included": 0,
            },
            "result": run["result"],
            "gpu": run["gpu"],
        }

    (ROOT / "REPRODUCTION_TRACE_INDEX.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Later two-hour reproduction traces",
        "",
        "These are full, credential-redacted traces from the later fresh 120-minute",
        "reproduction runs for Tasks 1 and 2. They are post-deadline, non-ranking",
        "reference material. The official account results and the autonomous-only",
        "prefix package remain separate and are not overwritten by this material.",
        "",
        "The JSONL retains startup/organizer prompts, visible Agent messages, tool",
        "calls, tool outputs, lifecycle events, and cumulative token telemetry.",
        "Opaque encrypted reasoning is replaced by a placeholder; secrets and private",
        "endpoints are redacted. The Task 1 final continuation is a preconfigured",
        "runtime-resume template, not a human method or target-score instruction.",
        "",
        "| Task | Trace events | User / assistant | Logical calls | `exec` calls | Tokens | Result |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for task, data in index["tasks"].items():
        trace = data["trace_file"]
        result = data["result"]["selected_submission"]
        lines.append(
            f"| {task} | {trace['event_count']} | {trace['message_counts'].get('user', 0)} / {trace['message_counts'].get('assistant', 0)} | "
            f"{trace['logical_function_calls']} | {trace['exec_wrapper_custom_tool_calls']} | "
            f"{trace['token_usage_cumulative_final']['total_tokens']} | "
            f"`{result['submission_id']}` / Public {result['public_lb']} |"
        )
    lines.extend([
        "",
        "## Scope and result separation",
        "",
        "Do not use the scores in this table as the official final scores. They are",
        "results produced by later fresh runs and were submitted after the official",
        "competition deadline. For official account reconciliation, use",
        "[`FINAL_SUBMISSION_RESULTS.md`](FINAL_SUBMISSION_RESULTS.md). For the strict",
        "human-intervention-free material, use [`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json).",
        "",
    ])
    for task, data in index["tasks"].items():
        trace = data["trace_file"]
        lines.extend([
            f"## {task}",
            "",
            f"Competition: `{data['competition']}`; account: `{data['account']}`.",
            f"Run window: `{data['window']['start_utc']}` to `{data['window']['deadline_utc']}`.",
            f"Official Kaggle deadline: `{data['official_deadline_utc']}` (the run starts after it).",
            f"Trace: [`rollout.jsonl`]({trace['path']}) — {trace['event_count']} events; SHA-256 `{trace['published_sha256']}`.",
            "",
            "Prompt classes:",
            "",
        ])
        for item, count in trace["user_prompt_classes"].items():
            lines.append(f"- `{item}`: {count}")
        selected = data["result"]["selected_submission"]
        lines.extend([
            "",
            f"Selected reproduction result: submission `{selected['submission_id']}`, candidate `{selected['candidate']}`, Public LB `{selected['public_lb']}`, local CV `{selected['local_cv']}`.",
            f"Observed compute: {json.dumps(data['gpu'], ensure_ascii=False)}",
            "",
        ])
    (ROOT / "REPRODUCTION_TRACE_MATERIAL.md").write_text("\n".join(lines), encoding="utf-8")

    costs = {
        "schema": "ioai.later-reproduction-costs.v1",
        "scope": "full later two-hour reproduction traces for Tasks 1 and 2",
        "currency": "USD",
        "api_cost_usd_total": None,
        "api_cost_status": "unavailable_no_provider_invoice_or_applicable_rate",
        "gpu_cost_usd_total": None,
        "gpu_cost_status": "unavailable_no_invoice_or_rate",
        "tasks": {
            task: {
                "competition": run["competition"],
                "model_provider": "ioai_allowed",
                "model": "gpt-5.6-sol",
                "reasoning_effort": "max",
                "trace_token_usage": run["trace"]["token_usage_cumulative_final"],
                "api_cost_usd": None,
                "gpu": run["gpu"],
            }
            for task, run in tasks.items()
        },
    }
    (ROOT / "REPRODUCTION_COSTS.json").write_text(json.dumps(costs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest_paths = [
        "REPRODUCTION_TRACE_INDEX.json",
        "REPRODUCTION_TRACE_MATERIAL.md",
        "REPRODUCTION_COSTS.json",
        "tools/build_reproduction_trace_material.py",
    ] + [data["trace_file"]["path"] for data in index["tasks"].values()]
    manifest = "\n".join(f"{trace_tools.sha256(ROOT / path)}  {path}" for path in sorted(manifest_paths)) + "\n"
    (ROOT / "REPRODUCTION_MATERIAL_MANIFEST.sha256").write_text(manifest, encoding="utf-8")
    print(json.dumps({task: data["trace_file"]["event_count"] for task, data in index["tasks"].items()}))


if __name__ == "__main__":
    main()
