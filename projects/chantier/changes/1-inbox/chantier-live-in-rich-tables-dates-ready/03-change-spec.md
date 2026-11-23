# chantier live: Rich tables, local dates, Agents and Ready boxes

Short name: `live-rich`. Destination: the running batch batch-31. Owner's words of 2026-11-23
(`intake/request.md`), grilled in `02-answers.md` (live-rich-Q1 to Q11, and the spec critic's
findings recorded there).

## Goal

The owner runs `chantier live` and finds it plain ("en ASCII"). He wants:

- real tables with colours;
- the date beside each event's time;
- a key that switches the times to "how long ago";
- the Agents in a box of their own;
- a Ready box above Tasks, listing the PRs or MRs ready to review or to merge, each with its state in the board's colours and a link he can click where the terminal allows.

## What the code does today (read for this spec)

- **The plain look.** `chantier live` is already drawn with Rich (`clients/tui/screen.py`): `Table.grid` columns with
  no header, `box.SQUARE` panels, one bold count line, no colour. The "ASCII" look the owner saw is
  this monochrome, headerless grid, not a missing library.
- **Rich is not a new dependency** (finding kept in `02-answers.md`, answer 8). `pyproject.toml`
  already pins `rich==15.0.0` and `blessed==1.53.0`. Both are listed in
  `[tool.ruff.lint.flake8-tidy-imports] banned-module-level-imports`, so they load inside the
  drawing functions when `live` runs, and `uv.lock` holds them. The
  `uvx --from <plugin root> chantier` and `uv run --no-sync --project` launches are unchanged; this
  CR edits neither `pyproject.toml` nor `uv.lock`. `tzdata==2026.2` is already a dependency (the
  zone database on Windows).
