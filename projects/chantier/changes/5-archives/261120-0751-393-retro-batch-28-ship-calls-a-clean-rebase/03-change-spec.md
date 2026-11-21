# Change Specification: a clean rebase in a stack carries, whatever branch the record or the forge names

## Goal

In batch-28 (retro, 2026-11-19), `ship` printed `off: ... does not carry: the rebase changed the
patch` after clean restacks: for CR-375 and CR-383 (restack A-19) and for CR-379 (order O-24). It
refused to carry the verdict and the long gate, and a fresh inspector or verifier run was ordered
each time. CR-379's Driver then found the rebase clean and carried both (ask A-28). CR-376's Driver
showed by hand that the patch-ids were unchanged.

The user's goal: before calling a patch changed, compare the patch-ids of the CR's own commits before
and after the rebase. Equal patch-ids carry the verdict and the gate.

## Why the CLI said "changed" when the patch-ids were equal

The patch-id comparison already exists (CR-332): `carry_check` in
`skills/chantier/scripts/cli/src/chantier/commands/crs.py` compares the exact patch-ids (`git
patch-id --verbatim`) of `<judged base>..<judged head>` and `<new base>..<new head>`, in order. The
fault is in which commits it counts as the CR's own. The base of a head comes from `head_base` in
`commands/carry.py`. It tries only three branch names:

- the start base, `stack_base(d, c, repo)`;
- the PR's base as `ship` last read it, `c.pr_base`;
- the planned place, `stack_base(d, c, repo, planned=True)`.

From those whose remote tip is an ancestor of the head, it keeps the nearest. In a stack, during a
restack, none of the three names the branch just under the head:

- a CR that `stack <cr>...` has not marked yet (`c.stacked` false) has its planned place equal to
  its start base. That is the default branch, or a dependency such as CR-369 for CR-383 (the CR-390
  bug);
- the PR's base on the forge is still the old one until `forge-stack rebuild`, which the stack
  driver runs after `ship`;
- the remote tip of the CR below is stale while the stack driver has rebased it locally and not yet
  pushed it.

The default branch's tip is still an ancestor, so `head_base` returns it. The new range
`main..head` then holds every lower CR's commits too, the two lists differ in length, and `ship`
prints `the rebase changed the patch`. The same miss at `gate` or `verdict` time records too low a
`base`, and a later carry compares a judged list that holds lower CRs' commits. A later `ship` that
carried (CR-379, A-28) ran once the record or the forge named the right base.

`ship` also says "changed" when one of its two git calls fails: `_patch_ids` runs `git log` and
`git patch-id` with `check=False` and reads an empty list.

## What changes

### 1. The base a head sits on: every branch of the batch is a candidate (`commands/carry.py`, `head_base`)

`head_base(repo, d, c, wt, head)` keeps its rule, "the nearest candidate tip that is an ancestor of
the head", and its signature. The candidates become, read in the CR's worktree:

1. the three existing names (start base, `c.pr_base`, planned place), by their remote tips, as
   today;
2. the remote tip of the default branch (`<remote>/<default_branch>`);
3. for each other CR of the batch (`d.crs`, not `c` itself, and not `cancelled`): its branch's
   remote tip (`<remote>/<branch>`) and its local tip (`refs/heads/<branch>`), each one that git
   can read.

A cancelled CR's branch is never a base. When the head still holds a dropped CR's commits, they
count as the CR's own, so the carry is refused until the drop's `rebase --onto` removes them
(`driver.md`, "Removing a dropped CR").

The local tip is what lets the carry hold when the stack driver has rebased the CR below and not yet
pushed it. The remote tip covers a branch with no local ref in this clone.

`Base.branch` stays the branch name. It is what the `carried: ... (clean rebase onto <branch>)`
line prints, the same whether the remote tip or the local tip was nearer. `Base.sha` is the tip's
full SHA. When two candidates have the same SHA, the first in the order above names it.
`head_base` stays read-only.

Every caller takes the wider rule with no edit of its own: `gate` (`commands/gate.py`, the `base`
recorded on every gate event), `verdict` (`commands/delivery.py`), `ship_carry`
(`commands/carry.py`), `handback ready` (`commands/driver_checks.py` `_carry_why`, and
`commands/driver.py` for the `(clean rebase onto ...)` words), and the gate and verdict boxes
(`commands/facts.py` `_carried_lines`). The judged side and the new side therefore both count, as
the CR's own, the commits above the nearest branch of the batch or the default branch.

### 2. The carry check names a git failure, and a changed patch says by how much (`commands/crs.py`)

- `_patch_ids(wt, base, head)` checks both processes. When `git log` or `git patch-id` exits non-zero,
  `carry_check` returns `git could not read the patch-ids of <base7>..<head7>: <first line of git's
  stderr>`. A failure is never read as an empty list, and so never as "changed".
- When the two lists differ, the reason becomes `the rebase changed the patch (own commits: <n> at
  <g7> above <gbase7>, <m> at <h7> above <hbase7>)`. When the counts are equal, it names
  the first differing commit instead: `the rebase changed the patch (commit <i> of <n> differs)`.
  The reason reaches the `off:` lines of `ship`, the hand-back's `does not carry: <why>` and the
  boxes as today. The Driver or the stack driver reads at once whether a base was missed (counts
  differ) or a commit changed.
