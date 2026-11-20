# Answers

- Priority: user, 2026-11-20: "oui" to P1, together with its neighbour (drop destination and holding a ready CR out of the stack); then "relance un foreman avec les inbox et les p1".

## Settled by the Chief of Staff (2026-11-20, the user asks no questions)
- Grilled enough: the intent is the grill. The user's go, 2026-11-20: "relance un foreman avec les inbox et les p1"; this CR joins batch-29 (factory, stack) once specified.
- Spec question 1, a held PR on the forge (Settled by the Chief of Staff, 2026-11-20): it goes to draft and onto the default branch, so it cannot be merged with the PRs under it by accident; that is what the user did with #346 and #347 at batch-28's end.
- Spec question 2, a release while a CR is held (Settled by the Chief of Staff, 2026-11-20): keep the release last. A held CR blocks the release; when the user asks for a release with a CR held, the Chief of Staff says so and offers to unhold it, or to take it out of the batch to the backlog (the neighbour CR `order-drop-asks-where-the-cr-goes-trash-`).
- Spec critic findings (Settled by the Chief of Staff, 2026-11-20, the user asks no questions):
  - A. While a CR is held, the Foreman does not start the release (final-order take, release take): it relays to the Chief of Staff, who proposes unhold or moving the CR out of the batch.
  - B. `stack --out-of-draft <held cr>` is refused ("unhold it first").
  - C. On hold, the held CR's base is the default branch everywhere: `start_base` skips a held owner, and `start_on` is unset for the held CR and for open CRs started on its branch, so every base read (carry, unstack rows, facts, the driver's carried line) gives the default branch.
  - D. A held CR's ready line and waits column say "held out of the stack (order O-n): `order unhold <cr>`", through `draft_waited`/`draft_clause`: the text of an existing field, no new STATUS.json field.
  - E. `order unhold` takes max(order of all CRs)+1, as `order add` does; a switch to series unsets `held` before computing places and gives the formerly held CR a unique order.
  - F. Moving a held CR out of the batch (the drop and its destination) belongs to the neighbour CR `order-drop-asks-where-the-cr-goes-trash-`; this CR only assumes the CR is no longer open after a drop, and the drop's status and PR handling follow the neighbour. No depends.json (a shared file is not a dependency).
