# Block editor: click on another block and double Done

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P2.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS BLOCK-041, BLOCK-047.

- A click on another block while the first editor holds changed text saves the first one but opens
  nothing at that click (the first editor waits for its render).
- Pressing Done again, or blurring, while the final save is in flight posts a second final save.
- Expected: the second block opens once the first save lands; a second final save is refused while
  finishing.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
