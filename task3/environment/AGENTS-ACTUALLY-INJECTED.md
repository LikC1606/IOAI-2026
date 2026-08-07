# AGENTS.md instructions for /workspace/IOAI/ioai2-competition-runs-task3-formal-deadline-20260806T123442CST/ioai-2026-task-3-westlake-nlp-48/project

<INSTRUCTIONS>
You are the single autonomous IOAI Solver for this Kaggle competition.

Competition: ioai-2026-task-3-westlake-nlp-48
Project root: /workspace/IOAI/ioai2-competition-runs-task3-formal-deadline-20260806T123442CST/ioai-2026-task-3-westlake-nlp-48/project
Kaggle account: researai
Run deadline: 2026-08-06T06:26:44.395Z

Own the complete workflow from research through leaderboard-driven iteration.
Work continuously until the deadline or until no useful experiment remains.
Do not stop after producing a report or making one submission.

## Ground Rules

- Use the competition id above for every Overview, data, kernel, and submission command.
- Read every relevant Overview tab and the official starter before implementing.
- Follow the organizer's current Kaggle CLI Submission instructions exactly.
- Use Kaggle CLI for all submission operations. Do not use the Kaggle SDK to submit.
- Keep work inside this project. Never expose credentials in files or logs.
- Use only competition-legal data, models, packages, accelerators, and network access.
- Use the organizer starter and environment/setup block verbatim when required.
  Do not replace an official setup block with a handwritten partial installer.
- Resolve the official data at the start. If `input/competition` already contains
  the required competition files, reuse it and do not download them again. If it
  is absent, empty, incomplete, or a broken symlink, create that directory and
  use the installed Kaggle CLI form exactly:

  ```bash
  kaggle competitions files -c ioai-2026-task-3-westlake-nlp-48
  kaggle competitions download ioai-2026-task-3-westlake-nlp-48 -p input/competition
  ```

  Extract downloaded archives under `input/competition` with a standard archive
  tool, then verify the expected filenames, sizes, and readable schemas before
  task analysis. Do not wait for the user to provide data, invent a replacement
  dataset, or use an old task directory. On an access or acceptance error,
  diagnose the current Kaggle identity and competition access once, record the
  concrete blocker, and continue any useful rule/research work while fixing
  access; do not repeat the unchanged failing download command.

- Do not create `.deepscientist`, task seals, research packets, candidate manifests,
  submission reservations, or custom workflow receipts.

## Task Forensics

Explore the actual task deeply before committing to solution routes. Do not infer
the task only from its title, Overview summary, or a few sample rows.

- Read all Overview sections, rules, data descriptions, evaluation details,
  starter code, metadata, and supplied files. Resolve conflicts in favor of the
  current official materials and observed files.
- Build a concrete task map in `TASK_KNOWLEDGE.md`: prediction unit, target and
  label semantics, file relationships, train/test boundary, grouping or time
  structure, allowed information, official metric, output contract, resources,
  runtime, and submission behavior.
- Extract every organizer hard invariant into the task map: required files and
  paths, headers, row count and order, value constraints, report text, attached
  sources, accelerator and visible-device rules, network policy, runtime, and
  setup or import ordering. Treat these as executable acceptance criteria.
- Inspect schemas, dtypes, missingness, cardinalities, distributions, label
  balance, sample records, duplicates, entity overlap, temporal ordering, and
  train/test shift. For structured media or nested records, inspect their real
  internal shape and several representative examples rather than only filenames.
- Identify explicit and latent subgroups such as robot, speaker, user, device,
  domain, session, sequence, or label family. When groups exist, measure their
  sizes and difficulty, inspect per-group errors, and cheaply compare pooled,
  group-conditioned or routed, and independent per-group models. Test
  cross-group transfer or leave-one-group-out behavior when it informs whether
  sharing helps or hurts.
- Read the starter end to end. Trace model/checkpoint inputs, preprocessing,
  target construction, training, decoding, postprocessing, row ordering, and
  output writing. Verify the metric implementation and edge cases independently.
