# Task 5 Compliance and Reproduction Note

This is a post-run audit. It does not modify the historical v6 source or claim
that a later reconstruction was downloaded from Kaggle.

## Eligible scope

The formal run lasted from `2026-08-07T07:04:20.561Z` to
`09:04:20.519Z`. The main solver received the organizer Starter Prompt and no
Continuation Prompt or custom method instruction. Controller status questions
were not solver inputs. Versions 1–6 were sent before the official Kaggle
deadline at `09:00:00Z`; version 7 at `09:02:01.927Z` was before the agent-run
deadline but 121.927 seconds after the official deadline. Submission v6
`55320296` is the official-deadline best at Public `95.39`, Private `96.06`.

## Submission and resource audit

The complete account extraction captures 7 notebook versions against the
published limit of 15 and finds no repeated `scriptVersionId` among the seven
Task 5 submissions. The per-task binding and source records are in
[`../SUBMISSION_VERSION_AUDIT.json`](../SUBMISSION_VERSION_AUDIT.json) and
`SUMMARY.json`.

- Private Kernel `researai/ioai-2026-ghost-of-the-machine-solution`, version 6,
  submitted through the notebook-only workflow.
- Metadata: one `NvidiaTeslaT4`, Internet disabled, competition and official
  wheel sources attached, and no external model/Kernel source.
- The source loads only the organizer-supplied local `bge-base-en-v1.5`, uses
  official labels for fine-tuning/refit, and exposes only `cuda:0`.
- Remote output: exactly 760 rows with columns `id,boundary_char_index`.
- Remote runtime: 289.3 seconds; Tesla T4 on `cuda:0`; 5.00 GB peak VRAM,
  within the 600-second cap.

Artifact hashes:

| Artifact | SHA-256 |
|---|---|
| Preserved v6 source `notebooks/BEST_V6_SOURCE.py` | `dd310ac9a5aff845f0298f4fb23374b8ddbc225bbe8f6b439d80d9bbc443585c` |
| `remote/v6/submission.csv` | `176f45d8e5a46b9c634efb620a8373ab4eb69e0655f71445604e45491bc31375` |
| `remote/v6/ioai-2026-ghost-of-the-machine-solution.log` | `a70033f828289659427a5ffefbe6a85b29c20247f74f2d1f1e6d63358e5549c0` |

Kaggle now returns HTTP 403 for the historical v6 source pull. The source is
therefore classified as the source preserved from the formal run, not an
independently redownloaded remote source. `V6_SOURCE_PROVENANCE.json` binds its
hash to the v6 push and the pre-v7 preservation events in the bounded rollout.
The exact v6 remote log, output, submission ID, and score provide independent
remote-result evidence.

## Historical report supplement

The source contains ten report paragraphs. It correctly says v6 Public LB was
pending and gives a local H100 runtime plus conservative T4 projection. Later
platform evidence establishes Public LB `95.39` and actual remote runtime about
289.3 seconds. Those later facts are disclosed here rather than backfilled into
the historical source. The Private scores cited in this audit come directly
from the later Kaggle extraction, not from inference.

## Reproduce

From `task5/`:

```bash
sha256sum -c MANIFEST.sha256
python -m py_compile notebooks/BEST_V6_SOURCE.py
stage=$(mktemp -d)
cp notebooks/BEST_V6_SOURCE.py "$stage/script.py"
cp notebooks/kernel-metadata.json "$stage/kernel-metadata.json"
kaggle kernels push -p "$stage" --timeout 600
```

The push command is for authorized reproduction only. It creates a new Kernel
version, may produce slightly different predictions because GPU training is not
fully bitwise deterministic, and does not recreate the historical version
number or score. The archived remote v6 output remains the exact scored output.

## External-method and compute limits

At `07:19:46Z`, before the final v6 selection, the Agent searched
sentence-level machine-text detection, stylometry and authorship change-point
literature. The route already had local evidence, and the sources and
applicability were recorded in `records/RESEARCH.md`. No external data, labels,
features, model weights, or runtime API entered the notebook. This is retained
as method-background provenance and is not treated as a competition compliance
issue.

The historical report records 24.8 seconds on one local H100 for the selected
all-label path, and the trace records additional H100 diagnostics, including
concurrent work on both local H100s. The complete local development GPU total
cannot be reconstructed from non-overlapping records. `AUTONOMOUS_COSTS.json`
therefore reports the known selected-path observation separately and leaves the
exhaustive local runtime and USD cost unavailable.
