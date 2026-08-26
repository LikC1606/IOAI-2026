# API and H100 server cost estimate

This page provides the requested numeric cost estimate for the selected
Task 1–6 execution-trace scope. It is a reproducible budget estimate, not a
provider invoice or a claim that the assumed H100 time equals measured local
runtime. Exact token vectors remain in [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json).

## Assumptions

The current OpenAI standard API prices used here are, per one million tokens:

| GPT-5.6 Sol token class | USD / 1M tokens |
|---|---:|
| Uncached input | $4.00 |
| Cached input | $0.40 |
| Cache write | $5.00 |
| Output, including reasoning tokens already contained in `output_tokens` | $20.00 |

Source: [OpenAI API pricing](https://platform.openai.com/docs/pricing). The
[GPT-5.6 release page](https://openai.com/index/gpt-5-6/) records the model's
pricing history and the 2026-08-21 temporary Sol price reduction. The trace
telemetry reports a 258,400-token model context window, below the published
long-context price threshold, so the standard row is used. No cache-write
charge occurs because all selected traces report zero cache-write tokens.

For server cost, the user requested the same assumption for every Task:

```text
2 H100 GPUs × 2 hours = 4 H100 GPU-hours per Task
```

Fourteen normalized public on-demand H100 rates surveyed on 2026-08-26 are
`$2.19, $2.89, $2.99, $3.19, $3.29, $3.85, $3.90, $3.95, $4.41, $5.36,
$5.95, $6.16, $6.88, $6.98` per GPU-hour. Their median is
`$3.925/GPU-hour`, producing `$15.70` per Task. The observed range would
produce `$8.76–$27.92` per Task and `$52.56–$167.52` across all six Tasks.
The primary comparison and cross-checks are:

- [Thunder Compute H100 price comparison](https://www.thundercompute.com/blog/nvidia-h100-pricing)
- [Lambda H100 price comparison](https://www.spheron.network/blog/lambda-cloud-h100-pricing-2026/)
- [RunPod/Lambda/Vast.ai comparison](https://tech-insider.org/runpod-vs-lambda-vs-vast-ai-2026/)
- [Vast.ai live pricing](https://vast.ai/pricing)

Prices vary with provider, region, storage, SLA, PCIe/SXM configuration, and
market availability. The median is therefore a transparent budgeting proxy,
not a historical bill.

## Task 1–6 estimate

The API formula is:

```text
(input - cached_input) / 1M × $4
+ cached_input / 1M × $0.40
+ cache_write_input / 1M × $5
+ output / 1M × $20
```

| Task | API estimate | H100 estimate (2 cards × 2 h) | Combined estimate |
|---|---:|---:|---:|
| Task 1 | $24.487053 | $15.70 | $40.187053 |
| Task 2 | $17.044876 | $15.70 | $32.744876 |
| Task 3 | $52.671526 | $15.70 | $68.371526 |
| Task 4 | $135.569914 | $15.70 | $151.269914 |
| Task 5 | $99.197706 | $15.70 | $114.897706 |
| Task 6 | $31.816745 | $15.70 | $47.516745 |
| **Total** | **$360.787820** | **$94.20** | **$454.987820** |

Task 1's main line uses the canonical reproduction prefix through
`task_complete`. For the separately retained full later Task 1 reproduction,
the API estimate is `$24.549085`; Task 2 remains `$17.044876`. The full
two-trace reproduction estimate is therefore `$41.593961` for API,
`$31.40` for the same H100 assumption, and `$72.993961` combined. See
[`REPRODUCTION_COSTS.json`](REPRODUCTION_COSTS.json).

## Interpretation

The numeric estimates above satisfy the requested cost calculation while
preserving the distinction between calculation and evidence:

- `api_cost_usd` and `gpu_cost_usd` remain `null` where no invoice exists;
- `api_cost_estimate_usd` applies official public token rates to exact counters;
- `h100_server_cost_estimate_usd` applies the explicit two-card/two-hour
  assumption to the surveyed median rate;
- observed Kaggle T4 runtimes remain separately recorded and are not added to
  the user-specified H100 server estimate.
