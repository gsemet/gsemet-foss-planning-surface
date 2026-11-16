CR-111. A batch is the CRs active at one time under one Foreman: it has a number, no name.

## What changes

- **Identity:** a batch is `batch-<nn>`, numbered from `.batch-number`; folder `3-requests/batch-<nn>/`, branch `chantier/batch-<nn>/<cr>-<slug>`, worktree `<repo>.worktrees/batch-<nn>-<cr>`. `open` takes no name; `--batch` and `$CHANTIER_BATCH` take `4`, `04` or `batch-04`.
- **One open batch:** `open` exits 2, naming the batch, until `close`. New work joins with `order add`.
- **Slots:** the default of `open --slots` goes from 2 to 4.
- **Stack by default:** `--parallel` makes independent CRs, `--stack` goes. A stack merged in part leaves a new stack in the same batch, restacked on the default branch; `take stack` prints each CR's base. Release and fix CRs sit outside the stack; `order add` goes on top.
- **Reusing the last Foreman:** the previous Foreman's session may be reused, even stopped, after recommending `/compact`: an idle one gets the new prompt by a message, into a closed one the user pastes it. A reused Foreman claims the batch's epoch, 1 for a new batch, which starts at 0; it does not continue the old Foreman's.

## Host proof

The Foreman of the batch that built this PR is the proof, as the user answered: `foreman set --epoch 1` was accepted in a reused session, and a Chief of Staff's message started a turn in an idle one. A closed session stays unproved. The card states exactly that.

## Checks

- `just check` and `just scenario` pass at this head, on Windows; CI runs them on the other platforms.
- The scenario has a new case: the new names, a second `open` refused, an `order add` joining the batch, a stack merged in part.

An old live `NN-name/` batch folder is no longer found by `--batch`: run this with no batch open, there is no migration.
