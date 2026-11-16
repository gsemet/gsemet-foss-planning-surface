# Retro

## 2026-11-13: batch-15, CR-196 to CR-213 (all merged; v0.9.0 tagged)

- Old session stop: the epoch-1 Drivers of CR-196 to CR-199 were lost when the direct steering session stopped, and restarted under the Foreman: a batch switched from direct to Foreman mode restarts every live CR by the restart path; say so in the switch's card.
- Long gate queue: one gate at a time with four Drivers ran past the one-hour wait, and the refusal named a stale holder; CR-196 and CR-205 lost an hour each and their Drivers read it as an infrastructure fault or a stale lock: the refusal names the gates queued ahead (or the real holder), and the wait limit scales with the queue.
- Driver out of context: CR-200 and CR-208 Drivers ran out of context and were restarted: the Driver delegates more to workers and keeps its context lean; measure the Driver's turns per CR.
- Driver edited code: CR-200's out-of-context Driver patched `costs.py` itself through PowerShell and damaged a docstring: the no-edit rule for Drivers also covers shell writes, and the write guard names it.
- Driver repaired a worktree itself: CR-212's round-3 Driver ran `git reset --hard` after a coder's botched attempt (nothing pushed was lost): a dirty worktree after a failed coder goes to a new coder or a conflict-resolver, with the Driver's reset named in the card as allowed or not.
- Byte-order mark: CR-196's PR body carried a BOM: CR-199's check now rejects it in tracked files; the PR body rule is in the cards (CR-207).
- PR descriptions failed the description pass for role names (CR-203, CR-206 and others): the PR template says where role names may appear, and the Driver checks it before posting.
- Extra rounds: CR-198 (a race found by review), CR-206, CR-211 (a stray `round` call before any work spent a round) and CR-213 needed a second round, CR-212 a third: `round` refuses a second call with no worker run since the last.
- Infrastructure: one GitHub 502 rerun on CR-200's CI, and CR-213's first Driver was ended by a host API 403 after its gate: a host failure is a restart, not a silent end; the card says so.
- Unchecked UI: CR-202's Refresh button placement was not seen in a real pane: a change to the board's pane gets one screenshot from a real session as evidence.
- Stack driver id race: I recorded the stack driver's id before it ran `take stack`, which then refused it; it happened twice: the Foreman runs `take stack` and passes its output in the prompt, or `take stack` gives a read-only form for the driver.
- Restack force pushes refused: the host refused the stack driver's 14 force pushes, then refused them to the Chief of Staff; they waited for the user overnight (ask A-17): the force-push route is written in the cards and the permission rules allow `--force-with-lease` on `chantier/` branches.
- Pairwise conflicts in a parallel batch: 15 PRs all on main conflicted pairwise in the cards and SCORECARD.md, so the stack had to be restacked as a chain: CR-211's chain proposal (wait for a CR editing the same lines) applies at the plan.
- Test plan SHAs left stale after a restack: the first post-merge restack did not refresh the PR bodies' Test plan SHAs until asked: `ship` after a restack prints the PR body lines whose SHA is now stale.
- Native stack insertion: inserting CR-213 below the release in GitHub stack #155 was refused by the permission check (to the stack driver, and my message carrying the commands); the user unstacked #155 and made #157 (ask A-22): CR-213's `forge-stack` gains an insert or rebuild, and the cards route it to the user.
- `order after` refused on a ready CR: CR-212's recorded base stayed CR-211's branch after the insertion, since `after` cannot change on a ready CR: `stack` (the recorded order) sets the base, or `order after` accepts a ready CR with a restack note.
- Spec-writers: two spec-writers were started on one CR after a refusal of the prompt's first line (Chief of Staff's report): every agent states the first line its prompt must start with (CR-213), and the parent checks it before starting.
- Release publication refused: `gh release create v0.9.0` was refused to the Foreman by the permission check after `just tag` passed; it waits for the user (ask A-24): the release step 5 is run by the user or allowed by a named permission rule.
