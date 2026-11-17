# A request that names an older render gets no answer

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P2.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS BLOCK-248, BLOCK-123, BLOCK-183, BLOCK-218, PALETTE-175 (gate in TRUST-065).

- The host drops a request naming an older render without answering, so the page waits for its own
  timeout (6 s for a list, 10 min for a file dialog), an arrow click stays pending, keyboard and
  clipboard requests fail silently.
- Expected: the host always answers, with the out-of-date reason; the page clears its pending state
  and shows the reason. Check together with P1/palette-stale-after-autosave.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
