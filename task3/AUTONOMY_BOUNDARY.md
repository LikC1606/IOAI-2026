# Autonomy Boundary

## Conservative boundary

This is a compliance exclusion, not an allowance. The instruction to change the
agent document and make the running Agent reread it is itself treated as human
supervision. We do not wait until the edited file is delivered or until a method
appears in the solver's output.

The first non-read-only supervisory instruction was received by the controlling
session at **2026-08-06 13:46:19.450 CST**
(`2026-08-06T05:46:19.450Z`):

> 对的 修正一下。然后用 continue prompt 让它重新读agent.md 后继续

The exact redacted event is preserved in
`evidence/SUPERVISION_BOUNDARY_EVENT.json`. Although the solver did not receive
the modified instructions until later, this package adopts the earlier external
supervision time. This is deliberately stricter than a “first method injection”
boundary.

The follow-up at `2026-08-06T05:50:50.061Z` (“use the official Continue Prompt,
but add reread `agent.md`”) is also excluded. It confirms the interpretation but
does not move the boundary later.

Read-only status requests and observations did not send messages to or alter the
running solver. They are therefore not solver inputs. Once the message above was
issued, however, the run is no longer treated as official-Prompt-only for this
claim, regardless of whether later work was independently conceived by the agent.

## Inputs received by the formal solver before the boundary

The mechanically filtered main rollout contains exactly two user-role input
messages before the boundary:

1. the startup-time `AGENTS.md` instructions plus environment context; and
2. the organizer's exact Starter Prompt with only the competition slug replaced.

It contains no Continuation Prompt, no ad hoc supervision, no user-proposed
method, no request to submit a specific candidate, and no request to restart a
worker. `official/STARTER_PROMPT_SUBSTITUTED.md` is byte-for-byte equal to the
organizer Starter Prompt after replacing `<COMPETITION-SLUG>`. The actual startup
instructions were mechanically exported from the rollout as
`environment/AGENTS-ACTUALLY-INJECTED.md`; they are not the later modified
project file.

The injected `AGENTS.md` payload is 32,951 bytes and ends mid-sentence at
`Preserve the exact code that prod` before the closing `</INSTRUCTIONS>` tag.
Direct byte comparison confirms that the exported file exactly matches the
startup message in the main rollout. This appears to be truncation at injection
time, not during this audit. The package preserves what the solver actually saw
and does not substitute the later, fuller project file.

Three child-agent rollouts were created autonomously by the main solver and are
included because they began and finished before the boundary. Their tasks came
from the main solver, not from human messages. All included rollout events have
timestamps at or before the boundary.

## Included score claim

Only remote submissions v1-v8 are included in the autonomous score claim. They
were all sent, completed, and scored before the boundary. The highest included
LB is 58.51666 (v4 and v8).

An additional source created before the boundary is retained only as an
unsubmitted research candidate. It is not represented as a scored result.

## Scope after the boundary

The package stops at the boundary. It does not inspect or make claims about any
later Task 3 activity. See `EXCLUSIONS.md`.
