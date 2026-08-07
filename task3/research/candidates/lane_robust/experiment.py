"""Cheap robustness screens for public/private embedding disagreement.

This file is intentionally self contained and only uses the competition data.
It compares the official hard half-space walk with soft/rank policies under
controlled synthetic judge spaces. It is a research artifact, not submission
source.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "input" / "competition"
WORDS = json.loads((DATA / "vocabulary.json").read_text())
WI = {w.casefold(): i for i, w in enumerate(WORDS)}
PUBLIC = np.load(DATA / "public_embeddings.npy").astype(np.float32)
PUBLIC /= np.linalg.norm(PUBLIC, axis=1, keepdims=True)
N = len(WORDS)


def logistic(z):
    z = np.clip(z, -20.0, 20.0)
    return 1.0 / (1.0 + np.exp(-z))


class HardWalk:
    """The official starter policy."""

    name = "hard"

    def __init__(self, emb):
        self.s = emb @ emb.T

    def new_game(self):
        self.alive = np.ones(N, dtype=bool)
        self.used = np.zeros(N, dtype=bool)

    def respond(self, msg):
        i1, i2 = WI[msg["word1"]], WI[msg["word2"]]
        verdict = msg["verdict"]
        if verdict in ("first", "second"):
            better, worse = (i1, i2) if verdict == "first" else (i2, i1)
            self.alive &= self.s[better] >= self.s[worse]
        self.alive[self.used] = False
        if not self.alive.any():
            self.alive[:] = True
            self.alive[self.used] = False
        c = WI[msg["winner_word"]]
        avail = np.flatnonzero(self.alive)
        pick = int(avail[np.argmax(self.s[c, avail])])
        self.used[pick] = True
        return WORDS[pick]


class SoftBelief:
    """Posterior update with a noisy public-order likelihood.

    Temperature controls how quickly a public margin becomes a vote and
    reliability mixes that vote with an uninformative 50/50 comparison.
    Champion weight retains the starter's local-neighbor bias.
    """

    def __init__(
        self,
        emb,
        temperature=0.03,
        reliability=0.65,
        champion_weight=3.0,
        rank_only=False,
        name=None,
    ):
        self.s = emb @ emb.T
        self.temperature = float(temperature)
        self.reliability = float(reliability)
        self.champion_weight = float(champion_weight)
        self.rank_only = bool(rank_only)
        self.name = name or (
            f"soft_t{temperature:g}_q{reliability:g}_a{champion_weight:g}"
        )

    def new_game(self):
        self.logp = np.zeros(N, dtype=np.float32)
        self.used = np.zeros(N, dtype=bool)

    def respond(self, msg):
        i1, i2 = WI[msg["word1"]], WI[msg["word2"]]
        verdict = msg["verdict"]
        if verdict in ("first", "second"):
            better, worse = (i1, i2) if verdict == "first" else (i2, i1)
            margin = self.s[:, better] - self.s[:, worse]
            if self.rank_only:
                # A bounded sign vote discards unstable margin magnitude.
                prob = np.where(
                    margin >= 0.0,
                    0.5 + 0.25 * self.reliability,
                    0.5 - 0.25 * self.reliability,
                )
            else:
                prob = logistic(margin / self.temperature)
                prob = self.reliability * prob + (1.0 - self.reliability) * 0.5
            self.logp += np.log(prob).astype(np.float32)
        self.logp[self.used] = -1.0e9
        c = WI[msg["winner_word"]]
        score = self.logp + self.champion_weight * self.s[c]
        score[self.used] = -1.0e9
        pick = int(np.argmax(score))
        self.used[pick] = True
        return WORDS[pick]


class BalancedBelief:
    """Soft posterior plus an information-seeking balanced query term."""

    name = "balanced"

    def __init__(
        self,
        emb,
        temperature=0.03,
        reliability=0.65,
        hit_weight=4.0,
        info_weight=0.15,
    ):
        self.s = emb @ emb.T
        self.temperature = float(temperature)
        self.reliability = float(reliability)
        self.hit_weight = float(hit_weight)
        self.info_weight = float(info_weight)

    def new_game(self):
        self.logp = np.zeros(N, dtype=np.float32)
        self.used = np.zeros(N, dtype=bool)

    def respond(self, msg):
        i1, i2 = WI[msg["word1"]], WI[msg["word2"]]
        verdict = msg["verdict"]
        if verdict in ("first", "second"):
            better, worse = (i1, i2) if verdict == "first" else (i2, i1)
            margin = self.s[:, better] - self.s[:, worse]
            prob = logistic(margin / self.temperature)
            prob = self.reliability * prob + (1.0 - self.reliability) * 0.5
            self.logp += np.log(prob).astype(np.float32)
        self.logp[self.used] = -1.0e9
        c = WI[msg["winner_word"]]
        avail = ~self.used
        lp = self.logp.copy()
        lp[~avail] = -1.0e9
        p = np.exp(lp - np.max(lp))
        p /= p.sum()
        # Restrict acquisition to plausible guesses so this remains lightweight.
        order = np.flatnonzero(avail)
        if order.size > 256:
            top = np.argpartition(lp[order], -256)[-256:]
            order = order[top]
        q = p @ logistic(
            (self.s[:, order] - self.s[:, c][..., None]) / self.temperature
        )
        info = 4.0 * q * (1.0 - q)
        score = self.hit_weight * p[order] + self.info_weight * info
        pick = int(order[np.argmax(score)])
        self.used[pick] = True
        return WORDS[pick]


class RankNeighbor:
    """Public-neighbor walk with bounded sign evidence and rank utility."""

    def __init__(self, emb, vote_weight=1.0, neighbor_weight=4.0, name=None):
        self.s = emb @ emb.T
        self.vote_weight = float(vote_weight)
        self.neighbor_weight = float(neighbor_weight)
        self.name = name or f"rank_v{vote_weight:g}_n{neighbor_weight:g}"

    def new_game(self):
        self.score = np.zeros(N, dtype=np.float32)
        self.used = np.zeros(N, dtype=bool)

    def respond(self, msg):
        i1, i2 = WI[msg["word1"]], WI[msg["word2"]]
        verdict = msg["verdict"]
        if verdict in ("first", "second"):
            better, worse = (i1, i2) if verdict == "first" else (i2, i1)
            self.score += self.vote_weight * np.sign(
                self.s[:, better] - self.s[:, worse]
            )
        self.score[self.used] = -1.0e9
        c = WI[msg["winner_word"]]
        rank = np.argsort(np.argsort(-self.s[c])).astype(np.float32) / N
        utility = self.score - self.neighbor_weight * rank
        utility[self.used] = -1.0e9
        pick = int(np.argmax(utility))
        self.used[pick] = True
        return WORDS[pick]


class FamilySmoothedBelief:
    """Smooth each comparison vote over a public nearest-neighbor family."""

    def __init__(
        self,
        emb,
        neighbors=12,
        family_mix=0.5,
        temperature=0.03,
        reliability=0.65,
        champion_weight=3.0,
        rank_only=True,
        name=None,
    ):
        self.s = emb @ emb.T
        self.neighbors = int(neighbors)
        self.family_mix = float(family_mix)
        self.temperature = float(temperature)
        self.reliability = float(reliability)
        self.champion_weight = float(champion_weight)
        self.rank_only = bool(rank_only)
        # Include self in the local family. Argpartition avoids sorting all 1602
        # entries and is deterministic for the supplied matrix.
        self.knn = np.argpartition(
            -self.s, self.neighbors - 1, axis=1
        )[:, : self.neighbors]
        self.name = name or (
            f"family_k{neighbors}_m{family_mix:g}_a{champion_weight:g}"
        )

    def new_game(self):
        self.logp = np.zeros(N, dtype=np.float32)
        self.used = np.zeros(N, dtype=bool)

    def respond(self, msg):
        i1, i2 = WI[msg["word1"]], WI[msg["word2"]]
        verdict = msg["verdict"]
        if verdict in ("first", "second"):
            better, worse = (i1, i2) if verdict == "first" else (i2, i1)
            raw = self.s[:, better] - self.s[:, worse]
            family = np.median(raw[self.knn], axis=1)
            margin = (1.0 - self.family_mix) * raw + self.family_mix * family
            if self.rank_only:
                prob = np.where(
                    margin >= 0.0,
                    0.5 + 0.25 * self.reliability,
                    0.5 - 0.25 * self.reliability,
                )
            else:
                prob = logistic(margin / self.temperature)
                prob = self.reliability * prob + (1.0 - self.reliability) * 0.5
            self.logp += np.log(prob).astype(np.float32)
        self.logp[self.used] = -1.0e9
        c = WI[msg["winner_word"]]
        score = self.logp + self.champion_weight * self.s[c]
        score[self.used] = -1.0e9
        pick = int(np.argmax(score))
        self.used[pick] = True
        return WORDS[pick]


def play(player, judge, secrets, seed=0, flip_prob=0.0):
    rng = np.random.default_rng(seed)
    vals, turns = [], []
    for secret in secrets:
        player.new_game()
        si = WI[secret]
        w1, w2 = "lamp", "potato"
        solved = None
        for turn in range(1, 31):
            i1, i2 = WI[w1], WI[w2]
            margin = float(judge[si] @ judge[i1] - judge[si] @ judge[i2])
            if flip_prob:
                first = (margin > 0) ^ (rng.random() < flip_prob)
                verdict, winner = ("first", w1) if first else ("second", w2)
            elif margin > 1e-12:
                verdict, winner = "first", w1
            elif margin < -1e-12:
                verdict, winner = "second", w2
            else:
                verdict, winner = "same", w1
            proposal = player.respond(
                {
                    "turn": turn,
                    "winner_word": winner,
                    "verdict": verdict,
                    "word1": w1,
                    "word2": w2,
                }
            )
            if proposal.casefold() == secret.casefold():
                solved = turn
                break
            w1, w2 = winner, proposal
        turns.append(solved)
        vals.append(
            0.0 if solved is None else 1.0 - 0.02 * max(0, solved - 10)
        )
    return 100.0 * float(np.mean(vals)), turns


def shifted(base, sigma, seed=0, mode="row_noise"):
    rng = np.random.default_rng(seed)
    if mode == "row_noise":
        out = base + float(sigma) * rng.standard_normal(base.shape).astype(np.float32)
    elif mode == "feature_scale":
        scale = np.exp(
            float(sigma) * rng.standard_normal(base.shape[1])
        ).astype(np.float32)
        out = base * scale
    elif mode == "low_rank":
        k = 16
        u = rng.standard_normal((base.shape[1], k)).astype(np.float32)
        coeff = rng.standard_normal((base.shape[0], k)).astype(np.float32)
        out = base + float(sigma) * (coeff @ u.T) / np.sqrt(base.shape[1])
    else:
        raise ValueError(mode)
    out /= np.linalg.norm(out, axis=1, keepdims=True)
    return out.astype(np.float32)


def summarize(label, factory, judge, secrets, seed=0, flip_prob=0.0):
    start = time.perf_counter()
    score, turns = play(
        factory(PUBLIC), judge, secrets, seed=seed, flip_prob=flip_prob
    )
    elapsed = time.perf_counter() - start
    solved = sum(x is not None for x in turns)
    median = (
        float(np.median([x for x in turns if x is not None]))
        if solved
        else None
    )
    print(
        f"{label:24s} score={score:7.3f} solved={solved:4d}/{len(secrets)} "
        f"median={median} sec={elapsed:.2f}"
    )
    return score, turns


if __name__ == "__main__":
    practice = json.loads((DATA / "test_public.json").read_text())
    factories = [
        ("hard", HardWalk),
        (
            "soft-top",
            lambda e: SoftBelief(e, .03, .65, 0.0, name="soft-top"),
        ),
        (
            "soft-neighbor",
            lambda e: SoftBelief(e, .03, .65, 3.0, name="soft-neighbor"),
        ),
        (
            "soft-rank",
            lambda e: SoftBelief(
                e, .03, .65, 3.0, rank_only=True, name="soft-rank"
            ),
        ),
        (
            "family-rank",
            lambda e: FamilySmoothedBelief(e, 12, .5, .03, .65, 3.0),
        ),
        ("balanced", lambda e: BalancedBelief(e, .03, .65, 4.0, .15)),
        ("rank-neighbor", lambda e: RankNeighbor(e, 1.0, 4.0)),
    ]
    print("PUBLIC PRACTICE")
    for label, factory in factories:
        summarize(label, factory, PUBLIC, practice)
    print("PUBLIC ALL WORDS")
    for label, factory in factories:
        summarize(label, factory, PUBLIC, WORDS)
    for mode in ("row_noise", "feature_scale", "low_rank"):
        for sigma in (.01, .03, .06):
            judge = shifted(PUBLIC, sigma, seed=17, mode=mode)
            print(f"SHIFT {mode} sigma={sigma}")
            for label, factory in factories:
                summarize(label, factory, judge, practice)
