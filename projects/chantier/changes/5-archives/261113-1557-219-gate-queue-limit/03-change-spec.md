# Change Specification: the long gates queue first-come, and a refusal names what is live

## Goal

With several Drivers and one long gate at a time, a gate that waits its turn in a real queue is
never refused for the length of the queue. Gates run in the order they arrived. The only refusal
left is for one gate that holds the lock (or whose suite runs on) for over an hour, and it names
that gate, the one alive at that moment, not the one seen when the wait began.

What happened (batch-15 retro, `5-archives/261113-1149-213-stack-merges-in-one-go/retro.md`; the
STATUS of CR-196 and CR-205 in `5-archives/`): four Drivers, one long gate at a time. CR-196 and
CR-205 waited more than an hour behind gates that took the lock in turn (CR-203, CR-204...), and
were refused with "the long gate of CR-197 / CR-203 has run for over an hour: check it". That
holder was the one seen when the wait began, long finished; the lock was live and held by
another CR. Both Drivers read it as a stale lock or an infrastructure fault, and lost about an
hour each (CR-205 waited about 2 h in all).

## Decision taken here (no user-visible choice left)

The request offers two fixes: size the limit on the slots, or queue first-come with no limit.
This specification takes **first-come with no limit on the queue**, and keeps the existing
one-hour limit on a **single** holder. Why:

- A limit sized on the slots (slots x one hour) still refuses a long but healthy queue (four
  slots, one Driver re-gating twice), and still measures the wrong thing: the total wait, not a
  stuck gate. First-come with a per-holder hour never refuses a healthy queue and still catches
  a hung gate, which is what the hour was for.
- The hour itself is unchanged (`LONG_GATE_WAIT_S = 3600`): today's message already claims "the
  long gate of X has run for over an hour"; this change makes that claim true. No new number, no
  new setting.
- First-come replaces today's free-for-all (each waiter polls the lock every second, whoever
  polls first wins), which can starve one waiter; the user sees only that gates run in arrival
  order.

## What changes

### 1. CLI: the long gate's lock (`skills/chantier/scripts/cli/src/chantier/commands.py`)

`_LongGateLock.__enter__` (around line 1933) and its helpers.

**A first-come queue.** Before it tries the lock, a `gate` writes a ticket in a new folder of the
planning folder, `.long-gate.queue/`: one file per waiting gate, its name sortable by arrival
(for example `<time.time_ns() zero-padded>-<pid>`), its content `<cr> pid <pid>`. A gate tries the
OS lock (`_try_lock`, unchanged) only when its own ticket is the first of the live tickets; it
removes its ticket once it holds the lock, and in every exit path (refusal, exception, the
command ended: `try/finally`). A ticket whose pid is no longer alive (`procs.alive`) is not live:
any waiter deletes it when it reads the queue (a Driver that ended its waiting `gate` command, as
`driver.md` tells it to, leaves such a ticket). The OS lock stays the one guarantee of exclusion;
the queue only orders who tries it. Standard library only, POSIX and Windows; a ticket read while
another process writes it is retried briefly, as `_run_read` does.

