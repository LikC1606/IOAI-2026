# Submission-version audit

This audit checks two literal published requirements against the complete
organizer-requested Kaggle account extraction: the task budget and the rule
that one Notebook version may be submitted at most once. It records evidence;
it does not decide whether the organizer grants an exception.

| Task | Published budget | Extracted count | Budget finding | Repeated scriptVersionId groups | Version-reuse finding | Official-final impact |
|---|---:|---:|---|---:|---|---|
| task1 | 20 notebook_versions | 38 | **known_deviation_under_published_wording** | 2 | **known_deviation_under_published_wording** | 55267333, 55267368 |
| task2 | 20 notebook_versions | 18 | **evidence_supported_account_extraction_scope** | 1 | **known_deviation_under_published_wording** | none |
| task3 | 15 scored_submissions | 27 | **known_deviation_under_published_wording** | 1 | **known_deviation_under_published_wording** | none |
| task4 | 20 notebook_versions | 4 | **evidence_supported_account_extraction_scope** | 0 | **evidence_supported_account_extraction_scope** | none |
| task5 | 15 notebook_versions | 7 | **evidence_supported_account_extraction_scope** | 0 | **evidence_supported_account_extraction_scope** | none |
| task6 | 20 notebook_versions | 8 | **evidence_supported_account_extraction_scope** | 0 | **evidence_supported_account_extraction_scope** | none |

## Repeated version details

- task1: scriptVersionId `340342513` was used by `55267333`, `55267368` (all before deadline).
- task1: scriptVersionId `340345171` was used by `55267587`, `55267607`, `55267647` (includes post-deadline activity).
- task2: scriptVersionId `340290308` was used by `55260462`, `55260695` (all before deadline).
- task3: scriptVersionId `340521169` was used by `55290807`, `55290810` (all before deadline).

Task 1's tied official-final refs are the same extracted scriptVersionId.
Task 2's repeated version is the formal autonomous v2 pair, while its official
final ref is not in that duplicate group. Task 3's duplicate pair was sent
immediately before the official deadline and is not its selected official final;
that pre-deadline reuse is a separate literal conflict from the question of how
the 16 post-deadline submissions are counted.

The full records, source hashes, timestamps, and deadline offsets are in
[`SUBMISSION_VERSION_AUDIT.json`](SUBMISSION_VERSION_AUDIT.json).
