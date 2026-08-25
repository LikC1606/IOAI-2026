"""Verify Task 1 evidence integrity, provenance, boundaries, and claims."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = "2026-08-05T10:16:52.222Z"
START_HASH = "cf6b223cb3d385fb2214c86cdd89cbf914f800d80af5ad5b642b61738e2cf2fb"
CONTINUE_HASH = "7b62aefca0a65c403671db3e1283e4fa9584506476e2e0d5bc21e4be8d303a14"
FROZEN_SOURCE_HASH = "b5aad75d324f118245f7358b4174b5ab7bab286e70b260ef80efa461c4713248"
REMOTE_SOURCE_HASH = "27448633c4e184771ceb1f49a68172918df463968a3a3b6f4b25f6abe09364f3"
REMOTE_CSV_HASH = "6447cb3b97cf7a0801c803d2bbf45397929fef75e2f25d241a4abee82aa9d090"
REMOTE_LOG_HASH = "ea88b665a45f78b00a89edea56969b55f8da6158c4622ee5b3fa9f8d66829302"
PRIVATE_ROLLOUT_HASH = "caeff9bb37bef475044391ca35ba834a3aaf144278b66b50adffbc023127e3d6"
CONTROLLER_PREFIX_HASH = "94789e2c1652f951f51d1d8891f57deeec0a33af9144293f1eceb0b21ea4ddf1"
CONTROLLER_BOUNDARY_LINE_HASH = "bd61e0bea2da1ca9492e483ac895c4c5492c7646a9bd6757c5c957c5728126d9"
SECRET_PATTERNS = {
    "kaggle_token": re.compile(r"KGAT_[A-Za-z0-9_-]{20,}"),
    "api_key": re.compile(r"(?<![A-Za-z0-9_-])sk-(?:proj-)?[A-Za-z0-9_]{24,}"),
    "private_endpoint": re.compile(
        r"https?://(?:codex\.aiswing\.fun|api\.smilecodex\.space|127\.0\.0\.1:\d+|8\.216\.32\.188(?::\d+)?)",
        re.IGNORECASE,
    ),
}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def rollout_user_messages(path: Path, window: str = "pre") -> list[tuple[str, str]]:
    messages = []
    for line in path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        timestamp = str(event.get("timestamp", ""))
        if window == "pre":
            assert not timestamp or timestamp < BOUNDARY, (path, timestamp)
        elif window == "post":
            assert not timestamp or timestamp >= BOUNDARY, (path, timestamp)
        else:
            raise ValueError(window)
        payload = event.get("payload", {})
        if event.get("type") == "response_item" and payload.get("type") == "message" and payload.get("role") == "user":
            messages.append((timestamp, "".join(part.get("text", "") for part in payload.get("content", []))))
    return messages


def visible_strings(value, key: str = ""):
    if key == "encrypted_content":
        return
    if isinstance(value, dict):
        for name, item in value.items():
            yield from visible_strings(item, str(name))
    elif isinstance(value, list):
        for item in value:
            yield from visible_strings(item, key)
    elif isinstance(value, str):
        yield value


def scan_secrets() -> dict:
    findings = []
    suffixes = {".md", ".json", ".jsonl", ".py", ".toml", ".csv", ".log", ".txt"}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if path.name in {"MANIFEST.sha256", "VERIFY_REPORT.json"}:
            continue
        try:
            if path.suffix.lower() == ".jsonl":
                objects = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
                texts = [text for obj in objects for text in visible_strings(obj)]
            elif path.suffix.lower() == ".json":
                texts = list(visible_strings(load_json(path)))
            else:
                texts = [path.read_text(encoding="utf-8")]
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        for name, pattern in SECRET_PATTERNS.items():
            if any(pattern.search(text) for text in texts):
                findings.append({"path": str(path.relative_to(ROOT)), "pattern": name})
    assert not findings, findings
    return {"plaintext_secret_findings": 0}


def check_csv() -> dict:
    path = ROOT / "remote/preboundary-baseline-not-scored/output/submission.csv"
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == ["filename", "prediction"]
        rows = list(reader)
    assert len(rows) == 200
    assert len({row["filename"] for row in rows}) == 200
    lengths = []
    for row in rows:
        prediction = json.loads(row["prediction"])
        assert isinstance(prediction, list)
        assert all(isinstance(value, int) and not isinstance(value, bool) for value in prediction)
        assert sorted(prediction) == list(range(len(prediction)))
        lengths.append(len(prediction))
    return {"rows": 200, "all_genuine_permutations": True, "min_length": min(lengths), "max_length": max(lengths)}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-write-report",
        action="store_true",
        help="verify without replacing VERIFY_REPORT.json (for aggregate read-only audits)",
    )
    args = parser.parse_args()
    report = {"checks": {}}

    for path in ROOT.rglob("*.json"):
        load_json(path)
    for path in ROOT.rglob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            json.loads(line)
    report["checks"]["json"] = "valid"

    assert sha256(ROOT / "official/STARTER_PROMPT.md") == START_HASH
    assert sha256(ROOT / "official/CONTINUE_PROMPT.md") == CONTINUE_HASH
    pages = load_json(ROOT / "official/OFFICIAL_PAGES_FULL.json")
    page_map = {page["name"]: page["content"] for page in pages}
    starter_blocks = re.findall(r"```\n(.*?)```", page_map["Starter Prompt"], flags=re.DOTALL)
    continue_blocks = re.findall(r"```\n(.*?)```", page_map["Continuation Prompt"], flags=re.DOTALL)
    starter_template = next(block for block in starter_blocks if block.startswith("Solve the Kaggle competition"))
    continue_template = next(block for block in continue_blocks if block.startswith("Continue solving the Kaggle competition"))
    competition = "ioai-2026-task-1-westlake-nlp-24"
    assert starter_template.replace("<COMPETITION-SLUG>", competition) == (ROOT / "official/STARTER_PROMPT.md").read_text(encoding="utf-8")
    assert continue_template.replace("<COMPETITION-SLUG>", competition) == (ROOT / "official/CONTINUE_PROMPT.md").read_text(encoding="utf-8")
    report["checks"]["official_prompts"] = {"starter_sha256": START_HASH, "continue_sha256": CONTINUE_HASH}

    session = load_json(ROOT / "environment/session.json")
    assert session["competitionId"] == "ioai-2026-task-1-westlake-nlp-24"
    assert session["deadlineUtc"] == "2026-08-05T10:30:00.000Z"
    assert session["registeredKaggleOwner"] == "researai"
    assert session["initialPromptSha256"] == START_HASH
    assert session["continuationPromptSha256"] == CONTINUE_HASH

    rollout = next((ROOT / "evidence/rollouts").glob("*.jsonl"))
    messages = rollout_user_messages(rollout)
    assert len(messages) == 2, messages
    assert messages[0][0] == "2026-08-05T09:20:55.908Z"
    assert messages[0][1].startswith("# AGENTS.md instructions for ") and "<INSTRUCTIONS>" in messages[0][1]
    body = messages[0][1].split("<INSTRUCTIONS>", 1)[1].split("</INSTRUCTIONS>", 1)[0].strip() + "\n"
    assert body == (ROOT / "environment/AGENTS-ACTUALLY-INJECTED.md").read_text(encoding="utf-8")
    assert messages[1] == ("2026-08-05T09:20:55.988Z", (ROOT / "official/STARTER_PROMPT.md").read_text(encoding="utf-8"))
    provenance = load_json(ROOT / "ROLLOUT_PROVENANCE.json")
    assert provenance["formal_solver"]["private_original_sha256"] == PRIVATE_ROLLOUT_HASH
    assert provenance["formal_solver"]["redacted_sha256"] == sha256(rollout)
    assert provenance["formal_solver"]["boundary_utc_exclusive"] == BOUNDARY
    assert provenance["supervising_controller"]["private_original_prefix_through_boundary_sha256"] == CONTROLLER_PREFIX_HASH
    assert provenance["supervising_controller"]["private_boundary_line_sha256"] == CONTROLLER_BOUNDARY_LINE_HASH
    report["checks"]["rollout"] = {"user_inputs": 2, "all_events_pre_boundary": True, "private_original_sha256": PRIVATE_ROLLOUT_HASH}

    excluded = provenance["formal_solver"]["excluded_post_boundary_suffix"]
    assert excluded["content_in_repository"] is False
    assert excluded["redacted_sha256"] == "390d1fa9399fe42bfd31412659af9156a8e98542713ad2b6371ee51efefe870b"
    assert not (ROOT / "evidence/submission-execution").exists()
    report["checks"]["excluded_post_boundary_suffix"] = {
        "content_in_repository": False,
        "redacted_sha256": excluded["redacted_sha256"],
    }

    boundary = load_json(ROOT / "evidence/SUPERVISION_BOUNDARY_EVENT.json")
    assert boundary["timestamp"] == BOUNDARY
    assert boundary["role"] == "user"
    assert boundary["content_in_repository"] is False
    assert "content" not in boundary and "payload" not in boundary
    report["checks"]["boundary"] = {"exclusive_utc": BOUNDARY, "hash_only": True}

    source = ROOT / "records/trial-605da205/FROZEN_CANDIDATE_SOURCE.py"
    result = load_json(ROOT / "records/trial-605da205/result.json")
    candidate = load_json(ROOT / "records/trial-605da205/candidate.json")
    attempt_output = load_json(ROOT / "records/trial-605da205/attempt-output.json")
    source_manifest = load_json(ROOT / "records/trial-605da205/source-manifest.json")
    assert sha256(source) == FROZEN_SOURCE_HASH
    assert result["trial_id"] == "trial-605da205" and result["valid"] is True
    assert result["score"] == 0.6827101986420873 and result["finished_at"] < BOUNDARY
    assert candidate["trial"]["trial_ref"] == "candidate-prefix-identity-b5aad75d324f"
    assert attempt_output["cases"][0]["candidate"]["score"] == result["score"]
    source_entry = next(item for item in source_manifest["sources"] if item["path"] == "candidates/prefix_identity.py")
    assert source_entry["sha256"] == FROZEN_SOURCE_HASH
    report["checks"]["local_trial"] = {"trial": "trial-605da205", "score": result["score"], "source_sha256": FROZEN_SOURCE_HASH}

    prepared = load_json(ROOT / "records/PREPARED_BASELINE_RECEIPT.json")
    ledger = load_json(ROOT / "records/submissions-ledger.json")
    assert prepared["payload"]["trial_id"] == "trial-605da205"
    assert prepared["prepared_at"] < BOUNDARY and prepared["status"] == "send_reserved"
    assert ledger["attempts"] == []
    report["checks"]["formal_submission_ledger"] = {"sent_attempts": 0, "prepared_only": True}

    assert sha256(ROOT / "remote/preboundary-baseline-not-scored/source/script.py") == REMOTE_SOURCE_HASH
    assert sha256(ROOT / "remote/preboundary-baseline-not-scored/output/submission.csv") == REMOTE_CSV_HASH
    assert sha256(ROOT / "remote/preboundary-baseline-not-scored/output/kernel.log") == REMOTE_LOG_HASH
    metadata = load_json(ROOT / "remote/preboundary-baseline-not-scored/source/kernel-metadata.json")
    assert metadata["id"] == "researai/ioai-task-1-prefix-baseline"
    assert metadata["enable_internet"] is False and metadata["enable_gpu"] is False
    report["checks"]["remote_unscored_baseline"] = {
        "source_sha256": REMOTE_SOURCE_HASH,
        "csv_sha256": REMOTE_CSV_HASH,
        "log_sha256": REMOTE_LOG_HASH,
        "csv": check_csv(),
    }

    summary = load_json(ROOT / "SUMMARY.json")
    assert summary["positive_claim"]["agent_executed_submission"] == 55267607
    assert summary["positive_claim"]["agent_executed_public_score"] == 0.78049
    assert summary["positive_claim"]["submission_actor"] == "formal_solver_agent"
    assert summary["positive_claim"]["official_prompt_only_autonomous_submission"] is None
    assert summary["positive_claim"]["official_ranking_eligible"] is False
    assert summary["positive_claim"]["best_pre_boundary_local_score"] == 0.6827101986420873
    assert summary["agent_executed_result"]["submission_id"] == 55267607
    assert summary["agent_executed_result"]["public_score"] == 0.78049
    assert summary["agent_executed_result"]["submitted_at_utc"] > summary["formal_run"]["official_competition_deadline_utc"]
    assert summary["official_final_submission_refs"] == [55267333, 55267368]
    assert summary["official_final_public_score"] == 0.77751
    assert summary["official_final_private_score"] == 0.80474

    submissions = load_json(ROOT / "remote/KAGGLE_SUBMISSIONS_CURRENT.json")
    excluded_remote = next(item for item in submissions if item["ref"] == 55267607)
    assert excluded_remote["publicScore"] == "0.78049"
    assert excluded_remote["date"] > "2026-08-05T10:30:00"
    submitted = ROOT / "submission/agent-executed-55267607"
    receipt = load_json(submitted / "SUBMISSION_RECEIPT.json")
    assert receipt["submission_id"] == 55267607 and receipt["public_score"] == 0.78049
    assert receipt["submitted_script_sha256"] == "81d89f00f1c68d70e39fc069086419f2409e9ee531459de25f09c621e518652f"
    assert sha256(submitted / "final/script.py") == "81d89f00f1c68d70e39fc069086419f2409e9ee531459de25f09c621e518652f"
    assert sha256(submitted / "final/submission.csv") == "f997dea01312701ffe9fae0094539634a92b5c8835a31437a51ab8aeb40d23a6"
    assert sha256(submitted / "final/kaggle-run.log") == "370cf90f0777675bf678c52a371d748fc3246018db281b55df8f1def6d52e40c"
    submitted_trial = load_json(submitted / "trial-9c1d23c5/result.json")
    assert submitted_trial["score"] == 0.785577
    report["checks"]["agent_executed_result"] = {"submission": 55267607, "score": 0.78049, "local_trial": "trial-9c1d23c5"}

    python_files = list(ROOT.rglob("*.py"))
    with tempfile.TemporaryDirectory(prefix="ioai-task1-evidence-pycache-") as pycache:
        compile_result = subprocess.run(
            [sys.executable, "-m", "py_compile", *map(str, python_files)],
            text=True,
            capture_output=True,
            env={**os.environ, "PYTHONPYCACHEPREFIX": pycache},
        )
    assert compile_result.returncode == 0, compile_result.stderr
    report["checks"]["python_compile"] = len(python_files)
    report["checks"]["secrets"] = scan_secrets()
    report["all_ok"] = True
    if not args.no_write_report:
        (ROOT / "VERIFY_REPORT.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
