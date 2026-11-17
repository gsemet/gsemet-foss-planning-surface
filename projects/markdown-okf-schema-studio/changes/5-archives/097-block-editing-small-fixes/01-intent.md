# Small block editing and palette fixes

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P3.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS BLOCK-138, BLOCK-179, PALETTE-183.

- AltGr with up/down is read as the move chord on Windows and Linux layouts that report Ctrl+Alt.
- The paste-next-to-include check looks only at the closing fence line, so it is enforced by the
  page only.
- The bibliography list says More entries exist when exactly 20 files exist and nothing was cut.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