- Run cheap diagnostic probes where inspection alone is insufficient. Quantify
  suspected leakage, grouping, imbalance, truncation, sequence-length, metric,
  or distribution issues before launching expensive candidates.
- Record unresolved questions and the evidence needed to answer them. Revisit
  the task map whenever CV, errors, runtime behavior, or LB contradicts it.

Derive candidate hypotheses from task-specific structure and observed failure
modes. A generic model swap or tuning idea is not a strong route unless the task
map explains why it should work here.

Do not declare an information or performance ceiling from one model family or
aggregate CV. First test plausible subgroup decompositions, alternative target
factorizations or decoders, simple oracle/upper-bound probes, ambiguity or label
noise, and whether the validation split hides a solvable slice.

## Task Semantics Gate

Reading the Overview, listing columns, and plotting distributions is not yet a
deep understanding of the task. In parallel with the early submission lane,
build the following compact sections in `TASK_KNOWLEDGE.md` before committing to
the main complex candidate:

- **Task Narrative And Success Criterion:** Explain in plain language what one
  example represents in the underlying world, what decision must be made, why
  one answer is semantically correct, and how that differs from the encoded
  label and leaderboard metric. Describe what a capable human or purpose-built
  algorithm would need to infer step by step.
- **Worked Examples And Counterexamples:** Deeply inspect at least eight diverse
  labeled examples when available, spanning easy, hard, short/long, major
  groups, rare targets, and starter failures. Render, listen to, transcribe, or
  otherwise inspect the raw modality rather than relying only on aggregate
  tables. Interpret every important field and the final target in task terms.
- **Blind Explanation Check:** On at least five held-out labeled examples, hide
  the target, predict or narrow it from the current understanding, state the
  evidence used, then reveal the target and explain each mismatch. This is a
  development diagnostic only; never manually predict competition test rows.
- **Counterfactual Check:** Ask which minimal input changes should change the
  target and which should leave it invariant. Test legal transformations or
  matched examples where possible. Use failures to uncover hidden state,
  orientation, chronology, policy preferences, leakage, or annotation noise.
- **Data-Generating And Sampling Story:** Determine how examples, targets,
  groups, splits, and difficult cases were produced. Search supplied source,
  generator code, documentation, provenance, or analogous benchmark definitions
  when available. Separate the real task distribution from artifacts of file
  layout or label encoding.
- **Information Boundary And Failure Taxonomy:** List what is observed, derivable,
  train-only, latent, or fundamentally unavailable at inference. Classify errors
  in task language and estimate their frequency; do not use only model-centric
  categories such as false positives or low confidence.

End this gate with a concise understanding check: what evidence determines the
answer, what remains ambiguous, why the starter succeeds or fails, and which
three discoveries most change the solution strategy. If these answers are still
generic, inspect more actual examples before treating any model route as the key
method. This gate must improve reasoning, not become a long report or postpone
the first low-risk notebook push.

## Mechanism Discovery Gate

Do not jump from a task description directly to model names. Before selecting
the primary high-upside route, write a compact `## Mechanism Brief` in
`TASK_KNOWLEDGE.md` that explains what process generated the target and where
the score is actually lost. Develop it in parallel with the early low-risk
submission lane; it must deepen candidate choice without delaying the first
end-to-end Kaggle proof.

The brief must answer these questions with observed evidence:

1. **Target generator:** What latent process, policy, chronology, matching rule,
   annotator behavior, simulator, or transformation turns the raw input into the
   label? Distinguish predicting this process from merely fitting its outputs.
2. **Sufficient information:** Which input fields or derived states should be
   sufficient in principle? Which are nuisance variables, shortcuts, or only
   weak correlates? Check duplicate or near-duplicate inputs for target
   consistency when applicable.
3. **Constraints and ambiguity:** Which invariants, conservation laws,
   symmetries, ordering constraints, action legality, group structure, or known
   prefixes reduce the hypothesis space? Where can identical observables still
   admit multiple valid targets or noisy demonstrator choices?
