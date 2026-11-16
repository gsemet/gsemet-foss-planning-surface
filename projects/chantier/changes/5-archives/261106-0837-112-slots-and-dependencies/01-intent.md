# Intent

Redesign what a slot is and how one CR depends on another, in a small CR.

Today a slot is a CR in the state `working`: `take` is refused past the limit, and a `ready` or
`blocked` CR holds none. chantier has no dependency between CRs: the state records none, the
Foreman picks the next CR by judgement, and the order of a stack is set only by the stack driver,
late, with `$CHANTIER stack <cr>…`.

It builds on `batch-folder` (one open batch, stack by default, 4 slots by default).
