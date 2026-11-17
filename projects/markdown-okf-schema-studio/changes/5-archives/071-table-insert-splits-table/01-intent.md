# Inserting a table with the caret inside a table splits it

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P2.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS TABLE-106, TABLE-107, TABLE-116, TABLE-119.

- With the caret in a pipe table, a list-table or an HTML table, the insert action puts the new
  table at the caret with blank lines, splitting the existing table.
- Expected: the new table goes after the table that holds the caret.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
