# Brief prints host rows by name only, so sessions boot lighter

Asked by the owner, 2026-11-27, verbatim: « ouvre un batch et lance ces 7 CR » (open a batch and launch these 7 CRs). Part of the card cleanup, plan steps 1 to 3.

Source files, in the planning folder, under `2-backlog/P1/card-inventory-open-rows/`: `work/fable-review-plan.md` (the plan), `work/fable-review-verdicts.md` (one verdict per file), `02-answers.md` (the owner's decisions, card-cleanup-Q1 to Q5), `intake/owner-cleanup-2026-11-27.md` (the owner's words). The plan is a proposal: its facts are checked against the base before they are used, and its "exists?" claims about what the CLI already prints are not verified.

## Wanted (plan section 6, step 3, item 4; section 4.2, level 0)

`chantier brief` prints the host rows of a role by name only, in a line, instead of their whole text. `chantier host <capability>` prints a row as today. Every card or CLI line that relied on the row being in the brief ("as the host row says") names the command that prints it, at the moment it is needed; a row that protects the user stays reachable from the line of its moment. Lower the ceilings of `skills/chantier/scripts/cli/tests/test_brief_bytes.py` to the new sizes (today: chief-of-staff 24,400 bytes, foreman 22,600).

Out of scope: rewriting the rows or the cards.

Proof: `brief chief-of-staff` and `brief foreman` are each under 9 KB; `host <capability>` prints what it printed; `just check` passes.