**The hour is per holder.** The deadline restarts each time the holder changes. The holder is
identified by the `<cr> pid <n>` part of `_lock_holder()` (the ` pg<m>` suffix a gate adds when it
starts each command does not make a new holder). Equally, in the second wait (the lock is free but
the previous gate's suite, `pg<m>`, still runs), the hour is counted from when that wait began. The
time is counted from when this waiter first saw that holder (no change to the lock file's format,
so `_gate_stop`'s `fullmatch` on `(\S+) pid (\d+)(?: pg(\d+))?` keeps working).

**The waiting notes.** The gate's log gets one line each time what it waits for changes (a new
holder, a new count ahead), never one per second. The line keeps today's prefix, which
`driver.md` and the scenario read: `waiting for the long gate of <holder>` followed by
`; queued ahead: <cr>, <cr>` when other live tickets are ahead of this one (omitted when none),
and today's `(its command still runs)` form for the second wait.

**The refusals.** Exit 2 (precondition), as today; the ticket removed, the lock file closed (and
unlocked in the second wait, as today). They name what is live at the moment of the refusal,
read again then, never a name kept from the start of the wait:

- A holder past the hour: `the long gate of <cr> (pid <n>) has held the lock for over an hour:
  check it; this gate was queued behind it` (followed by `and <cr>, <cr>` when other live tickets
  are ahead). When the holder's text is empty at that moment, say `the long gate lock has been
  held for over an hour by a process that names no CR: check it`.
- A suite past the hour after its gate ended: `the long gate of <cr> has ended but its suite
  (pg<m>) still runs after an hour: check it`.

No refusal ever comes from the length of the queue alone. The output stays within ten lines.

**Kept as is:** one long gate at a time; the lock file and its format; `.long-gate.run`,
`.long-gate.stop` and `gate <cr> --stop` (which still refuses while the lock names another CR,
including for a gate that is only queued); the log's first line; the events.

### 2. CLI: the ignored files (`skills/chantier/scripts/cli/src/chantier/state.py`)

Add `.long-gate.queue/` to `IGNORED` (line 200), so the planning folder's `.gitignore` keeps the
tickets out of git, like the lock.

### 3. CLI help (`skills/chantier/scripts/cli/src/chantier/cli.py`, line 181)

The `gate` help says the gate runs alone in the repository, "a second one waits its turn, first
come first served".

### 4. Cards and docs

- `skills/chantier/references/driver.md`, the long gate bullet (line 55): "(a second long gate
  waits its turn, in arrival order)"; and one sentence after the `--stop` paragraph: a wait in the
  queue is never refused for its length; a refusal for the hour names the gate that holds the
  lock (or whose suite runs on) at that moment: report it to the steering session as it is, do
  not read it as a stale lock, and never stop another CR's gate. Keep the sentence about the
  waiting log line (`waiting for the long gate of …`) true.
- `skills/chantier/references/concepts.md`, the paragraph on the long gate (`$CHANTIER`): add that
  long gates run one at a time in arrival order, and that `gate` is refused (exit 2) only when one
  gate has held the lock, or its suite has run on, for over an hour.
- `docs/gates.md`, line 11: "alone in the repository, in arrival order when several wait".
- No agent file changes (no role's contract moves), so `agents/` and
  `com.github.copilot/agents/` stay untouched.

## Out of scope

- Running more than one long gate at a time, or a per-project setting for the hour.
- Changing `gate --stop`, the run file, the stop marker or the lock file's format.
- Any `status` or `board` view of the gate queue.
- The Drivers' re-gating pace (when a Driver re-runs its gate) and the parallel rebase cost: other
  CRs.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes, with the existing checks in `scenario/run_scenario.py` around lines
  2624-2649 unchanged and green ("a second long gate waits for the first", "a long gate whose
  command died still holds the next one while its suite runs"), and one new check in the same
  place: with one gate holding the lock, two more `gate` commands started in a known order (the
  second started only once the first's ticket is in `.long-gate.queue/`) take the lock in that
  order (from the gate events' order in `events.jsonl`, or the logs' times), the later one's log
  says `queued ahead:` and names the earlier one, and `.long-gate.queue/` is empty at the end.
- A waiter whose `gate` command is ended (killed by its id) leaves a ticket that the next gate
  skips: a scenario check, or the Driver's command and output in `evidence/`.
- The refusal wording cannot be reached in the scenario without an hour's wait and the CLI gets
  no test-only setting for it: the Driver proves it with a local run against a copy with
  `LONG_GATE_WAIT_S` lowered (not committed), its command and output kept in the CR's
  `evidence/`, showing the refusal names the live holder after the holder changed during the
  wait; the Inspector checks the text on the diff.
- `.gitignore` in a fresh planning folder lists `.long-gate.queue/`.

## Open questions

None.
