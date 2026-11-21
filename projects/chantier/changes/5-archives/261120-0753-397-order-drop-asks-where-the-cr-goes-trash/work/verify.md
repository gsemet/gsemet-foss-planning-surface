# Verify CR-397 (order drop names where the CR goes)

Head: a872a662c025bd2ca2c1808abade5fe1134a6e18

Second pass, after the rebase onto CR-396 (base 9ff16d56) with one conflict resolved in `lifecycle/stages.py` and the
added test-only commit a872a662. The base changed what the proofs run (`git diff --name-only ad46081c 9ff16d56` lists
the CLI, cards, docs and scenario), so every claim of the first pass (ad46081c) was run again at a872a662, none carried.

All real runs: the head's CLI (`uv run --no-sync --project <worktree> chantier`) in a scratch git repository under
`work/scratch/p1` (a bare local `origin`; batch-01 of 5 CRs filed and opened with `chantier open`, Foreman seated, CR-101/102
taken with real worktrees; CR-103 set `ready` with a PR, CR-104 `kind release`, CR-105 `kind fix`, PRs set in `batch.json`
as the repo's own tests do). Paths shortened to `<scratch>`. The scratch is removed. Every claim judged at a872a662.

## 1. `order drop`, no usable destination: exit 1, nothing recorded (a872a662)

```
order drop CR-103                -> error: order drop <cr> --note trash|inbox|P1..P4: where the CR goes; ask the user when they have not said it   exit=1
order drop CR-103 --note P5      -> same, exit=1
order drop CR-103 --note ready   -> same, exit=1
order drop CR-103 --note 3-ready -> same, exit=1
batch.json md5 before and after: identical (the script printed "md5 same: True")
```

## 2. Release / fix CR: only the trash (a872a662)

```
order drop CR-104 --note P2    -> error: CR-104 is a release CR: it leaves the batch only to the trash (--note trash)  exit=2
order drop CR-105 --note inbox -> error: CR-105 is a fix CR: it leaves the batch only to the trash (--note trash)      exit=2
(batch.json md5 unchanged: True)
order drop CR-104 --note trash -> [chief-of-staff->foreman] order O-1: drop CR-104 6-trash
                                  dropped CR-104: 6-trash/261120-0325-104-delta-item   exit=0
```

## 3. Non-live drops, live drop plus cancel: placement and files (a872a662)

```
order drop CR-103 --note P2 (ready, PR, parallel) -> order O-2: drop CR-103 2-backlog/P2   (no PR clause)
                                                     dropped CR-103 to 2-backlog/P2: 2-backlog/P2/103-gamma-item
CR-101 live: --note trash -> O-3 ... ; --note p2 (lower case) -> O-4: drop CR-101 2-backlog/P2
cancel CR-101 --epoch 1  -> cancelled CR-101 to 2-backlog/P2; stopped 0: none   exit=0   (the later word replaced the earlier)
CR-102 live: --note inbox -> O-5 ; cancel CR-102 --epoch 1 -> cancelled CR-102 to 1-inbox; stopped 0: none
```

Folders: `2-backlog/P2/101-alpha-item`, `2-backlog/P2/103-gamma-item`, `1-inbox/102-beta-item` (no date); each holds
`03-change-spec.md STATUS.json STATUS.md formerly.json intake notes.md` (101 and 102 also `work/`).
`formerly.json` of CR-101: `{"cr": "CR-101", "batch": "batch-01", "branch": "chantier/batch-01/cr-101-alpha-item", "worktree": "<scratch>\p1.worktrees\batch-01-CR-101", "pr": "https://github.com/o/r/pull/01", "pr_draft": null}`.
`notes.md` ends `formerly CR-101 of batch-01`. `restored.json`: `{"last_number": 103}`.
After the drops `git worktree list` still lists batch-01-CR-101 and -CR-102, and `git branch` lists both `chantier/batch-01/cr-10[12]-...` branches.
Limit: the batch numbered up to 105, so "a new number above" is not isolated by the run; the in-process test
`test_a_dropped_cr_goes_where_the_order_names_with_its_work` (claim 9) asserts restored.json holds the number.

## 4. `cancel` follows the drop (a872a662)

```
cancel CR-101 --epoch 1 (live, no drop order) -> error: cancel CR-101: no destination recorded; the Chief of Staff's "order drop CR-101 --note trash|inbox|P1..P4" names it   exit=2
batch.json md5 unchanged: True
```

## 5. Name clash exits 2 before anything changes (a872a662)

With `2-backlog/P2/101-alpha-item` made by hand:

```
order drop CR-101 --note P2 -> error: cannot drop CR-101 to 2-backlog/P2: the name 101-alpha-item is already used by .agents/changes/2-backlog/P2/101-alpha-item   exit=2
batch.json md5 unchanged: True
```

## 6. PR clause (a872a662)

```
CR-101 (has PR, parallel) --note trash -> order O-3: drop CR-101 6-trash; close its PR https://github.com/o/r/pull/01
--note p2 (CR-101), --note P2 (CR-103)  -> no clause (claim 3)
```

Stack mode: `test_the_pr_of_a_trashed_cr_is_closed_outside_a_stack_only[case1]` (passed, claim 9).

## 7. Label (a872a662)

`4-batch/STATUS.md` rows: `[dropped to 2-backlog/P2]` (101, 103), `[dropped to 1-inbox]` (102), `[dropped]` (104, trash).
`STATUS.json` `crs[].label`: `dropped to 2-backlog/P2`, `dropped to 1-inbox`, `dropped to 2-backlog/P2`, `dropped`.
The backlog folder's own STATUS.md: `dropped to 2-backlog/P2 · batch-01 · [PR](https://github.com/o/r/pull/01)`.

Finding (not a failure): the `status` command's own per-CR line reads `cancelled` for every dropped CR, the trashed one included
(`CR-101 cancelled r0/3 https://github.com/o/r/pull/01 ...`, `CR-104 cancelled r0/3 - | long gate - release`); STATUS.md, STATUS.json
and the board read `dropped`. The PR body's "`status` reads `dropped` ..." should say STATUS.md, STATUS.json and the board.

## 8. `close` (a872a662)

After the six orders were marked done (`order done O-k --epoch 1`), `pause --epoch 1`, and a fake Foreman transcript recorded
in scratch (`CHANTIER_CLAUDE_PROJECTS`), `close` (no --yes):

```
the trashed CRs and the merged CRs' leftovers, to remove on the same word ...: CR-104 (dropped) worktree <scratch>\p1.worktrees\batch-01-CR-104 branch ...; CR-105 (dropped) worktree ... branch ...
kept, moved out with their work: CR-101 (2-backlog/P2/101-alpha-item) worktree ... branch ... PR https://github.com/o/r/pull/01; CR-102 (1-inbox/102-beta-item) ...; CR-103 (2-backlog/P2/103-gamma-item) ...
```

The removal line names 104 and 105 only; the kept line names 101, 102, 103. `close --yes` then closed the batch;
`5-archives/batches/batch-01.json`: CR-101 result dropped archive None to 2-backlog/P2; CR-102 dropped None 1-inbox; CR-103 dropped None 2-backlog/P2;
CR-104 dropped archive 6-trash/261120-0325-104-delta-item to 6-trash; CR-105 likewise.
`diff` of CR-101's backlog STATUS.md before and after `close --yes`: identical ("STATUS unchanged"); `grep -il final` over the backlog and
inbox STATUS.md files: no match (exit 1). The `moved since from 2-backlog/P2` line: in-process test only (claim 9).

## 9. Tests and the forge-stack fixture (a872a662)

`uv run --no-sync pytest skills/chantier/scripts/cli/tests/test_order_drop_to.py skills/chantier/scripts/cli/tests/test_forge_moved.py -q` gave `23 passed in 8.14s`,
among them `test_forge_stack_rebuild_names_a_moved_pr_apart_and_leaves_it_on_main`,
`test_a_gitlab_chain_retargets_a_moved_mr_to_the_default_branch_with_its_reason`,
`test_the_status_close_and_record_tell_a_trashed_cr_from_a_moved_one`, `test_a_held_cr_dropped_is_no_longer_held`,
`test_validate_reads_a_formerly_json_in_a_cr_folder_as_part_of_its_layout`. The forge fixture builds its record by hand, as the specification's Evidence section names for it.

## 10. Allow rules (a872a662)

`uv run --no-sync python -c "from chantier.commands.permissions import RECOMMENDED_ALLOW as R; print([r for r in R if 'close' in r or 'reopen' in r])"` gave
`['Bash(gh pr close*)', 'PowerShell(gh pr close*)', 'Bash(gh pr reopen*)', 'PowerShell(gh pr reopen*)', 'Bash(glab mr close*)', 'PowerShell(glab mr close*)', 'Bash(glab mr reopen*)', 'PowerShell(glab mr reopen*)']`.

## 11. Rebase delta (a872a662)

The conflict resolution in `lifecycle/stages.py` and the conftest fixture are covered by claims 1-9 (all as expected at the head;
the tests include the batch-end and restore paths that import `cr_slug`, `folder_taken`, `remember_cr`). CI at the head
(`gh pr view 370`): just check on ubuntu, macos and windows, just scenario (ubuntu), just eval-dry-run: all SUCCESS. The helpers moved out of
`intake.py` and `opening.py` are refactors the PR body's Changes does not name individually; behaviour is the same (the tests of
`restore` and the batch end pass); noted only.

## PR description (https://github.com/gsemet/chantier/pull/370, head a872a662, base `chantier/batch-29/cr-396-just-tag-fast-forwards-the-main-checkout`)

Read with `gh pr view 370 --json body`. It renders (headings, table, fold). Summary, Deliverables and Changes match
`git diff --stat 9ff16d56 HEAD` (44 files; every area the bullets name is there). Known gaps names the pane screenshot and the come-back CR. No image
attached. Two things to fix, neither a failed claim: (1) the status sentence (claim 7 finding); (2) Internal references still says
"after CR-394", the base is now CR-396's branch. The Test plan boxes and the Review box are the Driver's to fill after this pass.

VERIFIED
