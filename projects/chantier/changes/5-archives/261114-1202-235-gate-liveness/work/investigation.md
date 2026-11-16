# CR-235 investigation (read only, worktree batch-17-CR-235, on CR-237's layout)

Base: `src` below = `skills/chantier/scripts/cli/src/chantier/`. Line counts are real file lengths
(`Measure-Object -Line` skips blank lines, so use `.Count`).

## 1. Places and signatures to change

The spec's "today" names map to the current layout. Two corrections to the spec's table:
`cancel` lives in `commands/release.py` (not `delivery.py`), and the `_apply_order` merged branch
is `commands/orders_apply.py::_merged(w: Word)`.

| Spec item | Where today | Signature / lines |
| --- | --- | --- |
| `procs.alive`, `stop_group` | `src/procs.py` (117 lines) | `alive(pid:int)->bool` l.107-117; `stop_group(pgid:int)->bool` l.64-72; `stop(pids, grace_s)` l.89-104 (also calls `alive`) |
| lock text, holder, queue, wait | `src/commands/gate_lock.py` (154) | `lock_holder(repo)->str` l.19; `LongGateLock._ticket_cr(self,p)->str\|None` l.46-61 (`procs.alive(int(m[2]))` l.55); `_acquire(self)->None` l.99-141 (dead-suite wait: l.128-140, `procs.alive(int(m[1]))` l.130 and l.133); `holding(text)` l.143 |
| `_gate_stop` | `src/commands/gate.py` (307) | `_gate_stop(args, repo, batch, wt)->tuple[list[str],int]` l.73-106; `gate_alive = procs.alive(int(m[2]))` l.85; `procs.stop_group(pg)` l.89; `_run_read`, `_run_write`, `_run_file`, `_stop_file` l.34-70 |
| `order merged` | `src/commands/orders_apply.py` (312) | `_merged(w: Word)->list[str]` l.176-190: `merge_done(b,c)` (l.183) for a CR, `release_merged(b,c)` + the line `merged <cr>: the procedure goes on with a new Release driver` (l.189-190) for a release. Called from `apply_order` -> `HANDLERS["merged"]`, inside `orders.order` (`commands/orders.py` l.155-171) which already holds `changes_lock(repo)` and an open `RenderedBatch(... actor=...)` `b`. `merge_done` itself is in `src/rails_release.py` l.18-26 (returns `[f"merged {c.id}: moved to 3-done", maybe "every CR is merged..."]`) |
| `cancel` | `src/commands/release.py` (132) | `cancel(args)->list[str]` l.82-113; lock parse `re.fullmatch(rf"{cr} pid \d+ pg(\d+)", lock_holder(repo))` l.102; `procs.stop_group(int(m[1]))` l.103 |
| `_activity` | `src/commands/batch_status.py` (369) | `_activity(repo: Repo, d: BatchRecord)->list[str]` l.83-118; holder test `holder = lock_holder(repo).split()` l.105, `if holder and holder[0] == key:` l.110; `_targets(d)` l.45 gives `(key,label)`, keys are CR ids, `"stack"`, or QA order ids (`O-k`). Called only by `_refresh` l.154. `status --refresh` help text: l.349 (`"record, \`gate running\`, \`not measured\`) and the spend (recorded); "`), not `cli.py` |
| other `lock_holder` users | `release.py` l.102 (cancel), `gate.py` l.76, `batch_status.py` l.105 | the lock text is parsed four different ways today (gate.py `(\S+) pid (\d+)(?: pg(\d+))?`, release.py `... pid \d+ pg(\d+)`, gate_lock `\bpg(\d+)\b` and `(\S+) pid (\d+)(?: pg\d+)?`, batch_status `.split()`). One shared parser fits B. |

Callers of `procs.alive` for a recorded pid (the ones B must change): `gate_lock._ticket_cr`,
`gate_lock._acquire` (x2), `gate._gate_stop`. `cancel` and `release.py` call `procs.stop_group`
with no liveness test at all (it just tries to kill; on Windows `_end_tree` kills the pid's tree, so
a reused pid ends an unrelated tree: this is the real hazard). `gate._run_commands` l.159
`procs.stop_group(p.pid)` is the gate's own child: no check needed. `procs.stop` / `find` are for
worktree strays: no change.

How pid liveness is done today: `procs.alive` = `psutil.Process(pid)`, `is_running()` and status not
zombie; `NoSuchProcess` -> False; `AccessDenied` -> True. Nothing compares times. `stop_group` is POSIX
`os.killpg(SIGTERM)` (ProcessLookup/Permission -> False) or Windows `_end_tree` (psutil children kill,
then proc kill).

