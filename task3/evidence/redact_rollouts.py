"""Create pre-supervision, credential-redacted rollout evidence.

This is an audit helper, not part of the submitted solution.  It preserves JSONL
events whose event timestamp is at or before the declared external-supervision
boundary, then redacts credentials and secret transport settings recursively.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

BOUNDARY = "2026-08-06T05:46:19.450Z"
ROOT = Path(__file__).resolve().parent
RAW = Path(
    "/workspace/IOAI/ioai2-competition-runs-task3-formal-deadline-20260806T123442CST/"
    "ioai-2026-task-3-westlake-nlp-48/codex-home/sessions/2026/08/06"
)
OUT = ROOT / "rollouts"

SECRET_PATTERNS = (
    re.compile(r"KGAT_[A-Za-z0-9_-]+"),
    # Real OpenAI keys are long opaque values; do not mistake the competition
    # slug's short `sk-3` segment for a credential.
    re.compile(r"(?<![A-Za-z0-9_-])sk-(?:proj-)?[A-Za-z0-9_]{24,}"),
    re.compile(r"(?i)(api[_ -]?key|token|authorization|proxy|base[_ -]?url)"),
)
PRIVATE_ENDPOINT = re.compile(
    r"https?://(?:codex\.aiswing\.fun|api\.smilecodex\.space|127\.0\.0\.1:\d+)",
    re.IGNORECASE,
)

def redact(value, key=""):
    if isinstance(value, dict):
        result = {}
        for k, v in value.items():
            if SECRET_PATTERNS[2].search(str(k)):
                result[k] = "[REDACTED]"
            else:
                result[k] = redact(v, str(k))
        return result
    if isinstance(value, list):
        return [redact(v, key) for v in value]
    if isinstance(value, str):
        result = value
        result = SECRET_PATTERNS[0].sub("[REDACTED_KAGGLE_TOKEN]", result)
        result = SECRET_PATTERNS[1].sub("[REDACTED_API_KEY]", result)
        result = PRIVATE_ENDPOINT.sub("[REDACTED_PRIVATE_ENDPOINT]", result)
        if SECRET_PATTERNS[2].search(key):
            return "[REDACTED]"
        return result
    return value

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    boundary = BOUNDARY
    for source in sorted(RAW.glob("*.jsonl")):
        target = OUT / source.name
        kept = dropped = 0
        with source.open(encoding="utf-8") as inp, target.open("w", encoding="utf-8") as out:
            for line in inp:
                obj = json.loads(line)
                ts = str(obj.get("timestamp", ""))
                if ts and ts > boundary:
                    dropped += 1
                    continue
                out.write(json.dumps(redact(obj), ensure_ascii=False, separators=(",", ":")) + "\n")
                kept += 1
        if kept == 0:
            target.unlink()
        print(f"{source.name}: kept={kept} dropped={dropped} -> {target}")

if __name__ == "__main__":
    main()
