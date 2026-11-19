# The watcher starts on its own with a running batch

Short name: `watcher-autostart`. No tracker issue (verbal, the user, 2026-11-18).

Stacks on two CRs of batch-28, which land below or beside it: `open-empty-batch`
(`4-batch/1-pending/369-open-an-empty-batch-paused-waiting-for-i`) and `ready-joins-waiting-batch`
(`4-batch/1-pending/370-a-specified-cr-joins-the-waiting-batch-o`). It changes neither one's
behaviour; it adds one line to outputs they also touch, and where they land first it rebases on
their text (see "With the two batch-28 CRs").

## Goal

On 2026-11-18 the Chief of Staff opened batch-28 and did not start the watcher, though its card
says so in one long paragraph; started by hand, it was given a `--batch` flag `watch` does not take
and failed. The user: the watcher needs an automatic trigger, and the instructions must be clear
enough not to be missed. Wanted: at each moment a watcher is due, the CLI's own output ends with
the exact command to start in the background when no watcher of this session runs, and the
Chief of Staff's cards make that line a step it does at once, written where it reads it at the
moment it acts.

## Decisions carried from `02-answers.md`

1. The CLI never starts the watcher: the watcher's end must wake the Chief of Staff's session, so
   it is that session's background task. The trigger is a printed line, not a spawn.
2. When no watcher of this project started by this session runs and the batch runs, these outputs
   end with one line naming the exact command, with the right `--after <seq>` and no flag `watch`
   refuses: `open` (when the batch runs), the `take` or `order` that sets a paused batch running
   again, `status` with a running batch, and the switch to direct mode. When one runs, nothing is
   added; `status` keeps its `watch:` line as today. A watcher of another session (an earlier one,
   or another session on this machine) does not count: its end wakes that session, not this one;
   `status` names it in one line.
3. The line names the Chief of Staff; a Foreman or a Driver that sees it ignores it. Only the
   Chief of Staff starts the watcher, never a Foreman or a Griller.
4. The cards make the line a step done at once, with the session's yes; after the user's no in the
   session the line is ignored.
5. Answer 2 (clarity): the step is written where the Chief of Staff reads it when it acts: a
   numbered step of its own in `chief-of-staff.md` "Starting a batch" ("start the watcher"), a line
   in the Chief of Staff's startup core (read at every boot and reload), and an entry-points table
   row for the line.
6. The rule is one sentence with the command as printed: "run the printed command as is: no flag
   added".
7. A structure test checks that the startup core and "Starting a batch" carry the step.
8. Out of scope: what the watcher reads and when it ends; a paused batch (factory pause included)
   needs no watcher, and the line comes back when the batch runs again.
9. Answer 4: the watcher's own end, when a batch still runs, is one line of the same shape,
   `watch: <batch> still running: for the Chief of Staff, start again in the background now:
   <exact command>`, from the same helper (`cli_command(repo)`, never a bare `chantier`); with no
   running batch, its `no running batch` end and no restart, as today.
10. The startup reading limit does not rise: 12,544 in its three places. The startup core line fits
    by trimming wording, never a rule; the two cuts in `skills/chief-of-staff/SKILL.md` below are
    accepted (each clause stays said where the budget section names). If it cannot fit without
    dropping a rule, the Driver stops `blocked` with the measured numbers. The wider optimisation
    of the startup core is the CR `startup-core-optimise`, not this one.
11. The watcher's lock file in the git folder, named in `AGENTS.md`'s write lists, is accepted
    (its name is per session, below: `chantier/watch-<project>/<session>.lock`).

## What changes

All CLI paths are under `skills/chantier/scripts/cli/src/chantier/`.

### Knowing whether a watcher of this session runs (`hub/lock.py`, `hub/watch.py`)

The hub's lock and `hub.json` cannot say it: the hub is one watcher of the whole surface, maybe
another project's or another session's, and a watcher that is not the hub leaves no trace. So each
watcher holds a lock of its own, taken the same way as the hub's (an OS lock,
`core.files.try_lock`, never waited on, released by the OS when the process exits or dies, so
never stale), keyed by its project and its session:

