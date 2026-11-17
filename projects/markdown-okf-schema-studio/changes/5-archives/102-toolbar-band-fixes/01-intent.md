# Toolbar and sticky heading band fixes

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P3.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS TOOLBAR-006, TOOLBAR-020, TOOLBAR-041, TOOLBAR-043, TOOLBAR-131.

- The toolbar floats over the text and over VS Code's find widget.
- A zero-height heading still appears as a parent in the band; the band follows headings inside
  admonitions and the properties table that the TOC leaves out.
- The fold twisty keeps the same accessible name in both states.
- The editor-selection mark picks the block whose first line is nearest, not the block that
  contains the cursor.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
