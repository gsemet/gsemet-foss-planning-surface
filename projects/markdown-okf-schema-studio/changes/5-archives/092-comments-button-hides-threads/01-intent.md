# The Hide comments button leaves inline threads visible

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P3.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS REVIEW-158.

- The Comments button hides the gray chips only, while the setting preview.showComments hides chips
  and thread chips.
- Expected: the button hides both, like the setting.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