- `<session>` is `own_transcript(detect_host())` (`commands/seat.py`: `CLAUDE_CODE_SESSION_ID` or
  `COPILOT_AGENT_SESSION_ID`), read by the watcher from its own environment, which the session's
  background task inherits: no new flag on `watch`. Kept to `[A-Za-z0-9-]` (a host's session id
  is a UUID); with none, or nothing left, the key is `none`, and a CLI run with no session id
  matches the `none` watcher only. The same function gives the session at every reader below, so
  writer and reader always agree.
- The file: `chantier/watch-<project>/<session>.lock` in the git folder (`lock.folder(git_dir)`),
  `<project>` being `project_name(repo)` (the project's folder name under `projects/`, else the
  repository folder's name, as `hub.json` keys its projects). Its name is the record of the
  session: nothing is written in it. It is left in place at the watcher's end (empty, one per
  session that ran a watcher; never removed, so no race between a removal and a new watcher of the
  same session).
- `hub/lock.py`: a `WatcherLock(git_dir, project, session)` beside `HubLock` (same `acquire`,
  `release`, `held`; share the code rather than copy it), and
  `watchers(git_dir, project) -> list[str]`: the sessions whose lock file exists and is held now.
  For each `*.lock` file of `chantier/watch-<project>/` (a folder per project, so no project's
  name can prefix another's): open it (the probe never creates a file or folder), `try_lock`:
  taken means no watcher holds it, so release at once and skip it; refused means that session's
  watcher runs (the file's stem is the session).
- `hub/watch.py`, `Watch`: takes its own lock in `elect()` (the start, then every poll while
  not held), so a watcher that started while a probe briefly held the lock still takes it at the
  next poll; `close()` releases it. A second watcher of the same project and session (the session
  started two) simply never holds it and runs as today. Nothing else in the watcher changes: what
  it reads, its event lines and when it ends are as today; only its last line changes (below).

### The line (`hub/watch.py` or a small `hub/autostart.py`)

Two helpers, used by every output below and by the watcher's end, so the command exists once:

```
watch_command(repo, n) -> str          # f"{cli_command(repo)} watch --after {n}"
not_running_line(repo, status) -> list[str]
```

- `status` is the batch's status as the caller holds it in its record (the callers below compose
  their lines inside `RenderedBatch`, before `batch.json` is written: never re-read the disk).
- Returns `[]` when `status != "running"` or this session's key is among `watchers(...)`. Else one
  line:

  `watch: not running: for the Chief of Staff, start in the background: <command>`

  where `<command>` is `watch_command(repo, n)`: `cli_command` from
  `plugin_files.py` (the dev checkout's `uv run --no-sync --project "<plugin root>" chantier`, or
  the plugin's `uvx --from "<plugin root>" chantier --skill "<skill folder>"`, plus
  `--project "<project folder>"` on a planning surface), and `n` the journal's highest seq now
  (`journal.last_seq(journal.read(repo.changes)[0])`, the value `status`'s `watch:` line uses
  today). No `--batch`, no other flag: `watch` takes only `--after`.

### The watcher's end line (`hub/watch.py`, `Watch.lines`)

The `events` end (reached only while `running_batch(repo)` holds a running batch) now ends with:

`watch: <batch> still running: for the Chief of Staff, start again in the background now: <watch_command(repo, n)>`

`<batch>` the running batch's name (`running_batch(repo)`'s record, read at the end), `n` the
watcher's cursor (so the `--after` carries it; the old `watch: cursor <n>; next: chantier watch
--after <n>` line is gone, its cursor kept in the command). Its event lines come before it, as
today. The `no-batch` end is unchanged: `watch: no running batch in <project>; ended`, no restart.

### The outputs that end with it

Each appends the helper's result as its very last line, not indented, outside any Driver prompt
block (after the block's last line), so it is never part of what a Foreman copies into a Driver's
prompt or relays with the block.

- `open` (`commands/opening.py`, `open_batch`): after the CR lines, with the new record's status.
  A batch born paused (`open-empty-batch`) prints none.
- `take` (`commands/driver.py`): when `_reopen` set a paused batch running (its
  `was paused: running again` line), the take's output ends with the helper's line, after the
  Driver prompt block. Only that case: a `take` on a batch already running adds nothing.
- `order` (`commands/orders.py`, `_reopen`, kind `qa`): the same, when the QA order set the paused
  batch running, after its block. `order add` on a paused batch leaves it paused (and, with
  `ready-joins-waiting-batch`, so does the join of `triage --ready`): no line.
- The switch to direct mode (`commands/seat.py`, `_transcript`): when it prints
  `steering direct: the Chief of Staff steers <batch> as Foreman n°<n>`, the output ends with the
  helper's line for the batch's status (a paused batch: none).
- `status` (`commands/batch_status.py`): `_watch_lines` keeps `forge hub: …` always on a running
  batch. Then:
  - a watcher of this session runs: today's `watch: chantier watch --after <n>` line, as today;
  - none of this session runs: no `watch: chantier watch …` line there; the helper's line is the
    last line of the whole output (after `extra`, the refresh's lines), so one line names the
    command, not two;
  - a watcher of another session runs (any case above): one line in `_watch_lines`' place,
    `watch: session <id> runs a watcher too; its end wakes that session, not this one` (one line
    per such session; `<id>` the session key, `none` included);
  - a paused batch: as today, no `watch:` line.

### The ten-line cut keeps it (`cli.py`)

`open` and `foreman` are not in `FULL_OUTPUT`: past `MAX_LINES` their output is cut from the end,
which would drop a last line. Extract the cut into a small function and make it keep a last line
that starts with `watch: not running:`: `[*lines[: MAX_LINES - 2], "… <k> more lines", last]`,
`k` the lines dropped (twelve lines: three). Any other output is cut as today.

### Cards (`skills/chantier/references/`, `skills/chief-of-staff/SKILL.md`)

The one sentence, word for word everywhere it appears: **run the printed command as is: no flag
added.**

- `skills/chief-of-staff/SKILL.md`, "## Startup core" (read at every boot and reload): one line
  after its present text:

  ```text
  A `watch: not running` line in any output, a reload's too: start the watcher now, on the session's yes; run the printed command as is: no flag added.
  ```

- `skills/chief-of-staff/SKILL.md`, the reload sentence: "follow `session-start.md`, "5. Reload",
  nothing else of this file" becomes "… "5. Reload", nothing else of this file but its Startup
  core", so the reload reads the line above (the budget already counts the Startup core in the
  reload's reading set).
- `chief-of-staff.md`, "Entry points" table, a row after the "a watcher's end" row:

  ```text
  | a `watch: not running` line in any output (`open`, `take`, `order qa`, `foreman transcript`, `status`) | start the watcher now in the background, by the host's means, on the session's yes (asked once per session): run the printed command as is: no flag added; after the user's no in this session, ignore the line | While it runs |
  ```

  The "a watcher's end" row says: its last line `watch: <batch> still running: …` names the
  restart: run the printed command as is: no flag added (on the session's yes already given).
- `chief-of-staff.md`, "Starting a batch": a new numbered step, written `5. **Start the watcher.**`
  as the other steps are, after step 4 (the Foreman's start or direct steering, with its "Reusing
  the last Foreman" paragraph), before "### The floor": when `open` ends with
  `watch: not running: …`, start it now in the background, by the host's means, on the session's
  yes (the first time in the session, ask as `session-start.md` says): run the printed command as
  is: no flag added. A batch opened paused (`open` with no CR) prints no such line: it comes with
  the first `take` that sets the batch running (direct mode: your own `take`; Foreman mode: the
  Foreman's `take`, which the Foreman ignores, so the line reaches you at your next `status`, your
  next report or the next Foreman message you act on).
- `chief-of-staff.md`, "The watcher" (~line 1220): the *When it starts* bullet is rewritten around
  the line: the CLI prints `watch: not running: for the Chief of Staff, start in the background:
  <command>` when the batch runs and no watcher of this session runs (after `open`, the `take` or
  `order qa` that sets a paused batch running, the switch to direct mode, `status` at a session
  start, a reload or any time); start it at once, on the session's yes: run the printed command as
  is: no flag added. In Foreman mode the resuming `take` is the Foreman's, so the line reaches you
  at your next `status` (your next report, or the next Foreman message you act on). A watcher of
  another session, which `status` names, does not wake you: start your own. After a watcher's end:
  its last line `watch: <batch> still running: …` prints the restart: run the printed command as
  is: no flag added. A watcher that ends with `no running batch` is not started again; a paused
  batch prints no line (a factory batch at its pause included); the line returns once the batch
  runs again. The *Never* bullet stays. Remove its present text that this replaces, explicitly
  including, at ~lines 1227-1228, "with the `--after <seq>` of its last line (else the `watch:`
  line of `status`)", so no card names a bare-`chantier` line as a command to run.
- `chief-of-staff.md`, the seat hand-over (~line 1683): the new Chief of Staff starts its own
  watcher from the line of its `status` (another session's watcher, the old one's included, does
  not count; its `status` names it).
- `chief-of-staff.md`, "Switching to direct mode", step 7 (Claim): after the steering line, start
  the watcher if the output ends with the line (the same sentence).
- `session-start.md`, "The watcher" (~line 97): the start is the `watch: not running` line of
  `status` (or of any output later): with the session's yes, start it at once; run the printed
  command as is: no flag added. `session-start.md`, "## 5. Reload", is not edited (the reload's
  start comes from the startup core's line).
- `foreman.md` (~line 772, the heartbeat bullet): the `watch: not running` line in any output,
  `take`'s and `order qa`'s included, like the `forge hub:` and `watch:` lines, is the Chief of
  Staff's: do nothing with it, send no message about it; it is no undone order. The CLI prints it
  outside the Driver prompt block, not indented: never copy it into a Driver's prompt nor relay it
  with the block.
- `hosts/claude-code.md` and `hosts/copilot.md`, row "Run the watcher": the command is the one the
  `watch: not running` or `still running` line prints, as is (in place of
  `$CHANTIER watch --after <n>`); the rest of each row unchanged.
- The agent files (`agents/`, `com.github.copilot/agents/`) are not touched.

### The startup reading budget

The Chief of Staff's reload on Copilot reads 12,544 bytes today, the allowed maximum
(`startup-manifest.json` `limit`, `STARTUP_LIMIT` in `tests/test_startup_manifest.py` and
`tests/test_plugin_files.py`); the limit is not raised. The additions are paid by cuts in the
Chief of Staff's own `SKILL.md`, which only that role reads (measured with UTF-8, LF):

| Change | Bytes |
| --- | --- |
| Startup core line, with its newline and blank line | +151 |
| Reload sentence: ` but its Startup core` | +21 |
| `SKILL.md`: drop "Nothing to install but `uv`: the project's `AGENTS.md` and an optional `chantier.yaml` (the project's, and its planning surface's) are the only configuration; " and join the rest into one sentence: "chantier writes only to the planning folder (`.agents/changes/`, or the project's folder of an external surface), and a CR's archive in its PR when the project asks; in a planning surface, `$CHANTIER` also carries `--project <the project's folder>`." (the zero-configuration rule stays in `session-start.md`, "Zero configuration", and the user's `AGENTS.md`) | -159 |
| `SKILL.md`: drop "; only the steering session syncs, never a Foreman, a Driver or a worker" (this file is read by the Chief of Staff alone, the steering session; `chief-of-staff.md` step 1 keeps "Only you sync, never a Foreman, a Driver or a worker") | -72 |
| Net, Chief of Staff | -59 |

