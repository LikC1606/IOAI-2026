# Request for Organizer Determination

## Purpose and current status

This document asks the IOAI organizer or Jury to determine whether Task 1
submission `55267607` may receive exceptional recognition. It does not assert
that the submission satisfied the official-prompt-only autonomy condition or
the competition deadline. Unless and until the organizer issues a written
decision, the package records the result as **Agent-executed, supervised, late,
and not ranking-eligible under the published rules**.

## Facts supported by the retained evidence

| Fact | Evidence-backed value |
|---|---|
| Submission actor | Formal solver Agent using the Kaggle CLI |
| Submission ID | `55267607` |
| Kernel | `researai/ioai-find-order-mfcc-qwen-beam`, version 1 |
| Local score | `0.785577` |
| Public Leaderboard score | `0.78049` |
| Kaggle submission time | `2026-08-05T10:54:51.343Z` |
| Agent run deadline | `2026-08-05T10:30:00.000Z` |
| Official Kaggle deadline | `2026-08-05T10:50:00.000Z` |
| Conservative supervision boundary | `2026-08-05T10:16:52.222Z` |

The exact submitted source, Kernel metadata, remote log, generated CSV,
submission receipt, local trial record, and hash-only execution provenance are
preserved under `submission/agent-executed-55267607/` and
`ROLLOUT_PROVENANCE.json`. Their hashes are covered by
`MANIFEST.sha256`.

## Attribution and eligibility are different claims

The execution trace supports attributing the Kaggle submission action to the
formal solver Agent. That attribution does not establish strict autonomy: the
controlling session had already received material human continuation,
optimization, and submission-priority instructions. It also does not override
the timestamp: Kaggle received the submission 24 minutes and 51 seconds after
the Agent run deadline and 4 minutes 51 seconds after the official Kaggle
deadline.

Accordingly, the evidence supports the statement "the Agent executed the
submission and obtained Public score `0.78049`." It does not support the
stronger statements "the result was produced under only the official prompts"
or "the result was eligible for the official ranking under the published
deadline rule."

## Basis for requesting organizer discretion

The result may still be technically useful to the organizer because the Agent
performed the final CLI submission itself, the exact artifact is reproducible,
the local and Public scores are closely aligned, and the full provenance is
available for inspection. The participant therefore asks the organizer to
decide whether these facts justify an exception, exhibition credit, or another
non-ranking form of recognition despite the disclosed supervision and timing
limitations.

## Decision states

- **Pending (current):** retain the score as an Agent-executed reference result,
  not an official-prompt-only or ranking-eligible result.
- **Approved exception:** use the exact label "Organizer-approved exception,"
  quote the scope of the organizer's decision, and retain a copy or hash of the
  written decision in this package.
- **Not approved:** keep the result as a reproducible technical record only and
  make no eligibility or official-ranking claim.

An organizer decision should specify whether it recognizes technical authorship,
autonomy, deadline eligibility, ranking eligibility, or only exhibition value;
these are separate questions. No package status should be upgraded merely from
an informal or participant-authored interpretation.

## Non-concealment statement

This request does not remove, rewrite, or hide the supervision boundary,
instructions, submission timestamp, deadline, or original artifacts. Any future
summary that cites an organizer exception must also preserve the underlying
facts and identify the exception as an organizer decision rather than ordinary
rule compliance.
