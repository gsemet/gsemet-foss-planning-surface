# Watcher runs through several events instead of exiting on each

Short name: `watcher-limit`. Read against main at 3c29dd7c.

## Goal

In the user's terms: while a batch runs, one watcher stays up and wakes the Chief of Staff at each
event, so the Chief of Staff does not start it again after every merge (about twenty times in
batch-30). The watcher no longer ends after 2 h with no event while a batch runs or is paused with
open PRs, so a long CI wait or the owner's merge pause does not take the board down (Studio
batch-09: four restarts by hand). With no such batch, the 2 h limit stays. The watcher always ends
when the project's seat is another session's (watcher-limit-Q1). The forge hub also reads the open
PRs of a paused batch, so a watcher kept alive on a pause sees the merge (watcher-limit-Q2).

## What the code does today (main 3c29dd7c)

- `skills/chantier/scripts/cli/src/chantier/hub/watch.py`, `Watch.poll`: returns `EVENTS` once
  `hub_times.quiet_s()` (20 s) has passed since the last new waking line and
  `events.wake_every` since the start; `IDLE` when no waking line came and
  `hub_times.idle_end_s()` (2 h) passed since the start; `SEAT` when `seat_moved`; `END` on a link
  failure. `run` then prints `Watch.lines(reason)` and the process exits, whatever the reason.
- `hub/times.py`: `IDLE_END_S = 7200.0`; `CHANTIER_HUB_TEST_TIMES` = `<cycle>:<quiet>[:<idle_end>]`.
- `hub/watch_lines.py`: `EVENTS_END` (`watch: {name} still running: ... start again in the
  background now: {watch}`) and `IDLE_END` (`watch: no event for {name} in 2 h; ended, so a session
  that has ended leaves no board running: ...`).
- `hub/autostart.py`: `watch_command(repo, n)` = `<cli> watch --after <n>`, used by
  `not_running_line`, both end lines and the board's lines; `detect_host()` (in `plugin_files.py`)
  already tells `claude` from `copilot` (`ChantierError` with no host).
- `hub/watch.py`, `open_batch`: the id of a batch `running` or `paused`. `hub/batch_prs.py`,
  `to_read(d)`: whether a CR has a PR the record holds neither merged nor cancelled.
- `hub/batch_prs.py`, `running_batch(repo)`: the batch of `4-batch/batch.json` when its status is
  `running`, else None ("a paused or closed one is not followed"). `BatchPrs.collect` returns the
  `pr` interests only for that batch and only when `to_read(d)`; `BatchPrs.judge` judges the read
  against it. `hub/waits.py`, `Waits.collect`, follows `batch_prs.running_batch` too. So a paused
  batch's PRs and waits are never read by the hub today.
