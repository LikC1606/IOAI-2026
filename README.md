# IOAI 2026 Evidence Records

Organizer-review materials for IOAI 2026 Tasks 1-5, preserved as five
independent task directories.

| Task | Competition | Recorded Public LB | Status |
|---|---|---:|---|
| [Task 1](task1/) | `ioai-2026-task-1-westlake-nlp-24` | 0.78049 | Agent-executed; supervised continuation and late-submission status disclosed |
| [Task 2](task2/) | `ioai-2026-task-2-westlake-nlp-24` | 0.55416 | Best submission before conservative autonomy boundary |
| [Task 3](task3/) | `ioai-2026-task-3-westlake-nlp-48` | 58.51666 | Best submission before conservative autonomy boundary |
| [Task 4](task4/) | `ioai-2026-task-4-westlake-nlp-24` | 98.41 | Submitted before the run deadline |
| [Task 5](task5/) | `ioai-2026-task-5-westlake-nlp-24` | 95.39 | Best submission before the run deadline |

No Private/final leaderboard score is claimed for any task in this package.

Each directory contains its own README, official prompts/pages, environment
record, solver evidence, solution artifacts, remote records, summary, and
SHA-256 manifest. Task-specific limitations are disclosed in the corresponding
README, `COMPLIANCE.md`, `EXCLUSIONS.md`, or boundary documents.

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
