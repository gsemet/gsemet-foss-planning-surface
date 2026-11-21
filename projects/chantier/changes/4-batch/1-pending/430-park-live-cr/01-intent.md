# Park a live CR that waits on an outside step

From the batch-29 retro (kept point 2): CR-415 kept a slot and its stack place for five hours while it waited on the user's phone trial, because `order hold` takes only a ready CR. Intent: a live CR waiting on an outside step can be parked out of the slots and the stack, and brought back.
