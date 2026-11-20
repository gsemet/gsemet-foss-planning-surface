# Mutation Testing Driver: one-shot campaign for redundant tests and holes

Priority P2, later: grill and specify after Studio's working case (its batch-07 P1). From the user, relayed by the Studio project's Chief of Staff, 2026-11-20, corrected the same day. The user's words, on the correction: "je te demande qqu chose de one-shot et tu me dis que c'est PR par PR".

A new role, the **Mutation Testing Driver**, a sibling of the QA Driver: **one-shot**, not a check on every PR. Like the QA Driver, it runs one campaign on the project's head:

- it runs the project's mutation tool over the existing code and tests;
- it finds the **redundant tests** (they kill no mutant that other tests do not already kill), to remove or merge, so the suite gets **smaller**;
- it finds the **holes** (surviving mutants in code that matters), each calling for a test to add.

Constraints: a requirement marker never loses its coverage (the marker moves to a kept test), and no published requirement is removed. The project gives the tool, the scope and the budget; chantier adds no tool.

**First case.** Studio is the first project: its batch-07 P1 sets up StrykerJS on `node:test`. It ends with a note for chantier: the command, the scope, how the report was read, the rules for removing a test, and the time taken. Grill and specify chantier's side from that note.

## The user's answer (2026-11-20)

"yes": the one-shot campaign holds, the suite may get smaller. The user's words: "ce sera le harnais projet qui definira les tests et mutation a faire, mais le driver lui peu accompagner les gens pour determiner la campagne adaptee, faire ce mutation, corriger quand ca coute pas cher, ouvrir des findings quand cest plus grave. le Studio va faire un premier essaye et te rendre. tu devras faire en sorte de stocker quelque chose de generalisable. il faudra mettre dans la doc et les svg."

- **The project's harness defines** the tests and the mutations to run (tool, command, scope, budget): chantier adds no tool.
- **The Driver accompanies the people** to choose the campaign that fits the project, runs it, **fixes what is cheap** (removes or merges a redundant test, adds an obvious missing test), and **opens findings** for what is more serious, as the QA Driver does.
- **Generalisable:** Studio runs the first trial and hands its note back; the Chief of Staff keeps from it what holds for any project (the role's card, the project interface it reads, the campaign's steps and its report), not Studio's specifics.
- **Docs and diagrams:** the role goes into chantier's docs and its SVG diagrams, beside the QA Driver.
