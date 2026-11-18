# Conflicts: CR-344 rebased onto CR-343's branch (ad5dd947)

Command: `git rebase --onto chantier/batch-24/cr-343-change-specification-the-prs-page-filter 1690ec4f`. Only the first commit (306f15b9, now d05ad19f) conflicted; the other two applied cleanly.

## css/views/postit.css
Hunk: CR-343 widened `.lbtn[data-pf]::before` to `[data-pvf]`/`[data-pvs]`; CR-344 had moved the `.lbtn` rules out to `components/chip.css`.
Choice: dropped the block from postit.css (CR-344's move) and added CR-343's three-selector `content: none` rule to `css/components/chip.css`, next to `.lbtn.on`. Both intents kept.

## js/views/batch-graph.js
Hunk: CR-343 had `recordedNode`/`node` as hand-written markup using `t('pr.tag')` (MR on GitLab); CR-344 draws them through `card()`.
Choice: kept CR-344's `card()` calls; `prMark` now renders `t('pr.tag')` instead of the literal `PR`, so CR-343's wording survives.

## js/views/overview.js
Hunks: (1) imports: CR-343 `t, tf`, CR-344 `card`; kept both. (2) `render`: kept CR-343's `sharedForge`, `head(forge)`, `tf(forge, 'overview.note')`, with CR-344's `projectCard` in the cards list.

## Fast gate
`just check` at head: ruff format/check, mypy, uv lock --check, biome, pytest (549 passed), release-notes check. Result: pass.
