# Intent: a clear batch lifecycle, ending in a pause

## Problem

The cards do not say one thing about how a batch ends. In `chief-of-staff.md`, direct mode:
"The pause" says that after `land` the batch is paused, inbox ideas are grilled and added with
`order add`, and `close` stays the user's word; but "The end" says `land`, then the `close` flow
of Landing, and the Completion report ends with "For you: closing the batch". `concepts.md` says
one batch is open at a time until the user's `close`. The Chief of Staff read this as: all CRs
merged, then land, then offer the close. The user wants the batch paused when everything is done.

## Wanted

One lifecycle, stated once (in `concepts.md`) and followed by every card and the CLI: open,
running, landed = paused when every CR is merged or cancelled, running again on `order add`, and
closed only on the user's explicit word. The reports at the end of a run say the batch is paused,
not that it awaits closing.
