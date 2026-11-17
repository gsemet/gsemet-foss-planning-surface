# Returning to a document loses its view state

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P2.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS LIFE-138, LIFE-139, LIFE-140, LIFE-030 (deduced from the code, verify first).

- Switching A → B → A loses the focused block, the selection, the open sections and the Description
  choice of A: the pending page clears the remembered state before the render reads it.
- Expected: verify, then restore the remembered state of A after the switch; integration test.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
