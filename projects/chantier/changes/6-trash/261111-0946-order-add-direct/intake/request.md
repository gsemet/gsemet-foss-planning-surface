# `order add` queues a CR on a running direct batch

Batch-09 retro, 2026-11-11 (`4-batch/retro.md`, point 8), kept by the user as a friction that
costs time and tokens.

## What happened

The user asked to encode a rule (it became CR-170) while CR-165 was running. `order add` was
refused on the running direct batch ("strict"), and `pause` needs every CR merged: CR-170 had to
wait for the user's merge of CR-165, then a pause, then an add.

## What main says today (fde3da8)

In Foreman mode `order add` queues a CR for the Foreman; on a running direct batch it is refused.

## Proposed fix (to grill)

`order add` on a running direct batch queues the CR as it does in Foreman mode; the Chief of
Staff takes it when a slot frees.
