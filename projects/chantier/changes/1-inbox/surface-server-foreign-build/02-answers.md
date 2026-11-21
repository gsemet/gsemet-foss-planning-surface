# Answers

No grill held: the user delegated tonight's spec questions to a Fable advisor ("plus de question", 2026-11-21).

foreign-build-Q1 (2026-11-21, Fable advisor): **How a build is identified: A, `source`, the resolved folder of the loaded package, in the `server` and `hub` entries.** Exact for "not this checkout's" and free to compute; a content hash would raise the notice at almost every `status` while a CR edits `src/`.
foreign-build-Q2 (2026-11-21, Fable advisor): **Where the notice is said: A, `status`'s `board:` line, the watcher's start line, and one added non-refusing line on `board --seat`.** `board` silently reusing a foreign build is the measured case; the published API is not changed with no request for it.
foreign-build-Q3 (2026-11-21, Fable advisor): **Which sessions are told: A, dev-mode chantier sessions only (CR-436's test).** A plugin-mode session runs a cached build itself and can do nothing about other installs.
foreign-build-Q4 (2026-11-21, Fable advisor): **Same-version entry with no `source`: A, told as another build of unknown source.** Such an entry was written by a build older than this CR, so it is stale by definition; the case ends at the first restart.
foreign-build-Q5 (2026-11-21, Fable advisor): **Destination: A, batch-30, after CR-436 and CR-429, before CR-447 `docs-gardening`.** It rewrites a sentence CR-436 adds in this same batch; `depends.json` `{"after": ["sync-blocked-by-others", "board-fingerprint-cache"]}` for real needs (it calls CR-436's `is_chantier_project`, and is written on the watcher and start line as CR-429 leaves them).
