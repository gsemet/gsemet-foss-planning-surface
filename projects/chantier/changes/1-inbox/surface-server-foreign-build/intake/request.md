# Tell a chantier session when the surface server runs a foreign build

Priority P3. Split out of `sync-blocked-by-others` (its answer sync-lock-Q12, a Fable advisor's in the user's place, 2026-11-21).

A chantier session in dev mode is told when the surface's server, writer or forge hub runs a build that is not its checkout's, at the same version string. Today nothing shows it: `hub/state.py:other_version`, `board/command.py` (`_recorded`, `_answering`) and `hub/watch.py:start_line` compare version strings only. With `sync-blocked-by-others`, another project's session (Studio) launches these surface-wide processes through a cached `uvx --from "<checkout>"` build, which then serves the chantier project too.

Measured basis: 2026-11-14, a board with no Triage view, an old build at the same version.

To grill: how a build is identified in `chantier/server.json` beyond `version` (launch form or source); whether it is one line on `status` and the `watch:` start line only. Never a kill or an automatic restart.
