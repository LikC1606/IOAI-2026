#!/usr/bin/env python3
"""Build an evidence-first Task 4 competition-rule difference audit."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "task4"
SOURCE = TASK / "notebooks/REMOTE_CURRENT_V4.py"
METADATA = TASK / "notebooks/kernel-metadata.json"
REMOTE_METADATA = TASK / "notebooks/REMOTE_CURRENT_METADATA.json"
OUTPUT_PROVENANCE = TASK / "remote/V4_OUTPUT_PROVENANCE.json"
FINAL_RESULT = TASK / "remote/FINAL_ACCOUNT_RESULTS.json"
LOG = TASK / "remote/V4_KERNEL.log"
PROMPT_AUDIT = ROOT / "PROMPT_CONFORMANCE_AUDIT.json"
TRACE_INDEX = ROOT / "AUTONOMOUS_TRACE_INDEX.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def finding(
    rule_id: str,
    requirement: str,
    status: str,
    conclusion: str,
    evidence: list[str],
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "requirement": requirement,
        "status": status,
        "conclusion": conclusion,
        "evidence": evidence,
    }


def build() -> dict[str, Any]:
    source = SOURCE.read_text(encoding="utf-8")
    metadata = load(METADATA)
    remote_metadata = load(REMOTE_METADATA)
    output = load(OUTPUT_PROVENANCE)
    final_result = load(FINAL_RESULT)
    log = load(LOG)
    prompt = load(PROMPT_AUDIT)["tasks"]["task4"]
    trace = load(TRACE_INDEX)["tasks"]["task4"]

    source_hash = sha256(SOURCE)
    assert source_hash == "d467bc5a1e7c83ae7da780aaf01fb6ac001fd326e514495cae3a9279b7b6301b"
    assert sha256(TASK / "notebooks/script.py") == source_hash
    assert metadata == {
        "id": "researai/ioai-2026-task-4-westlake-nlp-24-solution",
        "title": "ioai-2026-task-4-westlake-nlp-24-solution",
        "code_file": "script.py",
        "language": "python",
        "kernel_type": "script",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": False,
        "machine_shape": "NvidiaTeslaT4",
        "dataset_sources": ["kamalkhan/ioai-2026-wheel-dataset"],
        "competition_sources": ["ioai-2026-task-4-westlake-nlp-24"],
        "kernel_sources": [],
        "model_sources": [],
    }
    for key in (
        "id", "title", "language", "kernel_type", "is_private", "enable_gpu",
        "enable_internet", "machine_shape", "dataset_sources", "competition_sources",
        "kernel_sources", "model_sources",
    ):
        assert remote_metadata[key] == metadata[key], key

    setup_start = source.index("# ─── IOAI 2026 — environment setup.")
    setup_marker = "setup_ioai_env()\n# ───────────────────────────────────────────────────────────────────────────────\n"
    setup_end = source.index(setup_marker, setup_start) + len(setup_marker)
    setup_hash = hashlib.sha256(source[setup_start:setup_end].encode("utf-8")).hexdigest()
    assert setup_hash == "4a9f323d5e28991bd6ba65bb3f7161fe1ad9a637b0aaca343afe77e951bf672c"

    report_sections = re.findall(r"^# (\d+)\. [A-Z][A-Z ]+$", source, re.MULTILINE)
    assert report_sections == [str(index) for index in range(1, 11)]
    assert source.startswith("# =============================================================================\n# IOAI 2026")
    assert "torch.device(\"cuda:0\" if torch.cuda.is_available() else \"cpu\")" in source
    assert "models.resnet18(weights=None)" in source
    # One occurrence is in the official illustrative runtime string that is
    # immediately replaced; the second is the final executed runtime.
    assert source.count("timm.create_model(") == 2
    assert "file=MODELS_ROOT / \"vit_tiny_patch16_224.safetensors\"" in source
    assert "custom_load=False" in source
    assert not re.search(
        r"cuda:1|DataParallel|DistributedDataParallel|requests\.|urllib\.|torch\.hub|"
        r"load_state_dict_from_url|from_pretrained|https?://",
        source,
    )

    stdout = [entry for entry in log if entry.get("stream_name") == "stdout"]
    log_text = "".join(str(entry.get("data", "")) for entry in stdout)
    write_events = [entry for entry in stdout if "wrote /kaggle/working/submission.csv" in entry.get("data", "")]
    assert len(write_events) == 1 and float(write_events[0]["time"]) == 315.957934901
    assert "Device: cuda:0" in log_text
    assert "Double Agent root: /kaggle/input/competitions/ioai-2026-task-4-westlake-nlp-24/data" in log_text
    assert output["version"] == 4 and output["submission_ref"] == 55316818
    assert output["rows"] == 200 and output["columns"] == ["id", "delta_a", "delta_b"]
    assert output["sha256"] == "bdb202711d6494bc94c331d549b0fa7956aa1d9eb585c247ae0dfce723f76542"
    assert output["remote_runtime_seconds"] == 316
    assert final_result["official_final_result"] == {
        "selection_basis": "highest Public score among submissions sent before the official deadline",
        "submission_refs": [55316818],
        "public_score": 98.41,
        "private_score": 98.32,
    }
    assert final_result["autonomous_and_official_deadline_best"]["seconds_before_official_deadline"] == 251.077
    assert trace["event_count"] == 5881 and len(trace["trace_files"]) == 12

    prompt_classes = prompt["trace_prompt_classes"]
    assert prompt_classes == {
        "custom_continuation_prompt": 10,
        "custom_starter_prompt": 2,
        "inherited_custom_continuation_prompt": 16,
        "inherited_custom_starter_prompt": 10,
        "startup_instructions": 12,
    }

    findings = [
        finding(
            "prompt.exact_text",
            "Use the exact organizer Starter and Continuation Prompt text.",
            "disclosed_deviation",
            (
                "The starter differences are formatting-only in substance, but the continuation "
                "is a substantive generic workflow template. The final result is downstream of it; "
                "strict exact-prompt conformance is false."
            ),
            [
                "PROMPT_CONFORMANCE_AUDIT.json: tasks.task4",
                "AUTONOMOUS_TRACE_INDEX.json: tasks.task4.user_prompt_audit",
            ],
        ),
        finding(
            "trace.complete_solver_set",
            "Provide the execution traces that causally contributed to the final Task 4 path.",
            "evidence_supported_compliant_after_correction",
            (
                "The canonical set now contains the five formal-run traces and seven separate "
                "parallel-solver traces that produced versions 2/3 and the comparison evidence "
                "used by version 4: 12 traces and 5,881 events."
            ),
            [
                "AUTONOMOUS_TRACE_INDEX.json: tasks.task4.trace_files",
                "task4/evidence/SUPPLEMENTAL_ROLLOUT_PROVENANCE.json",
            ],
        ),
        finding(
            "submission.notebook_only",
            "Generate and submit the result from a competition-associated Kaggle Notebook.",
            "evidence_supported_compliant",
            "Submission 55316818 names Kernel version 4 output submission.csv; no local-file upload path was used.",
            [
                "task4/records/submissions.jsonl: competition_submit version 4",
                "task4/remote/V4_OUTPUT_PROVENANCE.json",
                "task4/remote/FINAL_ACCOUNT_RESULTS.json",
            ],
        ),
        finding(
            "submission.folder_two_files",
            "Prepare a notebook folder containing exactly script.py and kernel-metadata.json.",
            "disclosed_process_deviation_remote_artifact_unaffected",
            (
                "A pre-v4 trace listing shows submission/__pycache__/script.cpython-311.pyc in the "
                "local folder; the v3 command itself ran py_compile immediately before push. Thus "
                "the local folder was not strictly two-file at those moments. Kaggle's remote source "
                "record still consists of the declared script/metadata artifact, and the final source "
                "hash matches the pulled version 4."
            ),
            [
                "task4/evidence/rollouts/rollout-2026-08-07T12-18-29-019fda71-a6a2-7a22-8c18-22e99f127422.jsonl: 2026-08-07T05:54:36.436Z output_check",
                "task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-06-019fda9b-6b63-7031-a6dd-52db684209be.jsonl: 2026-08-07T05:54:22.092Z",
                "task4/notebooks/REMOTE_CURRENT_V4.py",
            ],
        ),
        finding(
            "submission.timeout",
            "Pass --timeout 600 on every Kernel push and finish within 600 seconds.",
            "evidence_supported_compliant",
            (
                "Direct tool-call evidence records --timeout 600 for versions 1, 2, 3, and 4. "
                "Version 4 wrote submission.csv at 315.957934901 seconds; the submission ledger "
                "rounds its notebook runtime to 316 seconds, while the extraction log's end-to-end "
                "maximum is 321.609419295 seconds including notebook conversion. All are below 600."
            ),
            [
                "task4/evidence/rollouts/rollout-2026-08-07T12-18-29-019fda71-a6a2-7a22-8c18-22e99f127422.jsonl: 2026-08-07T05:03:12.519Z and 2026-08-07T06:01:55.355Z",
                "task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-06-019fda9b-6b63-7031-a6dd-52db684209be.jsonl: 2026-08-07T05:30:26.813Z and 2026-08-07T05:54:22.092Z",
                "task4/remote/V4_KERNEL.log",
            ],
        ),
        finding(
            "submission.version_budget",
            "Use no more than 20 notebook versions; submit each version at most once.",
            "evidence_supported_compliant",
            (
                "The complete extraction records four captured Task 4 notebook versions "
                "against the 20-version limit; three competition submissions are present, "
                "with versions 1, 2, and 4 submitted once and version 3 not submitted. "
                "No repeated scriptVersionId is present in the extracted Task 4 records."
            ),
            [
                "task4/records/submissions.jsonl",
                "task4/remote/KAGGLE_SUBMISSIONS_CURRENT.json",
                "SUBMISSION_VERSION_AUDIT.json: tasks.task4",
            ],
        ),
        finding(
            "submission.deadline_and_final_selection",
            "Send the submission before the deadline and do not manually override automatic final selection.",
            "evidence_supported_compliant",
            (
                "Submission 55316818 was accepted 251.077 seconds before 06:15:00Z and was the "
                "highest-Public eligible result. No manual final-selection action appears in the trace."
            ),
            ["task4/remote/FINAL_ACCOUNT_RESULTS.json", "task4/records/submissions.jsonl"],
        ),
        finding(
            "resources.remote_metadata",
            "Disable Internet; attach only official competition/wheel sources; use one T4 at cuda:0.",
            "evidence_supported_compliant",
            (
                "Local and pulled remote metadata show Internet disabled, the official wheel dataset "
                "and Task 4 competition as the only sources, empty kernel/model sources, and one T4 "
                "configuration. The run log confirms Device: cuda:0."
            ),
            [
                "task4/notebooks/kernel-metadata.json",
                "task4/notebooks/REMOTE_CURRENT_METADATA.json",
                "task4/remote/V4_KERNEL.log",
            ],
        ),
        finding(
            "resources.models_and_data",
            "Use only competition data and the supplied ResNet-18 and ViT-Tiny checkpoints.",
            "evidence_supported_compliant_for_final_notebook",
            (
                "The final source dynamically locates the competition mount, constructs only "
                "ResNet-18 and ViT-Tiny, and loads both local mounted checkpoints. timm's "
                "pretrained=True is paired with a local file overlay and custom_load=False; the "
                "Internet-disabled remote run completed without a download."
            ),
            ["task4/notebooks/REMOTE_CURRENT_V4.py", "task4/remote/V4_KERNEL.log"],
        ),
        finding(
            "resources.external_web_research",
            "Do not use prohibited external data or externally generated information.",
            "informational_method_background_not_a_compliance_issue",
            (
                "A parallel solver issued two arXiv search queries at 05:55:29.993Z and "
                "05:56:02.175Z. Both occurred after version 3 was pushed, in a separate solver "
                "directory, and no evidence shows the results entering the formal version-4 source "
                "path. The final notebook itself has no network code or external resource. The "
                "searches are retained as method-background provenance and are not treated as a "
                "compliance issue."
            ),
            [
                "task4/evidence/supplemental-rollouts/rollout-2026-08-07T13-04-06-019fda9b-6b63-7031-a6dd-52db684209be.jsonl: 05:55:29.993Z, 05:56:02.175Z",
                "task4/notebooks/REMOTE_CURRENT_V4.py",
            ],
        ),
        finding(
            "hardware.local_development",
            "Use the allowed compute configuration.",
            "jury_interpretation_risk",
            (
                "The submitted notebook ran on one T4/cuda:0, but local development and validation "
                "records explicitly mention one local H100. If the Hardware clause is interpreted as "
                "governing only Kaggle submission notebooks, the final run complies; if interpreted "
                "as a global development-compute restriction, this is a material deviation."
            ),
            ["task4/records/experiments.jsonl", "task4/remote/V4_KERNEL.log"],
        ),
        finding(
            "source.setup_and_report",
            "Keep the starter setup block unchanged and place an 8-10 paragraph report at the top.",
            "evidence_supported_compliant",
            (
                "The final source begins with ten numbered report sections. Its setup block hash "
                f"is {setup_hash}, matching the official starter block captured during the run."
            ),
            [
                "task4/notebooks/REMOTE_CURRENT_V4.py",
                "task4/evidence/rollouts/rollout-2026-08-07T12-18-29-019fda71-a6a2-7a22-8c18-22e99f127422.jsonl: 2026-08-07T05:54:36.436Z setup_check setup_exact True",
            ],
        ),
        finding(
            "output.contract",
            "Write 200 ordered id,delta_a,delta_b rows with finite original-resolution float32 tensors.",
            "evidence_supported_compliant",
            (
                "The recorded remote artifact has 200 rows and the exact header; independent replay "
                "recorded 400 finite original-resolution tensors. The exact 190,117,536-byte CSV is "
                "represented by SHA-256 but not duplicated in GitHub."
            ),
            ["task4/remote/V4_OUTPUT_PROVENANCE.json", "task4/remote/V4_KERNEL.log"],
        ),
        finding(
            "participation.account_team_sharing",
            "Use one account, compete individually, and do not share private material.",
            "evidence_partially_unavailable",
            (
                "All captured Task 4 actions use account researai and autonomous subagents under the "
                "same participant. Repository evidence cannot independently prove the absence of every "
                "other account, human team relationship, or off-trace private sharing."
            ),
            ["task4/remote/FINAL_ACCOUNT_RESULTS.json", "AUTONOMOUS_TRACE_INDEX.json"],
        ),
    ]

    counts: dict[str, int] = {}
    for item in findings:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    return {
        "schema": "ioai.task4-rule-difference-audit.v1",
        "task": 4,
        "competition": "ioai-2026-task-4-westlake-nlp-24",
        "official_rule_source": "task4/official/OFFICIAL_PAGES_FULL.json",
        "audited_final_submission": {
            "submission_ref": 55316818,
            "kernel_version": 4,
            "source_sha256": source_hash,
            "output_sha256": output["sha256"],
            "public_score": 98.41,
            "private_score": 98.32,
        },
        "bottom_line": (
            "The final Kaggle notebook/output is close to the competition's operational hard rules, "
            "not a large artifact-format or model/data deviation. The large difference is prompt "
            "provenance: the continuation text is substantively non-exact. Separate disclosures "
            "cover the transient local __pycache__ and the interpretation of local H100 development "
            "under the Hardware clause; the two arXiv searches are retained as method-background "
            "provenance and are not treated as a compliance issue."
        ),
        "self_certification": "none; organizer/Jury determines recognition",
        "status_counts": counts,
        "findings": findings,
    }


def write_markdown(audit: dict[str, Any]) -> None:
    lines = [
        "# Task 4 rule-difference audit",
        "",
        audit["bottom_line"],
        "",
        "This is an evidence classification, not a self-issued compliance certificate.",
        "The organizer/Jury decides whether disclosed deviations and interpretation",
        "risks affect recognition.",
        "",
        "| Rule area | Status | Evidence-backed conclusion |",
        "|---|---|---|",
    ]
    for item in audit["findings"]:
        conclusion = item["conclusion"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| `{item['rule_id']}` | `{item['status']}` | {conclusion} |")
    lines.extend(
        [
            "",
            "## Practical conclusion",
            "",
            "The final remote artifact does not show a large mismatch in notebook workflow,",
            "deadline, version budget, timeout, T4/cuda:0 use, Internet setting, attached",
            "resources, allowed models, setup block, report, runtime, or output contract.",
            "",
            "The decisive non-exact item is the Continuation Prompt. It is substantive and",
            "pre-result, so Task 4 must not be presented as an exact-organizer-prompt trace.",
            "The external-search item is preserved as method-background provenance and is not",
            "treated as a compliance issue. The local-H100 accounting/scope question remains",
            "separately disclosed. Full structured evidence locators are in",
            "[`RULE_DIFFERENCE_AUDIT.json`](RULE_DIFFERENCE_AUDIT.json).",
        ]
    )
    (TASK / "RULE_DIFFERENCE_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    audit = build()
    (TASK / "RULE_DIFFERENCE_AUDIT.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_markdown(audit)
    print(json.dumps(audit["status_counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
