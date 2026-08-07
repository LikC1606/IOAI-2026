"""Exact-public and controlled private-space-shift probe for query balance.

Run from the project root with ``python candidates/lane_query_balance/evaluate.py``.
The diagonal perturbation rescales embedding coordinates, preserving the legal
data boundary while changing comparison order in a controlled way.
"""

import json
from pathlib import Path

import numpy as np

from query_balance import BalancedPolicy, GreedyPolicy, evaluate


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "input" / "competition"


def load():
    words = json.loads((DATA / "vocabulary.json").read_text())
    emb = np.load(DATA / "public_embeddings.npy").astype(np.float32, copy=False)
    emb /= np.linalg.norm(emb, axis=1, keepdims=True)
    wi = {word.casefold(): i for i, word in enumerate(words)}
    secrets = [wi[word.casefold()] for word in json.loads((DATA / "test_public.json").read_text())]
    return words, emb, wi, np.asarray(secrets, dtype=np.intp)


def run():
    words, emb, wi, secrets = load()
    public_sim = emb @ emb.T
    lamp, potato = wi["lamp"], wi["potato"]
    print("policy,shift,score,solved,median_turn")

    # Exact public practice is the contract/sanity check.
    for name, factory in (
        ("greedy", lambda s: GreedyPolicy(s)),
        ("balanced", lambda s: BalancedPolicy(s, alpha=0.3)),
    ):
        score, solved, turns = evaluate(factory, secrets, public_sim, public_sim, lamp, potato)
        finite = [t for t in turns if t is not None]
        print(f"{name},exact,{score:.3f},{solved},{np.median(finite):.1f}")

    # Use held-out vocabulary words for shift tests, so the public practice
    # list does not determine the conclusion.  Three fixed seeds give a small
    # stability check without pretending to estimate the private leaderboard.
    practice = set(secrets.tolist())
    heldout = np.asarray([i for i in range(len(words)) if i not in practice], dtype=np.intp)
    heldout = heldout[np.random.default_rng(2026).choice(len(heldout), 480, replace=False)]
    for level in (0.05, 0.10, 0.20, 0.35):
        rows = {"greedy": [], "balanced": []}
        for seed in range(3):
            rng = np.random.default_rng(1000 + seed)
            scale = np.exp(level * rng.standard_normal(emb.shape[1])).astype(np.float32)
            shifted = emb * scale
            shifted /= np.linalg.norm(shifted, axis=1, keepdims=True)
            judge_sim = shifted @ shifted.T
            for name, factory in (
                ("greedy", lambda s: GreedyPolicy(s)),
                ("balanced", lambda s: BalancedPolicy(s, alpha=0.3)),
            ):
                score, solved, _ = evaluate(factory, heldout, public_sim, judge_sim, lamp, potato)
                rows[name].append((score, solved))
        g = np.asarray(rows["greedy"], dtype=float)
        b = np.asarray(rows["balanced"], dtype=float)
        print(
            f"both,diag{level:.2f},greedy={g[:, 0].mean():.3f}/"
            f"{g[:, 1].mean():.1f},balanced={b[:, 0].mean():.3f}/"
            f"{b[:, 1].mean():.1f},delta={b[:, 0].mean() - g[:, 0].mean():+.3f}"
        )


if __name__ == "__main__":
    run()
