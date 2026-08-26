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

## Deadline-scope cross-check

The timeline section says a Submission counts for ranking only when its
command is sent before the Final Submission Deadline. The limit section
uses different wording for Task 3 (scored Submissions) and Tasks 1/2/4/5/6
(Notebook versions), so both the account-wide extraction and the
deadline-scoped submission counts are shown below without choosing an
organizer interpretation:

| Task | Before deadline | After deadline | Account-wide extracted count | Deadline-scope reading |
|---|---:|---:|---:|---|
| task1 | 15 | 15 | 38 | Version cap is push-based; submission rows are only a lower-bound cross-check |
| task2 | 5 | 11 | 18 | Version cap is push-based; submission rows are only a lower-bound cross-check |
| task3 | 11 | 16 | 27 | 11 <= 15 under deadline-scoped reading; account-wide count remains subject to adjudication |
| task4 | 3 | 0 | 4 | Version cap is push-based; submission rows are only a lower-bound cross-check |
| task5 | 6 | 1 | 7 | Version cap is push-based; submission rows are only a lower-bound cross-check |
| task6 | 4 | 2 | 8 | Version cap is push-based; submission rows are only a lower-bound cross-check |

Task 1's tied official-final refs are the same extracted scriptVersionId.
Task 2's repeated version is the formal autonomous v2 pair, while its official
final ref is not in that duplicate group. Task 3's duplicate pair was sent
immediately before the official deadline and is not its selected official final;
that pre-deadline reuse is a separate literal conflict from the question of how
the 16 post-deadline submissions are counted.

The full records, source hashes, timestamps, and deadline offsets are in
[`SUBMISSION_VERSION_AUDIT.json`](SUBMISSION_VERSION_AUDIT.json).
