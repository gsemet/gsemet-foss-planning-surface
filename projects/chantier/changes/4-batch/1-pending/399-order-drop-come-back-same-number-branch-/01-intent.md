# A CR taken out of a batch comes back under its number, with its branch and PR

Split from `order-drop-asks-where-the-cr-goes-trash-` (spec-critic finding 10, 2026-11-20). That
CR lets `order drop` send a CR to the inbox or the backlog (`P1`..`P4`). The moved folder keeps its
number (`2-backlog/P2/381-<slug>`), the number is reserved in `restored.json`, and the drop writes
`formerly.json` in the folder: `{"cr", "batch", "branch", "worktree", "pr", "pr_draft"}`. This CR
reads and consumes it.

Seen at batch-28's end: CR-381 and CR-382 were only postponed. The user wanted them back later as
CR-381 and CR-382, with their PRs #346 and #347, not as new CRs with new numbers and fresh branches.

Wanted:
- A folder that joins a batch (`open`, `order add`, a factory's `triage --ready`; `add_cr` in
  `commands/opening.py`) and holds `formerly.json` takes the CR's number back (`CR-381`, folder
  `1-pending/381-<slug>`), not `next_cr_number`'s.
- Re-added to the batch it left (that batch still holds the CR, cancelled, with `left_to`), the
  existing entry is reopened instead of a second one being added. Its status becomes `queued`, and
  every per-round and stack field is reset: `round`, `agent`, `left_to`, `stacked`, `head`,
  `pr_base`, `start_on`, `blocked_reason`, `attempts`, `phase`, `phase_detail`, `phase_at`,
  `gate_waiver`. `pr_draft` comes from `formerly.json`. Its notes and cost stay.
- Its branch still exists (`core/git.py` `branch_exists`): `branch`, `worktree`, `pr` and
  `pr_draft` come from `formerly.json`, and the output says `joins with its branch <b> and PR
  <link>`. Branch gone: the same number, a fresh branch and worktree named the usual way, no PR,
  and the output says `joins fresh: its branch <b> is gone`.
- `formerly.json` is deleted once the record holds the CR again.
- The Driver card (driver.md, worktree bullet): a CR whose first take shows a `PR:` came back.
  - Use its branch: its recorded worktree if it is there, else `worktree add <path> <branch>`.
  - Rebase it on the base `take` names, and ship to that same PR. Never open a second PR.
  - A recorded PR found closed: reopen it (`gh pr reopen <n>`, `glab mr reopen <n>`) before any
    push to its branch. "GitHub refuses to reopen a PR after a force-push" is unproved: it is
    either proved or dropped in the specification.
  - A recorded PR found merged: nothing to do; ask the Chief of Staff.
- A moved-out CR whose PR the user merges later, outside any batch: on "I merged #n", the Chief of
  Staff adds the CR to the open batch (`order add --note <folder>`), which brings back its number
  and PR, then records the merge (`order merged <cr>`). chief-of-staff.md names this route.
