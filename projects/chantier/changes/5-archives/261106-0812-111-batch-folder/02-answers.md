# Answers

Given by the user on 2026-11-06, in the Chief of Staff's session.

- **Folder:** `.agents/changes/3-requests/batch-<n>/<cr>-<slug>/`, for example `batch-01`.
- **Name:** the number alone. `open` takes no name; `--batch` takes the number.
- **Open batches:** one. Its purpose in fast production is to deliver a stacked PR.
- **Partial merge:** when a stack merges only in part, what remains forms another stack in the
  same batch. Several stacks, one batch.
- **Merged CR:** it can be archived while its stack is still live.
- **Reuse:** a new batch can reuse the previous Foreman if its session is there, even stopped;
  useful above all under Remote Control.
- **Before a reuse:** always recommend that the user clear the Foreman's context; `/compact`, the
  safer of `/compact` and `/clear`.
- **Slots:** variable during the batch, 4 by default.
- **Mode:** stack by default; independent CRs stay possible.
- **End:** as today: no live CR left, `land`, then the user's `close`.
- **Specification:** approved on 2026-11-06, priority P1.
- **When:** after the running batch. No migration: `03-eval-real-050` and `04-cr-board` are
  closed first.

Ask A-1, answered by the user on 2026-11-06:

- **Merging during this batch:** PR 48 is not held. The main checkout, where the plugin loads
  from, stays at `f378d8b` until `close`, so this batch keeps the old CLI; nobody updates it
  before then.
- **Host proof:** the Foreman of this batch is the proof. `foreman set --epoch 1` was accepted in a
  reused session, and a Chief of Staff's message started a turn in an idle one. A closed session
  stays unproved. The card states exactly that, and the PR waits for no other proof.
- **Epoch:** a reused Foreman claims the epoch of the batch, 1 for a new batch, which starts at
  0; it does not continue the old Foreman's. The card's wording says so.
