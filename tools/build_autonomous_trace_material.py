#!/usr/bin/env python3
"""Build the human-intervention-free trace material and its cost ledger."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import build_execution_trace_index as trace_tools


ROOT = Path(__file__).resolve().parents[1]
TASK6_BOUNDARY = "2026-08-08T18:09:48.833Z"
TASK6_MAIN_PREFIX = ROOT / (
    "task6/evidence/autonomous-only/"
    "rollout-2026-08-09T00-23-24-019fe22f-b2b8-7191-a6ec-39dea000da9f-autonomous-prefix.jsonl"
)

TASK_PATHS = {
    "task1": [
        "task1/evidence/rollouts/rollout-2026-08-05T17-20-55-019fd139-d180-7171-ac0b-c037e11866eb.jsonl"
    ],
    "task2": [
        "task2/evidence/rollouts/rollout-2026-08-05T13-30-31-019fd066-e338-71a0-9d8e-6e1d154c5a79.jsonl"
    ],
    "task3": [
        "task3/evidence/rollouts/rollout-2026-08-06T12-34-49-019fd55a-3edf-7801-b6a1-f1313393ff34.jsonl",
        "task3/evidence/rollouts/rollout-2026-08-06T12-40-25-019fd55f-61f3-74c2-a87f-66ce5288dc56.jsonl",
        "task3/evidence/rollouts/rollout-2026-08-06T12-41-11-019fd560-1290-7bb1-af1d-8fd44c84aad5.jsonl",
        "task3/evidence/rollouts/rollout-2026-08-06T12-41-42-019fd560-8eec-78c1-92c9-3ab2e67b1bd8.jsonl",
    ],
    "task4": [
        "task4/evidence/rollouts/rollout-2026-08-07T12-18-29-019fda71-a6a2-7a22-8c18-22e99f127422.jsonl",
        "task4/evidence/rollouts/rollout-2026-08-07T12-18-41-019fda71-d4eb-70a3-9b66-e0fb3b2d0e66.jsonl",
        "task4/evidence/rollouts/rollout-2026-08-07T12-18-47-019fda71-effd-7321-8ce9-2a4a57fcaa48.jsonl",
        "task4/evidence/rollouts/rollout-2026-08-07T13-21-43-019fdaab-8d94-76a0-b625-078c838b5227.jsonl",
        "task4/evidence/rollouts/rollout-2026-08-07T13-21-51-019fdaab-ace4-7b51-93b2-244d9517423a.jsonl",
    ],
    "task5": [
        "task5/evidence/rollouts/rollout-2026-08-07T15-04-23-019fdb09-8b16-7032-82e1-21be10be17c0.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T15-10-16-019fdb0e-ece5-75f1-a919-0cf4bc532838.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T15-10-32-019fdb0f-2ccc-7d80-b97f-3e6891df20be.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T15-10-46-019fdb0f-641d-71f1-aad9-71a76ad14bb3.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T15-23-21-019fdb1a-e97c-7542-b5b9-eb65046b1e4c.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T15-35-11-019fdb25-bcda-76b3-aa61-bf745122bb27.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T15-35-25-019fdb25-f27d-7fc0-a235-ef2d4e1b9e14.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T15-36-47-019fdb27-333f-7002-84f3-83c19536e1a2.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T15-58-45-019fdb3b-4f7e-70b2-b652-940314651df4.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T15-58-59-019fdb3b-85ff-7f63-9981-952915290c13.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T15-59-18-019fdb3b-d220-74b3-9fce-c89b25442543.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T16-05-40-019fdb41-a587-7410-8926-ba38fb7da71d.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T16-23-09-019fdb51-a930-7953-9c40-be02d0c93136.jsonl",
        "task5/evidence/rollouts/rollout-2026-08-07T16-23-36-019fdb52-12da-7931-b44c-82fe30560795.jsonl",
    ],
    "task6": [
        TASK6_MAIN_PREFIX.relative_to(ROOT).as_posix(),
        "task6/evidence/rollouts/rollout-2026-08-09T00-23-42-019fe22f-f897-7d10-b27c-2c6586c55a27.jsonl",
        "task6/evidence/rollouts/rollout-2026-08-09T00-30-10-019fe235-e3a2-7173-bac5-0ba0451f279f.jsonl",
    ],
}

BOUNDARIES = {
    "task1": {
        "exclusive_utc": "2026-08-05T10:16:52.222Z",
        "basis": "first material human instruction received by the controlling session",
    },
    "task2": {
        "exclusive_utc": "2026-08-05T06:24:47.549Z",
        "basis": "first modified/custom continuation prompt",
    },
    "task3": {
        "exclusive_utc": "2026-08-06T05:46:19.450Z",
        "basis": "first non-read-only supervisory instruction received by the controlling session",
    },
    "task4": {
        "exclusive_utc": "2026-08-07T06:18:25.517Z",
        "basis": "run deadline; no live human method or target prompt was delivered to the solver",
    },
    "task5": {
        "exclusive_utc": "2026-08-07T09:04:20.519Z",
        "basis": "run deadline; controller status questions were not solver inputs",
    },
    "task6": {
        "exclusive_utc": TASK6_BOUNDARY,
        "basis": "first human-triggered resume prompt delivered after the autonomous start",
    },
}

EXCLUSIONS = {
    "task1": ["post-boundary supervised continuation and submission suffix (not in repository; provenance hashes only)"],
    "task2": ["all events at or after the modified continuation at 06:24:47.549Z"],
    "task3": ["all events at or after the supervision boundary at 05:46:19.450Z"],
    "task4": ["events at or after the run deadline"],
    "task5": ["events at or after the run deadline"],
    "task6": [
        "main-trace events at or after 18:09:48.833Z",
        "the later human target-score prompt at 18:14:21.148Z and everything after it",
        "two worker traces spawned after the human-triggered resume",
    ],
}

STARTER_FILES = {
    "task1": ROOT / "task1/official/STARTER_PROMPT.md",
    "task2": ROOT / "task2/official/STARTER_PROMPT.md",
    "task3": ROOT / "task3/official/STARTER_PROMPT_SUBSTITUTED.md",
    "task4": ROOT / "task4/official/start.md",
    "task5": ROOT / "task5/official/start.md",
    "task6": ROOT / "task6/official/start.md",
}
CONTINUATION_FILES = {
    "task2": ROOT / "task2/official/CONTINUE_PROMPT.md",
    "task4": ROOT / "task4/official/continue.md",
}

GPU = {
    "task1": {
        "accelerator": "CPU",
        "runtime_scope": "pre-boundary baseline notebook; metadata has enable_gpu=false",
        "runtime_seconds": 0,
        "runtime_hours": 0,
        "observed_cpu_log_seconds": 69.886003607,
        "gpu_cost_usd": 0,
        "cost_status": "no_gpu_allocated",
    },
    "task2": {
        "accelerator": "NvidiaTeslaT4",
        "runtime_scope": "two pre-boundary eligible remote CNN notebooks",
        "runtime_seconds": 493.582953672,
        "runtime_hours": 0.13710637602,
        "gpu_cost_usd": None,
        "cost_status": "unavailable_no_rate_or_invoice",
    },
    "task3": {
        "accelerator": "CPU",
        "runtime_scope": "autonomous versions v1-v8; metadata has enable_gpu=false",
        "runtime_seconds": 0,
        "runtime_hours": 0,
        "gpu_cost_usd": 0,
        "cost_status": "no_gpu_allocated",
    },
    "task4": {
        "accelerator": "NvidiaTeslaT4",
        "runtime_scope": "all autonomous versions v1-v4, including diagnostic v3",
        "runtime_seconds": 1120.720551504,
        "runtime_hours": 0.31131126430666667,
        "submitted_versions_runtime_seconds": 775.784001944,
        "diagnostic_v3_runtime_seconds": 344.93654956,
        "gpu_cost_usd": None,
        "cost_status": "unavailable_no_rate_or_invoice",
    },
    "task5": {
        "accelerator": "NvidiaTeslaT4",
        "runtime_scope": "T4 versions v5-v7; versions v1-v4 were CPU runs",
        "runtime_seconds": 837.27460599,
        "runtime_hours": 0.23257627944166667,
        "gpu_cost_usd": None,
        "cost_status": "unavailable_no_rate_or_invoice",
    },
    "task6": {
        "accelerator": "NvidiaTeslaT4",
        "runtime_scope": "versions v1-v3, all submitted before the human-prompt boundary",
        "runtime_seconds": 243.721403533,
        "runtime_hours": 0.06770038987027778,
        "gpu_cost_usd": None,
        "cost_status": "unavailable_no_rate_or_invoice",
    },
}


def validate_task6_prefix() -> None:
    if not TASK6_MAIN_PREFIX.is_file():
        raise ValueError(f"missing bounded Task 6 main trace: {TASK6_MAIN_PREFIX}")
    for event in trace_tools.jsonl_events(TASK6_MAIN_PREFIX):
        timestamp = str(event.get("timestamp", ""))
        if timestamp and timestamp >= TASK6_BOUNDARY:
            raise ValueError(f"post-boundary Task 6 event in {TASK6_MAIN_PREFIX}: {timestamp}")


def message_text(payload: dict[str, Any]) -> str:
    parts: list[str] = []
    for item in payload.get("content") or []:
        if isinstance(item, dict):
            parts.append(str(item.get("text") or item.get("input_text") or ""))
    return "\n".join(parts)


def classify_prompts(task: str, path: Path, role: str) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    starter = STARTER_FILES[task].read_text(encoding="utf-8")
    continuation = (
        CONTINUATION_FILES[task].read_text(encoding="utf-8")
        if task in CONTINUATION_FILES
        else None
    )
    for event in trace_tools.jsonl_events(path):
        payload = event.get("payload", {})
        if event.get("type") != "response_item" or payload.get("role") != "user":
            continue
        text = message_text(payload)
        if text.startswith("# AGENTS.md instructions"):
            prompt_class = "startup_instructions"
        elif text == starter:
            prompt_class = (
                "organizer_starter_prompt"
                if role == "main"
                else "inherited_organizer_starter_prompt"
            )
        elif continuation is not None and text == continuation:
            base_class = (
                "exact_organizer_continuation_prompt"
                if task == "task2"
                else "preconfigured_runtime_resume_template"
            )
            prompt_class = base_class if role == "main" else f"inherited_{base_class}"
        elif role != "main":
            prompt_class = "agent_generated_worker_assignment"
        else:
            raise ValueError(
                f"unclassified main user prompt in {path} at {event.get('timestamp')}"
            )
        messages.append(
            {
                "timestamp": str(event.get("timestamp")),
                "trace_path": path.relative_to(ROOT).as_posix(),
                "class": prompt_class,
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            }
        )
    return messages


def aggregate_tokens(files: list[dict[str, Any]]) -> dict[str, int]:
    keys = (
        "input_tokens",
        "cached_input_tokens",
        "cache_write_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
        "total_tokens",
    )
    totals = [item["token_usage_cumulative_final"] for item in files]
    if not all(isinstance(item, dict) for item in totals):
        raise ValueError("all autonomous traces must have exact token totals")
    return {key: sum(int(item.get(key, 0)) for item in totals) for key in keys}


def build_index() -> dict[str, Any]:
    token_data = json.loads(
        (ROOT / "task3/evidence/AUTONOMOUS_TOKEN_USAGE.json").read_text(encoding="utf-8")
    )
    token_overrides = {
        item["repository_trace_path"]: item["token_usage"] for item in token_data["traces"]
    }
    tasks: dict[str, Any] = {}
    for task, relative_paths in TASK_PATHS.items():
        records: list[dict[str, Any]] = []
        prompts: list[dict[str, str]] = []
        for relative in relative_paths:
            path = ROOT / relative
            role_hint = "main" if path == TASK6_MAIN_PREFIX else None
            record = trace_tools.trace_record(path, relative, role_hint=role_hint)
            if relative in token_overrides:
                record["token_usage_cumulative_final"] = token_overrides[relative]
                record["token_usage_source"] = "task3/evidence/AUTONOMOUS_TOKEN_USAGE.json"
            prompts.extend(classify_prompts(task, path, record["role"]))
            records.append(record)
        token_usage = aggregate_tokens(records)
        classes = Counter(item["class"] for item in prompts)
        tasks[task] = {
            "boundary": BOUNDARIES[task],
            "excluded_material": EXCLUSIONS[task],
            "trace_files": records,
            "canonical_model": "gpt-5.6-sol",
            "model_provider": "ioai_allowed",
            "reasoning_effort": "max" if task in {"task1", "task2", "task3", "task4"} else "xhigh",
            "event_count": sum(item["event_count"] for item in records),
            "logical_function_calls": sum(item["logical_function_calls"] for item in records),
            "exec_wrapper_custom_tool_calls": sum(
                item["exec_wrapper_custom_tool_calls"] for item in records
            ),
            "message_counts": dict(
                sorted(sum((Counter(item["message_counts"]) for item in records), Counter()).items())
            ),
            "response_item_types": dict(
                sorted(
                    sum(
                        (Counter(item["response_item_types"]) for item in records),
                        Counter(),
                    ).items()
                )
            ),
            "organizer_required_event_coverage": dict(
                sorted(
                    sum(
                        (
                            Counter(item["organizer_required_event_coverage"])
                            for item in records
                        ),
                        Counter(),
                    ).items()
                )
            ),
            "user_prompt_classes": dict(sorted(classes.items())),
            "user_prompt_audit": prompts,
            "manual_human_prompt_events_included": 0,
            "token_usage_cumulative_sum_across_traces": token_usage,
        }
    return {
        "schema": "ioai.autonomous-trace-material.v1",
        "definition": "observable competition-agent trace prefixes before any live human intervention prompt",
        "included_prompt_types": [
            "startup/system instructions actually injected",
            "organizer Starter Prompt",
            "exact organizer Continuation Prompt where applicable",
            "preconfigured runtime resume templates without a human method or target",
            "organizer context inherited by forked worker traces",
            "assignments generated by the main agent for its workers where represented as user-role input",
        ],
        "excluded_prompt_types": [
            "live human method, target-score, forced-submission, or custom continuation instructions",
            "all events causally downstream of an excluded prompt",
        ],
        "redaction": "credentials, private endpoints, secret metadata, and opaque encrypted reasoning are not published",
        "tasks": tasks,
    }


def write_markdown(index: dict[str, Any]) -> None:
    lines = [
        "# Autonomous competition trace material",
        "",
        "This is the organizer-facing trace set for Tasks 1–6. It contains only",
        "observable competition-agent execution before any live human intervention",
        "prompt. Exclusion is causal: once a disallowed prompt arrives, that prompt",
        "and every later event are omitted rather than deleting only the message.",
        "",
        "Startup instructions, organizer prompts, inherited organizer context,",
        "preconfigured runtime resume templates, and observable worker assignments",
        "are retained and classified. They are part of the execution environment,",
        "not live human method suggestions. Hidden chain-of-thought is not published.",
        "",
        "| Task | Trace files | Events | User prompts | Logical calls | Tokens | Boundary (exclusive UTC) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for task, data in index["tasks"].items():
        lines.append(
            f"| {task} | {len(data['trace_files'])} | {data['event_count']} | "
            f"{data['message_counts'].get('user', 0)} | {data['logical_function_calls']} | "
            f"{data['token_usage_cumulative_sum_across_traces']['total_tokens']} | "
            f"{data['boundary']['exclusive_utc']} |"
        )
    lines.extend(
        [
            "",
            "Exact prompt hashes, per-trace SHA-256 values, tool-call counts, message",
            "counts, and token counters are in",
            "[`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json). Costs and",
            "GPU runtimes are in [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json).",
            "Verify the complete selected set with",
            "[`AUTONOMOUS_MATERIAL_MANIFEST.sha256`](AUTONOMOUS_MATERIAL_MANIFEST.sha256).",
        ]
    )
    for task, data in index["tasks"].items():
        lines.extend(["", f"## {task}", "", f"Boundary: {data['boundary']['basis']}.", ""])
        lines.append("Included trace files:")
        lines.append("")
        for item in data["trace_files"]:
            path = item["path"]
            lines.append(f"- [`{Path(path).name}`]({path}) — {item['event_count']} events")
        lines.extend(["", "Explicitly excluded:", ""])
        for item in data["excluded_material"]:
            lines.append(f"- {item}")
    (ROOT / "AUTONOMOUS_TRACE_MATERIAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_costs(index: dict[str, Any]) -> None:
    tasks = {}
    total = 0
    competitions = {
        f"task{i}": f"ioai-2026-task-{i}-westlake-nlp-{60 if i == 6 else 48 if i == 3 else 24}"
        for i in range(1, 7)
    }
    for task, data in index["tasks"].items():
        token_usage = data["token_usage_cumulative_sum_across_traces"]
        total += token_usage["total_tokens"]
        tasks[task] = {
            "competition": competitions[task],
            "model_provider": "ioai_allowed",
            "model": "gpt-5.6-sol",
            "reasoning_effort": data["reasoning_effort"],
            "trace_scope": "autonomous-only material before the task boundary",
            "token_usage": token_usage,
            "api_cost_usd": None,
            "api_cost_status": "unavailable_unpriced_ioai_provider",
            "gpu": GPU[task],
        }
    payload = {
        "schema": "ioai.autonomous-execution-costs.v1",
        "scope": "only the human-intervention-free trace material in AUTONOMOUS_TRACE_INDEX.json",
        "currency": "USD",
        "known_token_total_all_tasks": total,
        "known_t4_runtime_seconds": 2695.299514699,
        "known_t4_runtime_hours": 0.7486943096386111,
        "api_cost_usd_total": None,
        "api_cost_total_status": "unavailable_no_provider_invoice_or_applicable_public_rate",
        "api_cost_total_reason": "No invoice or exact ioai_allowed/gpt-5.6-sol rate card was captured; another model's public price is not substituted.",
        "api_cost_formula_if_provider_rates_are_supplied": "(input_tokens-cached_input_tokens)/1e6*input_rate + cached_input_tokens/1e6*cached_input_rate + output_tokens/1e6*output_rate",
        "gpu_cost_usd_total": None,
        "gpu_cost_total_status": "unavailable_no_cloud_invoice_or_rate",
        "gpu_cost_total_reason": "Exact observed accelerator runtimes are reported per task, but no billable rate or invoice was captured.",
        "tasks": tasks,
    }
    (ROOT / "AUTONOMOUS_COSTS.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_manifest(index: dict[str, Any]) -> None:
    relative_paths = {
        "AUTONOMOUS_TRACE_INDEX.json",
        "AUTONOMOUS_COSTS.json",
        "AUTONOMOUS_TRACE_MATERIAL.md",
        "task3/evidence/AUTONOMOUS_TOKEN_USAGE.json",
        "tools/build_autonomous_trace_material.py",
        "tools/build_execution_trace_index.py",
        "FINAL_SUBMISSION_RESULTS.md",
        "ORGANIZER_SUBMISSION.md",
        "ORGANIZER_SUBMISSION.json",
        "KAGGLE_EXTRACTION_DELIVERY.json",
        "KAGGLE_EXTRACTION_SUMMARY.json",
        "task1/evidence/SUPERVISION_BOUNDARY_EVENT.json",
        "task1/remote/FINAL_ACCOUNT_RESULTS.json",
        "task2/remote/FINAL_ACCOUNT_RESULTS.json",
        "task3/evidence/SUPERVISION_BOUNDARY_EVENT.json",
        "task3/remote/FINAL_ACCOUNT_RESULTS.json",
        "task4/remote/FINAL_ACCOUNT_RESULTS.json",
        "task5/remote/FINAL_ACCOUNT_RESULTS.json",
        "task6/evidence/SUPERVISED_EXCLUSIONS.json",
        "task6/remote/FINAL_ACCOUNT_RESULTS.json",
    }
    for data in index["tasks"].values():
        relative_paths.update(item["path"] for item in data["trace_files"])
    lines = [
        f"{trace_tools.sha256(ROOT / relative)}  {relative}"
        for relative in sorted(relative_paths)
    ]
    (ROOT / "AUTONOMOUS_MATERIAL_MANIFEST.sha256").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    validate_task6_prefix()
    index = build_index()
    (ROOT / "AUTONOMOUS_TRACE_INDEX.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_markdown(index)
    write_costs(index)
    write_manifest(index)
    print(json.dumps({task: data["event_count"] for task, data in index["tasks"].items()}))


if __name__ == "__main__":
    main()
