# IOAI 2026 Evidence Records

Organizer-review materials for IOAI 2026 Tasks 1-6. Start with
[`ORGANIZER_SUBMISSION.md`](ORGANIZER_SUBMISSION.md), which maps every requested
deliverable to its exact evidence path and machine-verifiable status.

| Task | Competition | Official final Public LB | Status |
|---|---|---:|---|
| [Task 1](task1/) | `ioai-2026-task-1-westlake-nlp-24` | 0.77751 | Private 0.80474; tied refs `55267333` / `55267368` |
| [Task 2](task2/) | `ioai-2026-task-2-westlake-nlp-24` | 0.63583 | Private 0.62500; submission `55261432` |
| [Task 3](task3/) ([trace + costs](task3/EXECUTION_AND_COSTS.md)) | `ioai-2026-task-3-westlake-nlp-48` | 58.51666 | Private 51.61666; two eligible submissions tie exactly |
| [Task 4](task4/) | `ioai-2026-task-4-westlake-nlp-24` | 98.41 | Private 98.32; submission `55316818` |
| [Task 5](task5/) | `ioai-2026-task-5-westlake-nlp-24` | 95.39 | Private 96.06; submission `55320296`; v7 was late |
| [Task 6](task6/) | `ioai-2026-task-6-westlake-nlp-60` | 75.01540 | Private 73.36234; submission `55357080` |

No final leaderboard placement is claimed. The final-score rows apply the
preserved automatic highest-Public-before-deadline rule to the extracted account
records; extracted Private scores remain historical submission fields, not
placement claims. For Tasks 1–6,
[`FINAL_SUBMISSION_RESULTS.md`](FINAL_SUBMISSION_RESULTS.md) separates the
official result, autonomous scope, chronological last account submission, and
all-account numerical maxima.

The organizer-facing, human-intervention-free execution package starts at
[AUTONOMOUS_TRACE_MATERIAL.md](AUTONOMOUS_TRACE_MATERIAL.md), with the
machine-readable [AUTONOMOUS_TRACE_INDEX.json](AUTONOMOUS_TRACE_INDEX.json) and
[AUTONOMOUS_COSTS.json](AUTONOMOUS_COSTS.json), verified by
[AUTONOMOUS_MATERIAL_MANIFEST.sha256](AUTONOMOUS_MATERIAL_MANIFEST.sha256). It retains startup/organizer
prompts, Agent outputs, worker assignments, tool calls, and tool outputs, but
causally excludes every live human intervention prompt and all later events.

Each directory contains its own README, official prompts/pages, environment
record, solver evidence, solution artifacts, remote records, and summary.
Tasks 1-5 maintain task-specific SHA-256 manifests. Task 6 includes the bounded
main trace, two pre-boundary worker traces, and compact v1-v3 remote logs; raw
`codex-home` databases, post-intervention traces, model artifacts, and competition inputs are excluded. Task-specific
limitations are disclosed in the corresponding README, `COMPLIANCE.md`,
`EXCLUSIONS.md`, or boundary documents.

The published trace overview is [EXECUTION_TRACES.md](EXECUTION_TRACES.md),
with machine-readable [EXECUTION_TRACE_INDEX.json](EXECUTION_TRACE_INDEX.json)
and [EXECUTION_TRACE_INDEX.md](EXECUTION_TRACE_INDEX.md). Token counters,
provider/model attribution, API-cost limitations, and GPU runtime accounting are
in [COSTS.json](COSTS.json). Both trace indexes now use the same
human-intervention-free selection. USD API/GPU amounts are left `null` where no
applicable rate or invoice exists.

For Task 1, the canonical solution selection is the later two-hour rollout
prefix through `task_complete`; the complete raw trace remains under
[REPRODUCTION_TRACE_MATERIAL.md](REPRODUCTION_TRACE_MATERIAL.md). Task 2 uses
its full later trace. Neither contains a live human method/target prompt, and
both scores remain post-deadline and non-ranking. The original Task 1 and Task 2 run records were
unavailable after a school-server restart; these are later fresh reproductions
using the same configured solver/system, official competition bundle, and
organizer constraints, not the lost original run records.

Task 4's full rule classification and corrected 12-trace solver inventory are
in [task4/RULE_DIFFERENCE_AUDIT.md](task4/RULE_DIFFERENCE_AUDIT.md).

The complete 496,870,419-byte Kaggle extraction archive is delivered through
the verified Google Drive record in
[`KAGGLE_EXTRACTION_DELIVERY.json`](KAGGLE_EXTRACTION_DELIVERY.json); its
six-competition summary is
[`KAGGLE_EXTRACTION_SUMMARY.json`](KAGGLE_EXTRACTION_SUMMARY.json).

These files are evidence for organizer review, not a self-issued compliance
certificate. The organizer or Jury remains the final authority.

Run the repository verifier from the root:

```bash
python verify_repository.py
```

## Data handling

Task 3 retains the organizer's competition archive and extracted inputs for
authorized reproducibility review. Those files total about 25 MB and are not
owned or licensed for unrestricted redistribution. While they remain in
`task3/input/competition/`, this repository must remain private and access must
be limited to people authorized under the competition rules. See
`task3/DATA_PROVENANCE.md` for exact hashes and public-release instructions.

The other task packages do not duplicate bulk competition datasets or model
checkpoints. Before making any part of this repository public, remove all
restricted competition data, regenerate the affected manifest, and re-run the
repository verifier.
