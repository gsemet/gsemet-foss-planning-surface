# Verify CR-447 (garden the docs)

Head: 4c9943619983b8d91c0a3a3d317961214a89e2ce

All claims judged at 4c99436 (the pushed head, base 5691a05d). No Help edit (no `js/` file in the diff), so the docs-only gate rule holds.

- Anchors, 4c99436: `python -I work/check_anchors.py .` -> `186 links checked, 0 problem(s)` (evidence/anchors-verifier.txt).
- Added-file naming, 4c99436: `git diff --name-only --diff-filter=A 5691a05d...HEAD -- docs/` -> surface-server-texts.md, surface-server.svg, web-board/help-pc.png, help-phone.png; the script's naming check passes; surface-server.svg is linked from README.md:237, docs/web-board.md:170, CONTRIBUTING.md:132; help pictures from docs/web-board.md.
- SVG parse + `<desc>`/`<title>` equality, 4c99436: `uv run --no-project --script work/check_svgs.py . <out> --render` -> 12 `ok`, `problems: 0` (evidence/svgs-verifier.txt).
- Renders looked at, 4c99436: evidence/svg-verifier/*.png; looked at surface-server, how-chantier-works, cr-lifecycle, batch-lifecycle, cr-lifecycle-simple, cr-folder-lifecycle: no clipped or overlapping text from this CR (a slight tight fit of two labels in cr-folder-lifecycle's 6-trash and 5-archives boxes predates it: only its `<desc>` changed).
- Removed-words search, 4c99436: grep -i "factory mode|order factory" and the French wording, over README, CONTRIBUTING, docs/*.md, docs/*.svg, en-help.js, fr-help.js -> no hit; `order drop ... 1-inbox` -> no hit; `0.0.0.0` -> one hit, docs/web-board.md:207 (`--host 0.0.0.0`, an address a user chooses, not named as the default): holds.
- Pictures, 4c99436: opened help-pc, help-phone, batch-pc (Kanban tab: 1-pending, 2-actives, 3-done, PRs to review/draft, matches the caption), writer-pc, config-pc, inbox-pc: show the new sidebar (Inbox, Help), made-up project and paths (/home/demo), no username or home folder.
- Kanban check (docs-garden-Q6): inventory row records cr-folder-lifecycle draws 1-pending/2-actives/3-done; rendered image confirms.
- Inventory, 4c99436: work/garden-inventory.md has a row per text page, diagram pair (batch-pace out of scope with reason), picture group; complete against the spec's lists. Minor: one row says the README caption was "fixed", another "holds" (the caption is correct at head); release-process.md read in part only.
- Docs against code, 4c99436: surface-server words vs code: QUIET_S 1.0 / MOST_S 5.0 (board/watch_files.py), hub CYCLE_S 20 (hub/times.py), writer 300 s (writer/times.py), 304 on unchanged fingerprint (board/fingerprint.py), idle look 5 s (board/idle.py), `read-only:` start line (board/command.py), `cli.run` op (board/api/ops.py). The web-board four tabs (Kanban, Graph, Gantt, Time cards) match the picture. Key/webui/Griller sentences match AGENTS.md.
- Spec deviation, minor: the Help section is `## Help` in docs/web-board.md (spec: `### Help` under "The views"); anchors and links resolve, so no failure.
- Tests, 4c99436: `pytest test_plugin_files.py test_board_design.py` -> `85 passed`. CI at the head (evidence/ci-checks.log): just check on 3 OSes, eval-dry-run and scenario (ubuntu) pass.
- Review box, 4c99436: `chantier log CR-447`: "r2 approved at bfdf5a2b, committed as 4c994361 (rebased on origin/main, tree unchanged)": proves the review at the head.
- PR description, 4c99436: read with `gh pr view 435`: renders (sections, fold), no images attached, Summary/Deliverables/Changes match the diff (54 files), Known gaps names the unverified costs.md figure and the kept captures. The Test plan boxes are the Driver's to tick.
- Local gate: `just scenario` at 4c99436 failed one step (surface-board webui on a running server; port 8765 held by the user's own board, environmental); no gate pass at the head on this machine. CI scenario (ubuntu) passed. Not a docs defect; the local Windows run remains owed before merge.

VERIFIED
