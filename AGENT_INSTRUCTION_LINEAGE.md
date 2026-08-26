# Agent instruction lineage for Tasks 1–6

There is no single `AGENT.md` file that was literally shared by all six timed
runs. Each run received a task-scoped startup payload, preserved as
`taskN/environment/AGENTS-ACTUALLY-INJECTED.md` and hash-bound in
[STARTUP_INSTRUCTION_INDEX.md](STARTUP_INSTRUCTION_INDEX.md). This distinction
matters because later project-file edits must not be mistaken for instructions
that were present when a run started.

| Tasks | Instruction family | Runtime evidence |
|---|---|---|
| 1–2 | Persistent platform-delivered solver system payload, with task identity and deadline injected separately | `task1/environment/AGENTS-ACTUALLY-INJECTED.md`, `task2/environment/AGENTS-ACTUALLY-INJECTED.md` |
| 3 | Formal-run autonomous solver `AGENTS.md` payload, including the Task 3 project identity and deadline | `task3/environment/AGENTS-ACTUALLY-INJECTED.md` |
| 4–6 | Primary autonomous IOAI Solver payload, including each task's identity, account, and run deadline | `task4/environment/AGENTS-ACTUALLY-INJECTED.md`, `task5/environment/AGENTS-ACTUALLY-INJECTED.md`, `task6/environment/AGENTS-ACTUALLY-INJECTED.md` |

Tasks 4–6 use the same instruction *family* and common workflow priorities, but
their injected files still contain different competition IDs, project roots,
deadlines, and task-specific state. Tasks 1–2 and the formal Task 3 run use a
different platform payload family. The six files in the table are the complete
runtime startup records published for this evidence package; unrelated parent
repository `AGENTS.md` files are intentionally not substituted for them.

For a quick integrity check, run:

```bash
python3 tools/build_autonomous_trace_material.py
python3 verify_repository.py
```

