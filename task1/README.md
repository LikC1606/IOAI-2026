# IOAI 2026 Task 1 Organizer Review Package

Competition: `ioai-2026-task-1-westlake-nlp-24`.

This package preserves the formal Task 1 Agent's submitted result and separates
execution attribution from strict autonomy/ranking status. It is evidence for organizer review, not a self-issued
compliance certificate; the organizer or Jury remains the final authority.

## Defensible result

| Claim | Result |
|---|---:|
| Formal run start | 2026-08-05 09:20:36.326 UTC |
| Exclusive autonomy boundary | 2026-08-05 10:16:52.222 UTC |
| Agent-executed Kaggle submission | `55267607` |
| Agent-executed Public LB | **0.78049** |
| Best pre-boundary local trial | `trial-605da205` |
| Best pre-boundary local score | **0.6827101986420873** |
| Official-prompt-only scored submission | None |

The formal solver received the `AGENTS.md` instructions actually present at
startup and the exact organizer Starter Prompt. The positive rollout is cut
before the controlling session first received a material human instruction:

> 你让他继续优化 找到高分了再提交

The solver had already created and validated a prefix-aware baseline. A Kaggle
notebook containing that baseline completed and generated a valid 200-row CSV,
but no `kaggle competitions submit` action associated that notebook with a
scored competition submission. It is retained under
`remote/preboundary-baseline-not-scored/` as execution evidence, not as a
leaderboard result.

## Agent-executed result

Submission `55267607`, Public LB `0.78049`, is treated as the main
Agent-executed result. The post-boundary solver trace directly retains the
Agent's CLI submission actions and returned submission identity. Exact files
are under `submission/agent-executed-55267607/`.

This execution attribution does not erase provenance: the result was completed
after material human continuation instructions and was sent at 10:54:51 UTC,
after the official 10:30:00 UTC deadline. It is therefore an Agent result, but
not an official-prompt-only autonomous or official-ranking-eligible result.

`ORGANIZER_REVIEW_REQUEST.md` presents the result for organizer discretion. It
separates execution attribution, strict autonomy, deadline eligibility, and
possible exceptional recognition. The current status remains pending; only a
written organizer decision can change it to "Organizer-approved exception."

Start with `COMPLIANCE.md`, `ORGANIZER_REVIEW_REQUEST.md`,
`AUTONOMY_BOUNDARY.md`, `EXCLUSIONS.md`, and `SUMMARY.json`. The exact
credential-redacted pre-boundary
solver trace is under `evidence/rollouts/`, and `ROLLOUT_PROVENANCE.json` binds
it to the private original by SHA-256.

Verify after extraction:

```bash
sha256sum -c MANIFEST.sha256
python tools/verify_package.py
```

The package does not duplicate organizer competition data or model weights.
The exact frozen candidate source, evaluator, trial receipt, remote source,
remote log, scored output, and Agent submission trace are included.
