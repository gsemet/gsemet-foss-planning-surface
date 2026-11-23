# chantier live: Rich tables, local dates, Agents and Ready boxes

Short name: `live-rich`. Destination: the running batch batch-31. Owner's words of 2026-11-23
(`intake/request.md`), grilled in `02-answers.md` (live-rich-Q1 to Q5).

## Goal

The owner runs `chantier live` and finds it plain ("en ASCII"): he wants real tables with colours,
the date beside each event's time, a key that switches the times to "how long ago", the Agents in a
box of their own that lists the sessions really at work, and a Ready box, above Tasks, with the PRs
or MRs ready to review or to merge, each with its state in the web board's colours and a link he can
click where the terminal allows.

## What the code does today (read for this spec)

- `chantier live` is already drawn with Rich (`clients/tui/screen.py`): `Table.grid` columns with
  no header, `box.SQUARE` panels, one bold count line, no colour. The "ASCII" look the owner saw is
  this monochrome, headerless grid, not a missing dependency.
- **Rich is not a new dependency.** `pyproject.toml` already pins `rich==15.0.0` and
  `blessed==1.53.0`, both in `[tool.ruff.lint.flake8-tidy-imports] banned-module-level-imports`
  (they load inside the functions that draw, when `live` runs), and `uv.lock` holds them. The
  `uvx --from <plugin root> chantier` and `uv run --no-sync --project` launches are unchanged; no
  `pyproject.toml` or `uv.lock` edit is part of this CR. `tzdata==2026.2` is already a dependency
  too (the zone database on Windows).
