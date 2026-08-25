# Task 4 Autonomous Evidence

Competition: `ioai-2026-task-4-westlake-nlp-24`.

For the consolidated rule, artifact, report-correction, and reproduction audit,
start with `RULE_DIFFERENCE_AUDIT.md` and `COMPLIANCE.md`.

The formal run used a formatting-modified copy of the organizer Starter Prompt
plus a substantive generic runtime resume template that is not the exact
organizer Continuation Prompt. The resume template did not inject a live
human-selected method, candidate, score target, or forced-submission
instruction, but this remains a prompt-text deviation. The trace set includes
the formal main/workers and seven supplemental parallel-solver traces that
produced versions 2/3 and the comparison evidence used by version 4.
`evidence/SUPPLEMENTAL_ROLLOUT_PROVENANCE.json` records why they were added and
binds them to the private originals.

Accordingly, this package supports a no-live-human execution claim, not a
strict exact-organizer-prompt claim. The final selected submission is downstream
of the custom continuation events. See `../PROMPT_CONFORMANCE_AUDIT.md`; the
organizer/Jury decides whether the disclosed deviation is recognized.

The full rule audit also discloses three narrower risks: the local notebook
folder contained a transient `__pycache__` before some pushes even though the
remote source artifact was unaffected; a parallel solver made two arXiv search
queries after version 3 was pushed without evidence that their results entered
the final version-4 path; and local development records mention one H100 while
the final notebook itself ran on the required one T4 at `cuda:0`. These are not
silently recast as compliant facts; see `RULE_DIFFERENCE_AUDIT.md`.

Eligible submissions:

| Kernel version | Submission | UTC sent | Public LB | Private LB |
|---:|---:|---|---:|---:|
| 1 | 55315359 | 05:08:49.403 | 98.23 | 98.14 |
| 2 | 55316194 | 05:41:32.143 | 98.36 | 98.27 |
| 4 | 55316818 | 06:10:48.923 | **98.41** | **98.32** |

Version 3 was an autonomous diagnostic Kernel but was not submitted. Version 4
was accepted 4 minutes 11.077 seconds before the official Kaggle deadline at
06:15:00 UTC and 7 minutes 36.594 seconds before the agent-run deadline at
06:18:25.517 UTC. It ran on one Tesla T4 in about 316 seconds. Its exact current remote source matches
`notebooks/script.py` with SHA-256
`d467bc5a1e7c83ae7da780aaf01fb6ac001fd326e514495cae3a9279b7b6301b`.

The exact scored output had 200 rows, the required `id,delta_a,delta_b` schema,
400 finite original-resolution tensors, and size 190,117,536 bytes. Its SHA-256
is `bdb202711d6494bc94c331d549b0fa7956aa1d9eb585c247ae0dfce723f76542`.
The large CSV is not duplicated in this compact package; `remote/V4_KERNEL.log`
and `remote/V4_RUNTIME_HELPER.py` are exact downloaded remote artifacts, and the
CSV remains retrievable from Kernel
`researai/ioai-2026-task-4-westlake-nlp-24-solution`, version 4.

The score became visible just after the local run deadline. The scored action
itself was sent before both deadlines, and the project record states the organizer
rule that an already-sent notebook may finish scoring afterward. No later model
tuning or resubmission is included.

The organizer-requested extraction later restored all three Private scores. The
latest, highest Public, highest Private, official-deadline, and autonomous result
are all submission `55316818`; see `remote/FINAL_ACCOUNT_RESULTS.json`.
