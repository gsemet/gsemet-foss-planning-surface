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
