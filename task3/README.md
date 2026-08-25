# IOAI 2026 Task 3 — Official-Prompt Autonomous Verification Package

This package preserves the complete defensible portion of the formal run for
`ioai-2026-task-3-westlake-nlp-48`: the organizer Starter Prompt, the instructions
actually injected at startup, competition data and official-page snapshot,
pre-supervision main/worker rollouts, autonomous research artifacts, exact remote
notebook outputs, decoded submitted sources, Kaggle submission records, and local
reproduction results. It is intentionally broader than a single v4 source file.

The autonomy claim stops at **2026-08-06 13:46:19.450 CST**
(`2026-08-06T05:46:19.450Z`), when the first non-read-only supervisory message
asked to modify the continuation and make the running agent reread `AGENTS.md`.
Progress inspection before that time did not inject anything into the solver.
Nothing at or after the boundary is used to claim an autonomous score.
The document-edit/reread instruction itself is therefore classified as a rule
violation for the autonomous claim, rather than as part of the allowed startup.

The eight fully scored pre-boundary submissions are v1-v8. The highest verified
Public Leaderboard score is **58.51666** and the corresponding extracted Private
score is **51.61666**, reached independently by v4 and v8.
Submission IDs are 55289569 and 55289823. v8 removes the practice-centroid prior
while preserving the v4 likelihood/acquisition mechanism, so the tie is useful
ablation evidence.

The later Kaggle extraction found 27 account submissions in total. This does not
change the autonomous claim. Chronologically, the account's last submission is
`55306794` (Public `41.16666`, Private `41.15000`); the highest Private score
among all account submissions is `55.48333` on `55290027`, submitted 67.763
seconds after the autonomy boundary but before the official competition
deadline. Exact autonomous, official-deadline, all-account-best, and latest
account scopes are separated in `remote/FINAL_ACCOUNT_RESULTS.json`.

Start with these documents:

- `AUTONOMY_BOUNDARY.md`: exact inclusion boundary and input audit.
- `SUBMISSION_TIMELINE.md`: all autonomous remote submissions and scores.
- `COMPLIANCE.md`: rules-to-evidence audit and candid limitations.
- `REPORT_COMPLIANCE.md`: audit of the historical source-header reports.
- `SUPPLEMENTARY_TECHNICAL_REPORT.md`: nine-paragraph explanation of v8 with
  reproduced win-turn statistics and the corrected local score.
- `REPRODUCE.md`: exact local and Kaggle notebook reproduction procedure.
- `DATA_PROVENANCE.md`: organizer-data hashes, access restrictions, and
  public-release handling.
- `EXCLUSIONS.md`: the exact Task 3 evidence-scope boundary.
- `evidence/LOCAL_REPRODUCTION.json`: machine-readable v1-v8 verification.
- `MANIFEST.sha256`: integrity hashes for the package.

`solutions/v1.py` through `solutions/v8.py` were decoded from the corresponding
remote `submission.csv` files. They are immutable historical sources, not
reconstructed or polished versions. `notebooks/v1` through `notebooks/v8` pair
each exact source with the actual legal Kernel metadata for straightforward
reproduction.

The report header in every historical source is shorter than the organizer's
requested 8-10 paragraphs, and v8's header reports a 98.63 local score whereas
the exact v8 artifact currently reproduces at 96.62. These documentation issues
do not change the exact payload, executable contract, or Kaggle LB evidence, but
they are disclosed rather than silently repaired. A clearly labeled post-run
explanation is provided in `SUPPLEMENTARY_TECHNICAL_REPORT.md`; it is not
represented as part of the historical submission. The official page states
that the report carries no score and uses “should carry”; the jury decides
whether the format deviation matters.

The `evidence/rollouts` files are timestamp-truncated and credential-redacted
copies. Their private originals remain at the paths and hashes recorded in
`evidence/ROLLOUT_PROVENANCE.md`; do not publish the originals because session
metadata can contain credentials or private transport configuration.
