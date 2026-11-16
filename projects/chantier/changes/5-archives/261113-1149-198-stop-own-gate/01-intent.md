# A Driver stops its own long gate by a named means, never with `cancel`

## The problem

In batch-11 (2026-11-11) CR-183's Driver had a long gate running when a rebase note arrived. The
gate's result could no longer count (the head was about to move), so the Driver wanted it
stopped, found no means for that in its card, and ran `chantier cancel CR-183`: the gate stopped,
and the CR was cancelled and moved to the trash with its work. `cancel` is the steering session's
command for a CR the user dropped.

## Where it shows

- `skills/chantier/references/driver.md`: the long gate bullet says how to run a gate and nothing
  on stopping one; "stop only one you started, by its id" is the only nearby rule; `cancel` is
  not named at all, so nothing forbids it to a Driver.
- That nearby rule does not work for a gate: `gate` starts the suite in its own process group
  (`commands.py`, `gate`), so ending the `gate` command leaves the suite running, and the next
  long gate of the repository waits for that process, up to an hour (`_LongGateLock`).
- The only code that stops a running suite properly is inside `cancel` (`procs.stop_group` on the
  group the lock names), bound to cancelling the CR.
- `cancel` takes `--epoch` but does not require it (`state.check_epoch` returns on a missing
  epoch): a bare `chantier cancel <cr>` from any agent is accepted.

## What would fix it

- A named CLI means, on the `gate` command, that stops the running long gate of the CR it is
  given: it stops the suite's process group, frees the gate for the next CR, records the run as
  stopped (no pass, not a failure of the code) and changes nothing else in the CR's state. It
  touches only a gate the lock names for that CR.
- driver.md, the long gate bullet: when a Driver stops its own gate (its result can no longer
  count because the head will move, or the steering session said `stop`), by that means only;
  and one sentence: `cancel` is the steering session's command on the user's drop, never a
  Driver's, whatever the reason.
- `cancel` without `--epoch` is refused, as the steering commands' rule already implies.

This is a CLI addition from a measured incident (a CR lost with its work), inside the CLI's
scope (the batch's frame and its gate), not a speculative tool.

## Out of scope

- Any change to what `cancel` does for the steering session.
- Recovering CR-183 or any CR cancelled by mistake (`restore` exists).
- Stopping CI, a worker, or any process other than the long gate.
- A timeout on a gate that hangs.
- The agent files of both hosts: the contract lives in the card.
