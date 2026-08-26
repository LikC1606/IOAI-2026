# Original session recovery — Tasks 1–2

The initial expected-path copies of the formal Task 1 and Task 2 sessions were
thought to have been lost after a school-server restart. A subsequent audit of
the private local run archives located both complete raw JSONL sessions. This
register records their hashes and event counts so the recovery is auditable
without publishing private human-influenced content.

The complete raw sessions are deliberately **not** copied into GitHub. Each
contains events at and after a live-human supervision boundary. The public
package therefore retains the exact-prompt prefix before that boundary and
excludes the boundary prompt, its body, and every causally downstream event.
This is a causal evidence decision, not a claim that the raw session is still
missing.

| Task | Private raw events | Private SHA-256 | Published prefix | Excluded suffix | Boundary (exclusive UTC) |
|---|---:|---|---:|---:|---|
| 1 | 775 | `caeff9bb37bef475044391ca35ba834a3aaf144278b66b50adffbc023127e3d6` | 350 | 425 | `2026-08-05T10:16:52.222Z` |
| 2 | 1,367 | `0573b7a06093526fa9d81856ec370801e66fff4404e2c6811909db8ef292b09d` | 705 | 662 | `2026-08-05T06:24:47.549Z` |

The machine-readable fields, private archive paths, prefix hashes, timestamps,
and suffix classifications are in
[`ORIGINAL_SESSION_RECOVERY.json`](ORIGINAL_SESSION_RECOVERY.json).

## What a reviewer should conclude

- The 350-event Task 1 and 705-event Task 2 files are verified prefixes of the
  recovered raw sessions, not fabricated replacements.
- The omitted Task 1 suffix contains the later human continuation and its
  downstream actions. The omitted Task 2 suffix begins exactly with the first
  modified continuation prompt and contains its downstream actions.
- Human prompt bodies, private endpoints, credentials, and opaque reasoning are
  not released. A reviewer with authorized access to the local archive can
  verify the private SHA-256 values independently.
- The account's official final submissions remain separate from these prefixes;
  a recovered raw session does not retroactively establish causal trace
  alignment.

The six-task package remains an organizer-review evidence package rather than a
self-issued compliance certificate.