## 2. psutil

Already a dependency: root `pyproject.toml` line 9 `"psutil==7.2.2"` (pinned with `==`, checked by
`test_code_targets`). Ruff bans a module-level `import psutil` (`banned-module-level-imports`,
pyproject l.56), so every function in `procs.py` imports it inside the function (`_snapshot`,
`_end_tree`, `_signal`, `alive`). `alive_since` must do the same. `procs.py` uses psutil for: process
listing (`process_iter` with `cwd`, `cmdline`), tree kill (`children(recursive=True)`, `kill`),
`terminate/kill`, and `alive`. It does not yet use `create_time()`.

Proposed shape (spec's name): `alive_since(pid: int, recorded: float) -> bool | None`-like. Keep it
simple: a function taking the pid and the file's mtime (epoch float), returning True when
`Process(pid)` exists, is not a zombie and `create_time() <= recorded + 1`. Three answers matter
(spec open point 3): same process / not the same / cannot tell (`AccessDenied` on `create_time`).
Either return a small enum-like (`"same" | "other" | "unknown"`) or two functions, or an arg
`unreadable: bool` naming what to answer for the unreadable case (waiting passes True, stopping
passes False). The last is the smallest and keeps callers' arg counts low.
Note `psutil.Process.is_running()` already guards pid reuse only for an object held across time; a
fresh `Process(pid)` gives no protection, which is the bug.

Measured on this Windows machine (psutil 7.2.2): `create_time()` of the current process is correct
epoch; a file opened `a+` and kept open reports a fresh `os.stat().st_mtime` immediately after
`write/flush` (age 0.0002 s), so the lock file's mtime is reliable while the gate holds it open. The
lock's text is written (`holding`) after the process it names exists, as the spec says.

## 3. The scenario helpers and where E1-E5 go (`scenario/run_scenario.py`, 5574 lines; not a size target)

- `lock_names(w, what) -> bool` l.2589: polls up to 10 s for `what` in the lock file text (opens it,
  `seek(1)` because byte 0 is the locked byte on Windows). It only reads the text, so the lock format
  must stay `\0<space>?<cr> pid <n>[ pg<m>]`: the file really starts with byte 0 = `\0` (the OS lock)
  and then ` ` + text (`holding` writes `f" {text}"`).
- `stop_own_gate(w)` l.2635 (section 18b): imports `from chantier import procs` (`procs.alive`, l.2675).
  `slow_stop.py` writes its pid to `slow_stop.pid` then sleeps 60; `slow_gate = '"<python>" "<slow>"'`;
  two CRs `one`, `two` (slots 2); helpers inside: `events(cr)` (gate events from `events.jsonl`),
  `logs(cr)` (gate logs), `background(cr)` (Popen `python -m chantier gate cr slow_gate`, then
  `lock_names(w, f"{cr} pid")`, `lock_names(w, " pg")`). This is the natural home of **E1** (gate
  alive + suite, `order merged --epoch 1` instead of `--stop`; check exit 4/STOPPED, `events(cr)[-1]
  ["result"]=="stopped"`, CR in `3-done`, `procs.alive` of the pid file false, then a gate of `two`
  runs with no waiting line) and **E2** (lock names `two`, `order merged one`, no `stopped` line, two's
  suite still alive). Caveat: `order merged` needs the CR to be in a state `merge_done` accepts (the
  CR must be past `working`; check `done_cr`/the `ready` requirement) and a merged CR cannot run the
  next gate steps of 18b (they use `one`), so E1 is best run last in this function on a spare CR, or
  with a third item.
- `rails(w)` l.2737 (section 19), gate-queue steps l.2823-2904: `held_gate(cr)`, "a long gate whose
  command died still holds the next one while its suite runs" (l.2838-2848, `held.kill()` then
  `gate two` waits, asserts `its command still runs`), then the queue block (l.2850-2904:
  `queue = w.state/".long-gate.queue"`, `tickets()`, `wait_tickets(n)`, `queued_gate(cr)`,
  `gate_events()`; "a waiter killed in the queue leaves a ticket that the next gate skips"
  l.2890-2904). **E3** (reused pid: write the lock `\0<cr> pid <dead> pg<P>` with `P` a sleeper started
  after the write, `os.utime` 10 s back) and **E4** (ticket with a reused pid and mtime set back) go
  right after l.2904, same function. Careful: the "its command still runs" check there relies on
  the new rule: the suite's pg is created before `holding()` writes it, so it still passes the
  identity test.
