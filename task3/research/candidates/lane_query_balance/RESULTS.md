# Query Balance Probe

Hypothesis: with the starter's hard public half-space belief held fixed,
proposal selection by predicted public partition entropy plus a small
champion-similarity term beats greedy nearest-champion selection and degrades
more gracefully under a coherent private-space shift.

Run:

```bash
python candidates/lane_query_balance/evaluate.py
```

Exact `test_public.json` result:

| Policy | Score | Solved | Median turn |
|---|---:|---:|---:|
| Starter greedy | 92.583 | 119/120 | 10 |
| Balance, alpha=0.3 | 98.867 | 120/120 | 9 |

The same exact-public simulation over all 1,602 vocabulary secrets scored
91.237 (1,589 solved) for greedy and 98.593 (1,602 solved) for balance.  The
balanced 120-game run took 0.581 seconds after pairwise similarity construction;
the 1,602-game run took 6.791 seconds.

Synthetic shift uses 480 fixed vocabulary secrets disjoint from the public
practice list, three perturbation seeds, and log-normal diagonal rescaling of
the public embedding coordinates before judge comparisons:

| Shift sigma | Greedy score / solved | Balance score / solved | Delta |
|---:|---:|---:|---:|
| 0.05 | 88.461 / 464.7 | 95.996 / 477.7 | +7.535 |
| 0.10 | 85.549 / 454.0 | 92.978 / 471.3 | +7.429 |
| 0.20 | 80.147 / 433.0 | 87.488 / 457.3 | +7.340 |
| 0.35 | 72.186 / 397.3 | 77.424 / 419.3 | +5.237 |

An independent row-noise check on 240 held-out words and two seeds also favored
balance at sigma 0.002, 0.005, and 0.01 by +8.44, +7.69, and +5.86 points.  It
reversed at sigma 0.02 (28.00 balance versus 30.69 greedy) and both policies
collapsed near 4.8 at sigma 0.05.  Thus the acquisition result is strong while
public semantic structure remains informative; it does not repair the starter's
irreversible hard filtering under a severely decorrelated judge.