- Unchanged: one method only, `git patch-id --verbatim`, compared in order (CR-332's decision,
  carry-Q8). Still refused: a git older than 2.39, a judged event with no recorded base, a merge
  commit on either side, a ref git cannot read, and a `ship --conflict` at or after the judged
  head (carry-Q10). A whitespace-only change still does not carry.

### 3. Cards (`skills/chantier/references/driver.md`)

- The long gate bullet (around lines 250-258, "`ship` checks both with git ..."). After "on the base
  the judged head sat on and on the base the new head sits on", add that this base is the nearest
  branch under the head among the batch's CRs' branches (local or remote) and the default branch,
  read by git, whatever the record or the PR names. When `off:` says the patch changed, it gives
  both counts: unequal counts mean the CR's own commits were miscounted, which is an anomaly to
  report, not a reason to re-verify.
- The stack driver's paragraph (around line 897, "when the move changed a CR's patch (a
  `conflict-resolver` ran, or the carry is refused)") is unchanged: a refused carry still gets a
  `verifier` and an `inspector`. This CR only makes the refusal true.
- The same edit goes into the Copilot and Claude Code agent files only if they quote this text.
  They do not today (the contract lives in the cards), so none is expected.

## Decisions carried from `02-answers.md`

- The intent is the grill, settled by the Chief of Staff on 2026-11-20 (the user asks no
  questions). This CR joins batch-29 (factory, stack) once specified.
- The intent's method holds: patch-ids of the CR's own commits, before and after the rebase. Equal
  patch-ids carry the verdict and the gate. `git range-diff` is not added: the exact patch-id is
  already the one method (CR-332, carry-Q8), and what was wrong was the range, not the
  comparison.

## Out of scope

- Which base `take`, `take stack` and the record give a CR in a stack batch: that is CR-390 (in
  batch-29). This CR does not depend on it and does not edit `stacks.py`. With CR-390 merged or
  not, `head_base` finds the nearest branch from git.
- Accepting a judged list longer than the new one, such as a suffix match for events recorded with
  too low a base before this change. A dropped own commit would pass such a check, so it is not
  done. Those older events keep their one-time cost (see Known gaps).
- The `ship --conflict` rule, the verifier and inspector rules after a refused carry, and the
  forge reads of `ship`.

## Known gaps (for the PR)

- A head judged before this change merges, whose `gate` or `verdict` event recorded too low a base
  (the default branch instead of the CR below), still does not carry at its next move. It gets a
  new long gate and a verifier once. From the next judgment on, the recorded base is the nearest
  branch.

## Evidence

Tests, in-process on a prepared repository, in
`skills/chantier/scripts/cli/tests/test_carry_ship.py`. They reuse its `stack` fixture, extended to
three CRs where a case needs it, and `test_gate_carry.py`'s `commit` and `git_at`. Keep them few and
parametrized, within the `just test` budget of AGENTS.md:

1. **The batch-28 shape, carried (parametrized).** A stack batch whose upper CR was judged (gate
   pass, and a `verdict VERIFIED` with its `verify.md` `Head:` line) on the default branch. It is
   then rebased cleanly onto the CR below, with **no** `stack <cr>...` before `ship`, and the PR's
   base read as `main`. Today this case prints `the rebase changed the patch`. Cases:
   - `pushed`: the CR below's remote tip is its new tip;
   - `local only`: the CR below was amended and the upper CR rebased onto it, with the remote ref
     left at the old tip (only `refs/heads/<branch>` has the new tip);
   - `three CRs`: C rebased onto B, which sits on A, with C's start base `main`.

   Each case asserts that `ship` logs one `carry` event with `gate_from` and `verdict_from` equal to
   the judged head and `base` equal to the tip of the CR just below, and prints `carried: long gate
   and verdict from <sha7> (clean rebase onto <that CR's branch>)` and no `off: ... does not
   carry`.
2. **The base at judgment is the nearest branch.** In the `three CRs` shape, `gate` on C, sitting on
   B's tip with neither record nor PR naming B, records `base` = B's tip.
3. **A real change is still refused, with its counts (parametrized).**
   - a commit added on top after the rebase: `off:` reads `the rebase changed the patch (own
     commits: 1 at <g7> above ..., 2 at <h7> above ...)`;
   - one own commit edited: `(commit 1 of 1 differs)`;
   - a cancelled CR's commits left under the head (its branch is not a candidate): refused, the
     counts differ.
4. **A git failure is named, not "changed".** `_patch_ids` (or `carry_check`) with a git that fails
   on `git patch-id` (monkeypatch `subprocess.run` for that argv only) returns `git could not read
   the patch-ids of ...`.
5. The existing tests in `test_gate_carry.py` (exact patch-ids, whitespace, merge commit, no base,
   old git, unreadable ref) and `test_carry_ship.py` pass unchanged, or with only the reason text
   updated where one asserts `the rebase changed the patch` by equality. The new text starts with
   those words (`test_gate_carry.py`'s cases at lines 92 and 98).

Gates (AGENTS.md): `just check`; before the first push, `just eval-dry-run` (a change under the
CLI's `src/`); `just scenario` green at the PR's head (a CLI and cards change). The scenario's
existing restack steps exercise `ship`'s carry. The scenario's check of that reason
(`scenario/run_scenario.py`, around line 5536) matches `does not carry: the rebase changed the
patch` as a substring, so it holds as is.

No host or default matrix: the behaviour depends on neither the host nor a configured value.
