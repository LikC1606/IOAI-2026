# Excluded Work and Results

The following material is not part of the official-Prompt-only autonomous score
claim, even when it exists in the original run directory or Kaggle history.

## Boundary-based exclusions

- Every solver action or result at or after 2026-08-06 13:46:19.450 CST, the
  first request to modify Continue behavior and reread `AGENTS.md`.
- Every modified or augmented Continuation Prompt, including otherwise official
  continuation text with an extra sentence.
- Later worker-restart, reasoning-effort, API-provider, parallelism, method,
  urgency, or forced-submission prompts.
- Current `TASK_KNOWLEDGE.md`, `RESEARCH.md`, `CANDIDATES.md`, and project
  `AGENTS.md`, because they were modified after the boundary and are not valid
  historical snapshots. A clearly labelled evidence-based summary is provided
  instead at `research/PRE_BOUNDARY_RESEARCH_SUMMARY.md`.

## Version and method exclusions

- v10's remote Submission 55290027 and LB 53.43333. Its source was created before
  the boundary and may be inspected as a research candidate, but the scored
  submit was sent at 13:47:27 CST, after the boundary.
- The centered-geometry route and every broad-round/tail route created after the
  boundary, including v11/v12 and the late tail submissions.
- User-suggested static/dynamic semantic-embedding routes and any “use early
  games to update an embedding” work. Those suggestions occurred well after the
  conservative boundary.
- All later online-metric, multiview, particle, or other post-deadline work, even
  if its code used only legal competition data.
- v13 and v14 external GloVe/fastText submissions. They used external embeddings
  and are directly incompatible with the official no-external-data/model/embedding
  rule. They are not copied into this package and must not be presented as legal.

## Score exclusion rule

Only v1-v8 remote results are reported as autonomous scores. A later result is
not rehabilitated by the fact that a related idea, partial source, or autonomous
thought existed earlier. The complete scored action must fall before the boundary.

`remote/KAGGLE_SUBMISSIONS_CURRENT.json` is retained as a full platform-history
snapshot solely so exclusions can be audited. The authoritative positive subset
is `remote/KAGGLE_SUBMISSIONS_AUTONOMOUS_V1_V8.json`.
