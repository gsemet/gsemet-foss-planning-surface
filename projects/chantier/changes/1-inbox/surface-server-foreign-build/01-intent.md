# Tell a chantier session when the surface server runs a foreign build

Split out of `sync-blocked-by-others` (CR-436 of batch-30): its answer sync-lock-Q12 (a Fable
advisor's in the user's place, 2026-11-21) accepted, in words only, that the board server, its
writer and the forge hub, started from another project's session in the plugin mode, run that
session's cached `uvx --from "<checkout>"` build and serve every project of the surface, chantier
included, with no notice while the version string is equal; "a notice of a foreign build is out
of scope: the inbox item `surface-server-foreign-build`". This is that item.

Intent: a chantier session in the dev mode is told, in one line, when the surface's server (and
its writer) or forge hub runs a build that is not its own checkout's, at the same version string;
the notice says how to get its own build (stop the process by hand, then start it again from the
chantier session). Never a kill, never an automatic restart.

Measured basis: 2026-11-14, a board with no Triage view, served by an old build at the same
version. Today `hub/state.py:other_version`, `board/command.py` (`_recorded`, `_answering`) and
`hub/watch.py:start_line` compare version strings only.

No grill was held: the user delegated the spec questions of 2026-11-21 to a Fable advisor ("plus
de question"); the open choices are the specification's numbered questions (foreign-build-Q1...).

Priority P3.
