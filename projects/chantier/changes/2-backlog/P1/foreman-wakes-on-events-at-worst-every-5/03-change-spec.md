# The Foreman runs its own watcher and wakes at worst every 55 minutes

Short name: `foreman-wake`. Destination: the next batch (`3-ready`), after
`watcher-runs-through-several-events-inst` (`watcher-limit`) and after CR-471 (`slim-cards`).

## Goal

In the owner's words (Markdown Studio batch-07 retro, 2026-11-22): with the notification server
and the watchers, the Foreman should no longer need to wake on a timer; at worst once every 55
minutes, to stay under the 1-hour cache TTL. The user chose (foreman-wake-Q1, option B, not the
recommended A) to keep the timer, at 30 to 55 minutes on Claude Code, and to give the Foreman a
watcher of its own that subscribes to the batch's events (a merge, a red CI, a wait met) instead of
having the Chief of Staff relay them. AGENTS.md's rule that the watcher is the Chief of Staff's is
rewritten.

## Where it stands (main at 3c29dd7c, 2026-11-24)

- **The timer.** `config/chantier.defaults.yml`, `hosts: claude: timing: steering_wake: 30m` (the
  Claude Code value is general; only the `session` column reads it, `board/state.py`
  `steering_wake_min`). `playbook/timing_check.py` refuses a Claude Code `steering_wake` over 60
  minutes (`MAX_STEERING_WAKE_CLAUDE`). `hosts/claude-code.md`, "Heartbeat": the Foreman's `/loop`
  schedules each wake with `ScheduleWakeup` at the steering wake (1800 s by default). Its row
  "Steering wake bound (60 minutes)" holds 30 minutes proved (real-direct run 1, 2026-11-12), any
  other value up to 60 unproved. The session's `cache_ttl` is `1h`. Copilot's Foreman wakes by the
  `/every` the Chief of Staff sends (`steering_wake: 4m`).
- **The watcher is the Chief of Staff's.** `hub/watch.py`: one watcher per project and session
  (lock `chantier/watch-<project>/<session>.lock`, `hub/lock.py`), subscribed to `project`, its own
  `session:<key>` and its `--for` values; it starts the server when none runs only for the session
  that holds the seat (`Watch.seat_rule`), and ends when `seat.json` names another session
  (`seat_moved`). A Foreman's session would see its watcher end at the first seat check, since the
  seat is the Chief of Staff's. `hub/autostart.py` `not_running_line` prints, to every session with
  no watcher lock, `watch: not running: for the Chief of Staff, start in the background: ...`,
  the Foreman's `status --refresh` included; `foreman.md` (heartbeat item, and the closing
  paragraph's "the one exception is the Chief of Staff's watcher in direct mode") tells the Foreman
  to ignore it and to start no background task of its own.
- **The relay.** The hub writes `merged@1`, `checks-red@1` and `wait-cleared@1` lines (audience
  `project`). Their texts (`hub/schemas.py`): `merged_text` and `red_text` end "for the Chief of
  Staff: ...", `wait_cleared_text` already says "for the steering session". The Chief of Staff, at
  its watcher's end (`chief-of-staff.md`, "The watcher", *A watcher's end*), checks a merge on the
  forge, runs `order merged <cr>` and sends its line to the Foreman; sends `checks red <cr> <pr> at
  <head7>` (`routing.md`, Chief of Staff → Foreman); clears a met wait and takes the CR back or
  sends `order note`. The Foreman already acts on a `wait-cleared@1` line itself (`foreman.md`, the
  blocked CR with `; waits:`) and on `checks red` (a note to a live Driver).
