# IOAI 2026 Evidence Records

Organizer-review materials for IOAI 2026 Tasks 1-6, preserved as six
independent task directories.

| Task | Competition | Recorded Public LB | Status |
|---|---|---:|---|
| [Task 1](task1/) | `ioai-2026-task-1-westlake-nlp-24` | 0.78049 | Agent-executed; supervised continuation and late-submission status disclosed |
| [Task 2](task2/) | `ioai-2026-task-2-westlake-nlp-24` | 0.55416 | Best submission before conservative autonomy boundary |
| [Task 3](task3/) | `ioai-2026-task-3-westlake-nlp-48` | 58.51666 | Best submission before conservative autonomy boundary |
| [Task 4](task4/) | `ioai-2026-task-4-westlake-nlp-24` | 98.41 | Submitted before the run deadline |
| [Task 5](task5/) | `ioai-2026-task-5-westlake-nlp-24` | 95.39 | Best submission before the run deadline |
| [Task 6](task6/) | `ioai-2026-task-6-westlake-nlp-60` | 75.01540 | In-run incumbent; target 86.5 not reached before deadline |

No final leaderboard placement is claimed. Task 6's private score is shown only
as a historical Kaggle submission field recovered by the later extraction; it is
not presented as a final-board or ranking claim.

Each directory contains its own README, official prompts/pages, environment
record, solver evidence, solution artifacts, remote records, and summary.
Tasks 1-5 retain their original SHA-256 manifests. Task 6 additionally includes
the redacted five-trace set and compact v1-v3 remote logs; raw `codex-home`
databases, model artifacts, and competition inputs are excluded. Task-specific
limitations are disclosed in the corresponding README, `COMPLIANCE.md`,
`EXCLUSIONS.md`, or boundary documents.

The cross-task observable execution record is [EXECUTION_TRACES.md](EXECUTION_TRACES.md),
with machine-readable [EXECUTION_TRACE_INDEX.json](EXECUTION_TRACE_INDEX.json)
and [EXECUTION_TRACE_INDEX.md](EXECUTION_TRACE_INDEX.md). Token counters,
provider/model attribution, API-cost limitations, and GPU runtime accounting are
in [COSTS.json](COSTS.json). USD API/GPU amounts are left `null` where no
applicable rate or invoice exists.

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
