# Final Kaggle account result reconciliation — Tasks 3–6

This page reconciles the organizer-requested Kaggle extraction for account
`researai` with the human-intervention-free trace claims. Under the preserved
competition rule, Kaggle automatically chooses the highest-Public submission
sent before the official deadline. That rule determines the official final
score below. The extraction does not expose a `selected-for-final` flag, so Task
3's exact selected submission ID cannot be reduced beyond its two tied eligible
submissions; both have the same Public and Private scores.

“Final submission” is not used for the chronological last submission, the
all-account maximum Private score, or a late submission. Those scopes are
reported separately so post-deadline account activity cannot overwrite the
official result.

| Task | Official deadline | Official final result | Chronological last account submission | All-account numerical best |
|---|---|---|---|---|
| 3 | 2026-08-06 06:30 UTC | `55289569` / `55289823`: Public 58.51666, Private 51.61666 | `55306794`: Public 41.16666, Private 41.15000 | Public 58.51666; Private 55.48333 on `55290027` (post-autonomy, pre-deadline) |
| 4 | 2026-08-07 06:15 UTC | `55316818`: Public 98.41000, Private 98.32000 | same | same |
| 5 | 2026-08-07 09:00 UTC | `55320296`: Public 95.39000, Private 96.06000 | `55320652`: Public 94.17000, Private 96.31000, 121.927 s late | Public best `55320296`; Private best `55320652` (late) |
| 6 | 2026-08-08 18:30 UTC | `55357080`: Public 75.01540, Private 73.36234 | `55358739`: Public 76.41428, Private 73.74666, post-deadline | `55358739`, post-deadline and non-autonomous |

For Tasks 3–6, the official final result is also the best autonomous Public
result. Machine-readable details, counts, timestamps, provenance hashes, and
boundary classifications are in each task's `remote/FINAL_ACCOUNT_RESULTS.json`.
