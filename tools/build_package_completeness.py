#!/usr/bin/env python3
"""Build a compact coverage matrix for the organizer evidence package.

The detailed trace, prompt, result, and cost ledgers remain authoritative. This
builder only joins their recorded fields; it does not infer compliance or
promote candidate-level provenance to an exact claim.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

TASK_META: dict[str, dict[str, str]] = {
    "task1": {
        "canonical_material": "Later 120-minute reproduction prefix; 350-event exact-prompt formal prefix is supplemental",
        "official_binding": "Account result is reconciled, but neither public trace selection is causal evidence for the official final",
        "artifact_status": "Agent/reproduction artifacts are preserved; official-final extraction is a kernel-linked candidate, not byte-confirmed",
        "known_gap": "Custom starter in reproduction; recovered formal human-influenced suffix withheld; 38 captured versions vs literal 20 and repeated official version",
    },
    "task2": {
        "canonical_material": "Complete later 120-minute reproduction; 705-event exact-prompt formal prefix and eligible v2 chain are supplemental",
        "official_binding": "Account result is reconciled, but the official final is downstream of the modified formal continuation and not bound to the later reproduction",
        "artifact_status": "Eligible v2 source/output/log are exact; official-final extraction is a kernel-linked candidate, not byte-confirmed",
        "known_gap": "Custom starter in reproduction; recovered formal modified-continuation suffix withheld; repeated pre-deadline version",
    },
    "task3": {
        "canonical_material": "Four autonomous traces covering the eight scored pre-boundary versions",
        "official_binding": "Official final refs and selected trace are aligned",
        "artifact_status": "Eight source/output chains replay and verify against the supplied competition data",
        "known_gap": "Account-wide count and repeated version conflict remain for organizer interpretation; historical reports are short and v8 contains factual score/distribution errors",
    },
    "task4": {
        "canonical_material": "Twelve autonomous traces, including the corrected supplemental parallel-solver set",
        "official_binding": "Official final ref and selected trace are aligned",
        "artifact_status": "Final source, metadata, log, and output hash are verified; the 190 MB CSV is retained by hash in the compact package",
        "known_gap": "Starter formatting differs and continuation is substantively non-exact; local __pycache__ and H100-development scope are disclosed",
    },
    "task5": {
        "canonical_material": "Fourteen autonomous traces through the run boundary",
        "official_binding": "Official v6 final ref and selected trace are aligned",
        "artifact_status": "v6 output/log/metadata and source hash are preserved; historical v6 source pull currently returns HTTP 403",
        "known_gap": "Source is the trace-preserved formal-run copy rather than an independently redownloaded historical v6 file; exhaustive local H100 runtime is unavailable",
    },
    "task6": {
        "canonical_material": "Three autonomous traces: bounded main trace plus two pre-boundary worker traces",
        "official_binding": "Official v3 final ref and selected trace are aligned",
        "artifact_status": "Exact notebook, metadata, CSV, decoded source, weights, and parameter count verify",
        "known_gap": "Historical report has dropout/range errors; evaluator batching dependence and incomplete local H100 accounting are explicitly disclosed",
    },
}


def read_json(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def build() -> dict[str, Any]:
    trace_index = read_json("AUTONOMOUS_TRACE_INDEX.json")
    costs = read_json("AUTONOMOUS_COSTS.json")
    reproduction = read_json("REPRODUCTION_TRACE_INDEX.json")

    tasks: dict[str, Any] = {}
    total_files = total_events = total_tokens = 0
    for task, trace in trace_index["tasks"].items():
        cost = costs["tasks"][task]
        official = read_json(f"{task}/remote/FINAL_ACCOUNT_RESULTS.json")[
            "official_final_result"
        ]
        coverage = trace["organizer_required_event_coverage"]
        task_files = len(trace["trace_files"])
        task_events = trace["event_count"]
        task_tokens = trace["token_usage_cumulative_sum_across_traces"]
        total_files += task_files
        total_events += task_events
        total_tokens += task_tokens["total_tokens"]
        gpu = cost["gpu"]
        tasks[task] = {
            "canonical_material": TASK_META[task]["canonical_material"],
            "trace": {
                "paths": [item["path"] for item in trace["trace_files"]],
                "trace_file_count": task_files,
                "event_count": task_events,
                "total_tokens": task_tokens["total_tokens"],
                "manual_human_prompt_events_included": trace[
                    "manual_human_prompt_events_included"
                ],
                "strict_exact_organizer_prompt_text_conformance": trace[
                    "strict_exact_organizer_prompt_text_conformance"
                ],
                "user_prompt_classes": trace["user_prompt_classes"],
            },
            "observable_coverage": {
                "assistant_output_events": coverage["assistant_output_events"],
                "logical_function_call_events": trace["logical_function_calls"],
                "function_call_output_events": coverage["function_call_output_events"],
                "custom_tool_call_events": coverage["custom_tool_call_events"],
                "custom_tool_call_output_events": coverage[
                    "custom_tool_call_output_events"
                ],
            },
            "model": {
                "provider": trace["model_provider"],
                "model": trace["canonical_model"],
                "reasoning_effort": trace["reasoning_effort"],
            },
            "official_result": {
                "submission_refs": official["submission_refs"],
                "public_score": official["public_score"],
                "private_score": official["private_score"],
                "binding_status": TASK_META[task]["official_binding"],
            },
            "compute": {
                "accelerator": gpu["accelerator"],
                "runtime_scope": gpu["runtime_scope"],
                "runtime_seconds": gpu["runtime_seconds"],
                "gpu_cost_usd": gpu["gpu_cost_usd"],
                "gpu_cost_status": gpu["cost_status"],
                "local_development_runtime_seconds": gpu.get(
                    "local_development_runtime_seconds"
                ),
                "local_development_runtime_status": gpu.get(
                    "local_development_runtime_status"
                ),
            },
            "api_cost": {
                "usd": cost["api_cost_usd"],
                "status": cost["api_cost_status"],
                "token_vector": cost["token_usage"],
            },
            "artifact_status": TASK_META[task]["artifact_status"],
            "known_gap": TASK_META[task]["known_gap"],
        }

    reproduction_files = len(reproduction["tasks"])
    reproduction_events = sum(
        task["trace_file"]["event_count"] for task in reproduction["tasks"].values()
    )
    reproduction_tokens = sum(
        task["trace_file"]["token_usage_cumulative_final"]["total_tokens"]
        for task in reproduction["tasks"].values()
    )
    return {
        "schema": "ioai.package-completeness.v1",
        "generated_by": "tools/build_package_completeness.py",
        "scope": "reviewer-facing coverage join over checked-in trace, result, prompt, and cost ledgers",
        "source_ledgers": [
            "AUTONOMOUS_TRACE_INDEX.json",
            "AUTONOMOUS_COSTS.json",
            "REPRODUCTION_TRACE_INDEX.json",
            "taskN/remote/FINAL_ACCOUNT_RESULTS.json",
        ],
        "global": {
            "autonomous_trace_files": total_files,
            "autonomous_events": total_events,
            "autonomous_tokens": total_tokens,
            "later_reproduction_trace_files": reproduction_files,
            "later_reproduction_events": reproduction_events,
            "later_reproduction_tokens": reproduction_tokens,
            "api_cost_usd_total": costs["api_cost_usd_total"],
            "gpu_cost_usd_total": costs["gpu_cost_usd_total"],
            "strict_all_six_claim_supported": False,
        },
        "tasks": tasks,
        "interpretation": {
            "complete": "The named observable material is present within the declared scope and passes integrity checks.",
            "qualified": "The material is present but its causal, exact-prompt, exact-version, or artifact scope is limited as stated.",
            "unavailable": "The ledger deliberately records null/incomplete rather than estimating from unsupported rates or overlapping runtime records.",
            "not_a_certificate": "This matrix does not decide organizer/Jury eligibility or recognition.",
        },
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Package completeness and evidence coverage",
        "",
        "This page is a compact join of the checked-in trace, prompt, result, and",
        "cost ledgers. It answers **where each requested deliverable is and what",
        "qualification travels with it**; it is not a compliance certificate.",
        "The machine-readable form is [`PACKAGE_COMPLETENESS.json`](PACKAGE_COMPLETENESS.json).",
        "",
        "## Global coverage",
        "",
        "| Scope | Trace files | Events | Cumulative tokens |",
        "|---|---:|---:|---:|",
        f"| Selected human-intervention-free material | {data['global']['autonomous_trace_files']} | {data['global']['autonomous_events']} | {data['global']['autonomous_tokens']:,} |",
        f"| Later Task 1/2 reproduction material | {data['global']['later_reproduction_trace_files']} | {data['global']['later_reproduction_events']} | {data['global']['later_reproduction_tokens']:,} |",
        "",
        "All selected traces include zero live-human prompt events. Observable",
        "startup/organizer prompts, visible Agent messages, worker assignments,",
        "tool-call envelopes, tool outputs, timestamps, and token telemetry are",
        "retained within each declared boundary. Hidden chain-of-thought, opaque",
        "encrypted reasoning, credentials, private endpoints, and excluded human",
        "prompt bodies are not published.",
        "",
        "## Requested deliverables by task",
        "",
        "| Task | Trace and prompt coverage | Observable outputs/tool calls | Model and tokens | Official result binding | GPU/runtime and USD | Main qualification |",
        "|---|---|---|---|---|---|---|",
    ]
    for task, item in data["tasks"].items():
        tr = item["trace"]
        obs = item["observable_coverage"]
        model = item["model"]
        comp = item["compute"]
        official = item["official_result"]
        prompt = "exact" if tr["strict_exact_organizer_prompt_text_conformance"] else "non-exact/custom disclosed"
        if comp["gpu_cost_usd"] == 0:
            gpu_usd = "0 (" + str(comp["gpu_cost_status"]) + ")"
        else:
            gpu_usd = "null (" + str(comp["gpu_cost_status"]) + ")"
        local = comp["local_development_runtime_status"] or "not applicable"
        lines.append(
            f"| [{task}]({task}/README.md) | {tr['trace_file_count']} files / {tr['event_count']} events; {prompt}; 0 live-human events | assistant {obs['assistant_output_events']}; logical calls {obs['logical_function_call_events']}; tool calls {obs['custom_tool_call_events']} (+ outputs) | `{model['provider']} / {model['model']}` / `{model['reasoning_effort']}`; {tr['total_tokens']:,} total tokens | `{official['submission_refs']}`: Public {official['public_score']}, Private {official['private_score']}; {official['binding_status']} | {comp['accelerator']}, {comp['runtime_seconds']} s; GPU USD {gpu_usd}; local: {local} | {item['known_gap']} |"
        )
    lines.extend(
        [
            "",
            "## Cost interpretation",
            "",
            "Token vectors and the selected remote runtime are recorded per task.",
            "API USD is `null` for every task because no provider invoice or",
            "applicable `ioai_allowed / gpt-5.6-sol` rate was captured. GPU USD is",
            "also `null` except the explicit zero for the CPU-only Task 3 scope.",
            "Tasks 4–6 additionally contain local H100 development observations",
            "whose exhaustive non-overlapping runtime is unavailable; no estimate",
            "is substituted.",
            "",
            "## Where to verify",
            "",
            "- Trace inventory and event-level coverage: [`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json) and [`AUTONOMOUS_TRACE_MATERIAL.md`](AUTONOMOUS_TRACE_MATERIAL.md).",
            "- Prompt exactness and custom/inherited prompt classes: [`PROMPT_CONFORMANCE_AUDIT.md`](PROMPT_CONFORMANCE_AUDIT.md).",
            "- Official account reconciliation: [`FINAL_SUBMISSION_RESULTS.md`](FINAL_SUBMISSION_RESULTS.md) and each task's `remote/FINAL_ACCOUNT_RESULTS.json`.",
            "- Model/token/remote-runtime accounting: [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json) and [`COSTS.json`](COSTS.json).",
            "- Remaining organizer/Jury decisions: [`OPEN_REVIEW_ITEMS.md`](OPEN_REVIEW_ITEMS.md).",
            "- Integrity route: `python3 verify_repository.py` plus the six task manifests and the two root material manifests.",
            "",
            "The current package deliberately keeps `strict_all_six_claim_supported` false.",
            "A green verifier result proves internal consistency only; it does not",
            "establish organizer acceptance.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    data = build()
    (ROOT / "PACKAGE_COMPLETENESS.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (ROOT / "PACKAGE_COMPLETENESS.md").write_text(markdown(data), encoding="utf-8")


if __name__ == "__main__":
    main()
