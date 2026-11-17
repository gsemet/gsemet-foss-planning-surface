# Change Specification: the batch pauses when its last CR ends, and the close is offered

## Goal

When the last CR of a batch ends (merged, released or cancelled), the batch is paused at once,
its merged CRs' worktrees and branches are cleaned, and the user is asked, unprompted, whether to
close the batch. Today (batch-22, direct mode) the steering session skipped the pause after the
last merge, never offered the close, and the user's "close" was refused "running, not paused". In
the user's words: "as it is finished it must have been paused automatically, and you should have
cleaned what had to be cleaned and asked me whether I want to close the batch."

## Decisions carried from `02-answers.md`

- **auto-pause-Q1 (who pauses):** the CLI, at once. The `order merged` that records a batch's last
  CR runs the pause itself, and removes the merged CRs' worktrees and branches with it. The
  steering session (the Foreman, or the Chief of Staff in direct mode) then only writes the retro
  and offers the close.
- **auto-pause-Q2 (the close):** offered, on the user's yes. The steering session shows the bilan
  (`close` without `--yes`) and asks at once, unprompted; `close --yes` runs only on the user's
  yes, as today.
- Spec critic: yes (the CLI's lifecycle and the steering session's contract change).
- **Spec questions of 2026-11-17:**
  - **auto-pause-Q2b (pending orders):** the automatic pause marks done every pending order the
    CLI fully applied (`applied: true`); only a note, a QA order or the drop of a live CR blocks
    it.
  - **auto-pause-Q3 (git refuses a removal):** the worktree is kept (no `--force`), a
    `cleanup: ... not removed` line is printed, and the batch is paused anyway; the user decides
    at `close`.
  - **Kept worktrees at `close`** (the Chief of Staff, 2026-11-17): `close` also names, in its
    line of worktrees and branches to remove on the user's word, every merged CR whose worktree
    folder or branch still exists, read from the record, so a session that lost the pause's
    output still shows them.
  - **auto-pause-Q4 (other ends):** `handback released`, `cancel` and `order drop` of the last CR
    also pause and clean at once.
  - **auto-pause-Q5 (`AGENTS.md`):** the PR amends `AGENTS.md` to name this git exception of the
    CLI.
  - **auto-pause-Q6 (`status` flag):** kept: "every CR is merged or cancelled, not paused: <what
    blocks>".
  - **auto-pause-Q7 (a Driver that may still run):** the CLI skips any merged CR whose agent the
    record still holds, prints `cleanup: <cr> kept: agent <id> still held`, and still pauses; the
    steering session removes that worktree once the Driver has ended.
  - **auto-pause-Q8 (Windows, an open worktree):** the CLI removes only worktrees whose Driver has
    ended (Q7); this specification states the partial-delete case and points to
    `git worktree prune` and the user's word for a leftover folder; one test runs on Windows with
    an open handle.
  - **The close and the retro critic** (close-batch-agents-only, close-agents-Q5): the steering
    session offers or runs `close` only after its retro critic has handed back.

## What changes

### 1. CLI: the end of a batch's last CR pauses the batch

