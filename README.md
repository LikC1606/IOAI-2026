# IOAI 2026 Evidence Records

Organizer-review materials for IOAI 2026 Tasks 1-5, preserved as five
independent task directories.

| Task | Competition | Recorded result | Status |
|---|---|---:|---|
| [Task 1](task1/) | `ioai-2026-task-1-westlake-nlp-24` | 0.78049 | Agent-executed; supervised continuation and late-submission status disclosed |
| [Task 2](task2/) | `ioai-2026-task-2-westlake-nlp-24` | 0.55416 | Best submission before conservative autonomy boundary |
| [Task 3](task3/) | `ioai-2026-task-3-westlake-nlp-48` | 58.51666 | Best submission before conservative autonomy boundary |
| [Task 4](task4/) | `ioai-2026-task-4-westlake-nlp-24` | 98.41 | Submitted before the run deadline |
| [Task 5](task5/) | `ioai-2026-task-5-westlake-nlp-24` | 95.39 | Best submission before the run deadline |

Each directory contains its own README, official prompts/pages, environment
record, solver evidence, solution artifacts, remote records, summary, and
SHA-256 manifest. Task-specific limitations are disclosed in the corresponding
README and `EXCLUSIONS.md` or boundary documents.

These files are evidence for organizer review, not a self-issued compliance
certificate. The organizer or Jury remains the final authority.

Run the repository verifier from the root:

```bash
python verify_repository.py
```

Competition data and model checkpoints are not duplicated except where an
existing evidence record already contains a small organizer-owned input needed
for reproducibility.
