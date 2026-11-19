# Change Specification: addressed events, one typed journal that says whom to wake

No tracker issue: the CR is verbal (the user, 2026-11-18, during batch-28; drawing:
`../surface-server-one-elected-process-for-t/intake/architecture.svg`, the "Event log and router"
box). Checked against `main` at `7ee43d0d`.

**Stacks on** (`depends.json`) CR-383 `config-spec-writers-slots`
(`4-batch/1-pending/383-spec-writers-and-slots-set-from-the-boar`) and CR-384
`session-events-board-griller` (`4-batch/1-pending/384-session-events-board-griller`), and through
CR-384 on CR-375 `watcher-autostart`. Read their `03-change-spec.md`: this CR generalizes the lines
they add (`config`, `board`) and the watcher as they leave it (no batch needed, `--once`, the seat
end, CR-375's session key, lock and printed commands). The surface server CR
(`1-inbox/surface-server-one-elected-process-for-t`) stacks on this one.

## Goal

The user: "Don't do all of that, but let us lay solid bases to allow it later." Later, one server
in front of the watchers will route each event to the right session (the Chief of Staff, a
Foreman, a Driver, the user) and spare a costly Chief of Staff turn. The base laid now: every event
is one typed, versioned line in one journal per project, which says whom it is for, and a watcher
wakes only on the events for it, with its wake rules (buffer, filter, rate limit) in one place.
Today's behaviour does not change: every line written today is for the project, so the Chief of
Staff's watcher, started by today's printed command, wakes on exactly what wakes it today.

Built: the line, its audience, the watcher's filter and rate limit, the reading of today's lines.
Not built: any routing to a role, a CR or the user, any new audience's watcher, user
notifications, delegated actions, any new forge read.

## Decisions carried (from `02-answers.md`)

| Answer | Decision | Where below |
|---|---|---|
| 1. Scope | A foundation only: the line, its audience, the watcher's filter and wake rules, the reading of old lines. No Foreman or Driver watcher, no user notification, no delegated action, no new forge read | Out of scope |
| 2, 11. One journal per project, its name | The one journal stays `forge-journal.jsonl` in the planning folder, never published, holding the hub's lines and CR-383's and CR-384's: no move, no second file. Only the line's format changes; an old line reads as version 0. The docs say the name is historical | 1, 2, 6 |
| 3. The line | `v`, `seq` (the cursor counts it), `t`, `kind` (today's: `merged`, `checks-red`, `config`, `board`), `source` (`hub`, `board`, `cli`), `audience`; payload fields per kind, unchanged | 1 |
| 4, 9. The audience | Values `project`, `role:<name>`, `cr:<id>`, `session:<key>`, `user`; no audience is the project. Every line written today carries `["project"]`. No role name in the code or the defaults: the CLI checks a value's form only; the later CRs add their routing with their watchers. No new AGENTS.md exception | 1, 3 |
| 5, 9. Wake rules in one place | A watcher subscribes to `project` plus its own session; `watch --for ...` adds audiences; no `--for` is today's command. The 20 s quiet is the buffer; the filter by audience; the rate limit `events.wake_every`, default 20 s, the one configurable key | 3, 4 |
| 6. Writers | The forge hub, the board's PRs page, Configuration page and backlog writes all write through `hub.journal.append`; no second writer path | 2 |
| 7. Order | After CR-383 and CR-384; the surface server CR stacks on this one | Above |
| 8, 12. Docs and texts | `docs/planning-folder.md` gets the line's reference; the Chief of Staff's card (its watcher line, outside its Startup core), AGENTS.md and CONTRIBUTING.md state the new end rule; the PR names the AGENTS.md change | 6 |
| 10. A configuration problem | The watcher refuses only on a problem in its own `events` block; any other problem it names in its start line and runs | 3 |
| 13. No name collision | The configuration reader is `read_wake_rules`, not `read_events` (`core/records.py` has that name) | 4 |

## What changes

`cli/` is `skills/chantier/scripts/cli/`, `chantier/` is `cli/src/chantier/`. Every path is in
chantier's repository. Everything below is as CR-383, CR-384 and CR-375 leave it.

### 1. The event line (`chantier/hub/journal.py`)

The module stays the journal's one module (the surface server CR may move it; not this one). Its
docstring and `chantier/hub/__init__.py`'s become the reference of section 6 in short.

- `FILE = "forge-journal.jsonl"`, unchanged (the name is historical: the file holds every event of
  the project, the forge's and the board's). `KINDS = ("merged", "checks-red", "config",
  "board")`; `SOURCES = ("hub", "board", "cli")`; `VERSION = 1`.
- **A version 1 line**, one JSON object, fields in this order:

  ```json
  {"v": 1, "seq": 41, "t": "2026-11-18T10:02:03Z", "kind": "merged", "source": "hub",
   "audience": ["project"], "batch": "batch-29", "cr": "CR-12", "pr": "#88", ...}
  ```

  - `v`: the line's version, `1` here.
  - `seq`: 1 for the first line, then the highest readable `seq` plus one (today's rule); the
    watcher's cursor counts it.
  - `t`: the time of the append (`clock.now()`, today's).
  - `kind`: one of `KINDS`. `checks-red` keeps its name (answer 3's `ci-red` is an example; renaming
    it would change how old lines read).
  - `source`: who wrote it. `hub` (the forge hub's cycle), `board` (the PRs page, the Configuration
    page, the backlog writes), `cli` (a CLI command; no writer of it today, the value is room for
    the next).
  - `audience`: a list of one or more audience values (below). Written on every version 1 line;
    every writer of today writes `["project"]`. A line with no `audience`, or an empty one, is for
    the project.
  - The payload: each kind's fields, unchanged: `merged` and `checks-red` as on main, `config` as
    CR-383 and CR-384 write it (`key`, `old`, `new`, `batch`), `board` as CR-384 writes it
    (`action`, `items`, `text`, `wakes`).
  - `by` is no longer written: `source` takes its place.
- **Audience values** (a string each; `<name>`, `<id>` and `<key>` match `[A-Za-z0-9-]+`):

  | Value | For | Written today |
  |---|---|---|
  | `project` | every watcher of the project | by every writer, on every line |
  | `role:<name>` | the watchers that subscribe to `role:<name>` | no |
  | `cr:<id>` | the watchers that subscribe to that CR (its Driver, later) | no |
  | `session:<key>` | the one session whose key (CR-375's, `own_transcript(detect_host())` kept to `[A-Za-z0-9-]`) it is | no |
  | `user` | the user must act (a notification, later) | no |

  The CLI checks a value's form, never what it names: no role name is in the code, the defaults
  or a test fixture of the shipped files. A later CR that routes to a role, a CR or the user adds
  that routing with its watcher.
- **Reading a line** (`read`, one function, for every reader): a line with no `v` is version 0,
  today's line: its source is its `by`, its audience is the project. It is never rewritten. A line
  whose `v` is above `VERSION` counts for `seq` (the cursor passes it) but is told by no one and
  wakes no one; `status` names it (section 5). An unreadable line is skipped, as today. `read`
  returns each entry with its effective `source` and `audience` filled, so no reader looks at `by`
  or `v` itself.
- `_key` (dedup), `event_text`, `merged_text`, `red_text`, `lines()` (the `status` lines): as CR-384
  leaves them; the audience does not enter the dedup key (a `merged` line by the board and one by
  the hub stay one line).

### 2. One writer path

- `append(repo, events, source)` is the one function that writes the journal (answer 6). It takes
  `source` in place of `by`, refuses (a `ValueError`, a code fault) a `source` outside `SOURCES`, a
  `kind` outside `KINDS` or an audience value of a wrong form, and writes `v`, `seq`, `t`, `kind`,
  `source`, `audience`, then the payload. An event that carries no `audience` is written with
  `["project"]`. It reads no configuration.
- The writers, each calling `append` and nothing else, none passing an audience today:
  `chantier/hub/cycle.py` (`"hub"`), `chantier/board/prs.py` (`"board"`), CR-383's and CR-384's
  `chantier/board/config_api.py` and `chantier/board/write_api.py` (`"board"`). No other module
  opens `FILE` for writing (a structure test, Evidence).
- The file keeps its name and its place: no move, nothing new in `core/files.py` `IGNORED` or
  `board/fingerprint.py` `SINGLE`. Old lines and new ones live in the same file, `seq` continuing,
  so a cursor held by a running watcher stays true. A board or a hub of an older chantier still
  running writes version 0 lines there, which this version reads as for the project: nothing is
  lost during an upgrade.

### 3. The watcher's filter (`chantier/hub/watch.py`, `chantier/declare/watch.py`)

```
chantier watch [--after SEQ] [--for AUDIENCE ...]
chantier watch --once --after SEQ [--for AUDIENCE ...]
```

- **Its subscription**: `project`, its own `session:<key>` when its key is not `none`, and each
  `--for` value (repeatable, one audience value each; `project` and its own session given again
  are taken once). No `--for` is today's command: the printed commands (`watch_command(repo, n)`,
  CR-384's pull path) do not change, and since every line today is for the project, they wake on
  what they wake on today.
- **A line for it**: its audience holds a value of the subscription. Only lines for it are printed
  at its end and only those wake it (CR-384's `wakes: false` rule for a `board` line kept: for it,
  carried, printed at the next end, never starting or extending the wait). A line not for it is
  passed: the cursor moves past it, it is never printed, it neither starts nor extends the wait.
  The end's `next` command carries the cursor of the last line read, whoever it was for.
- `--once` filters the same way.
- **Start line**: `watch: <project> from cursor <n> for <values>` (the subscription, `project`
  first, then the session, then the `--for` values in their order), then today's and CR-384's
  clauses (`, the hub`, `; hub is chantier <v>`, the board's version).
- **Refusals**, nothing written, no lock taken:
  - a `--for` value of a wrong form (`EXIT_USAGE`):
    `watch: --for "<v>": one of project, role:<name>, cr:<id>, session:<key>, user`;
  - a problem in the `events` block of any layer (`EXIT_PRECONDITION`):
    `watch: <the problem, with its file and line>: fix it, then start the watcher again`.
- **Any other configuration problem** (answer 10) stops nothing: the watcher runs, with its rules
  read from the `events` block, and its start line ends with `; configuration: <the first problem,
  with its file and line>` (one problem, the first that `playbook` would print).
- The help text names the audience, `--for` and the end rule.

The forge hub's cycle does not change: the watcher that is the hub writes every project's events,
whatever its own subscription.

### 4. Wake rules in one place (`config/chantier.defaults.yml`, `chantier/playbook/`)

The wake rules are the watcher's own (section 3) and this one key; no other module decides a wake.

- **Shipped defaults**, a new top-level block with a one-line comment:

  ```yaml
  events:
    wake_every: 20s   # a watcher ends no sooner than this after its start (one wake per window)
  ```

- **The buffer** is today's quiet, unchanged: a watcher ends `quiet_s()` (20 s, `hub/times.py`,
  the `CHANTIER_HUB_TEST_TIMES` seam kept) after the last new line for it that wakes. Not
  configurable (answer 5 makes the rate limit configurable, not the buffer).
- **The rate limit** `events.wake_every`: a watcher ends no sooner than this after its own start.
  The session starts it again right after an end, so this keeps one wake per watcher per window
  with no state on disk. With the shipped 20 s and the 20 s quiet, no watcher ends sooner than it
  does today. Under `CHANTIER_HUB_TEST_TIMES`, `hub/times.py` caps it at the test's quiet, so the
  scenario keeps its short times.
- **Checks** (`chantier/playbook/config.py`, the way `long_gate` is checked; `events` joins the
  known top-level keys and the unknown-key message's list):
  - `events: unknown key "<k>": one of wake_every`;
  - `events: "wake_every" is <whole number><s|m|h>, 20s or more, found "<v>"` (the form of
    `timing_check._DURATION`; 20 s is the quiet, below it the limit changes nothing);
  - `default` takes the key back to the weaker layer, as for every key.
  These are the "problems in the `events` block" that section 3 refuses on; the checks tag each
  problem with its block so the watcher can tell them from the others.
- **Reading**: `chantier/plugin_files.py`, `read_wake_rules(repo)` next to `read_timing` (not
  `read_events`, which `core/records.py` has), resolving `events.wake_every` through the user
  layers, strongest first, then the shipped file, as CR-383's `read_limits` does. It returns the
  value with its layer, the problems of the `events` block, and the first other problem. With no
  plugin root and no user layer setting the key: no value, no rate limit beyond the quiet (as
  CR-383's rule for a key with no value: the CLI holds no value of its own).
- `chantier playbook` prints one `events:` line after CR-383's `limits:` line, with the playbook's
  label rule (no label for a shipped value, `[<layer>]` otherwise): `events: wake every 20s`, or
  `events: wake every: not set`.

**How this stays within "the CLI knows no role"** (answers 4 and 9): no role name is written, read
or defaulted anywhere; `role:<name>` is a form the CLI checks and a string it matches. AGENTS.md
gets no new exception. A test keeps it so (Evidence).

### 5. `chantier status` (`chantier/commands/batch_status.py`)

- `_seen_lines` reads through `journal.read` (both versions) and names, with `journal.FILE` in its
  text: an unreadable line (today's), and a line of a newer version: `forge-journal.jsonl: line <n>
  is version <v>, newer than this chantier: update it`.
- What `status` prints from the journal is otherwise CR-384's (`merged`, CR-383's `batch.slots`
  line), for every audience: `status` is the Chief of Staff's and the Foreman's report, not a
  watcher.

### 6. Docs, AGENTS.md, CONTRIBUTING.md, the card

The end rule, in the same words everywhere (answer 12): the watcher ends 20 s after the last new
event for it, and no sooner than `events.wake_every` after its start.

- **`docs/planning-folder.md`**: a section "The event journal": `forge-journal.jsonl`, never
  published, its name historical (it holds every event of the project, not only the forge's); the
  line's fields (section 1's tables); today's kinds, their sources and payloads, all for the
  project; the version 0 reading; `watch --for`, the end rule and `events.wake_every`. ~line 49's
  list of local files is unchanged.
- **`skills/chantier/references/chief-of-staff.md`**, "The watcher" bullet (~line 1228, in "While
  it runs", outside the card's Startup core, as CR-375 and CR-384 leave it): "ends 20 s after the
  last new one" becomes the end rule above, with "for it" and `events.wake_every`. No other card
  changes: the printed commands do not change.
- **`AGENTS.md`**, the CLI's scope bullet, the forge hub's exception: "each session's watcher reads
  only its project's journal, never the forge, and ends 20 s after the last new event, which wakes
  its session" (as CR-384 leaves it) says the end rule above. The journal's name is unchanged. No
  new exception (section 4). The PR's description names this change.
- **`CONTRIBUTING.md`** (~line 116, its mirror of that text): the same, in its own words.
- `scenario/README.md`: the new checks with their unit.

## Out of scope

- Any routing to a role, a CR, a session or the user: no writer of an audience other than
  `project`, no `events.watch` or `events.audience` key, no role name; the later CRs add them with
  their watchers.
- A watcher for a Foreman, a Driver, a Griller or the user; the `cli` source's first writer.
- User notifications, delegated actions, a new forge read (reviews, ready PRs).
- One writer process, the election of a surface server, the read interface, an index: the surface
  server CR's.
- Renaming or moving the journal; rewriting, converting or merging old lines.
- Making the 20 s quiet or the hub's 20 s cycle configurable.
- A change to `event_text`, the dedup keys, the `status` lines' choice, `board-journal.jsonl`,
  `STATUS.md`, `STATUS.json`, the CR board pane, `hooks/`, `types/`, `board/web/`.
- A version bump.

## Host and default matrix

The host does not change the line or the filter. The cells differ by where `events.wake_every`
comes from and by the configuration's state. Each is proved through a real flow (a hub cycle or a
board write through `append`, then `chantier watch` / `playbook`); the shipped value is read from
`config/chantier.defaults.yml` at the head under test, never copied into a test.

| Source | `watch` (no `--for`) | `playbook` `events:` |
|---|---|---|
| shipped default (20s) | subscribes `project, session:<key>`; ends 20 s after the last event, as today | `wake every 20s`, no label |
| surface project `chantier.yaml` sets `events.wake_every: 2m` | ends no sooner than 2 min after its start | `[surface project]` |
| repository `chantier.yaml` sets it | the same, the repository's value | `[repository]` |
| no plugin root, no user layer | no rate limit beyond the quiet | `wake every: not set` |
| a problem in an `events` block | refused, exit 3, names the problem | the problem |
| a problem elsewhere (for example in `hosts`) | runs; its start line names the problem | the problem |

## Evidence

**Gates.** A change under the CLI's `src/` and a card: before the first push, `just check` and
`just eval-dry-run` in the worktree at the rebased head; before the PR, the pipeline's
`just scenario (ubuntu-latest)` job green at its head, and the local `just scenario`
(`chantier gate`) when this CR is the top of its batch. No `hooks/` or `types/` change (no
`just mod`), nothing under `board/web/` (no `DESIGN.md`), no pane change (no screenshot).

**Unit tests** (`cli/tests/`, in-process, few, parametrized, injected clock, no sleep; `just test`
within its budget), mostly in `test_forge_hub.py`:

- The line: an `append` from each source writes `v: 1`, `seq`, `t`, `kind`, `source`,
  `audience: ["project"]` first, the payload unchanged, no `by`; a `source`, a `kind` or an
  audience value outside its form raises.
- Version 0: a prepared old line (`by`, no `v`; a case today's writer can no longer produce) in the
  same file reads with its `by` as source and `["project"]`, wakes a watcher, and the next
  `append` continues its `seq`. A `v: 2` line: the cursor passes it, no watcher prints it or wakes
  on it, `status` names it.
- The filter (parametrized, with prepared lines for audiences no writer produces today, named as
  such): a `project` line ends every watcher; a `role:x` line ends a `--for role:x` watcher and not
  the default one; a `session:<own key>` line ends only that session's watcher (key from the
  host's environment variable); a line not for it moves the cursor and is not printed; `--once`
  filters the same; the start line lists the subscription; a bad `--for` is refused with nothing
  written.
- The rate limit: `wake_every` 60 s, an event at 0 s ends the watcher at 60 s, not 20 s; at the
  shipped 20 s, read from the shipped file, today's end times hold
  (`test_a_watcher_ends_twenty_seconds_after_the_last_event` unchanged).
- Configuration problems: a bad `events.wake_every` refuses `watch` with exit 3; a bad `hosts`
  value leaves `watch` running with the problem in its start line.
- Config checks: accepted forms, each refusal's exact text, `default`, the unknown-key list; the
  shipped defaults file, read from the repository at the head under test, holds
  `events.wake_every` and passes the checks.
- Role-free: no file under `chantier/` and no line of `config/chantier.defaults.yml` holds
  `role:` followed by a name; and no module but `hub/journal.py` opens `FILE` for writing (one
  writer path).
- The card's watcher line, read from `skills/chantier/references/chief-of-staff.md` as it ships,
  states the end rule (`for it`, `events.wake_every`) and lies outside its Startup core.

**Scenario** (`scenario/run_scenario.py`, units `surface-board` and the forge hub's; README
bullets; `test_scenario_coverage.py` passes):

- The existing journal checks (~lines 1593-1830) hold, the file's name unchanged; the lines they
  read carry `v`, `source` and `audience: ["project"]`.
- A journal holding version 0 lines from before: a board merge appends a version 1 line after
  them; the watcher started with the printed `--after` prints the merge and nothing twice.
- Two watchers on demo: the printed default one and `watch --for role:griller`: a forge merge (for
  the project) ends both with its line.
- `events.wake_every: 2m` set in demo's surface `chantier.yaml` under the test times: `playbook`
  prints it with `[surface project]` (the cap of section 4 keeps the end short).
- Windows: the same units on the user's machine at the local gate.

## Known gaps (for the PR)

None of its own: the line's routing is unproved by design until a later CR writes an audience
other than `project`.

## Open questions

None: every point the answers left to the spec (the keys, the reader's name, the start line's
problem clause) is settled above within them.
