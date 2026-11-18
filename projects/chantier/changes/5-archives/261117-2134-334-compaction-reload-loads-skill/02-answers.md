# Answers

- The user (2026-11-17): after a compaction, the session must load its role's skill again, not only
  the short cores. A message added by the `session.compact` hook that says so is enough.
- The user (2026-11-17), the wording: plain and short, of the form "You are the <ROLE> in a chantier
  session; after this compaction, call the skill <skill> now." It replaces today's `RELOAD_LINE`.
- The user (2026-11-17): add it to the running batch (batch-24).

## Grill after the spec critic (2026-11-17)

- reload-Q1 (the role changed by the user's word or a fork, the atom still names the old one): the
  reload follows the seat. The skill called with `reload` reads `$CHANTIER seat` first; if the seat
  contradicts the message's role, the session loads the other role's skill with `reload`.
- reload-Q2 (the router is itself named `chantier`, so "your chantier skill" may resolve to it): the
  router delegates. The router called with `reload`, in a session whose `roles` atom (or seat) holds a
  role, loads that role's skill with `reload`; so the reload works whichever skill the model picks.
- reload-Q3 (calling the chief-of-staff skill reopens the pane on its first page): no. A
  `skill.prompt` whose argument is `reload` leaves an open pane as it is.

## Settled by the Chief of Staff

- A free seat at a reload (e.g. after "become a griller" ran `seat leave`) while the message names
  the Chief of Staff: the session reloads as the Griller (a reload takes nothing, so no seat), and
  says in its reload line that the seat is free; the user may say "become chief of staff".

- The user (2026-11-17), superseding the Chief of Staff's first settlement: the message does not
  name the skill; the model knows its installed skills and finds the one for its role. The message
  names the role only (from the `roles` atom: the last role skill loaded, `chief-of-staff` or
  `griller`, the router `chantier` only when alone), e.g. "You are the Chief of Staff in a chantier
  session; after this compaction, call your chantier skill again with the argument reload."
- The argument: the skill is called with `reload`; `chief-of-staff` and `griller` then follow
  `session-start.md`, "5. Reload", like the router: read only, no role question, no introduction, no
  batch change, one line saying the rules were reloaded.
- Router alone (no role yet): "You are in a chantier session; after this compaction, call your
  chantier skill again with the argument reload." (the spec-writer's proposal, kept).
- "the Griller", as in the user's example ("You are the <ROLE>"), like "the Chief of Staff".
- Unchanged: the hook's conditions (main loop only, `manual` or `auto` trigger, a role skill loaded,
  never skips a compaction); the pane is not touched, so no pane screenshot.
- Gates: `just mod` before the PR (a change to `hooks/`), `just check`, the pipeline's
  `just scenario (ubuntu-latest)` green at the PR's head if the cards change.

## During the batch (2026-11-17)

- reload-Q4 (the engine's `skill.prompt` event carries no argument, so the hook cannot see`reload`): the user does not mind the pane going back to its first page after a compaction. reload-Q3 is dropped; the pane behaves as today on any skill load.