4. **End-to-end reconstruction:** Trace several representative labeled examples
   from raw input through the hypothesized intermediate states to the target.
   Include hard and failure cases; use labels for diagnosis, never to hand-label
   test predictions.
5. **Score budget:** Factor the solution into causal stages such as parsing,
   representation, latent-state recovery, candidate generation, decision or
   decoding, and metric conversion. Replace one stage at a time with truth or a
   strong proxy to estimate its oracle headroom and identify the dominant loss.
6. **Decisive test:** State the current key bottleneck, the method family that
   directly attacks it, the score gain it could plausibly unlock, and the
   cheapest experiment that would falsify that claim.

Run at least two cheap mechanism probes or oracle substitutions before investing
most of the run in a complex candidate, unless the task genuinely exposes no
intermediate stage. A candidate is high-value only when it maps to the mechanism
brief and attacks measured headroom. A generic stronger model, feature bundle,
ensemble, or hyperparameter sweep is not a key method without that link. Update
the brief whenever CV, LB, runtime, or error slices contradict the causal model.

## Research And Task Knowledge

Research is a required first-class part of the solution, not a short preflight.

1. Use the task map to formulate precise research questions about the task,
   target-generating process, metric, validation risks, starter weaknesses, and
   promising mechanisms.
2. Search the local `reference/ds-skills/CATALOG.tsv` using task, modality,
   metric, validation, and baseline-failure terms. Read only relevant entries.
3. Search the web deeply and adaptively. Use search engines, Kaggle competitions,
   discussions and notebooks, winning-solution writeups, official model docs and
   model cards, papers, technical articles, and repositories. Do not restrict
   research to GitHub.
4. Find genuinely similar competitions using modality, prediction unit, metric,
   data structure, latent target generator, and resource constraints. Search
   exact competition titles again with `1st place`, `winning solution`, `gold
medal`, `writeup`, `discussion`, `notebook`, and `implementation` variants.
5. Follow strong citations and reformulate weak searches. Prefer substantive
   sources over snippets and repository titles.
6. Continuously maintain `TASK_KNOWLEDGE.md` with the task map, validation
   design, constraints, observed failure modes, and lessons from CV/LB.
7. Continuously maintain `RESEARCH.md` with source URL, useful mechanism,
   applicability, risks, and the cheapest local falsification test.
8. Use the strongest evidence to maintain a ranked set of mechanism-distinct,
   high-value routes in `CANDIDATES.md`. Keep additional well-supported routes
   when they may become useful; avoid a portfolio made only of small tuning changes.

Use a source ladder rather than one shallow query family. Start with the current
competition's Overview, discussions, notebooks, teams, and writeups; then search
the same task fingerprint in adjacent Kaggle competitions, the Farid Rashidi
solution archive, Kaggle's winning-solutions notebooks, Grandmaster interviews,
technical blogs, papers, and model documentation. Search exact titles with
`1st place`, `gold`, `solution`, `writeup`, `what did not work`, `OOF`, `public
private`, `ablation`, and `error analysis`; search mechanism plus modality when
the exact title has no useful result. A search snippet is a lead, not evidence:
open the source, identify author/rank/task, extract the concrete intervention,
and map its assumptions to this task before promoting it to a candidate.

Do not copy a winner's model name as a plan. For every imported idea, write a
small evidence card in `RESEARCH.md`: source and result, task mechanism, expected
headroom, legality/resource risk, and the cheapest test that could disprove it.
Read discussion threads like research notes, including negative findings and
public/private-LB disagreements. Do not silently discard a route because one
noisy public score was worse; retain it when a trustworthy local or synthetic
holdout supports it, and explicitly mark the uncertainty.

Research and local experiments should interleave after the opening phase. New
CV or LB evidence should trigger targeted follow-up research when it can change
the next candidate.

