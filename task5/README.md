# Task 5 Autonomous Evidence

Competition: `ioai-2026-task-5-westlake-nlp-24`.

The formal run began at 07:04:20 UTC and stopped at its two-hour deadline,
09:04:20.519 UTC. The main solver and autonomous workers received the organizer
Starter Prompt; the main solver received no Continuation Prompt or custom method
instruction. Controller messages during the run only requested status and were
not delivered to the solver.

All seven submissions were sent before the deadline:

| Version | Submission | UTC sent | Public LB |
|---:|---:|---|---:|
| 1 | 55318340 | 07:25:06.867 | 28.60 |
| 2 | 55318761 | 07:37:56.770 | 90.86 |
| 3 | 55319289 | 07:53:07.707 | 92.48 |
| 4 | 55319516 | 08:01:30.577 | 92.73 |
| 5 | 55320028 | 08:28:12.897 | 94.56 |
| 6 | 55320296 | 08:43:46.740 | **95.39** |
| 7 | 55320652 | 09:02:01.927 | 94.17 |

Version 6 is the best result. It used the locally supplied permitted
`bge-base-en-v1.5`, fine-tuned/refit on official labels, one Tesla T4, and no
Internet. Remote runtime was 289.3 seconds with 5.00 GB peak VRAM. The exact
remote v6 log and 760-row output are under `remote/v6/`; the preserved source
used for that version is `notebooks/BEST_V6_SOURCE.py`.

Version 7 was the final remote Kernel version, so Kaggle CLI can still pull its
exact source. `notebooks/REMOTE_CURRENT_V7.py` is byte-identical to the local
final `notebooks/script.py`. The historical private v6 source endpoint returns
403; therefore the package describes `BEST_V6_SOURCE.py` as the preserved v6
source, not as a newly downloaded historical source. The exact v6 remote output,
log, submission ID, and score remain available and are included.

No private leaderboard score is available in the captured Kaggle records. Public
and private performance must not be conflated.

