# Official prompt conformance audit

The Kaggle Overview for every Task 1–6 competition contains an exact Starter
Prompt and exact Continuation Prompt. On 2026-08-25, all 12 live page bodies
were retrieved with the Kaggle CLI and matched against the stored official
sources. Trace inputs were then compared as exact Unicode text, normalizing
only the optional final newline.

No-live-human autonomy and exact-organizer-prompt conformance are separate.
The former does not make a custom preconfigured/appended prompt official.

| Task | Exact starter events | Exact continuation events | Custom prompt events | Strict exact text | Causal finding |
|---|---:|---:|---:|:---:|---|
| task1 | 0 | 0 | 2 | No | The custom starter appendix precedes all work. The custom continuation at 2026-08-05T18:25:04.940Z is after submission 55277782, the final Agent answer, and task_complete at 2026-08-05T18:24:58.140Z, so that continuation did not cause the selected result. |
| task2 | 0 | 0 | 1 | No | The custom starter appendix precedes all work. No continuation event occurs in the later reproduction trace. |
| task3 | 4 | 0 | 0 | Yes | The selected traces contain exact organizer Starter Prompt text and no continuation event. |
| task4 | 0 | 0 | 15 | No | The starter has formatting changes. Six main-runtime custom continuation events begin at 2026-08-07T04:34:35.176Z; the selected submission 55316818 was sent later at 2026-08-07T06:10:48.923Z. Four inherited copies of the custom starter and four inherited copies of the continuation also appear in worker traces. |
| task5 | 14 | 0 | 0 | Yes | The selected traces contain exact organizer Starter Prompt text and no continuation event. |
| task6 | 3 | 0 | 0 | Yes | The selected pre-intervention traces contain exact organizer Starter Prompt text and no continuation event. |

## Result

- Exact-prompt trace text: Tasks 3, 5, and 6.
- Non-exact prompt text: Tasks 1, 2, and 4.
- Task 1's custom continuation is post-result, but its custom starter appendix
  still prevents an exact-prompt-only claim.
- Task 4's custom continuation is pre-result and substantive; its final
  selected submission is downstream of it.

This repository does not self-certify organizer acceptance. The Jury decides
whether disclosed deviations are recognized. Event hashes, timestamps, prompt
classes, and official prompt hashes are in
[`PROMPT_CONFORMANCE_AUDIT.json`](PROMPT_CONFORMANCE_AUDIT.json).
