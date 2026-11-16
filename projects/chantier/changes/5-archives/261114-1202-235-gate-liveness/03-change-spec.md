# Change Specification: the gate lock and the activity line tell the truth

## Goal

This CR comes from batch-16's retro, points 3 and 4 (`.agents/changes/5-archives/261113-1726-215-stack-after-ready/retro.md`),
reviewed by an advisor (`intake/request.md`). The user accepted the proposal as filed: "ok pour tout. fait ca
maintenant" (`02-answers.md`).

- **Point 3.** CR-217's long-gate lock outlived its merged CR, with a dead pid. CR-216 then waited
  about 40 minutes and was refused. A merged CR must not leave a suite running that blocks the
  next gate. A pid that the lock or a queue ticket records must count as alive only while it is
  still the same process, including after Windows reuses the pid.
- **Point 4.** CR-220 showed 48 minutes with no activity. Its gate was queued, not running, and
  the ping got a pong. The activity line must show a queued gate, and the Foreman's lost-Driver
  check must skip it as it skips `gate running`.

## Decisions carried from `02-answers.md`

| Decision | Where this spec carries it |
| --- | --- |
| 1. The proposal as filed is the scope. Points the request does not settle take this spec's defaults and are listed as open points. | "What changes", A to D; "Open points" |
| 2. The CR joins the running batch-17. | "Order in batch-17" |

## Order in batch-17: after CR-221 (`python-inline-deps`)

This CR waits for CR-221. The reason is a real need, not a shared file. The pid identity check
(B below) needs each process's creation time on Linux, macOS and Windows. CR-221 rewrites
`procs.py` on `psutil` ("Libraries", `psutil`), and psutil gives that time as
`Process(pid).create_time()`. Before CR-221, the only way would be hand-written per-system code:
`GetProcessTimes` through `ctypes`, `/proc/<pid>/stat` with the boot time, and `ps -o lstart`.
That is the kind of code CR-221 removes, and CR-221's Driver, mid-rewrite of `procs.py` (round 2
of 3), would have to port it a second time.

**For the Chief of Staff:** record `{"after": ["python-inline-deps"]}` in this CR's
`depends.json`. This spec writes nothing outside `03-change-spec.md`.

The places named below are first given as today's names in
`skills/chantier/scripts/cli/src/chantier/`, then as the module CR-221's layout puts them in. The
Driver works on the code as CR-221 merged it, and keeps CR-221's targets: file and function sizes,
ruff, `mypy --strict`, and no import cycle.

| Today | After CR-221 |
| --- | --- |
| `commands._apply_order`, kind `merged` (around line 1202) | `commands/orders.py`, the `merged` handler |
| `rails.merge_done`, `rails.release_merged` (lines 265 to 281) | `rails.py` (unchanged in role) |
| `commands._lock_holder`, `_LongGateLock` (2081 to 2213) | `commands/gate_lock.py` |
| `commands._gate_stop`, `_run_read`, `_run_write` (2221 to 2284) | `commands/gate.py` |
| `commands.cancel` (2545 to 2570) | `commands/delivery.py` |
| `commands._activity` (1382 to 1450) | `commands/batch_status.py` |
| `procs.alive`, `procs.stop_group` | `procs.py` (psutil) |
| `cli._parser`, help of `status --refresh` (line 125) | the `register(sub)` of `commands/batch_status.py` |

## What changes

### A. `order merged` stops the CR's own long gate

Today `cancel` stops the suite group that the lock names for the CR (`commands.py` line 2560).
`order merged` does nothing of the kind: `_apply_order` calls `merge_done`, which moves the
folder and sets the status. If the lock still names the merged CR with a suite `pg<m>`, the next
gate waits up to an hour for that suite (`_LongGateLock._acquire`, lines 2188 to 2198), whatever
the CR's status.

The change: `order merged <cr>` (from the Chief of Staff, or the Foreman with `--epoch`) stops
that CR's long gate when the lock names it. It does so in the same way as `gate <cr> --stop`
(`_gate_stop`), so the record says `stopped`: no pass, no failure.

