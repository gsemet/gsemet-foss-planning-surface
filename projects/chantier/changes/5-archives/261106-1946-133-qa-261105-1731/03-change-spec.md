# The CLI's errors say what happened and what to do

## Problem

`findings.md`, in this folder, lists what a QA run found. Exit codes, messages and a few accepted
calls mislead a new user.

## Change

Replay each finding on the current code, in a throwaway repository, and fix those that remain:

- `file` of an existing slug exits 2 and its message names `--slug`.
- `triage` of a backlog item moves it to the new priority; a path that is neither inbox nor backlog
  says which it expects.
- A second `order drop` of a CR is refused with "already dropped", and records no order. The CR
  arguments of `order` accept `101` as well as `CR-101`.
- `order note` on a cancelled CR is refused.
- `order rounds` and `order budget` errors give the full usage and why the value is refused.
- `status` tells an order the CLI has applied, which the Foreman still has to mark done, from one
  nothing has touched yet; `land`'s refusal says how such orders end.
- `open` says where each folder moved and what comes next. The refusal of a QA folder says it is an
  item to triage and split, not to open.
- `docs/use-cases.md` says what `cost` and `close` answer on a batch with no Foreman yet, that a
  dropped CR shows as `cancelled`, and that the path through `land` and `close` needs a Foreman.

`close` keeps refusing when it cannot price the batch: that refusal is wanted (CR-130).

## Out of scope

New commands, and any change to what `rails.py` refuses beyond the above. The CLI stays free of
dependencies, and its output stays within its ten lines.

## Done when

- Each finding is fixed, or the PR says why it no longer holds, with the command that shows it.
- `just check` and `just scenario` pass.