Files: `skills/chantier/scripts/cli/src/chantier/commands/orders.py` (`order`),
`commands/orders_apply.py` (`_merged`, `_drop`), `rails_release.py` (`merge_done`),
`commands/driver.py` (`handback`, the release's `released` branch), `commands/release.py`
(`cancel`), `commands/closing.py` (`pause`), `core/git.py` (`git`), `rails.py` (`all_merged`).

- **The triggers.** Four commands, once they have recorded their CR's end and `all_merged(b.record)`
  (every CR merged or cancelled) is now true:
  1. `order merged <cr>` of an ordinary CR (`merge_done`), in both forms: the Chief of Staff's
     (no `--epoch`) and the steering session's own (`--epoch <n>`);
  2. `handback <cr> ready <version>` of a release CR with no PR recorded (`driver.py`: the CR
     `released`, in `3-done`, status `merged`); the release Driver runs this itself;
  3. `cancel <cr> --epoch <n>` (the steering session's, on the user's word);
  4. `order drop <cr>` of a CR that is not live (`_drop`: the CR trashed, status `cancelled`).

  Never a trigger: a release CR's `order merged` (`release_merged`, the CR goes back to `queued`);
  an `order merged` on a CR already merged (`already merged`); an `order drop` of a live CR (it
  only prints that the Foreman stops its Driver, then `cancel`, which is then the trigger).
- **What it checks** (auto-pause-Q2b). The same conditions as `pause` (`closing.py`): no CR
  live, queued, ready or blocked, no stack driver recorded, and no pending order, with one
  difference: pending orders
  the CLI applied in full (`applied: true` in the record, set by `_record_order`: `merged`,
  `drop` of a CR not live, `rounds`, `slots`, `budget`, ..., including the order being recorded
  now) do not block it, and the pause marks each of them done (`done` set, as `order done`
  would). A pending order the CLI did not apply in full (a `note`, a `qa`, the drop of a live CR)
  blocks it.
- **Order of its steps,** once the end is recorded and the locks of the command released:
  1. **The cleanup.** For each CR of the batch recorded `merged`:
     - **its agent still recorded** (`CrEntry.agent` set: its Driver may still run, as a release
       Driver does when it runs `handback released`, or a Driver the steering session has not
       yet cleared with `agents set <cr> -`): nothing is touched, and one line is printed,
       `cleanup: <cr> kept: agent <id> still held`;
     - **otherwise:** `git worktree remove <worktree>` when the folder exists, then
       `git branch -D <branch>` when the branch exists, through `core/git.py`'s `git`, in the main
       checkout (the repository root), or with a planning surface in the project's clone
       (`Repo.clone`, as `git -C <clone>`). No `--force` on `worktree remove`: a worktree with
       changes, or locked, is refused by git and kept. When git refuses the worktree's removal,
       its branch is not tried (git refuses to delete a branch a worktree still holds) and stays.
       A refusal prints one line, `cleanup: <cr> <worktree path and/or branch> not removed: <git's
       message, one line>`, and does not stop the pause.

     A cancelled CR's worktree and branch are never touched: they stay for the user's word at
     `close`, as today. A merged CR's worktree or branch left here (`kept:` or `not removed:`)
     is named by `close` too (part 2).
  2. **The pause.** The body of `pause` runs, factored out of `closing.py`'s `pause` so all share
     it: the cost to date computed and recorded (`cost_rows`, `record_costs`, `cost_summary`,
     "Spent: unknown (...)" when it cannot be read, never a false $0.00), the record set
     `status: paused`, `paused`, `summary`, `heartbeat_stopped`, and a `pause` event logged. The
     event names its trigger (the order's id, `handback <cr>` or `cancel <cr>`), so the log tells
     an automatic pause from a `pause --epoch <n>`. This shared body is the only place a pause is
     recorded: whatever a later change adds at the pause (the pending `1-inbox/batch-takeover`'s
     publish-at-pause, for one) goes in it, and so covers every pause, the automatic ones and
     `pause --epoch <n>`.
- **What it prints.** The command's usual lines, then, in place of today's `every CR is merged or
  cancelled: \`chantier pause --epoch <n>\`` (printed today by `merge_done`, `handback released`
  and `cancel`):
  - one line per merged CR: `cleanup: <cr> worktree <path> and branch <branch> removed`, or the
    `kept:` or `not removed:` line above;
  - `paused <batch>: every CR is merged or cancelled; cost to date below`, the `report:
    <STATUS.md path>` line and the cost summary, as `pause` prints them;
  - `next: the retro (with its critic), then offer the close (\`chantier close\`, then \`close
    --yes\` on the user's yes)`, and, when a `kept:` or `not removed:` line was printed, `kept:
    remove them once their Driver has ended, or on the user's word at \`close\`, which names
    them`.
- **When the pause cannot run** (a blocking order, a stack driver recorded): the end stays
  recorded, nothing is cleaned, and the command prints `every CR is merged or cancelled, not
  paused: <the causes, as pause names them>; \`chantier pause --epoch <n>\` once they are done`.
  The command itself succeeds (its usual exit code).
- **`pause --epoch <n>` stays** as it is, for a batch whose automatic pause was blocked. It does
  no cleanup (the steering session's git, as today).
- **Windows: a worktree a process still holds.** The CLI removes only worktrees whose Driver has
  ended (Q7), but on Windows another process (an editor, a stray shell or gate process, an
  indexer) may still hold a file open in one. `git worktree remove` can then delete part of the
  files and fail on the held ones: the folder stays, partly emptied, and git's message is printed
  in the `not removed:` line, the branch kept. The CLI does not retry, force or delete the folder
  itself. `close` names it (part 2) and the steering session tells the user at the close offer;
  once the folder is gone (the
  holding process ended, the folder deleted on the user's word), `git worktree prune` clears git's
  entry for it, then `git branch -D <branch>`. Those are the steering session's git, on the user's
  word for the folder.
- **The project's rules.** This gives the CLI two git writes it does not have today (`git worktree
  remove`, `git branch -D`), which `AGENTS.md` forbids as written ("The agents do the work, git and
  the forge included"; "chantier writes only in the planning folder ..."; "The board's server is
  also the CLI's one git exception ... The rest of the CLI keeps no git write."). The PR amends
  `AGENTS.md` (the user agreed, auto-pause-Q5), in the same words as the other named exceptions:
  - the CLI's scope bullet and the "chantier writes only in ..." list name it: the end of a
    batch's last CR (`order merged`, `handback released`, `cancel`, `order drop`) removes the
    batch's merged CRs' worktrees and branches whose Driver has ended, from the main checkout or
    the project's clone, with no `--force`, and nothing else;
  - the board bullet's "the CLI's one git exception ... The rest of the CLI keeps no git write" is
    rewritten as two named exceptions: the board's server (it may serve without joining the
    planning surface's autosync group) and the batch's end cleanup (above); the rest of the CLI
    keeps no git write.

### 2. CLI: `close` names the merged CRs' leftover worktrees and branches

Files: `commands/closing.py` (`_closing`, the `dropped` list and its `tail` line), `core/git.py`
(a read: whether a branch exists).

- Today `close` (with or without `--yes`) prints one line, `the dropped CRs, to remove on the same
  word where they still exist (\`git [-C <clone>] worktree remove --force\`, \`git branch -D\`):
  <cancelled CRs' worktree and branch> | none`, read from the record's `cancelled` CRs.
- It now also names, in that same line, every CR recorded `merged` whose worktree folder still
  exists (`Path(c.worktree).exists()`) or whose branch still exists (a git read in the main
  checkout or the project's clone, `git [-C <clone>] rev-parse --verify --quiet
  refs/heads/<branch>`), with only what still exists of the two. The line's head names both
  kinds: `the dropped CRs and the merged CRs' leftovers, to remove on the same word where they
  still exist (\`git [-C <clone>] worktree remove --force\`, \`git branch -D\`; for a folder git
  no longer knows, \`git worktree prune\` once it is deleted)`; each entry says which kind it is:
  `<cr> (dropped) worktree <path> branch <branch>` or `<cr> (merged) worktree <path> branch
  <branch>`.
- Nothing else in `close` changes: its refusals, its pricing, its archive, and what `--yes` does
  itself. The removal stays the Chief of Staff's git on the user's yes, as for the dropped CRs
  today; the CLI removes nothing at `close`.

### 3. CLI: `status` flags a complete batch that is not paused

Files: `commands/batch_status.py`, `status/views.py` (the text `status` prints, the heartbeat's
`status --refresh --epoch <n>` included). Kept by auto-pause-Q6.

- While the batch is `running` and `all_merged` is true (an automatic pause was blocked), `status`
  prints one line: `every CR is merged or cancelled, not paused: <what blocks: the pending orders,
  the stack driver, or "nothing">; \`chantier pause --epoch <n>\``.
- Not in `STATUS.json`'s fields the CR board pane reads (`hooks/register.tsx`), so no pane
  change and no screenshot rule.

### 4. Cards

Both hosts read the same cards; no agent file changes.

- `skills/chantier/references/foreman.md`:
  - "Your goal" (lines 22-27): every CR merged or cancelled; the end of the last CR (your
    `order merged`, `cancel`, the Chief of Staff's `order merged` or `order drop`, a release
    Driver's `handback released`) cleans the merged CRs' worktrees and branches and pauses the
    batch; then your retro (with its critic) and, once the critic has handed back,
    `[foreman→chief-of-staff] final <STATUS.md path>`. Your own `pause --epoch <n>` only when the
    CLI says the automatic pause did not run, with the cleanup before it as today.
  - "The retro is yours: before `pause`": becomes after the pause and before `final`. The retro
    critic's cost lands after the cost to date; `close` prices it in the final cost.
  - "Never code, review, ..." (lines 139-143): the merged CRs' cleanup is the CLI's at the
    batch's end; yours only before a `pause --epoch <n>` of your own, for a CR the CLI printed
    `kept: agent <id> still held` (once its Driver has ended and you ran `agents set <cr> -`:
    `git worktree remove`, `git branch -D`), and for a removal the CLI printed `not removed`
    (named to the Chief of Staff in `final`; `close` names it too, for the user's word there; a
    partly deleted folder on Windows: `git worktree prune` once the folder is gone).
  - "The main checkout after a merge" (lines 440-446): "by git (the CLI runs none)" becomes: by
    git; the CLI runs no fast-forward (it removes, at the batch's end, only the merged CRs'
    worktrees and branches). For the last merge, the order is already marked done by the pause;
    the fast-forward still runs right after it, with its `main checkout:` note (`note` on a paused
    batch passes `--batch <batch>` where the CLI asks for it).
  - Lines 439-440 ("removed by the usual cleanup before `pause`"): by the CLI at the batch's end.
  - The Heartbeat bullet (lines 621-632): "right after `pause`" becomes right after the pause,
    yours or the automatic one: cancel the armed wake then, where ending it is yours. The record
    alone does not stop it: the pause records `heartbeat_stopped`, but a later wake's
    `status --refresh --epoch <n>` resets it (`commands/batch_status.py`, lines 64-66) and the
    heartbeat goes on. So `pause` "records it itself" stays true for every pause, and cancelling
    the wake stays the steering session's step.
- `skills/chantier/references/chief-of-staff.md`:
  - "Steering a batch yourself", "The pause" (lines 1462-1479): the end of the last CR (`order
    merged <cr> --epoch <n>`, `cancel`, `order drop`, a release Driver's `handback released`)
    pauses the batch and cleans; then, in the same turn: cancel the armed wake (as the host's
    reference says), the fast-forward, the retro with its critic, the Completion report with the
    Retro offered, then, **once the retro critic has handed back, the close offered at once,
    unprompted**: run `$CHANTIER close --batch <batch>` (the check, no `--yes`), show the bilan,
    the final cost, what goes, and its line of worktrees and branches to remove, which now names
    the merged CRs' leftovers beside the dropped CRs' (with why each was kept, from the cleanup
    lines when the session still has them), and ask "close the batch?"; `close --yes` only on the
    user's yes, as the Closing bullet says, and on the same yes remove every entry of that line,
    merged and dropped alike (`git worktree prune` for a folder git no longer knows).
    When the CLI printed that the pause did not run, do what blocks it, then the cleanup and
    `pause --epoch <n>` as today.
  - Line 1461 ("A paused batch is not running: all of this lifts at the pause."): when the CLI
    paused the batch, the steering session's retro and its retro critic run after the pause and
    before `final` (in direct mode, before the close offer); what lifts at the pause does not lift
    them.
  - "The pause" (Foreman mode, lines 1208-1240): on the Foreman's `final`, the same close offer,
    unprompted, after the Completion report and the Retro; the merged CRs' leftovers are in
    `close`'s line of worktrees and branches to remove, whatever `final` said. In Foreman mode the Chief of Staff's own `order merged <cr>` or `order drop <cr>` of the
    last CR prints the pause: still send its line to the Foreman (it cancels its armed wake, runs
    the fast-forward, the retro with its critic, and `final`); the close is offered after `final`,
    never before (the Foreman's retro critic must have handed back).
  - "Closing" (line 1290): "only on the user's word" stays for `--yes`; the check without `--yes`
    is now also run unprompted at the pause, to offer it, and only once the retro critic has
    handed back (close-agents-Q5). Where it names the dropped CRs' worktrees and branches removed
    on the same word, it now names the merged CRs' leftovers too.
  - The task table, rows "the `final` message, the batch paused" and "close the batch" (lines
    28-29): the close offered at the pause.
  - The Tips "End of a batch" example "close the batch" is dropped (the close is now asked).
- `skills/chantier/references/driver.md` (line 993, the release Driver's `handback ready <release
  link or tag>`): the `handback` may print the pause and `cleanup:` lines,
  its own worktree `kept: agent <id> still held`; it changes nothing in what the Driver does
  next (its hand-back line to the steering session, then its end).
- `skills/chantier/references/concepts.md`, "Batch lifecycle":
  - step 2 "Complete" (lines 247-249): the end of the last CR removes each merged CR's worktree
    and branch whose Driver has ended and pauses the batch; the steering session runs `pause`
    itself only when that did not happen, and removes the worktrees the CLI kept once their
    Driver has ended.
  - step 3 "Paused" (lines 250-252, "... has written the batch's retro for this pause"): when the
    CLI paused the batch, the steering session's retro and its retro critic run after the pause
    and before `final` (in direct mode, before the close offer); when the steering session ran
    `pause` itself, as today.
  - "Each CR is named a branch ..." (line 242): a merged CR's worktree is removed by the CLI at
    the batch's end, or by the steering session when the CLI kept it.
- The host references, Heartbeat sections:
  - `references/hosts/claude-code.md` (lines 63-64, "right after `pause`"): right after the pause,
    the steering session's own or the automatic one, it runs `ScheduleWakeup` `stop: true`; the
    record (`heartbeat_stopped`, which every pause writes) does not stop the wake, and a later
    wake's `status --refresh` resets it.
  - `references/hosts/copilot.md` (lines 56-62, "At the pause the Chief of Staff tells the user to
    delete the `/every`"): at every pause, the automatic ones included, the Chief of Staff tells
    the user to delete the `/every` (in direct mode, in its own session); until it is deleted,
    each `/every` wake clears the mark, which is true.

### 5. Docs

The same story, where they tell it: `docs/tutorial-claude-code.md` (line 187),
`docs/planning-folder.md` (line 74), `docs/use-cases-foreman.md` (line 101),
`docs/use-cases-direct.md` (line 65), `docs/planning-modes.md` (line 21, the worktree removal),
`docs/batch-lifecycle-texts.md` and `docs/batch-lifecycle.svg` (and `cr-lifecycle-texts.md` /
`cr-lifecycle.svg` where they name the cleanup), redrawn by their own method.

## Out of scope

- An automatic close: `close --yes` stays the user's yes.
- The CLI forcing a removal, retrying it, deleting a leftover folder or running
  `git worktree prune`: those stay the steering session's git, on the user's word for a folder.
- The CLI touching a cancelled CR's worktree or branch.
- The CLI fast-forwarding the main checkout: it stays the steering session's git.
- The CLI cancelling the heartbeat's armed wake: it stays the steering session's (or, on Copilot,
  the user's) step.
- Any other change to `close`: its refusals, its pricing, its archive, and the CLI removing
  anything at `close` (part 2 only adds names to one line).
- The CR board pane and `STATUS.json`.
- Publishing at the pause: `1-inbox/batch-takeover`'s; this CR only makes the shared pause body
  the one place it would go.

## Items touching the same lines

- `1-inbox/batch-takeover` (pending; its publish-at-pause goes in the shared pause body, part 1)
  and `2-backlog/P1/close-batch-agents-only` both edit `chief-of-staff.md`'s Closing and
  `concepts.md`'s Batch lifecycle. Whichever of them and this CR merges second rebases on the
  first; no `depends.json`.

## Evidence

- **Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; in
  `test_rail_refusals.py` or `test_cli_runs.py`, with a real git repository from the fixtures):
  - one parametrized test over the four triggers (`order merged` in both forms, `handback
    released` of a release CR, `cancel`, `order drop` of a queued CR) as the last CR's end: the
    batch `status: paused`, `paused`, `summary` and `heartbeat_stopped` set, the pending applied
    orders marked done, the merged CRs' worktrees and branches gone (agent cleared), a cancelled
    CR's kept;
  - a merged CR whose agent is still recorded (and, in the `handback released` case, the release
    CR itself): its worktree and branch kept, the `kept: agent <id> still held` line, the batch
    paused;
  - not the last: nothing paused, nothing removed;
  - blocked (a pending `note` order; a stack driver recorded): the end recorded, not paused,
    nothing removed, the `not paused:` line, the command's usual exit code;
  - a worktree with an uncommitted change: kept with its branch, the `cleanup: ... not removed`
    line, the batch paused;
  - Windows only (skipped elsewhere; runs in the `just check (windows-latest)` CI job and on the
    user's machine): a merged CR's worktree with a file held open by the test: the batch paused,
    exit as usual, the `not removed:` line with git's message, the branch kept;
  - a release CR's `order merged`, and `order drop` of a live CR: no pause.
  - `status` on a running batch whose CRs are all merged or cancelled (a blocking `note`): the
    `not paused:` line.
  - `close` (without `--yes`) on a paused batch with one merged CR's worktree kept (an
    uncommitted change), one merged CR whose folder is gone but branch kept, one merged CR fully
    removed and one cancelled CR: its line names the first two as `(merged)` with only what still
    exists, the cancelled one as `(dropped)`, and not the removed one.
  - `just test` stays within its time limit.
- **Scenario** (`scenario/run_scenario.py`):
  - `Foreman.turn` (lines 625-629): the Foreman no longer calls `remove_merged` and `pause` when
    the CLI already paused; it keeps them for a batch the CLI did not pause.
  - The block at lines 1126-1175: `order merged CR-105` (the Chief of Staff's form, the last
    CR) is checked to print the pause, and the checks "the last merge makes the Foreman pause the
    batch" and "the Foreman removed the merged worktrees and branches; the cancelled one stays"
    become "the last `order merged` pauses the batch" and "it removed the merged worktrees and
    branches; the cancelled one stays", checked right after that order, before `fm.turn()`. The
    scenario clears each merged CR's agent before (`agents set <cr> -`), as the Foreman's card
    asks when a Driver ends. The fast-forward checks after it still pass (the Foreman's
    fast-forward of the last merge runs on the paused batch).
  - The check at line 1161 on the Foreman's git (`worktree`, `branch`) stays true; the CLI's own
    git is not in `fm.git_main`.
  - A leftover: before the last `order merged`, the scenario leaves an uncommitted file in one
    merged CR's worktree; the order prints its `cleanup: ... not removed` line and still pauses;
    the Chief of Staff's `close` (the check, no `--yes`) names that CR as `(merged)` in its line of
    worktrees and branches to remove, beside the cancelled one; after `close --yes`, the scenario's
    Chief of Staff removes both on the same word (`worktree remove --force`, `branch -D`), and the
    check that they are gone holds.
  - A direct-mode step (where the scenario drives one): the steering session's
    `order merged <cr> --epoch <n>` of the last CR pauses.
- `just check` passes on Linux, macOS and Windows; `just scenario (ubuntu-latest)` green at the
  PR's head (a CLI, card and scenario change); `just mod` is not needed (no `hooks/` or `types/`
  change).

## Open questions

None. The Chief of Staff settled the last two (2026-11-17): `close` also names, in its line of worktrees and branches to remove on the user's word, every merged CR whose worktree folder or branch still exists, read from the record, so a session that lost the pause's output still shows them. The pending-orders answer is `auto-pause-Q2b` in `02-answers.md` (`auto-pause-Q2` stays the grill's close answer).
