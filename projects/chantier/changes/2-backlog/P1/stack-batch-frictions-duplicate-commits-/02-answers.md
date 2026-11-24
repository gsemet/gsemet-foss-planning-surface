Short name: `stack-frictions`

No question asked (2026-11-24, the Fable advisor's reading; the user said to grill all the P1s and keep only impactful questions). Defaults the specification takes:
1. stack-frictions-D1: **Item 1, duplicate commits after a rebase merge.** CR-466 already pre-authorises rebase and force-with-lease on own CR branches, and the stack driver's card already holds the one-pass restack after a partial merge. What stays: `order merged` in a stack batch prints one line saying a restack is owed and by whom. A printed line, no new tool.
2. stack-frictions-D2: **Item 2, `take` prints wrong bases.** Fix it; `92c7a795` did part of it, the Studio batch-09 retro (0.15.1) still reports it after a reorder. Folds in the inbox item `take-prints-the-old-worktree-base-after-`.
3. stack-frictions-D3: **Item 3, `off:` where `carried:` belongs after a clean restack.** A defect in `commands/carry.py`: fix it.
4. stack-frictions-D4: **Item 4, dead Drivers' claims block `ship`.** The cards already let the steering session end a lease once the host shows the holder ended (`foreman.md`); what stays is that the refusal names the exact command. Folds in the inbox item `foreman-s-stack-lease-goes-stale-with-no`.
Destination: next batch (3-ready): it touches the Stack driver and Foreman cards that CR-471 cuts, and `status` lines that CR-474 edits; it follows both.
