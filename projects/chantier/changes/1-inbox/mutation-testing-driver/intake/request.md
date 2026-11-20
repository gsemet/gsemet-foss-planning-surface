# Mutation Testing Driver: one-shot campaign for redundant tests and holes

Priority P2, later: grill and specify after Studio's working case (its batch-07 P1). From the user, relayed by the Studio project's Chief of Staff, 2026-11-20, corrected the same day. The user's words, on the correction: "je te demande qqu chose de one-shot et tu me dis que c'est PR par PR".

A new role, the **Mutation Testing Driver**, a sibling of the QA Driver: **one-shot**, not a check on every PR. Like the QA Driver, it runs one campaign on the project's head:

- it runs the project's mutation tool over the existing code and tests;
- it finds the **redundant tests** (they kill no mutant that other tests do not already kill), to remove or merge, so the suite gets **smaller**;
- it finds the **holes** (surviving mutants in code that matters), each calling for a test to add.

Constraints: a requirement marker never loses its coverage (the marker moves to a kept test), and no published requirement is removed. The project gives the tool, the scope and the budget; chantier adds no tool.

**First case.** Studio is the first project: its batch-07 P1 sets up StrykerJS on `node:test`. It ends with a note for chantier: the command, the scope, how the report was read, the rules for removing a test, and the time taken. Grill and specify chantier's side from that note.

To confirm at the grill: the first relay quoted the user as "... et pas on va faire du mutation testing pour reduire le nombre de test actuels", which reads against removing tests; the correction says the campaign makes the suite smaller. Ask the user which holds.
