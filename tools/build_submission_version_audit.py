#!/usr/bin/env python3
"""Audit notebook-version budgets and repeated submission of one version.

The source is the organizer-requested Kaggle extraction archive.  The audit is
literal and evidence-scoped: it records conflicts with the published wording,
but does not decide whether the organizer grants a post-deadline or platform
exception.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import tarfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SHA256 = "eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c"
SUMMARY_SHA256 = "0ccd29d1e4a8542ddaf7f05a0526dcbb17e1b0975e0cabac46bc925e6985865b"

TASKS = {
    1: ("ioai-2026-task-1-westlake-nlp-24", "notebook_versions", 20),
    2: ("ioai-2026-task-2-westlake-nlp-24", "notebook_versions", 20),
    3: ("ioai-2026-task-3-westlake-nlp-48", "scored_submissions", 15),
    4: ("ioai-2026-task-4-westlake-nlp-24", "notebook_versions", 20),
    5: ("ioai-2026-task-5-westlake-nlp-24", "notebook_versions", 15),
    6: ("ioai-2026-task-6-westlake-nlp-60", "notebook_versions", 20),
}

EXPECTED_ALL_SUBMISSIONS_SHA256 = {
    1: "922375f34f447965c28bf7d7d089427376cac9e00afee2e739360f6275b60c04",
    2: "cd78ff77983ad75afb301ee1bdf7bc79962ff9dc5a7efa91d19110e3dee740b2",
    3: "b1492e3213fad6ae0c77a2a97f02e4e39542f18b9aee950af1349d55cd60588e",
    4: "8afbfb3ad2a6a6fd0711b03e92db38fb6a46fb038ac2a106a4bb4356a9b94038",
    5: "d72861924dd58ad649c70bca45cdcda276253d88a5dcd2a51cb8da402b5b5820",
    6: "220c181eafc7be3db00a8bc1a955c7af351d62e3e73384fb0adfbf941221b50f",
}

VERSION_ONCE_RULE = "A Notebook version may be submitted to the Competition at most once."


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def official_rule_text(task: int) -> str:
    pages = json.loads(
        (ROOT / f"task{task}/official/OFFICIAL_PAGES_FULL.json").read_text(encoding="utf-8")
    )
    rules = next(item["content"] for item in pages if item.get("name") == "rules")
    assert VERSION_ONCE_RULE in rules, task
    return rules


def normalize_utc(value: str) -> str:
    """Render extraction timestamps as unambiguous ISO-8601 UTC strings."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    else:
        parsed = parsed.astimezone(timezone.utc)
    return parsed.isoformat(timespec="microseconds").replace("+00:00", "Z")