Measured on 2026-11-18 (`pytest -s -k measures`, `startup-bytes`), with this table applied:

| Role, host | Boot today | Reload today | Boot after | Reload after |
| --- | --- | --- | --- | --- |
| chief-of-staff, Copilot | 11,801 | 12,544 | 11,742 | 12,485 |
| chief-of-staff, Claude Code | 11,795 | 12,538 | 11,736 | 12,479 |
| router, Copilot (highest other) | 11,759 | 12,502 | unchanged | unchanged |

No file read by another role changes (the shared Reload clause of the previous version is
dropped), so every other role and host is unchanged. The Driver measures it again and keeps every
role and host at or under 12,544. The limit stays 12,544 in its three places
(`startup-manifest.json`, `test_startup_manifest.py`, `test_plugin_files.py`), none edited. Should
the measure differ from this table, the Driver may trim further wording only (never a rule) in
the files the Chief of Staff reads at boot and reload, named in the PR; if it still cannot fit
without dropping a rule, it stops `blocked` with the measured numbers (each role and host, boot
and reload). Any wider optimisation of the startup core is `startup-core-optimise`.

### Docs and project rules

- `AGENTS.md`, both places that list what chantier writes in the git folder (the configuration
  bullet: "the forge hub keeps its lock and, while it runs, … there too (`chantier/hub.lock`,
  `chantier/hub.json`)", and the forge hub exception): add each watcher's lock,
  `chantier/watch-<project>/<session>.lock`, one per project and session that ran a watcher, held
  while it runs, empty and never removed.
