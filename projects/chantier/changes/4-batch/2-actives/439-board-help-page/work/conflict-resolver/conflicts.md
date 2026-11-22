# CR-439 restack onto e4199b7f (CR-438 head): conflicts

Rebase finished: 5 commits remain (the pictures commit became empty). New head c8b88ad6.

Commit 1 (batch mode and legend into the title row): main already carried the same move (batch-head.js, batch.css, DESIGN.md, docs/web-board.md) plus the mode switch tooltips, so HEAD (main) won in docs/web-board.md, DESIGN.md, css/views/batch.css and js/views/batch-head.js; only the CR's title-row tests in test_board_design.py were kept next to main's new tests.
Commit 2 (pictures): 5 PNG add/add conflicts; kept main's pictures (already retaken with the title row, 531bf319 and later); commit dropped as empty.
Commit 3 (tests in own file): test_board_design.py, removed the title-row tests (they live in test_board_title_row.py), kept main's dashboard and fold tests.
Commit 4 (Help page): both sides kept in DESIGN.md (Help section after the writes-count text), index.html (inbox.css + help.css), en.js/fr.js (imports, nav.help after nav.inbox, ...help after ...dashboard), registry.js (help import, help entry moved after the Inbox entry as the test requires; offline comment added), header.js (main's comment), test_board_design.py (both test sets), router.js (main's dashboard/history keys plus the Help topic: configure(topics), topic in resolve/apply/href).
Commit 6 (Help tests own file): removed the Help tests from test_board_design.py, kept main's.

Edits beyond conflict markers, needed for the gate (uncommitted, in the worktree): router.js split into askedKeys, viewState, helpKeys (biome complexity limit 10); css/views... shell.css: dropped the CR's duplicate `overflow-x: auto` in `.bnav` (main already has it).

Fast gate: `just check` in the worktree: pass (mypy, biome, 1925 passed 20 skipped, release notes ok).