def duplicate_groups(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for item in rows:
        version_id = item.get("script_version_id")
        if version_id is not None:
            grouped[int(version_id)].append(item)
    result = []
    for version_id, items in sorted(grouped.items()):
        if len(items) < 2:
            continue
        observations = [
            {
                "submission_ref": item["ref"],
                "submitted_at_utc": normalize_utc(item["submitted_at_utc"]),
                "seconds_before_official_deadline": item["seconds_before_deadline"],
                "before_official_deadline": item["seconds_before_deadline"] >= 0,
            }
            for item in sorted(items, key=lambda value: value["submitted_at_utc"])
        ]
        result.append(
            {
                "script_version_id": version_id,
                "submission_count": len(items),
                "submission_refs": [item["submission_ref"] for item in observations],
                "all_before_official_deadline": all(
                    item["before_official_deadline"] for item in observations
                ),
                "observations": observations,
            }
        )
    return result


def load_archive_records(archive: Path) -> tuple[dict[int, dict[str, Any]], dict[int, str]]:
    records: dict[int, dict[str, Any]] = {}
    paths: dict[int, str] = {}
    with tarfile.open(archive, "r:gz") as bundle:
        members = {
            member.name: member
            for member in bundle.getmembers()
            if member.isfile() and member.name.endswith("/researai/all-submissions.json")
        }
        for task, (competition, _, _) in TASKS.items():
            suffix = f"/{competition}/researai/all-submissions.json"
            matches = [name for name in members if name.endswith(suffix)]
            assert len(matches) == 1, (task, matches)
            name = matches[0]
            extracted = bundle.extractfile(members[name])
            assert extracted is not None
            raw = extracted.read()
            assert sha256_bytes(raw) == EXPECTED_ALL_SUBMISSIONS_SHA256[task], task
            records[task] = json.load(io.BytesIO(raw))
            paths[task] = name
    return records, paths


def build(archive: Path) -> dict[str, Any]:
    assert sha256_file(archive) == ARCHIVE_SHA256
    summary_path = ROOT / "KAGGLE_EXTRACTION_SUMMARY.json"
    assert sha256_file(summary_path) == SUMMARY_SHA256
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary_by_competition = {item["competition"]: item for item in summary["competitions"]}
    final_results = {
        task: json.loads(
            (ROOT / f"task{task}/remote/FINAL_ACCOUNT_RESULTS.json").read_text(encoding="utf-8")
        )["official_final_result"]["submission_refs"]
        for task in TASKS
    }
    source_records, source_paths = load_archive_records(archive)

    tasks: dict[str, Any] = {}
    for task, (competition, budget_kind, limit) in TASKS.items():
        official_rule_text(task)
        rows = source_records[task]["submissions"]
        groups = duplicate_groups(rows)
        extraction = summary_by_competition[competition]
        observed_budget = (
            extraction["versions_captured"]
            if budget_kind == "notebook_versions"
            else extraction["submissions"]
        )
        budget_conflict = observed_budget > limit
        repeated_refs = {
            ref for group in groups for ref in group["submission_refs"]
        }
        final_refs = final_results[task]
        tasks[f"task{task}"] = {
            "competition": competition,
            "official_rule_source": f"task{task}/official/OFFICIAL_PAGES_FULL.json#rules-2.3",
            "official_budget_kind": budget_kind,
            "official_budget_limit": limit,
            "observed_budget_count": observed_budget,
            "observed_budget_source": "KAGGLE_EXTRACTION_SUMMARY.json",
            "budget_literal_status": (
                "known_deviation_under_published_wording"
                if budget_conflict
                else "evidence_supported_account_extraction_scope"
            ),
            "post_deadline_scope_note": (
                "The observed count includes activity captured after the official deadline. "
                "The published limit text does not state a post-deadline exemption; the "
                "organizer decides whether any requested audit/reproduction activity receives one."
                if budget_conflict
                else "No budget excess is visible in the complete extraction summary."
            ),
            "one_submission_per_version_rule": VERSION_ONCE_RULE,
            "submission_record_count": len(rows),
            "submission_status_counts": {
                status: sum(item.get("status") == status for item in rows)
                for status in sorted({item.get("status") for item in rows})
            },
            "known_script_version_id_records": sum(
                item.get("script_version_id") is not None for item in rows
            ),
            "unknown_script_version_id_records": sum(
                item.get("script_version_id") is None for item in rows
            ),
            "unique_known_script_version_ids": len(
                {item["script_version_id"] for item in rows if item.get("script_version_id") is not None}
            ),
            "duplicate_script_version_groups": groups,
            "predeadline_duplicate_script_version_groups": [
                group for group in groups if group["all_before_official_deadline"]
            ],
            "version_reuse_literal_status": (
                "known_deviation_under_published_wording"
                if groups
                else "evidence_supported_account_extraction_scope"
            ),
            "official_final_submission_refs": final_refs,
            "official_final_refs_affected_by_version_reuse": sorted(
                set(final_refs) & repeated_refs
            ),
            "combined_budget_and_reuse_status": (
                "known_deviation_under_published_wording"
                if budget_conflict or groups
                else "evidence_supported_account_extraction_scope"
            ),
            "all_submissions_archive_path": source_paths[task],
            "all_submissions_sha256": EXPECTED_ALL_SUBMISSIONS_SHA256[task],
        }

    return {
        "schema": "ioai.submission-version-audit.v1",
        "purpose": "Literal audit of published submission/version limits and repeated Kaggle scriptVersionId use; not an organizer adjudication.",
        "generated_by": "tools/build_submission_version_audit.py",
        "source_archive": archive.name,
        "source_archive_sha256": ARCHIVE_SHA256,
        "extraction_summary": "KAGGLE_EXTRACTION_SUMMARY.json",
        "extraction_summary_sha256": SUMMARY_SHA256,
        "status_definition": {
            "known_deviation_under_published_wording": "The extracted account record directly conflicts with the literal published requirement. Only the organizer can grant an exception or narrower enforcement scope.",
            "evidence_supported_account_extraction_scope": "No conflict appears in the complete extracted account fields used for this check; this does not prove unobservable off-account facts.",
        },
        "tasks": tasks,
        "overall": {
            "tasks_with_literal_budget_excess": [
                task for task, item in tasks.items()
                if item["budget_literal_status"] == "known_deviation_under_published_wording"
            ],
            "tasks_with_repeated_script_version_submission": [
                task for task, item in tasks.items()
                if item["version_reuse_literal_status"] == "known_deviation_under_published_wording"
            ],
            "strict_all_six_budget_and_version_reuse_claim_supported": False,
        },
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Submission-version audit",
        "",
        "This audit checks two literal published requirements against the complete",
        "organizer-requested Kaggle account extraction: the task budget and the rule",
        "that one Notebook version may be submitted at most once. It records evidence;",
        "it does not decide whether the organizer grants an exception.",
        "",
        "| Task | Published budget | Extracted count | Budget finding | Repeated scriptVersionId groups | Version-reuse finding | Official-final impact |",
        "|---|---:|---:|---|---:|---|---|",
    ]
    for task, item in data["tasks"].items():
        impact = ", ".join(map(str, item["official_final_refs_affected_by_version_reuse"])) or "none"
        lines.append(
            f"| {task} | {item['official_budget_limit']} {item['official_budget_kind']} | "
            f"{item['observed_budget_count']} | **{item['budget_literal_status']}** | "
            f"{len(item['duplicate_script_version_groups'])} | "
            f"**{item['version_reuse_literal_status']}** | {impact} |"
        )
    lines += [
        "",
        "## Repeated version details",
        "",
    ]
    for task, item in data["tasks"].items():
        for group in item["duplicate_script_version_groups"]:
            refs = ", ".join(f"`{ref}`" for ref in group["submission_refs"])
            when = "all before deadline" if group["all_before_official_deadline"] else "includes post-deadline activity"
            lines.append(
                f"- {task}: scriptVersionId `{group['script_version_id']}` was used by {refs} ({when})."
            )
    lines += [
        "",
        "Task 1's tied official-final refs are the same extracted scriptVersionId.",
        "Task 2's repeated version is the formal autonomous v2 pair, while its official",
        "final ref is not in that duplicate group. Task 3's duplicate pair was sent",
        "immediately before the official deadline and is not its selected official final.",
        "",
        "The full records, source hashes, timestamps, and deadline offsets are in",
        "[`SUBMISSION_VERSION_AUDIT.json`](SUBMISSION_VERSION_AUDIT.json).",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--check", action="store_true", help="Compare with tracked outputs instead of writing")
    args = parser.parse_args()
    data = build(args.archive)
    json_text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    md_text = markdown(data)
    outputs = {
        ROOT / "SUBMISSION_VERSION_AUDIT.json": json_text,
        ROOT / "SUBMISSION_VERSION_AUDIT.md": md_text,
    }
    if args.check:
        for path, expected in outputs.items():
            assert path.read_text(encoding="utf-8") == expected, path
    else:
        for path, content in outputs.items():
            path.write_text(content, encoding="utf-8")
    print(json.dumps(data["overall"], sort_keys=True))


if __name__ == "__main__":
    main()
