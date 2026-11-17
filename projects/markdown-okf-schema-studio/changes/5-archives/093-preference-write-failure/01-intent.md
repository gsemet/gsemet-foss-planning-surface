# A failed preference write is only logged

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P3.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS THEME-014, TOOLBAR-014.

- When storing the theme or view preferences fails, the host only logs to the console; the reader
  sees nothing and the choice is lost at the next start.
- Expected: a short warning to the reader.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