- `CONTRIBUTING.md` (~line 89): the same file added beside `chantier/hub.lock` and `hub.json`.
- `hub/__init__.py` docstring: one sentence on the watcher's lock per project and session, and that
  `status`, `open`, `take`, `order` and the switch read it to print the `watch: not running` line.
- `scenario/README.md`: the coverage bullets below (and its `watch: cursor 1; next: ...` mention,
  ~line 305, rewritten to the new end line).

## With the two batch-28 CRs

- `open-empty-batch`: `open` with no CR is born paused, so it prints no `watch: not running` line;
  its `status` (paused, `no CR yet`) prints none either, as `_watch_lines` already returns nothing
  on a paused batch. The first `take` sets it running and its output ends with the line (direct
  mode: the Chief of Staff's `take`, which it acts on; Foreman mode: the Foreman's, ignored, so the
  Chief of Staff gets the line at its next `status`, its next report or the next Foreman message it
  acts on). The card's new step 5 says so. Its own `open` output (`opened … no CR, paused …`,
  `next: …`) is unchanged.
- `ready-joins-waiting-batch`: `open --factory` with CRs runs, so its output ends with the line,
  after its `3-ready holds …` line. A factory batch at its pause: the watcher ends with `no running
  batch` and is not restarted; `status` prints no line; `triage --ready` joining it leaves it
  paused (no line); the `take` that runs it again prints it. `order factory on|off` never changes
  the batch's status, so it prints none.
