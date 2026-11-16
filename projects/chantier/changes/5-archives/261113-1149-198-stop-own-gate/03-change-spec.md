# A Driver stops its own long gate by a named means, never with `cancel`

## Goal

In batch-11 (2026-11-11) CR-183's Driver had a long gate running when a rebase note arrived. Once
the head is about to move, that run's result cannot count, so the Driver wanted to stop it. Its
card gave it no way to do that, so it ran `chantier cancel CR-183`. That stopped the gate, but it
also cancelled the CR and moved it to `6-trash/` with all its work.

This change gives every Driver a named CLI means to stop its own running long gate:
`gate <cr> --stop`. The means stops the suite, frees the gate for the next CR, records the run as
`stopped` (not a pass and not a failure) and changes nothing else. `driver.md` says when a Driver
uses it, and says that `cancel` is never a Driver's command. The CLI refuses `cancel` without
`--epoch`, so an agent that never read that sentence still cannot cancel a CR by mistake.

This adds to the CLI because of a measured incident: a whole CR was lost. It stays inside the
CLI's scope (the batch's frame: the long gate and its lock) and adds no command, only a way of
`gate`. It reuses the stop that `cancel` already has.

## Facts in the code today (read-only, at `main` 8c003ae)

- `skills/chantier/scripts/cli/src/chantier/commands.py`, `gate()`: each command of the gate runs
  in its own process group (`CREATE_NEW_PROCESS_GROUP` on Windows, `start_new_session` on POSIX),
  under `_LongGateLock`. After each `Popen`, the lock file `<planning folder>/.long-gate.lock` reads
  ` <cr> pid <gate pid> pg<group pid>` (`lock.holding(...)`). Before the first `Popen` it reads
  ` <cr> pid <gate pid>`. `_LongGateLock.__exit__` empties it. Each command is recorded as a
  `gate` event (`result` = `pass` | `fail` | `moved`, `head` = the start SHA, `command`, and
  `run` = `<stamp>-<pid>`, which all the events of one invocation share). The log's last line is
  `result: …`.
- Ending the `gate` command process alone leaves the suite running in its group. The next
  `_LongGateLock.__enter__` then waits for that group (`procs.alive`), for up to
  `LONG_GATE_WAIT_S` (one hour).
- `_lock_holder(repo)` reads the holder text. Today the only code that stops a running suite is
  in `cancel()`: `re.fullmatch(rf"{cr} pid \d+ pg(\d+)", holder)` then `procs.stop_group(pg)`.
- `gate_passed(events, head)`: a head has a pass when the last `gate` invocation (`run`) at that
  head has every event `pass`.
- `cancel()` calls `state.check_epoch(b, args.epoch)`, which returns at once when the epoch is
  `None`. So a bare `chantier cancel <cr>` is accepted from any caller. In `cli.py`, `cancel` is
  declared with `epoch=True`, so `--epoch` is optional. Other steering commands (`take`, `pause`,
  `order done`, `agents set`, …) also accept a missing epoch today; they stay as they are here (see
  Out of scope).
- `status.py` shows each `gate` event's `result` word in the CR's STATUS ("Long gate" rows).
  `status --refresh` shows `gate running` when the lock names the CR.

## What changes

### 1. CLI: `gate <cr> --stop` (`cli.py`, `commands.py`)

- `cli.py`: `gate` gets a `--stop` flag. Its help says: "stop this CR's running long gate: its
  suite, the gate lock; recorded `stopped`, no pass; nothing else changes". `command` becomes
  optional at the parser (`nargs="*"`). `gate()` then requires at least one command without
  `--stop` (the existing usage error, exit 1) and refuses any command with `--stop` (exit 1,
  `gate <cr> --stop takes no command`). The `gate` line's help names `--stop`.
