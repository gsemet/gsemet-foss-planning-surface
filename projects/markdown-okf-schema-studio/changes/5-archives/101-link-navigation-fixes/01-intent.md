# Link navigation and history fixes

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P3.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS TOOLBAR-061, TOOLBAR-075, TOOLBAR-079, TOOLBAR-087, TOOLBAR-093, TOOLBAR-119.

- Back/Next in the same document does not scroll when Anchor is off.
- A failed open still moves the history position.
- Link tooltips are computed once per page and go stale when files are created or deleted.
- A link to a missing or blocked target looks like a valid link.
- A file name with a literal % cannot be reached; a doubly encoded % is decoded twice; the
  leftover-escape check misses %41 (page uses [da-f], host [0-9a-f]).

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
