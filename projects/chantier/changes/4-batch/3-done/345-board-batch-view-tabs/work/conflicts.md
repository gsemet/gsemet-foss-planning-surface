# Conflicts: CR-345 rebase onto CR-344 (03ee16df)

Command: `git -C <worktree> rebase --onto chantier/batch-24/cr-344-change-specification-the-board-s-design- 6f63babc`
New head: 15359cc8b32b39b099134947565bf3834aca52a4. Only commit 94f0924c conflicted; 7f075653 applied cleanly.

## skills/chantier/scripts/cli/src/chantier/board/web/js/core/router.js (8 hunks, all kept from both sides)

1. Header comment: merged text naming `&t=<tab>` (Batch tab) and `&st=&sort=` (PRs), with the PRs view in the batch views list.
2. Constants: kept CR-343's exported `BATCH_VIEWS = ['costs','batch','prs']`, `PRS_STATES`, `PRS_SORTS`; added CR-345's `TABS` (the old unexported `BATCH_VIEWS` of CR-345 dropped).
3. `resolve`: kept CR-343's `only()`/`st`/`sort`; added `tab` (only on the batch view); returns `{project, view, batch, tab, st, sort}`.
4. `settle`: on "All projects" clears `batch`, `tab` (to TABS[0]), `st`, `sort`.
5. `apply`: destructures `tab, st, sort`; update sets `batchTab`, `prsState`, `prsSort`; the `closed`/`reset` spreads stay once, before (CR-343's order; CR-345's duplicate after dropped).
6. `href`: writes `st`/`sort` (PRs view) and `t` (non-default tab).
7. Helpers: kept `prsOf`, added `tabOf` beside it.
8. `go`: passes both `tab: tabOf(...)` and `...prsOf(...)`.

No BOM added (file starts as before).

## Fast gate
Command as run: `just check` in the worktree at the rebased head.
Result: pass (exit 0): 565 passed in 22.85s; release-notes check ok. Log: work/conflict-resolver/check.log
