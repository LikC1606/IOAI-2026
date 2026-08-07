"""Local exact-public and synthetic private-geometry probes for soft_belief."""
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "input" / "competition"
WORDS = json.loads((DATA / "vocabulary.json").read_text())
SECRETS = json.loads((DATA / "test_public.json").read_text())
WI = {w.casefold(): i for i, w in enumerate(WORDS)}
PUBLIC = np.load(DATA / "public_embeddings.npy").astype(np.float32)
PUBLIC /= np.linalg.norm(PUBLIC, axis=1, keepdims=True)


def load_player(path):
    os.environ["POTATO_DATA_DIR"] = str(DATA)
    spec = importlib.util.spec_from_file_location("potato_candidate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def play(mod, judge, secrets=SECRETS, seed=0, flip_noise=0.0):
    """Return score, solved count, turn list under a supplied judge matrix."""
    rng = np.random.default_rng(seed)
    player = mod.PotatoPlayer(WORDS, PUBLIC)
    scores, turns = [], []
    for secret in secrets:
        player.new_game()
        si = WI[secret.casefold()]
        sv = judge[si]
        word1, word2 = "lamp", "potato"
        found = None
        for turn in range(1, 31):
            i1, i2 = WI[word1.casefold()], WI[word2.casefold()]
            margin = float(sv @ judge[i1] - sv @ judge[i2])
            if flip_noise:
                # Independent comparison noise, useful for a non-transitive
                # stress test in addition to row-wise embedding perturbation.
                p_first = 1.0 / (1.0 + np.exp(-margin / flip_noise))
                first = bool(rng.random() < p_first)
            else:
                first = margin > 1e-12
            if abs(margin) <= 1e-12 and not flip_noise:
                verdict, winner = "same", word1
            elif first:
                verdict, winner = "first", word1
            else:
                verdict, winner = "second", word2
            proposal = player.respond({
                "turn": turn,
                "word1": word1,
                "word2": word2,
                "verdict": verdict,
                "winner_word": winner,
            })
            if proposal.casefold() == secret.casefold():
                found = turn
                break
            word1, word2 = winner, proposal
        turns.append(found)
        scores.append(0.0 if found is None else 1.0 - 0.02 * max(0, found - 10))
    return 100.0 * float(np.mean(scores)), sum(t is not None for t in turns), turns


def noisy_rows(sigma, seed):
    rng = np.random.default_rng(seed)
    x = PUBLIC + np.float32(sigma) * rng.normal(size=PUBLIC.shape).astype(np.float32)
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    return x


def mixed_rows(weight, seed):
    """Blend public vectors with independent row noise, then renormalize."""
    rng = np.random.default_rng(seed)
    z = rng.normal(size=PUBLIC.shape).astype(np.float32)
    z /= np.linalg.norm(z, axis=1, keepdims=True)
    x = np.float32(1.0 - weight) * PUBLIC + np.float32(weight) * z
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    return x


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("soft_belief.py")
    mod = load_player(path)
    cases = [("public", PUBLIC)]
    for sig in (0.005, 0.01, 0.02, 0.03, 0.05, 0.10):
        cases.append((f"rownoise{sig:g}", noisy_rows(sig, 17)))
    for w in (0.05, 0.10, 0.20, 0.40):
        cases.append((f"mix{w:g}", mixed_rows(w, 17)))
    for label, judge in cases:
        start = time.perf_counter()
        score, solved, turns = play(mod, judge, seed=123)
        elapsed = time.perf_counter() - start
        print(f"{label:12s} score={score:7.3f} solved={solved:3d}/120 "
              f"mean_turn={np.mean([t for t in turns if t]):.2f} "
              f"runtime={elapsed:.3f}s")
    # A fixed stochastic-comparison run makes robustness to isolated flips
    # visible without changing the candidate's public matrix.
    for noise in (0.005, 0.01, 0.02, 0.04):
        score, solved, turns = play(mod, PUBLIC, seed=123, flip_noise=noise)
        print(f"flip{noise:g}: score={score:.3f} solved={solved}/120 "
              f"mean_turn={np.mean([t for t in turns if t]):.2f}")


if __name__ == "__main__":
    main()
