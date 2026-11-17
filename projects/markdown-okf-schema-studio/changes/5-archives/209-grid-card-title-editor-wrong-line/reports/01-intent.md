# Grid card title editor opens on the wrong source line and Done overwrites line 1 (data loss)

GitHub issue #229 (filed 2026-10-31 by the CR 203 Driver). A `{grid-item-card}` title such as
"2. Status projection" is parsed as an ordered list; its `data-line` is relative to the title
snippet, so the block editor opens the document's FIRST line. Pressing Done overwrites that line.
Pre-existing; easier to hit since #230 (CR 203) makes the title editor readable.

Decision pending (owner, via the Chief of Staff): fix tonight as CR 209 stacked right above CR 203,
then #230 switches to "Closes #226". Until confirmed: prepare locally only (worktree, failing
regression test, root-cause notes); no PR, no push to a PR branch.
