# A batch is numbered and dynamic

The user sees a batch as the CRs active at one time under one Foreman, not as a named set chosen
upfront: a CR added to the Foreman joins the same batch. A name then soon stops being true, and
`3-requests/04-cr-board/` reads like a CR, not like a batch. In fast production a batch's purpose
is to deliver a stack of PRs.

So a batch loses its name and is `batch-<n>`, one is open at a time, and its mode is a stack by
default. This changes the CLI that runs batches, so it waits until no batch is open.