- Whichever lands first, the other rebases: the helper's line is always the output's last line,
  after anything those CRs add.

## Command form (the line's `<command>`)

The line does not depend on the host (Claude Code and Copilot print the same line; each host's
reference says how to start it in the background). It depends on the install and the planning
folder, through `cli_command`:

- Plugin copy, in-project `.agents/changes/`: `uvx --from "<plugin root>" chantier --skill "<skill folder>" watch --after <n>`.
- Plugin copy, planning surface: the same with `--project "<project folder>"` after `--skill …`.
- chantier's own checkout, in-project: `uv run --no-sync --project "<plugin root>" chantier watch --after <n>`.
- chantier's own checkout, planning surface: the same with `--project "<project folder>"` after `chantier`.

## Out of scope

- What the watcher reads and when it ends (only its end line changes, above).
- Raising the startup limit; optimising the startup core beyond this line (`startup-core-optimise`).
- The CLI starting the watcher; stopping another session's watcher.
- Removing the watchers' lock files.
- A watcher on a paused batch; any change to the factory pause.
- Any other output gaining the line (`order add`, `order merged`, `seat take`, `handback`, …).
- The CR board pane and `STATUS.json`: nothing they show changes, so no pane screenshot is owed.

## Evidence

Tests (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; mostly
`test_forge_hub.py`):

1. `watchers`, parametrized: no lock file (`[]`, and no file created); a `Watch` started
   in-process under session `s1` holding its lock (`["s1"]`); after its `close()` (`[]`, the file
   still there). A `Watch` whose first `elect()` lost its lock to a probe takes it at its next
   `poll`. A held `watch-<other project>/s1.lock` is not listed.
