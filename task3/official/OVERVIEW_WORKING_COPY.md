# Official Overview

Source: authenticated Kaggle competition pages for
`ioai-2026-task-3-westlake-nlp-48`, accessed 2026-08-06 12:39 CST with
`kaggle competitions pages`.

## Description

The judge selects one hidden word from a fixed vocabulary of 1,602 words. Each
game begins with `lamp` versus `potato`. The judge reports which word is closer
to the hidden word, retains that winner, and compares it with the player's next
proposal. The player wins by proposing the hidden word within 30 turns.

The supplied 2,560-dimensional embeddings are public competition data. Every
official comparison is made in a different, unavailable private embedding
space, so public self-score is an upper bound and robustness to comparison-space
disagreement is the core challenge.

## Data

- `vocabulary.json`: 1,602 unique lowercase legal proposals.
- `public_embeddings.npy`: normalized-on-load `float32` matrix `(1602, 2560)`;
  row order matches the vocabulary.
- `test_public.json`: 120 labelled public-practice secrets.
- `ioai-starter.py`: required contract, loader, evaluator, and base64 envelope.
- `potato_doc.md`: official guide.

The public practice, `leaderboard-a`, and `leaderboard-b` each contain 120
disjoint vocabulary words. There is no labelled training split. The grader sets
`POTATO_DATA_DIR`; the starter's data search must remain intact.

## Evaluation

The grader imports the source and calls `load_public_data()` once per round,
constructs `PotatoPlayer(words, embeddings)` once per round, calls `new_game()`
before each game, and calls `respond(message)` for turns 1 through 30. A response
must return a vocabulary string. Interface errors, invalid words, or exceptions
fail the current and all remaining games in the round.

A win on turn `t` scores `1 - 0.02 * max(0, t - 10)`; an unsolved game scores
zero. The official score is 100 times the mean over 120 games. One round has a
single 600-second CPU budget covering imports, precomputation, and all games.

## Legal Resources

Only competition data and ordinary libraries without external data or pretrained
resources are allowed. No external embeddings, models, APIs, datasets, attached
datasets, Internet, or private-asset reconstruction. The notebook is private,
offline, CPU-only, and only creates the transport CSV. Teams are forbidden.

## Submission Contract

`submission.csv` has exactly columns `id,program_b64` and exactly rows
`leaderboard-a` and `leaderboard-b`, both containing the same source payload.
The source limit is 512 KB. The official starter's loader, contract check, and
Kaggle block stay unchanged; only the `PotatoPlayer` class body is edited.

Every submitted solution carries an 8-10 paragraph technical report in a comment
block above imports. It describes the implemented search, public/private gap,
public and actual LB scores, win-turn distribution, precomputation/runtime, and
discarded approaches. The report itself is unscored.
