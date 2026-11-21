# Park a live CR that waits on an outside step

In batch-29, CR-415 (eval operator from the phone) waited on an outside step (the user's phone trial) with no Driver at work, yet it kept a slot and its place in the stack from 22:18 to 03:38: `order hold` takes only a ready CR, not a live one. The slots were raised three times around it (O-68, O-70, O-73), and in the end it was dropped to P2 with its work.

Wanted: a way to park a live CR that waits on something outside the batch, so it stops holding a slot and the stack, and to bring it back later.

Source: batch-29 retro, kept point 2 (the retro critic kept it).
