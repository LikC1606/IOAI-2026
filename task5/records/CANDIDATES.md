# Candidate Routes

## Breakthrough Objective

Produce a verified legal notebook that materially beats the official mean-fraction baseline (28.60 Public / 32.68 Private) by locating a passage-specific structural/style change. No calibrated hidden estimate exists yet; observable success is stable full-dev and both-half improvement with acceptable T4 runtime.

## Deployable Frontier

- Incumbent: remote-complete/submitted version 1, official mean-fraction baseline. Local dev 28.5655, Public 28.60, CPU runtime 63.5 seconds including setup, exact notebook output validated. Kernel: `researai/ioai-2026-ghost-of-the-machine-solution`.
- Incumbent replacement: submitted remote version 2, structural + classical TF-IDF local-transition decoder. Full dev 94.615, Public 90.86, confirmation 92.866, deterministic dev halves 93.848/95.552, remote CPU runtime 114.8 seconds. Preserve while rebuilding the evaluation boundary around the dev/Public gap.
- Current incumbent: submitted version 6 all-label fine-tuned local-BGE sequence. Public 95.39, runtime 289.3 seconds, 5.00GB T4 VRAM, and exact remote output/deployment checks passed. It changed 9/760 remote predictions versus version 5 and gained +0.83 Public. Version 5 (94.56 Public) remains preserved.

## Scientific Frontier

| Route | Family | Changed causal stage / clue | Assumption and cheapest test | Time / remote path | Status |
|---|---|---|---|---|---|
| Structural + classical seam ranker | mechanism-distinct representation | Lossless sentence candidates plus local origin transition and first-machine-sentence score. | 94.615 dev, 92.866 confirmation, 90.86 Public; transfers strongly but dev optimistic by 3.755. | 114.8s remote CPU. | Deployable incumbent version 2. |
| Frozen bge window change-point | mechanism-distinct representation | Semantic/style embedding sequence rather than surface-only features. | Supported but lower: 86.822 dev; grouped-CV mean/worst 87.244/85.305. | Estimated <250s one T4 including setup. | Verified fallback; do not promote over classical. |
| Prefix/suffix sequence likelihood | mechanism-distinct core paradigm | Enforces exactly one human prefix and one machine suffix rather than local-only argmax. | Remote dev 93.563 / Public 92.48; held-out folds 93.02/94.37/92.67. | 96.0s remote CPU. | Deployable incumbent version 3. |
| All-label sequence refit | information-use expansion | Same selected decoder, refit on 1,221 train + 380 official dev labels after honest selection. | Public 92.73, +0.25 over v3; additional coverage transferred. | 115.3s remote CPU. | Deployable incumbent version 4. |
| Fine-tuned local BGE emissions | mechanism-distinct learned representation | Full adaptation of the only permitted encoder on sentence origins, then one-transition decode with 180-word feasibility. | Holdout 94.557 vs paired lexical 94.324; remote dev/Public 95.688/94.56. | 244.4s remote one T4, 5.00GB. | Deployable incumbent version 5. |
| All-label fine-tuned BGE refit | information-use expansion | Same v5 model/seed/epoch/decoder refit on all 1,601 official labels. | Version 6 Public 95.39, +0.83 over v5 from 9 changed remote rows; in-sample dev is not selection evidence. | 289.3s remote one T4, 5.00GB. | Deployable incumbent version 6; preserve v5. |
| Neural local-transition decoder | mechanism-distinct task decomposition | Scores the adjacent right-minus-left BGE origin jump instead of cumulative suffix state. | Holdout/dev improved +1.483/+1.086, but version 7 Public 94.17, -1.22 versus v6. | 291.8s remote one T4, 5.00GB. | Hidden transfer falsified; retired. |
| Mean boundary fraction | same-family sanity baseline | Global target prior from official starter. | 28.5655 dev / 28.60 Public; interface only. | 63.5s remote CPU including setup. | Deployable incumbent version 1. |

## Selection Gate

A scientific route becomes deployable only after exact full-dev scoring, output/range checks, runtime/scale estimate including offline install, and code derived from the tested candidate. Diagnostic or locally accelerated artifacts are not submission candidates unless their training/inference is reproduced inside the notebook from competition inputs.

## Retired Routes And Lessons

- Direct frozen-bge local boundary ranker: 81.315 dev, dominated by bge sequence emissions.
- Standalone first-machine-sentence onset classifier: about 64.5, insufficient without sequence/state evidence.
- Direct left/right pair-seam classifier: 89.483 dev and 91.976 late-id confirmation; dominated by cumulative/local state routes.
- BGE fallback fusion: train OOF selects zero replacements; falsified.
- Train-only classical fraction cap: OOF -0.412 and dev -0.822; falsified.
- Classical-to-sequence confidence fallback: all train OOF folds improve, but untouched dev falls 0.158 and one half falls 0.584; confirmation-unstable, so do not submit as a fusion.
- Multi-sentence contextual emissions: held-out mean/worst 87.762/85.829 and dev 90.356; context blurs states under cumulative decoding.
- Multinomial/Bernoulli NB emissions: held-out means 91.949/91.238 and dev about 90.5; heavier tails and dominated by linear sequence.
