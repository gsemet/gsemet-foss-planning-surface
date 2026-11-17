# Change Specification: the batch pauses when its last CR merges, and the close is offered

## Goal

When the last CR of a batch is recorded merged, the batch is paused at once, its merged CRs'
worktrees and branches are cleaned, and the user is asked, unprompted, whether to close the batch.
Today (batch-22, direct mode) the steering session skipped the pause after the last merge, never
offered the close, and the user's "close" was refused "running, not paused". In the user's words:
"as it is finished it must have been paused automatically, and you should have cleaned what had to
be cleaned and asked me whether I want to close the batch."

## Decisions carried from `02-answers.md`

- **auto-pause-Q1:** the CLI pauses, at once. The `order merged` that records a batch's last CR
  runs the pause itself, and removes the merged CRs' worktrees and branches with it. The steering
  session (the Foreman, or the Chief of Staff in direct mode) then only writes the retro and
  offers the close.
- **auto-pause-Q2:** the close is offered, on the user's yes. The steering session shows the bilan
  (`close` without `--yes`) and asks at once, unprompted; `close --yes` runs only on the user's
  yes, as today.
- Spec critic: yes (the CLI's lifecycle and the steering session's contract change).

## What changes

### 1. CLI: `order merged` pauses the batch at its last CR

Files: `skills/chantier/scripts/cli/src/chantier/commands/orders.py` (`order`),
`commands/orders_apply.py` (`_merged`), `rails_release.py` (`merge_done`),
`commands/closing.py` (`pause`), `core/git.py` (`git`).

- **When.** After `order merged <cr>` has recorded an ordinary CR merged (`merge_done`), in both
  forms: the Chief of Staff's (no `--epoch`) and the steering session's own (`--epoch <n>`), and
  `all_merged(b.record)` (`rails.py`) is now true (every CR merged or cancelled). A release CR's
  `order merged` (`release_merged`, the CR goes back to `queued`) never triggers it. An
  `order merged` on a CR already merged (`already merged`) does not trigger it either.
- **What it checks.** The same conditions as `pause` (`closing.py`): no CR live, queued, ready or
  blocked, no stack driver recorded, and no pending order, with one difference: pending orders the
  CLI applied in full (`applied: true` in the record: `merged`, `rounds`, `slots`, `budget`, ...,
  including the `order merged` being recorded now) do not block it; they are marked done by the
  pause (see open question 1). A pending order the CLI did not apply in full (`note`, `qa`, the
  drop of a live CR) blocks it.
