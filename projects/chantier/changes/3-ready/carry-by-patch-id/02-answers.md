---
type: cr-answers
description: The user's answers to the grill of carry-by-patch-id.
---

# Answers

## Round 1 (2026-11-17)

### batch-Q8: in which batch

The user: the six retro points of batch-23 join the next batch, with the four board CRs of
2026-11-17.

### carry-Q7: as filed

The user: as filed. The verdict carry compares the patch-id, not the diff text, and is recorded at
the restack.

## Spec questions (2026-11-17, after the spec critic)

### carry-Q8: whitespace

The user chose the recommended answer: the exact patch-id (`git patch-id --verbatim`, git 2.39
or later; an older git is refused with its reason). A rebase that changes only whitespace does
not carry the pass or the verdict.

### carry-Q9: the CR below changed

The user chose the recommended answer: yes. The CR's own commits are counted above the base it
was judged on, recorded with the gate pass and the verdict; a change in the CR below does not
break the carry when this CR's own commits did not change.

### carry-Q10: after a resolved conflict

The user chose the recommended answer: a resolved conflict (a conflict-resolver run) still gets a
new long gate and a Verifier, even with equal patch-ids; the cards keep that rule, and the carry
holds only for a rebase with no conflict.
### carry-Q11: the batch this CR ships in

The user chose the recommended answer: accept the one-time cost (CRs judged before this CR
merges have no recorded base and get a new long gate and Verifier at their next move), named in
this PR's Known gaps; take-base-nearest-pr's "a clean move costs no gate" holds from the batch
after this merge.- Settled by the Chief of Staff (third critique): the base recorded at `gate` and `verdict` is the branch the head actually sits on: among the start base, `pr_base` and the planned base, the one whose remote tip is an ancestor of the head; when none is, no base is recorded and the pass does not carry.
