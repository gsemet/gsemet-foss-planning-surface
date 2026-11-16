A merge may come at any moment, one PR at a time, in any batch shape

From batch-16's retro (points 5 and 12), reviewed by an advisor. The user (2026-11-13): "I may merge
little by little, so you and the Driver must be flexible."

- Root cause: the cards describe one merge path per shape. chief-of-staff.md (around 552-563) knows only
  the one-action stack merge; foreman.md (around 152-161) starts the stack driver only once every open
  CR is ready. In batch-16 the user merged each stack PR on its own, so the stack driver and
  `forge-stack` never ran, and the Foreman improvised rebase notes.
- Fix: no merge path is fixed at the go. The Chief of Staff offers each PR on the default branch as
  mergeable now, once its Driver has handed back ready. The Foreman picks, per recorded merge, a rebase
  note for the working Drivers or a restack.
- Point 12: CR-215 was merged while its Driver was still finishing (`gh pr ready`, a body edit), so its
  `ready` hand-back was refused (commands.py around 1916). The Chief of Staff says "you can merge" only
  after the ready line. A Driver whose hand-back is refused because its CR is merged notes what it left
  undone and ends. The CLI keeps the refusal; at most its text gets clearer.
- Lands: cards (chief-of-staff.md, foreman.md, driver.md).