- `driver_liveness(w)` l.2907 (section 12c): l.2931 writes `f"{three} pid 1 pg1"`; l.2938 expects
  `activity {three} gate running`; l.2968 unlinks the lock. **E5** changes the pid to `os.getpid()` of
  the scenario (fresh mtime) and adds queue-ticket cases around l.2932-2939. Note: on POSIX pid 1
  exists and passes the identity test (older than mtime), on Windows pid 1 does not exist: hence the
  spec's change. Section 12c has `one,two,three` all working CRs with agents set.
- Scenario sections are called from `scenario(w)` l.538; `cancel_during_gate` (section 18, l.2603)
  is the natural place for the `cancel` + reused pg check of E3.
- Also `gate_passed` helper l.2627 (adds `src` to `sys.path`; scenario already imports `chantier`
  modules in-process, so E3/E4 may call `procs` there).

## 4. foreman.md (the spec's line numbers are stale)

On this worktree: **line 102** is the activity list (inside "Your means", `$CHANTIER status` bullet
l.100-104: "...the age of its last event or session record, `gate running`, or `not measured`;..."),
and **line 284** is the lost-Driver "Suspect" rule ("shows no activity and no `gate running` for one
full heartbeat interval (30 minutes). A line"). The spec's 97 and 279 are old. Nothing in
`agents/` or `com.github.copilot/agents/` mentions them (grep: only foreman.md l.102/284, `gate.py`,
`batch_status.py` l.88/111/349 and the scenario l.2938). Re-flow the paragraph at each place: the
text is wrapped at about 100 columns, so the edit may move line breaks within the same bullet.
Check also `scenario` card checks (spec E6) and `docs/` for the phrase `gate running`: none found.

## 5. Headroom against the targets (`tests/test_code_targets.py`: file <= 400, function <= 50;
ruff: complexity 10, args 5, positional 5, branches 12, returns 6, statements 50, nested blocks 3)

| Module | Lines | Room | Risk |
| --- | --- | --- | --- |
| `procs.py` | 117 | 283 | none |
| `commands/gate_lock.py` | 154 | 246 | `_acquire` is 43 lines (l.99-141) with many branches/`and/or`: it is already near complexity 10 and 50 lines. The new identity tests in the wait must go into helpers (e.g. a `_suite_left(text)` returning the live pg or None and a `_wait_suite`), not inline. `_ticket_cr` 16 lines, fine |
| `commands/gate.py` | 307 | 93 | `_gate_stop` is 34 lines. The shared stop for A needs the run-file helpers (`_run_read`, `_run_file`, `_stop_file`) and a batch write; if it is added here the file reaches ~350. Better: move the stop (and the run-file helpers) into one module (e.g. `commands/gate_run.py` or `gate_stop.py`) imported by `gate.py` and `orders_apply.py`. Importing `gate.py` from `orders_apply.py` is not a cycle today (gate imports crs, gate_lock, registry, core, lifecycle; none import orders*), but gate.py also registers a command, so a plain helper module is cleaner |
| `commands/batch_status.py` | 369 | 31 | **Tight.** `_activity` is 36 lines (l.83-118) and the spec adds queued logic (2 more lines kinds, reading `.long-gate.queue`, parse, ahead ordering): ~35-45 more lines. It will pass 400. Move `_activity` and its helpers (`_event_ages`, `_targets`, `_mine`, `_record_line`, and the new gate-state helper) to a new module (e.g. `commands/activity.py`); `_refresh` imports it. Check the `test_cli_runs`/other tests do not import `batch_status._activity` (grep found none in tests) |
| `commands/orders_apply.py` | 312 | 88 | `_merged` is 15 lines; +10 for the stop call. Fine |
| `commands/release.py` | 132 | 268 | `cancel` is 32 lines; +4-6 for the identity check. Fine |
| `core/batch.py`, `rails_release.py` | untouched | | `rails` stays process-free, as spec |

Args: the shared stop needs `(repo, b: Batch, cr: str, wt?)`; `_gate_stop` today has 4. The
stop must not open a second `RenderedBatch` when called from `order merged` (the spec says so): take the
open `Batch` and call `b.log("gate", cr, result="stopped", head=..., command=run.command, run=run.run)`
(`Batch.log(kind, cr=None, **fields)`, `core/batch.py` l.178). `_gate_stop` keeps its own `RenderedBatch`
and passes it in. Note `head` for the merged case: `_gate_stop` falls back to `git rev-parse HEAD` in the
CR's worktree; at `merged` time the worktree may be gone, so use `run.head` only (spec says "the run's head").
The "ten-line cap" for `order` output: effect is `reopened + apply_order(...)`; one more line is fine.

