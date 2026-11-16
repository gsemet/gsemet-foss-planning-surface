# Grill answers

## 2026-11-14

- MS-Q1, switching to a stack (from parallel or series): the open PRs are stacked; the stack driver
  rebases each on the one below, in order; CRs not yet started join on top (A).
- MS-Q2, leaving a stack or series for parallel: each open PR is rebased on main, its long gate and
  CI run again, and it leaves draft once ready (A).
- MS-Q3, the order of a stack or series made by a switch: the CRs already handed back ready at the
  bottom, in the order they became ready, then the others in the batch's order; the recorded
  chains are kept (A).
- MS-Q4, when: this CR joins batch-18 at the head of the queue, right after CR-253 and CR-254;
  batch-18 switches to a stack once it is merged (A).
- Never changed by a switch: the merged CRs.

- Spec open points 1-5 (2026-11-14): the spec's defaults stand, decided by the Chief of Staff to start it at once in batch-18 (MS-Q4): 1. parallel to series chains every open PR now, in MS-Q3's order; 2. stack to series sends the PRs above the bottom to draft and the Chief of Staff names them; 3. a running stack driver stops after the branch it pushes, then `unstack` runs; 4. a started release CR is redone once the others merge; 5. on a switch to a stack the Chief of Staff names the PRs in draft with "do not merge", a merge anyway is recorded and the rest restacked.

