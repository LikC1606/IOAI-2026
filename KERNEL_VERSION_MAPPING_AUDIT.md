# Kaggle official-ref to Kernel-version mapping audit

This note makes the Task 1/2 extraction limitation explicit at the level a
reviewer sees in Kaggle's account export. The `scriptVersionId` values below
come directly from each `all-submissions.json` record and are exact identifiers
for the linked Kernel revision. The numeric `vN` directories are the version
folders downloaded by the extraction script; they are candidate folders, not a
claim that Kaggle exposed a byte digest for the submitted revision.

| Task | Official ref | Exact linked `scriptVersionId` | Strongest archive candidate | Why this candidate | Exact-byte status |
|---|---:|---:|---|---|---|
| 1 | `55267333`, `55267368` | `340342513` | `ioai-2026-task1-pairwise-kemeny/v5` | Both descriptions say V5/v5; v5 contains the matching strong-speaker/Kemeny source and output | **Not byte-confirmed**; archive v5 and v6 are byte-equivalent for source/output |
| 2 | `55261432` | `340299118` | `ioai-2026-structured-extratrees-v1/v1` | The description says structured ExtraTrees v1; v1 is the first matching version and satisfies the runtime/output/report checks | **Not byte-confirmed**; no submitted-file digest is present in the export |

## What is exact and what is not

For both tasks, the account export proves the competition, Kernel slug, exact
internal `scriptVersionId`, submission timestamp, score, and deadline offset.
The archive also proves the hashes of the selected candidate source, output,
run log, and metadata; an authorized reviewer can rerun
`tools/verify_extraction_bindings.py` against the downloaded Drive archive.

On 2026-08-26, an authenticated Kaggle CLI `kernels output` cross-check was
performed for the Task 1 `v4/v5/v6` and Task 2 `v1` arguments. The CLI's output
request ignores the `/version` suffix and returns the kernel's latest output;
the receipt records this behavior explicitly. The latest Task 1 output is
byte-equal to the archive candidate output, while the latest Task 2 output is
not byte-equal to the archived v1 candidate (it corresponds to a later output).
Version-qualified source pulls were denied with HTTP 403. This cross-check
therefore does not prove any historical submitted-file digest or upgrade the
exact-version status above. The complete hash receipt is the
`independent_live_output_crosscheck` block in
[`EXTRACTION_BINDING_RECEIPT.json`](EXTRACTION_BINDING_RECEIPT.json).

The remaining gap is narrow but material: the extraction's metadata has an
empty `matched_version_confidence` list and each submission JSON has
`_version_confirmed: false`. Therefore this package does not say that the
candidate bytes are the exact bytes scored by Kaggle. For Task 1, archive
versions 5 and 6 have identical source and output hashes, so the unresolved
choice is between two byte-identical archive copies. For Task 2, the v1
candidate is selected by the explicit description and version naming, but no
submitted-file digest is available to independently prove it.

The machine-readable details are embedded in
`task1/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json` and
`task2/remote/OFFICIAL_FINAL_EXTRACTION_PROVENANCE.json` under
`kernel_linked_candidate.version_mapping_audit`. This is an evidence-strength
improvement, not a promotion to an exact-version or organizer-approved claim.
