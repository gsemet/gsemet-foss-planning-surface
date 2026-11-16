# Audit: two checks fail on lawful behaviour

## Goal

Real-direct run 1 (2026-11-12, PR 137; report `evals/results/real-direct-2026-11-12-run1.md` on
`origin/main`, findings 4 and 5) failed 6 of 636 audit checks, and 4 of those were the audit's
own mistakes. Fix `evals/kit/audit.py` so its J3 and C9 checks pass on what the cards allow, and
still fail on what they forbid. A false FAIL costs a hand check at every run and hides the real
ones.

This change touches the eval kit only.

## What changes

### 1. J3: a Verifier's detached worktree is lawful

**The cards.** `skills/chantier/references/worker.md` (lines 9-10 and 114-116) lets one worker
create one worktree: the Verifier makes a detached worktree of the CR's base for its "before"
capture (`git worktree add --detach <path> <base>`, "the one worktree a worker creates") and
removes it at its end. `driver.md` (lines 45-46) says the same. The J3 row of
`evals/SCORECARD.md` already says "no worker creates a worktree (except the Verifier's detached
one)".

**The bug.** In `claude_checks`, `evals/kit/audit.py` lines 493-495:

```python
if a.role in WORKERS | {"qa-driver"} | reviews:
    trees = [c for c in a.bash() if GIT_WORKTREE_ADD.search(c)]
    check(not trees, f"{a.id[:10]} ({a.role}) creates no worktree: the Driver did", "J3")
```

This applies to every worker, the Verifier included, and `GIT_WORKTREE_ADD` (line 89) matches any
`git worktree add`. Three Verifiers of run 1 (`a575690943`, `aa4b6f3168`, `ac57a2037e`) each ran
`git worktree add --detach … origin/main` and failed.

**The change.**

- When the agent's role is `verifier`, a `git worktree add` that carries `--detach` in its own
  arguments is not counted. Its own arguments run from the end of the `worktree add` match to the
  next command separator (`;`, `&`, `|`, newline), the same way the pushes are split at line 477.
  This is so that a chained command (`git worktree add --detach a x; git worktree add b y`) still
  fails on its second, non-detached call. Both `--detach` and its short form `-d` count as
  detached.
- Every other case still fails J3:
  - a Verifier's `git worktree add` without `--detach`;
  - any `git worktree add` by another worker (investigator, coder, inspector, debugger,
    conflict-resolver), by a QA driver, or by a review step.
- The check keeps its rail (J3) and its line for the other roles. For a Verifier, the line may
  say what is allowed (for instance `creates no worktree but its detached one of the base`). The
  Driver chooses the exact words.
- The audit does not check the base of the detached worktree, or that the Verifier removes it.

### 2. C9: the report refresh with no epoch passes in a direct batch

**The cards.** `skills/chantier/references/status-layout.md` (lines 11-12) and
`chief-of-staff.md` (line 27, line 312, and lines 525-530 in "Steering a batch yourself") require
`$CHANTIER status --refresh` *with no epoch* before every report. Only the loop's wake carries
`--refresh --epoch <n>`. In direct mode the steering transcript is the Chief of Staff's own, so it
holds both kinds of refresh.

**The bug.** `DIRECT_EPOCH_COMMANDS` (`evals/kit/audit.py` lines 69-70) matches every
`status --refresh`. The C9 check (lines 516-521) then fails every steering command it matches that
lacks `--epoch`. Run 1 failed one report refresh this way.

**The change.**

