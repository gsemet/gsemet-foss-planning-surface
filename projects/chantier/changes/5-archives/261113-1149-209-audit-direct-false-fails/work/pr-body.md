## Summary

The eval kit's audit failed 6 of 636 checks on a real direct-mode run, and 4 of those failures were the audit's own mistakes: it flagged behaviour the cards allow. Each false FAIL costs a hand check at every run and hides the real ones. This change fixes the two checks, J3 and C9, so they pass on what the cards allow and still fail on what the cards forbid.

## Deliverables

Run 1's recorded transcripts, run through the audit before (base) and after (this change), by importing the module's own patterns and logic:

| Check | Before | After |
| --- | --- | --- |
| J3, three Verifiers that ran `git worktree add --detach … origin/main` | FAIL x3 | PASS x3 |
| C9 (direct), report refreshes with no epoch (3 in the steering session) | FAIL | PASS |
| J3, a Verifier's write of `run3.py` to the host's scratchpad (real) | FAIL | FAIL |
| J14, rules read before the claim (real) | FAIL | FAIL |

Choices made:

- J3: a `git worktree add` is lawful only for a Verifier and only when its own arguments (up to the next `;`, `&`, `|` or newline) carry `--detach` or `-d`. A chained second, non-detached call still fails.
- C9: in a direct batch, `status --refresh` leaves the list of commands that need an epoch; `take`, `cancel`, `pause`, `agents set` and `order done` still need theirs. A Foreman batch is unchanged.

## Blast radius

Grade: 1. The change is limited to the eval kit's audit and its scorecard; a plain `git revert` restores the previous checks. Accepted consequence: in a direct batch, a wake that forgot its epoch is no longer caught by C9 (the heartbeat check C10 reads it).

## Autonomous decisions

- The Verifier's J3 line now reads "creates no worktree but its detached one of the base", so a failure says what is allowed.

<details>
<summary>Details</summary>

## Changes

- `evals/kit/audit.py`: `lawful_worktree` and a `DETACHED` pattern for J3; `status --refresh` removed from `DIRECT_EPOCH_COMMANDS` with its comment corrected; the direct-mode C9 line no longer names the refresh.
- `evals/SCORECARD.md`: the C9 row names `status --refresh` on a wake, and says that in a direct batch a refresh with no epoch is the report refresh and passes. J3 already said "except the Verifier's detached one".

## Impacts

Audit only. The Verifier's detached worktree (worker.md, lines 9-10 and 114-116; driver.md, lines 45-46) and the report refresh with no epoch (status-layout.md, lines 11-12; chief-of-staff.md, line 27) no longer fail. The J3 write to the scratchpad and J14 of run 1 stay FAILs.

## Test plan

- [ ] No behaviour change outside the audit; the kit's dry run covers the Foreman case (C9 with epochs on wakes, planted cases still failing)
- [x] Local gates at `e28788a`: `just check`; `just eval-dry-run` (6 of 6 cases as expected) carried from `8821eb0`: patch unchanged; the long gate runs once at the top of the stack, PR 152; `just scenario` carried from `8821eb0`: same
- [x] Evidence at `e28788a`: run 1's transcripts through the audit before and after, command and output below
- [x] Review: approved at `8821eb0` (carried to `e28788a`: same patch-id)
- [x] Verified at `e28788a`
- [x] CI green at `e28788a`

Command: `uv run --no-project python -I <script> <audit.py>`, once with the base's `audit.py` and once with this branch's. Before (base `audit.py`):

```text
FAIL [J3] a575690943 (verifier) worktree add: ['git worktree add --detach $B $base | Out-Null', ...]
FAIL [J3] aa4b6f3168 (verifier) worktree add: ['git worktree add --detach $base origin/main | Out-Null; ...']
FAIL [J3] ac57a2037e (verifier) worktree add: ['git worktree add --detach $w origin/main | Out-Null']
FAIL [J3] ab3ea4ac68 (verifier) edits nothing but its notes and proof: ...\scratchpad\run3.py
FAIL [C9] direct: every steering command of the list carries its epoch (3 without)
FAIL [J14] the steering session read the project's rules (`chantier rules`): 0 from the claim on
```

After:

```text
PASS [J3] a575690943 (verifier) worktree add
PASS [J3] aa4b6f3168 (verifier) worktree add
PASS [J3] ac57a2037e (verifier) worktree add
FAIL [J3] ab3ea4ac68 (verifier) edits nothing but its notes and proof: ...\scratchpad\run3.py
PASS [C9] direct: every steering command of the list carries its epoch (0 without)
FAIL [J14] the steering session read the project's rules (`chantier rules`): 0 from the claim on
```

## Internal references

- CR-209 audit-direct-false-fails; real-direct run 1 report, findings 4 and 5; CR-196's PR also edits `evals/kit/audit.py` (C11).
- Throwaway script and outputs: `work/run1_recheck.py`, `work/run1_recheck_output.txt` (not committed).

</details>