## 6. Other findings for the Driver

- Lock order in `order`: `changes_lock(repo)` is held while `_merged` runs. The gate (stopped command)
  also writes the batch (`RenderedBatch` in `_finish_stopped`) later and does not take `changes_lock`
  at the point of the stop; confirm `RenderedBatch` serialises on its own lock before relying on it,
  since the stopped gate will record its own `stopped` event just after `order merged` released.
  `cancel` already does the same with `changes_lock` + `stop_group`, so there is precedent.
- Windows: `order merged` moves the CR's folder (`done_cr`) while the gate's log may still be open by
  the suite: `_spawn` closes the log handle while the gate runs ("a cancel must be able to move the CR's
  folder on Windows"), but the suite's stdout is that file handle (`stdout=f` passed to Popen, and the
  child keeps it open). `cancel` has the same shape and the scenario passes, since the pg is killed
  before `trash_cr`. For A, stop the pg **before** `merge_done` moves the folder, or the move can hit a
  sharing violation. The spec says "the stop runs only after the refusals pass"; it does not fix the
  order against the move. Recommend: refusals, then stop, then `merge_done`/`release_merged`.
  The stop writes `result: stopped` to `run.log` (a path inside the CR folder): do it before the move
  as well, or the recorded path is stale (the gate has the same concern: `if g.log.exists()`).
  This changes where the spec places the output line; the line is still appended after
  the `merged ...` line.
- `merge_done` returns lines; a stopped line is appended by the caller (`_merged`) after, never inside
  `rails_release`.
- Release CR: `release_merged` touches only the record and returns None; `_merged` adds the line.
- `.long-gate.run` has `RunRecord` fields `cr, run, head, log, command, pg` (`core/records.py` l.211):
  check `cr` of the run record, not only the lock's holder, before recording on behalf of a dead gate.
- psutil `create_time()` of a zombie/other-user process: `AccessDenied` handled per open point 3;
  `NoSuchProcess` -> not alive.

## 7. Evidence plan (what the Verifier keeps in `work/verifier/evidence/`)

Run in the worktree; the CLI is `uv run --locked --project <worktree> chantier`.

1. `just check` on Windows (lint with the size/complexity targets, `mypy --strict`, tests): capture the
   tail + exit code.
2. `just scenario` on both forges on Windows (the scenario takes long; `procs.py` is per system, spec E7),
   output saved, with the new check lines quoted:
   - E1 (18b): `order merged` stops the gate (output holds `stopped the long gate of <cr> (pg`, suite pid
     gone, gate exit 4 `STOPPED`, last gate event `stopped`, CR in `3-done`, next gate no waiting line).
   - E2: another CR's suite untouched, no `stopped` line.
   - E3 (in `rails`/`cancel_during_gate`): reused-pid lock, a gate of another CR passes at once, `cancel`
     lists no `pg<P>` and `<P>` still alive; same for `order merged`.
   - E4: reused-pid ticket deleted by the next gate.
   - E5 (12c): `gate running` with the scenario's own pid; `gate queued behind {three}`, ticket kept
     after `status`; `gate queued` alone; dead-pid lock -> an age; dead-pid ticket -> no `queued` line.
3. A manual repro of the retro case on Windows (not only the scenario): start a gate with a slow suite,
   `order merged --epoch`, then show the lock empty and the next gate starting at once; and `activity`
   output with a queued gate, copied raw.
4. E6: `git diff -- skills/chantier/references/foreman.md` showing the two bullets only (lines ~102 and
   ~284 on this base) and the scenario's card checks passing.
5. Unit-level proof of the identity rule: a short in-process check (or a structure test) of
   `procs.alive_since` (same process true; pid with a later creation time false; nonexistent false;
   AccessDenied branch). AGENTS.md says tests check the structure only, so this stays a scenario step
   (E3/E4), not a new test file.
6. CI on Linux, macOS and Windows green on the PR (E7), with `lint` including sizes: quote the run
   URL. Because CI runs the scenario on Linux only, the Windows run above is the only proof for
   `taskkill`/`_end_tree` paths: keep that log.
7. No `just mod` needed (no `hooks/` or `types/` change), no pane screenshot (no `STATUS.json` field
   changes): say so in the PR.
