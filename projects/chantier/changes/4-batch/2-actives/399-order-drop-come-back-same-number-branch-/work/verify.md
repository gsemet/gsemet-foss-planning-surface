# Verify CR-399

Head: 75b7a1887d5d778b387a37d99f4f92da9b6e6619

All runs use the head's CLI (`uv run --no-sync --project <worktree> chantier`, version 0.14.0, imports
from the worktree) on a scratch git repo under `work/scratch/r1` (its own repository, `--project`
unset, working folder = the scratch repo). The scratch record was prepared by hand only for
`status ready`, `pr`, `pr_draft`, `notes`, `cost_usd` (no forge here); every drop is a real
`order drop <cr> --note P2`. A batch's end was simulated by removing `4-batch` and `init` (the real
`close` refuses: no steering transcript to price). Logs: `work/verifier/evidence/*.log`.

1. Another batch (judged at 75b7a18). VERIFIED.
   Real `order drop CR-101 --note P2` of a CR holding PR #346, a local branch: wrote
   `2-backlog/P2/101-alpha/formerly.json` (cr, batch-01, branch, worktree, pr, pr_draft true) and
   `restored.json` `{"last_number": 101}`. Then `open <folder> --direct ...` (batch-02) printed:
   `CR-101 alpha: 2-backlog/P2/101-alpha -> 4-batch/1-pending/101-alpha` then
   `CR-101 joins with its branch chantier/batch-01/cr-101-alpha and PR https://github.com/o/r/pull/346`.
   Record: id CR-101, queued, branch chantier/batch-01/cr-101-alpha, worktree `...batch-01-CR-101`,
   pr .../346, pr_draft True; `find -name formerly.json` empty. Then `file Gamma` + `order add`:
   `added CR-102, queued` (higher than 101).
2. Same batch reopened (75b7a18). VERIFIED.
   Record patched ready/round 2/attempts 1/agent/head/stacked/phase, notes ["kept"], cost 1.5, then real
   drop, then `order add --note 2-backlog/P2/101-alpha` (log `run7-there.log`): output `added CR-101, queued`,
   `CR-101 joins with its branch ... and PR ...346` right after; one CR-101 entry, status queued, round 0,
   attempts 0, stacked False, no agent/head/phase/left_to, notes ["kept"], cost_usd 1.5, order 3 (max 2 + 1),
   pr and pr_draft from formerly.json; formerly.json gone, P2 empty.
   Branch deleted (`git branch -D`, log `run7-gone.log`): `CR-101 joins fresh: its branch
   chantier/batch-01/cr-101-alpha is gone; its former PR https://github.com/o/r/pull/346 is left as it is`;
   entry branch `chantier/batch-02/cr-101-alpha`, worktree `batch-02-CR-101`, no pr/pr_draft, notes and cost kept, order highest.
3. Refusals (75b7a18). VERIFIED (`run10.log`).
   Folder in P2 with a real formerly.json; each case: sha1 of batch.json before = after
   (11fdea5f...), folder with formerly.json in place. No `cr` -> exit 2, `formerly.json: expected {"cr": "CR-<n>", "batch", "branch", ...}`;
   `not json` -> same, exit 2; `pr_draft: "yes"` -> same, exit 2; `cr` = CR-102 held live ->
   exit 2, `2-backlog/P2/101-alpha: formerly.json names CR-102, which batch-02 already holds`.
   Also `pytest tests/test_came_back.py tests/test_rail_refusals.py -q`: 32 passed.
4. Cards (75b7a18). VERIFIED. `git diff <base>...HEAD -- skills/chantier/references`: driver.md names
   `PR:` link at first take, own branch/worktree (`git -C <main checkout> worktree add <path> <branch>`), `gh pr view`/`glab mr view`,
   open/closed (`gh pr reopen`, `glab mr reopen` before any push, refused -> `handback <cr> blocked question: ...`)/merged
   (`blocked question: ... already merged`), rebase on base, "never open a second PR for it".
   chief-of-staff.md: `order add --note <folder>` then `order merged <cr>` at once, Foreman one message add first, no batch open
   -> tell the user, leave the folder; the Driver's merged blocked question recorded with `order merged`.
   concepts.md: lifecycle line carries the specified clause.
5. PR description (`work/pr-body.md`, 75b7a18). VERIFIED. Summary/Deliverables/Changes match the diff
   (came_back.py, joining.py with add_cr/join_cr/new_entry, Batch.consume, orders_apply/orders_release imports,
   3 cards, tests, scenario step). Known gaps (remote-only branch counts as gone; card rules not run on a real forge)
   are true. No image. Note for the Driver: the Test plan's `<sha7>` placeholders and the Review box are still unfilled, as expected pre-ship.

Observation (not a failure): in one early scratch run a drop of a `ready` CR, issued after a gone-branch
reopen, left the entry `ready` in P2 with left_to set; I could not reproduce it in three replays
(`run7-*.log`, `run10.log` and a later replay all drop to `cancelled`), and I suspect my own scratch state.

