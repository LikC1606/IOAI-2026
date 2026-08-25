# Final Kaggle account result reconciliation — Tasks 1–6

This page reconciles the organizer-requested Kaggle extraction for account
`researai` with the human-intervention-free trace claims. Under the preserved
competition rule, Kaggle automatically chooses the highest-Public submission
sent before the official deadline. That rule determines the official final
result below.

The extraction does not expose a `selected-for-final` flag. Task 1 and Task 3
each have two deadline-eligible submissions tied with identical Public and
Private scores, so their exact selected submission ID cannot be reduced beyond
the tied refs. “Final submission” is not used for the chronological last
submission, an all-account numerical maximum, a late submission, or a narrower
autonomous-trace result.

| Task | Official deadline | Official final result | Human-intervention-free result | Chronological last account submission |
|---|---|---|---|---|
| 1 | 2026-08-05 10:50 UTC | `55267333` / `55267368`: Public 0.77751, Private 0.80474 | No scored pre-boundary submission | `55300144`: Public 0.81854, Private 0.82775, post-deadline |
| 2 | 2026-08-05 07:35 UTC | `55261432`: Public 0.63583, Private 0.62500 | `55260695`: Public 0.55416, Private 0.54833 | `55280319`: Public 0.65888, Private 0.66166, post-deadline |
| 3 | 2026-08-06 06:30 UTC | `55289569` / `55289823`: Public 58.51666, Private 51.61666 | Same tied result | `55306794`: Public 41.16666, Private 41.15000 |
| 4 | 2026-08-07 06:15 UTC | `55316818`: Public 98.41000, Private 98.32000 | Same | Same |
| 5 | 2026-08-07 09:00 UTC | `55320296`: Public 95.39000, Private 96.06000 | Same | `55320652`: Public 94.17000, Private 96.31000, 121.927 s late |
| 6 | 2026-08-08 18:30 UTC | `55357080`: Public 75.01540, Private 73.36234 | Same | `55358739`: Public 76.41428, Private 73.74666, post-deadline |

## Scope notes

- Task 1's separately preserved Agent-executed submission `55267607` scored
  Public 0.78049 / Private 0.76808 but was submitted 291.343 seconds after the
  official Kaggle deadline and after human intervention. It is not the official
  final result or part of the organizer trace selection.
- Task 2's deadline-eligible official final `55261432` occurred after the
  conservative human-intervention-free trace boundary. The trace result remains
  `55260695`; the official account result remains `55261432`.
- Task 3's official-deadline best Private was 55.48333 on `55290027`, but the
  competition selected by Public score, and that submission was not autonomous.
- Task 5's v7 and Task 6's later numerical maxima cannot replace their official
  results because they were submitted after the official deadlines.

Machine-readable counts, timestamps, source hashes, maxima, and scope labels
are in `task1/remote/FINAL_ACCOUNT_RESULTS.json` through
`task6/remote/FINAL_ACCOUNT_RESULTS.json`. The full extraction archive and its
Google Drive delivery metadata are in
[`KAGGLE_EXTRACTION_DELIVERY.json`](KAGGLE_EXTRACTION_DELIVERY.json).
