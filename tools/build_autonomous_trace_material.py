#!/usr/bin/env python3
"""Build the human-intervention-free trace material and its cost ledger."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import build_execution_trace_index as trace_tools


ROOT = Path(__file__).resolve().parents[1]
TASK1_RAW = ROOT / "task1/evidence/reproduction-120m/rollout.jsonl"
TASK1_SOLUTION_PREFIX = ROOT / "task1/evidence/canonical/rollout-solution-prefix.jsonl"
TASK1_TASK_COMPLETE_UTC = "2026-08-05T18:24:58.140Z"
TASK1_FIRST_POST_SOLUTION_PROMPT_UTC = "2026-08-05T18:25:04.940Z"
TASK6_BOUNDARY = "2026-08-08T18:09:48.833Z"
TASK6_MAIN_PREFIX = ROOT / (
    "task6/evidence/autonomous-only/"
    "rollout-2026-08-09T00-23-24-019fe22f-b2b8-7191-a6ec-39dea000da9f-autonomous-prefix.jsonl"
)

TASK_PATHS = {
    "task1": [
        TASK1_SOLUTION_PREFIX.relative_to(ROOT).as_posix()
    ],
    "task2": [
        "task2/evidence/reproduction-120m/rollout.jsonl"
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
        "task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-06-019fda9b-6b63-7031-a6dd-52db684209be.jsonl",
        "task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-23-019fda9b-ade0-7912-868f-a922606fd40f.jsonl",
        "task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-30-019fda9b-c906-70a0-8f5c-99fc2f25fafa.jsonl",
        "task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-39-019fda9b-ed93-7473-96c5-f8c030d3e4bc.jsonl",
        "task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-57-14-019fdacc-1073-7f03-ac6e-346ad63c0c4f.jsonl",
        "task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-57-22-019fdacc-2e9c-78a2-b037-135a4b172944.jsonl",
        "task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-57-28-019fdacc-47fe-7bc3-8cac-d77f25b124e1.jsonl",
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
        "exclusive_utc": TASK1_FIRST_POST_SOLUTION_PROMPT_UTC,
        "basis": "canonical causal solution prefix ends at task_complete; the complete later reproduction remains in the separate reproduction audit package",
    },
    "task2": {
        "exclusive_utc": "2026-08-05T18:20:08.972Z",
        "basis": "later two-hour reproduction deadline; no live human method/target prompt was delivered",
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
    "task1": [
        "the 15-event suffix after task_complete, beginning with the post-solution custom continuation",
        "the complete 1,398-event reproduction remains available under task1/evidence/reproduction-120m and REPRODUCTION_TRACE_INDEX.json",
        "the official account's earlier deadline and all post-deadline scores are outside official-ranking scope",
        "the older formal-run prefix remains under task1/evidence/rollouts as historical audit material",
    ],
    "task2": [
        "events at or after the later two-hour reproduction deadline",
        "the official account's earlier deadline and all post-deadline scores are outside official-ranking scope",
        "the older formal-run prefix remains under task2/evidence/rollouts as historical audit material",
    ],
    "task3": ["all events at or after the supervision boundary at 05:46:19.450Z"],
    "task4": ["events at or after the run deadline"],
    "task5": ["events at or after the run deadline"],
    "task6": [
        "main-trace events at or after 18:09:48.833Z",
        "the later human target-score prompt at 18:14:21.148Z and everything after it",
        "two worker traces spawned after the human-triggered resume",
    ],
}

COMPETITIONS = {
    f"task{i}": f"ioai-2026-task-{i}-westlake-nlp-{60 if i == 6 else 48 if i == 3 else 24}"
    for i in range(1, 7)
}
PROMPT_FILE_FALLBACKS = {
    ("task6", "Starter Prompt"): ROOT / "task6/official/start.md",
    ("task6", "Continuation Prompt"): ROOT / "task6/official/CONTINUE_PROMPT_EXACT.md",
}
PROMPT_CONFORMANCE_NOTES = {
    "task1": (
        "The reproduction starter contains a user-requested fresh-run-isolation appendix. "
        "The canonical solution prefix ends at task_complete and contains no continuation "
        "event, but the custom starter still prevents an exact-prompt-only claim. The full "
        "raw reproduction preserves the later post-solution continuation separately."
    ),
    "task2": (
        "The reproduction starter contains a user-requested fresh-run-isolation appendix; "
        "there is no continuation event in this reproduction."
    ),
    "task4": (
        "The injected starter has formatting changes and the main-runtime continuation "
        "events use a substantive generic workflow template rather than the exact organizer "
        "Continuation Prompt. The final selected submission is downstream of those events; "
        "the complete selection includes the supplemental parallel-solver traces."
    ),
}


def build_task1_solution_prefix() -> None:
    """Copy the immutable Task 1 event prefix through the selected task_complete."""
    if not TASK1_RAW.is_file():
        raise ValueError(f"missing full Task 1 reproduction trace: {TASK1_RAW}")
    lines: list[str] = []
    complete_count = 0
    next_user_prompt_utc: str | None = None
    after_complete = False
    for line_number, line in enumerate(TASK1_RAW.read_text(encoding="utf-8").splitlines(True), 1):
        if not line.strip():
            continue
        event = json.loads(line)
        payload = event.get("payload", {})
        if not after_complete:
            lines.append(line)
        if (
            event.get("timestamp") == TASK1_TASK_COMPLETE_UTC
            and event.get("type") == "event_msg"
            and payload.get("type") == "task_complete"
        ):
            complete_count += 1
            after_complete = True
            continue
        if after_complete and event.get("type") == "response_item" and payload.get("role") == "user":
            next_user_prompt_utc = str(event.get("timestamp"))
            break
    if complete_count != 1:
        raise ValueError(f"expected one selected Task 1 task_complete, found {complete_count}")
    if next_user_prompt_utc != TASK1_FIRST_POST_SOLUTION_PROMPT_UTC:
        raise ValueError(
            "unexpected first post-solution Task 1 prompt: "
            f"{next_user_prompt_utc!r}"
        )
    if len(lines) != 1383:
        raise ValueError(f"unexpected Task 1 canonical prefix length: {len(lines)}")
    TASK1_SOLUTION_PREFIX.parent.mkdir(parents=True, exist_ok=True)
    TASK1_SOLUTION_PREFIX.write_text("".join(lines), encoding="utf-8")
    events = trace_tools.jsonl_events(TASK1_SOLUTION_PREFIX)
    totals = trace_tools.token_totals(events)
    if totals is None or totals.get("total_tokens") != 40830176:
        raise ValueError(f"unexpected Task 1 prefix token totals: {totals}")
RECOVERY_NOTES = {
    "task1": (
        "The complete raw formal Task 1 session was subsequently located in a private "
        "local archive after a school-server restart. Its human-influenced suffix is "
        "not published; a bounded pre-boundary formal prefix remains under "
        "task1/evidence/rollouts. The canonical trace is a later fresh reproduction "
        "using the same configured solver/system, official competition bundle, and "
        "organizer constraints. See ORIGINAL_SESSION_RECOVERY.md/json."
    ),
    "task2": (
        "The complete raw formal Task 2 session was subsequently located in a private "
        "local archive after a school-server restart. Its human-influenced suffix is "
        "not published; a bounded pre-boundary formal prefix remains under "
        "task2/evidence/rollouts. The canonical trace is a later fresh reproduction "
        "using the same configured solver/system, official competition bundle, and "
        "organizer constraints. See ORIGINAL_SESSION_RECOVERY.md/json."
    ),
}

GPU = {
    "task1": {
        "accelerator": "NvidiaTeslaT4",
        "runtime_scope": "all six notebook versions in the later 120-minute reproduction",
        "runtime_seconds": 1946.54,
        "runtime_hours": 0.5407055555555556,
        "gpu_cost_usd": None,
        "cost_status": "unavailable_no_rate_or_invoice",
    },
    "task2": {
        "accelerator": "NvidiaTeslaT4",
        "runtime_scope": "version 2 in the later 120-minute reproduction; versions 1 and 3 were CPU",
        "runtime_seconds": 263.17,
        "runtime_hours": 0.07310277777777778,
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
        "runtime_scope": "Kaggle notebook versions v1-v4, including diagnostic v3",
        "runtime_seconds": 1120.720551504,
        "runtime_hours": 0.31131126430666667,
        "submitted_versions_runtime_seconds": 775.784001944,
        "diagnostic_v3_runtime_seconds": 344.93654956,
        "gpu_cost_usd": None,
        "cost_status": "unavailable_no_rate_or_invoice",
        "local_development_accelerator": "Nvidia H100 (trace-recorded)",
        "local_development_runtime_seconds": None,
        "local_development_runtime_status": "unavailable_non_exhaustive_overlapping_approximate_records",
        "known_selected_body_local_runtime_seconds": 161.0,
        "known_selected_body_runtime_source": "historical final notebook technical report",
        "local_development_gpu_cost_usd": None,
        "local_development_cost_status": "unavailable_no_complete_runtime_or_rate",
    },
    "task5": {
        "accelerator": "NvidiaTeslaT4",
        "runtime_scope": "T4 versions v5-v7; versions v1-v4 were CPU runs",
        "runtime_seconds": 837.27460599,
        "runtime_hours": 0.23257627944166667,
        "gpu_cost_usd": None,
        "cost_status": "unavailable_no_rate_or_invoice",
        "local_development_accelerator": "Nvidia H100 (trace-recorded)",
        "local_development_runtime_seconds": None,
        "local_development_runtime_status": "unavailable_multiple_overlapping_runs",
        "known_selected_path_local_runtime_seconds": 24.8,
        "known_selected_path_runtime_source": "historical v6 technical report",
        "local_development_gpu_cost_usd": None,
        "local_development_cost_status": "unavailable_no_complete_runtime_or_rate",
    },
    "task6": {
        "accelerator": "NvidiaTeslaT4",
        "runtime_scope": "versions v1-v3, all submitted before the human-prompt boundary",
        "runtime_seconds": 243.721403533,
        "runtime_hours": 0.06770038987027778,
        "gpu_cost_usd": None,
        "cost_status": "unavailable_no_rate_or_invoice",
        "local_development_accelerator": "Nvidia H100 (trace-recorded)",
        "local_development_runtime_seconds": None,
        "local_development_runtime_status": "unavailable_multiple_experiment_records_not_exhaustively_allocated",
        "known_v3_candidate_local_runtime_seconds": 31.03,
        "known_v3_candidate_runtime_source": "records/experiments.jsonl and historical v3 technical report",
        "local_development_gpu_cost_usd": None,
        "local_development_cost_status": "unavailable_no_complete_runtime_or_rate",
    },
}

# Reviewer-requested cost estimate assumptions.  The observed Kaggle runtime
# and actual provider charge fields above remain unchanged; these fields are a
# reproducible estimate for budgeting only.  OpenAI's current pricing page
# lists GPT-5.6 Sol at $4/M uncached input, $0.40/M cached input, $5/M cache
# writes, and $20/M output.  The user-requested server assumption is two H100
# GPUs for two hours per task.  A representative H100 on-demand rate of
# $3.925/GPU-hour is used as the median of 14 surveyed public per-GPU rates
# ($2.19-$6.98/GPU-hour); no claim is made that this was the billed rate.
API_ESTIMATE_PRICING = {
    "source_url": "https://platform.openai.com/docs/pricing",
    "as_of_utc": "2026-08-26T00:00:00Z",
    "input_usd_per_million": 4.0,
    "cached_input_usd_per_million": 0.40,
    "cache_write_usd_per_million": 5.0,
    "output_usd_per_million": 20.0,
}
H100_ESTIMATE = {
    "accelerator": "Nvidia H100",
    "gpu_count": 2,
    "hours": 2.0,
    "gpu_hours": 4.0,
    "rate_usd_per_gpu_hour": 3.925,
    "low_rate_usd_per_gpu_hour": 2.19,
    "high_rate_usd_per_gpu_hour": 6.98,
    "low_cost_usd_per_task": 8.76,
    "median_cost_usd_per_task": 15.70,
    "high_cost_usd_per_task": 27.92,
    "rate_basis": "median of 14 surveyed public on-demand H100 per-GPU rates ($2.19-$6.98/GPU-hour), based on the 2026-08-21 comparison table",
    "surveyed_rates_usd_per_gpu_hour": [
        2.19,
        2.89,
        2.99,
        3.19,
        3.29,
        3.85,
        3.90,
        3.95,
        4.41,
        5.36,
        5.95,
        6.16,
        6.88,
        6.98,
    ],
    "survey_source_urls": [
        "https://www.thundercompute.com/blog/nvidia-h100-pricing",
        "https://www.spheron.network/blog/lambda-cloud-h100-pricing-2026/",
        "https://tech-insider.org/runpod-vs-lambda-vs-vast-ai-2026/",
        "https://vast.ai/pricing",
    ],
    "survey_note": "Public comparison prices vary by provider, region, storage, SLA, and spot/on-demand tier; the median is a budgeting proxy only.",
}


def api_cost_estimate(token_usage: dict[str, int]) -> float:
    uncached = token_usage["input_tokens"] - token_usage["cached_input_tokens"]
    return round(
        uncached * API_ESTIMATE_PRICING["input_usd_per_million"] / 1_000_000
        + token_usage["cached_input_tokens"]
        * API_ESTIMATE_PRICING["cached_input_usd_per_million"]
        / 1_000_000
        + token_usage["cache_write_input_tokens"]
        * API_ESTIMATE_PRICING["cache_write_usd_per_million"]
        / 1_000_000
        + token_usage["output_tokens"]
        * API_ESTIMATE_PRICING["output_usd_per_million"]
        / 1_000_000,
        6,
    )


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


def exact_organizer_prompt(task: str, page_name: str) -> str:
    """Return the slug-substituted prompt published on the Kaggle page."""
    snapshot = ROOT / f"{task}/official/OFFICIAL_PAGES_FULL.json"
    if snapshot.is_file():
        pages = json.loads(snapshot.read_text(encoding="utf-8"))
        content = next(
            item["content"] for item in pages if item.get("name") == page_name
        )
        blocks = re.findall(r"```(?:[^\n]*)\n(.*?)```", content, re.DOTALL)
        if not blocks:
            raise ValueError(f"no fenced exact prompt in {snapshot}: {page_name}")
        return blocks[-1].replace("<COMPETITION-SLUG>", COMPETITIONS[task])
    fallback = PROMPT_FILE_FALLBACKS.get((task, page_name))
    if fallback is None or not fallback.is_file():
        raise ValueError(f"no official prompt source for {task}: {page_name}")
    return fallback.read_text(encoding="utf-8")


def classify_prompts(task: str, path: Path, role: str) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    starter = exact_organizer_prompt(task, "Starter Prompt")
    continuation = exact_organizer_prompt(task, "Continuation Prompt")
    for event in trace_tools.jsonl_events(path):
        payload = event.get("payload", {})
        if event.get("type") != "response_item" or payload.get("role") != "user":
            continue
        text = message_text(payload)
        if text.startswith("# AGENTS.md instructions"):
            prompt_class = "startup_instructions"
        elif text == starter:
            prompt_class = (
                "exact_organizer_starter_prompt"
                if role == "main"
                else "inherited_exact_organizer_starter_prompt"
            )
        elif text == continuation:
            prompt_class = (
                "exact_organizer_continuation_prompt"
                if role == "main"
                else "inherited_exact_organizer_continuation_prompt"
            )
        elif text.startswith("Solve the Kaggle competition"):
            prompt_class = (
                "custom_starter_prompt"
                if role == "main"
                else "inherited_custom_starter_prompt"
            )
        elif text.startswith("Continue solving the Kaggle competition"):
            prompt_class = (
                "custom_continuation_prompt"
                if role == "main"
                else "inherited_custom_continuation_prompt"
            )
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
                "organizer_prompt_text_status": (
                    "exact"
                    if "exact_organizer_" in prompt_class
                    else "custom"
                    if "custom_" in prompt_class
                    else "not_applicable"
                ),
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
        prompts: list[dict[str, Any]] = []
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
        custom_prompt_events = sum(
            count for name, count in classes.items() if "custom_" in name
        )
        tasks[task] = {
            "boundary": BOUNDARIES[task],
            "excluded_material": EXCLUSIONS[task],
            **({"record_recovery_note": RECOVERY_NOTES[task]} if task in RECOVERY_NOTES else {}),
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
            "strict_exact_organizer_prompt_text_conformance": custom_prompt_events == 0,
            "custom_prompt_event_count_including_inherited_context": custom_prompt_events,
            "prompt_conformance_note": PROMPT_CONFORMANCE_NOTES.get(
                task,
                "All starter/continuation prompt events match the exact organizer text; no continuation was needed where none is present.",
            ),
            "token_usage_cumulative_sum_across_traces": token_usage,
        }
    return {
        "schema": "ioai.autonomous-trace-material.v1",
        "definition": "observable competition-agent trace prefixes before any live human intervention prompt",
        "included_prompt_types": [
            "startup/system instructions actually injected",
            "exact organizer Starter/Continuation Prompt events where actually matched",
            "custom preconfigured prompt events retained for audit and explicitly marked non-exact",
            "organizer context inherited by forked worker traces",
            "assignments generated by the main agent for its workers where represented as user-role input",
        ],
        "compliance_limit": (
            "No-live-human autonomy and exact-organizer-prompt conformance are separate. "
            "Tasks 1, 2, and 4 contain custom prompt text and are not claimed here to satisfy "
            "the strict exact-prompt rule; organizer/Jury recognition is not assumed."
        ),
        "excluded_prompt_types": [
            "live-human method, target-score, forced-submission, or custom continuation instructions at the task boundary",
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
        "Startup instructions, organizer prompts, inherited context, custom runtime",
        "prompt text, and observable worker assignments are retained and classified.",
        "No-live-human autonomy is not treated as proof of the separate exact-prompt",
        "rule. Tasks 1, 2, and 4 contain custom prompt text and are disclosed as",
        "non-exact; organizer/Jury recognition is not assumed. Hidden chain-of-thought",
        "is not published.",
        "The actual startup instruction payload for each task is indexed and hash-bound",
        "in [`STARTUP_INSTRUCTION_INDEX.md`](STARTUP_INSTRUCTION_INDEX.md) and the",
        "machine-readable [`STARTUP_INSTRUCTION_INDEX.json`](STARTUP_INSTRUCTION_INDEX.json).",
        "",
        "Completeness here means completeness of the selected observable prefix, not",
        "proof of competition-rule compliance. Tasks 1 and 2 do not bind the official",
        "final result to an original autonomous trace. Method research is retained as",
        "background provenance, and Task 6's evaluator-batch dependence is retained as",
        "a measured technical behavior; neither is treated as a compliance blocker. See",
        "`RULE_COMPLIANCE_AUDIT.md/json`.",
        "",
        "For Tasks 1 and 2, complete raw formal sessions were subsequently recovered",
        "in private local archives after a school-server restart. Their human-influenced",
        "suffixes are intentionally unpublished; bounded formal prefixes remain separate",
        "historical audit material, while the selected traces are later fresh reproductions",
        "using the same configured solver/system and organizer constraints. See",
        "`ORIGINAL_SESSION_RECOVERY.md/json`.",
        "",
        "| Task | Trace files | Events | User prompts | Logical calls | Unfinished calls | Tokens | Boundary (exclusive UTC) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for task, data in index["tasks"].items():
        lines.append(
            f"| {task} | {len(data['trace_files'])} | {data['event_count']} | "
            f"{data['message_counts'].get('user', 0)} | {data['logical_function_calls']} | "
            f"{sum(len(item['call_pairing']['unmatched_calls']) for item in data['trace_files'])} | "
            f"{data['token_usage_cumulative_sum_across_traces']['total_tokens']} | "
            f"{data['boundary']['exclusive_utc']} |"
        )
    unfinished_total = sum(
        len(item["call_pairing"]["unmatched_calls"])
        for data in index["tasks"].values()
        for item in data["trace_files"]
    )
    lines.extend(
        [
            "",
            f"Call-envelope audit found {unfinished_total} call(s) whose output is absent",
            "because the trace ends on that call at the declared capture boundary. Each",
            "call ID and timestamp is recorded below and in the JSON index; orphan outputs,",
            "duplicate IDs, out-of-order outputs, or unmatched calls away from the final",
            "event are rejected by `verify_repository.py`.",
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
        if "record_recovery_note" in data:
            lines.extend([f"Record recovery note: {data['record_recovery_note']}", ""])
        lines.extend(
            [
                f"Strict exact organizer prompt text: **{'yes' if data['strict_exact_organizer_prompt_text_conformance'] else 'no'}**.",
                f"Prompt audit note: {data['prompt_conformance_note']}",
                "",
            ]
        )
        lines.append("Included trace files:")
        lines.append("")
        for item in data["trace_files"]:
            path = item["path"]
            pairing = item["call_pairing"]
            unfinished = ", ".join(
                f"`{call['call_id']}` ({call['kind']})"
                for call in pairing["unmatched_calls"]
            ) or "none"
            lines.append(
                f"- [`{Path(path).name}`]({path}) — {item['event_count']} events; "
                f"call pairing `{pairing['status']}`; unfinished calls: {unfinished}"
            )
        lines.extend(["", "Explicitly excluded:", ""])
        for item in data["excluded_material"]:
            lines.append(f"- {item}")
    (ROOT / "AUTONOMOUS_TRACE_MATERIAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_costs(index: dict[str, Any]) -> None:
    tasks = {}
    total = 0
    estimated_api_total = 0.0
    estimated_h100_total = 0.0
    estimated_h100_low_total = 0.0
    estimated_h100_high_total = 0.0
    for task, data in index["tasks"].items():
        token_usage = data["token_usage_cumulative_sum_across_traces"]
        total += token_usage["total_tokens"]
        estimated_api = api_cost_estimate(token_usage)
        estimated_h100 = round(H100_ESTIMATE["gpu_hours"] * H100_ESTIMATE["rate_usd_per_gpu_hour"], 6)
        estimated_api_total += estimated_api
        estimated_h100_total += estimated_h100
        estimated_h100_low_total += H100_ESTIMATE["low_cost_usd_per_task"]
        estimated_h100_high_total += H100_ESTIMATE["high_cost_usd_per_task"]
        tasks[task] = {
            "competition": COMPETITIONS[task],
            "model_provider": "ioai_allowed",
            "model": "gpt-5.6-sol",
            "reasoning_effort": data["reasoning_effort"],
            "trace_scope": (
                "canonical later two-hour autonomous reproduction; post-deadline non-ranking"
                if task in {"task1", "task2"}
                else "autonomous-only material before the task boundary"
            ),
            "token_usage": token_usage,
            "api_cost_usd": None,
            "api_cost_status": "actual_charge_unavailable_estimate_provided",
            "api_cost_estimate_usd": estimated_api,
            "api_cost_estimate_status": "estimate_using_current_public_openai_price_assumption",
            "h100_server_cost_estimate_usd": estimated_h100,
            "h100_server_cost_estimate_low_usd": H100_ESTIMATE["low_cost_usd_per_task"],
            "h100_server_cost_estimate_high_usd": H100_ESTIMATE["high_cost_usd_per_task"],
            "h100_server_cost_estimate_status": "user_assumed_two_h100_gpus_for_two_hours",
            "h100_server_cost_assumption": H100_ESTIMATE,
            "estimated_total_api_plus_h100_usd": round(estimated_api + estimated_h100, 6),
            "gpu": GPU[task],
        }
    payload = {
        "schema": "ioai.autonomous-execution-costs.v1",
        "scope": "only the human-intervention-free trace material in AUTONOMOUS_TRACE_INDEX.json",
        "currency": "USD",
        "known_token_total_all_tasks": total,
        "known_t4_runtime_seconds": 4411.426561027,
        "known_t4_runtime_hours": 1.2253962669519445,
        "api_cost_usd_total": None,
        "api_cost_total_status": "actual_charge_unavailable_estimate_provided",
        "api_cost_total_reason": "No provider invoice was captured. The separately labeled estimate applies the current official public gpt-5.6-sol token rates to the exact trace counters.",
        "api_cost_formula_if_provider_rates_are_supplied": "(input_tokens-cached_input_tokens)/1e6*input_rate + cached_input_tokens/1e6*cached_input_rate + cache_write_input_tokens/1e6*cache_write_rate + output_tokens/1e6*output_rate",
        "api_cost_estimate_usd_total": round(estimated_api_total, 6),
        "api_cost_estimate_status": "budgetary_estimate_not_invoice",
        "api_cost_estimate_pricing": API_ESTIMATE_PRICING,
        "gpu_cost_usd_total": None,
        "gpu_cost_total_status": "actual_charge_unavailable_user_assumption_estimate_provided",
        "gpu_cost_total_reason": "Observed Kaggle T4 runtimes are reported, but exhaustive local H100 runtime and an invoice were not captured. The separately labeled H100 server estimate uses the user's two-GPU/two-hour-per-Task assumption.",
        "gpu_compute_accounting_status": "remote_kaggle_runtime_complete_selected_scope_local_development_incomplete",
        "h100_server_cost_estimate_usd_total": round(estimated_h100_total, 6),
        "h100_server_cost_estimate_low_usd_total": round(estimated_h100_low_total, 6),
        "h100_server_cost_estimate_high_usd_total": round(estimated_h100_high_total, 6),
        "h100_server_cost_estimate_status": "user_assumption_two_h100_gpus_for_two_hours_per_task_not_actual_invoice",
        "h100_server_cost_estimate_basis": H100_ESTIMATE,
        "estimated_api_plus_h100_usd_total": round(estimated_api_total + estimated_h100_total, 6),
        "tasks": tasks,
    }
    (ROOT / "AUTONOMOUS_COSTS.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    # Keep the legacy public execution-cost view in lockstep with the richer
    # autonomous ledger.  Its actual-charge fields remain null; estimate
    # fields are explicitly labeled as budgetary assumptions.
    public_costs = json.loads((ROOT / "COSTS.json").read_text(encoding="utf-8"))
    public_costs.update(
        {
            "api_cost_method": "exact token telemetry plus separately labeled estimate using current official GPT-5.6 Sol rates",
            "api_cost_formula_if_provider_rates_are_supplied": payload[
                "api_cost_formula_if_provider_rates_are_supplied"
            ],
            "api_cost_total_status": payload["api_cost_total_status"],
            "api_cost_total_reason": payload["api_cost_total_reason"],
            "api_cost_estimate_usd_total": payload["api_cost_estimate_usd_total"],
            "api_cost_estimate_status": payload["api_cost_estimate_status"],
            "api_cost_estimate_pricing": payload["api_cost_estimate_pricing"],
            "gpu_cost_total_status": payload["gpu_cost_total_status"],
            "gpu_cost_total_reason": payload["gpu_cost_total_reason"],
            "h100_server_cost_estimate_usd_total": payload[
                "h100_server_cost_estimate_usd_total"
            ],
            "h100_server_cost_estimate_low_usd_total": payload[
                "h100_server_cost_estimate_low_usd_total"
            ],
            "h100_server_cost_estimate_high_usd_total": payload[
                "h100_server_cost_estimate_high_usd_total"
            ],
            "h100_server_cost_estimate_status": payload[
                "h100_server_cost_estimate_status"
            ],
            "h100_server_cost_estimate_basis": payload[
                "h100_server_cost_estimate_basis"
            ],
            "estimated_api_plus_h100_usd_total": payload[
                "estimated_api_plus_h100_usd_total"
            ],
        }
    )
    for task, task_cost in tasks.items():
        public_task = public_costs["tasks"][task]
        public_task.update(
            {
                "api_cost_status": task_cost["api_cost_status"],
                "api_cost_estimate_usd": task_cost["api_cost_estimate_usd"],
                "api_cost_estimate_status": task_cost["api_cost_estimate_status"],
                "h100_server_cost_estimate_usd": task_cost[
                    "h100_server_cost_estimate_usd"
                ],
                "h100_server_cost_estimate_low_usd": task_cost[
                    "h100_server_cost_estimate_low_usd"
                ],
                "h100_server_cost_estimate_high_usd": task_cost[
                    "h100_server_cost_estimate_high_usd"
                ],
                "h100_server_cost_estimate_status": task_cost[
                    "h100_server_cost_estimate_status"
                ],
                "h100_server_cost_assumption": task_cost[
                    "h100_server_cost_assumption"
                ],
                "estimated_total_api_plus_h100_usd": task_cost[
                    "estimated_total_api_plus_h100_usd"
                ],
            }
        )
    (ROOT / "COSTS.json").write_text(
        json.dumps(public_costs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_manifest(index: dict[str, Any]) -> None:
    relative_paths = {
        ".gitattributes",
        "AUTONOMOUS_TRACE_INDEX.json",
        "AUTONOMOUS_COSTS.json",
        "AUTONOMOUS_TRACE_MATERIAL.md",
        "EXECUTION_TRACE_INDEX.json",
        "EXECUTION_TRACE_INDEX.md",
        "EXECUTION_TRACES.md",
        "COSTS.json",
        "task3/evidence/AUTONOMOUS_TOKEN_USAGE.json",
        "task1/tools/verify_package.py",
        "task3/evidence/verify_artifacts.py",
        "tools/build_autonomous_trace_material.py",
        "tools/build_execution_trace_index.py",
        "FINAL_SUBMISSION_RESULTS.md",
        "FORMAL_PREFIX_AUDIT.json",
        "FORMAL_PREFIX_AUDIT.md",
        "task1/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json",
        "task2/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json",
        "SUBMISSION_VERSION_AUDIT.json",
        "SUBMISSION_VERSION_AUDIT.md",
        "tools/build_submission_version_audit.py",
        "ORGANIZER_SUBMISSION.md",
        "ORGANIZER_SUBMISSION.json",
        "ORGANIZER_REVIEW_GUIDE.md",
        "OPEN_REVIEW_ITEMS.md",
        "ORIGINAL_SESSION_RECOVERY.md",
        "ORIGINAL_SESSION_RECOVERY.json",
        "AUDIT_STATUS.md",
        "AGENT_INSTRUCTION_LINEAGE.md",
        "KERNEL_VERSION_MAPPING_AUDIT.md",
        "STARTUP_INSTRUCTION_INDEX.md",
        "STARTUP_INSTRUCTION_INDEX.json",
        "ACCESS_CONTROL_AUDIT.json",
        "ACCESS_CONTROL_AUDIT.md",
        "REPRODUCTION_MATERIAL_MANIFEST.sha256",
        "tools/build_reproduction_trace_material.py",
        "tools/scan_extraction_archive.py",
        "tools/verify_extraction_bindings.py",
        "REQUIREMENT_EVIDENCE_MATRIX.json",
        "REQUIREMENT_EVIDENCE_MATRIX.md",
        "tools/build_requirement_evidence_matrix.py",
        "PACKAGE_COMPLETENESS.json",
        "PACKAGE_COMPLETENESS.md",
        "tools/build_package_completeness.py",
        "EXTRACTION_BINDING_RECEIPT.json",
        "KAGGLE_EXTRACTION_DELIVERY.json",
        "KAGGLE_EXTRACTION_SUMMARY.json",
        "PROMPT_CONFORMANCE_AUDIT.json",
        "PROMPT_CONFORMANCE_AUDIT.md",
        "RULE_COMPLIANCE_AUDIT.json",
        "RULE_COMPLIANCE_AUDIT.md",
        "task4/RULE_DIFFERENCE_AUDIT.json",
        "task4/RULE_DIFFERENCE_AUDIT.md",
        "task4/evidence/SUPPLEMENTAL_ROLLOUT_PROVENANCE.json",
        "task4/notebooks/REMOTE_CURRENT_V4.py",
        "task4/remote/V4_KERNEL.log",
        "task4/remote/V4_OUTPUT_PROVENANCE.json",
        "task6/official/CONTINUE_PROMPT_EXACT.md",
        "task4/official/OFFICIAL_PAGES_FULL.json",
        "task4/official/STARTER_PROMPT_EXACT.md",
        "task4/official/CONTINUE_PROMPT_EXACT.md",
        "task4/official/README.md",
        "task3/official/README.md",
        "task5/official/OFFICIAL_PAGES_FULL.json",
        "task5/official/STARTER_PROMPT_EXACT.md",
        "task5/official/CONTINUE_PROMPT_EXACT.md",
        "task5/official/README.md",
        "task6/official/OFFICIAL_PAGES_FULL.json",
        "task6/official/STARTER_PROMPT_EXACT.md",
        "task6/official/README.md",
        "tools/build_prompt_conformance_audit.py",
        "tools/build_task4_rule_audit.py",
        "tools/build_task4_supplemental_traces.py",
        "task1/evidence/SUPERVISION_BOUNDARY_EVENT.json",
        "task1/remote/FINAL_ACCOUNT_RESULTS.json",
        "task2/remote/FINAL_ACCOUNT_RESULTS.json",
        "task3/evidence/SUPERVISION_BOUNDARY_EVENT.json",
        "task3/remote/FINAL_ACCOUNT_RESULTS.json",
        "task4/remote/FINAL_ACCOUNT_RESULTS.json",
        "task5/remote/FINAL_ACCOUNT_RESULTS.json",
        "task6/evidence/SUPERVISED_EXCLUSIONS.json",
        "task6/evidence/EVALUATOR_BATCHING_PROVENANCE.json",
        "task6/ARTIFACT_PROVENANCE.json",
        "task6/notebooks/v3/script.py",
        "task6/notebooks/v3/kernel-metadata.json",
        "task6/RULE_DIFFERENCE_AUDIT.json",
        "task6/RULE_DIFFERENCE_AUDIT.md",
        "task6/SUPPLEMENTARY_TECHNICAL_REPORT.md",
        "task6/remote/v3/custom_model.py",
        "task6/remote/v3/submission.csv",
        "task6/tools/verify_v3_artifacts.py",
        "task6/remote/FINAL_ACCOUNT_RESULTS.json",
        "verify_repository.py",
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


def write_startup_instruction_index() -> None:
    """Build a machine-readable and human-readable index of startup payloads."""
    payloads: dict[str, dict[str, Any]] = {}
    competitions = {
        "task1": "ioai-2026-task-1-westlake-nlp-24",
        "task2": "ioai-2026-task-2-westlake-nlp-24",
        "task3": "ioai-2026-task-3-westlake-nlp-48",
        "task4": "ioai-2026-task-4-westlake-nlp-24",
        "task5": "ioai-2026-task-5-westlake-nlp-24",
        "task6": "ioai-2026-task-6-westlake-nlp-60",
    }
    for task, competition in competitions.items():
        relative = f"{task}/environment/AGENTS-ACTUALLY-INJECTED.md"
        path = ROOT / relative
        payloads[task] = {
            "competition": competition,
            "path": relative,
            "manifest": f"{task}/MANIFEST.sha256",
            "size_bytes": path.stat().st_size,
            "sha256": trace_tools.sha256(path),
        }
    data = {
        "schema": "ioai.startup-instruction-index.v1",
        "purpose": (
            "Index the credential-redacted AGENTS.md payload actually injected "
            "at startup for each preserved Task run."
        ),
        "generated_by": "tools/build_autonomous_trace_material.py",
        "payloads": payloads,
        "notes": [
            "These payloads are runtime evidence and are distinct from later project-file edits.",
            "Selected JSONL traces remain authoritative for delivery timestamps and autonomy boundaries.",
            "The index records only the six task-runtime payloads, not an unrelated parent-repository AGENTS.md.",
        ],
    }
    (ROOT / "STARTUP_INSTRUCTION_INDEX.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Startup instruction index",
        "",
        "This index identifies the `AGENTS.md` payload actually injected at the start",
        "of each preserved Task 1–6 run. These files are runtime evidence, not a claim",
        "that later edits to a project instruction file were present at startup. Each",
        "file is included in its Task package manifest and is linked from the trace",
        "records where the corresponding user-role startup envelope appears.",
        "",
        "The machine-readable binding is [`STARTUP_INSTRUCTION_INDEX.json`](STARTUP_INSTRUCTION_INDEX.json).",
        "",
        "| Task | Competition | Injected startup payload | Bytes | SHA-256 |",
        "|---|---|---|---:|---|",
    ]
    for task, item in payloads.items():
        lines.append(
            f"| {task.removeprefix('task')} | `{item['competition']}` | "
            f"[`AGENTS-ACTUALLY-INJECTED.md`]({item['path']}) | "
            f"{item['size_bytes']:,} | `{item['sha256']}` |"
        )
    lines.extend(
        [
            "",
            "The payloads are credential-redacted exports. The selected JSONL traces remain",
            "the authoritative event-level evidence for when each startup envelope was",
            "delivered and for the subsequent autonomy boundary. This index does not add",
            "the unrelated parent-repository `AGENTS.md`; it records only the six",
            "task-runtime payloads that were injected into the preserved runs.",
            "",
            "Verify the files through the six Task manifests and the root repository",
            "verifier:",
            "",
            "```bash",
            "for t in 1 2 3 4 5 6; do (cd task$t && sha256sum -c MANIFEST.sha256); done",
            "python3 verify_repository.py",
            "```",
        ]
    )
    (ROOT / "STARTUP_INSTRUCTION_INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    build_task1_solution_prefix()
    import build_task4_supplemental_traces

    build_task4_supplemental_traces.build()
    validate_task6_prefix()
    index = build_index()
    (ROOT / "AUTONOMOUS_TRACE_INDEX.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_markdown(index)
    write_costs(index)
    # Build after writing AUTONOMOUS_TRACE_INDEX.json because the prompt audit
    # compares the exact official pages with that canonical trace selection.
    import build_prompt_conformance_audit as prompt_audit

    audit = prompt_audit.build()
    (ROOT / "PROMPT_CONFORMANCE_AUDIT.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    prompt_audit.write_markdown(audit)
    import build_task4_rule_audit

    task4_audit = build_task4_rule_audit.build()
    (ROOT / "task4/RULE_DIFFERENCE_AUDIT.json").write_text(
        json.dumps(task4_audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    build_task4_rule_audit.write_markdown(task4_audit)
    write_startup_instruction_index()
    # Keep the organizer-facing rule navigation synchronized with the same
    # canonical refresh.  This builder is archive-independent, unlike the
    # submission/version audit, which has its own explicit --archive input.
    import build_requirement_evidence_matrix as evidence_matrix

    matrix = evidence_matrix.build()
    (ROOT / "REQUIREMENT_EVIDENCE_MATRIX.json").write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "REQUIREMENT_EVIDENCE_MATRIX.md").write_text(
        evidence_matrix.markdown(matrix), encoding="utf-8"
    )
    write_manifest(index)
    print(json.dumps({task: data["event_count"] for task, data in index["tasks"].items()}))


if __name__ == "__main__":
    main()
