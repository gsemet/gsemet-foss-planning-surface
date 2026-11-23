# Slim session-start.md: split by role, forge-neutral, sync card

Filed on the owner's words of 2026-11-23, relayed by the Chief of Staff of okf-schema. To grill later with the owner, not now.

The owner's words (French), after a Chief of Staff start in a planning surface: "il y a plusieurs problemes rien que dans cette procedure d'initialisation : le session-start.md est enorme. La section 1 est bonne. La section 2 est tres detaillee, peut etre trop, pour chaque role ET il y a des references directes a gh ou glab. Le but est que chantier soit abstrait et que l'on puisse etendre facilement a d'autres forges plus tard. La partie 3 n'est pas utile pour les coder, driver, ..., uniquement CoS, foreman et griller. La partie sync the checkout est hyper detaillee pareil, ca devrait etre dans un document de reference car seul le chief of staff est concerne par ca."

In short, `skills/chantier/references/session-start.md` (about 29 KB, read at each session start) should shrink and split:

- Section 1 (start checks): keep as is.
- Section 2 (the seat and the role): too detailed and written for every role at once; it names `gh` and `glab` directly (the board's forge reads, among others). chantier should speak of an abstract forge so another forge can be added later. Split it by role (Chief of Staff, Foreman, Griller), each reading only its part.
- Section 3 (titles): only the Chief of Staff, the Foreman and the Griller need it, not the coder, the Driver and the other workers; it must not be in what they read at start.
- Section 6 (sync the checkout): only the Chief of Staff in the dev mode is concerned; move it to its own reference card, read only when a sync runs.

Related, not the same: the inbox CR "Slim the startup cards of the Chief of Staff, Foreman and Driver" (the same care: the right instruction at the right moment, nothing lost). This one is the session-start card and its forge wording.
