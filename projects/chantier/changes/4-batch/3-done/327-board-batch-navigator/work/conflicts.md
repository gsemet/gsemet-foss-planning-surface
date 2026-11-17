# Conflicts: CR-327 rebased onto chantier/batch-24/cr-326-cr (a16ff1b)

Only one conflict, in commit 967da89; the two later commits applied cleanly.

## skills/chantier/scripts/cli/src/chantier/board/web/js/ui/header.js, `crumbs()`
- Base (a16ff1b): chip carries a state-hue class (`chip ${shown}`), batch taken from `state.data.batch`.
- This CR: batch chosen by `shownBatchChip(state)` (closed record gets a grey "closed" chip).
- Choice: keep the CR's `shownBatchChip` logic and add the base's hue class: `<span class="chip ${shown.icon}">`. No BOM added.

Fast gate: `just check` -> pass (ruff clean, 449 tests passed, release-notes check ok). Tree clean after.
