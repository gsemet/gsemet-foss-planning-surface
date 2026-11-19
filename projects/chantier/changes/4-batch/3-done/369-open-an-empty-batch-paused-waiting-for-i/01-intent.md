# Open an empty batch, paused, waiting for its first CR

On 2026-11-18, after batch-27 closed, the user asked for a new batch with a new Foreman, waiting
for a CR still to be written. `chantier open` refused: it needs at least one prepared CR, and
`3-ready` was empty. The batch, its Foreman and the stack it will hold had to wait for the first
spec, though the user had already given the go.

Wanted: `open` with no CR opens the batch directly paused; CRs then join it with `order add` as
their specs become ready, and the first `take` sets it running, as for any paused batch.

Source: the user, 2026-11-18: « fait une CR qui permet de faire un batch vide directement en
pause ».
Short name: `open-empty-batch`
