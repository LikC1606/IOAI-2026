# Task 6 Exclusions and Limits

- Main-trace events at or after `2026-08-08T18:09:48.833Z`, the first
  human-triggered resume prompt, and every causally downstream event are outside
  the autonomous claim.
- The later human target-score prompt and the two workers created after resume
  are excluded. Their timestamps and hashes remain in
  `evidence/SUPERVISED_EXCLUSIONS.json`; their prompt bodies are not published.
- Submissions `55357740`, `55358042`, and `55358739` are outside the autonomous
  v3 claim. The last two were also after the official deadline.
- Bulk competition inputs, protected binaries, intermediate local checkpoints,
  raw Codex SQLite state, credentials, and encrypted hidden reasoning are not
  redistributed.
- The organizer evaluator source is not copied. Its SHA-256, function/call-site
  locators, and observed batching behavior are recorded in
  `evidence/EVALUATOR_BATCHING_PROVENANCE.json` for comparison with the Jury's
  organizer copy.
- Unlike the earlier compact package, the exact final v3 notebook, metadata,
  submitted CSV, and decoded submitted model source are now included because
  they are necessary to audit the official result.
- The exact v3 notebook was recovered from the preserved original Task 6
  project rather than independently downloaded from a historical Kaggle source
  endpoint. The exact remote CSV independently binds its decoded source and
  weights.
- No official Jury decision on the evaluator-batch-dependent method is claimed.
  `RULE_DIFFERENCE_AUDIT.md` records the evidence and interpretation boundary.