- **When the lock names `<cr>`** (`<cr> pid <n>[ pg<m>]`):
  - If the gate command `<n>` is alive (identity check, B), the `.long-gate.stop` marker is
    created, and that gate records its own `stopped` run and exits 4, as today after `--stop`.
  - The suite group `pg<m>` is stopped if it is alive (identity check, B).
  - If the gate command is dead and `.long-gate.run` exists, the stopper does the recording. It
    appends `result: stopped at <head>: no pass` to the run's log if the log still exists. It
    logs the `gate` event `result="stopped"` with the run's head, command and run id. It removes
    `.long-gate.run`. This happens in the same batch record write as the order (no second
    `Batch` opened inside the first).
- **When the lock names another CR, or no CR:** nothing is stopped and nothing more is printed.
- **Output:** one more line after `merged <cr>: moved to 3-done` (or after the release's
  `merged <cr>: the procedure goes on with a new Release driver`):
  `stopped the long gate of <cr> (pg<m>)`. When only the gate command was alive and there was no
  suite, the line is `stopped the long gate of <cr>`. When nothing was stopped, no line is added.
  The ten-line cap still applies.
- **Both kinds of CR:** a CR, and a release CR whose release PR merged (`release_merged`). A
  merged PR makes a running gate of its head pointless in both cases.
- **The refusals of `order merged` do not change.** The stop runs only after they pass:
  `already merged`, `cannot mark cancelled … merged`, and the release-merges-last rule.
- **Where the code goes:** in the command layer (`_apply_order` / `commands/orders.py`), as
  `cancel` does. `rails.py` stays what the CLI refuses, with no process handling. The stop is one
  function shared by `_gate_stop` and the `merged` handler, not a copy.

### B. A recorded pid counts as alive only while it is the same process

`procs.alive(pid)` asks only whether some process has that pid. Windows reuses pids soon after a
process ends, so a dead gate's `pg<m>` can name an unrelated live process. The next gate then
waits an hour for it. Worse, `cancel` and `gate --stop` run `taskkill /F /T` on it and end an
unrelated process tree. POSIX reuses pids too, less often. The rule is the same on every system:

**A pid recorded in a file counts as alive only if a process with that pid runs and its creation
time is no later than that file's last write, plus a one-second margin for clock rounding.**

- **The lock's `pid <n>` and `pg<m>`:** checked against `.long-gate.lock`'s modification time.
  The holder text is written by `holding()` only after the process it names exists: the `gate`
  command writes its own pid, and the suite's `Popen` returns before `holding(... pg<p.pid>)`. A
  process that reuses the pid is created after the original ended, which is after that write.
- **A queue ticket's `pid <n>`** (`.long-gate.queue/<ns>-<pid>`, written by the waiting gate
  itself): checked against the ticket's modification time.
- **Where it applies:** every liveness test of a recorded pid.
  - `_LongGateLock._ticket_cr`: a ticket whose pid fails the check is deleted, as a dead one is
    today.
  - `_acquire`'s wait for a dead gate's suite (lines 2188 to 2198). A pg that fails the check is
    not waited for: no `(its command still runs)` note, no hour.
  - `_gate_stop`'s `gate_alive`.
  - The stop of A.
  - `cancel`: the lock's `pg<m>` is stopped only if it passes the check. A pg that fails it is
    not signalled and not listed in `stopped …`.
  - `_activity` (C).
- **No new file and no new field.** The lock's text format (`<cr> pid <n>[ pg<m>]`), the ticket
  format and `.long-gate.run` stay as they are. Two things read the lock today and must keep
  working: the scenario's `lock_names` helper, and the parsers of `cancel` and `_gate_stop`.
- **A creation time that cannot be read** (psutil `AccessDenied` on a process of another user):
  for waiting, the process counts as alive, which is today's behaviour. For stopping, it is not
  stopped. See open point 3.
- **The API:** `procs` gets one function that takes the pid and the time it was recorded, and
  answers whether it is the same process (for example `procs.alive_since(pid, recorded)`). It is
  built on psutil's `create_time()`. `procs.alive(pid)` stays for the callers that hold their
  own child (none needs the check). `procs.stop_group` is only ever called after the check.

### C. `activity` shows a queued gate

