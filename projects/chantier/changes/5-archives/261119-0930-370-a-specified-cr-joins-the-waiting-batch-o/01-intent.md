# A specified CR joins the waiting batch on its own

With an empty batch opened to wait for CRs (`open-empty-batch`), each CR whose specification
becomes final still needs its own `order add` and the user's go to join. The user opened the
batch for exactly that work: a CR made ready while it waits should join it automatically.

Wanted: in a batch opened empty, a CR marked ready (`triage <folder> --ready`) joins the batch at
once, as `order add` would, with no separate go; the relay to the Foreman (or the `take` in
direct mode) follows as usual.

Source: the user, 2026-11-18: « et une CR qui permet dans ce mode d'envoyer directement une CR
spécifiée dans le batch de manière automatique ».
Short name: `ready-joins-waiting-batch`
Depends on: `open-empty-batch` (same batch, below it in the stack).
