# A report tells blocked from waiting, with a legend and a short explanation

## Problem

A progress report draws every stopped CR in red, so a CR that needs the user's decision reads like one
that waits for work already on its way. Each row gives its own Driver's words, so one cause reads as
several, and the report has no legend.

## Change

In `skills/chantier/references/chief-of-staff.md`, the progress report:

- opens its table with a legend line of the icons it uses;
- has six icons, each with its word: ⚪ not started, 🟡 working, 🟠 waiting, 🔵 to review, 🔴 blocked,
  ✅ merged;
- draws 🟠 for a CR that waits for a thing already on its way, named: the stack driver, another CR, a
  slot; 🔴 for a CR that nothing moves until someone decides or repairs it;
- gives rows with one cause the same words, whatever each Driver wrote;
- has, under the table, a short explanation when a CR is 🟠 or 🔴: what it waits for, and who unblocks it.

The Chief of Staff judges 🟠 or 🔴 from the `blocked` text and the batch's state; the record does not
change.

## Out of scope

`status.py`, `hooks/register.tsx`, `3-requests/STATUS.md` and the board keep their icons: the record has
one `blocked` state, and telling the two apart there is a CLI change of its own.

## Done when

- The card says all of the above.
- `just check` passes. The change is to a card, so `just scenario` passes too.
