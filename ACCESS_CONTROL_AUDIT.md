# Access-control audit

This page separates two delivery channels that have different access
properties. It is an evidence record, not an organizer authorization decision.

## Repository

The current GitHub repository is `PRIVATE`, verified on 2026-08-26 with the
authenticated GitHub CLI. The restricted organizer-provided Task 3 inputs are
under [`task3/input/competition/`](task3/input/competition/); their provenance
and handling rules are in [`task3/DATA_PROVENANCE.md`](task3/DATA_PROVENANCE.md).

## Google Drive extraction

The requested Kaggle extraction is delivered separately as
`ioai-kaggle-fetch-researai-20260813.tar.gz` (496,870,419 bytes; SHA-256
`eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c`). The
historical live delivery check recorded HTTP 200, matching content length, and
byte-range support. The Drive link does not inherit GitHub's Private setting.

The local archive contains 1,401 entries (1,151 files and 250 directories). A path-name scan found no entries
matching the known competition-data patterns (`input`, `dataset`, `.npy`,
`.wav`, `.zip`, `public_embeddings`, `vocabulary.json`, `field_config`, and
similar). All file paths classify as extraction metadata, Kernel source/log,
notebook output, or submission records. This is useful scope evidence, but it
is not a proof that arbitrary
compressed contents contain no restricted bytes; an authorized reviewer makes
the final sharing decision.

As an additional heuristic, every regular member was stream-scanned for
competition-data markers such as `test_leaderboard`, `public_embeddings`,
`vocabulary.json`, `field_config`, checkpoint extensions, and Kaggle input
paths. The scan found 98 source files containing such words as code-level path
or filename references, but no data-file or checkpoint member. This is still
only a heuristic content check and does not replace an authorized review of
the archive before redistribution.

The scan is reproducible without extracting the archive:

```bash
python3 tools/scan_extraction_archive.py \
  --archive /path/to/ioai-kaggle-fetch-researai-20260813.tar.gz
```

It prints only counts, member names, and hashes; it does not write or publish
archive contents.

See the machine-readable details in
[`ACCESS_CONTROL_AUDIT.json`](ACCESS_CONTROL_AUDIT.json) and the delivery
record in [`KAGGLE_EXTRACTION_DELIVERY.json`](KAGGLE_EXTRACTION_DELIVERY.json).