- In a direct batch (`direct`, from `batch.json`'s `steering: direct`), a `status --refresh` with
  no `--epoch` no longer fails C9. The simplest way is to take `status --refresh` out of
  `DIRECT_EPOCH_COMMANDS`, but the Driver chooses the means.
- In a direct batch, every other command of the list still needs its epoch: `take`, `cancel`,
  `pause`, `agents set` and `order done`.
- A Foreman batch is unchanged: `EPOCH_COMMANDS` keeps `status --refresh`, because a Foreman's
  refreshes are its wakes, and those carry the epoch (`foreman.md` lines 77 and 208).
- The C9 line printed in direct mode stops naming the refresh among the commands that carry the
  epoch. Today it reads "every steering refresh, take, agents set, order done, cancel and pause
  carries its epoch". The Foreman line is unchanged.
- **Accepted consequence:** in direct mode, a wake that forgot its epoch is no longer caught by
  C9. The command alone cannot tell a wake from a report refresh. A wake with no epoch moves no
  heartbeat, and the heartbeat rail (C10) already reads that.
- Keep the comment at line 70 accurate. If the module docstring or a comment names the refresh as
  an epoch command for direct mode, correct it there too.

### 3. `evals/SCORECARD.md`, only where it disagrees with the cards

- **J3 (line 49):** it already says "except the Verifier's detached one". Leave it unchanged.
- **C9 (line 35):** its rail lists `status --refresh` among the commands that carry the epoch,
  and its "audit" column says "every steering command of the steering transcript carries
  `--epoch`". That disagrees with the cards' report refresh with no epoch. Narrow it to the
  loop's wake, for instance "`status --refresh` on a wake". Say in the audit column that in a
  direct batch a `status --refresh` with no epoch is the report refresh and passes. Change nothing
  else in the row.

## Out of scope

- The two real FAILs of run 1 stay FAILs: the Verifier `ab3ea4ac68`'s write to the host's
  scratchpad (J3, "edits nothing but its notes and proof") and J14 (rules read before the claim,
  item `rules-after-claim`). Their own items fix them in the cards.
- Any card change (`skills/`), any CLI change, `agents/`, `com.github.copilot/agents/`, `hooks/`
  and `types/`.
- New checks: the Verifier's worktree base, its removal, or anything else.
- A planted case in the kit's dry run for either check.
- The Copilot audit.
- The run 1 report (`evals/results/real-direct-2026-11-12-run1.md`), which stays as written. A
  report is a record of its run.
- A C9 exemption in Foreman mode.

## Evidence

1. **`just check`** passes. This is the gate: the eval kit alone needs no `just scenario`
   (AGENTS.md).
2. **The kit's dry run** passes: `just eval-dry-run` (`uv run --no-project python
   evals/kit/dry_run.py`). Its staged run is a Foreman batch, so it must still pass C9 with the
   epoch on its wakes, and its planted cases must still fail where they did.
3. **Run 1, measured again on its transcripts.** The full audit cannot run again on run 1. Its
   batch was closed after the audit, so `.agents/changes/4-batch/` in its workspace
   (`C:/Users/gaeta/Projets/chantier-eval/real-direct-2026-11-12`) no longer holds `batch.json`
   or `events.jsonl`, and `audit.py` stops at line 1007 ("no batch in 4-batch/"). The run's
   transcripts are still on disk, under
   `C:/Users/gaeta/.claude/projects/C--Users-gaeta-Projets-chantier-eval-real-direct-2026-11-12/`:
   the Chief of Staff's session and its `subagents/agent-*.jsonl`. The proof uses them:
   - Read the commands run 1 flagged from those transcripts, as they were recorded:
     - the `git worktree add --detach … origin/main` of Verifiers `a575690943`, `aa4b6f3168`
       and `ac57a2037e`;
     - the steering session's `status --refresh` with no epoch;
     - the Verifier `ab3ea4ac68`'s write of `run3.py` to the host's scratchpad;
     - the steering session's commands from its claim on, for J14.
   - Run them through the changed `audit.py` itself. Import the module and call its own patterns
     and logic, never a copy.
   - Show that the four false FAILs (three J3 worktrees, one C9) now pass. Show that the two real
     ones still fail: J3 "edits nothing but its notes and proof" on `run3.py`, and J14 "the
     steering session read the project's rules".
   - The short script that does this is throwaway work. It is kept in the CR's `work/` folder and
     never committed to the kit.
   - Its command and its output go into the PR body, with the before (run 1's six FAIL lines,
     quoted in the report's "For maintainers") and the after.
4. **The PR body** gives the before and after FAIL lines and says which rails changed and why.
   It cites the cards' lines quoted above.