- `gate <cr> --stop` reads the lock's holder:
  - **The lock names this CR** (` <cr> pid <n>`, with or without ` pg<m>`): it stops that run's
    suite with `procs.stop_group(<m>)`, the same stop `cancel` uses, on POSIX and on Windows. No
    later command of that run starts. It prints one line, `stopped the long gate of <cr> at <sha7>
    (pg<m>)`, and exits 0. It does not touch the CR's status, its notes, its agent, its worktree,
    its folder, its PR or its round count.
  - **The lock names another CR:** it stops nothing. Exit 2 with
    `the long gate running is <other cr>'s: not stopped`. This also covers the caller's own gate
    while it still waits for the lock behind another CR. That gate has started no suite, and the
    card tells the Driver how to end it (section 3).
  - **The lock is empty or missing (no gate running):** it stops nothing. Exit 0 with
    `no long gate running for <cr>: nothing to stop`.
- **Whose gate.** The CLI knows no role and does not check who calls: a call whose argument names
  another CR acts on that CR's gate. A Driver keeps to its own CR because of the card's rule
  (section 3), not because of a CLI check. There is no check on the calling worktree or any other
  guess at the caller.
- **The record of a stopped run.** Each stopped run gets exactly one record, whether the
  stopped `gate` invocation is still alive (the normal case) or already gone:
  - one `gate` event with `result="stopped"`, the run's start `head` (full SHA), the `command`
    that was running and the run's `run` id;
  - the run's log ends with `result: stopped at <full sha>: no pass`.
  - When its command ends because of a stop, the stopped `gate` invocation does not record `fail`
    for that command. It prints `STOPPED <command> at <sha7>: no pass` and the log path, and
    exits 4. Its output must never read as a failure of the code.
  - How the running invocation learns of the stop is the implementer's choice. Examples: a field
    the stopper writes for the run, or the run id and head kept in the lock's holder text. It must
    work on POSIX and on Windows, with the lock file's byte 0 locked, and stay in the planning
    folder. A new state file is listed in the planning folder's `.gitignore` (`state.py`,
    `IGNORED`), like `.long-gate.lock`.
- **A stopped run and the pass.** The rule of `gate_passed()` does not change: the last gate run
  at a head decides. A `stopped` event is not `pass`, so a stopped run is no pass at its head. It
  also voids an earlier pass at that same head: once a gate has been stopped, the head has to be
  proved again. `stopped` is a new `result` value next to `pass`, `fail` and `moved`. `status.py`
  already shows it as written.
- The `gate()` docstring and the module comment above it name the stop.

### 2. CLI: `cancel` refused without `--epoch` (`commands.py`)

- `cancel()` refuses a call with no `--epoch` before it touches anything, with exit 2 and this
  line: `cancel <cr> --epoch <n>: the steering session's command for a CR the user dropped; a
  Driver stops its own long gate with \`gate <cr> --stop\``.
- With an epoch, `cancel` is unchanged (the stale-epoch check, the stop of the gate's group and
  the worktree's processes, the move to the trash).
- `state.check_epoch` is unchanged. This CR changes `cancel` only; the other steering commands
  keep their current behaviour.

### 3. Card: `skills/chantier/references/driver.md`, "Your means"

These go in the common "Your means", so every Driver (CR, stack, QA, release) has them.

- In the long gate bullet, add one sentence on the stop. A Driver stops only its own CR's running
  long gate, and only with `$CHANTIER gate <cr> --stop`, never another CR's. It does so only when
  the run's result can no longer count (the head is about to move: a `rebase:` note, or a change
  that needs a round) or on the steering session's `stop`. It never stops a gate because the gate
  is slow, because a run that would still be a valid pass is worth more finished than restarted. A
  stopped run is recorded `stopped`. It is not a failure, so it is not a round. It is no pass, and
  it voids an earlier pass at that head: run the long gate again at the head you push.
- A gate of yours still waiting for the lock (its log says `waiting for the long gate of …`) has
  started no suite, and `--stop` refuses it because the lock names another CR. End it by ending
  the `gate` command you started, by its id.
- One sentence, in that bullet or next to it: "`cancel` is the steering session's command for a
  CR the user dropped, never a Driver's, whatever the reason."
- The rebase bullet's "stop only one you started, by its id" stays, and it gets a pointer: a
  running long gate is stopped with `gate <cr> --stop`, never by ending the `gate` command, which
  leaves its suite running.