- **Order of its steps,** once the merge is recorded and the locks of the order released:
  1. **The cleanup.** For each CR of the batch recorded `merged`: `git worktree remove <worktree>`
     when the folder exists, then `git branch -D <branch>` when the branch exists, through
     `core/git.py`'s `git`, in the main checkout (the repository root), or with a planning surface
     in the project's clone (`Repo.clone`, as `git -C <clone>`). No `--force` on `worktree
     remove` (a worktree with changes is refused by git and kept). A cancelled CR's worktree and
     branch are never touched: they stay for the user's word at `close`, as today. A removal git
     refuses prints one line, `cleanup: <cr> <worktree or branch> not removed: <git's message>`,
     and does not stop the pause (see open question 2).
  2. **The pause.** The body of `pause` runs, factored out of `closing.py`'s `pause` so both
     share it: the cost to date computed and recorded (`cost_rows`, `record_costs`,
     `cost_summary`, "Spent: unknown (...)" when it cannot be read, never a false $0.00), the
     record set `status: paused`, `paused`, `summary`, `heartbeat_stopped`, and a `pause` event
     logged. The event carries the order's id, so the log tells an automatic pause from a
     `pause --epoch <n>`. This shared body is the only place a pause is recorded: whatever a later
     change adds at the pause (the pending `1-inbox/batch-takeover`'s publish-at-pause, for one)
     goes in it, and so covers both kinds of pause, the automatic one and `pause --epoch <n>`.
- **What it prints.** The order's usual lines, then, in place of today's `every CR is merged or
  cancelled: \`chantier pause --epoch <n>\``:
  - one line per CR cleaned: `cleanup: <cr> worktree <path> and branch <branch> removed` (or the
    refusal line above);
  - `paused <batch>: every CR is merged or cancelled; cost to date below`, the `report:
    <STATUS.md path>` line and the cost summary, as `pause` prints them;
  - `next: the retro, then offer the close (\`chantier close\`, then \`close --yes\` on the
    user's yes)`.
- **When the pause cannot run** (a blocking order, a stack driver recorded): the merge stays
  recorded, nothing is cleaned, and the order prints `every CR is merged or cancelled, not paused:
  <the causes, as pause names them>; \`chantier pause --epoch <n>\` once they are done`. The order
  itself succeeds (exit 0).
- **`pause --epoch <n>` stays** as it is, for a batch whose last CR ended another way (a release
  CR's `handback released`, a `cancel`, an `order drop`, see open question 3), or whose automatic
  pause was blocked. It does no cleanup (the steering session's git, as today).
- **The project's rules.** This gives the CLI two git writes it does not have today (`git worktree
  remove`, `git branch -D`), which `AGENTS.md` forbids as written ("The agents do the work, git and
  the forge included"; "chantier writes only in the planning folder ..."; "The board's server is
  also the CLI's one git exception ... The rest of the CLI keeps no git write."). The PR amends
  `AGENTS.md`, in the same words as the other named exceptions:
  - the CLI's scope bullet and the "chantier writes only in ..." list name it: the last
    `order merged` of a batch removes the batch's merged CRs' worktrees and branches, from the main
    checkout or the project's clone, and nothing else;
  - the board bullet's "the CLI's one git exception ... The rest of the CLI keeps no git write" is
    rewritten as two named exceptions: the board's server (it may serve without joining the
    planning surface's autosync group) and the last `order merged`'s cleanup (above); the rest of
    the CLI keeps no git write.
  See open question 4: the user confirms the amendment before the PR.

### 2. CLI: `status` flags a complete batch that is not paused

Files: `commands/batch_status.py`, `status/views.py` (the text `status` prints, the heartbeat's
`status --refresh --epoch <n>` included). From the request (`intake/request.md`), see open
question 5.

- While the batch is `running` and `all_merged` is true, `status` prints one line:
  `every CR is merged or cancelled, not paused: <what blocks: the pending orders, the stack
  driver, or "nothing">; \`chantier pause --epoch <n>\``.
- Not in `STATUS.json`'s fields the CR board pane reads (`hooks/register.tsx`), so no pane
  change and no screenshot rule.

### 3. Cards

Both hosts read the same cards; no agent file changes.

- `skills/chantier/references/foreman.md`:
  - "Your goal" (lines 22-27): every CR merged or cancelled; the last `order merged` (yours or the
    Chief of Staff's) cleans the merged CRs' worktrees and branches and pauses the batch; then
    your retro (with its critic) and `[foreman→chief-of-staff] final <STATUS.md path>`. Your own
    `pause --epoch <n>` only when the CLI says the automatic pause did not run, or the last CR
    ended another way, with the cleanup before it as today.
  - "The retro is yours: before `pause`": becomes after the pause and before `final`. The retro
    critic's cost lands after the cost to date; `close` prices it in the final cost.
  - "Never code, review, ..." (lines 139-143): the merged CRs' cleanup is the CLI's at the last
    `order merged`; yours only before a `pause --epoch <n>` of your own, and for a removal the CLI
    printed as refused (see open question 2).
  - "The main checkout after a merge" (lines 440-446): "by git (the CLI runs none)" becomes: by
    git; the CLI runs no fast-forward (it removes, at the last `order merged`, only the merged
    CRs' worktrees and branches). For the last merge, the order is already marked done by the
    pause; the fast-forward still runs right after it, with its `main checkout:` note (`note` on
    a paused batch passes `--batch <batch>` where the CLI asks for it).
  - Line 439-440 ("removed by the usual cleanup before `pause`"): by the CLI at the last merge.
  - The Heartbeat bullet (lines 621-632): "right after `pause`" becomes right after the pause,
    yours or the one the last `order merged` ran (yours or the Chief of Staff's): cancel the armed
    wake then, where ending it is yours. The record alone does not stop it: the pause records
    `heartbeat_stopped`, but a later wake's `status --refresh --epoch <n>` resets it
    (`commands/batch_status.py`, lines 64-66) and the heartbeat goes on. So `pause` "records it
    itself" stays true for both pauses, and cancelling the wake stays the steering session's step.
- `skills/chantier/references/chief-of-staff.md`:
  - "Steering a batch yourself", "The pause" (lines 1462-1479): the last `order merged <cr>
    --epoch <n>` pauses the batch and cleans; then, in the same turn: cancel the armed wake (as
    the host's reference says), the fast-forward, the retro (with its critic), the Completion
    report with the Retro offered, then **the close offered at once, unprompted**: run
    `$CHANTIER close --batch <batch>` (the check, no `--yes`), show the bilan, the final cost and
    what goes, and ask "close the batch?"; `close --yes` only on the user's yes, as the Closing
    bullet says. When the CLI printed that the pause did not run, do what blocks it, then the
    cleanup and `pause --epoch <n>` as today.
  - Line 1461 ("A paused batch is not running: all of this lifts at the pause."): when the CLI
    paused the batch, the steering session's retro and its retro critic run after the pause and
    before `final` (in direct mode, before the close offer); what lifts at the pause does not
    lift them.
  - "The pause" (Foreman mode, lines 1208-1240): on the Foreman's `final`, the same close offer,
    unprompted, after the Completion report and the Retro. In Foreman mode the CoS's own `order
    merged <cr>` of the last CR prints the pause: still send its line to the Foreman (it cancels
    its armed wake, runs the fast-forward, the retro and `final`); the close is offered after
    `final`, never before (the Foreman's retro critic must have ended for `close` to pass).
  - "Closing" (line 1290): "only on the user's word" stays for `--yes`; the check without
    `--yes` is now also run unprompted at the pause, to offer it.
  - The task table, rows "the `final` message, the batch paused" and "close the batch" (lines
    28-29): the close offered at the pause.
  - The Tips "End of a batch" example "close the batch" is dropped (the close is now asked).
- `skills/chantier/references/concepts.md`, "Batch lifecycle":
  - step 2 "Complete" (lines 247-249): the last `order merged` removes each merged CR's worktree
    and branch and pauses the batch; the steering session runs `pause` itself only when that did
    not happen.
  - step 3 "Paused" (lines 250-252, "... has written the batch's retro for this pause"): when the
    CLI paused the batch, the steering session's retro and its retro critic run after the pause
    and before `final` (in direct mode, before the close offer); when the steering session ran
    `pause` itself, as today.
  - "Each CR is named a branch ..." (line 242): a merged CR's worktree is removed by the CLI at
    the last merge.
- The host references, Heartbeat sections:
  - `references/hosts/claude-code.md` (lines 63-64, "right after `pause`"): right after the pause,
    the steering session's own or the one the last `order merged` ran, it runs `ScheduleWakeup`
    `stop: true`; the record (`heartbeat_stopped`, which both pauses write) does not stop the
    wake, and a later wake's `status --refresh` resets it.
  - `references/hosts/copilot.md` (lines 56-62, "At the pause the Chief of Staff tells the user to
    delete the `/every`"): at either pause, the automatic one included, the Chief of Staff tells
    the user to delete the `/every` (in direct mode, in its own session); until it is deleted,
    each `/every` wake clears the mark, which is true.

### 4. Docs

The same story, where they tell it: `docs/tutorial-claude-code.md` (line 187),
`docs/planning-folder.md` (line 74), `docs/use-cases-foreman.md` (line 101),
`docs/use-cases-direct.md` (line 65), `docs/planning-modes.md` (line 21, the worktree removal),
`docs/batch-lifecycle-texts.md` and `docs/batch-lifecycle.svg` (and `cr-lifecycle-texts.md` /
`cr-lifecycle.svg` where they name the cleanup), redrawn by their own method.

## Out of scope

- An automatic close: `close --yes` stays the user's yes.
- An automatic pause from `handback released`, `cancel` or `order drop` (see open question 3).
- The CLI fast-forwarding the main checkout: it stays the steering session's git.
- The CLI cancelling the heartbeat's armed wake: it stays the steering session's (or, on Copilot,
  the user's) step.
- Any change to `close`, its refusals, its pricing or its archive.
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
  - the last `order merged`, both forms (`--epoch <n>` and none), pauses: `status: paused`,
    `paused` and `summary` set, `heartbeat_stopped` set, the pending applied orders marked done,
    the merged CRs' worktrees and branches gone, a cancelled CR's kept;
  - not the last: nothing paused, nothing removed;
  - blocked (a pending `note` order; a stack driver recorded): merged, not paused, nothing
    removed, the `not paused:` line, exit 0;
  - a worktree with an uncommitted change: kept, the `cleanup: ... not removed` line, the batch
    paused (or per open question 2);
  - a release CR's `order merged`: no pause.
  - `just test` stays within its time limit.
- **Scenario** (`scenario/run_scenario.py`):
  - `Foreman.turn` (lines 625-629): the Foreman no longer calls `remove_merged` and `pause` when
    the CLI already paused; it keeps them for a batch the CLI did not pause.
  - The block at lines 1126-1175: `order merged CR-105` (the Chief of Staff's form, the last
    CR) is checked to print the pause, and the checks "the last merge makes the Foreman pause the
    batch" and "the Foreman removed the merged worktrees and branches; the cancelled one stays"
    become "the last `order merged` pauses the batch" and "it removed the merged worktrees and
    branches; the cancelled one stays", checked right after that order, before `fm.turn()`. The
    fast-forward checks after it still pass (the Foreman's fast-forward of the last merge runs
    on the paused batch).
  - The check at line 1161 on the Foreman's git (`worktree`, `branch`) stays true; the CLI's own
    git is not in `fm.git_main`.
  - A direct-mode step (where the scenario drives one): the steering session's
    `order merged <cr> --epoch <n>` of the last CR pauses.
- `just check` passes on Linux, macOS and Windows; `just scenario (ubuntu-latest)` green at the
  PR's head (a CLI, card and scenario change); `just mod` is not needed (no `hooks/` or `types/`
  change).

## Open questions

1. **Pending applied orders.** In Foreman mode the Chief of Staff's `order merged` of the last CR
   is itself a pending order (the Foreman marks it `order done` after the fast-forward), so a
   pause that waits for every order would never run from it. Proposed: the automatic pause marks
   done every pending order the CLI applied in full (`applied: true`), the last `order merged`
   included, and only an order not applied in full (a note, a QA, the drop of a live CR) blocks
   it. Agreed?
2. **A removal git refuses** (a worktree with uncommitted changes, a locked worktree). Proposed:
   the worktree is kept (no `--force`), the CLI prints the `cleanup: ... not removed` line, the
   batch is paused anyway, and the steering session tells the user, who decides at `close` as for
   a dropped CR's worktree. Or should the refusal stop the pause?
3. **Other last ends.** The last CR can also end by a release Driver's `handback released`, a
   `cancel` or an `order drop` of a queued CR; the answers name `order merged` only. Should those
   pause the batch at once too, with the same cleanup? (Not in this specification until the user
   says so; until then `status` flags the batch, part 2.)
4. **`AGENTS.md`.** The automatic cleanup is a git write by the CLI, which `AGENTS.md` forbids as
   written. Does the user agree that the PR amends `AGENTS.md` to name this one exception (the
   last `order merged` removes the batch's merged CRs' worktrees and branches, nothing else)?
5. **The `status` flag** (part 2) comes from the request, not from the answers. Keep it?
