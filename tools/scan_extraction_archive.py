#!/usr/bin/env python3
"""Read-only heuristic scan of the external Kaggle extraction archive.

This tool deliberately reports names and counts, not archive contents.  It is
scope evidence for an authorized reviewer, not a data-license or secrecy
certificate.  Nested compressed log payloads are not decompressed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tarfile
from collections import Counter
from pathlib import Path
from typing import BinaryIO


PATH_MARKERS = re.compile(
    r"(?i)(^|/)(input|inputs|dataset|datasets|competition|data)(/|$)"
    r"|\.(npy|npz|wav|zip|safetensors|pt|pth|ckpt|bin|onnx)$"
    r"|public_embeddings|vocabulary\.json|field_config|ioai-starter|ioai-field"
)
CONTENT_MARKERS = re.compile(
    rb"(?i)(test_leaderboard|public_embeddings|vocabulary\.json|field_config"
    rb"|/kaggle/input/competitions|\.(?:safetensors|pt|pth|ckpt|bin|onnx)\b)"
)
CHUNK_SIZE = 1024 * 1024
MAX_MARKER_LENGTH = 64
KERNEL_SOURCE_BASENAMES = {"kernel-source.py", "kernel-source.ipynb"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contains_marker(handle: BinaryIO) -> bool:
    carry = b""
    while True:
        chunk = handle.read(CHUNK_SIZE)
        if not chunk:
            return bool(CONTENT_MARKERS.search(carry))
        window = carry + chunk
        if CONTENT_MARKERS.search(window):
            return True
        carry = window[-MAX_MARKER_LENGTH:]


def scan(archive: Path) -> dict[str, object]:
    entries = files = directories = 0
    path_hits: list[str] = []
    content_hits: list[str] = []
    with tarfile.open(archive, "r|gz") as bundle:
        for member in bundle:
            entries += 1
            if member.isdir():
                directories += 1
            elif member.isfile():
                files += 1
                if PATH_MARKERS.search(member.name):
                    path_hits.append(member.name)
                handle = bundle.extractfile(member)
                if handle is not None and contains_marker(handle):
                    content_hits.append(member.name)
    hit_basenames = Counter(Path(name).name for name in content_hits)
    non_kernel_source_hits = [
        name for name in content_hits if Path(name).name not in KERNEL_SOURCE_BASENAMES
    ]
    return {
        "archive": str(archive),
        "archive_size_bytes": archive.stat().st_size,
        "archive_sha256": sha256_file(archive),
        "entry_count": entries,
        "file_count": files,
        "directory_count": directories,
        "data_like_path_matches": len(path_hits),
        "data_like_path_examples": path_hits[:20],
        "content_marker_hit_files": len(content_hits),
        "content_marker_hit_basenames": dict(sorted(hit_basenames.items())),
        "content_marker_non_kernel_source_files": len(non_kernel_source_hits),
        "content_marker_non_kernel_source_examples": non_kernel_source_hits[:20],
        "content_marker_hit_examples": content_hits[:20],
        "method": (
            "Stream-read every regular tar member and search bytes for the "
            "configured markers; nested compressed members are not decompressed."
        ),
        "interpretation": (
            "The basename and non-kernel-source counts show whether marker "
            "hits are confined to kernel source text documenting paths or "
            "filenames; marker hits do not by themselves indicate restricted data."
        ),
        "limitation": (
            "This heuristic does not certify that arbitrary source, CSV, or "
            "compressed-log bytes contain no restricted information."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(scan(args.archive), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
