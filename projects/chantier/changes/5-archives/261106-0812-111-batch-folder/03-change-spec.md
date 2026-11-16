# A batch is numbered, single and a stack by default

A batch is the CRs active at one time under one Foreman. It has no name, only a number, and a CR
added through the Foreman joins it. Run this CR only when no batch is open: there is no migration.

## The batch's identity

- Its id is `batch-<n>`, `<n>` on two digits from `.agents/changes/.batch-number`, which keeps
  counting all batches: the next one after folder `04-…` is `batch-05`.
- Its folder is `3-requests/batch-<n>/`; a CR's is `3-requests/batch-<n>/<number>-<slug>/`.
- A CR's branch is `chantier/batch-<n>/<cr>-<slug>`, its worktree
  `<repo>.worktrees/batch-<n>-<cr>`.
- `chantier open` takes no name: `open <prepared-folder>… [--default-branch] [--slots] [--budget]
  [--parallel] [--release N]`.
- `--batch` and `$CHANTIER_BATCH` take the number, `4` or `batch-04`.

## One open batch

`open` exits 2, saying which batch, while a batch is open, whatever its state until `close`.
New work goes to it with `order add`. The end does not change: no live CR left, `land`, then the
user's `close`.

## Slots

A batch's slots vary during its life, by `order slots`, as today. The default of `open --slots`
in `cli.py` goes from 2 to 4; the cards and the README follow where they give it.

## Stack by default

`open` makes a stack; `--parallel` makes independent CRs, and `--stack` goes. When a stack merges
only in part, what remains forms another stack in the same batch: the batch stays open, and the
stack driver restacks what remains on the default branch. A batch can so hold several stacks in
turn. A merged CR goes to `4-archives/` at once and alone, as it does today, even while its stack
is still live: nothing waits for the stack's end. Read `stack-driver`'s card and `driver.md` first; if the state or a rail cannot say this,
extend them, and report what you changed.

## Reusing the last Foreman

In `chief-of-staff.md`, step 4 of "Starting a batch": when the previous batch's Foreman session
still exists, even stopped, the Chief of Staff may send it the new Foreman prompt instead of
starting a session, with the next epoch. This is the way to start a batch under Remote Control,
where the host refuses a new session. A new session stays the default at the desktop: a reused
Foreman carries its old context, and the batch pays for it. The Foreman's card says that a new
prompt starts from the state alone, never from what it remembers of the last batch.

Before a reuse, the Chief of Staff always recommends that the user type `/compact` in the
Foreman's session, not `/clear`: compaction continues the same conversation, connected devices
follow it, and `chantier cost` keeps the Foreman's transcript, which `/clear` may replace. No role
can run it for them: it is typed by the person.

Claude Code's docs do not say a message reaches a stopped session, whose process has ended: they
describe waking it by a reply from the user. So a stopped Foreman is woken by the user, who
pastes the prompt into it. Prove on the host that the epoch claim works in a reused session, and
whether a message wakes a stopped one; the card says what was proved, and only that.

## What follows

- `skills/chantier/scripts/cli/src/chantier/`: `state.py`, `commands.py`, `status.py` and what
  reads the batch's id or folder name. `STATUS.json` keeps its fields, with `batch` and `folder`
  as `batch-<n>`; a folder of the old form in `4-archives/` or a CR's record stays readable.
- `scenario/run_scenario.py`, and the tests in `skills/chantier/scripts/cli/tests/`.
- The cards in `skills/chantier/references/` that name `<NN>-<batch>`, the batch's name or
  `--stack`, in particular `concepts.md`, `chief-of-staff.md`, `foreman.md` and `driver.md`.
- `README.md`, `docs/cr-folder-lifecycle.svg` and `docs/cr-folder-lifecycle-texts.md`.
- `evals/`: runbooks and `kit/audit.py` where they name a batch or call `open`.

## Done when

- `just check` and `just scenario` pass; the scenario covers the new names, a second `open`
  refused, an `order add` joining the batch, and a stack merged in part.
- `grep -rn "<NN>-<batch>" skills docs README.md` finds nothing.