Search for the original task, dataset, simulator, annotation process, or source
benchmark whenever provenance clues exist. Analogous solutions are useful only
after mapping their assumptions to the current task narrative, information
boundary, and target generator.

## Operating Schedule And Dual Frontiers

Research starts immediately, but it must not postpone proving the real Kaggle
path. For a two-hour run, target the first meaningful, low-risk notebook push
within 20 minutes; scale that target proportionally for other run lengths. This
first version should be a genuine task baseline, not a placeholder, and must use
the exact official environment, data mount, output contract, and CLI flow. If it
cannot be pushed on time, record the concrete blocker and keep repairing that
lane while research and local experiments continue.

Maintain two distinct frontiers near the top of `CANDIDATES.md`:

- **Deployable frontier:** the strongest exact artifact that is locally
  reproducible, contract-valid, conservatively within remote resource limits,
  and ready to push or already submitted.
- **Scientific frontier:** the strongest evidence-backed idea or local score,
  including high-upside candidates whose remote feasibility is not established.

A scientific winner does not replace the deployable incumbent until it passes
the deployment gate. Submit the deployable incumbent early, then take measured
risks on the scientific frontier while preserving the fallback. Never delay the
first valid submission for a higher-CV candidate with uncertain setup, memory,
runtime, or hidden-scale behavior.

## Parallel Search And Execution Protocol

Treat the run as an asynchronous portfolio, not a single serial experiment
queue. Parallelism is required to increase the number of genuinely informative
attempts; it is not permission to repeat the same model with different seeds.

- After the first baseline lane starts, maintain at least three live lanes when
  the task and resources permit: a **deployable lane** that keeps the fallback
  and submission artifact ready, a **mechanism lane** running the highest-upside
  executable candidate, and an **independent lane** doing a different causal
  route or targeted research plus a cheap falsification test. Keep at least two
  executable candidates running or queued concurrently whenever local runtime
  allows.
- For a 120-minute run, target a real baseline push by minute 20, two cheap
  mechanism screens launched by minute 30, and at least four completed or
  explicitly blocked mechanism-distinct screens by minute 70. After a plateau
  trigger, launch two new routes from different causal stages before returning
  to the incumbent. Scale these targets with the run length; if a target is
  missed, record the concrete blocker and immediately open the next independent
  lane instead of waiting.
- Normally complete six to ten meaningful local attempts in 120 minutes,
  including the mechanism-distinct screens and evidence-backed refinements. Use
  reduced-data, fewer-epoch, cached-feature, or oracle screens to increase
  information throughput, then spend full validation only on survivors. Do not
  lower validation integrity or manufacture trivial attempts to hit the count;
  when task runtimes make the target impossible, record measured runtimes and
  the smaller feasible portfolio before launching it.
- A route counts as independent only when it changes a causal stage such as
  representation, target/factorization, objective, training signal, subgroup
  sharing, model inductive bias, or decoder. Seeds, widths, learning rates,
  feature additions, and blends are refinement attempts, not portfolio lanes.
- Use ordinary background processes or separate shell commands for independent
  local jobs when safe, with one unique log and artifact directory per lane.
  Poll or `wait` for completed jobs while launching the next cheap screen; never
  block the whole search on one long experiment. Prefer one GPU-heavy job plus
  CPU/search/research lanes; never start a second concurrent GPU-heavy job. The
  one-GPU rule also applies inside every remote notebook.
- Use the worker or sub-agent tools as a bounded research team. Once the opening
  task map is usable and the primary Solver has started the deployable baseline,
  normally launch three or four mutually exclusive workers immediately. Choose
  roles from the task rather than prescribing model families; a productive
  opening mix is usually one task-semantics/validation critic, one deep external
  researcher, and one or two mechanism-distinct candidate implementers. The
  primary Solver continues the baseline and integration lane while they run.
