"""Compare starter and soft belief on structured synthetic private spaces."""
import importlib.util
import os
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    data = ROOT / "input" / "competition"
    os.environ["POTATO_DATA_DIR"] = str(data)
    p = load("probe", ROOT / "candidates/lane_soft/probe.py")
    base = load("base", ROOT / "candidates/deployable_baseline/starter.py")
    soft = load("soft", ROOT / "candidates/lane_soft/soft_belief.py")
    rng = np.random.default_rng(7)
    e = p.PUBLIC
    cases = [("public", e)]
    for sigma in (0.005, 0.01, 0.02):
        for seed in (3, 17):
            cases.append((f"noise{sigma:g}s{seed}", p.noisy_rows(sigma, seed)))
    for sigma in (0.1, 0.3, 0.6, 1.0):
        scales = np.exp(np.float32(sigma) * rng.normal(size=e.shape[1])).astype(np.float32)
        x = e * scales[None, :]
        x /= np.linalg.norm(x, axis=1, keepdims=True)
        cases.append((f"anis{sigma:g}", x))
    for drop in (0.1, 0.3, 0.5):
        keep = rng.random(e.shape[1]) >= drop
        x = e * keep[None, :]
        x /= np.linalg.norm(x, axis=1, keepdims=True)
        cases.append((f"drop{drop:g}", x))
    # Independent random row vectors interpolate from semantic to chance.
    z = rng.normal(size=e.shape).astype(np.float32)
    z /= np.linalg.norm(z, axis=1, keepdims=True)
    for w in (0.1, 0.2, 0.4):
        x = np.float32(1.0 - w) * e + np.float32(w) * z
        x /= np.linalg.norm(x, axis=1, keepdims=True)
        cases.append((f"randmix{w:g}", x))

    os.environ.update(POTATO_SOFT_TAU="0.003", POTATO_SOFT_FLIP="0.05",
                      POTATO_SOFT_ALPHA="1", POTATO_SOFT_CHAMP="2",
                      POTATO_SOFT_INFO="2", POTATO_SOFT_TOPK="128")
    for label, judge in cases:
        st = time.perf_counter()
        bscore, bsolved, _ = p.play(base, judge, seed=123)
        sscore, ssolved, _ = p.play(soft, judge, seed=123)
        print(f"{label:14s} base={bscore:7.2f} ({bsolved:3d}) soft={sscore:7.2f} ({ssolved:3d}) "
              f"delta={sscore-bscore:+6.2f} sec={time.perf_counter()-st:.2f}", flush=True)


if __name__ == "__main__":
    main()
