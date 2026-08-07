# Autonomy Boundary

## Rule

The positive claim ends when the controlling session first receives a material
instruction about method, priority, optimization, submission policy, resource
use, restart, or document rereading. This is stricter than waiting until that
instruction is relayed to the formal solver. Read-only status inspection and
verbatim organizer Starter/Continuation Prompts do not by themselves alter the
solver's technical decisions.

## Task 1 boundary

The exclusive boundary is `2026-08-05T10:16:52.222Z`. At that time the
controller received:

> 你让他继续优化 找到高分了再提交

The exact event is in `evidence/SUPERVISION_BOUNDARY_EVENT.json`. The private
controller rollout is not distributed because it includes unrelated tasks and
private transport material; its SHA-256 is recorded in
`ROLLOUT_PROVENANCE.json`.

Earlier controller interactions were treated as non-method control:

- 09:31:42: scope/status instruction to inspect only the registered account.
- 10:03:22: restatement that submission must follow the official Overview CLI.
- 10:14:55: request to continue, followed by the official Continuation Prompt.
- 10:15:43: question about why the baseline was uploaded.

The official Continuation Prompt reached the solver at 10:17:36, already after
the conservative external boundary, so it is not included in the positive
rollout even though its text was organizer-authorized.

## Correction to the earlier boundary description

An earlier informal account used `2026-08-05T10:24:03.008Z`, when a custom
target-score instruction reached the solver. That boundary was too permissive.
This package instead uses the earlier controller-arrival boundary at 10:16:52.
No result from the intervening interval is promoted into the positive claim.

Every event distributed in the positive formal rollout has a timestamp strictly
earlier than the boundary. Its only solver-role user inputs are the injected
startup `AGENTS.md` envelope and the exact organizer Starter Prompt.

The separate `evidence/submission-execution/` trace retains the later supervised
Agent activity. It supports the claim that submission `55267607` was executed
by the Agent, while keeping that attribution distinct from the narrower
official-prompt-only autonomy window.
