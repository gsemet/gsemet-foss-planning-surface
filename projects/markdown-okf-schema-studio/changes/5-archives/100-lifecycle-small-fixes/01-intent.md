# Small preview lifecycle fixes

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P3.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS LIFE-010, LIFE-094, LIFE-099, CORE-027.

- The Open Preview command is refused from a Studio Open With tab (no check for a custom editor).
- An edit applied by another tool to the active document counts as typing and never glows.
- The double-click reveal setting has no visible effect: a single click already reveals the line.
- A failed engine warm-up is cached, so the first render does not retry the load.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
