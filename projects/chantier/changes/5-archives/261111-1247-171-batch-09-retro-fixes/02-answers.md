# Answers

## 2026-11-11, before filing

- Points kept: "Le 6 oui je le veux. 7 ok tu peux discard." Points 5, 8, 9, 10, 11, 14 and 16
  are kept as well. Points 15 (Auto-fix) and 17 (the BOM) are left out.
- Asked how the gates work: "Donc, le CLI donne les portes à passer comme des check list c est
  ca ?". The answer given: `take` lists the two gates, and `handback ready` refuses when one is
  missing.
- Asked where the gates are stored: "C'est traduis sous quelle forme dans un fichier ? Un json".
  The answer given:
  - the gate and verdict events go in `events.jsonl`, and the PR's head in `batch.json`;
  - a new `verdict` command records the verdict.
- The eight points in one CR: "Une seule CR".

## 2026-11-11, grill

1. **The hook on a worker's write outside its worktree.** It refuses the write; it does not
   only warn. (The user chose "Il refuse".)
2. **A CR the project's rules exempt from the long gate (docs only, here).** The Driver passes
   `handback ready --no-gate "<the project's rule>"`. The exemption is logged and shown in the
   report, and the verdict `VERIFIED` stays mandatory. (The user chose "Dispense avec raison".)
3. **The Copilot host.** Part 1 applies to Claude Code only, and Copilot stays as it is. Nothing
   is added there, not even the Driver's check of the main checkout. (The user chose "Claude
   Code seulement".)
4. **Priority.** P1. (The user chose "P1".)
5. **The Driver's check of the main checkout.** Dropped: the hook's refusal is enough. The
   Chief of Staff proposed it in the restatement, and the user answered "Ok de le retirer."
6. **Grilled enough.** "Tu peux la lancer": the spec-writer is started.

## 2026-11-11, the spec-writer's open questions

7. **Q1, who runs `verdict <cr> VERIFIED`.** The Verifier itself, at the head it verified, as it
   already runs `gate`. (The user chose "Le Verifier".)
8. **Q2, NOT VERIFIED.** Yes: `verdict` also records `NOT VERIFIED`, and the last verdict at a
   head decides. (The user chose "Oui, le dernier décide".) As the Chief of Staff said in the
   question, a skipped pass on the PR description is still not caught by the CLI; it stays the
   Driver's judgement.
9. **Q3, a project with no long gate at all.** The user's words: "Le driver peut, sous
   vérification du foreman ou le cas échéant du chief of staff, que le projet a vraiment pas de
   gate long. Il faudra expliquer les bonnes pratiques à avoir pour que l'utilisateur sache ce
   que c'est une gâte courte et longue, comment les déclarer dans le AGENTS.md ou faire déclarer
   par chantier". Read as:
   - The Driver may use `--no-gate`.
   - The steering session (the Foreman, or the Chief of Staff in direct mode) verifies that the
     project truly has no long gate.
   - The docs explain the good practice: what a short gate and a long gate are, how to declare
     them in `AGENTS.md`, or how to have chantier declare them.
10. **Q5, the hook's scope.** Not answered: "Je ne comprend pas ce que tu veux faire avec ces
    hook. Reexplique moi". The Chief of Staff explains it again.
11. **Q5, after the explanation.** The hook guards workers only, and only their Write and Edit.
    Drivers and shell writes stay out. (The user: "Ok pour les 2".)
12. **Q4, QA drivers in `cost`.** A QA driver keeps its own Driver line; it does not go on the
    steering session's line. (The user: "Ok pour les 2".)
