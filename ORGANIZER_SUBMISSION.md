# Organizer submission — Tasks 1–6

This is the single entry point for every requested deliverable. The
machine-readable checklist is [`ORGANIZER_SUBMISSION.json`](ORGANIZER_SUBMISSION.json),
and `python3 verify_repository.py` validates the paths, hashes, score records,
trace coverage, model/cost fields, and extraction metadata.

| Organizer requirement | Status | Evidence |
|---|---|---|
| Execution traces for Tasks 1–6 | Complete | [`AUTONOMOUS_TRACE_MATERIAL.md`](AUTONOMOUS_TRACE_MATERIAL.md), [`AUTONOMOUS_TRACE_INDEX.json`](AUTONOMOUS_TRACE_INDEX.json) |
| Prompts and visible Agent outputs | Complete | Full payloads are in every indexed JSONL trace; prompt classes and hashes are in the index |
| Tool calls and tool outputs | Complete | Per-task and per-file counts cover `function_call`, `function_call_output`, `custom_tool_call`, and `custom_tool_call_output` |
| LLM(s) used | Complete | [`AUTONOMOUS_COSTS.json`](AUTONOMOUS_COSTS.json): `ioai_allowed` / `gpt-5.6-sol`; Tasks 1–4 `max`, Tasks 5–6 `xhigh` |
| Total API costs | Complete with explicit unavailable-USD status | Exact per-task tokens and total are provided; USD is `null` because no invoice or exact provider/model rate was captured |
| GPU compute/cost per task | Complete | Exact observed accelerator seconds/hours are provided; USD is `null` where no invoice/rate exists, and `0` where no GPU was allocated |
| Kaggle extraction results | Complete | [`KAGGLE_EXTRACTION_DELIVERY.json`](KAGGLE_EXTRACTION_DELIVERY.json), [`KAGGLE_EXTRACTION_SUMMARY.json`](KAGGLE_EXTRACTION_SUMMARY.json), and the linked Drive archive |
| Final submitted results matching Kaggle | Complete | [`FINAL_SUBMISSION_RESULTS.md`](FINAL_SUBMISSION_RESULTS.md) and six task-level `FINAL_ACCOUNT_RESULTS.json` files |

## Human-intervention-free trace scope

The organizer trace selection contains the observable prefix before the first
live human intervention for each task. It retains startup/organizer prompts,
inherited context, Agent-generated worker assignments, visible outputs, tool
calls, and tool outputs. The first excluded human prompt and its entire causal
suffix are not part of the selected material. Boundary records expose only
timestamp, classification, and cryptographic hashes; they do not reproduce the
human prompt bodies.

Hidden chain-of-thought and opaque encrypted reasoning are not published.
Credentials, private endpoints, and secret metadata are redacted. These
omissions do not remove observable prompts, Agent responses, or tool envelopes.

## Kaggle extraction archive

The complete organizer-requested extraction archive for account `researai` is
496,870,419 bytes and contains 1,401 archive entries. Its SHA-256 is
`eb14e52057c3cfca21972993fb73c2addaf9f214abc9c6f38b88bca97d93fe3c`.
It exceeds GitHub's single-file limit and is therefore delivered on Google
Drive:

<https://drive.google.com/file/d/1c9yRn5SUo6LOPDrHLrAVjj-9JLFti9Vz/view?usp=drivesdk>

## Verification

```bash
python3 tools/build_execution_trace_index.py
python3 tools/build_autonomous_trace_material.py
python3 verify_repository.py
sha256sum -c AUTONOMOUS_MATERIAL_MANIFEST.sha256
```

The USD cost fields deliberately remain `null` rather than pricing
`gpt-5.6-sol` with a different model's public rate or inventing a Kaggle GPU
invoice.
