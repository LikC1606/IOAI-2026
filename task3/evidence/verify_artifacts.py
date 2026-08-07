"""Verify exact remote payloads and locally execute submitted v1-v8 sources."""
from __future__ import annotations

import argparse
import base64
import ast
import csv
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "input" / "competition"

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def executable_outside_player(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    tree.body = [
        node for node in tree.body
        if not (isinstance(node, ast.ClassDef) and node.name == "PotatoPlayer")
    ]
    return ast.dump(tree, include_attributes=False)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="replace evidence/LOCAL_REPRODUCTION.json with this run's result",
    )
    args = parser.parse_args()
    results = []
    all_ok = True
    starter_outside_player = executable_outside_player(DATA / "ioai-starter.py")
    for version in range(1, 9):
        source_path = ROOT / "solutions" / f"v{version}.py"
        csv_path = ROOT / "remote" / f"v{version}" / "submission.csv"
        source = source_path.read_bytes()
        with csv_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        ids = [row.get("id") for row in rows]
        payloads = [row.get("program_b64", "") for row in rows]
        decoded = base64.b64decode(payloads[0], validate=True) if payloads else b""
        csv_ok = (
            ids == ["leaderboard-a", "leaderboard-b"]
            and len(payloads) == 2
            and payloads[0] == payloads[1]
            and decoded == source
        )
        env = os.environ.copy()
        env["POTATO_DATA_DIR"] = str(DATA)
        env["PYTHONPYCACHEPREFIX"] = "/tmp/ioai-verification-pycache"
        started = time.monotonic()
        proc = subprocess.run(
            [sys.executable, str(source_path)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=600,
        )
        elapsed = time.monotonic() - started
        local_ok = proc.returncode == 0 and "contract OK" in proc.stdout and "self-score" in proc.stdout
        starter_preserved = executable_outside_player(source_path) == starter_outside_player
        result = {
            "version": version,
            "source_sha256": sha256(source),
            "csv_sha256": sha256(csv_path.read_bytes()),
            "csv_contract_ok": csv_ok,
            "decoded_source_matches": decoded == source,
            "local_returncode": proc.returncode,
            "local_contract_ok": local_ok,
            "starter_executable_outside_player_preserved": starter_preserved,
            "elapsed_seconds": round(elapsed, 3),
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
        results.append(result)
        all_ok &= csv_ok and local_ok and starter_preserved
    output = {
        "python": sys.version,
        "data_directory": str(DATA),
        "all_ok": all_ok,
        "results": results,
    }
    if args.write_report:
        (ROOT / "evidence" / "LOCAL_REPRODUCTION.json").write_text(
            json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0 if all_ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