- **The measure** (inbox `foreman-idle-wakes`, `experiments/foreman-cost-study.md`, Fable study of
  2026-11-21, the source of every figure here). Batch-29: Foreman $59.71 of $243.54 (25 %), 291
  wakes, 983 calls, 185k tokens of context on average. Its timer wakes: 36 heartbeats with nothing
  new ($6.25) and 5 heartbeats followed by an action ($1.50), 41 of 291 wakes; idle wakes of every
  kind 114 ($11.1). Each heartbeat injects the `/loop` command's text, about 9,000 characters
  (325,000 in batch-29), and so brings compactions closer. The watcher never woke the Foreman (0 of
  1,522 wakes over 13 batches): it wakes the Chief of Staff, who relays by a message or an order.
  The study's verdict: removing every idle wake takes the Foreman's share from 25 % to 21 %
  (batch-29); the larger levers are the calls per event, the context and the model. The request's
  figure (336 wakes "on its timer" in Studio batch-07, $118 of $236 for orchestration) comes from
  another project's batch, whose transcripts this CR did not read; it counts all of that Foreman's
  wakes, not its timer's, and is not used.

## What changes

### 1. The timer: 55 minutes by default on Claude Code

- `config/chantier.defaults.yml`: `hosts: claude: timing: steering_wake: 55m` (from `30m`), the
  comment above the `timing` block saying why (at worst one wake per 55 minutes, under the
  session's 1-hour cache). A project's `chantier.yaml` still sets its own value; the CLI's bound
  (60 minutes) does not change. Copilot's `4m` does not change.
- `hosts/claude-code.md`, "Heartbeat": the default becomes 55 minutes, 3300 seconds. Row
  "Steering wake bound (60 minutes)": 55 minutes is unproved until a batch's Foreman transcript
  shows a `ScheduleWakeup` of 3300 seconds and a wake about 55 minutes later; the first batch run
  on this version is that trial, and records its date and result in the row.
- What follows the steering wake follows it to 55 minutes with no other edit: the board's late
  mark (`steering_wake_min`, wake plus 5 minutes) and the Foreman's **Suspect** rule ("one full
  heartbeat interval (the steering wake, 30 minutes by default)", `foreman.md`, which becomes "55
  minutes by default"); see question 2. The heartbeat's stop "on the first wake that sees no
  Driver of any kind run for 30 minutes or more" keeps its 30 minutes.
- The texts that state the 30-minute default: `foreman.md` (Suspect), `docs/hosts.md` (Claude
  Desktop row), `docs/agents-and-models.md` (the timing line).

### 2. A watcher for the Foreman

The behaviour, in the CLI (`hub/watch.py`, `hub/autostart.py`, `hub/watch_lines.py`,
`declare/watch.py`'s help, `hub/__init__.py`'s docstring):

- **Who it is for.** A `watch` run by the session that the running or paused batch records as
  its Foreman (`foreman_transcript` of `batch.json`, compared as `session_key()` compares the seat:
  kept to `[A-Za-z0-9-]`) is the Foreman's watcher. The CLI tells it apart by that record (the
  batch's steering frame, as `--epoch` is), never by a role name.
- **What it reads.** Only the lines of its batch that the Foreman acts on: `merged@1`,
  `checks-red@1` and `wait-cleared@1` whose `batch` is the recorded batch; every other line
  (`board@1`, `config@1`, `arrived@1`, `issue@1`, `sync-*@1`, another batch's) moves its cursor and
  is neither printed nor waking. How the filter is made (an audience the hub adds, or a filter in
  the watcher) is the Driver's choice; the CLI knows no role either way.
- **The server.** It starts none: the seat is the Chief of Staff's. With no server running it ends
  at once with one line that says so and names the timer as the Foreman's wake until the Chief of
  Staff's watcher or board starts one. Linked, it is one more subscribed client, so the hub keeps
  reading the forge while it runs.
- **Its end.** It wakes its session as the Chief of Staff's watcher does once `watcher-limit` has
  landed (that CR's shape: one watcher through several events while a batch runs, waking the
  session per event). It never ends on the seat: the seat check (`seat_moved`) does not apply to
  it. It ends when the batch no longer records this session as its Foreman (another epoch, a
  switch to direct mode) or the batch is closed, with one line saying which; see question 3.
- **The `watch: not running` line.** In the Foreman's session of a running batch, `status`,
  `take` and `order` print `watch: not running: for the Foreman, start in the background:
  <command>` (no pull-path clause: the Foreman has no user message to pull at), instead of the
  Chief of Staff's line. In any other session the line stays as it is.
- **The Chief of Staff's view.** `status`, in the Chief of Staff's session of a batch in Foreman
  mode, prints whether the Foreman's watcher runs (the Foreman's session holds a watcher lock of
  the project, `lock.watchers`): `foreman watch: running` or `foreman watch: not running`.
- **The lines' texts** (`hub/schemas.py`): `merged_text` and `red_text` say "for the steering
  session" where they say "for the Chief of Staff", as `wait_cleared_text` already does; a red
  line's action names a note to the CR's live Driver and nothing recorded.

The cards:

- `foreman.md` (or the piece of it that CR-471's cut gives the heartbeat and the background-task
  rule): the Foreman starts its watcher in the background with the command its `watch: not
  running` line prints, as is, in the turn that arms the heartbeat (its first `take`), and again
  after each end that asks for it; it stops it, by its id, with the heartbeat (pause, the
  30-minute stop, the switch to direct mode). The closing paragraph's "the one exception is the
  Chief of Staff's watcher in direct mode" names this watcher too. At its watcher's end (or wake):
  - a `forge saw merged ... order merged <cr>` line: check it on the forge as the Chief of Staff
    does today (`gh pr view <pr> --json state,baseRefName,mergedAt`, `glab mr view <iid>`), then
    `order merged <cr> --epoch <n>` and what follows an `order merged` today (dependents, the
    fast-forward); a `not landed` line: record nothing; a line the forge does not confirm: record
    nothing and send the Chief of Staff one line (see question 1);
  - a `forge saw checks red` line: as a `checks red` line today (a note to a live Driver, else
    nothing);
  - a `forge saw ... met` line: as today (`wait <cr> clear <id> --epoch <n>`, then the take-back).
  The heartbeat item's "the `forge hub:` and `watch:` lines are the Chief of Staff's" keeps the
  `forge hub:` line and the Chief of Staff's own `watch:` lines; the `for the Foreman` line is the
  Foreman's.
- `chief-of-staff.md`, "The watcher", *A watcher's end*, and the merge paragraph ("A `forge saw
  merged: <cr> …` line ... in Foreman mode, send its line to the Foreman"): in Foreman mode, while
  `status` shows `foreman watch: running`, the Chief of Staff tells the user the merge or the red
  CI, records nothing and sends the Foreman nothing for these three kinds of line; with `foreman
  watch: not running` (a host where the Foreman cannot run it, or a watcher not started), the
  route stays today's. Direct mode is unchanged. The table row (line 31) follows.
- `routing.md`, Chief of Staff → Foreman: the `checks red` relay is sent only while the Foreman's
  watcher does not run.
- `hosts/claude-code.md`: row "Run the watcher" names the Foreman's watcher (same tool, same
  command form); its wake of an idle Foreman session is unproved, trial: a merge in a batch with
  the Foreman's watcher running, the Foreman's transcript showing the notice, the forge check and
  the `order merged <cr> --epoch <n>` with no message from the Chief of Staff between. Row "The
  watcher when the session ends": a Foreman's watcher left behind ends when the batch records
  another Foreman or closes.
- `hosts/copilot.md`: row "Run the watcher" names the Foreman's watcher under the same rule: if
  the host has no background command or its end does not start a turn, the Foreman starts none,
  says so in one line to the Chief of Staff, and the relay stays today's. Copilot's `/every` is
  unchanged.
- `session-start-chief-of-staff.md`, "The watcher", if it states that the watcher is the Chief of
  Staff's alone.
- `docs/use-cases-foreman.md`, `docs/hosts.md`: one sentence each on the Foreman's watcher.

### 3. AGENTS.md

The rule's sentences as they stand at 3c29dd7c, each rewritten so that a watcher may be the Chief
of Staff's or the batch's Foreman's (rebase onto `watcher-limit` first, which rewrites the end
clause of the same sentence; the rewrite below applies to the text as that CR leaves it):

1. "each session's watcher, run for the Chief of Staff's whole session, with or without a batch,
   subscribes to the surface server's `events` topic for its project (...)": add the Foreman's
   watcher, run for its batch while it runs, which reads only its batch's merge, red-CI and
   wait-met lines.
2. "and starts the server, detached, when none runs and its session holds the seat": the Foreman's
   watcher starts none.
3. "or when the project's seat is another session's": for the Foreman's watcher, when the batch no
   longer records its session as its Foreman or closes, never on the seat.
4. "which `status`, `open`, `take`, `order` and the switch to direct mode read to print the
   `watch: not running` line": the line names whose watcher (the Chief of Staff's or the
   Foreman's), and `status` prints `foreman watch:` for the Chief of Staff.
5. The three "the Chief of Staff's watcher" mentions of the board's journal lines ("which the
   Chief of Staff's watcher reads", "which the Chief of Staff's watcher carries", "`status` and the
   watcher carry to the Chief of Staff"): unchanged in meaning (those lines are not the Foreman's);
   checked that no wording now reads as excluding the Foreman's watcher from merges.
6. "Its measured cost to justify it: one round trip with the user per merge and per board session
   ("rescan")": add the Foreman's watcher's justification: the user's answer foreman-wake-Q1
   (2026-11-22), on the cost study of `foreman-idle-wakes` (batch-29: 41 timer wakes of 291, the
   relays of merges and red CIs by the Chief of Staff), with the gain not measured before the next
   batch's retro.

The forge hub's sentence ("started by a session's watcher, detached, when none runs and the
session holds the seat") stays true and is not edited.

## What it takes from `foreman-idle-wakes`, and what stays paused

That inbox item stays in the inbox, paused; this CR does not move or close it, and its PR says
which part it covers.

- **Taken:** the study's figures (above), and its proof method (foreman-idle-Q8): the first batch
  run on this version, at its retro, repeats the study's wake classification and compares with
  batch-29: the timer's wakes (heartbeats with and without action), the watcher's wakes of the
  Foreman (0 today), the Chief of Staff's relay messages and orders for merges and red CIs, dollars
  per CR, calls per wake, and no event left unanswered.
- **Superseded:** foreman-idle-Q3 (a slow heartbeat of about 20 minutes): foreman-wake-Q1 sets the
  timer at 30 to 55 minutes.
- **Left paused there:** any target share or figure (foreman-idle-Q2, set aside by Q5 until a
  structural study); the levers it set aside (Q7): fewer calls per event, a smaller context or an
  earlier fresh Foreman, the host's "Driver waiting on its own background work" notices (52 wakes
  in batch-29), a turn that reads less when nothing is new; the Foreman's model (Q6: batch-28 and
  batch-29 Foremans ran Opus against the card's Sonnet rule).

## Files and overlaps

Touched: `AGENTS.md`; `config/chantier.defaults.yml`; under
`skills/chantier/scripts/cli/src/chantier/`: `hub/watch.py`, `hub/autostart.py`,
`hub/watch_lines.py`, `hub/schemas.py`, `hub/__init__.py`, `declare/watch.py`, the `status` view
that prints the `watch:` lines (`commands/batch_status.py` or its helper); tests
`skills/chantier/scripts/cli/tests/test_playbook_timing.py` (`SHIPPED_WAKE = 30` becomes 55),
`test_watch_events.py`, `test_watcher_step.py`, `test_watcher_autostart.py`; cards
`skills/chantier/references/foreman.md` (and its CR-471 pieces), `chief-of-staff.md` (and its
pieces), `routing.md`, `hosts/claude-code.md`, `hosts/copilot.md`,
`session-start-chief-of-staff.md` if needed; `docs/hosts.md`, `docs/agents-and-models.md`,
`docs/use-cases-foreman.md`; `scenario/run_scenario.py` and `scenario/README.md`.

Overlaps:
- **`watcher-limit`** (`2-backlog/P1/watcher-runs-through-several-events-inst`) comes first: it
  rewrites the watcher's end (no 2 h limit while a batch runs; the seat lost always ends it), the
  same AGENTS.md sentence, `hub/watch.py`, `chief-of-staff.md` and `hosts/claude-code.md`. This CR
  rebases on it and gives the Foreman's watcher the same run-and-wake shape, with its own end.
- **CR-471** (`slim-cards`, running) cuts `foreman.md` and `chief-of-staff.md` into pieces read by
  `startup-manifest.json` actions: the sections named here may have moved; the Driver edits them
  where they stand at its base, and a rule this CR adds to a piece is reached by an action as
  CR-471's test requires.
- `uv-sync-blocked-by-the-running-board-and` names the session's own watcher among the holders it
  may stop: a Foreman's watcher is not the Chief of Staff's "own" (`hosts/claude-code.md`, the
  holders row); the Driver keeps that reading true.

## Out of scope

- Removing the Foreman's timer (option A); Copilot's `/every` value; the 60-minute bound.
- Direct mode: the Chief of Staff steers with its one watcher, unchanged.
- The levers left paused in `foreman-idle-wakes` (above).
- Any new forge read: the hub reads what it reads today.

## Evidence

- `just check`, `just eval-dry-run` (a CLI change), and the long gate `just scenario`.
- Unit tests, in-process, on a prepared state:
  - `test_playbook_timing.py`: the shipped Claude Code steering wake is 55 minutes, read from
    `config/chantier.defaults.yml` as it ships (`steering_wake_min(BatchRecord(host="claude"))`);
    a configured `30m` still wins; `90m` is still refused.
  - the Foreman's watcher (session key equal to the batch's `foreman_transcript`, through
    `watch_fakes.py`): a `merged@1`, a `checks-red@1` and a `wait-cleared@1` of its batch wake it
    and are printed; a `board@1`, a `config@1`, an `arrived@1` and another batch's `merged@1` move
    its cursor and print nothing; a seat naming another session does not end it; a record naming
    another Foreman ends it with its line; with no server it starts none and ends with its line.
  - `not_running_line`: in the Foreman's session, the `for the Foreman` line; in another session,
    today's line; `status` in the Chief of Staff's session prints `foreman watch: running` while
    a lock of the Foreman's session is held, `not running` otherwise.
  - the texts of `merged_text` and `red_text` say "for the steering session".
- Scenario (`scenario/run_scenario.py`, unit `surface-board`, with `README.md`): in a Foreman-mode
  batch, a watcher started under the Foreman's session key with A's seat held by another session
  subscribes, starts no board, and ends (or wakes, per `watcher-limit`'s shape) on A's merge with
  the `forge saw merged ... for the steering session: order merged <cr>` line; a board write in
  the same window is not printed by it; the Chief of Staff's `status` shows `foreman watch:
  running` while it runs.
- Host and default matrix:
  - Claude Code, shipped default: the Foreman wakes at 55 minutes (3300 s); unproved until the
    first batch's Foreman transcript shows it (row "Steering wake bound").
  - Claude Code, configured value (`session: steering_wake: 30m`): unchanged, proved.
  - Claude Code, the Foreman's watcher waking an idle Foreman session: unproved; trial in row "Run
    the watcher".
  - Copilot, shipped `4m` `/every`: unchanged; the Foreman's watcher: unproved, or none with one
    line when the host cannot run it, and the relay stays.
  - Direct mode, either host: unchanged.
- At the next batch's retro: the study's measure repeated and compared with batch-29 (above).

## Open questions

1. **Who records a user's merge in Foreman mode** (read here from "instead of having them
   relayed"): the Foreman, from its watcher (forge check, then `order merged <cr> --epoch <n>`),
   the Chief of Staff telling the user only, while the Foreman's watcher runs; or the Chief of
   Staff keeps recording and the Foreman's watcher wakes it only for the red CI and the wait met?
2. **The Suspect threshold** (a Driver with no activity for one heartbeat interval): does it follow
   the steering wake to 55 minutes, or stay at 30 minutes?
3. **The Foreman's watcher's end**: when the batch records another Foreman or closes, as written;
   and while the batch is paused with no Driver running, does it end with the heartbeat (as
   written) or keep running for a merge of a PR handed back ready?
4. **"30 to 55 minutes"**: a shipped default of 55 minutes with the 60-minute bound kept, as
   written; or should the CLI also refuse a Claude Code value below 30 or above 55?
