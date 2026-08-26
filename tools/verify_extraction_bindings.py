#!/usr/bin/env python3
"""Verify hashes for archive members cited by extraction provenance records.

The Kaggle extraction archive is intentionally external to this compact
repository.  This read-only checker lets an authorized reviewer verify the
candidate source/output/log bytes after downloading the archive from Drive.
It never promotes a kernel-linked candidate to an exact-version claim: the
confidence fields from the provenance records are carried into the report.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ARCHIVE_SHA256 = "eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c"
EXPECTED_ARCHIVE_SIZE = 496870419


def sha256_stream(stream: Any) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    while True:
        block = stream.read(1024 * 1024)
        if not block:
            break
        digest.update(block)
        size += len(block)
    return digest.hexdigest(), size


def sha256_file(path: Path) -> str:
    with path.open("rb") as stream:
        return sha256_stream(stream)[0]


def validate_metadata(name: str, metadata: dict[str, Any], expected: dict[str, Any]) -> None:
    """Check internal metadata claims against the separately cited hashes."""
    if metadata.get("source_sha256") != expected["metadata_source_sha256"]:
        raise ValueError(f"metadata source hash mismatch: {name}")
    output = metadata.get("outputs", {}).get("submission.csv", {})
    if output.get("sha256") != expected["metadata_output_sha256"]:
        raise ValueError(f"metadata output hash mismatch: {name}")
    if output.get("reused_from_disk") is not False or metadata.get("produced_output_file") is not True:
        raise ValueError(f"metadata output provenance flags mismatch: {name}")
    observed_runtime = metadata.get("runtime", {}).get("observed_runtime_s")
    if observed_runtime != expected["metadata_runtime_seconds"]:
        raise ValueError(f"metadata runtime mismatch: {name}")
    if float(observed_runtime) > float(expected["metadata_cap_seconds"]):
        raise ValueError(f"metadata runtime exceeds cap: {name}")
    matched = set(metadata.get("matched_submissions", []))
    if not matched.intersection(expected["metadata_expected_refs"]):
        raise ValueError(f"metadata has no linked expected submission ref: {name}")


def expected_members() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for task in (1, 2):
        provenance = json.loads(
            (ROOT / f"task{task}/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json").read_text(
                encoding="utf-8"
            )
        )
        candidate = provenance["kernel_linked_candidate"]
        expected_refs = provenance.get("official_submission_refs")
        if expected_refs is None:
            expected_refs = [provenance["official_submission_ref"]]
        records.extend(
            [
                {
                    "task": task,
                    "role": "source",
                    "path": candidate["archive_source_path"],
                    "sha256": candidate["source_sha256"],
                },
                {
                    "task": task,
                    "role": "output",
                    "path": candidate["archive_output_path"],
                    "sha256": candidate["output_sha256"],
                },
                {
                    "task": task,
                    "role": "run_log_gzip",
                    "path": candidate["archive_log_path"],
                    "sha256": candidate["log_gzip_sha256"],
                },
                {
                    "task": task,
                    "role": "metadata",
                    "path": candidate["archive_metadata_path"],
                    "sha256": None,
                    "metadata_source_sha256": candidate["source_sha256"],
                    "metadata_output_sha256": candidate["output_sha256"],
                    "metadata_runtime_seconds": candidate["observed_runtime_seconds"],
                    "metadata_cap_seconds": 600 if task == 1 else 300,
                    "metadata_expected_refs": expected_refs,
                },
            ]
        )

    provenance = json.loads(
        (ROOT / "task4/remote/V4_OUTPUT_PROVENANCE.json").read_text(encoding="utf-8")
    )
    archive = provenance["extraction_archive"]
    records.extend(
        [
            {
                "task": 4,
                "role": "source",
                "path": archive["archive_source_path"],
                "sha256": archive["archive_source_sha256"],
                "size_bytes": archive["archive_source_size_bytes"],
            },
            {
                "task": 4,
                "role": "output",
                "path": archive["archive_output_path"],
                "sha256": archive["archive_output_sha256"],
                "size_bytes": archive["archive_output_size_bytes"],
            },
            {
                "task": 4,
                "role": "metadata",
                "path": archive["archive_metadata_path"],
                "sha256": archive["archive_metadata_sha256"],
                "size_bytes": archive["archive_metadata_size_bytes"],
                "metadata_source_sha256": archive["archive_source_sha256"],
                "metadata_output_sha256": archive["archive_output_sha256"],
                "metadata_runtime_seconds": archive["archive_metadata_observation"]["observed_runtime_seconds"],
                "metadata_cap_seconds": 600,
                "metadata_expected_refs": [55316818],
            },
            {
                "task": 4,
                "role": "run_log_gzip",
                "path": archive["archive_log_path"],
                "sha256": archive["archive_log_gzip_sha256"],
                "size_bytes": archive["archive_log_gzip_size_bytes"],
            },
        ]
    )
    return records


def verify(archive: Path) -> dict[str, Any]:
    delivery = json.loads(
        (ROOT / "KAGGLE_EXTRACTION_DELIVERY.json").read_text(encoding="utf-8")
    )
    delivery_archive = delivery["archive"]
    if delivery_archive["size_bytes"] != EXPECTED_ARCHIVE_SIZE:
        raise ValueError("delivery record archive size disagrees with checker")
    if delivery_archive["sha256"] != EXPECTED_ARCHIVE_SHA256:
        raise ValueError("delivery record archive SHA-256 disagrees with checker")
    if archive.stat().st_size != EXPECTED_ARCHIVE_SIZE:
        raise ValueError(f"archive size mismatch: {archive.stat().st_size}")
    archive_sha = sha256_file(archive)
    if archive_sha != EXPECTED_ARCHIVE_SHA256:
        raise ValueError(f"archive SHA-256 mismatch: {archive_sha}")

    records = expected_members()
    by_path = {item["path"]: item for item in records}
    if len(by_path) != len(records):
        raise ValueError("duplicate expected archive member path")
    observed: dict[str, dict[str, Any]] = {}
    with tarfile.open(archive, "r|gz") as bundle:
        for member in bundle:
            expected = by_path.get(member.name)
            if expected is None:
                continue
            if not member.isfile():
                raise ValueError(f"expected archive member is not a file: {member.name}")
            stream = bundle.extractfile(member)
            if stream is None:
                raise ValueError(f"cannot read archive member: {member.name}")
            if expected["role"] == "metadata":
                stream_data = stream.read()
                digest = hashlib.sha256(stream_data).hexdigest()
                size = len(stream_data)
            else:
                digest, size = sha256_stream(stream)
            result = {
                "task": expected["task"],
                "role": expected["role"],
                "path": member.name,
                "size_bytes": size,
                "sha256": digest,
                "expected_sha256": expected["sha256"],
            }
            if "size_bytes" in expected:
                result["expected_size_bytes"] = expected["size_bytes"]
                if size != expected["size_bytes"]:
                    raise ValueError(f"size mismatch: {member.name}")
            if expected["sha256"] is not None and digest != expected["sha256"]:
                raise ValueError(f"SHA-256 mismatch: {member.name}")
            if expected["role"] == "metadata" and expected.get("metadata_source_sha256"):
                metadata = json.loads(stream_data.decode("utf-8"))
                validate_metadata(member.name, metadata, expected)
            observed[member.name] = result

    missing = sorted(set(by_path) - set(observed))
    if missing:
        raise ValueError(f"missing archive members: {missing}")
    return {
        "schema": "ioai.extraction-bindings-verification.v1",
        "archive": {
            "path": str(archive),
            "size_bytes": archive.stat().st_size,
            "sha256": archive_sha,
        },
        "checked_members": list(observed.values()),
        "checked_count": len(observed),
        "exact_version_confidence": {
            "task1": "kernel_linked_candidate_not_byte_confirmed_exact_version",
            "task2": "kernel_linked_candidate_not_byte_confirmed_exact_version",
            "task4": "source_output_bytes_match_archive_provenance; linked-ref exact-version confidence remains as recorded in provenance",
        },
        "all_ok": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.archive), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
