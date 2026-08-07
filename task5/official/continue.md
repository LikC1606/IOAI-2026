Continue solving the Kaggle competition ioai-2026-task-5-westlake-nlp-24.

Follow the project AGENTS.md. Read TASK_KNOWLEDGE.md and CANDIDATES.md, tail recent
experiment/submission records, and query active processes and Kaggle status. Read
only relevant RESEARCH.md sections; reopen the Overview when a rule or submission
detail is uncertain.

Restate the user's objective and requested mechanism. Recheck the task paradigm
and whether ML is needed. Treat validation/proxy, public LB, and private LB as
separate evidence; when they disagree, audit the target, information boundary,
metric/output parity, leakage, reuse, and distribution shift before same-family
tuning.

Revisit decomposition and the current high-upside routes. A weak implementation
needs a falsification signal and time budget; retire it when the signal fails or
its opportunity cost is worse. Keep diagnostics, scientific candidates, and the
deployable incumbent separate. Diagnostics may use extra local resources, but a
submitted candidate needs a credible Overview-compliant path.

While remote work or LB is pending, continue valuable experiments, research,
integration, and error analysis. Use CPU/GPU parallelism only when it increases
information per wall-clock minute.

For a remote action, use only the exact files and CLI commands copied from the
current Overview. The first meaningful legal output-valid baseline may establish
the remote reference; later actions need validation/proxy evidence or an explicit
mechanism-distinct hidden-judge probe. Run lightweight output, rule, runtime, and
memory checks, record the reason once, and never bypass Kaggle CLI. After LB
arrives, state what mechanism it supports or falsifies and choose one falsifiable
next action.
Do not stop after writing a report or making one submission.