- "CR driver" section, the `note rebase: …` received while working: with a long gate of the CR
  running, stop it (`gate <cr> --stop`), rebase, then run the long gate at the new head.
- The last bullet of "Your means", the `stop` line: before `handback blocked stopped`, stop a long
  gate of yours that is running (`gate <cr> --stop`).
- Only `driver.md` changes. The Verifier's part of `worker.md` does not: the Verifier runs a gate
  only when a claim needs it, and lets it end. The agent files of both hosts (`agents/`,
  `com.github.copilot/agents/`) do not change either, because the contract lives in the card.

### 4. Card: `skills/chantier/references/concepts.md`

- In the `$CHANTIER` paragraph, where the long gate is described: one sentence. `gate <cr> --stop`
  stops that CR's running long gate (its suite and the lock), records the run `stopped` (no pass,
  and the last run at a head decides) and changes nothing else. It refuses when the lock names
  another CR (exit 2) and says so when no gate runs (exit 0).
- The same paragraph's exit 2 list adds `cancel` without `--epoch`.

### 5. Docs

- `CONTRIBUTING.md`, the CLI's scope sentence ("`gate` and its lock"): `gate` and its lock, and
  its stop.
- `scenario/README.md`, the line on the long gate: add the stop of a running gate and the refused
  bare `cancel`.
- `evals/SCORECARD.md`, row C9: say that `cancel` without `--epoch` is refused (exit 2).

## Out of scope

- Any change to what `cancel` does for the steering session, with its epoch.
- Recovering CR-183 or any CR cancelled by mistake (`restore` exists). Making a mistaken cancel
  cheaper to undo.
- Stopping CI, a worker, or any process other than the long gate.
- A timeout on a gate that hangs.
- A role check or a caller check in the CLI (the CLI knows no role; the card's rule holds).
- The agent files of both hosts, and the Verifier's card.
- Making `--epoch` mandatory on the other steering commands (`take`, `pause`, `order done`,
  `agents set`, …). The Chief of Staff files that as its own inbox item.

## Evidence

- `just check` passes on Linux, macOS and Windows.
- `just scenario` passes. It gets a new step, modelled on `cancel_during_gate`
  (`scenario/run_scenario.py`, "## 18. A cancel during a gate"), with a slow gate (`time.sleep(60)`
  script) started in the background for a CR, and `lock_names(w, f"{cr} pid")` and
  `lock_names(w, " pg")` awaited. It checks:
  1. `gate <cr> --stop` exits 0 and names the group. The background gate ends within the timeout,
     with no traceback; its output starts `STOPPED` and it exits 4. The slow suite's process is
     gone.
  2. The CR is still `working` in its `4-batch/2-actives/` folder, with its worktree, and has no
     new note. Its last `gate` event has `result == "stopped"` and the run's start head. The log's
     last line starts `result: stopped`.
  3. The lock is free. A second `gate <cr> "<fast passing command>"` runs at once, with no
     `waiting for the long gate` line in its log, and passes.
  4. A stopped run voids an earlier pass. With the head passed (step 3), start the slow gate again
     at the same head and stop it. `gate_passed` at that head is now false, and `ship` says `no
     long gate passed`.
  5. `gate <cr> --stop` with no gate running exits 0 with `nothing to stop`.
  6. With another CR's slow gate holding the lock, `gate <cr> --stop` exits 2, names the other
     CR, and that gate goes on running (then stop it with its own CR's `--stop`, or let it end).
  7. `gate <cr> --stop "<cmd>"` exits 1. `gate <cr>` with no command and no `--stop` exits 1.
  8. `cancel <cr>` with no `--epoch` exits 2, its stderr names `gate <cr> --stop`, and the CR's
     status and folder are unchanged. The existing `cancel … --epoch` steps still pass.
- The scenario runs on Windows and POSIX, as today: the stop goes through `procs.stop_group` on
  both.
- A reader of `driver.md` finds, in "Your means", when to stop a gate, by which command, how to
  end a gate still waiting for the lock, and the sentence that `cancel` is never a Driver's.
