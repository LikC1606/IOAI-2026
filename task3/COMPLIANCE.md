# Competition Compliance Audit

## Submission and execution contract

- Notebook-only: all eight entries were submitted from Kernel versions using the
  organizer's `kaggle competitions submit ... -k ... -v ... -f submission.csv`
  flow. The stored CSVs are remote Kernel outputs, not local prediction uploads.
- Notebook metadata: private, CPU-only, Internet disabled, blank machine shape,
  only the competition source attached, and empty dataset/kernel/model sources.
- Output: exactly two columns and two rows with identical payloads.
- Grader API: every source defines `load_public_data()` and
  `PotatoPlayer(words, embeddings)` with `new_game()` and `respond(message)`.
- Local contract: v1-v8 all execute successfully against the supplied data.
- Size: every decoded source is about 16-23 KB, far below the 512 KB limit.
- Runtime: local full public runs complete in roughly 0.2-2.6 seconds after
  process startup, far below the 600-second CPU budget.

## Data, model, and dependency audit

The submitted sources import only the Python standard library and NumPy. Runtime
inputs are limited to `vocabulary.json`, `public_embeddings.npy`, and, for local
self-scoring or the competition-provided prior experiment, `test_public.json`.
These are all organizer-supplied Competition Data. The sources do not download,
call external APIs, load external embeddings/models/checkpoints, or attach any
external dataset/model/Kernel.

The methods are algorithmic sequential-search policies, which the rules expressly
permit. They do not access or reconstruct grader-side private embeddings or hidden
word lists. Verdicts received through the official `respond()` protocol are used
only as intended by the task. v6 uses earlier officially returned comparison
histories causally within the same graded round; it does not inspect grader files.

External web research by the development agent is not embedded in or called by
the submitted program and did not introduce an external runtime resource. The
exact submitted source and attached-source metadata are preserved for inspection.
If the organizers interpret the development-time external-research restriction
more broadly than the runtime/data/model restrictions stated on the official
page, they should make the final determination; this package does not conceal the
rollout evidence.

## Reproducibility evidence

`evidence/verify_artifacts.py` checks CSV schema, identical payloads, decoded
source identity, execution, contract output, and self-score for all eight
versions. The resulting `evidence/LOCAL_REPRODUCTION.json` reports `all_ok: true`.
`notebooks/vN` contains each exact `script.py` plus the actual legal metadata.
Remote logs, outputs, submission IDs, scores, and integrity hashes are included.

## Autonomy evidence

The official Starter Prompt is exact after slug substitution. The startup
`AGENTS.md` actually seen by the solver is preserved separately from later edits.
That injected payload ends mid-sentence; the export is nevertheless byte-exact
to the rollout input and is not silently completed from the later project file.
The main and three child rollouts are truncated at the conservative first
supervision boundary and recursively redacted. Mechanical inspection shows no
Continuation Prompt or user method instruction in the solver input before that
boundary. See `AUTONOMY_BOUNDARY.md` and `evidence/ROLLOUT_PROVENANCE.md`.

## Disclosed limitations

The historical header reports do not meet the requested 8-10 paragraph length;
most have six logical paragraphs (v1 has five). Several versions were submitted
before their own LB score was known and therefore cannot report that score in
their immutable source. v8 includes the actual 58.51666 LB but omits the requested
win-turn distribution and currently reproduces at 96.62 rather than the 98.63
stated in its report. These are documentation deficiencies, not silently repaired
artifacts. See `REPORT_COMPLIANCE.md`.

The official Report page says every solution “should carry” the report and says
the report “carries no score.” The submission page calls it a report requirement.
This package does not decide whether the Jury treats the format deviations as
material; it provides the exact sources and a separate truthful audit.

Only v1-v8 are claimed. Post-boundary results and external-embedding experiments
are explicitly excluded. In particular, v13/v14 used prohibited external
embeddings and must never be presented as compliant official submissions.
