# The sandbox merge waits for the restack's checks

## Goal

In a stack run on the eval sandbox, each bottom merge makes GitHub restack the PRs above and rerun
their CI. The operator's next `sandbox.py merge <n>` then meets a pending check at the new head
and is refused at once (real-foreman run 2 of 2026-11-15: `sandbox.py: refused: PR #7's checks are
not all green at its head 59edd1f: test=pending; nothing merged`; the operator ran
`gh pr checks <n> --watch`, 10-20 s, and merged on the retry). After this change, `merge` waits
for the checks at the PR's head, for a bounded time, instead of refusing at once; the README says
so. Evidence: `C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md`, item 4.

Planned by the user (2026-11-15, `02-answers.md`) for the next batch, run in parallel, before the
next release. No issue line: the CR has none.

## Starting point (PR #224, merged on main as 0819a22 and b07c8d5)

`evals/kit/sandbox.py`, `cmd_merge`: reads the run record, then `merged_with(n)` (the PRs a merge
of #n takes: #n alone, or the open native stack's PRs from the bottom up to #n, from
`gh api repos/<REPO>/stacks`), then one `gh pr view <m> --json
number,state,title,headRefOid,statusCheckRollup` per PR and `merge_refusal(view, prefix)` on each;
the first refusal prints `sandbox.py: refused: <reason>; nothing merged` and exits 2. Then
`merge_async(n, sha)` (`PUT .../pulls/<n>/merge-async`, read every `MERGE_WAIT` s, at most
`MERGE_TRIES` reads). `checks_green(rollup)` is shared with the audit's J5.

## What changes

### `evals/kit/sandbox.py`, `merge`

1. **Which refusal waits.** Only a refusal for checks that are not finished waits: the rollup
   holds no failed check and at least one pending one. A check is pending when it is a check run
   whose `status` is not `COMPLETED` (its `conclusion` empty), or a status context whose `state`
   is `PENDING` or `EXPECTED`; the fake forge's pending check (`status: IN_PROGRESS`,
   `conclusion: ""`) is one. A rollup with no check at all also waits (the restacked head's CI may
   not be registered yet when the merge reads it; see the open question). Every other refusal
   stays immediate, as today: the PR not open, the title without the run's prefix, any check
   finished and not `SUCCESS` (failure, cancelled, skipped, neutral...), even when another check is
   still pending.
2. **The wait.** While a PR the merge takes waits, `merge` reads again, every `CHECKS_WAIT`
   seconds, for at most `CHECKS_TRIES` reads (suggested 10 s and 30, so 300 s; module constants
   beside `MERGE_WAIT`, `MERGE_TRIES`; no new option, no environment variable). Each read redoes
   the whole check from `merged_with(int(n))` on: the stack and the heads may have moved with the
   restack. The merge goes ahead at the first read where every PR it takes passes
   `merge_refusal`; the head it passes to `merge_async` is the one that read gave
   (`--match-head-commit` semantics unchanged: a head that moves after that read makes the forge
   refuse, as today). A read whose refusal is not a waiting one (point 1) refuses at once, with
   that reason.
3. **Messages.** When the wait starts, one line on stdout, flushed:
   `waiting for the checks of PR #<m> at its head <sha7> (up to <N> s)` (for a stack, the PR that
   waits). No line per read. When the bound passes still pending: the usual refusal with the
   wait named, exit 2, nothing merged, e.g.
   `sandbox.py: refused: PR #7's checks are not all green at its head 59edd1f after waiting 300 s: test=pending; nothing merged`.
   The success line is unchanged (`merged PR #<n> at <sha7> into main by rebase (...)`).
4. **Unchanged:** the command line and the merge line `setup.py` prints (so the allow rule the
   dry run checks still matches `<merge line> <n>`), exit codes (0, 1, 2, 4), `checks_green` (the
   audit's J5 rule), `merge_refusal`'s reasons, `merge_async`, `reset`, `build`. Standard library
   only; POSIX and Windows.
5. The module docstring's `merge` sentence, if it names the refusals, says that a pending check is
   waited for, bounded.

### `evals/kit/sandbox_forge.py` (the dry run's fake `gh`)

`mark_pending(ref)` keeps a head pending forever (today's behaviour). Add a way to stage a head
that is pending for its first `k` reads of `statusCheckRollup`, then has its real (or a given)
conclusion, kept in the state file (it is read by a new process per `gh` call). Update the module
docstring's sentence on pending heads.

### `evals/kit/dry_run.py`

- `case_merge_refused`: the failed and the unprefixed PRs are still refused through the operator's
  merge line (subprocess, as now), and each refusal comes back without waiting (it prints no
  `waiting for` line). The forever-pending PR is still refused (exit 2, `refused:`, `pending`,
  `after waiting`, `nothing merged`, the PR stays open), without the dry run taking the real bound:
  call `sandbox.main(["merge", <n>, "--workspace", <ws>])` in-process with `CHECKS_WAIT` and
  `CHECKS_TRIES` patched small (the Driver checks that the fake `gh` is on this process's `PATH`
  and `FAKE_GH_STATE` set, as the dry run's other in-process calls need), or an equivalent that
  keeps the operator's line untouched.
- A new staged PR (in this case or a new case added to `CASES` and the docstring's list): pending
  for its first 2 reads, then `SUCCESS`; `merge` prints the `waiting for` line, then merges it
  (`merged PR #<n>`), the PR is merged on the forge. Same in-process, patched-constants call.
- The case's returned summary line says what it now proves.

### `evals/README.md`

- "A merge" (around lines 86-89): the merge command refuses a PR not open, without the run's
  prefix, or with a check finished and not green; a pending check (as after a stack's restack) is
  waited for, up to the bound, then refused; the operator no longer needs `gh pr checks --watch`
  before a merge.
- The `kit/sandbox.py` row of the kit table (around line 275) and the `sandbox.py merge` paragraph
  (around lines 309-314): the wait and its bound, in one sentence each.

## Out of scope

- The judge reading heads the restack replaced (same audit, item 5), `cost` on a paused batch
  (item 6): other CRs.
- Native stacks in the fake forge (it still answers no stack); the asynchronous merge's own wait
  (`merge_async`) as it is.
- The chantier CLI, the cards, the agents, `just scenario`, CI files: untouched. No CI job is
  added or changed.

## Evidence

- `just check` passes (Linux, macOS, Windows).
- `just eval-dry-run` passes locally, and its pipeline job `just eval-dry-run (ubuntu-latest)` is
  green at the PR's head; the `merge-refused` case (and the new one, if separate) proves: failed
  and unprefixed refused at once, forever-pending refused after the (patched) bound, pending-then-
  green waited for and merged; `stale-lock` still has its release PR refused for a failed check.
- Gate: a change to the eval kit alone needs no `just scenario` (AGENTS.md).
- What only a real run proves: the shape of GitHub's rollup on a restacked head (an empty rollup
  first, or pending checks at once) and that 300 s covers the sandbox's CI; the next real-foreman
  run in a stack is the proof (each `merge` after a bottom merge prints `waiting for` and merges,
  with no refusal and no `gh pr checks --watch`). The PR's Known gaps name it.

## Open questions for the user

1. A PR whose head has no check at all yet (the restacked head before its CI is registered): wait
   for it, up to the bound, as this specification says, or refuse at once as today (and wait only
   for a check that is there and pending)? Waiting means a PR with no CI at all is refused only
   after the bound.
