# Conflicts: rebase of CR-436's branch onto origin/main

Branch `chantier/batch-30/cr-436-dev-mode-only-for-chantier-itself-other-` rebased from d91edcf3
(CR-428's two commits on old main 99fa847f) onto origin/main 33d10454. New head: 14160a65
(7baa6633 `feat(order): drop a CR to ready, never to the inbox`, 14160a65 `fix(scenario): the
inbox refusal of order drop exits usage`). Not pushed. Only the first commit conflicted; the second
replayed clean.

## Hunks and choices

1. `skills/chantier/references/chief-of-staff.md`, "Where a dropped CR goes": main widened
   `order hold` to "a CR out of the order for now (a ready CR of a stack, or a live CR in any
   mode)"; CR-428 dropped the inbox as a destination and added "the backlog and the next batch keep
   it as a draft", "moved to the backlog or the next batch (`3-ready`)". Kept main's hold sentence
   and CR-428's destination sentences.
2. `skills/chantier/scripts/cli/src/chantier/commands/forge_stack.py`, `_plan` docstring: main
   added "the dependents of an apart CR (to `<cr> waits with held <p>`...)"; CR-428 replaced "the
   inbox or the backlog" with "the backlog or the next batch, `3-ready`". Kept both: CR-428's
   destinations followed by main's apart-dependents clause.
3. `skills/chantier/scripts/cli/src/chantier/declare/orders.py`, `order` kind help: main changed the
   hold text to "(a live CR, or a ready CR of a stack, out of the slots and the order, and back)";
   CR-428 changed `drop (--note trash|inbox|P1..P4)` to `trash|ready|P1..P4`. Kept CR-428's drop
   notes and main's hold text.

No byte-order mark in any resolved file (first bytes checked before `rebase --continue`). No
product-intent clash.

## Fast gate

Command, run in the worktree at 14160a65: `just check`
Result: pass (exit 0): `1622 passed, 20 skipped in 138.84s`; `release-notes: ... ok`.
Raw log: `work/gates/conflict-resolver-just-check.log`.
