## Summary

A PR description could claim a review that the change's record did not hold: the Verifier then said `NOT VERIFIED` for a sound change, and each time it cost a verification pass and a description fix. The cards now order the Driver to record every approving review with `$CHANTIER note` before the PR body cites it, and the Verifier judges the Review box against that note.

## Deliverables

Order of work for a review pass, before and after:

| Step | Before | After |
|---|---|---|
| Review returns `APPROVE` | nothing recorded until the round's commit | Driver notes verdict and `head` at once |
| Review box of the PR body | written freely | filled only from a recorded note, with its SHA; unchecked otherwise |
| Verifier on the box | no proof in the record: `NOT VERIFIED` | the note with the cited SHA proves the review happened |

Choices: the record is a plain `$CHANTIER note` (no CLI change), the stack driver is bound like the CR driver, and a `FIX-REQUIRED` needs no note.

## Blast radius

Grade: 1

Documentation of agent behaviour only (three cards); a plain `git revert` restores the previous wording.

## Autonomous decisions

- The new Driver order is a separate paragraph after the "move" paragraph, not inside the long round-flow sentence, to keep it readable.

<details>
<summary>Details</summary>

## Changes

- Driver card, CR driver: note every `APPROVE` (round, body-only re-inspection, review step, move) with four greppable forms; the Review box is filled only from a recorded note.
- Driver card, Stack driver: record the restack inspection on the CR before updating the Test plan SHAs.
- Worker card, Verifier: judge the Review box against the note read with `$CHANTIER log`; the note proves the review, not the code.
- PR template: the Review item names the SHA of a recorded pass.

## Human decisions

- The Driver records the pass, copying the verdict and `head` from the Inspector's reply; the Inspector stays read-only.
- The record is a note, not a new CLI record; `handback ready` is not refused for a missing pass.
- The Verifier accepts the note with the cited SHA as proof of the review only.

## Impacts

No visual change; Drivers write one more note per approval.

## Test plan

- [x] New or changed tests: No behaviour change (cards only)
- [x] Local gates at `a246894`: `just check`; `just scenario` carried from `10ff69c`: patch unchanged; the long gate runs once at the top of the stack, PR 152
- [x] Evidence: none, the diff is the evidence (verified by reading at `a246894`)
- [x] Review: approved at `10ff69c` (carried to `a246894`: patch unchanged by the restack)
- [x] Verified at `a246894`
- [x] CI green at `a246894`

## Internal references

- CR-204 record-inspector-pass

</details>
