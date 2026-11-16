# Intent: pause a batch to grill, then add the grilled CRs to the same batch

The user's idea, filed during batch-08 (steered in direct mode), to be grilled once that batch
completes.

A direct batch is strict today, as CR-140 specifies: no CR joins it while it runs, because the
Chief of Staff holds no grill while it steers. The user proposes a clear mechanic instead: ideas
that come in while the batch runs are stacked in the inbox; when the running work is done (or at
a chosen moment), the batch is **paused**, the Chief of Staff grills the stacked ideas with the
user, and the grilled CRs are added to the **same batch**, which then resumes. The one exception
is a release CR, which needs no real grill and may join without a pause.

Facts at filing time: a batch's record has a `status` (`open` until `close` deletes it, with a
`landed` time once `land` ran); `status` shows whether Drivers are live. There is no paused
state.

To grill: what "paused" means for running Drivers (finish, or stop and resume); who may pause
(the user's word only?); whether it also applies to Foreman mode; how it changes CR-140's
"strict batch" rule and `order add`'s refusal on a direct batch; the release exception's limits.
