# Task 4 Compliance and Reproduction Note

This is a post-run audit. It preserves the historical version 4 source and
separates facts known at submission time from later platform observations. The
full rule-by-rule classification is in `RULE_DIFFERENCE_AUDIT.md/json`.

## Eligible scope

The formal solver used a formatting-modified copy of the organizer Starter
Prompt and a substantive generic runtime resume template rather than the exact
organizer Continuation Prompt. The template contained no live human method,
candidate, target-score, or forced-submission instruction, but it remains a
prompt-text deviation and the final submission is downstream of it. This note
therefore does not claim strict exact-organizer-prompt compliance; see
`../PROMPT_CONFORMANCE_AUDIT.md`. Organizer/Jury recognition is not assumed.
Submission `55316818` was sent at `2026-08-07T06:10:48.923Z`, 251.077 seconds
before the official Kaggle deadline at `06:15:00Z` and 456.594 seconds before
the agent-run deadline at `06:18:25.517Z`. Its extracted scores are Public
`98.41` and Private `98.32`.

## Submission and resource audit

- Private Kaggle Kernel:
  `researai/ioai-2026-task-4-westlake-nlp-24-solution`, version 4.
- Metadata: one `NvidiaTeslaT4`, Internet disabled, competition and official
  wheel sources attached, and no external dataset/model/Kernel source.
- Source: exact current remote version 4 source, using only organizer-provided
  classifiers and `cuda:0`.
- Output: exactly 200 rows, columns `id,delta_a,delta_b`, and 400 finite
  original-resolution tensors.
- Remote runtime: 316 seconds, within the 600-second cap.

Direct trace evidence records `--timeout 600` for all four Kernel pushes. The
formal and supplemental trace set now includes 12 files: the seven added
parallel-solver traces account for versions 2/3 and their contribution to the
version-4 comparison path.

Three limitations remain disclosed. A pre-push folder listing contains a local
`submission/__pycache__/script.cpython-311.pyc`, so the instruction that the
local folder hold exactly two files was not literally satisfied at every
moment, although the pulled remote source is the declared script/metadata
artifact. A parallel solver issued two arXiv search queries after version 3 had
already been pushed; there is no evidence their results entered the final v4
source, and they are retained as provenance rather than treated as a method or
external-information violation. Finally, local development records mention one
H100; the final submitted notebook itself used the required one T4 at `cuda:0`.
The separate local-development accounting question remains disclosed below.

Artifact hashes:

| Artifact | SHA-256 |
|---|---|
| `notebooks/REMOTE_CURRENT_V4.py` | `d467bc5a1e7c83ae7da780aaf01fb6ac001fd326e514495cae3a9279b7b6301b` |
| `remote/V4_KERNEL.log` | `bc7cfde1adb09278a12c9d623422d07039f3bdac3afe22c5041ea5653832b535` |
| Historical `submission.csv` | `bdb202711d6494bc94c331d549b0fa7956aa1d9eb585c247ae0dfce723f76542` |

The 190,117,536-byte CSV is not duplicated in this compact package. Its hash,
schema, row count, runtime, Kernel/version, and retrieval path are recorded in
`remote/V4_OUTPUT_PROVENANCE.json`. The organizer-requested Kaggle extraction
archive also contains the exact output bytes and matching source/output hashes;
the extraction metadata reports an empty `matched_version_confidence`, so the
archive strengthens byte identity without silently converting linked-ref
matching into an exact-version claim. The compact-package omission is a
disclosed storage choice, not evidence that the output was locally uploaded.

## Historical report supplement

The source contains the requested ten report paragraphs. It records the first
two Public scores and estimates the refined T4 runtime because version 4's own
result was not yet known. Post-run evidence establishes version 4 Public LB
`98.41` and actual remote runtime about 316 seconds. Those later facts are
documented here rather than inserted into the immutable source report. No
Private score is inferred from the local checks or Public LB; the `98.32` value
comes directly from the later Kaggle extraction recorded in
`remote/FINAL_ACCOUNT_RESULTS.json`.

## Reproduce

From `task4/`:

```bash
sha256sum -c MANIFEST.sha256
cmp notebooks/script.py notebooks/REMOTE_CURRENT_V4.py
python -m py_compile notebooks/REMOTE_CURRENT_V4.py
kaggle kernels output researai/ioai-2026-task-4-westlake-nlp-24-solution -p reproduced-v4/
sha256sum reproduced-v4/submission.csv
```

The final digest should be the historical CSV hash above while version 4
remains the Kernel's retrievable current output. A new push would create a new
version and is unnecessary for artifact verification.

## Compute-accounting limit

The historical report records 161 seconds for the complete refined local H100
body, but other local diagnostics overlap and are not exhaustively attributable.
The 1,120.720551504 seconds of Kaggle T4 runtime are complete for versions v1-v4;
the total local development GPU time and all GPU USD remain unavailable. Root
cost files therefore separate observed remote runtime from incomplete local
development accounting.
