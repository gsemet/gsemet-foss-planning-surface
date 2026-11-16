# A Driver records each Inspector pass before the PR body cites it

## Goal

A PR description must never claim a review the CR's record does not hold. In real-direct run 1
(2026-11-12, PR 137) the Verifier said `NOT VERIFIED` three times for one cause: the PR body's
Test plan said `Review: approved at <sha7>`, and nothing in the CR's record showed that pass. Each
cost a Verifier pass and a description fix on a sound change.

The fix is an order, in the cards only: every `APPROVE` an Inspector or a review step returns is
recorded at once by the Driver with `$CHANTIER note`; the Review box of the PR body is filled or
updated only from such a note, with the SHA it holds; the Verifier judges the box against that
note. No CLI change.

## What changes

Three cards, all in `skills/chantier/references/`. The agent files (`agents/`,
`com.github.copilot/agents/`) are not touched.

### 1. `driver.md`, section "CR driver"

Today the only recorded approval is the note after a round's commit (`note <cr> "r<n> approved at
<head from the JSON>, committed as <sha>"`), and nothing orders a note before the body is
written. Change the section so that:

- **Every `APPROVE` is recorded at once**, as soon as the Driver reads the JSON, before any other
  step (before the next review step, the commit, or any write of `pr-body.md` or the posted
  description). This covers:
  - the round's `inspector`;
  - a body-only re-inspection in the same round (the `FIX-REQUIRED` whose blocking items are all
    `pr-body.md: …`);
  - each review step the `Team:` lists;
  - the `inspector` after a move (a rebase whose range-diff shows the CR's patch changed, a
    resolved conflict).
- **What the note holds:** the verdict and the `head` copied from the Inspector's (or review
  step's) JSON, and what was reviewed (the round, the body alone, a move and its range, or the
  review step's name). Suggested forms, to keep the record greppable:
  - `r<n> inspector approved at <head>`
  - `r<n> body re-inspection approved at <head>`
  - `r<n> <review step> approved at <head>`
  - `move <old7>..<new7> (<kind>) inspector approved at <head>`
- **The commit ties the pass to the commit.** The existing note after the round's commit stays,
  `r<n> approved at <head from the JSON>, committed as <sha>`: the Inspector's `head` predates
  the round's commit, and this note is what lets the Review box cite the commit. A move's pass
  needs no second note: its `head` is already the moved, committed head.
- **A `FIX-REQUIRED` needs no note:** the next round's brief carries it.
- **Note first, then the box, always.** The Review box of `pr-body.md` (and of the posted
  description) is filled or updated only from a recorded note, citing the SHA that note holds for
  the reviewed state at the PR's head: the round's `committed as <sha>`, or the head of the move
  for a later pass. A box whose pass is not recorded stays unchecked. A pass carried over a later
  move (a clean rebase, no patch change) is written `carried from <sha7>` as the PR template
  already says, and the `<sha7>` is the one in the note.

### 2. `driver.md`, section "Stack driver"

When it starts an `inspector` after a move (the CR's patch changed) and its reply is `APPROVE`, the
stack driver records the pass on that CR (`$CHANTIER note <cr> "move <old7>..<new7> (restack)
inspector approved at <head>"`) before it updates that PR's Test plan SHAs with `gh pr edit
--body-file` / `glab mr update --description`. The Review box it writes cites only a recorded
note, as for the CR driver.

### 3. `worker.md`, section "Verifier"

Today: "their notes and green CI are not proof", and a description claim "with no proof in
`verify.md`, the gates or the evidence is `NOT VERIFIED`". Add the one case of the Review box:

- The Review box (`Review: approved at <sha7>`) is judged against the Driver's note of the pass in
  the CR's record, read with `$CHANTIER log <cr>` (complete; `handoff` shows only the last ten
  notes). A note of an approved pass whose SHA is the one the box cites (the reviewed `head`, the
  round's `committed as <sha>`, or the move's head; for a box `carried from <sha7>`, that
  `<sha7>`) proves the claim. No such note, or another SHA: `NOT VERIFIED`, as today.
- That note proves that a review happened and where, not the code: every other claim is still
  proven by the Verifier itself, and the sentence "their notes and green CI are not proof" stays
  true of everything else (say so where the exception is written).
- This applies to the description-only pass too.

### 4. `pr-template.md`

- The Test plan's Review item says it names the SHA of a recorded pass, e.g.
  `- [ ] Review: approved at \`<sha7>\` <!-- the SHA of the pass recorded in the CR's notes; unchecked until it is -->`.
- In "The rules", the paragraph on proofs and SHAs gains one line: the Review item cites the SHA
  of a pass the Driver recorded with `$CHANTIER note`, and stays unchecked while none is recorded.
- The template's head comment and the Inspector's audit list are unchanged (what the Inspector
  reviews is out of scope).

## Decisions carried from `02-answers.md`

- The Driver records the pass, copying the verdict and `head` from the Inspector's JSON; the
  Inspector stays read-only, its reply its only output.
- The record is a `$CHANTIER note`, not a new CLI record.
- Every `APPROVE` is recorded: a round's, a body-only re-inspection, a move's inspection (rebase or
  restack that changed the patch), each review step of the `Team:`; `FIX-REQUIRED` needs none.
- The Review box cites the SHA the note holds for the reviewed state at the PR's head: the approved
  round's commit (the note ties the reviewed `head` to `committed as <sha>`), or the move's head.
- The Verifier accepts the Driver's note with the SHA the box cites as proof that a review
  happened and where; none or another SHA is `NOT VERIFIED`. It still proves the code itself.
- Note first, always; the box is filled or updated only from a recorded note; an unrecorded pass
  leaves the box unchecked.
- The stack driver is bound too: it records the pass on the CR before it updates the PR's Test
  plan SHAs.
- `handback ready` is not refused for a missing pass: the CLI knows no role and reads no notes.

## Out of scope

- Any CLI change: no `verdict`-like record of the Inspector, no `handback` check on it, no change
  to `note`, `log` or `handoff`.
- The Inspector writing anything; it stays read-only.
- What the Inspector reviews, its audit list, and when a new inspection is needed after a move.
- The agent files of both hosts (`agents/`, `com.github.copilot/agents/`).
- The release PR (it keeps its own form).

## Evidence

- `just check` passes (structure tests and release notes), on the CR's pushed head.
- `just scenario` passes: the change touches the cards, and AGENTS.md requires it for a card
  change. No scenario step is added: the CLI is unchanged and the scenario does not run the cards.
- No new test: `tests/test_structure.py` checks structure only, and the change adds no file.
- The diff shows, by reading:
  - `driver.md` "CR driver": the order to note every `APPROVE` at once (round, body-only
    re-inspection, review step, move), the existing commit note kept, no note for `FIX-REQUIRED`,
    and the Review box filled only from a recorded note with its SHA;
  - `driver.md` "Stack driver": the note on the CR before the Test plan SHAs are updated;
  - `worker.md` "Verifier": the Review box judged against the note found with `log`, `NOT
    VERIFIED` without it or with another SHA, and the note proving the review only;
  - `pr-template.md`: the Review item and the rule naming a recorded pass.
- `grep -n "approved at" skills/chantier/references/*.md` lists the new note forms in
  `driver.md`, the Verifier's check in `worker.md` and the Review item in `pr-template.md`.
