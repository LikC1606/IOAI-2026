"""Retained-champion query policies for the Potato Contact task.

This lane deliberately keeps the starter's public half-space belief update and
changes only acquisition.  ``GreedyPolicy`` is the starter policy.  The
balanced policy chooses a legal proposal whose public comparison against the
current champion gives the most even split over surviving secret candidates,
with a small champion-similarity tie-break.  The judge still compares the
proposal with the retained champion, so this does not change the protocol.
"""

from __future__ import annotations

import numpy as np


class GreedyPolicy:
    """Official starter acquisition rule (for an apples-to-apples baseline)."""

    def __init__(self, similarity: np.ndarray):
        self.similarity = similarity
        self.n = similarity.shape[0]

    def new_game(self):
        self.mask = np.ones(self.n, dtype=bool)
        self.proposed = set()

    def choose(self, champion: int, previous: int, winner: int, verdict: str) -> int:
        if verdict in ("first", "second"):
            better, worse = (
                (champion, previous) if verdict == "first" else (previous, champion)
            )
            self.mask &= self.similarity[better] >= self.similarity[worse]
        if self.proposed:
            self.mask[np.fromiter(self.proposed, dtype=np.intp)] = False
        if not self.mask.any():
            self.mask[:] = True
            if self.proposed:
                self.mask[np.fromiter(self.proposed, dtype=np.intp)] = False
        alive = np.flatnonzero(self.mask)
        return int(alive[np.argmax(self.similarity[winner, alive])])


class BalancedPolicy(GreedyPolicy):
    """Public partition-balance acquisition with a champion-local tie-break.

    For each legal query q, estimate the public probability that q beats the
    current champion over the surviving candidate secrets.  Binary entropy is
    maximal near a 50/50 partition.  ``alpha`` preserves the useful tendency
    to guess words close to the retained champion when several queries have
    comparable information gain.
    """

    def __init__(self, similarity: np.ndarray, alpha: float = 0.3):
        super().__init__(similarity)
        self.alpha = float(alpha)

    def choose(self, champion: int, previous: int, winner: int, verdict: str) -> int:
        if verdict in ("first", "second"):
            better, worse = (
                (champion, previous) if verdict == "first" else (previous, champion)
            )
            self.mask &= self.similarity[better] >= self.similarity[worse]
        if self.proposed:
            self.mask[np.fromiter(self.proposed, dtype=np.intp)] = False
        if not self.mask.any():
            self.mask[:] = True
            if self.proposed:
                self.mask[np.fromiter(self.proposed, dtype=np.intp)] = False

        # Queries are restricted to surviving, unproposed vocabulary words.
        # Keep the starter's opening-word behavior: a champion may be proposed
        # on turn one, which preserves correctness if an opening word is ever
        # used as a hidden secret.  The comparison is still always against the
        # retained champion supplied to this method.
        alive = np.flatnonzero(self.mask)
        if self.proposed:
            proposed = np.fromiter(self.proposed, dtype=np.intp)
            alive = alive[~np.isin(alive, proposed)]
        if alive.size == 0:
            alive = np.flatnonzero(self.mask)
            if self.proposed:
                proposed = np.fromiter(self.proposed, dtype=np.intp)
                alive = alive[~np.isin(alive, proposed)]

        # ``outcome[s, q]`` is the public prediction for q beating champion
        # when s is the hidden word.  Mean over candidate secrets gives the
        # predicted branch mass for each query.
        outcome = self.similarity[np.ix_(alive, alive)] > self.similarity[alive, champion, None]
        p = outcome.mean(axis=0)
        p = np.clip(p, 1e-6, 1.0 - 1e-6)
        entropy = -(p * np.log2(p) + (1.0 - p) * np.log2(1.0 - p))
        score = entropy + self.alpha * self.similarity[winner, alive]
        return int(alive[np.argmax(score)])


def play(policy, secret: int, judge_similarity: np.ndarray, lamp: int, potato: int, turns: int = 30):
    """Play one hidden-secret game and return (discounted score, win turn)."""
    policy.new_game()
    champion, previous = lamp, potato
    for turn in range(1, turns + 1):
        margin = float(judge_similarity[secret, champion] - judge_similarity[secret, previous])
        if abs(margin) <= 1e-12:
            winner, verdict = champion, "same"
        elif margin > 0:
            winner, verdict = champion, "first"
        else:
            winner, verdict = previous, "second"
        proposal = policy.choose(champion, previous, winner, verdict)
        if proposal == secret:
            return 1.0 - 0.02 * max(0, turn - 10), turn
        policy.proposed.add(proposal)
        champion, previous = winner, proposal
    return 0.0, None


def evaluate(policy_factory, secrets, public_similarity, judge_similarity, lamp, potato):
    policy = policy_factory(public_similarity)
    result = [play(policy, int(secret), judge_similarity, lamp, potato) for secret in secrets]
    scores, turns = zip(*result)
    return 100.0 * float(np.mean(scores)), sum(t is not None for t in turns), turns
