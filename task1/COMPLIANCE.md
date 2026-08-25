# Task 1 Compliance and Reproduction Note

This is a post-run organizer-review note. It does not alter the historical
submission, claim an organizer decision, or convert a supervised late result
into an official-prompt-only result.

## Record recovery note

The original Task 1 run record was unavailable after a school-server restart.
The published `evidence/reproduction-120m/rollout.jsonl` is a later fresh
reproduction using the same configured solver/system, official competition
bundle, and organizer constraints. Its first 1,383 unmodified events through
`task_complete` are selected as the canonical solution trace at
`evidence/canonical/rollout-solution-prefix.jsonl`; the complete trace is kept
as raw audit evidence. Both are separated from the lost original run and the
official account result.

## Status

| Question | Evidence-backed answer |
|---|---|
| Was submission 55267607 executed by the formal solver Agent? | Yes |
| Was it produced under only the official Starter/Continuation prompts? | No |
| Was it sent before the official deadline? | No |
| Agent-executed Public / Private | 0.78049 / 0.76808 |
| Official final Public / Private | 0.77751 / 0.80474 |
| Organizer exception | Pending; not assumed |

The exclusive autonomy boundary is `2026-08-05T10:16:52.222Z`. The scored
submission was sent at `2026-08-05T10:54:51.343Z`, after both the first material
human continuation instruction and the official `10:50:00Z` Kaggle deadline.
The formal Agent run had an earlier `10:30:00Z` deadline. See
`AUTONOMY_BOUNDARY.md` and `ORGANIZER_REVIEW_REQUEST.md` for the exact scope.

Before that boundary, the Agent produced a valid 200-row remote baseline and a
local score of 0.6827101986420873, but did not send a competition submission.
It is evidence of autonomous work, not an autonomous leaderboard score.

The account's official final result is the exact tie `55267333` / `55267368`,
Public 0.77751 and Private 0.80474. It comes from the organizer-requested Kaggle
extraction and is not attributed to the human-intervention-free trace.

## Scored artifact

- Submission: `55267607`, Kernel version 1, Public LB `0.78049`.
- Source SHA-256: `81d89f00f1c68d70e39fc069086419f2409e9ee531459de25f09c621e518652f`.
- CSV SHA-256: `f997dea01312701ffe9fae0094539634a92b5c8835a31437a51ab8aeb40d23a6`.
- Remote log SHA-256: `370cf90f0777675bf678c52a371d748fc3246018db281b55df8f1def6d52e40c`.
- Output: 200 rows with columns `filename,prediction`; the remote run completed
  in about 335.4 seconds.

The historical ten-paragraph source report says Public LB was pending, which
was true when written. The value above is a later platform observation and is
not silently inserted into the immutable source report.

## Verify

From `task1/`:

```bash
sha256sum -c MANIFEST.sha256
python tools/verify_package.py
```

`tools/verify_package.py` verifies the boundary hashes, local
trial, unscored baseline, scored receipt, source/output hashes, and absence of
plaintext secrets. Because it refreshes `VERIFY_REPORT.json`, regenerate the
manifest if that report changes. This package supports organizer review; the
Jury decides recognition and eligibility.

The later 120-minute reproduction trace is published in full at
`evidence/reproduction-120m/rollout.jsonl` and indexed in
`../REPRODUCTION_TRACE_INDEX.json`. Its canonical solution trace is
`evidence/canonical/rollout-solution-prefix.jsonl`. The `55277782` / `0.74121`
score is post-deadline reference evidence only; it is not an official-ranking
result or a replacement for the official account reconciliation.

This reproduction is not claimed as strict exact-organizer-prompt text. Its
starter appends a custom fresh-run-isolation section. The canonical prefix has
no continuation; the complete raw trace retains a later custom continuation
after the selected submission, final Agent answer, and `task_complete`. See
`../PROMPT_CONFORMANCE_AUDIT.md` for hashes and timestamps.

## Additional rule and material limits

- The official final refs `55267333` / `55267368` are not bound to either the
  lost original trace or the later reproduction. The GitHub task package does
  not contain their exact notebook/source/output as a trace-linked final
  artifact set. They may appear in the separately delivered Kaggle extraction,
  but that does not establish autonomous causality.
- The later reproduction searched AI4Code, sentence-ordering and Qwen method
  material before candidate selection. No external runtime data or weights were
  added beyond organizer-supplied resources, but the method information may
  have influenced the reproduced solution. Whether method literature is
  prohibited "externally generated information" is a Jury-interpretation risk.
- The extraction captured 38 Task 1 notebook versions across the account,
  compared with the published 20-version limit. Many are post-deadline,
  including later reproduction activity. The package cannot establish from the
  current summary whether the Jury counts only competition-window versions or
  every captured version, so this is disclosed as an account-history budget
  risk rather than silently marked compliant.
- API USD, GPU USD, and the original lost run's compute total remain
  unavailable. Cost records cover the selected later reproduction only.
