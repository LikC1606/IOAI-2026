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

The separate [`SUBMISSION_VERSION_AUDIT.md`](SUBMISSION_VERSION_AUDIT.md) checks
the published budget and the rule that one Notebook version may be submitted at
most once. It records repeated `scriptVersionId` values in Tasks 1–3; Task 1's
two official tied refs share one version. Those account-history findings are not
silently removed from this score reconciliation.

| Task | Official deadline | Official final result | Canonical no-live-human rollout | Chronological last account submission |
|---|---|---|---|---|
| 1 | 2026-08-05 10:50 UTC | `55267333` / `55267368`: Public 0.77751, Private 0.80474 | `55277782`: Public 0.74121; Private not recorded; post-deadline, non-ranking | `55300144`: Public 0.81854, Private 0.82775, post-deadline |
| 2 | 2026-08-05 07:35 UTC | `55261432`: Public 0.63583, Private 0.62500 | `55277682`: Public 0.675; Private not recorded; post-deadline, non-ranking | `55280319`: Public 0.65888, Private 0.66166, post-deadline |
| 3 | 2026-08-06 06:30 UTC | `55289569` / `55289823`: Public 58.51666, Private 51.61666 | Same tied result | `55306794`: Public 41.16666, Private 41.15000 |
| 4 | 2026-08-07 06:15 UTC | `55316818`: Public 98.41000, Private 98.32000 | Same | Same |
| 5 | 2026-08-07 09:00 UTC | `55320296`: Public 95.39000, Private 96.06000 | Same | `55320652`: Public 94.17000, Private 96.31000, 121.927 s late |
| 6 | 2026-08-08 18:30 UTC | `55357080`: Public 75.01540, Private 73.36234 | Same | `55358739`: Public 76.41428, Private 73.74666, post-deadline |

## Scope notes

- The complete raw formal Task 1 and Task 2 sessions were subsequently located
  in private local archives after a school-server restart. Their human-influenced
  suffixes are intentionally unpublished. Bounded pre-boundary formal prefixes
  remain as supplemental evidence, while their canonical no-live-human traces
  are later fresh reproductions run with the same configured solver/system,
  official competition bundle, and organizer constraints. Neither later
  reproduction substitutes for the recovered private formal session; see
  `FORMAL_PREFIX_AUDIT.md/json` and `ORIGINAL_SESSION_RECOVERY.md/json`.
- Task 1's separately preserved Agent-executed submission `55267607` scored
  Public 0.78049 / Private 0.76808 but was submitted 291.343 seconds after the
  official Kaggle deadline and after human intervention. It is not the official
  final result or part of the organizer trace selection.
- Task 1's earlier formal run had no scored pre-boundary submission. Its
  later 120-minute reproduction (`55277782`) is the canonical published
  no-live-human rollout, but it started after the official deadline and is not
  ranking-eligible.
- Task 2's earlier formal run produced `55260695` before its conservative
  supervision boundary. Per the requested two-hour reproduction selection, the
  canonical published rollout is the later fresh run (`55277682`); both are
  separate from the official account result `55261432`.
- Task 3's official-deadline best Private was 55.48333 on `55290027`, but the
  competition selected by Public score, and that submission was not autonomous.
- Task 5's v7 and Task 6's later numerical maxima cannot replace their official
  results because they were submitted after the official deadlines.

Machine-readable counts, timestamps, source hashes, maxima, and scope labels
are in `task1/remote/FINAL_ACCOUNT_RESULTS.json` through
`task6/remote/FINAL_ACCOUNT_RESULTS.json`. The full extraction archive and its
Google Drive delivery metadata are in
[`KAGGLE_EXTRACTION_DELIVERY.json`](KAGGLE_EXTRACTION_DELIVERY.json).
