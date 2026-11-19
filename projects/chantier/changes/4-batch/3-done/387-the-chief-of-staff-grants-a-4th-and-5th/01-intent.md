# The Chief of Staff grants a 4th and 5th round when the batch caused the red

## The user's words (2026-11-19)

> Oui tu as le droit dans ces cas là de donner un 4 eme et un 5 eme tour il faut que tu l'encode

"These cases" is batch-28's CR-383: its 3 rounds were used; after the Chief of Staff's restack (A-19)
moved CR-375 under it, the pipeline's `just scenario` went red on two surface-board checks that
still expected the watcher's old last line. The fix was scenario-only. The Chief of Staff issued
`order rounds CR-383 --note 4` as its own call; the Foreman rightly held it, since the cards say the
round limit is the user's (`chief-of-staff.md` ~967 and table row G ~1486, `concepts.md` ~606).
The whole batch then waited on the user for a trivial fix.

## What changes

The round limit stays the user's, with one exception the Chief of Staff applies on its own:

- It may grant a CR's 4th round, then its 5th, never beyond, when the round that ran out failed on
  a red the batch itself caused, not on the CR's own work failing to converge: a restack or a
  rebase onto another CR's branch, ordered by the Chief of Staff, the Foreman or a stack driver; a
  CR merged or moved below it.
- It says so to the user in the same message, with the cause, and the order's note names the
  exception, so the Foreman can take it without the user's word.
- Any other blocked-rounds hand-back, and any round past the 5th, stays the user's word, as today.

## Where

- `skills/chantier/references/chief-of-staff.md`: the `order rounds` line (~967) and table row G.
- `skills/chantier/references/concepts.md`: the escalation row (~606), "the round limit stays the
  user's".
- `skills/chantier/references/foreman.md`: the Foreman takes such an order without the user's word
  when its note names the exception.
- Whether the CLI should check the order's reason is for the spec; the CLI knows no role today.
