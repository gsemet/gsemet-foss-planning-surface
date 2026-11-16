# Intent: a direct mode, a batch run by the Chief of Staff with no Foreman

The user wants a way to run a batch where no Foreman session is started: the Chief of Staff
starts and steers the Drivers itself, with the same CR lifecycle, the same batch frame (`open`,
slots, rounds, budget, `land`, `close`) and the same hand-backs.

Why: the Foreman needs a host that can start a separate session (today preflight's P1 asks for
Claude Desktop), so a terminal or VS Code host refuses every batch; and for a small batch a
whole Foreman session costs more than the work it steers.

What it changes, as grilled so far (see `02-answers.md`): the hard rule "you start no Driver and
never message one" becomes a rule of Foreman mode only; in direct mode the Chief of Staff does
the Foreman's job until the batch completes and holds no grill or discussion meanwhile.

To be processed after the init CR (`chantier-init-tour`), on the user's word. No specification
yet: it is written when this CR is refined.
