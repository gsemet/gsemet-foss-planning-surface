# A line break pasted into a table cell breaks the table

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P2.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS TABLE-093, TABLE-070, TABLE-072.

- The cell text box has no paste handler: a pasted line break splits the row in the source, the
  table stops rendering as one row, and List-table then does nothing with no message.
- Expected: pasted line breaks become spaces (or `<br>` if the writer chooses); remove the dead
  refusal branch of TABLE-072 or make it reachable.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
