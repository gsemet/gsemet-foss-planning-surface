# docs: the archive-in-the-PR default disagrees between two pages

Found by CR-382's Driver (batch-28, ask A-17), left as is in PR 347.

- `docs/explanation/planning-modes.md` says a CR's archive in its PR defaults to **no**.
- `docs/reference/planning-folder.md` says it defaults to **yes**.

The CLI decides **no**: `plugin_files.py` (around line 126) puts the archive in the PR only when
the project's `AGENTS.md` sets `- Archive in the PR: yes`; `repo.py` reads that line.

Change: make `planning-folder.md` say no, matching the CLI and `planning-modes.md`. Docs only; it
lands after CR-382 (PR 347), which moved these pages.
