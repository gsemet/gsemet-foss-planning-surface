# Conflicts: rebase of CR-428 onto origin/main (33d10454)

New head: 0f3dd8ce (f291230e feat(order)..., 0f3dd8ce fix(scenario)...). Not pushed.
Only commit 5501f1ce conflicted; d91edcf3 applied clean. No byte-order mark added (checked).

## skills/chantier/references/chief-of-staff.md ("Where a dropped CR goes")

- main (CR-427): `order hold` keeps "a ready CR of a stack, or a live CR in any mode" out of the order.
- CR-428: destinations are trash, next batch (`3-ready`), backlog; the backlog and next batch keep the PR as a draft; `formerly.json` for backlog or `3-ready`.
- Choice: main's hold sentence, then CR-428's destination/draft/formerly sentences.

## skills/chantier/scripts/cli/src/chantier/commands/forge_stack.py (`_plan` docstring)

- main: added "the dependents of an apart CR (to `<cr> waits with held <p>`)".
- CR-428: "moved to the backlog or the next batch, `3-ready`" instead of "the inbox or the backlog".
- Choice: CR-428's wording for the moved CRs, plus main's apart-dependents clause.

## skills/chantier/scripts/cli/src/chantier/declare/orders.py (`order` kind help)

- main: hold|unhold "(a live CR, or a ready CR of a stack, out of the slots and the order, and back)".
- CR-428: drop `--note trash|ready|P1..P4`.
- Choice: CR-428's drop notes plus main's hold text.

## Fast gate

`just check` (in the worktree, at 0f3dd8ce): pass, exit 0; 1622 passed, 20 skipped; release-notes ok.
Log: work/gates/conflict-resolver-check.log
