# Reproduction Guide

## Verify the archived artifacts locally

Use Python 3 with NumPy. The captured local environment was Python 3.11.11 and
NumPy 1.26.4. From this package directory run:

```bash
sha256sum -c MANIFEST.sha256
PYTHONPYCACHEPREFIX=/tmp/ioai-evidence-pycache python -m py_compile \
  solutions/v1.py solutions/v2.py solutions/v3.py \
  solutions/v4.py solutions/v5.py solutions/v6.py solutions/v7.py solutions/v8.py
python evidence/verify_artifacts.py
```

`verify_artifacts.py` performs, for each v1-v8:

1. parse the downloaded remote `submission.csv`;
2. verify the exact IDs and identical payloads;
3. base64-decode the source and compare it byte-for-byte with `solutions/vN.py`;
4. execute that source with `POTATO_DATA_DIR=input/competition`; and
5. require the official `contract OK` and `self-score` outputs.

The verifier prints the current result without modifying the evidence package.
Pass `--write-report` only when deliberately refreshing
`evidence/LOCAL_REPRODUCTION.json`; doing so also requires regenerating the
package manifests.

Expected scores from the current mechanical run are preserved in
`evidence/LOCAL_REPRODUCTION.json`: v1 92.58, v2 99.20, v3 99.05, v4 98.63,
v5 90.72, v6 99.05, v7 98.95, and v8 96.62. The verification result is
`all_ok: true`. These public scores are contract/sanity checks, not LB predictors.

## Reproduce the Notebook output

Each `notebooks/vN` directory contains exactly the historical `script.py` and the
legal `kernel-metadata.json`. The metadata points to the original private Kernel
ID and attaches only the competition source. To reproduce a version on an
authorized Kaggle account, authenticate the CLI outside this package, then run
the organizer's workflow, for example for v8:

```bash
kaggle kernels push -p notebooks/v8/
kaggle kernels status researai/ioai-2026-task-3-westlake-nlp-48-solution
kaggle kernels output researai/ioai-2026-task-3-westlake-nlp-48-solution -p reproduced-v8/
```

Pushing now creates a new Kernel version; it cannot recreate the historical
version number. The resulting `submission.csv` payload should still decode to
the exact `notebooks/v8/script.py`, assuming the organizer data remains available.
Do not edit the archived source or metadata before comparing hashes.

The historical scored-submit form was:

```bash
kaggle competitions submit ioai-2026-task-3-westlake-nlp-48 \
  -k researai/ioai-2026-task-3-westlake-nlp-48-solution \
  -v 8 \
  -f submission.csv \
  -m "v4 likelihood without practice sampling prior"
```

`-f submission.csv` names the remote completed Notebook output; it is not a local
file upload. This command is shown for provenance. Do not resend it after the
competition or against another account/version and expect the historical result.

## Reproduce the autonomy evidence

The shareable rollout copies already stop at the declared boundary. To recreate
them from the private originals at their recorded paths, run:

```bash
python evidence/redact_rollouts.py
```

Then compare the resulting hashes with `evidence/ROLLOUT_PROVENANCE.md` or the
package manifest. The helper removes every event after
`2026-08-06T05:46:19.450Z` and redacts credentials/private endpoints recursively.
The originals are intentionally not included in the shareable package.
