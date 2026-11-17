# Table editor polish

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P3.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS TABLE-062, TABLE-063, TABLE-104, TABLE-051, TABLE-054.

- Col +/− rewrites the whole table (padding, indentation and outer pipes lost) with no notice.
- Row/column buttons and every cell move close the open popover, link panel and slash menu.
- Editor and renderer disagree on a pipe inside a code span (`x|y`).
- Toolbar separators: a rule also separates Col + from Col −; the separator stays at the end of the
  first line when the group wraps.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
