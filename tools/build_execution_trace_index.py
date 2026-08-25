#!/usr/bin/env python3
"""Index observable agent traces and import a redacted Task 6 trace set.

The repository already contains redacted Task 1--5 JSONL files.  Task 6 was
captured locally, so this helper copies it into the package after removing
credentials, private transport endpoints, and opaque encrypted reasoning.
The JSONL events retain user/developer prompts, visible assistant messages,
tool-call envelopes, tool outputs, timestamps, and token-count telemetry.
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
    function_calls: Counter[str] = Counter()
    custom_calls: Counter[str] = Counter()
    roles = Counter()
    timestamps = [str(event["timestamp"]) for event in events if event.get("timestamp")]
    models: set[str] = set()
    role = role_hint
    for event in events:
        payload = event.get("payload", {})
        if event.get("type") == "response_item":
            item_type = payload.get("type")
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
        text = json.dumps(event, ensure_ascii=False)
        models.update(re.findall(r"\bgpt-[0-9]+\.[0-9]+-[A-Za-z0-9-]+\b", text))
    return {
        "path": relative,
        "sha256": sha256(path),
        "role": role or "unknown",
        "event_count": len(events),
        "event_types": dict(sorted(event_types.items())),
        "first_timestamp": min(timestamps) if timestamps else None,
        "last_timestamp": max(timestamps) if timestamps else None,
        "message_counts": dict(sorted(roles.items())),
        "logical_function_calls": sum(function_calls.values()),
        "logical_function_call_names": dict(sorted(function_calls.items())),
        "exec_wrapper_custom_tool_calls": sum(custom_calls.values()),
        "custom_tool_call_names": dict(sorted(custom_calls.items())),
        "models_observed": sorted(models),
        "token_usage_cumulative_final": token_totals(events),
    }


def import_task6(raw_dir: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    imported: list[Path] = []
    for source in sorted(raw_dir.glob("*.jsonl")):
        target = output_dir / source.name
        with source.open(encoding="utf-8") as source_handle, target.open("w", encoding="utf-8") as target_handle:
            for line in source_handle:
                if not line.strip():
                    continue
                target_handle.write(
                    json.dumps(redact(json.loads(line)), ensure_ascii=False, separators=(",", ":"))
                    + "\n"
                )
        imported.append(target)
    return imported


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task6-raw", type=Path, default=DEFAULT_TASK6_RAW)
    args = parser.parse_args()

    task6_output = ROOT / "task6/evidence/rollouts"
    if not args.task6_raw.is_dir():
        raise SystemExit(f"Task 6 raw trace directory not found: {args.task6_raw}")
    import_task6(args.task6_raw, task6_output)

    task_roots: dict[str, list[Path]] = {
        f"task{task}": [ROOT / f"task{task}/evidence/rollouts"] for task in range(1, 6)
    }
    # Task 1 deliberately has a second, post-boundary agent-execution trace.
    # It is part of the observable run and must be counted separately from the
    # formal pre-boundary rollout.
    task_roots["task1"].append(ROOT / "task1/evidence/submission-execution")
    task_roots["task6"] = [task6_output]
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
        "scope": "full observable trace package, including separately disclosed post-boundary material where present",
        "redaction": {
            "task1_to_task5": "repository-provided redacted traces",
            "task6": "credentials/private endpoints removed; encrypted_content replaced by an opaque placeholder",
            "raw_task6_not_in_repository": True,
        },
        "tasks": {},
    }
    for task_name, trace_roots in task_roots.items():
        files = []
        for trace_root in trace_roots:
            for path in sorted(trace_root.glob("*.jsonl")):
                relative = path.relative_to(ROOT).as_posix()
                role_hint = None
                if "submission-execution" in path.parts:
                    role_hint = "agent-executed-after-supervision-boundary"
                record = trace_record(path, relative, role_hint=role_hint)
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
            "canonical_model": "gpt-5.6-sol",
            "model_provider": "ioai_allowed",
            "event_count": sum(item["event_count"] for item in files),
            "logical_function_calls": sum(item["logical_function_calls"] for item in files),
            "exec_wrapper_custom_tool_calls": sum(item["exec_wrapper_custom_tool_calls"] for item in files),
            "message_counts": dict(sorted(sum((Counter(item["message_counts"]) for item in files), Counter()).items())),
            "models_observed": sorted({model for item in files for model in item["models_observed"]}),
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
