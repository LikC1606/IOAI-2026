# Task 1 Compliance and Reproduction Note

This is a post-run organizer-review note. It does not alter the historical
submission, claim an organizer decision, or convert a supervised late result
into an official-prompt-only result.

## Status

| Question | Evidence-backed answer |
|---|---|
| Was submission 55267607 executed by the formal solver Agent? | Yes |
| Was it produced under only the official Starter/Continuation prompts? | No |
| Was it sent before the official deadline? | No |
| Public LB | 0.78049 |
| Private/final LB | Not available |
| Organizer exception | Pending; not assumed |

The exclusive autonomy boundary is `2026-08-05T10:16:52.222Z`. The scored
submission was sent at `2026-08-05T10:54:51.343Z`, after both the first material
human continuation instruction and the `10:30:00Z` deadline. See
`AUTONOMY_BOUNDARY.md` and `ORGANIZER_REVIEW_REQUEST.md` for the exact scope.

Before that boundary, the Agent produced a valid 200-row remote baseline and a
local score of 0.6827101986420873, but did not send a competition submission.
It is evidence of autonomous work, not an autonomous leaderboard score.

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

`tools/verify_package.py` verifies the boundary, submission actor trace, local
trial, unscored baseline, scored receipt, source/output hashes, and absence of
plaintext secrets. Because it refreshes `VERIFY_REPORT.json`, regenerate the
manifest if that report changes. This package supports organizer review; the
Jury decides recognition and eligibility.
