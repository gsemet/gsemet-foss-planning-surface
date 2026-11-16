# A batch closes only when nothing runs

## Intent

A batch's cost is only worth reading if nothing spent after it was taken. So a batch cannot end while
a Driver of any kind (CR, stack, QA, release, a user's own) or its Foreman is still active. Once all
is finished, it closes on the user's approval, as today.

## Why now

On batch-06, `order add` was accepted 27 s after `land`: CR-129 ran on a landed batch, and its spend
and the Foreman's after landing are in no figure.

## Open questions, with the recommended answer

1. What proves an agent is no longer active? Recommended: the CLI refuses on recorded state, and on
   a transcript of the Foreman or a Driver that wrote within the last few minutes, so the proof holds
   on both hosts and needs no host API.
2. `order add` on a landed batch: reopen it or refuse? Recommended: reopen it, `land` runs again.
   The card's "new work joins with `order add` until `close`" stays true and the spend keeps counting.
3. When is the cost final? Recommended: at `close`, once nothing runs, so the Foreman's work after
   `land` counts; `land` prints it as not final.