`_activity` prints `activity <label> gate running` only for the CR the lock names (lines 1423 to
1429). It ignores `.long-gate.queue/`, where CR-219's tickets show a gate waiting for its turn.

The change, for each target whose key is a CR id:

1. **`gate running`:** the lock's holder text names the CR, and its `pid <n>` or its `pg<m>`
   passes the check of B. A holder text whose processes are all dead is not a running gate: it
   is a stale lock. See open point 4.
2. **Otherwise, `gate queued behind <other>`:** a ticket in `.long-gate.queue/` names the CR,
   and its pid passes B. `<other>` is chosen in this order:
   - the CR the lock names, when that holder passes 1's liveness test;
   - otherwise, the CR of the first live ticket ahead of this CR's earliest live ticket, in name
     order (the queue's arrival order);
   - otherwise, nothing: the line is `activity <label> gate queued` (the gate is next and is
     about to take the lock).
3. **Otherwise:** the age, `not measured` or `session-level` line, as today.

`_activity` only reads. It never deletes a ticket, unlike `_ticket_cr`, because `status` must
not change the queue. A ticket being written is read as `_ticket_cr` reads it: retried, and
skipped if still unreadable. The stack driver and QA orders run no gate of their own, and their
lines do not change.

The text `gate queued behind <cr>` is the request's. The `<cr>` is spelled as the record spells
it (`CR-219`).

Help and docstring:

- `status --refresh`'s help (`cli.py` line 127) becomes "(age of its last event or session
  record, `gate running`, `gate queued behind <cr>`, `not measured`)".
- `_activity`'s docstring names both lines and the identity check.

### D. The Foreman card skips a queued gate

`skills/chantier/references/foreman.md`:

- **Line 279**, the lost-Driver "Suspect" rule: "shows no activity and no `gate running`" becomes
  "shows no activity, no `gate running` and no `gate queued`". The match is the prefix, so the
  `behind <cr>` form and the bare form are both skipped.
- **Line 97**, "Your means": the list of what an `activity` line gives adds `gate queued behind
  <cr>` after `gate running`.

No agent file changes (`agents/`, `com.github.copilot/agents/`). The card is shared by both
hosts. In a direct batch the Chief of Staff reads the same card, so nothing else changes.

## Out of scope

- A waiting gate that checks the CR status of the lock's last holder and stops waiting when that
  CR is merged or cancelled. A and B remove the cause at the source. See open point 1.
- Ending the waiting `gate` commands (queue tickets) of a CR that `order merged` records. See
  open point 2.
- Stopping the processes in a merged CR's worktree, as `cancel` does with `procs.find`. The
  merged CR's worktree is the Driver's to clean, and its Driver may still be finishing (retro
  point 16).
- `cancel` keeps its route: it stops the pg, and the gate records FAIL. Only the identity check
  is added to it.
- The one-hour limit `LONG_GATE_WAIT_S`, the queue's design and the lock's format.
- The CR board pane: `STATUS.json` and `hooks/register.tsx` do not show activity lines, so
  `AGENTS.md`'s screenshot rule is not triggered. No `hooks/` or `types/` change, so no `just mod`.
- The other retro points of batch-16.

## Evidence

The Verifier keeps each item in `work/verifier/evidence/`, and the PR body quotes them. The CLI
and a card change, so `just check` and `just scenario` (both forges) apply (`AGENTS.md`).

New or changed scenario steps go in `scenario/run_scenario.py`, beside the gate-queue steps
(around line 2676) and the 12c activity steps (`driver_liveness`, around line 2757). Each one
works on Linux, macOS and Windows.

- **E1. `order merged` stops the CR's gate.**
  1. Start `gate <cr> "<slow suite>"` in the background. Use a suite that writes its pid to a
     file and sleeps 60 s, as in 18b's `slow_stop.py`. Wait for `lock_names(w, " pg")`.
  2. Run `order merged <cr> --epoch 1`.
  3. Check:
     - the output holds `stopped the long gate of <cr> (pg`;
     - the suite's pid is gone;
     - the gate command exits 4 with `STOPPED`;
     - the last `gate` event of the CR has `result: "stopped"`;
     - the CR is in `3-done`;
     - a gate of another CR started after it runs at once: its log holds no `waiting for the
       long gate`, and no `its command still runs`.