- `hub/lines.py`, `watch_lines`: prints the hub's line in `status` only when `d.status ==
  "running"`.
- `declare/interests.py`, `HELP`: "the running batch's PRs or MRs, which the forge hub reads".
- `declare/watch.py`: the `watch` parser and its `HELP`, which states the 2 h end.

## What changes

### 1. The 2 h limit (watcher-limit-Q1, answer A)

- The idle end applies only while the project has no batch running and no batch paused with a PR
  the record holds neither merged nor cancelled. Call this "a batch in flight"; it is exactly the
  batch the hub follows (section 5): the watcher tests it with `batch_prs.followed_batch(repo) is
  not None`, so the watcher stays up exactly while the hub reads the PRs it waits for.
- The 2 h are counted from the latest of: the watcher's start, its last new line for it that
  wakes, and the last moment it saw a batch in flight. So a batch that closes, or pauses with its
  last PR merged, gives the watcher 2 h more from that moment, never an immediate end.
- `Watch.poll` reads the batch state at most every `SEAT_CHECK_S` (as it reads the seat), through
  `batch_prs.followed_batch` (which reads `4-batch/batch.json` with `read_batch_json`), an
  unreadable file counting as no batch in flight.
- The seat end (`SEAT`) and the link-failure end (`END`) are unchanged and apply in every state.
- `IDLE_END`'s text keeps its words (`no event for {name} in 2 h; ended, ...`); `{name}` is the
  project's `(no batch)` form or the closed or paused batch's id, as `open_batch` gives today.

### 2. Running through several events (the request's intent)

- New flag `watch --stream` (in `declare/watch.py`, with a help line; refused with `--once`,
  exit `EXIT_USAGE`, one line `watch: --stream and --once do not go together`).
- With `--stream`, at the point where the watcher would end with `EVENTS`, it prints instead the
  block of events gathered (each with `told(e)`, the arrivals marked through
  `arrival_mark.tell_arrivals`, as `Watch.lines` does), then one closing line, a new constant
  `STREAM_TOLD` in `watch_lines.py`:
  `watch: {name} told up to cursor {n}; still watching (if this watcher stops, start again: {watch})`
  printed in one write with `flush=True`, then empties its gathered events, clears `last_new` and
  goes on polling. The next block comes no sooner than `events.wake_every` after the previous one.
- With `--stream`, it ends only on `SEAT`, `IDLE` (section 1) or `END`, with the same last lines
  as today, each still naming the restart command.
- Without `--stream`, the behaviour is today's: it ends with `EVENTS_END` after the first block
  (the Copilot form, and any run without a host).
- `autostart.watch_command(repo, n)` appends ` --stream` when `detect_host()` is `claude`, and
  not for `copilot` nor when no host is known. Every line that names the watcher's command
  (`not_running_line`, `EVENTS_END`, `IDLE_END`, `STREAM_TOLD`, `BAD_KEY`, `REFUSED`, `NOT_SERVED`,
  `NO_SEAT`, `NO_TRANSCRIPT`, `UNREADABLE_SEAT`) carries the host's form, so the cards' "run the
  printed command as is: no flag added" holds. `pull_command` is unchanged.
- The docstrings of `hub/watch.py` and `hub/times.py` (`IDLE_END_S`'s comment) and `HELP` in
  `declare/watch.py` say the new end rule and the stream form.

### 3. AGENTS.md: the sentence on the watcher's end and its orphan guarantee, and the hub's

The exact text replaced, in the forge hub bullet (lines 157 to 160 at 3c29dd7c), from "and ends"
to "stops);":

> and ends 20 s after the last new event for it that wakes, and no sooner than `events.wake_every`
> after its start, which wakes its session, or when the project's seat is another session's, or
> 2 h after its start with no event for it that wakes (so a watcher an ended session left behind
> stops);

The new text:

> and, 20 s after the last new event for it that wakes and no sooner than `events.wake_every`
> after its start or its last telling, tells the events it gathered, which wakes its session: in
> its streaming form (`watch --stream`, which the CLI prints on a host whose reference runs it so)
> it prints them and runs on, else it ends; it ends when the project's seat is another session's,
> and, while no batch of the project runs and none is paused with a PR the record holds neither
> merged nor cancelled, 2 h after the latest of its start, its last event for it that wakes and the
> last moment such a batch ran or was paused so (so a watcher an ended session left behind stops
> once the seat moves, or 2 h after its batch is done);

The hub sentence (watcher-limit-Q2), in the same bullet (lines 148 to 153 at 3c29dd7c), from
"those: today," to "(`wait-cleared@1`)":

> those: today, the PRs of a project's running batch while one of them is not held merged or
> cancelled, and the PRs or MRs that the open approval, pipeline and merge waits of the running
> batch's CRs name, in the same query; it appends to that project's `forge-journal.jsonl` (planning
> folder, never published) one line per merge the record does not hold, per CI turning red on
> a PR ready to merge and per wait of a running batch's CR that the forge shows met
> (`wait-cleared@1`)

The new text:

> those: today, the PRs of a project's batch that runs, or is paused with open PRs, while one of
> them is not held merged or cancelled, and the PRs or MRs that the open approval, pipeline and
> merge waits of that batch's CRs name, in the same query; it appends to that project's
> `forge-journal.jsonl` (planning folder, never published) one line per merge the record does not
> hold, per CI turning red on a PR ready to merge and per wait of that batch's CR that the forge
> shows met (`wait-cleared@1`)

And the `interests` sentence of the same bullet (lines 173 to 174), which the widening would
otherwise make false: "(the running batch's PRs or MRs, read by the forge hub," becomes "(the PRs
or MRs of the batch that runs or is paused with open PRs, read by the forge hub,".

The hub's cadence sentence ("at most once every 20 s while at least one client is subscribed ...
`--forge-always` ...") is unchanged. Nothing else in AGENTS.md changes (the watcher stays the Chief
of Staff's; the Foreman-wake CR rewrites that).

### 4. The cards and the docs

- `skills/chantier/references/hosts/claude-code.md`:
  - Row "Run the watcher" (line 55): the means becomes the `Monitor` tool, in its form with no
    timeout, with the command the `watch: not running` line prints, as is (it ends with
    `--stream`); each notification (a block of event lines ending with the `still watching` line)
    starts a turn of the idle Chief of Staff session; the monitor's end (its last line: seat, 2 h,
    or a board it cannot link) starts one too. Status: unproved; trial: a batch with two merges and
    one watcher, the Chief of Staff's transcript showing two notifications, two forge checks and
    two `order merged`, no watcher started between them, no user message between. Say that
    auto mode drops every `Monitor` allow rule (the section "What not to add"), so the start is the
    classifier's call. Keep the row's other trials (the `config@1` line, the detached board), with
    "its end" read as "its notification". The `no event for <name> in 2 h` line keeps its rule
    (start again at once, nothing told).
  - Row "The watcher when the session ends" (line 56): an orphaned watcher ends once the project's
    seat is another session's, or, with no batch in flight, 2 h after its last event or after its
    batch is done (the CLI); while a batch is in flight it runs until the seat moves (accepted,
    watcher-limit-Q1); the board it observed stops 30 minutes after it ends.
  - Row "Name the holders..." (line 39): "a running watcher task" reads "a running watcher task (a
    monitor or a shell)".
- `skills/chantier/references/hosts/copilot.md`, row "Run the watcher" (line 47): the CLI prints
  no `--stream` there; the watcher keeps ending after each block, started again from its last line;
  the `2 h` sentence follows section 1 (no 2 h end while a batch is in flight).
- `skills/chantier/references/chief-of-staff.md`, or, once CR-471 has merged, the piece that holds
  its "While it runs" table and "The watcher" item (CR-471's `chief-of-staff:steering` action):
  - The "While it runs" row "a watcher's end" (line 33) becomes "a watcher's notification or end":
    act on each line as in The watcher; a `still watching` line needs no restart; a
    `still running` or `no event for <name> in 2 h` last line names the restart, run as is.
  - "The watcher" item (lines 1540 to 1623): the end rule as in section 1 and 2; "A watcher's end"
    reads "A watcher's notification or end" (the same handling of each line), and "start the
    watcher again from its last line" applies only when the watcher ended (its last line is not
    `still watching`). "Never: start a second watcher in the same session while one runs" stays
    and covers a running monitor.
- `skills/chantier/references/session-start-chief-of-staff.md`, "The watcher" (lines 83 to 120):
  the question's explanation says the watcher runs on in the background and tells within about
  20 s (unchanged words), and the `no event for <name> in 2 h` bullet names when it comes (no
  batch in flight).
- `skills/chantier/references/concepts.md` line 776: "stops itself (at its end, 2 h after its
  start with no event, ...)" becomes "stops itself (after each block in its plain form, after 2 h
  with no event and no batch in flight, or when the seat is another session's)"; "started again
  after each end" stays.
- `docs/web-board.md` line 238: "A watcher ends by itself 2 h after its start with no event" says
  the section 1 rule.

### 5. The hub and a paused batch (watcher-limit-Q2, answer A)

- `hub/batch_prs.py`: `running_batch(repo)` is replaced by `followed_batch(repo)`: the batch of
  `4-batch/batch.json` when its status is `running`, or `paused` with `to_read(d)` true; None for a
  closed batch, a paused one with no PR left open, no file or an unreadable one. Its docstring and
  the module's say "the running batch, or a paused one with open PRs". `BatchPrs.collect` and
  `BatchPrs.judge` call it; the rest (`state_of`, `events_of`, the `merged` and `checks-red`
  events, `apply_batch_settings`) is unchanged, so a paused batch's merge gives the same
  `merged@1` line (`source: hub`) as a running batch's, once, and the board's PRs page and the hub
  still share the journal line.
- `hub/waits.py`: `Waits.collect` calls `batch_prs.followed_batch`; the module docstring says "the
  waits of the followed batch's CRs (running, or paused with open PRs)". So a paused batch's open
  approval, pipeline and merge waits are read in the same project query while one of its PRs is
  open, and give `wait-cleared@1` as today; once every PR of the paused batch is merged or
  cancelled, neither its PRs nor its waits are read.
- `hub/lines.py`, `watch_lines`: the hub's line prints for the batch the hub follows (running, or
  paused with open PRs), so `status` on such a paused batch says whether the hub reads it; its
  docstring follows.
- `declare/interests.py`, `HELP`: "the PRs or MRs of the batch that runs or is paused with open PRs,
  which the forge hub reads"; `chantier interests` lists them through the same providers.
- `docs/web-board.md` line 228: "only the PRs a running batch waits for" becomes "only the PRs a
  running batch, or a paused one with open PRs, waits for".
- Unchanged: the server's own batch-PR read for a client (AGENTS.md's first exception, its own
  10 s rule), the hub's cadence and `--forge-always`, the issues provider (never read by the hub).

## Files the CR touches

CLI: `skills/chantier/scripts/cli/src/chantier/hub/watch.py`, `hub/watch_lines.py`,
`hub/times.py`, `hub/autostart.py`, `hub/batch_prs.py`, `hub/waits.py`, `hub/lines.py`,
`declare/watch.py`, `declare/interests.py`. Tests:
`skills/chantier/scripts/cli/tests/test_watch_events.py`, `tests/test_watcher_autostart.py`,
`tests/forge_world.py`, `tests/test_forge_hub.py`, `tests/test_forge_hub_waits.py`.
Scenario: `scenario/run_scenario.py` (step 16d). Cards: `hosts/claude-code.md`,
`hosts/copilot.md`, `chief-of-staff.md` (or CR-471's piece), `session-start-chief-of-staff.md`,
`concepts.md`. Docs: `docs/web-board.md`. Root: `AGENTS.md`.

## Overlaps and order

- CR-471 (`slim-the-startup-cards-of-the-three-role`, active in batch-31) cuts
  `chief-of-staff.md` into pieces: this CR starts after it merges and edits the piece that holds
  "The watcher" and the "While it runs" table.
- `foreman-wakes-on-events-at-worst-every-5` (`foreman-wake`) comes after this CR: it reuses the
  stream form for a Foreman's watcher and rewrites AGENTS.md's rule that the watcher is the Chief
  of Staff's; this CR does not touch that rule.
- `uv-sync-blocked-by-the-running-board-and` (`board-restart`) shares the watcher's start and stop
  (`session-start-chief-of-staff.md`, AGENTS.md's forge hub bullet, `hosts/claude-code.md` line 39
  "Own" reading): ordered with this CR, never in the same batch's parallel slots; the second rebases
  on the first.

## Out of scope

- The second half of the inbox item `watcher-ends-after-2-h-with-no-event-don` (removing
  junctions and symlinks from a CR's work folder at the move to done): it stays in that item.
- The "slow heartbeat" the inbox item proposed: watcher-limit-Q1 sets no limit while a batch is in
  flight, with no heartbeat.
- A streaming form on Copilot (no host means proved for it); the pull path; the board's own 30
  minute stop; the hub's cadence; the server's per-client batch-PR read; a closed batch's PRs.

## Host and default matrix

- Claude Code, shipped `events.wake_every: 20s`: `watch --stream` through `Monitor`, one
  notification per block, at most one per 20 s.
- Claude Code, configured `events.wake_every`: the same, at most one block per configured window.
- Copilot (either value): plain `watch --after <n>`, ends after each block, started again from its
  last line; pull path at each user message until its row's trial is recorded.
- No host known (a bare terminal): plain form, as Copilot.
- The hub's read of a paused batch depends on no host: a board with a subscribed client (either
  host's watcher, a page, `chantier live`) reads it at most every 20 s; a board started with
  `--forge-always` (a host that cannot run the watcher) every 20 s with or without a client.

## Evidence

- `test_watch_events.py`, parametrized (the existing `ENDS` table driving `Watch.poll` on a
  monotonic `t`, with `CHANTIER_HUB_TEST_TIMES` giving a short third field for the idle end):
  - stream: two waking lines 40 polls apart give two blocks, each ending with the `STREAM_TOLD`
    line naming the cursor, and no end; a seat moved after them ends it with `SEAT_LINE`;
  - idle, one row per state: batch running, paused with an open PR, paused with every PR merged,
    paused with no PR, closed, no batch: no `IDLE` for the first two within several idle periods,
    `IDLE` after one period for the others;
  - a batch going from running to closed during the run: `IDLE` one idle period after the change,
    not after the start;
  - without `--stream`, the existing rows keep their expected ends (`EVENTS_END`).
  - `--stream --once` is refused with its line and `EXIT_USAGE`.
- `test_watcher_autostart.py`: `watch_command` with `CHANTIER_HOST=claude` ends with `--stream`,
  with `copilot` and with no host it does not; `not_running_line` carries the same form.
- The hub and a paused batch, on the fake forge world (`forge_world.py`):
  - the fixture: gamma's paused batch holds no PR left open (`crs_of("gamma", "cancelled")`), so
    `CALLS = 2` and the tests that count calls keep their meaning; the comment of
    `test_a_hub_cycle_reads_only_what_there_is_to_read_and_is_due_every_twenty_seconds` reads
    "gamma is paused with no PR left open";
  - `test_the_hub_never_collects_the_issues_provider`: alpha and beta are written paused with
    `crs_of(name, "merged")`, so no PR is read and the test still proves the issues are never
    read;
  - a new test, parametrized on the paused batch's CRs (one PR open; every PR merged; every PR
    cancelled; no PR): one cycle reads that project's PRs in one call for the first row only;
    with the forge showing the open PR merged, the next cycle appends one `merged@1` line
    (`source: hub`) to that project's journal, and a third cycle none;
  - in `test_forge_hub_waits.py`, a new row: a paused batch with one PR open and a met `merge`
    wait on it gives one `wait-cleared@1` line, in the same one call per project and cycle;
  - `followed_batch` drives `Watch.poll`'s idle rows above (the same states), so the watcher's
    "batch in flight" and the hub's followed batch are tested as one rule.
- `scenario/run_scenario.py`, step 16d: one `watch --stream` watcher (quick times) through two
  merges the hub sees, printing two `forge saw merged` blocks each closed by `still watching`, the
  process still alive after the second; then the batch is paused with one PR open, the forge shows
  it merged and the watcher prints a third `forge saw merged` block (the hub read the paused
  batch), still alive past the quick idle end; then a seat taken by another session ends it with
  the seat line.
- `just check`, `just eval-dry-run` (a change under the CLI's `src/`), and the long gate `just
  scenario (ubuntu-latest)` green at the PR's head.
- Cost: the PR's Deliverables state the baseline measured in batch-30 (about twenty watcher
  restarts by the Chief of Staff, one per merge) and in Studio batch-09 (four board restarts by
  hand); the Claude Code row's trial, run in the first batch after the merge, records the count of
  watcher starts in that batch next to its merges.
- Cost of the hub's paused-batch read: a paused batch's PRs and waits join the project's one query,
  so the forge is read at most once every 20 s while a client is subscribed (and every 20 s with
  `--forge-always`), as for a running batch, one call per project and cycle; none once every PR of
  the paused batch is merged or cancelled. The new hub test asserts the one call; the
  Deliverables say it.
