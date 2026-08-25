# Execution trace index

Generated from the JSON index by `tools/build_execution_trace_index.py`.
The JSONL files are credential-redacted observable traces; see
[`EXECUTION_TRACES.md`](EXECUTION_TRACES.md) for interpretation and limits.

| Task | Files | Events | Logical calls | Outer exec calls | Tokens |
|---|---:|---:|---:|---:|---:|
| task1 | 2 | 775 | 16 | 133 | 30380753 |
| task2 | 1 | 705 | 4 | 128 | 14457808 |
| task3 | 4 | 2427 | 135 | 373 | unavailable |
| task4 | 5 | 2717 | 75 | 387 | 109119898 |
| task5 | 14 | 4705 | 131 | 409 | 160243108 |
| task6 | 5 | 2871 | 63 | 341 | 104143733 |

## Files

| Task | Role | Events | SHA-256 | Path |
|---|---|---:|---|---|
| task1 | main | 350 | `bcfb0c6ffca945638aedd4b3771915bc88abf72ca29843b457e966427684eb89` | `task1/evidence/rollouts/rollout-2026-08-05T17-20-55-019fd139-d180-7171-ac0b-c037e11866eb.jsonl` |
| task1 | agent-executed-after-supervision-boundary | 425 | `390d1fa9399fe42bfd31412659af9156a8e98542713ad2b6371ee51efefe870b` | `task1/evidence/submission-execution/rollout-2026-08-05T17-20-55-019fd139-d180-7171-ac0b-c037e11866eb-post-boundary.jsonl` |
| task2 | main | 705 | `a7dc48c7a837b3536d835c17fdee63db6fe27b79cd1cc577cbf4e15672f45014` | `task2/evidence/rollouts/rollout-2026-08-05T13-30-31-019fd066-e338-71a0-9d8e-6e1d154c5a79.jsonl` |
| task3 | main | 990 | `44c7225a3b4a9840d68ffbc330f7bd954c8158d9d05272977c7dbaf41f31122a` | `task3/evidence/rollouts/rollout-2026-08-06T12-34-49-019fd55a-3edf-7801-b6a1-f1313393ff34.jsonl` |
| task3 | subagent | 690 | `f4d78c9539763ff7784dd20e71b3a293ce05aed41f5278f558ac978abf35bffb` | `task3/evidence/rollouts/rollout-2026-08-06T12-40-25-019fd55f-61f3-74c2-a87f-66ce5288dc56.jsonl` |
| task3 | subagent | 385 | `a663de82720476e2f46f7531b3c802dad650c9799c53871643e288d319fa8934` | `task3/evidence/rollouts/rollout-2026-08-06T12-41-11-019fd560-1290-7bb1-af1d-8fd44c84aad5.jsonl` |
| task3 | subagent | 362 | `d83acc1a9aa4b316fca3e6618b93885d909dca9e0bde7404fb389f0804b95dc6` | `task3/evidence/rollouts/rollout-2026-08-06T12-41-42-019fd560-8eec-78c1-92c9-3ab2e67b1bd8.jsonl` |
| task4 | main | 1549 | `222c0023f6c2a8d277a54375aaf2183bbdb2f8f48f8289e3a400f7803f78d08b` | `task4/evidence/rollouts/rollout-2026-08-07T12-18-29-019fda71-a6a2-7a22-8c18-22e99f127422.jsonl` |
| task4 | subagent | 229 | `e2a4f52b4f01fa8e7f6dfc61244158093c40b367485166131efbbdbfe4d0d203` | `task4/evidence/rollouts/rollout-2026-08-07T12-18-41-019fda71-d4eb-70a3-9b66-e0fb3b2d0e66.jsonl` |
| task4 | subagent | 239 | `1c95db393d686208e5ce4d0bf7557eb343d693093838eb8cef69645f12e33bc8` | `task4/evidence/rollouts/rollout-2026-08-07T12-18-47-019fda71-effd-7321-8ce9-2a4a57fcaa48.jsonl` |
| task4 | subagent | 351 | `71be87c96740c72287821089d12e09124fad371cf9d4b868572017898aefa88a` | `task4/evidence/rollouts/rollout-2026-08-07T13-21-43-019fdaab-8d94-76a0-b625-078c838b5227.jsonl` |
| task4 | subagent | 349 | `ff3d1c60a3052f12e32275139170923778b6d344bc7390b3a6a2b2da49c44a62` | `task4/evidence/rollouts/rollout-2026-08-07T13-21-51-019fdaab-ace4-7b51-93b2-244d9517423a.jsonl` |
| task5 | main | 1230 | `bc25826f180ce0ae427f7fbe6545628321a0ba2b48520ad1d5a5f14fd40c135c` | `task5/evidence/rollouts/rollout-2026-08-07T15-04-23-019fdb09-8b16-7032-82e1-21be10be17c0.jsonl` |
| task5 | subagent | 167 | `bcbc8e97128cf6a9b3e4548d4b41f897df56946ffbf8f96a08001716f54ed7c4` | `task5/evidence/rollouts/rollout-2026-08-07T15-10-16-019fdb0e-ece5-75f1-a919-0cf4bc532838.jsonl` |
| task5 | subagent | 153 | `9abffaf5ee9d98aae66398b5c255a83b98d396544f3200daccb6aba3179b30bf` | `task5/evidence/rollouts/rollout-2026-08-07T15-10-32-019fdb0f-2ccc-7d80-b97f-3e6891df20be.jsonl` |
| task5 | subagent | 202 | `b62435b32842b4de0b6ca3111293436203a41becf77d6ee76f2df8b481d60d9a` | `task5/evidence/rollouts/rollout-2026-08-07T15-10-46-019fdb0f-641d-71f1-aad9-71a76ad14bb3.jsonl` |
| task5 | subagent | 221 | `7cefc07365879c0949a2849a2adbbdaf98d2187add64f92dec174a506411053f` | `task5/evidence/rollouts/rollout-2026-08-07T15-23-21-019fdb1a-e97c-7542-b5b9-eb65046b1e4c.jsonl` |
| task5 | subagent | 256 | `1760d79578466bf684877061332fb9498dcaaecb93e83672e2e347cb41158d81` | `task5/evidence/rollouts/rollout-2026-08-07T15-35-11-019fdb25-bcda-76b3-aa61-bf745122bb27.jsonl` |
| task5 | subagent | 226 | `a31505cde8dd72b1c1153d743777b95bb8649e0ad15e99f51067a5dfcafb1a09` | `task5/evidence/rollouts/rollout-2026-08-07T15-35-25-019fdb25-f27d-7fc0-a235-ef2d4e1b9e14.jsonl` |
| task5 | subagent | 241 | `2a3b991bce9d6cff0fcfcff166c65615d701bcac79b815394530b069d2b817fc` | `task5/evidence/rollouts/rollout-2026-08-07T15-36-47-019fdb27-333f-7002-84f3-83c19536e1a2.jsonl` |
| task5 | subagent | 337 | `b3305a1d3a25689ed8296dd8fd4b53ce284135bb36e73c7ad50a29db24f4e7c6` | `task5/evidence/rollouts/rollout-2026-08-07T15-58-45-019fdb3b-4f7e-70b2-b652-940314651df4.jsonl` |
| task5 | subagent | 253 | `52367321a1fabf26f3acaa48d5576a656f58e498cf9f3c496709645c9f75b0b0` | `task5/evidence/rollouts/rollout-2026-08-07T15-58-59-019fdb3b-85ff-7f63-9981-952915290c13.jsonl` |
| task5 | subagent | 264 | `235b80df2cf633938ac0c354aeb95f8bc6dace3a677ffb3ccb09e2b363d4f0b5` | `task5/evidence/rollouts/rollout-2026-08-07T15-59-18-019fdb3b-d220-74b3-9fce-c89b25442543.jsonl` |
| task5 | subagent | 402 | `4653a18d04cd8e40651e24a7c707692989546c2e40bb07dda8f2fd3eb9c866d4` | `task5/evidence/rollouts/rollout-2026-08-07T16-05-40-019fdb41-a587-7410-8926-ba38fb7da71d.jsonl` |
| task5 | subagent | 396 | `4536a98d9fd32a9448ec6c528ce59a29f7fedad98fbecf194c0c81ae91a7730f` | `task5/evidence/rollouts/rollout-2026-08-07T16-23-09-019fdb51-a930-7953-9c40-be02d0c93136.jsonl` |
| task5 | subagent | 357 | `f2b7101d6c24109c2d01a12880454d06a5426b4287547f7018f1d96c66144d7e` | `task5/evidence/rollouts/rollout-2026-08-07T16-23-36-019fdb52-12da-7931-b44c-82fe30560795.jsonl` |
| task6 | main | 1348 | `80e17c82be60a61fb363353f4e417e2814029af2b49d8a63c3ff6fcf6e92dca7` | `task6/evidence/rollouts/rollout-2026-08-09T00-23-24-019fe22f-b2b8-7191-a6ec-39dea000da9f.jsonl` |
| task6 | subagent | 346 | `71ec1e6011b5d8f56eb9b3e23153f3e604fe6105f579f026022259d1b7e41eae` | `task6/evidence/rollouts/rollout-2026-08-09T00-23-42-019fe22f-f897-7d10-b27c-2c6586c55a27.jsonl` |
| task6 | subagent | 349 | `e8db254c402a2054402b8d07818de3aed0fb220bc02a5f9082ef2a81e58f395b` | `task6/evidence/rollouts/rollout-2026-08-09T00-30-10-019fe235-e3a2-7173-bac5-0ba0451f279f.jsonl` |
| task6 | subagent | 418 | `839e71c808b6712fd5d98ed58f8af597992552e0ddc0f15e669915b2a87ea04a` | `task6/evidence/rollouts/rollout-2026-08-09T02-10-50-019fe292-0fce-7f73-9f85-0bfc38fe76dd.jsonl` |
| task6 | subagent | 410 | `64620cee9f356d1ecc8a3b464cdb5ec2f9d6a1e800c8202f7aec6fd4ce6c1dc5` | `task6/evidence/rollouts/rollout-2026-08-09T02-12-36-019fe293-ac6b-7451-a0a4-39d4cae3e7f0.jsonl` |
