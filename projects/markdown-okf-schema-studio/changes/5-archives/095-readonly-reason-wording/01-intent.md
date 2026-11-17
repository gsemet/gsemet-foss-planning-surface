# Read-only refusals blame workspace trust for files outside the workspace

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P3.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS REVIEW-132, REVIEW-180, TRUST-002.

- Comment and thread refusals say the workspace is untrusted, also for a file outside every
  workspace folder (same wording issue as GFM-026 in P3/checkbox-refusal-feedback: fix them
  together).
- The first load of a read-only page has edit cells in the properties table until the host rebuilds
  it.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
