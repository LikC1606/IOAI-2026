#!/usr/bin/env python3
"""Audit canonical trace prompts against the exact Kaggle prompt pages."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import build_autonomous_trace_material as material


ROOT = Path(__file__).resolve().parents[1]
LIVE_VERIFIED_UTC = "2026-08-25T12:26:55Z"
LIVE_NORMALIZED_HASHES = {
    "task1": {
        "starter": "f5c9018277ed64ee0f145fd4b9137277746cb1e4749aa011b1fb54310dcb73f4",
        "continuation": "f47d39855e6dc9a05e807a07aa190b9a365a846015c2c0db19db443c6cc5a1bf",
    },
    "task2": {
        "starter": "0d9e449a25d03ee9b067a063a05954dd66eb4b0636112c8f80602348badd55fd",
        "continuation": "e32045e13d252359b7b6201a1c64d00bd6db3f583b538933511f0e08d60e98fc",
    },
    "task3": {
        "starter": "7f219b0aa91b84df541a7107c4fee509dc765f2123aeb88fcb70ed09000c0952",
        "continuation": "c6d589f35bf3c61c537dd5ca944ee3fd785bedfffc4e6098ccdd4fd700d5b162",
    },
    "task4": {
        "starter": "c92f3a6300b4003e6ae4be991643c7a2a588a3b998b8a3873125fca204fca017",
        "continuation": "f6ffbc8d4db8e7235424287327b7ac546facda42b63adaabe5479c259145ac21",
    },
    "task5": {
        "starter": "c52cb147324def2436dc6c60b0c2a5d67454d94eb56e35e8e679f9a3bf7e4681",
        "continuation": "0acd3348752c3f145334b5a9e07e27f9b3f9ef6bf12316d6835cd35eca61a9ae",
    },
    "task6": {
        "starter": "1f9ab9a60ff7c52faff799b1c26e1370f1b02db6b55c9911bee52e8725882911",
        "continuation": "81cc3563c50cb0f1bb667b6fd103cc1a01374a7a9a3d5d80a2015fba00c23986",
    },
}
CAUSAL_FINDINGS = {
    "task1": {
        "selected_result_downstream_of_custom_prompt_text": True,
        "detail": (
            "The custom starter appendix precedes all work. The canonical solution trace "
            "ends at task_complete at 2026-08-05T18:24:58.140Z and contains no continuation. "
            "The complete raw reproduction separately preserves the post-solution custom "
            "continuation beginning at 2026-08-05T18:25:04.940Z."
        ),
    },
    "task2": {
        "selected_result_downstream_of_custom_prompt_text": True,
        "detail": (
            "The custom starter appendix precedes all work. No continuation event occurs "
            "in the later reproduction trace."
        ),
    },
    "task3": {
        "selected_result_downstream_of_custom_prompt_text": False,
        "detail": "The selected traces contain exact organizer Starter Prompt text and no continuation event.",
    },
    "task4": {
        "selected_result_downstream_of_custom_prompt_text": True,
        "detail": (
            "The two main solver starters have formatting changes. Ten main-runtime custom "
            "continuation events begin at 2026-08-07T04:34:35.176Z; the selected submission "
            "55316818 was sent later at 2026-08-07T06:10:48.923Z. Ten inherited custom "
            "starters and sixteen inherited continuation copies also appear across the "
            "complete worker/parallel-solver trace set."
        ),
    },
    "task5": {
        "selected_result_downstream_of_custom_prompt_text": False,
        "detail": "The selected traces contain exact organizer Starter Prompt text and no continuation event.",
    },
    "task6": {
        "selected_result_downstream_of_custom_prompt_text": False,
        "detail": "The selected pre-intervention traces contain exact organizer Starter Prompt text and no continuation event.",
    },
}


def normalized(text: str) -> str:
    """Ignore only the optional final newline introduced by copy/serialization."""
    return text.rstrip("\n")


def digest(text: str) -> str:
    return hashlib.sha256(normalized(text).encode("utf-8")).hexdigest()


def build() -> dict[str, Any]:
    index = json.loads((ROOT / "AUTONOMOUS_TRACE_INDEX.json").read_text(encoding="utf-8"))
    tasks: dict[str, Any] = {}
    for task, data in index["tasks"].items():
        starter = material.exact_organizer_prompt(task, "Starter Prompt")
        continuation = material.exact_organizer_prompt(task, "Continuation Prompt")
        official = {
            "starter": {"normalized_length": len(normalized(starter)), "normalized_sha256": digest(starter)},
            "continuation": {
                "normalized_length": len(normalized(continuation)),
                "normalized_sha256": digest(continuation),
            },
        }
        assert {name: item["normalized_sha256"] for name, item in official.items()} == LIVE_NORMALIZED_HASHES[task]
        custom_events = [
            item for item in data["user_prompt_audit"] if item["organizer_prompt_text_status"] == "custom"
        ]
        strict = data["strict_exact_organizer_prompt_text_conformance"]
        assert strict == (not custom_events)
        tasks[task] = {
            "competition": material.COMPETITIONS[task],
            "official_prompt_source": (
                f"{task}/official/OFFICIAL_PAGES_FULL.json"
                if (ROOT / f"{task}/official/OFFICIAL_PAGES_FULL.json").is_file()
                else {
                    "starter": f"{task}/official/start.md",
                    "continuation": f"{task}/official/CONTINUE_PROMPT_EXACT.md",
                }
            ),
            "official_prompt_hashes": official,
            "live_kaggle_page_matches_repository_source": True,
            "trace_prompt_classes": data["user_prompt_classes"],
            "custom_prompt_events": custom_events,
            "strict_exact_organizer_prompt_text_conformance": strict,
            "no_live_human_prompt_events_included": data["manual_human_prompt_events_included"] == 0,
            **CAUSAL_FINDINGS[task],
            "jury_status": "not_self_certified; organizer/Jury determines recognition",
        }
    return {
        "schema": "ioai.prompt-conformance-audit.v1",
        "scope": "canonical traces selected by AUTONOMOUS_TRACE_INDEX.json",
        "comparison": "Exact Unicode text after replacing <COMPETITION-SLUG>; only final newline is normalized.",
        "live_kaggle_cli_verification": {
            "verified_utc": LIVE_VERIFIED_UTC,
            "account": "researai",
            "command_pattern": (
                "KAGGLE_COMPETITION=<slug> kaggle competitions pages list "
                "--page-name '<Starter Prompt|Continuation Prompt>' --content --format json"
            ),
            "result": "All 12 live prompt bodies match the stored official sources and normalized hashes.",
        },
        "rule_reference": {
            "ioai_rules_format": "https://ioai-official.org/ai-model-track/rules-format/",
            "competition_pages": "Each Kaggle competition Overview contains Starter Prompt and Continuation Prompt pages marked for exact use.",
        },
        "important_distinction": (
            "No-live-human autonomy does not itself prove exact-organizer-prompt conformance. "
            "Custom preconfigured or appended prompt text is disclosed even when it contains "
            "no live human method or target suggestion."
        ),
        "tasks": tasks,
        "strict_exact_prompt_tasks": [task for task, data in tasks.items() if data["strict_exact_organizer_prompt_text_conformance"]],
        "non_exact_prompt_tasks": [task for task, data in tasks.items() if not data["strict_exact_organizer_prompt_text_conformance"]],
        "overall_jury_recognition": "not guaranteed; organizer/Jury determination required",
    }


def write_markdown(audit: dict[str, Any]) -> None:
    lines = [
        "# Official prompt conformance audit",
        "",
        "The Kaggle Overview for every Task 1–6 competition contains an exact Starter",
        "Prompt and exact Continuation Prompt. On 2026-08-25, all 12 live page bodies",
        "were retrieved with the Kaggle CLI and matched against the stored official",
        "sources. Trace inputs were then compared as exact Unicode text, normalizing",
        "only the optional final newline.",
        "",
        "No-live-human autonomy and exact-organizer-prompt conformance are separate.",
        "The former does not make a custom preconfigured/appended prompt official.",
        "",
        "| Task | Exact starter events | Exact continuation events | Custom prompt events | Strict exact text | Causal finding |",
        "|---|---:|---:|---:|:---:|---|",
    ]
    for task, data in audit["tasks"].items():
        classes = data["trace_prompt_classes"]
        exact_starter = sum(v for k, v in classes.items() if "exact_organizer_starter" in k)
        exact_continuation = sum(v for k, v in classes.items() if "exact_organizer_continuation" in k)
        custom = sum(v for k, v in classes.items() if "custom_" in k)
        lines.append(
            f"| {task} | {exact_starter} | {exact_continuation} | {custom} | "
            f"{'Yes' if data['strict_exact_organizer_prompt_text_conformance'] else 'No'} | "
            f"{data['detail']} |"
        )
    lines.extend(
        [
            "",
            "## Result",
            "",
            "- Exact-prompt trace text: Tasks 3, 5, and 6.",
            "- Non-exact prompt text: Tasks 1, 2, and 4.",
            "- Task 1's canonical solution prefix has no continuation, but its custom",
            "  starter appendix still prevents an exact-prompt-only claim; the raw",
            "  reproduction retains the post-result suffix separately.",
            "- Task 4's custom continuation is pre-result and substantive; its final",
            "  selected submission is downstream of it.",
            "",
            "This repository does not self-certify organizer acceptance. The Jury decides",
            "whether disclosed deviations are recognized. Event hashes, timestamps, prompt",
            "classes, and official prompt hashes are in",
            "[`PROMPT_CONFORMANCE_AUDIT.json`](PROMPT_CONFORMANCE_AUDIT.json).",
        ]
    )
    (ROOT / "PROMPT_CONFORMANCE_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    audit = build()
    (ROOT / "PROMPT_CONFORMANCE_AUDIT.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_markdown(audit)
    print(json.dumps({task: data["strict_exact_organizer_prompt_text_conformance"] for task, data in audit["tasks"].items()}))


if __name__ == "__main__":
    main()
