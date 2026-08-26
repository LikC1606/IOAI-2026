# Startup instruction index

This index identifies the `AGENTS.md` payload actually injected at the start
of each preserved Task 1–6 run. These files are runtime evidence, not a claim
that later edits to a project instruction file were present at startup. Each
file is included in its Task package manifest and is linked from the trace
records where the corresponding user-role startup envelope appears.

The machine-readable binding is [`STARTUP_INSTRUCTION_INDEX.json`](STARTUP_INSTRUCTION_INDEX.json).

| Task | Competition | Injected startup payload | Bytes | SHA-256 |
|---|---|---|---:|---|
| 1 | `ioai-2026-task-1-westlake-nlp-24` | [`AGENTS-ACTUALLY-INJECTED.md`](task1/environment/AGENTS-ACTUALLY-INJECTED.md) | 15,697 | `ce4bfa8a2339ad84ced241df576b307fadd763180b34b3a3fe65a3551fa6ad98` |
| 2 | `ioai-2026-task-2-westlake-nlp-24` | [`AGENTS-ACTUALLY-INJECTED.md`](task2/environment/AGENTS-ACTUALLY-INJECTED.md) | 15,740 | `9d4f1918cb840bd0620be0243bd35e46fe894ae3220a7ec194f15c3c6080e417` |
| 3 | `ioai-2026-task-3-westlake-nlp-48` | [`AGENTS-ACTUALLY-INJECTED.md`](task3/environment/AGENTS-ACTUALLY-INJECTED.md) | 32,951 | `2bf4a713178b0f6d0d707575fe22d16d15ea640f580abd60f672a935476b8f84` |
| 4 | `ioai-2026-task-4-westlake-nlp-24` | [`AGENTS-ACTUALLY-INJECTED.md`](task4/environment/AGENTS-ACTUALLY-INJECTED.md) | 26,191 | `8e0b9851cb90a9e95385ce629acbbb28760c93f3c3abcbd439ca140138dcda48` |
| 5 | `ioai-2026-task-5-westlake-nlp-24` | [`AGENTS-ACTUALLY-INJECTED.md`](task5/environment/AGENTS-ACTUALLY-INJECTED.md) | 28,929 | `42b34f4925e4cde8c6b311e3c56f0437fdc8f5f14e2bdcdf8bef9ce5f1edf5dc` |
| 6 | `ioai-2026-task-6-westlake-nlp-60` | [`AGENTS-ACTUALLY-INJECTED.md`](task6/environment/AGENTS-ACTUALLY-INJECTED.md) | 28,945 | `020fc980f4a6c5195014dd08ab265c30021da52c8730fd5cf0f66177e50a41f6` |

The payloads are credential-redacted exports. The selected JSONL traces remain
the authoritative event-level evidence for when each startup envelope was
delivered and for the subsequent autonomy boundary. This index does not add
the unrelated parent-repository `AGENTS.md`; it records only the six
task-runtime payloads that were injected into the preserved runs.

Verify the files through the six Task manifests and the root repository
verifier:

```bash
for t in 1 2 3 4 5 6; do (cd task$t && sha256sum -c MANIFEST.sha256); done
python3 verify_repository.py
```
