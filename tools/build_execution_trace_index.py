#!/usr/bin/env python3
"""Index the observable agent traces selected for repository publication.

Task 6 was captured locally and redacted before publication.  Its repository
selection contains only the prefix before the first live human intervention;
the complete source and post-intervention worker traces remain outside the
repository.  The selected JSONL events retain startup/organizer prompts,
visible assistant messages, tool-call envelopes, tool outputs, timestamps,
and token-count telemetry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASK3_TOKEN_USAGE = ROOT / "task3/evidence/AUTONOMOUS_TOKEN_USAGE.json"
DEFAULT_TASK6_RAW = Path(
    "/workspace/IOAI/ioai2-competition-runs-task6-20260809/"
    "ioai-2026-task-6-westlake-nlp-60/codex-home/sessions/2026/08/09"
)
RECOVERY_NOTES = {
    "task1": (
        "The original Task 1 run record was unavailable after a school-server restart; "
        "the selected trace is a later fresh reproduction using the same configured "
        "solver/system and organizer constraints, not the original run record."
    ),
    "task2": (
        "The original Task 2 run record was unavailable after a school-server restart; "
        "the selected trace is a later fresh reproduction using the same configured "
        "solver/system and organizer constraints, not the original run record."
    ),
}

PRIVATE_ENDPOINT_RE = re.compile(
    r"https?://(?:codex\.aiswing\.fun|api\.smilecodex\.space|127\.0\.0\.1:\d+)",
    re.IGNORECASE,
)
SECRET_VALUE_RES = (
    re.compile(r"KGAT_[A-Za-z0-9_-]+"),
    re.compile(r"(?<![A-Za-z0-9_-])sk-(?:proj-)?[A-Za-z0-9_]{24,}"),
    re.compile(
        r"(?i)(?:KAGGLE_API_TOKEN|OPENAI_API_KEY|ACCESS_TOKEN|REFRESH_TOKEN|"
        r"BEARER)\s*[=:]\s*[^\s,;]+"
    ),
)
SENSITIVE_KEY_RE = re.compile(
    r"(?i)^(?:token|api[_ -]?key|authorization|proxy|base[_ -]?url|"
    r"password|secret|credential)$"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def redact(value: Any, key: str = "") -> Any:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for child_key, child_value in value.items():
            # This is encrypted internal reasoning, not an observable prompt,
            # output, or tool call.  Do not publish or attempt to interpret it.
            if child_key == "encrypted_content":
                result[child_key] = "[OMITTED_OPAQUE_REASONING]"
            elif SENSITIVE_KEY_RE.search(str(child_key)):
                result[child_key] = "[REDACTED]"
            else:
                result[child_key] = redact(child_value, str(child_key))
        return result
    if isinstance(value, list):
        return [redact(item, key) for item in value]
    if isinstance(value, str):
        result = value
        for pattern in SECRET_VALUE_RES:
            result = pattern.sub("[REDACTED_SECRET]", result)
        result = PRIVATE_ENDPOINT_RE.sub("[REDACTED_PRIVATE_ENDPOINT]", result)
        if SENSITIVE_KEY_RE.search(key):
            return "[REDACTED]"
        return result
    return value


def jsonl_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL {path}:{line_number}") from exc
    return events


def token_totals(events: list[dict[str, Any]]) -> dict[str, int] | None:
    candidates: list[dict[str, Any]] = []
    for event in events:
        payload = event.get("payload", {})
        if event.get("type") != "event_msg" or payload.get("type") != "token_count":
            continue
        total = payload.get("info", {}).get("total_token_usage")
        if isinstance(total, dict) and isinstance(total.get("total_tokens"), int):
            candidates.append(total)
    if not candidates:
        return None
    # Cumulative telemetry is monotone in normal traces; max is robust to a
    # repeated final event and avoids counting per-turn deltas twice.
    return max(candidates, key=lambda item: item["total_tokens"])


def trace_record(path: Path, relative: str, role_hint: str | None = None) -> dict[str, Any]:
    events = jsonl_events(path)
    event_types = Counter(str(event.get("type")) for event in events)
    response_item_types: Counter[str] = Counter()
    function_calls: Counter[str] = Counter()
    custom_calls: Counter[str] = Counter()
    roles = Counter()
    timestamps = [str(event["timestamp"]) for event in events if event.get("timestamp")]
    models: set[str] = set()
    reasoning_efforts: set[str] = set()
    role = role_hint
    for event in events:
        payload = event.get("payload", {})
        if event.get("type") == "response_item":
            item_type = str(payload.get("type", "<unknown>"))
            response_item_types[item_type] += 1
            if item_type == "function_call":
                function_calls[str(payload.get("name", "<unknown>"))] += 1
            elif item_type == "custom_tool_call":
                custom_calls[str(payload.get("name", "<unknown>"))] += 1
            if payload.get("role"):
                roles[str(payload["role"])] += 1
        if event.get("type") == "session_meta":
            meta = payload
            if role is None:
                role = "subagent" if meta.get("thread_source") == "subagent" else "main"
        # Only turn_context identifies the model executing this trace. Model
        # names printed by unrelated shell processes are not execution evidence.
        if event.get("type") == "turn_context" and isinstance(payload.get("model"), str):
            models.add(payload["model"])
            effort = payload.get("effort") or payload.get("reasoning_effort")
            if isinstance(effort, str):
                reasoning_efforts.add(effort)
    coverage = {
        "prompt_message_events": roles.get("user", 0) + roles.get("developer", 0),
        "user_prompt_events": roles.get("user", 0),
        "developer_prompt_events": roles.get("developer", 0),
        "assistant_output_events": roles.get("assistant", 0),
        "function_call_events": response_item_types.get("function_call", 0),
        "function_call_output_events": response_item_types.get("function_call_output", 0),
        "custom_tool_call_events": response_item_types.get("custom_tool_call", 0),
        "custom_tool_call_output_events": response_item_types.get("custom_tool_call_output", 0),
    }
    return {
        "path": relative,
        "sha256": sha256(path),
        "role": role or "unknown",
        "event_count": len(events),
        "event_types": dict(sorted(event_types.items())),
        "response_item_types": dict(sorted(response_item_types.items())),
        "organizer_required_event_coverage": coverage,
        "first_timestamp": min(timestamps) if timestamps else None,
        "last_timestamp": max(timestamps) if timestamps else None,
        "message_counts": dict(sorted(roles.items())),
        "logical_function_calls": sum(function_calls.values()),
        "logical_function_call_names": dict(sorted(function_calls.items())),
        "exec_wrapper_custom_tool_calls": sum(custom_calls.values()),
        "custom_tool_call_names": dict(sorted(custom_calls.items())),
        "models_observed": sorted(models),
        "reasoning_efforts_observed": sorted(reasoning_efforts),
        "token_usage_cumulative_final": token_totals(events),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    task_roots: dict[str, list[Path]] = {
        "task1": [ROOT / "task1/evidence/canonical"],
        "task2": [ROOT / "task2/evidence/reproduction-120m"],
        "task3": [ROOT / "task3/evidence/rollouts"],
        "task4": [
            ROOT / "task4/evidence/rollouts",
            ROOT / "task4/evidence/supplemental-rollouts",
        ],
        "task5": [ROOT / "task5/evidence/rollouts"],
    }
    task_roots["task6"] = [
        ROOT / "task6/evidence/autonomous-only",
        ROOT / "task6/evidence/rollouts",
    ]
    token_overrides: dict[str, dict[str, int]] = {}
    if TASK3_TOKEN_USAGE.is_file():
        token_data = json.loads(TASK3_TOKEN_USAGE.read_text(encoding="utf-8"))
        token_overrides = {
            item["repository_trace_path"]: item["token_usage"]
            for item in token_data.get("traces", [])
        }

    index: dict[str, Any] = {
        "schema": "ioai.execution-trace-index.v1",
        "generated_by": "tools/build_execution_trace_index.py",
        "scope": "published human-intervention-free observable trace package for Tasks 1-6",
        "redaction": {
            "task1_to_task5": "repository-provided redacted pre-intervention traces",
            "task6": "pre-human-intervention prefix only; credentials/private endpoints removed; encrypted_content replaced by an opaque placeholder",
            "raw_task6_not_in_repository": True,
        },
        "tasks": {},
    }
    for task_name, trace_roots in task_roots.items():
        files = []
        for trace_root in trace_roots:
            for path in sorted(trace_root.glob("*.jsonl")):
                relative = path.relative_to(ROOT).as_posix()
                record = trace_record(path, relative)
                if relative in token_overrides:
                    record["token_usage_cumulative_final"] = token_overrides[relative]
                    record["token_usage_source"] = "task3/evidence/AUTONOMOUS_TOKEN_USAGE.json"
                files.append(record)
        files.sort(key=lambda item: item["path"])
        all_tokens = [item["token_usage_cumulative_final"] for item in files if item["token_usage_cumulative_final"]]
        aggregate: dict[str, int] | None
        if all_tokens:
            aggregate = {
                key: sum(int(item.get(key, 0)) for item in all_tokens)
                for key in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens")
            }
        else:
            aggregate = None
        index["tasks"][task_name] = {
            "trace_files": files,
            **({"record_recovery_note": RECOVERY_NOTES[task_name]} if task_name in RECOVERY_NOTES else {}),
            "canonical_model": "gpt-5.6-sol",
            "model_provider": "ioai_allowed",
            "reasoning_effort": "max" if task_name in {"task1", "task2", "task3", "task4"} else "xhigh",
            "event_count": sum(item["event_count"] for item in files),
            "logical_function_calls": sum(item["logical_function_calls"] for item in files),
            "exec_wrapper_custom_tool_calls": sum(item["exec_wrapper_custom_tool_calls"] for item in files),
            "message_counts": dict(sorted(sum((Counter(item["message_counts"]) for item in files), Counter()).items())),
            "response_item_types": dict(
                sorted(
                    sum(
                        (Counter(item["response_item_types"]) for item in files),
                        Counter(),
                    ).items()
                )
            ),
            "organizer_required_event_coverage": dict(
                sorted(
                    sum(
                        (
                            Counter(item["organizer_required_event_coverage"])
                            for item in files
                        ),
                        Counter(),
                    ).items()
                )
            ),
            "models_observed": sorted({model for item in files for model in item["models_observed"]}),
            "reasoning_efforts_observed": sorted(
                {
                    effort
                    for item in files
                    for effort in item["reasoning_efforts_observed"]
                }
            ),
            "token_usage_cumulative_sum_across_traces": aggregate,
            "token_usage_note": (
                "Task 3 totals were recovered from the matching local private originals; "
                "only aggregate telemetry and original hashes are published."
                if task_name == "task3"
                else "Final cumulative counters are summed once per trace."
            ),
        }

    (ROOT / "EXECUTION_TRACE_INDEX.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    markdown: list[str] = [
        "# Execution trace index",
        "",
        "Generated from the JSON index by `tools/build_execution_trace_index.py`.",
        "The JSONL files are credential-redacted observable traces; see",
        "[`EXECUTION_TRACES.md`](EXECUTION_TRACES.md) for interpretation and limits.",
        "",
        "Task 1 and Task 2 records were recovered as later fresh reproductions",
        "after the original run records became unavailable following a school-server",
        "restart; their notes and scope are recorded in the JSON index.",
        "",
        "| Task | Files | Events | Logical calls | Outer exec calls | Tokens |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for task_name, task_data in index["tasks"].items():
        tokens = task_data["token_usage_cumulative_sum_across_traces"]
        token_text = str(tokens["total_tokens"]) if tokens else "unavailable"
        markdown.append(
            f"| {task_name} | {len(task_data['trace_files'])} | "
            f"{task_data['event_count']} | {task_data['logical_function_calls']} | "
            f"{task_data['exec_wrapper_custom_tool_calls']} | {token_text} |"
        )
    markdown.extend(["", "## Files", "", "| Task | Role | Events | SHA-256 | Path |", "|---|---|---:|---|---|"])
    for task_name, task_data in index["tasks"].items():
        for item in task_data["trace_files"]:
            markdown.append(
                f"| {task_name} | {item['role']} | {item['event_count']} | "
                f"`{item['sha256']}` | `{item['path']}` |"
            )
    (ROOT / "EXECUTION_TRACE_INDEX.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    print(json.dumps(index, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
