# Task 4 Autonomous Evidence

Competition: `ioai-2026-task-4-westlake-nlp-24`.

The formal run used the organizer Starter Prompt and exact organizer
Continuation Prompt. No human method suggestion was found in solver-role inputs.
The additional rollout files are autonomous workers and official-prompt resumes;
they are included so the multi-agent provenance is inspectable rather than
collapsed into a single narrative.

Eligible submissions:

| Kernel version | Submission | UTC sent | Public LB |
|---:|---:|---|---:|
| 1 | 55315359 | 05:08:49.403 | 98.23 |
| 2 | 55316194 | 05:41:32.143 | 98.36 |
| 4 | 55316818 | 06:10:48.923 | **98.41** |

Version 3 was an autonomous diagnostic Kernel but was not submitted. Version 4
was accepted 7 minutes 36 seconds before the 06:18:25.517 UTC deadline and ran
on one Tesla T4 in about 316 seconds. Its exact current remote source matches
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
itself was sent before the deadline, and the project record states the organizer
rule that an already-sent notebook may finish scoring afterward. No later model
tuning or resubmission is included.