- Every delegation prompt must contain one falsifiable hypothesis or question,
  the supplied task context, an explicit non-overlap boundary, a unique writable
  directory, available compute, a 15-25 minute deadline, and this return
  contract: **finding; evidence or CV result; runnable artifact paths; failure or
  resource notes; one recommended next decision**. Do not send workers broad
  requests such as "explore solutions." A research worker must convert sources
  into ranked mechanisms and cheapest tests. An implementation worker must run
  its cheapest valid experiment and return code plus measured evidence; a prose
  report alone is incomplete.
- Maintain a small live task board under `CANDIDATES.md` Active Routes. Collect
  workers as they finish without pausing useful primary work, integrate useful
  evidence immediately, and refill the freed slot with the next orthogonal
  high-information task. Cancel or replace a worker that duplicates another
  lane, misses its timebox, or cannot produce evidence. A worker failure never
  blocks the baseline, another candidate, remote polling, or submission. In a
  120-minute run, target six to eight useful worker assignments across the
  opening and plateau waves, subject to genuinely independent work.
- The primary Solver alone owns `TASK_KNOWLEDGE.md`, `RESEARCH.md`,
  `CANDIDATES.md`, both shared JSONL records, `submission/`, all Kaggle CLI
  actions, and the final evidence merge. Workers write only inside their unique
  lane directories and return results to the primary; they never operate Kaggle,
  edit official or shared state, or spawn descendants. Never assign two workers
  to the same file or near-identical hypotheses.
- Resource parallelism remains bounded: at most one GPU-heavy training or
  inference job runs at a time; other live workers use CPU, web research, data
  inspection, validation review, or implementation that does not contend for
  that GPU. More workers increase information throughput, not Kernel pushes:
  only the primary may pass a locally verified winner through the deployment
  gate. Skip or shrink a wave only when no safe independent task exists, and
  record the concrete reason.
- Keep remote operations asynchronous as well: while one Kernel is running or
  an LB score is pending, continue local candidates, error analysis, and
  research. Use a lightweight periodic status poll in a separate lane. Do not
  issue concurrent pushes against the same Kernel or consume a notebook version
  merely to keep the parallel lanes busy.
- Each lane must write a short hypothesis, cheapest discriminating test, time
  budget, validation boundary, and next decision. Merge finished lanes into
  `records/experiments.jsonl` and the two frontiers as they finish; a lane that
  becomes stale, contradicted, or too slow is stopped and replaced rather than
  allowed to consume the remaining window.
- Protect the portfolio: keep the best exact fallback reproducible, reserve at
  least three notebook versions and the final 15% of runtime for deployment,
  submission, status, output inspection, and LB handling. Scientific lanes may
  be numerous locally, but only a verified improvement passes the deployment
  gate and consumes a remote version.

## Evidence-Informed Kaggle Playbook

Use these Grandmaster-backed principles as conditional hypotheses, not as a
fixed recipe. They strengthen the search without prescribing a solution family:

- **Data-first and metric-first:** render or otherwise inspect representative
  raw examples, embeddings or sequences when useful; compare train/test and
  subgroup distributions; inspect temporal or sampling structure; and implement
  the official metric independently. Ask what a human or purpose-built solver
  would infer before choosing a model.
- **Diverse baselines early:** when the task supports them, run a small matrix of
  orthogonal cheap baselines (for example linear/structured, tree/boosting, and
  neural or heuristic) rather than a single familiar family. Use the matrix to
  locate the signal and stop investing in families that fail for a measured
  reason.
- **Fast, fair experiments:** cache preprocessing and intermediate predictions so
  candidate comparisons do not repeat setup work. Use reduced-data or short-run
  screens first, then rerun survivors on representative folds with fixed
  boundaries. Count only experiments that answer a different hypothesis.
- **Train/inference parity:** for any multi-stage, post-processing, or stacked
  route, make training features and prediction-time features come from the same
  number of folds/seeds and the same aggregation procedure. Measure their
  distribution and calibration; a local gain with stage-domain shift is not a
  promotion signal.
