# The batch pauses when its last CR merges, and the close is offered

In direct mode the Chief of Staff skipped chief-of-staff.md "The pause" after the last merge (remove the merged worktrees and branches, retro, `pause`) and never offered the close; the user had to ask, and `close` refused "running, not paused". The user's words (French, translated): "as it is finished it must have been paused automatically, and you should have cleaned what had to be cleaned and asked me whether I want to close the batch." Long-term fix: the last `order merged` / `handback` of a batch prints the pause as the next step, `status` and the heartbeat flag "every CR merged, not paused", and the Chief of Staff offers the close at once.

From the retro of batch-22 (2026-11-17, kept by the retro critic; record: 5-archives/batches/batch-22.md). The user asked to treat every kept point in the next batch. Priority: P1, the user's word.