2. The outputs, parametrized over the command (`open <folder>`, `take` on a paused batch, `order
   qa` on a paused direct batch, `foreman transcript <chief uuid>` on a running Foreman batch,
   `status` on a running batch) × (no watcher, a `Watch` of this session, a `Watch` of another
   session; the session set through the host's environment variable): with no watcher of this
   session the last line is exactly `watch: not running: for the Chief of Staff, start in the
   background: ` + `cli_command(repo)` + ` watch --after <n>`, `n` the journal's last seq (a
   journal prepared with entries), not indented and after any Driver prompt block, and it holds
   no `--batch`; with this session's watcher, no such line, and `status` keeps
   `watch: chantier watch --after <n>`; with another session's, the line prints and `status` also
   holds `watch: session <id> runs a watcher too; …`. Plus the cases that print none: `open` with
   no CR (once `open-empty-batch` is below), `take` on a running batch, `order add` on a paused
   batch, `status` of a paused batch.
3. The existing `test_status_and_the_start_line_name_the_journal_the_hub_and_its_version`: its
   `got[:2]` expectation updated (no watcher: `forge hub: none running`, then the line last).
4. The watcher's end: `Watch.lines(EVENTS)`'s last line is `watch: <batch> still running: for the
   Chief of Staff, start again in the background now: ` + `watch_command(repo, n)`
   (`test_a_watcher_ends_twenty_seconds_after_the_last_event`'s expected `last` updated); the
   `no running batch` end unchanged.
5. The cut (`cli.py`): a list of twelve lines ending with a `watch: not running:` line keeps it
   last after `… 3 more lines`; any other twelve-line list is cut as today.
6. Structure test (a new parametrized test beside `test_startup_manifest.py`), reading the shipped
   files from the repository at the head under test, never a prepared text: the `## Startup core`
   section of `skills/chief-of-staff/SKILL.md` holds `` `watch: not running` `` and `run the printed
   command as is: no flag added`, and its reload sentence holds `but its Startup core`;
   `chief-of-staff.md`'s `## Starting a batch` section holds a numbered step
   `**Start the watcher.**` with the same sentence; its `## Entry points` table holds a row starting
   `` | a `watch: not running` line ``. The test reuses `_section_span` from
   `test_startup_manifest.py` (or a shared helper), so it reads sections as the budget does.
7. `test_startup_manifest_measures_every_real_role_and_host` passes with its limit unchanged.

`just test` stays within its budget (AGENTS.md).

Scenario (`scenario/run_scenario.py`):

- unit `surface-board`, `forge_hub`:
  - the check at ~line 1787 (`status` of a running batch before any watcher) now expects `forge
    hub: none running` and, last, the `watch: not running: …` line whose command ends `watch
    --after 0` and starts with the scenario's CLI form, and no `watch: chantier watch` line;
  - while watchers run (~line 1814, started from the scenario's session), `status` of `demo` holds
    `watch: chantier watch --after …` and no `watch: not running` line;
  - after A's watcher ended on its merge and before it is restarted, `status` of `demo` ends with
    the line again with the journal's last seq;
  - after A's batch paused (~line 1901), `status` of `demo` holds no `watch:` line;
  - the watcher end checks (the `cursor(n)` helper, ~line 1763, and every check using it) expect
    `watch: <batch> still running: for the Chief of Staff, start again in the background now: `
    followed by the scenario's CLI form and `watch --after <n>`.
- unit `direct`: the check at ~line 2627, "the first `take` says the batch was paused, and the
  event log has `reopen` before that `take`" (the first `take` on the reopened direct batch), also
  checks that this `take`'s output ends with the `watch: not running: …` line, not indented, after
  the Driver prompt block.

Each check mapped in `scenario/README.md`'s coverage list. The change touches the CLI and the
cards: the `just scenario (ubuntu-latest)` job is green at the PR's head before the PR; the Driver
runs `just check` and `just eval-dry-run` in its worktree at the rebased head before the first
push (AGENTS.md). No `hooks/` or `types/` change, so no `just mod`.

## Open questions

None for behaviour. One for the Chief of Staff to confirm: the accepted lock name
`chantier/watch-<project>.lock` becomes `chantier/watch-<project>/<session>.lock` (one per
session), which per-session detection needs; `AGENTS.md`'s write lists name the new form.