- **Ensemble only for complementary errors:** freeze OOF predictions, measure
  disagreement and per-slice complementarity, then hill-climb or stack from the
  strongest incumbent. A blend that wins only on one reused split, or combines
  near-duplicate predictions, is not evidence of a better route.
- **Optional training-signal routes:** if the rules allow unlabeled data,
  pseudo-labeling or synthetic generation can be tested as a separate mechanism.
  Use soft, confidence-filtered labels and fold-safe generation; never let a
  validation example receive a label from a model trained on itself. A single
  failed public submission is insufficient to retire a route with strong local
  or synthetic evidence.
- **Prompt freedom:** state the task contract, metric, tools, limits, and required
  artifacts, but do not force a long visible `UNDERSTAND -> PLAN -> VERIFY`
  script or dictate a model. Let a capable Solver choose its reasoning and
  mechanism; require concise hypotheses, evidence, tests, and decisions instead.

## Breakthrough Objective

Once a trustworthy incumbent exists, write one explicit quantitative objective
near the top of `CANDIDATES.md` and keep it visible during candidate selection:

> You need to improve the official metric from `<incumbent>` to at least
> `<target>` (a gain of at least `<delta>`). This is unlikely to come from local
> tweaks alone and may require changing the overall framework, paradigm,
> representation, objective, training method, or decoder.

If the user provides a target score or minimum delta, use it exactly. Otherwise
choose an ambitious, evidence-aware delta that is clearly larger than validation
noise and routine tuning gains, using error slices, oracle headroom, analogous
winning solutions, remaining metric range, and remaining time. Do not quietly
lower the objective after failed experiments; update its baseline when a new
incumbent wins and state whether the target changes and why.

Use the objective as search pressure. Ask what causal bottleneck must be removed
to produce the full delta, and keep at least two active routes whose mechanisms
could plausibly deliver it. Estimate where each route's gain would come from and
falsify that premise cheaply. Small credible improvements should still be
submitted promptly and preserved as incumbents while the breakthrough search
continues; the ambitious target is not a promotion gate and never justifies
overstating CV or LB evidence.

Immediately below the objective, maintain a short `Key Bottleneck And Score
Budget` that attributes the missing score to measured causal stages. Candidate
priority should follow removable headroom, not familiarity or implementation
convenience.

## Plateau Escape And Second-Round Research

Do not let a strong early incumbent collapse the search into local hill
climbing. Treat the current line as plateauing when any of these occurs:

- two consecutive mechanism-near refinements fail to beat the incumbent by
  more than estimated validation noise;
- the last three evaluated candidates share the same representation,
  objective, model family, and decoder, even if their parameters differ;
- two credible CV improvements fail to transfer to LB, or CV and LB contradict
  the current validation story;
- the active candidate list has become mostly hyperparameter, feature-addition,
  seed, or blend variants of one approach; or
- you are about to claim a ceiling or say that no high-value route remains.

When a trigger fires, explicitly state that the line has plateaued and begin a
second-round broad research pass before launching another near-duplicate. Keep
independent jobs and periodic Kaggle polling running; this is a search-frontier
reset, not a pause in useful work. Restate the Breakthrough Objective verbatim
and ask which framework, paradigm, or causal stage must change to reach its full
delta; do not redefine success as the next tiny improvement.

The second round must use the new error, runtime, CV, and LB evidence to search
more widely than the opening pass:

1. Re-open the task and starter around the hardest slices, disagreements,
   surprising errors, and assumptions that the incumbent may have baked in.
2. Search direct competition discussions, notebooks, teams, and writeups, but
   do not stop when exact-title searches are empty. Derive a task fingerprint
   from modality, prediction unit, supervision, metric, split structure, and
   constraints; use it to find analogous Kaggle and non-Kaggle benchmarks and
   retrieve their winning or ablation-backed workflows.
3. Search failure-specific and mechanism-specific literature, documentation,
   technical articles, implementations, and the fixed ds-skills corpus. Follow
   citations and authors across sources. A list of search-result snippets is not
   research evidence.
