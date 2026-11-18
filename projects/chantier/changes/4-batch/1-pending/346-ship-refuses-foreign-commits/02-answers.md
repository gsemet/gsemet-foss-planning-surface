# Answers: ship refuses a main-based PR that carries another CR's commits

## Settled by the Chief of Staff

No grill: the user asked to run this retro point as written ("file all six and run them in
batch-24", 2026-11-18). `intake/request.md` is the user's word. The working choices below are the
Spec-writer's, made to deliver it with the smallest change.

- W1. The refusal lives in `ship` (CLI, role-free): it raises `EXIT_PRECONDITION` and records
  nothing (no `ship` event, no `pr`/`head` change). Since `handback ready` already refuses a head
  that is not the one `ship` recorded, the CR cannot be handed back ready at such a head either.
- W2. "Based on main" is the PR's base as `ship` reads it on the forge (`read_state`), equal to
  the project's `default_branch`. A failed forge read (base or draft not read) refuses nothing:
  `ship` cannot know the base, and prints its usual `not read` text.
- W3. The refusal applies only to a PR read **out of draft** (`draft is False`). A draft cannot be
  merged, and the cards already put every PR the stack driver moves to draft while the stack is
  made or changed: this keeps every legitimate restack window (push, `ship`, then
  `forge-stack rebuild` retargets) unrefused, and refuses exactly the incident's shape (PR 297 out
  of draft on main, its head carrying CR-336).
- W4. "Another CR's commits" is read with git only, read-only: another CR of the same batch, not
  recorded `merged`, with a PR recorded, whose recorded `head` or remote branch tip
  (`<remote>/<its branch>`) is an ancestor of the shipped head and not an ancestor of
  `<remote>/<default_branch>`. A head that carries only part of another CR's commits is not
  caught (out of scope).
- W5. The refusal names each such CR with its PR and says what to do: put the PR back to draft,
  or rebase it onto the default branch without those commits, push, then `ship` again.
- W6. `ship --conflict` does not bypass the refusal.
- W7. The second half (the ask names the one PR to merge) is a card change only: the Foreman's
  `stack-ready-to-merge` ask gains a `merge <cr> <link>` part naming the highest PR of the
  mergeable part, and the Chief of Staff's card tells the user that one PR first, and that no
  other PR of the batch is to be merged meanwhile unless an ordinary `ready-to-merge` ask names it.
  The ask stays free text: `readiness_key` reads only its first word, so no CLI change.
- W8. One parametrized test in `test_carry_ship.py`; no new scenario step; no change to the
  Copilot or Claude Code agent files (cards only), to the eval scorecard or to the scenario.

## Settled by the Chief of Staff (after the spec critic)

The user is away; the Chief of Staff settled the critic's questions with the recommended option,
inside the request's intent (2026-11-18).

- S1 (replaces W7's exception). While the stack stands, the only other PR of the batch the user is
  told to merge is the PR of a CR that is not in the stack order (a fix CR) whose latest readiness
  ask names it. CR-337's case (in the stack order, handed back ready on its own) no longer passes.
- S2. After the refusal, the first step is always: put the PR back to draft, then `ship` again
  (which records the draft state, so the CR reads "PR in draft"), then rebase if needed. The
  refusal text and `driver.md` say so. A refused `ship` still records nothing (W1 stands).
- S3. The ask forms in the spec are written composed with `partial-stack-ask-windows-gate`'s
  local-gate clause; the CR that merges second rebases its edit onto the other's wording.
- S4. The `driver.md` sentence says "another CR of the batch not recorded merged" (a cancelled CR
  counts).
- S5. The refusal text and `driver.md` add: if the CR named is already merged on the forge, ship
  again once `status` shows it merged.
- S6. The Goal cites batch-24's two `ship` events of CR-337 (22:43:02, 22:47:28) as the proof.
- S7. The Chief of Staff's sentence adds: a merge the user makes anyway is recorded as any merge.
- S8. Out of scope: `stack --out-of-draft` and `gh pr ready` are not checked.
- S9. The test's "A recorded merged" case edits the record directly; the per-case `read_state`
  patch is applied after A's `ship`.