- **The `none` in Agents (live-rich-Q1's check).** `Model.agents()` (`clients/tui/model.py`) lists
  one `Driver <cr> <phase>` per CR in state `working` of a running batch, and `Stack driver` while
  `stack_lease` has not ended, and nothing else. At the same moment, preflight P14 reported
  "batch-20 running, steering direct, 0 Drivers". With no CR working and no stack lease, `none` was
  the right answer for that narrow list, not a reading bug. The new list (section 4) is the one
  Q1 asks for.
- **The time gap (live-rich-Q2's check).** Every time the screen shows is UTC:
  - the header prints `Model.now()` (the server's `now`, `%Y-%m-%dT%H:%M:%SZ`) as `HH:MM:SS UTC`;
  - `hms()` cuts `HH:MM:SS` out of the record's and the journal's `t`, also `...Z` (`core/clock.py`,
    `hub/journal.py`).

  A Flow line at 16:20 under a header at 11:26 is therefore an event of an earlier day. The Flow
  starts with the record's last 40 events (`board/state.py`, `EVENTS_SHOWN`), so a batch open for
  days shows events from earlier days. The fix: the date on every Flow line, and every time in the
  local zone, with the UTC offset in the header.
- **Ready's source exists.** The server's `prs` topic (`board/api/topics.py` `_prs`,
  `board/prs.py` `answer`; `docs/server-api.md`, `prs.get` / `prs`) gives the batch's PRs as the
  forge says them. Each row has `cr`, `pr`, `number`, `state` (`open`, `draft`, `merged`,
  `closed`), `conflicting`, `checking`, `checks` (`green`, `failing`, `running`, `none`),
  `ready_now` and `why` (`merged`, `draft`, `closed`, `conflicting`, `failing`, or null). The
  answer also carries `read_at`, `error` and `batch`.
  - It is in `READ_TOPICS`, so the public key may watch it.
  - The server reads the forge for it at most once every 10 s per project and batch while a client
    asks, with the user's own `gh` or `glab` (the AGENTS.md "batch's PRs" exception).
  - The same read appends one `merged@1` line to the project's `forge-journal.jsonl` when it finds
    a PR of the batch in `4-batch/` merged that the record does not hold. That is the same
    exception's second write, already named in AGENTS.md.

  No server change is needed.

## What changes

The code changes are in `skills/chantier/scripts/cli/src/chantier/clients/tui/` (`model.py`,
`view.py`, `screen.py`) and in `commands/live.py`; the rest is tests and docs. The server, its
API and the web client do not change. The TUI keeps importing nothing of chantier but itself,
`chantier.__version__` and `chantier.core.errors` (`clients/tui/__init__.py`).

### 1. Rendering (screen.py)

- Every box is a Rich `Panel` with `box.ROUNDED` (today `box.SQUARE`), its title at the left.
- Flow, Ready and Tasks are Rich `Table`s with a bold header row (`show_header=True`). Cells do
  not wrap and are cut with `…` as today (`overflow="ellipsis"`, `no_wrap=True`). Projects and
  Agents stay grids with no header: they are lists.
- **Colour**, always paired with a word. The screen's rule stays: no colour carries a meaning
  alone. The colours are the board's eight state colours, kept in one table of `screen.py`,
  `STATE_COLOURS`, with the same values as the `--state-<name>` variables of the web client's
  `clients/web/css/tokens.css`:

  | state | colour |
  |---|---|
  | `working` | `#4a76d9` |
  | `ready` | `#2f9e6b` |
  | `blocked` | `#d14b5e` |
  | `draft` | `#a77b4f` |
  | `waits` | `#d08a1f` |
  | `queued` | `#a3a7af` |
  | `merged` | `#2a7a55` |
  | `local` | `#8b6bd8` |

  They are used for:
  - a Tasks row's state word (working blue, blocked red);
  - a Ready row's state word (section 5);
  - the four header counts (working blue, ready green, held red, done merged-green).

  Times and the who column are dim. Rich lowers the hex colours to what the terminal has (256 or
  16 colours) by itself.
- **`--once`** (`screen.plain`) keeps printing plain text: `color_system=None`, `no_color=True`,
  and no control code at all. That means no colour and no OSC 8 link: with no colour system, Rich
  writes the text only. It keeps the Unicode box glyphs it prints today.

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

- **Left column** (`LEFT_W` 28), drawn from 100 columns (`NARROW`) as today:
  - Projects on top, sized to its lines (two per project watched, as today, plus its borders), at
    most half the body's height;
  - Agents below it, in its own box, taking the rest.

  Under 100 columns the whole left column is not drawn, as today.
- **Centre**: the Flow, as today but for its time column (section 3).
- **Right column** (`RIGHT_W` 44):
  - Ready on top, sized to its rows (one line per PR plus its header and borders, at least one
    line for its empty text), at most half the body's height;
  - Tasks below, taking the rest.
- **`--once` height.** `commands/live.py` `height_for` counts the four boxes:
  - the left column: Projects' lines plus Agents' lines, with their headers and borders;
  - the right column: Ready's rows plus Tasks' rows, with theirs;
  - the body: the tallest of the left column, the right column and the Flow (at most `FLOW_SHOWN`
    lines), as today.

### 3. Flow: local date and time, and the key `t` (live-rich-Q2, Q4, Q11)

- **The zone.** Every clock time the screen prints is in the user's local zone: the Flow's times,
  the header's clock, and `reconnecting since <time>`.
  - `Model` gets one more field, `zone` (a `tzinfo`). Its default, None, means the system's local
    zone, each instant converted with `astimezone()` so a daylight-saving change is honoured line
    by line.
  - Tests pass a fixed zone, `zoneinfo.ZoneInfo("Europe/Paris")`, which `tzdata` makes available
    on Windows too.
  - The record's and the journal's `t` stay UTC; only the drawing converts. The Flow stays sorted
    by `t`, as today.
- **The header** prints the server's now in that zone, with its full date and its UTC offset:
  `2026-11-23 12:26:25 UTC+01:00` (today `11:26:25 UTC`). The offset form is used on every system,
  because Windows zone names are long sentences. The clock text is the same with one board or
  several.
- **A Flow line's time column (live-rich-Q11 B: the short form).** The clock form is the default:
  - It reads `MM-DD HH:MM:SS` in the local zone, for example `11-23 12:26:25`: 14 characters
    (today `HH:MM:SS`, 8). The Flow keeps its room for the text.
  - The year is not shown on the line; the header's full date gives it.
  - A `t` that does not parse shows `----- --:--:--`.
  - The column header is `Time`.
- **The key `t`** switches the column to the time since the event, and back:
  - It counts from the server's now (`Model.now()`, as the lease times do).
  - Under 60 s it reads `<n> s`; under 60 min `<n> min`; under 24 h `<n> h`; else `1 day` or
    `<n> days`.
  - The number is rounded down ("no need to be precise"). An event in the future (a clock ahead)
    reads `0 s`.
  - Examples: 46 s gives `46 s`, 150 s gives `2 min`, 3 700 s gives `1 h`, 3 days 2 h gives
    `3 days`.
  - The column header is `Ago`.
  - One function of `model.py`, `since(ts, now) -> str`, computes it, tested alone.
- **Start and `--once`.** The screen starts in the clock form at every start; the choice is not
  kept between runs. `--once` reads no key and always prints the clock form.
- **`view.py`:**
  - `View` gets `ago: bool = False`.
  - `press("t")` flips it when no filter is being typed and the help is not shown. While typing,
    `t` is a character of the filter, as today. While the help shows, any key, `t` included, only
    closes it, as today.
  - `HELP` gets the line `("t", "the Flow's time: date and time / time since the event")`, after
    `End`.
  - `KEYS_FOOTER` becomes `? keys  / filter  t time  q quit`.

### 4. Agents, in its own box (live-rich-Q1, Q7, Q8)

The box lists the project's sessions, each with its role and, for a Driver, its CR. It reads the
`project` topic the TUI already reads: no new subscription and no server change. For each project
watched, in this order:

1. **`Chief of Staff (seat)  <seat title>`** (live-rich-Q8), when the project's state has a `seat`
   (`board/state.py` `_seat`: the session holding the project's seat and its `title`).
   - The title is cut with `…`. With no title, the line reads `Chief of Staff (seat)` alone.
   - The line names the seat holder only. It claims nothing about whether that session is
     running: no "steering", "live" or "active" word.
2. **`Foreman  <heartbeat>`**, when the batch is running and `steering == "foreman"`. The
   `<heartbeat>`, from the record's `heartbeat`, `heartbeat_stopped` and `steering_wake_min`:
   - `heartbeat stopped` when `heartbeat_stopped` is set;
   - else `beat <n> min ago`, from `heartbeat` and the server's now (minutes rounded to the nearest
     whole number), followed by `  late` in the blocked colour when `n > steering_wake_min + 5`;
   - with no `heartbeat` yet, the line reads `Foreman` alone.
3. **One `Driver <cr> <phase>` per CR in state `working`**, as today. `<phase>` is the row's `phase`
   (`status/words.py` `phase_text`). It names the worker the Driver runs (`coder r2`,
   `inspector r1`, a review, a gate), so the workers show through their Driver's line.
4. **`Stack driver`** while `stack_lease` has not ended, as today.

Other rules:

- With several projects watched, each line starts with the project's name (`<label>/<project>`
  with several boards), as today. With nothing to list, the box reads `none`.
- A paused batch lists no Foreman and no Driver. The seat line stays.
- QA drivers are left out (live-rich-Q7): the `project` topic does not carry an order's agent or
  lease.
- `Model.agents()` returns these lines. `screen.agents_table` draws them in the new `Agents` panel,
  which replaces today's bold "Agents" title inside the Projects panel.

### 5. Ready, above Tasks (live-rich-Q3, Q6, Q9, Q10)

- **Subscription.**
  - `Model.wanted()` adds one `prs` subscription for each project watched whose `project` state
    holds a batch in `4-batch/`, running or paused, with `{"project": <id>, "batch": <batch id>}`.
  - Its key names the batch: `prs:<project>:<batch id>`. The model reads the project as the text
    between the first and the last `:`. A new batch is therefore a new key: `Link.want`
    unsubscribes the old one and subscribes the new.
  - A project with no batch in `4-batch/` gets no `prs` subscription, so the TUI never makes the
    server read the forge for a closed batch.
  - `Model._event` keeps each answer in `Model.prs[project]`, and `_refused` drops it.
- **No forge call in the client.** It calls neither `gh` nor `glab`, nor anything but the server's
  API.
- **Rows.**
  - One row per CR whose row has `to_review` true (the record says it is ready to review or to
    merge), in a running or a paused batch: a paused batch's CRs to review are listed too.
  - They are in the batch's `merge_order`, the order their PRs merge in.
  - Each row takes its PR row from `Model.prs`, matched by `cr`.
  - The columns, with a header row:
    - `PR`: the number, `#<n>` for a GitHub PR, `!<n>` for a GitLab MR. An MR is a link with
      `/merge_requests/`.
    - `CR`: `<label> <CR>` with several boards, `<project> <CR>` with several projects.
    - `State`.
    - `Age`: the time since the hand-back, `handed_back_at`, as `age()` prints it today in Tasks.
      It moved here from Tasks (live-rich-Q6).
    - `Title`, cut.
- **State word and colour** (live-rich-Q9). This table is the TUI's own. It makes no claim of
  matching the web PRs page's tags; the colours are the board's state colours (section 1). An
  open PR to review with nothing else to say is grey, as on the board.

  | the PR row | word | colour |
  |---|---|---|
  | no row (not answered yet, the forge not read, or the PR not in the read) | `not read` | queued |
  | `why == "merged"` | `merged, not recorded` | merged |
  | `ready_now` | `ready to merge` | ready |
  | `why == "draft"` | `draft` | draft |
  | `why == "closed"` | `closed` | blocked |
  | `why == "conflicting"` | `conflicting` | blocked |
  | `why == "failing"` | `checks failing` | blocked |
  | `checking` or `checks == "running"` | `checks running` | waits |
  | otherwise (open, to review) | `to review` | queued (grey) |

  The first matching line, top to bottom, gives the word.
- **The link.** The `PR` cell carries the PR's URL as a Rich link (`Style(link=<url>)`), which Rich
  writes as an OSC 8 hyperlink in the interactive screen.
  - A terminal that knows OSC 8 makes the number clickable; one that does not shows the plain
    number.
  - Only an `http://` or `https://` URL is linked; any other shows the number with no link.
  - `--once` writes no link (section 1).
- **The box's title** is `Ready`. With a forge error in an answer, it reads
  `Ready  forge: <error>`, cut; with several projects, the error of the first project that has
  one.
- **The empty text** matches what the box lists (running or paused batches):
  - `no batch` when no project watched has a batch in `4-batch/`;
  - `no PR ready` when the batches there have no CR to review;
  - `no PR matches <text>` when the filter hides every row.
- **The filter** (`/`) narrows Ready as it narrows Tasks: a row stays when the text, in any case,
  is in its board label, project, CR, title or PR number.
- **`--once` and a slow or offline forge** (live-rich-Q10):
  - `missing()` does not name the `prs` subscriptions: the board, `project` and `events` first
    answers are still required, as today.
  - `once()` (`commands/live.py`) waits, within the same `ONCE_S` deadline, for every `prs`
    subscription's first answer too, then prints.
  - When the deadline comes with the other answers in but a `prs` answer missing, it prints the
    screen anyway, exit 0, and the Ready rows of that project read `not read`.
  - A `prs` answer that came with an error also shows its rows `not read` where it has no row,
    with the error in the box's title.
  - When a first answer other than `prs` is missing at the deadline, `--once` exits 4 with the
    missing ones named, as today.
  - A new model method, `pending_prs()`, lists the `prs` subscriptions not answered yet.

### 6. Tasks (live-rich-Q6)

Tasks loses its `to review` section: those CRs and their age are in Ready. It keeps:

- the working CRs (title, then lease time left, round and phase), as today;
- the blocked CRs with their reason, as today;
- `no running batch` when no running batch is watched;
- `no task matches <text>` when the filter hides every row.

The header's four counts are unchanged; `ready` still counts the CRs to review.

### 7. Docs

- **`docs/boards.md`, "The live terminal view":**
  - the layout: Projects and Agents on the left, the Flow, Ready above Tasks on the right;
  - what Agents lists (section 4), the seat line saying nothing of whether that session runs, and
    QA drivers not shown;
  - the Ready box:
    - its source, the server's `prs` topic, which the server reads on the forge at most once every
      10 s per project and batch while `live` watches;
    - that the same server read may append one "merged, not recorded" (`merged@1`) line to the
      project's `forge-journal.jsonl` when it finds a merge the record does not hold (the server's
      write, not `live`'s);
    - the state words and their colours, the `Age` column, the OSC 8 link, a paused batch's rows;
    - `--once` printing `not read` when the forge has not answered by the deadline;
  - Tasks without its `to review` section;
  - the local zone and the header's offset, the `MM-DD HH:MM:SS` time on each Flow line, and the
    key `t` in the keys table;
  - a new `--once` capture of the new screen (120 columns) in place of the old one.
- **`docs/server-api.md`**, the `chantier live` paragraph (line ~295): it also watches `prs` for
  each project with a batch in `4-batch/`, and the server's read for it may append the
  `merged@1` journal line, as for the web page.
- **No change to `AGENTS.md`.** The server's forge read for `prs` while a client subscribes, and
  its `merged@1` line, are already the named "batch's PRs" exception. `live` itself still writes
  nothing and messages no agent.

## Decisions carried from 02-answers.md

- **Q1 A:** Agents lists the project's sessions (Chief of Staff, Foreman, Drivers and their
  workers), each with its role and its CR. The observed `none` was right for the old narrow list
  (section 4).
- **Q2 A:** the user's local zone, written in the header as a UTC offset. The observed gap was
  events of an earlier day, with every time in UTC.
- **Q3 A:** Ready comes from the server's published API (`prs`). The client calls neither `gh`
  nor `glab`.
- **Q4 A:** the key `t`, starting on date and time, switching to the rounded time since the event
  and back.
- **Item 5, from the request:** Rich rendering with real tables and boxes, `--once` still plain
  text, the layout Projects / Agents / Flow / Ready / Tasks, the OSC 8 link where the terminal
  allows. Rich is already a pinned dependency (answer 8's finding).
- **Q5 A:** specified for the running batch batch-31.
- **Q6 A:** Tasks' `to review` section goes. The hand-back age is Ready's `Age` column; Tasks
  keeps working and blocked.
- **Q7 A:** QA drivers are left out; no server or API change.
- **Q8 A:** `Chief of Staff (seat)`, the seat holder, with no claim that it is running.
- **Q9 A:** the one-word state table is kept, with no claim of matching the web PRs page. An open
  PR to review is grey.
- **Q10 A:** `--once` prints at the deadline, with Ready saying `not read`.
- **Q11 B:** the short date form `MM-DD HH:MM:SS` on Flow lines. The user chose it over the
  recommended full form; the header keeps the full date.
- **The critic's findings recorded in 02-answers.md:**
  - The colour test parses the eight `--state-<name>` variables only, not the `-tint` ones
    (Evidence 8).
  - Ready lists a paused batch's CRs, and its empty text says `no batch`, which matches what it
    lists (section 5).
  - The docs say that the server's `prs` read can append the "merged, not recorded" line while
    `live` watches (section 7).

## Out of scope

- Any change to the server, its API, its topics, the protocol tables of `docs/server-api.md`, or
  the web client. The web client is only read for its colour values.
- QA drivers in Agents (live-rich-Q7).
- Keeping the `t` choice between runs, a key for the zone, or UTC shown beside local time.
- Colours or links in `--once`.
- New `chantier live` options, more boards, mouse support.
- Preflight P14's own counting (`core/surface_batches.py`).

## Evidence

Tests stay few, parametrized and fast (the `just test` budget, AGENTS.md). They extend
`skills/chantier/scripts/cli/tests/test_live_model.py` (prepared events, no server) and
`test_live_link.py` (the real server).

1. **Model, `since`** (parametrized):

   | input | output |
   |---|---|
   | 0 s | `0 s` |
   | 46 s | `46 s` |
   | 150 s | `2 min` |
   | 3 700 s | `1 h` |
   | 86 400 s | `1 day` |
   | 3 days 2 h | `3 days` |
   | 5 s in the future | `0 s` |

2. **Model, the zone**, with `zone=ZoneInfo("Europe/Paris")`:
   - a line at `2029-12-31T23:50:00Z` draws `01-01 00:50:00`;
   - the header reads `2030-01-01 01:00:00 UTC+01:00` for the server's now
     `2030-01-01T00:00:00Z` (the test file's `NOW`);
   - a summer instant gives `UTC+02:00`;
   - an unparsable `t` draws `----- --:--:--`;
   - the existing assertion `"23:50:00" in wide` becomes `"01-01 00:50:00" in wide` under that
     zone.
3. **Model, Agents** (parametrized on prepared `project` states):

   | prepared state | expected line |
   |---|---|
   | a seat with a title | `Chief of Staff (seat)  <title>` |
   | a seat with no title | `Chief of Staff (seat)` |
   | Foreman steering, `heartbeat` 3 min old, `steering_wake_min` 10 | `Foreman  beat 3 min ago` |
   | the same, 20 min old | the line ends with `late` |
   | `heartbeat_stopped` set | `Foreman  heartbeat stopped` |
   | one working CR | `Driver CR-1 coding` (the existing assertion) |
   | a live `stack_lease` | `Stack driver` |
   | no seat, no working CR, direct steering | `none` |
   | a paused batch with a seat | the seat line only |

   No line holds `steering`, `live` or `active`.
4. **Model, Ready:**
   - `wanted()` holds `prs:p:batch-01` with `{"project": "p", "batch": "batch-01"}` once the
     project state names `batch-01`, for a running and for a paused batch; it holds none before,
     and a new key after the batch id changes.
   - `missing()` never names `prs`, and `pending_prs()` names it until the `prs` event.
   - A `prs` answer with one row per line of the state table draws each word (parametrized over
     the table's nine lines).
   - The rows follow `merge_order`, and the `Age` column shows the hand-back age (the existing
     `12m  Ready one` case moves from Tasks to Ready).
   - The filter keeps a row by its PR number.
   - The empty texts read `no batch` and `no PR ready`.
5. **Screen, `--once` plain text** (`screen.plain` at 140 and 90 columns, as the existing
   `test_the_screen_shows_...`):
   - at 140, the panel titles `Projects`, `Agents`, `Flow`, `Ready`, `Tasks`; at 90, neither
     `Projects` nor `Agents`;
   - the column headers `Time`, `PR`, `State`, `Age`;
   - Tasks shows no `to review` line;
   - `"\x1b" not in` the output (no colour, no OSC 8), and every line is within the width.
6. **Screen, the interactive rendering.** `render`, printed through a Rich
   `Console(file=StringIO, force_terminal=True, color_system="truecolor", width=140)`:
   - holds the OSC 8 sequence `\x1b]8;` with the PR's `https://` URL for a Ready row, and none for
     a `file:` URL;
   - draws the `ready to merge` word in the SGR colour of `ready` (`38;2;47;158;107`), and the
     `to review` word in the colour of `queued` (`38;2;163;167;175`).
7. **Keys** (the existing parametrized `test_keys_scroll_pause_filter_and_help_...`), new cases:

   | keys | result |
   |---|---|
   | `["t"]` | `Ago` and `10 min` shown, `Time` hidden |
   | `["t", "t"]` | back to `Time` |
   | `["/", "t", "enter"]` | `filter: t`, still `Time` |
   | `["?", "t"]` | the help closed, still `Time` |

   The help lists `t`, and the footer test expects `? keys  / filter  t time  q quit`.
8. **The colours are the board's.** This check guards a shipped file:
   - A test reads `skills/chantier/scripts/cli/src/chantier/clients/web/css/tokens.css` from the
     repository as it ships, at the head under test, not a copy.
   - It parses only the eight variables `--state-<name>: #xxxxxx;`, for the names `blocked`,
     `working`, `ready`, `draft`, `local`, `waits`, `queued` and `merged` (matching
     `^\s*--state-([a-z]+):\s*(#[0-9a-f]{6});`, so the `-tint` variables and the `var(...)` aliases
     are not read).
   - It asserts that `screen.STATE_COLOURS` equals them, name by name.
9. **`--once` and the forge's deadline.** `once()` is fed by prepared links whose `prs` first
   answer never comes:
   - it prints the screen with `not read` in Ready and returns, exit 0;
   - with an `events` answer missing instead, it raises the exit-4 error naming it, as today.

   `ONCE_S` is shortened in the test, so it stays fast.
10. **`--once` against the real server** (`test_live_link.py`
    `test_live_once_prints_the_working_cr_and_its_lease_and_a_journal_line_comes_once`, both
    transports). It also asserts:
    - the `Agents` and `Ready` titles;
    - a Flow line's time (`\d{2}-\d{2} \d{2}:\d{2}:\d{2}`);
    - still `"\x1b" not in out`.

    Its batch's CR has no PR, so the `prs` subscription answers with no forge read and the test
    needs no network. The line for CR-418 in `scenario/README.md` names the two new boxes.
11. **The gates.** `just check` passes. The Driver also runs `just eval-dry-run` (a change under
    the CLI's `src/`) and the long gate `scenario` before the PR (a CLI change), as AGENTS.md says.
12. **By hand, once, on the user's Windows machine** (Windows Terminal), noted in the PR. A
    `chantier live` screen over the running batch shows:
    - the rounded boxes and the colours;
    - `t` switching the Flow's times;
    - a Ready row's PR number opening the PR on a click.

    No screenshot of the CR board pane is owed: this CR changes neither `hooks/register.tsx` nor
    `STATUS.json`.

There is no host or default matrix: nothing here depends on the host (Claude Code or Copilot) or
on a configured value.
