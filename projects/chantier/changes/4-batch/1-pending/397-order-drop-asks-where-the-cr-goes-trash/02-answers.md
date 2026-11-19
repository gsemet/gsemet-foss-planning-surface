# Answers

1. Q: Is the trash the only way out of a batch? User, 2026-11-20: "attend, ca veut dire que la
   seule possibilite pour sortir des CR d un batch c'est la poubelle ? il faut demander la
   destination: poubelle, inbox, backlog. Typiquemetn backlog pour les tache deleguees et
   poubelle pour les tache annulees. => rajoute une CR pour ca".
   Destination asked: trash, inbox or backlog; backlog for delegated tasks, trash for cancelled ones.

- Priority: user, 2026-11-20: "oui" to P1, together with its neighbour (drop destination and holding a ready CR out of the stack); then "relance un foreman avec les inbox et les p1".

## Settled by the Chief of Staff (2026-11-20, the user asks no questions)
- Grilled enough: the intent is the grill. The user's go, 2026-11-20: "relance un foreman avec les inbox et les p1"; this CR joins batch-29 (factory, stack) once specified.
- Spec question 1, the CR's number (Settled by the Chief of Staff, 2026-11-20): a CR moved out to the inbox or the backlog keeps its number. Its folder and the record carry it, and when it joins a later batch it gets the same number back (CR-381 stays CR-381); the number is never given to another CR.
- Spec question 2, its branch and PR when it comes back (Settled by the Chief of Staff, 2026-11-20): its new Driver picks up the existing branch and open PR (rebased on the new base), as the user wanted for #346 and #347; it starts fresh only when the branch is gone.
- Spec question 3, a trash drop outside a stack (Settled by the Chief of Staff, 2026-11-20): the steering session (the Foreman, or the Chief of Staff in direct mode) closes the PR, prompted by the drop's line; the CLI itself runs no forge write.
- Spec question 4, a PR moved out of a stack (Settled by the Chief of Staff, 2026-11-20): it goes to draft and onto the default branch, as a held PR does in the neighbour CR, so it is never merged by accident with the PRs below it.

## Spec-critic findings (settled by the Chief of Staff, 2026-11-20, the user asks no questions)
- 10. Split: this CR keeps the drop's destination (trash, inbox, backlog), the folder move with its number reserved (`restored.json`), `close`, the labels, the `forge-stack` wording and the trash PR close. The come-back (same number, branch and PR at `add_cr`, the same-batch reopen, `formerly.json` consumed, the Driver card bullet) moves to a new CR, `1-inbox/order-drop-come-back-same-number-branch-pr`. This CR still writes `formerly.json` at the drop (where the CR came from, with `pr_draft`), for the new CR to read and consume.
- 1. A moved-out CR whose PR the user merges later: on "I merged #n" the Chief of Staff adds it to the open batch and records the merge (`order add`, then `order merged`); the Driver card treats a recorded PR found merged as "nothing to do, ask the Chief of Staff". Goes to the new CR.
- 2. Every `cancel` and bare `order drop` call site of the scenario and the tests is listed in the Evidence; chief-of-staff.md's restart line (orphan processes) no longer uses a bare `cancel`.
- 3. A PR moved out of a stack reaches the default branch through `forge-stack rebuild`, which reads the moved-out PRs from the record, as the neighbour's held PR; no retarget by hand; the rule "never retarget a PR by hand" stays true.
- 4. `gh pr close*`, `gh pr reopen*`, `glab mr close*`, `glab mr reopen*` join the P10 allow rules (`commands/permissions.py`, group "batch").
- 5. A release CR or a fix CR leaves a batch only to the trash: `order drop` refuses another destination for them and says so.
- 6. A reopen resets every per-round and stack field; `pr_draft` is carried by `formerly.json`. Goes to the new CR.
- 7. This CR clears `held` at the drop (the neighbour, CR-394 in batch-29, defers the drop to this CR). A drop of a held CR needs no `take stack` (its PR is already a draft on the default branch). `_dropped` reads `left_to`, so a held-then-moved PR prints "moved to …".
- 8. Reopen a closed PR before any push to its branch; "GitHub refuses to reopen after a force-push" is marked unproved. Goes to the new CR.
- 9. In `batch-NN.json` a moved CR's `archive` is null, with `to` beside it; the `close` line names the folder, or says "moved since" when the recorded path is gone; no "cost final" STATUS files are written into a backlog or inbox folder.
