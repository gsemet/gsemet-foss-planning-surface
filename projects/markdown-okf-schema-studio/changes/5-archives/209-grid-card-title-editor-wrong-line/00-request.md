# 209 — Grid card title editor opens on the wrong source line (#229)

Night batch 2026-10-31. PREPARE ONLY until the owner confirms (via the Chief of Staff): local worktree, failing regression test, root-cause notes. No push to the PR branch, no PR.

Base: change-requests/203-grid-card-block-editor-layout (PR #230, head 806ec581). Will stack right above 203.

Backlog intent (verbatim):

> # Grid card title editor opens on the wrong source line and Done overwrites line 1 (data loss)
> 
> GitHub issue #229 (filed 2026-10-31 by the CR 203 Driver). A `{grid-item-card}` title such as
> "2. Status projection" is parsed as an ordered list; its `data-line` is relative to the title
> snippet, so the block editor opens the document's FIRST line. Pressing Done overwrites that line.
> Pre-existing; easier to hit since #230 (CR 203) makes the title editor readable.
> 
> Decision pending (owner, via the Chief of Staff): fix tonight as CR 209 stacked right above CR 203,
> then #230 switches to "Closes #226". Until confirmed: prepare locally only (worktree, failing
> regression test, root-cause notes); no PR, no push to a PR branch.

## GO (owner via Chief of Staff, 2026-10-31)

Fix tonight. Stack position: TOP, above CR 208 (local branch rebased onto a0ee07e4; test commit now 709b81b2).
Decisions (CoS, under the owner's go):
- Fix = candidate 3 in reports/root-cause.md ("option 2" for the CoS): parse the title inline only,
  map it explicitly to its directive line (data-line/data-end-line), skipped when `:link:` is set.
  Any card-title click opens the title editor (matches BLOCK-257). Behaviour change, say it plainly in the PR body.
- Scope also covers `:header:` (optionLine) and standalone `{card}`, each with a test that fails on main.
- One clean Conventional Commit (test + fix squashed), no force push, never merge, no release.
- PR closes #229; #230 switches to "Closes #226" afterwards (Foreman).

## Backlog item (archived 2026-10-31)

The backlog item `grid-card-title-editor-wrong-line` is kept in [backlog-item/](backlog-item/). Fixed by PR #236 (Closes #229); archived with this CR when #236 lands.
