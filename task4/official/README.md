# Task 4 prompt-source map

`OFFICIAL_PAGES_FULL.json` is the authoritative snapshot of the authenticated
Kaggle pages. `STARTER_PROMPT_EXACT.md` and `CONTINUE_PROMPT_EXACT.md` are the
byte-preserved official page bodies used for exact-text comparison.

The older `start.md` and `continue.md` files are retained because they are the
prompt payloads actually present in the historical project/trace. They are
**not** official prompt snapshots: the audit classifies them as a formatting-
modified starter and a substantive generic continuation template. Keeping
these files beside the official snapshots makes the deviation reviewable
instead of silently replacing it.

See [`../../PROMPT_CONFORMANCE_AUDIT.md`](../../PROMPT_CONFORMANCE_AUDIT.md)
and [`../RULE_DIFFERENCE_AUDIT.md`](../RULE_DIFFERENCE_AUDIT.md).
