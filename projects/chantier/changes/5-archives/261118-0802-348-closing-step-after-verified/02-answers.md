# Answers

No grill: a retro point of batch-24 (2026-11-18), kept by the retro critic, that the user put
straight into the batch.

## Settled by the Chief of Staff

- The user's word (2026-11-18): "file all six and run them in batch-24" ("Fait les 6 c'est très
  bien. Fait le dans le batch en cours"). This CR is one of the six, run as its request is written.
  The user asked no question and settled no behaviour; each choice below is settled by the Chief of
  Staff, within the request.
- cs-Q1 (when the closing step starts): always, as the request is written, not only above a
  context threshold. The trigger is the CR Driver's first `VERIFIED` from the `verifier` at the
  pushed head (the verdict that `handoff` shows at the PR's head), with the evidence, the Test plan
  boxes, the description pass, the PR turned ready and `handback ready` still to do. A matrix probe's
  `VERIFIED` (before any push) is not the trigger, and neither is a verdict carried by `ship` over a
  clean rebase (no Verifier runs). Settled by the Chief of Staff.
- cs-Q2 (who runs the closing step): a fresh CR Driver, started by the existing restart path, not a
  new role. A new role would need a new card, two agent files and the cost code's knowledge of it;
  the restart path already exists, counts no round and takes no slot. Settled by the Chief of Staff.
- cs-Q3 (how the hand-off is said): the Driver records its state with `note`, then hands back
  `blocked context: closing: VERIFIED at <sha7>; next: <what is left>`. It reuses the `context:`
  hand-back, which the CLI, the eval kit's audit and the Foreman already know, so no new hand-back
  word. The steering session takes it back with `take <cr> --note "resume: closing"`. Settled by the
  Chief of Staff.
- cs-Q4 (what the closing Driver reads): only the CR's notes: `handoff <cr>`, `log <cr>`,
  `pr-body.md`, `work/verify.md` and the evidence files `verify.md` names, and `pr-template.md` when
  it edits the body. It does not open the specification, `investigation.md`, the `r<n>.md` notes or
  the diff, unless a step outside the closing comes up (a red check, a move, a review item on the
  code), when the card's usual rules apply. Settled by the Chief of Staff.
- cs-Q5 (no loop): a Driver started with `resume: closing` never hands off for the closing again,
  even when a later move makes it run a new `verifier`; it closes the CR itself. Settled by the Chief
  of Staff.
- cs-Q6 (counting): a closing hand-off is not an out-of-context end. It does not count toward the
  Foreman's "driver out of context twice" ask nor toward "driver ended twice"; a report or a retro
  names it "the closing step", never "out of context". Settled by the Chief of Staff.
- cs-Q7 (the CLI): one small change to what `handback` prints, so the line does not say "out of
  context" for a closing hand-off: a `blocked` reason starting `context: closing` prints that the
  steering session starts a fresh Driver for the closing step. No new command, no new refusal, no
  new record field (AGENTS.md: no speculative CLI tool). Settled by the Chief of Staff.
- cs-Q8 (out of scope): the stack driver, the QA driver and the release driver keep their flow; the
  130,000-token context rule stays as it is; the Verifier's, Inspector's and Coder's cards do not
  change; no new agent file on either host. Settled by the Chief of Staff.
