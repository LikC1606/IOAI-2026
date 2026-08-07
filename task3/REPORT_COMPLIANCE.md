# Historical Technical-Report Compliance

This audit compares the immutable report header in each exact submitted source
with the organizer's `Report Generation Prompt`. It does not modify history.

The official prompt asks for 8-10 short paragraphs covering: the search/update
strategy; proposal selection; use of public embeddings and response to private
space mismatch; local self-score and actual LB with a conclusion from the gap;
win-turn distribution; 600-second/precomputation use; and rejected alternatives.
It also says to discuss the solution rather than the agent/harness/prompt.

| Version | Logical report paragraphs | Search and proposal | Public/private treatment | Local score | Own actual LB | Win-turn distribution | 600s/precompute | Rejected routes |
|---:|---:|---|---|---|---|---|---|---|
| v1 | 5 | Yes | Yes | Yes | No: pending at submission | Yes | Yes | Yes |
| v2 | 6 | Yes | Yes | Partly: promised after validation | No | No | Yes | Yes |
| v3 | 6 | Yes | Yes | Partly: promised after validation | No | No | Yes | Yes |
| v4 | 6 | Yes | Yes | Yes | No: score was not yet known in source | No | Yes | Yes |
| v5 | 6 | Yes | Yes | Yes | No: only earlier LB values | No | Yes | Yes |
| v6 | 6 | Yes | Yes | Yes | No: reports v4 LB, not v6 LB | No | Yes | Yes |
| v7 | 6 | Yes | Yes | Yes | No: reports v4 LB, not v7 LB | No | Yes | Yes |
| v8 | 6 | Yes | Yes | Stated, but see discrepancy below | Yes: 58.51666 | No | Yes | Yes |

All headers are at the top of the source, above imports; all describe the solution
rather than the agentic system. Their largest systematic deficiency is length:
none reaches the requested 8-10 paragraphs. v2-v7 also omit the candidate's own
actual LB because the exact source necessarily existed before its score returned.
This temporal conflict is not resolved by changing the historical payload.

v8 is the strongest reporting anchor because it includes the actual 58.51666 LB
and explains the public/private gap, ablation, search, dependencies, and runtime.
However, it omits the requested win-turn distribution. More importantly, its
header says “This softened version scores 98.63 locally,” while the exact v8
payload currently reproduces at **96.62** on the included official data. The
98.63 figure is the v4 result and appears to have been carried into the v8 report.
The exact v8 code, remote CSV, and LB remain verified; this is a report-value
error and is disclosed here.

The organizer pages are internally nuanced: the Submission page calls the report
a requirement, while the Report page says each source “should carry” it and that
it “carries no score.” This package makes no legal conclusion about materiality.
It preserves the exact source and gives the Jury the facts needed to decide.

A corrected supplementary explanation may be supplied alongside an appeal or
audit, but it must never be substituted for `solutions/vN.py` or represented as
the source that generated the historical Submission.
