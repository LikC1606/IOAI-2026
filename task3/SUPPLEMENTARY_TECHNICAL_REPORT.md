# Supplementary Technical Report for Version 8

This document is a post-run explanation of the exact immutable source in
`solutions/v8.py`. It is not represented as the comment header that accompanied
submission `55289823`, and it does not replace or alter that historical source.
The nine paragraphs below supply the requested technical detail and correct the
local-score value in the original header.

1. The solution treats Potato Contact as sequential noisy preference search
over all 1,602 legal words. Each judge verdict says which of two words is closer
to the hidden word, so the player maintains a log belief for every possible
secret and updates that belief after every comparison.

2. At initialization, the player normalizes the organizer-supplied public
embeddings and precomputes their full 1,602 by 1,602 cosine-similarity matrix.
Version 8 deliberately resets its initial log prior to uniform, making it an
ablation of the practice-secret centroid used by an earlier version.

3. For a verdict, the code compares each candidate's public similarity to the
two judged words. It converts the signed margin into a logistic probability at
temperature `0.01`, then mixes in a 20 percent symmetric mismatch component.
The resulting log likelihood changes the belief without permanently eliminating
a word after one apparently inconsistent comparison.

4. The soft update addresses the central distribution shift: the public and
private judges use different embedding spaces. Public geometry is therefore a
useful but fallible ranking signal, rather than a hard constraint. This choice
was supported by the large transfer failure of the hard starter and by the
leaderboard gains of the softened posterior variants.

5. The next proposal is selected from the 128 highest-belief unproposed words.
Its acquisition score combines posterior belief, similarity to the current
winning word, and the expected entropy of the next binary comparison. Proposed
words are excluded from the information calculation because reaching another
turn already proves that an earlier proposal was not the secret.

6. One `PotatoPlayer` instance is reused across all 120 games. When a game ends
before turn 30, the last proposal is recorded as solved and excluded from later
games, using the task's guarantee that round secrets are distinct. Per-game
belief and proposal state are reset in `new_game()`, while the similarity matrix
and solved-word set remain available across the round.

7. Reproduction of the exact v8 source on `test_public.json` gives **96.62**
(`96.6167` before rounding), with all 120 games solved. Its Public Leaderboard
score was **58.51666**, a gap of about 38.10 points. The gap confirms that high
public-space self-score is primarily a contract and sanity check; robustness to
embedding-space mismatch, not additional public-score tuning, controls transfer.

8. The reproduced public win-turn distribution is: turns 1-10, **65 games**;
turns 11-20, **53 games**; turns 21-30, **2 games**; unsolved, **0 games**. The
mean winning turn is `10.4583`. The exact per-turn counts are `2:2, 3:1, 4:1,
5:4, 6:8, 7:8, 8:15, 9:13, 10:13, 11:10, 12:15, 13:6, 14:6, 15:6, 16:7,
17:2, 19:1, 23:2`.

9. The one-time matrix multiplication dominates precomputation; later work is
vectorized NumPy over the full belief and a 128-word shortlist. The preserved
reproduction completed the 120 public games in about `1.523` seconds, far below
the 600-second grader budget. Hard half-space filtering was dropped because it
was brittle under private-space shift, while practice-prior penalties, online
calibration, and alternative softened mixtures did not beat the final robust
likelihood route on the observed leaderboard.

## Historical-report correction

The submitted v8 header says `98.63` locally. Mechanical reproduction of its
exact decoded payload gives `96.62`; `98.63` belongs to v4 and was carried into
the v8 prose by mistake. The original header also has six logical paragraphs
rather than the requested 8-10 and omits the win-turn distribution. Those are
documentation defects only: source identity, remote output identity, executable
contract, submission ID, and Public Leaderboard score remain independently
verified.
