# Status and Limitations

## No eligible scored submission

The formal run's pre-boundary baseline was prepared and executed remotely, but
it was never sent with `kaggle competitions submit`. The formal submission
ledger contains zero sent attempts. A completed Kernel and generated CSV do not
constitute a scored competition submission.

The account's full current Task 1 submission history is retained in
`remote/KAGGLE_SUBMISSIONS_CURRENT.json`. Other submissions visible there are
not attributed to this formal run merely because they share the same account or
overlap in wall-clock time.

## Post-boundary local work

The local `0.6994196064513399` trial completed after the 10:16:52 boundary and
is excluded. The later MFCC, Whisper, and Qwen development also followed custom
method/priority instructions and is excluded from the autonomous claim.

## Agent-executed `0.78049` result

The preserved submission record identifies:

- Kernel: `researai/ioai-find-order-mfcc-qwen-beam`, version 1
- Submission: `55267607`
- Submitted: `2026-08-05T10:54:51.343Z`
- Local score: `0.785577`
- Public LB: `0.78049`

This result remains labelled as a separately disclosed Agent-executed score in
the historical receipt and provenance. The post-boundary trace itself is not
part of the organizer-facing repository material.

Two limitations remain and are disclosed separately from actor attribution:

1. It was developed and submitted after material human supervision.
2. It was sent after the official Kaggle deadline
   `2026-08-05T10:50:00Z`. The formal Agent run's own deadline was the earlier
   `10:30:00Z`.

The exact receipt, submitted script, Kernel metadata, Kaggle log, CSV, final
trial record, and hash-only execution provenance are retained. A later controller
summary was deliberately omitted because it is not primary execution evidence
and contained private runtime details. Root `MANIFEST.sha256` covers every
retained artifact.

`ORGANIZER_REVIEW_REQUEST.md` asks the organizer to determine whether an
explicit exception or non-ranking recognition is appropriate. The request does
not itself change either limitation or the result's current eligibility status.

## Evidence limits

The published rollout excludes the boundary event and all post-boundary events
by construction. Private originals remain available locally for
organizer-supervised inspection and are bound by hashes. Competition audio,
labels, and model checkpoints are not
redistributed because the organizer already owns them and the competition rules
restrict data distribution.
