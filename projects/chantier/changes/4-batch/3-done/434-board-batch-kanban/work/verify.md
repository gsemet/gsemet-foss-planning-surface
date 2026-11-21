# Verify CR-434

Head: 0aec4529cf9513751ea64811222a61092914054b

All claims judged at 0aec4529 (worktree clean, `git rev-parse HEAD`).

1. Static checks pass (`uv run --no-sync pytest skills/chantier/scripts/cli/tests/test_board_design.py -q`): `34 passed in 1.31s`, including the 7 parametrized `test_the_batch_kanban_as_shipped` cells (TABS begins 'kanban', 8 keys en+fr, batch.kanban_closed in batch.js, shell.css `.main:has(.view > .kanban)` and no bare one, column/crCard imports, no write words, `.stage` and no `.folder`). VERIFIED.
2. Biome / lint (`just lint`): `Checked 152 files ... No fixes applied`, mypy `no issues found in 377 source files`. VERIFIED.
3. Panel behaviour on a fixture (`node work/verifier/evidence/probe.mjs <web>`, output `work/verifier/evidence/probe-output.log`), rows with `stage` as the spec describes: three columns `bcol-pending`, `bcol-actives`, `bcol-done` and root `class="kanban bkanban"` present; card order `CR-425 CR-430 | CR-410 CR-428 | CR-402 CR-401 CR-403` (number ascending in the first two; done by `merged_at` descending, missing last); rows with stage `0-inbox` or no stage (CR-499, CR-498) appear in no column. VERIFIED (against fixture rows, not a live server).
4. Router: `TABS kanban,graph,gantt,cards`; with no `t=` and nothing kept the tab is `kanban`; with kept `graph` it is `graph`; `t=kanban` gives `kanban`; `href` of a batch place writes `t=kanban`, of Home writes no `t=`; `tabOf` from Home with kept graph gives `graph`, from Batch to Batch (navigator) keeps the tab shown (`gantt`). Same probe log. VERIFIED. `apply()` write of the preference and `settle()` for "All projects" read in the diff (`keep()`, `keptTab()`), not run in a browser.
5. Closed batch note: diff of `recorded()` in batch.js maps `kanban` to `batch.kanban_closed`; key present in both language files (check 1). VERIFIED by reading and the static test; not seen rendered.
6. Docs and DESIGN.md: `git show HEAD` shows the web-board.md Batch paragraph rewritten (four views, device rule, closed note, address sentence replaced) and DESIGN.md "(Triage, Kanban, the Batch page's Kanban)". VERIFIED.
7. CI at 0aec4529 (`gh pr checks 407`): check macos/ubuntu/windows pass, eval-dry-run pass, scenario pass. Long gate at 140c12a (same tree, clean rebase) per the brief. VERIFIED.
8. Review box: Driver notes in `chantier log CR-434`: "r1 approved at 06410234..., committed as 140c12a9". The pushed head 0aec4529 is a later clean rebase of the same patch. VERIFIED (carried from 140c12a).
9. PR description (`gh pr view 407` body == pr-body.md): sections render; Summary, Deliverables, Changes match the diff (11 files); Known gaps names the missing screenshots and the `stage` dependency on #406, and the Deliverables mark screenshots UNVERIFIED. No images. Test plan lines still hold `<sha7>` placeholders, to be filled at ship. VERIFIED, with that note.
10. Rows' `stage` on a live board, and the by-hand screenshots (wide, phone, kept tab, private window, scroll, All projects, closed batch), the CSS layout (flex, phone snapping, page scroll with `.main:has(.view > .kanban)`): UNVERIFIED, not captured (no real board with `stage`, #406 not in this branch); static test and diff reading only.

Verdict: VERIFIED
