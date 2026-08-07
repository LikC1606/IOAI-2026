"""Assemble the strict Task 1 organizer-review evidence package."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = Path("/workspace/IOAI/next-task/ioai-2026-task-1-westlake-nlp-24")
PROJECT = RUN / "project"
ROLLOUT = RUN / "codex-home/sessions/2026/08/05/rollout-2026-08-05T17-20-55-019fd139-d180-7171-ac0b-c037e11866eb.jsonl"
CONTROLLER_ROLLOUT = Path("/workspace/.codex/sessions/2026/08/04/rollout-2026-08-04T21-48-47-019fcd08-b264-72b3-93f3-3afaf2cf41af.jsonl")
BOUNDARY = "2026-08-05T10:16:52.222Z"
BOUNDARY_TEXT = "你让他继续优化 找到高分了再提交"
COMPETITION = "ioai-2026-task-1-westlake-nlp-24"

KAGGLE_TOKEN = re.compile(r"KGAT_[A-Za-z0-9_-]+")
API_KEY = re.compile(r"(?<![A-Za-z0-9_-])sk-(?:proj-)?[A-Za-z0-9_]{24,}")
PRIVATE_ENDPOINT = re.compile(
    r"https?://(?:codex\.aiswing\.fun|api\.smilecodex\.space|127\.0\.0\.1:\d+|8\.216\.32\.188(?::\d+)?)",
    re.IGNORECASE,
)
SECRET_KEY = re.compile(
    r"(?i)(api[_ -]?key|api[_ -]?token|access[_ -]?token|authorization|proxy|base[_ -]?url|credential)"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.unlink()
    shutil.copy2(source, target)


def redact(value, key: str = ""):
    if isinstance(value, dict):
        return {
            name: "[REDACTED]" if SECRET_KEY.search(str(name)) else redact(item, str(name))
            for name, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item, key) for item in value]
    if isinstance(value, str):
        value = KAGGLE_TOKEN.sub("[REDACTED_KAGGLE_TOKEN]", value)
        value = API_KEY.sub("[REDACTED_API_KEY]", value)
        value = PRIVATE_ENDPOINT.sub("[REDACTED_PRIVATE_ENDPOINT]", value)
        if SECRET_KEY.search(key):
            return "[REDACTED]"
    return value


def user_message(event: dict) -> str:
    payload = event.get("payload", {})
    if event.get("type") != "response_item" or payload.get("type") != "message":
        return ""
    if payload.get("role") != "user":
        return ""
    return "".join(part.get("text", "") for part in payload.get("content", []))


def build_rollout() -> dict:
    target = ROOT / "evidence/rollouts" / ROLLOUT.name
    execution_target = ROOT / "evidence/submission-execution" / f"{ROLLOUT.stem}-post-boundary.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)
    execution_target.parent.mkdir(parents=True, exist_ok=True)
    kept = execution_kept = 0
    first_timestamp = last_timestamp = None
    execution_first_timestamp = execution_last_timestamp = None
    agents_body = None
    with (
        ROLLOUT.open(encoding="utf-8") as source,
        target.open("w", encoding="utf-8") as output,
        execution_target.open("w", encoding="utf-8") as execution_output,
    ):
        for line in source:
            event = json.loads(line)
            timestamp = str(event.get("timestamp", ""))
            if timestamp and timestamp >= BOUNDARY:
                execution_output.write(json.dumps(redact(event), ensure_ascii=False, separators=(",", ":")) + "\n")
                execution_kept += 1
                execution_first_timestamp = execution_first_timestamp or timestamp
                execution_last_timestamp = timestamp or execution_last_timestamp
                continue
            text = user_message(event)
            if text.startswith("# AGENTS.md instructions for ") and "<INSTRUCTIONS>" in text:
                agents_body = text.split("<INSTRUCTIONS>", 1)[1].split("</INSTRUCTIONS>", 1)[0].strip() + "\n"
            output.write(json.dumps(redact(event), ensure_ascii=False, separators=(",", ":")) + "\n")
            kept += 1
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp or last_timestamp
    if agents_body is None:
        raise RuntimeError("Injected AGENTS.md was not found in the formal rollout")
    (ROOT / "environment/AGENTS-ACTUALLY-INJECTED.md").write_text(agents_body, encoding="utf-8")
    return {
        "filename": target.name,
        "private_original_path": str(ROLLOUT),
        "private_original_sha256": digest(ROLLOUT),
        "redacted_sha256": digest(target),
        "boundary_utc_exclusive": BOUNDARY,
        "kept_events": kept,
        "dropped_events": execution_kept,
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
        "agent_execution_trace": {
            "filename": str(execution_target.relative_to(ROOT)),
            "redacted_sha256": digest(execution_target),
            "kept_events": execution_kept,
            "first_timestamp": execution_first_timestamp,
            "last_timestamp": execution_last_timestamp,
            "classification": "agent-executed-after-supervision-boundary",
        },
    }


def extract_boundary_event() -> dict:
    matches = []
    prefix_digest = hashlib.sha256()
    prefix_bytes = 0
    prefix_lines = 0
    boundary_line_sha256 = None
    with CONTROLLER_ROLLOUT.open("rb") as stream:
        for raw_line in stream:
            event = json.loads(raw_line)
            prefix_digest.update(raw_line)
            prefix_bytes += len(raw_line)
            prefix_lines += 1
            if event.get("timestamp") == BOUNDARY and user_message(event) == BOUNDARY_TEXT:
                matches.append(redact(event))
                boundary_line_sha256 = hashlib.sha256(raw_line).hexdigest()
                break
    if len(matches) != 1:
        raise RuntimeError(f"Expected one supervision boundary event, found {len(matches)}")
    write_json(ROOT / "evidence/SUPERVISION_BOUNDARY_EVENT.json", matches[0])
    return {
        "private_original_path": str(CONTROLLER_ROLLOUT),
        "private_original_prefix_through_boundary_sha256": prefix_digest.hexdigest(),
        "private_original_prefix_bytes": prefix_bytes,
        "private_original_prefix_lines": prefix_lines,
        "private_boundary_line_sha256": boundary_line_sha256,
        "extracted_event_sha256": digest(ROOT / "evidence/SUPERVISION_BOUNDARY_EVENT.json"),
    }


def kaggle_json(arguments: list[str]) -> object:
    result = subprocess.run(arguments, check=True, text=True, capture_output=True)
    return json.loads(result.stdout)


def fetch_remote_evidence() -> dict:
    pages = kaggle_json(
        [
            "kaggle", "competitions", "pages", COMPETITION, "list", COMPETITION,
            "--content", "--format", "json", "--quiet",
        ]
    )
    submissions = kaggle_json(
        ["kaggle", "competitions", "submissions", COMPETITION, "--format", "json", "--quiet"]
    )
    write_json(ROOT / "official/OFFICIAL_PAGES_FULL.json", pages)
    write_json(ROOT / "remote/KAGGLE_SUBMISSIONS_CURRENT.json", submissions)

    with tempfile.TemporaryDirectory(prefix="ioai-task1-evidence-fetch-") as temporary:
        temp = Path(temporary)
        source_dir = temp / "source"
        output_dir = temp / "output"
        subprocess.run(
            ["kaggle", "kernels", "pull", "researai/ioai-task-1-prefix-baseline", "-p", str(source_dir), "-m"],
            check=True,
            text=True,
            capture_output=True,
        )
        subprocess.run(
            ["kaggle", "kernels", "output", "researai/ioai-task-1-prefix-baseline", "-p", str(output_dir)],
            check=True,
            text=True,
            capture_output=True,
        )
        copy(source_dir / "ioai-task-1-prefix-baseline.py", ROOT / "remote/preboundary-baseline-not-scored/source/script.py")
        copy(source_dir / "kernel-metadata.json", ROOT / "remote/preboundary-baseline-not-scored/source/kernel-metadata.json")
        copy(output_dir / "submission.csv", ROOT / "remote/preboundary-baseline-not-scored/output/submission.csv")
        copy(output_dir / "ioai-task-1-prefix-baseline.log", ROOT / "remote/preboundary-baseline-not-scored/output/kernel.log")

    remote_files = {}
    remote_root = ROOT / "remote/preboundary-baseline-not-scored"
    for path in sorted(remote_root.rglob("*")):
        if path.is_file():
            remote_files[str(path.relative_to(ROOT))] = {"sha256": digest(path), "bytes": path.stat().st_size}
    provenance = {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "competition": COMPETITION,
        "kernel": "researai/ioai-task-1-prefix-baseline",
        "facts": {
            "kernel_completed": True,
            "output_generated": True,
            "competition_submission_from_this_kernel_found": False,
            "eligible_scored_submission_claimed": False,
        },
        "files": remote_files,
    }
    write_json(ROOT / "remote/REMOTE_FETCH_PROVENANCE.json", provenance)
    return provenance


def copy_local_evidence() -> None:
    copy(RUN / "session.json", ROOT / "environment/session.json")
    copy(PROJECT / "official/start.md", ROOT / "official/STARTER_PROMPT.md")
    copy(PROJECT / "official/continue.md", ROOT / "official/CONTINUE_PROMPT.md")

    trial = PROJECT / ".deepscientist/competition/trials/trial-605da205"
    attempt = PROJECT / ".deepscientist/competition/worktrees/trial-605da205/.deepscientist/competition/candidate-attempt"
    copy(trial / "candidate.json", ROOT / "records/trial-605da205/candidate.json")
    copy(trial / "result.json", ROOT / "records/trial-605da205/result.json")
    copy(attempt / "attempt-output.json", ROOT / "records/trial-605da205/attempt-output.json")
    copy(attempt / "source-manifest.json", ROOT / "records/trial-605da205/source-manifest.json")
    copy(attempt / "source/candidates/prefix_identity.py", ROOT / "records/trial-605da205/FROZEN_CANDIDATE_SOURCE.py")

    copy(PROJECT / "competition/evaluator.py", ROOT / "records/validation/evaluator.py")
    copy(PROJECT / "competition/task-spec.json", ROOT / "records/validation/task-spec.json")
    copy(PROJECT / "competition/validation/fixture.json", ROOT / "records/validation/fixture.json")
    copy(PROJECT / ".deepscientist/competition/official_submission/authorization.json", ROOT / "records/authorization.json")
    copy(PROJECT / ".deepscientist/competition/official_submission/submissions.json", ROOT / "records/submissions-ledger.json")
    copy(
        PROJECT / ".deepscientist/competition/official_submission/receipts/submission-f2f141cc.prepared.json",
        ROOT / "records/PREPARED_BASELINE_RECEIPT.json",
    )

    submission_source = PROJECT / "official/submission-record-2026-08-05"
    submission_target = ROOT / "submission/agent-executed-55267607"
    submission_target.mkdir(parents=True, exist_ok=True)
    for child in submission_target.iterdir():
        if child.name == "README.md":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    copy(submission_source / "SUBMISSION_RECEIPT.json", submission_target / "SUBMISSION_RECEIPT.json")
    for name in ("script.py", "kernel-metadata.json", "submission.csv", "kaggle-run.log"):
        copy(submission_source / "final" / name, submission_target / "final" / name)
    for name in ("candidate.json", "result.json"):
        copy(
            submission_source / "evaluation/trials/trial-9c1d23c5" / name,
            submission_target / "trial-9c1d23c5" / name,
        )


def write_summary(rollout_info: dict, controller_info: dict) -> None:
    summary = {
        "package_schema": "ioai.organizer-evidence.v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "task": 1,
        "competition": COMPETITION,
        "account_owner": "researai",
        "formal_run": {
            "joined_at_utc": "2026-08-05T09:20:36.326Z",
            "deadline_utc": "2026-08-05T10:30:00.000Z",
            "boundary_utc_exclusive": BOUNDARY,
            "boundary_basis": "first material supervisory instruction received by the controlling session",
            "official_starter_sha256": digest(ROOT / "official/STARTER_PROMPT.md"),
            "official_continue_sha256": digest(ROOT / "official/CONTINUE_PROMPT.md"),
        },
        "positive_claim": {
            "agent_executed_submission": 55267607,
            "agent_executed_public_score": 0.78049,
            "submission_actor": "formal_solver_agent",
            "submission_execution_evidence": rollout_info["agent_execution_trace"]["filename"],
            "official_prompt_only_autonomous_submission": None,
            "official_ranking_eligible": False,
            "best_pre_boundary_local_trial": "trial-605da205",
            "best_pre_boundary_local_score": 0.6827101986420873,
            "candidate_id": "candidate-prefix-identity-b5aad75d324f",
            "remote_baseline_kernel": "researai/ioai-task-1-prefix-baseline",
            "remote_baseline_scored_submission": False,
        },
        "agent_executed_result": {
            "submission_id": 55267607,
            "public_score": 0.78049,
            "submitted_at_utc": "2026-08-05T10:54:51.343Z",
            "autonomy_status": "agent-executed-after-human-supervision",
            "ranking_status": "submitted-after-official-deadline",
        },
        "rollout_provenance": rollout_info,
        "controller_provenance": controller_info,
    }
    write_json(ROOT / "SUMMARY.json", summary)


def main() -> None:
    copy_local_evidence()
    rollout_info = build_rollout()
    controller_info = extract_boundary_event()
    fetch_remote_evidence()
    provenance = {"formal_solver": rollout_info, "supervising_controller": controller_info}
    write_json(ROOT / "ROLLOUT_PROVENANCE.json", provenance)
    write_summary(rollout_info, controller_info)
    print(f"Built evidence package at {ROOT}")


if __name__ == "__main__":
    main()
