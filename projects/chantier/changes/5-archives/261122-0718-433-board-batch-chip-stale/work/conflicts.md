# Conflicts: CR-433 rebase onto 06410234

Rebase of 0eca7898 onto `chantier/batch-30/cr-432-chantier-s-allow-rules-name-real-paths-n`
(06410234). New head: e7584d79 (commit message kept).

## Hunks

1. `skills/chantier/scripts/cli/src/chantier/clients/web/DESIGN.md`, rule "One card, one column,
   one chip". The base (79eac1db) appended the lane sentences (a lane built by `lane(parts)`, no
   dot; Triage's last column holds "Running batch" over "Next batch"). This CR inserted, after
   "(inbox, P1 to P4, 3-ready);", that a card of a CR in the batch shows its batch folder
   (1-pending, 2-actives, 3-done) in a neutral grey chip, never a priority. Choice: both kept, in
   order: the CR's sentence, then the filter-toggle sentence, then the base's lane sentences. No
   BOM before or after.

## New reader check

The base added one new card for batch rows: `pending(c)` in
`skills/chantier/scripts/cli/src/chantier/clients/web/js/triage/columns.js` (the running-batch
lane draws the batch's queued CRs as plain cards). It does not read `c.priority` (so no stale
reader), but it drew no chip at all, against the DESIGN rule above. One-line fix applied in the
rebased commit: `priority: c.stage,` passed to `card()` (a null stage draws no chip, as
`card.js`'s `topRow` does). No other reader of a batch row's `priority` in `js/`.

## Fast gate

Command, as run in the worktree: `just check`
Result: pass (exit 0; 1610 passed, 20 skipped; release-notes ok). Raw log:
`work/gates/conflict-resolver-check.log`.