Not run: scenario step and Windows/Linux CI (CI green at this head per the Driver's note); the real
`just scenario` is the pipeline's job.

VERIFIED

## Move 75b7a18 -> 783329d (judged at 783329d76788e78d04fb296588e6dac4eefa6653)

Head: 783329d76788e78d04fb296588e6dac4eefa6653

Move: clean rebase onto CR-398's branch (base a872a66 -> 77089e3, CR patch-id identical, per the
brief) plus 783329d, which only edits skills/chantier/references/driver.md. Claims 1-5 above
(CLI behaviour: the CR's code files) are carried from 75b7a18: 783329d touches no code, and the
rebase left the CR's patch unchanged. CI is green at this head (per the brief; not re-read here).

6. Came-back rules of driver.md still all there (783329d). VERIFIED.
   `git show 783329d -- skills/chantier/references/driver.md` and `grep -n -A8 "came back to a"
   skills/chantier/references/driver.md` (lines 205-211) show: "A CR whose first `take` shows a `PR:`
   link came back to a batch: use the branch and worktree `take` printed, never a new branch";
   read the PR first (`gh pr view <n> --json state`, `glab mr view <n>`); open, go on; closed,
   `gh pr reopen` / `glab mr reopen` before any push, refused -> `handback <cr> blocked question: its
   PR <link> is closed and the forge refuses to reopen it: <exact text>`; merged -> `handback <cr>
   blocked question: its PR <link> is already merged` (Chief of Staff records `order merged`);
   "Then rebase on the base `take` names, ship to that PR: never open a second PR". The
   missing-worktree case (`worktree add <path> <branch>`) stays in the preceding sentence ("An
   earlier Driver's worktree is there: use it (its branch alone: ...)").
7. CR-398's rules in driver.md unchanged in meaning (783329d). VERIFIED.
   Read the whole 783329d diff of driver.md (62 insertions, 79 deletions): every hunk is a
   rewording or a removal of a duplicated sentence (rebase, first-push gate, PR body, ship, gate,
   CI, commits, end/hand-back); the closing hand-off (`context: closing: ...; next: ...`, 100,000
   tokens), one-Driver-per-CR rules, `ship --conflict`/early push, the `handback` refusals are all
   still present. Dropped sentences: "The fast gates you run yourself" (stated earlier in the same
   section) and "no look-alike" (AGENTS.md's no-fallback rule holds). No meaning change found.
8. CR-driver common-path budget (783329d). VERIFIED.
   `cd skills/chantier/scripts/cli && PYTHONPATH=src uv run --no-sync --project <main> pytest
   tests/test_startup_manifest.py tests/test_came_back.py tests/test_driver_prompt.py
   tests/test_plugin_files.py -q` -> `93 passed in 13.93s`, including
   `test_cr_driver_common_path_reads_at_most_the_card_budget` (limit 45_000) and test_came_back.py
   (PYTHONPATH makes the tests import the worktree's code, not the main checkout's).

VERIFIED

## Description pass at 783329d76788e78d04fb296588e6dac4eefa6653

Head: 783329d76788e78d04fb296588e6dac4eefa6653

The code verdict of the earlier pass stands (carried from 75b7a18 for the code; the move 524b899 and 783329d touched driver.md wording only). This pass judges the posted description alone (`gh pr view 371 --json body,headRefOid`: headRefOid 783329d76788e78d04fb296588e6dac4eefa6653).

- Summary, Deliverables, Changes match the diff against the PR base (`git diff --stat origin/<base>...HEAD`, 12 files): came_back.py, joining.py, opening.py, orders_apply.py, orders_release.py, core/batch.py (Batch.consume), driver.md, chief-of-staff.md, concepts.md, test_came_back.py, test_rail_refusals.py, scenario/run_scenario.py. No claimed change missing, none unmentioned.
- Test plan SHAs: `$CHANTIER log 399`: "before push at 783329d: just check: pass"; "before first push at 75b7a18: just eval-dry-run: pass"; "rebased ... pushed 524b899 ... verdict carried from 75b7a18"; `gh pr checks 371`: check x3, eval-dry-run, scenario all pass; log "CI: gh pr checks 371 at 783329d ... pass". Review: log "r2 approved at 524b899, committed as 783329d" and "r1 approved at a872a662, committed as 75b7a188" match the box. "Verified at 783329d": log note and the earlier verify.
- Internal references: CR-399 and CR-397 appear only in the Internal references section. Role names (Driver, Chief of Staff) are terms of the product, since the diff changes driver.md and chief-of-staff.md (pr-template rules).
- Known gaps: two bullets, honest; no UNVERIFIED claim, no failed accepted claim, no evidence pair uncaptured (Evidence: none, no visible change). No image, no STALE mark. Renders: sections, fold with blank line after summary.

VERIFIED