- **E2. `order merged` with no gate of its own stops nothing.**
  1. The lock names another CR, with a live suite.
  2. Run `order merged <cr>`.
  3. Check: the output has no `stopped` line, and the other CR's suite still runs.
- **E3. A reused pid is not the gate's suite.**
  1. Write `.long-gate.lock` with `\0<cr> pid <dead pid> pg<P>`. `<P>` is the pid of a sleeping
     process the scenario starts after the write. Then set the lock's mtime 10 s back
     (`os.utime`), which stands for Windows reusing the pid.
  2. Check:
     - a gate of another CR passes at once: its log has no `(its command still runs)`;
     - `cancel <cr>` lists no `pg<P>` in `stopped …`, and `<P>` is still alive afterwards;
     - the same holds for `order merged`.
  3. A dead pid is a short process the scenario started and waited for.
- **E4. A ticket with a reused pid is skipped.** A ticket whose content names a pid created after
  the ticket's mtime is deleted by the next gate, as a dead one is. This is the step "a waiter
  killed in the queue leaves a ticket that the next gate skips", with the ticket's mtime set
  back.
- **E5. Activity lines** (12c).
  - The existing step writes `{three} pid 1 pg1`. Pid 1 does not exist on Windows, so it now
    writes the scenario's own pid, with a fresh mtime, and still expects
    `activity {three} gate running`.
  - Added: a ticket `.long-gate.queue/<ns>-<pid>` with content `{two} pid <scenario pid>` gives
    `activity {two} gate queued behind {three}`, and the ticket is still there after `status`.
  - With the lock empty and that ticket alone, the line is `activity {two} gate queued`.
  - With the lock naming `{three}` and a dead pid and no pg, `{three}`'s line is an age, not
    `gate running`.
  - A ticket with a dead pid gives no `gate queued` line.
- **E6. The card.** `git diff` of `foreman.md` shows lines 97 and 279 only. The scenario's card
  checks pass.
- **E7.** `just check` passes on Windows locally, then in CI on Linux, macOS and Windows,
  including CR-221's `lint` (ruff, `mypy --strict`, sizes). `just scenario` passes on both forges
  on the Windows dev machine, because `procs.py` differs per system and CI runs the scenario on
  Linux only, and in CI.

## Open points (defaults taken, for the Chief of Staff to confirm with the user)

1. **A waiting gate that ignores a merged holder.** Retro point 3 says "the gate lock is released
   when its pid is dead or its CR merged". The request's fix is that `merged` stops the suite.
   **Default:** A (the merge stops the suite) and B (a dead or reused pid is not waited for). The
   waiting gate does not read the batch record to check the holder CR's status. The alternative
   adds that check to `_acquire`, which would cover a suite that `order merged` could not stop.
2. **Queued gates of a merged CR.** **Default:** `order merged` leaves that CR's queue tickets
   alone. Its waiting gate later runs a pass on a merged head, and its Driver hears of the merge
   from the Foreman. The alternative ends those waiting `gate` commands too.
3. **A creation time that cannot be read.** **Default:** counted alive for waiting (today's
   behaviour, safe for the suite), never stopped (safe for the other process). The alternative
   treats it as dead.
4. **`gate running` requires a live holder.** The request asks only for `gate queued`. The title
   is "tell the truth", and a stale holder text would otherwise show `gate running` for ever and
   hide a lost Driver from the D rule. **Default:** included (C.1). The alternative keeps today's
   text-only test.
5. **The stop route of `order merged`.** **Default:** that of `gate --stop` (marker, recorded
   `stopped`), not `cancel`'s (kill the pg, the gate records FAIL). This keeps a merged CR's
   record free of a false failure. The alternative is the literal "does the same as `cancel`".
6. **Both kinds of CR.** **Default:** the stop applies to a release CR's `order merged` too.
7. **Order in the batch.** **Default:** after CR-221, for psutil's creation time (see "Order in
   batch-17"). The alternative runs now on today's code, with hand-written `ctypes` and `/proc`
   code for the creation time, which CR-221 then rewrites.
