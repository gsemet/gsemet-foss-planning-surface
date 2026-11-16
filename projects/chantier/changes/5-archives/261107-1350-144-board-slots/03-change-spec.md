# Change Specification: the CR board shows each batch's slots

## Goal

The CR board mod (`hooks/register.tsx`, a read-only pane over
`.agents/changes/3-requests/STATUS.json`) does not show how many slots a batch has, how many are
taken and how many are free. Each batch's header gets a line such as **"Slots 2/4, 2 free"**.

## What changes

### 1. `STATUS.json` (`skills/chantier/scripts/cli/src/chantier/status.py`, `dashboard_view`)

Each batch entry gains its slots: the total (the batch's slot limit) and the number taken,
computed exactly as `status` computes its "live n/m" (the same function, not a copy: the live
Drivers and the open orders that hold a slot, a QA order included). Additive keys, e.g.
`"slots": {"taken": 2, "total": 4}`; the schema version moves only if the file's own rule for it
says so. `STATUS.md` (the dashboard) may show the same in its batch heading.

### 2. The board (`hooks/register.tsx`)

In each batch's header, one line: `Slots <taken>/<total>, <free> free` (free = total − taken,
never below 0). A `STATUS.json` written before this change, without the key, shows no slot line
and no error. `hooks/register.test.tsx` covers both.

## Evidence

The mod's tests pass (`claude plugin test hooks` or the project's way, as `just check` runs it);
a `STATUS.json` from `status --refresh` on a batch with live Drivers carries the right numbers.
