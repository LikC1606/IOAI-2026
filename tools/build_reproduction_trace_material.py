#!/usr/bin/env python3
"""Publish the later two-hour Task 1/2 reproduction traces.

The source JSONL files live in the private historical run archive.  This
builder copies only their observable event envelopes after applying the same
credential/private-endpoint/opaque-reasoning redaction used by the published
autonomous package. These runs are deliberately a separate, post-deadline,
non-ranking scope. The full Task 1 trace is retained here as raw audit evidence,
while its canonical solution trace is the immutable prefix through
`task_complete` selected by the autonomous index.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import build_execution_trace_index as trace_tools
import build_autonomous_trace_material as autonomous_material


ROOT = Path(__file__).resolve().parents[1]

RUNS: dict[str, dict[str, Any]] = {
    "task1": {
        "competition": "ioai-2026-task-1-westlake-nlp-24",
        "account": "researai",
        "run_kind": "later_reproduction_120m",
        "record_recovery_note": (
            "The complete original Task 1 run record was unavailable after a school-server "
            "restart; a bounded formal prefix remains as separate historical audit material. "
            "This is a later fresh reproduction using the same configured solver/system, "
            "official competition bundle, and organizer constraints."
        ),
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
        "record_recovery_note": (
            "The complete original Task 2 run record was unavailable after a school-server "
            "restart; a bounded formal prefix remains as separate historical audit material. "
            "This is a later fresh reproduction using the same configured solver/system, "
            "official competition bundle, and organizer constraints."
        ),
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
    if text.startswith("# AGENTS.md instructions"):
        return "startup_instructions"
    if text == autonomous_material.exact_organizer_prompt(task, "Starter Prompt"):
        return "exact_organizer_starter_prompt"
    if text == autonomous_material.exact_organizer_prompt(task, "Continuation Prompt"):
        return "exact_organizer_continuation_prompt"
    if text.startswith("Solve the Kaggle competition"):
        return "custom_starter_prompt"
    if text.startswith("Continue solving the Kaggle competition"):
        return "custom_continuation_prompt"
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
        "status": "full later no-live-human reproduction audit traces; post-deadline non-ranking reference material",
        "important_boundary": "Task 1's canonical solution trace is the prefix through task_complete under task1/evidence/canonical; its full trace remains here. Task 2 uses the full reproduction. Neither score replaces FINAL_SUBMISSION_RESULTS.md or becomes an official-ranking result.",
        "included_prompt_types": [
            "injected startup instructions",
            "custom organizer-like starter text retained and marked non-exact",
            "custom runtime continuation text retained and marked non-exact where present",
        ],
        "strict_exact_organizer_prompt_text_conformance": False,
        "compliance_limit": (
            "Both reproductions are no-live-human runs, but their starter user messages "
            "append a fresh-run-isolation section not present in the exact organizer Starter "
            "Prompt. The full Task 1 audit trace also preserves a custom continuation after "
            "its selected submission, final answer, and task_complete event; the canonical "
            "solution prefix excludes that causal suffix. These traces are not claimed to satisfy "
            "the strict exact-prompt rule."
        ),
        "redaction": "credentials, private endpoints, secret metadata, and encrypted_content are redacted or replaced by an opaque placeholder",
        "tasks": {},
    }
    for task, run in tasks.items():
        trace = run["trace"]
        index["tasks"][task] = {
            "competition": run["competition"],
            "account": run["account"],
            "run_kind": run["run_kind"],
            "record_recovery_note": run["record_recovery_note"],
            "canonical_autonomous_trace": task != "task1",
            **(
                {
                    "canonical_solution_prefix": "task1/evidence/canonical/rollout-solution-prefix.jsonl",
                    "full_trace_scope": "raw audit trace including the 15-event post-task_complete suffix",
                }
                if task == "task1"
                else {}
            ),
            "strict_exact_organizer_prompt_text_conformance": False,
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
        "reproduction runs for Tasks 1 and 2. Task 1's canonical solution trace",
        "is the exact prefix through task_complete under `task1/evidence/canonical/`;",
        "the full Task 1 stream remains here for audit. Task 2 uses its full stream.",
        "Both remain post-deadline, non-ranking reference material.",
        "",
        "The complete original Task 1 and Task 2 run records were unavailable after",
        "a school-server restart. Bounded formal prefixes remain as separate historical",
        "audit material. Each trace below is a later fresh reproduction using the same",
        "configured solver/system, official competition bundle, and organizer constraints.",
        "",
        "The JSONL retains startup and actual user prompts, visible Agent messages, tool",
        "calls, tool outputs, lifecycle events, and cumulative token telemetry.",
        "Opaque encrypted reasoning is replaced by a placeholder; secrets and private",
        "endpoints are redacted. Both starter messages append a custom fresh-run",
        "isolation section and therefore do not match the organizer Starter Prompt",
        "exactly. The full Task 1 trace preserves a custom continuation after its",
        "selected submission, final Agent answer, and task_complete event; that",
        "15-event suffix is outside the canonical Task 1 solution trace. Autonomy is",
        "reported separately from exact-organizer-prompt conformance.",
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
        "[`FINAL_SUBMISSION_RESULTS.md`](FINAL_SUBMISSION_RESULTS.md). The canonical",
        "Task 1 prefix and full Task 2 trace are selected in",
        "[`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json).",
        "",
    ])
    for task, data in index["tasks"].items():
        trace = data["trace_file"]
        lines.extend([
            f"## {task}",
            "",
            f"Competition: `{data['competition']}`; account: `{data['account']}`.",
            f"Record recovery note: {data['record_recovery_note']}",
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
                "record_recovery_note": run["record_recovery_note"],
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