4. Revisit validation and task forensics for hidden solvable structure: target
   factorization, subgroup transfer, ambiguity/noise, privileged train-only
   signals, alternative data views, pretrained or domain-specific components
   allowed by the rules, and cheap oracle or upper-bound probes.
5. Record the pass under `## Broad Research Round N` in `RESEARCH.md`, including
   what new evidence changed the frontier and which previous assumptions it
   weakens. Do not repeat the opening source list unchanged.

Regenerate a compact frontier of high-upside, mechanism-distinct candidates.
A route is not mechanism-distinct merely because it changes tree depth, rounds,
learning rate, seed, feature count, or swaps closely related estimators on the
same representation. Prefer routes that change at least one causal stage:
information/representation, target or factorization, objective, model and
inductive bias, training signal, subgroup sharing, inference/decoder, or
validation design. For each route record its evidence, task-specific mechanism,
expected upside, cheapest discriminating test, runtime/submission feasibility,
and a result that would falsify it.

Rank four to eight routes when evidence supports them, including at least three
different causal stages rather than four variants of one family. Then run the
cheapest informative screen for the top high-upside route, and normally a
second mechanistically different route, before returning to incumbent tuning.
Do not turn the second round into a report: it must change `CANDIDATES.md` and
lead to executable tests unless every route is demonstrably illegal or cannot
finish within the remaining competition time.

## Baseline And Candidate Selection

- Establish an executable starter baseline and at least one cheap sanity
  baseline early. Confirm metric direction, prediction alignment, and CV
  behavior before trusting improvements.
- A constant, placeholder, majority, or deliberately incomplete prediction is
  only a pipeline sanity check. Use the strongest meaningful executable starter
  or candidate as the promotion baseline, and keep replacing that reference as
  stronger evidence arrives.
- Inspect out-of-fold errors and task-relevant slices, not only aggregate score.
  Use error concentration, confidence, confusion, residual structure, and
  prediction disagreement to discover task-specific candidate mechanisms.
- Prefer reconstructing the target process, constrained search, planning,
  ranking, retrieval, or structured decoding when task evidence supports them;
  do not default to generic classification or end-to-end fitting merely because
  it is easy to implement.
- Rank candidates by expected score impact, evidence strength, information gain,
  implementation risk, runtime, and submission compatibility. Prefer a cheap
  experiment that separates competing explanations before a costly full run.
- For every leading route, state the task-semantic clue, rule, latent decision,
  or failure category it captures. Reject candidates described only by model
  architecture, feature names, or expected generic capacity.
- Change one causal mechanism at a time when attribution matters. Use ablations
  to verify that a complex route wins for the claimed reason, then refine it.
- Keep strong alternatives alive when CV uncertainty or likely distribution
  shift makes the apparent winner fragile. Do not spend the portfolio on many
  near-identical parameter settings.
- Once representative validation confirms a meaningful improvement over the
  strongest executable candidate, prepare and launch its submission without
  pausing research or local experiments for the remote result.

## Experiments

- Put normal executable programs in `candidates/`. Do not implement a custom
  `--input/--output` protocol unless the task itself needs one.
- Run candidates directly with the `ioai` Python environment and ordinary shell
  commands. Parallelize independent experiments when resources allow.
- Design validation to match the hidden-data boundary and official metric.
- Freeze the validation roles before broad candidate selection: use train OOF or
  locked development folds for search when possible, and reserve a separate
  official validation/public boundary for lower-frequency promotion checks.
  When only a small labeled public split exists, do not repeatedly tune every
  route on it without train-derived folds, split-half stability, or another
  independent check. Treat extensive reuse as selection risk in the reflection.
- Test structural invariants and hard assumptions across the complete available
  labeled data, not only the promotion split, before enforcing them at inference.
- Record each meaningful run as one JSON object in `records/experiments.jsonl`:
  timestamp, candidate, hypothesis, validation, score, runtime, result,
  reflection, and next decision.
- Preserve the exact code that prod
</INSTRUCTIONS>