- **The `none` in Agents (live-rich-Q1's check).** `Model.agents()` (`clients/tui/model.py`) lists
  one `Driver <cr> <phase>` per CR in state `working` of a running batch and `Stack driver` while
  `stack_lease` has not ended, and nothing else. Preflight P14 at the same moment reported
  "batch-20 running, steering direct, 0 Drivers" (`core/surface_batches.py`, which counts
  `rails.held` plus the stack agent). With no CR working and no stack lease, `none` was the code's
  right answer, not a reading bug; but the list left out the steering session and the Chief of
  Staff, so a batch steered by a live session showed no agent at all. The fix is the wider list
  below (live-rich-Q1). The okf-schema batch-20 record itself is no longer on the surface to read
  again; the conclusion rests on the code and P14's line.
- **The time gap (live-rich-Q2's check).** Every time the screen shows is UTC: the header prints
  `Model.now()` (the server's `now`, `%Y-%m-%dT%H:%M:%SZ`) as `HH:MM:SS UTC`, and `hms()` cuts
  `HH:MM:SS` out of the record's and the journal's `t`, also `...Z` (`core/clock.py`,
  `hub/journal.py`). Both sides are in the same zone, so a Flow line at 16:20 under a header at
  11:26 is an event of an earlier day: the Flow starts with the record's last 40 events
  (`board/state.py`, `EVENTS_SHOWN`), and a batch open for days has its last events on another day.
  It was the missing date, not a zone mix-up. The fix: the date on every line, and every time in
  the local zone, named in the header (live-rich-Q2).
- **The Ready list's source exists.** The server's `prs` topic (`board/api/topics.py`, `_prs`;
  `docs/server-api.md`, `prs.get` / `prs`) gives the batch's PRs as the forge says them: per row
  `cr`, `pr`, `number`, `state` (`open`, `draft`, `merged`, `closed`), `conflicting`, `checking`,
  `checks` (`green`, `failing`, `running`, `none`), `ready_now`, `why` (`merged`, `draft`,
  `closed`, `conflicting`, `failing` or null), plus the answer's `read_at`, `error`, `batch`. It is
  in `READ_TOPICS` (the public key may watch it); the server reads the forge for it at most once
  every 10 s per project and batch while a client asks (the AGENTS.md "batch's PRs" exception), with
  the user's own `gh` or `glab`. No server change is needed.

## What changes

All code changes are in `skills/chantier/scripts/cli/src/chantier/clients/tui/` (`model.py`,
`view.py`, `screen.py`) and `commands/live.py`, plus tests and docs. The server, its API and the
web client do not change. The TUI keeps importing nothing of chantier but itself,
`chantier.__version__` and `chantier.core.errors` (`clients/tui/__init__.py`).

### 1. Rendering (screen.py)

- Every box is a Rich `Panel` with `box.ROUNDED` (today `box.SQUARE`), its title at the left.
- Flow, Ready and Tasks are Rich `Table`s with a header row (`show_header=True`, bold), no wrap,
  cut with `…` as today (`overflow="ellipsis"`, `no_wrap=True`). Projects and Agents stay grids
  (no header): they are lists.
- Colour, always paired with a word (the screen's rule stays: no colour carries a meaning alone):
  the board's state colours, copied as hex values from the web client's
  `clients/web/css/tokens.css` into one table of `screen.py` (`STATE_COLOURS`): `working`
  `#4a76d9`, `ready` `#2f9e6b`, `blocked` `#d14b5e`, `draft` `#a77b4f`, `waits` `#d08a1f`,
  `queued` `#a3a7af`, `merged` `#2a7a55`, `local` `#8b6bd8`. Used for: a Tasks row's state word
  (working blue, blocked red), a Ready row's state word (below), the four header counts (working
  blue, ready green, held red, done merged-green). Times and the who column in a dim style.
  Rich lowers the hex colours to what the terminal has (256 or 16 colours) by itself.
- `--once` (`screen.plain`) keeps printing plain text: `color_system=None`, `no_color=True`, no
  control code at all (no colour, no OSC 8 link: with no colour system Rich writes the text only).
  It keeps the Unicode box glyphs it prints today.

### 2. Layout (screen.py `render`)

```
header (as today, 2 lines with one board, 2 + n with n boards)
+- Projects --+ +- Flow ------------------------+ +- Ready -----------+
|             | |                               | |                   |
+-------------+ |                               | +-------------------+
+- Agents ----+ |                               | +- Tasks -----------+
|             | |                               | |                   |
+-------------+ +-------------------------------+ +-------------------+
footer
```

- Left column (from 100 columns, `NARROW`, as today; `LEFT_W` 28): Projects on top, sized to its
  lines (two per project watched, as today, plus its borders), at most half of the body's height;
  Agents below it in its own box, taking the rest. Under 100 columns the whole left column is not
  drawn, as today.
- Centre: Flow, as today but for its time column (section 3).
- Right column (`RIGHT_W` 44): Ready on top, sized to its rows (one line per PR plus its header and
  borders, at least one line for its "none" text), at most half of the body's height; Tasks below,
  taking the rest.
- `commands/live.py` `height_for` (the `--once` height) counts the four boxes: the left column is
  Projects' lines plus Agents' lines plus their headers and borders; the right column is Ready's
  rows plus Tasks' rows plus theirs; the body is the tallest of the left column, the right column
  and the Flow (at most `FLOW_SHOWN` lines), as today.

### 3. Flow: date and time in the local zone, and the key `t` (live-rich-Q2, Q4)

- **The zone.** Every clock time the screen prints is in the user's local zone: the Flow's times,
  the header's clock and `reconnecting since <time>`. `Model` gets one more field, `zone`
  (a `tzinfo`, None by default: the system's local zone, each instant converted with
  `astimezone()` so a daylight-saving change is honoured line by line); tests pass a fixed zone
  (`zoneinfo.ZoneInfo("Europe/Paris")`, which `tzdata` makes available on Windows too). The
  record's and the journal's `t` stay UTC; only the drawing converts. The Flow stays sorted by
  `t` as today.
- **The header** prints the server's now in that zone with its date and its UTC offset:
  `2026-11-23 12:26:25 UTC+01:00` (today `11:26:25 UTC`). The offset form is used on every system
  (Windows zone names are long sentences). One board or several: the same clock text.
- **A Flow line's time column**, in the clock form (the default): `YYYY-MM-DD HH:MM:SS` in the local
  zone, 19 characters (today `HH:MM:SS`, 8). A `t` that does not parse shows
  `----------  --:--:--`. Column header: `Time`.
- **The key `t`** switches the column to the time since the event and back. Since-form, from the
  server's now (`Model.now()`, as the lease times): under 60 s `<n> s`; under 60 min `<n> min`;
  under 24 h `<n> h`; else `1 day` / `<n> days`; the whole number below the value (rounded down: "no
  need to be precise"), an event in the future (a clock ahead) reads `0 s`. Examples: 46 s →
  `46 s`, 150 s → `2 min`, 3 700 s → `1 h`, 3 days 2 h → `3 days`. Column header: `Ago`. One
  function in `model.py` (`since(ts, now) -> str`), tested alone.
- The screen starts in the clock form at every start; the choice is not kept between runs.
  `--once` reads no key and always prints the clock form.
- `view.py`: `View` gets `ago: bool = False`; `press("t")` flips it when no filter is being typed
  and the help is not shown (while typing, `t` is a character of the filter, as today; while the
  help shows, any key, `t` included, only closes it, as today). `HELP` gets the line
  `("t", "the Flow's time: date and time / time since the event")`, placed after `End`.
  `KEYS_FOOTER` becomes `? keys  / filter  t time  q quit`.
- The Tasks box's ages (`to review` age, lease time left) are unchanged: they are durations already.

### 4. Agents, in its own box (live-rich-Q1)

The box lists the project's active sessions, each with its role and, for a Driver, its CR, from the
`project` topic the TUI already reads (no new subscription, no server change). For each project
watched, in this order:

1. `Chief of Staff  <seat title>`: when the project's state has a `seat` (`board/state.py`
   `_seat`: the session holding the project's seat, its `title`); the title cut with `…`; with no
   title, `Chief of Staff`. Followed by `  steering` when the batch is running with
   `steering == "direct"`.
2. `Foreman  <heartbeat>`: when the batch is running and `steering == "foreman"`. `<heartbeat>` as
   the web board judges it (`clients/web/js/model/semantics.js` `heartbeat`): `heartbeat stopped`
   when `heartbeat_stopped` is set; else `beat <n> min ago` from `heartbeat` and the server's now,
   followed by `  late` (red) when `n > steering_wake_min + 5`; with no `heartbeat` yet, `Foreman`
   alone.
3. One `Driver <cr> <phase>` per CR in state `working`, as today; `<phase>` is the row's `phase`
   (`status/words.py` `phase_text`: it names the Driver's worker at work, `coder r2`, `inspector
   r1`, a review, a gate), so "workers" show through their Driver's line.
4. `Stack driver` while `stack_lease` has not ended, as today.

With several projects watched each line starts with the project's name (`<label>/<project>` with
several boards), as today. With nothing to list, `none`. A paused batch lists the Chief of Staff
only (no Foreman, no Driver: nobody steers or drives a paused batch). `Model.agents()` returns
these lines; `screen.agents_table` draws them in the new `Agents` panel (today a bold "Agents"
title inside the Projects panel, which goes).

### 5. Ready, above Tasks (live-rich-Q3)

- **Subscription.** `Model.wanted()` adds, for each project watched whose `project` state holds a
  batch in `4-batch/` (running or paused), one subscription to the `prs` topic with
  `{"project": <id>, "batch": <batch id>}`. Its key names the batch (`prs:<project>:<batch id>`, the
  model parsing the project as the text between the first and the last `:`), so a new batch is a
  new key: `Link.want` unsubscribes the old one and subscribes the new. A project with no batch in
  `4-batch/` gets no `prs` subscription (so the TUI never makes the server read the forge for a
  closed batch). `Model._event` keeps each answer in `Model.prs[project]`; `_refused` drops it;
  `missing()` lists `prs <id>` until its first answer, so `--once` waits for it like the others
  (a batch with no PR yet answers at once, with no forge read).
- **The client calls neither `gh` nor `glab`**, nor anything but the server's API.
- **Rows.** One row per CR of the project's batch whose row has `to_review` true (the record says
  it is ready to review or to merge), in the batch's `merge_order` (the order its PRs merge in), each
  with its PR row from `Model.prs` matched by `cr`. Columns, with a header row: `PR` (the number,
  `#<n>` for a GitHub PR, `!<n>` for a GitLab MR, as the web board's `prNumber`), `CR` (with
  several boards `<label> <CR>`, with several projects `<project> <CR>`), `State`, `Age` (the time
  since the hand-back, `handed_back_at`, in the form Tasks prints it today, `age()`; open question
  1), `Title` (cut).
- **State word and colour**, the same judgement as the web board's PRs page
  (`clients/web/js/views/prs-row.js`, `board/prs.py`):

  | the PR row | word | colour |
  |---|---|---|
  | no row yet (not answered, or the PR not read) | `not read` | queued |
  | `why == "merged"` | `merged, not recorded` | merged |
  | `ready_now` | `ready to merge` | ready |
  | `why == "draft"` | `draft` | draft |
  | `why == "closed"` | `closed` | blocked |
  | `why == "conflicting"` | `conflicting` | blocked |
  | `why == "failing"` | `checks failing` | blocked |
  | `checking` or `checks == "running"` | `checks running` | waits |
  | otherwise | `to review` | working |

- **The link.** The `PR` cell carries the PR's URL as a Rich link (`Style(link=<url>)`), which Rich
  writes as an OSC 8 hyperlink in the interactive screen; a terminal that knows OSC 8 makes it
  clickable, one that does not shows the plain number. Only an `http://` or `https://` URL is
  linked (as the web board's `safeUrl`); any other shows the number with no link. `--once` writes
  no link (section 1).
- **The box's title**: `Ready`; with a forge error in the answer, `Ready  forge: <error>` (cut);
  with several projects, the errors of the first one that has one.
- **Empty**: `no PR ready` when the batches watched have no CR to review; `no running batch` when
  no project watched has a batch in `4-batch/`.
- **The filter** (`/`) narrows Ready as it narrows Tasks: a row is kept when the text (any case) is
  in its board label, project, CR, title or PR number.

### 6. Tasks

Tasks keeps its working and blocked sections as today. Its `to review` section: see open
question 1 (the default this spec implements, pending the answer: it moves to Ready, which shows
the same CRs; Tasks then shows working and blocked only, and its `no running batch` and
`no task matches <text>` lines stay).

### 7. Docs

- `docs/boards.md`, "The live terminal view": the layout (Projects and Agents on the left, Flow,
  Ready and Tasks on the right), what Agents lists (section 4), the Ready box (source: the server's
  `prs` topic, read by the server at most once every 10 s while `live` watches, the states and
  their words, the OSC 8 link), the local zone and the header's offset, the date on each Flow line,
  the key `t` in the keys table, and a new `--once` capture of the new screen (120 columns) in
  place of the old one.
- `docs/server-api.md`, the `chantier live` paragraph (line ~295): it also watches `prs` for each
  project with a batch.
- No change to `AGENTS.md`: the server's forge read for `prs` while a client subscribes is already
  the named "batch's PRs" exception, and `live` still writes nothing and messages no agent.

## Decisions carried from 02-answers.md

- live-rich-Q1 A: Agents lists the project's active sessions (Chief of Staff, Foreman, Drivers and
  their workers), each with its role and its CR; the observed `none` is checked above: not a bug of
  the reading, a list too narrow (section 4).
- live-rich-Q2 A: date and time in the user's local zone, the zone written in the header; the
  observed gap was an earlier day's events, all times being UTC (sections "What the code does
  today" and 3).
- live-rich-Q3 A: Ready comes from the server's published API (`prs`), with the state in the board's
  colours; the client calls neither `gh` nor `glab` (section 5).
- live-rich-Q4 A: the key `t`, starting on date and time, switching to the rounded time since the
  event (`46 s`, `2 min`, `1 h`, `3 days`) and back (section 3).
- From the request (item 5): Rich rendering with real tables and boxes, `--once` still plain text,
  the layout Projects / Agents / Flow / Ready / Tasks, the OSC 8 link where the terminal allows,
  and the dependency check (Rich is already a pinned dependency: nothing to add).
- live-rich-Q5 A: specified for the running batch batch-31.

## Out of scope

- Any change to the server, its API, its topics, `docs/server-api.md`'s protocol tables, or the web
  client (it is only read for its colours and words).
- QA drivers (an order's `agent` and `lease` in `batch.json`): the `project` topic does not carry
  them; see open question 2.
- Keeping the `t` choice between runs; a key for the zone; showing UTC beside local.
- Colours or links in `--once`.
- New `chantier live` options, more boards, mouse support.
- Preflight P14's own counting (`core/surface_batches.py`).

## Evidence

Tests stay few, parametrized and fast (`just test` budget, AGENTS.md); they extend
`skills/chantier/scripts/cli/tests/test_live_model.py` (prepared events, no server) and
`test_live_link.py` (the real server).

1. **Model, `since`** (parametrized): 0 s → `0 s`, 46 s → `46 s`, 150 s → `2 min`, 3 700 s →
   `1 h`, 86 400 s → `1 day`, 3 days 2 h → `3 days`, a time 5 s in the future → `0 s`.
2. **Model, the zone**: with `zone=ZoneInfo("Europe/Paris")`, a line at `2029-12-31T23:50:00Z`
   draws `2030-01-01 00:50:00`, and the header reads `2030-01-01 01:00:00 UTC+01:00` for the
   server's now `2030-01-01T00:00:00Z` (`NOW` of the test file); a summer instant gives
   `UTC+02:00`. The existing assertion `"23:50:00" in wide` changes accordingly.
3. **Model, Agents** (parametrized on prepared `project` states): seat with title + running direct
   batch → `Chief of Staff  <title>  steering`; foreman steering with `heartbeat` 3 min old and
   `steering_wake_min` 10 → `Foreman  beat 3 min ago`; 20 min old → ends with `late`;
   `heartbeat_stopped` → `Foreman  heartbeat stopped`; one working CR → `Driver CR-1 coding` (the
   existing assertion); live `stack_lease` → `Stack driver`; no seat, no working CR, direct
   steering → `none`; paused batch → the Chief of Staff only.
4. **Model, Ready**: `wanted()` holds `prs:p:batch-01` with `{"project": "p", "batch":
   "batch-01"}` once the project state names `batch-01`, none before, and a new key after the batch
   id changes; `missing()` names `prs p` until the `prs` event; a `prs` answer with one row per
   case of the state table draws each word (parametrized over the table's nine lines); the rows
   follow `merge_order`; the filter keeps a row by its PR number.
5. **Screen, `--once` plain text** (`screen.plain` at 140 and 90 columns, as the existing
   `test_the_screen_shows_...`): the panel titles `Projects`, `Agents`, `Flow`, `Ready`, `Tasks` at
   140 and no `Projects` nor `Agents` at 90; the column headers `Time`, `PR`, `State`; the date in a
   Flow line; `"\x1b" not in` the output (no colour, no OSC 8); every line within the width.
6. **Screen, the interactive rendering**: `render` printed through a Rich `Console(file=StringIO,
   force_terminal=True, color_system="truecolor", width=140)` holds the OSC 8 sequence
   `\x1b]8;` with the PR's `https://` URL for a Ready row, none for a `file:` URL, and the SGR colour
   of `ready` (`38;2;47;158;107`) on the `ready to merge` word.
7. **Keys** (the existing parametrized `test_keys_scroll_pause_filter_and_help_...`): new cases
   `["t"]` → `Ago` and `12 min` shown, `Time` hidden; `["t", "t"]` → back to `Time`; `["/", "t",
   "enter"]` → `filter: t`, still `Time`; `["?", "t"]` → the help closed, still `Time`; the help
   lists `t`. The footer test expects `? keys  / filter  t time  q quit`.
8. **The colours match the board's** (a check guarding a shipped file): a test reads
   `skills/chantier/scripts/cli/src/chantier/clients/web/css/tokens.css` from the repository as it
   ships, at the head under test (not a copy), parses each `--state-<name>: #xxxxxx;` and asserts
   `screen.STATE_COLOURS` equals them, name by name.
9. **`--once` against the real server** (`test_live_link.py`
   `test_live_once_prints_the_working_cr_and_its_lease_and_a_journal_line_comes_once`, both
   transports): it also asserts the `Agents` and `Ready` titles and a Flow line's date
   (`\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}`), and still `"\x1b" not in out`. Its batch's CR has no
   PR: the `prs` subscription answers with no forge read, so the test needs no network. The
   scenario's line for CR-418 in `scenario/README.md` names the two new boxes.
10. `just check` passes; the Driver also runs `just eval-dry-run` (a change under the CLI's `src/`)
    and the long gate `scenario` before the PR (a CLI change), as AGENTS.md says.
11. **By hand, once, on the user's Windows machine** (Windows Terminal) and noted in the PR: a
    `chantier live` screen over the running batch shows the rounded boxes and colours, `t`
    switches the Flow's times, and a Ready row's PR number opens the PR on a click. No screenshot
    of the CR board pane is owed (this CR does not change `hooks/register.tsx` nor `STATUS.json`).

No host or default matrix: nothing here depends on the host (Claude Code or Copilot) or on a
configured value.

## Open questions

1. **Tasks' `to review` section.** Ready now lists the CRs to review; should Tasks drop its
   `to review` section (the spec's default: yes, Tasks keeps working and blocked; the age since
   the hand-back moves to Ready as a fifth column, `Age`) or keep it (the same CRs twice)?
2. **QA drivers in Agents.** A QA driver (an order's agent with its lease) is a Driver-like session
   the `project` topic does not carry today. Leave it out (this spec), or add it, which needs the
   server's `project` state to publish the orders' live leases (a server and API change)?
