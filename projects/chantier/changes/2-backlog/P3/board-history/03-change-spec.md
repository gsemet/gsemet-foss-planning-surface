# Web board History page: what was done per day, week or month

A read-only History page on the web board: pick a day, a week or a month, move with previous, next
and Today, and read, grouped by local day, every CR merged or dropped, every PR opened and every
release of that period, under five plain totals. It reads the records and the archived CRs' steps,
never the forge or git, and writes nothing; from now on a batch's close adds to its record the
times and the release mark the page needs. Joins batch-30.

All paths below are relative to `skills/chantier/scripts/cli/src/chantier/` unless they start with
`docs/`, `scenario/`, `tests/` (which is `skills/chantier/scripts/cli/tests/`) or the repository
root. Read `clients/web/DESIGN.md` first and keep it true (AGENTS.md).

## Goal, in the user's words

"le bilan du jour oui dans une page dédiée, genre historique, avec une vue par jour et tous les CR /
PR et release faites. un peu comme la page energie de home assistant, avec possibilité de faire
avant/apres, selectionner semaine etc." (2026-11-13). The board has no page that answers "what was
done today, this week, this month": the records hold it batch by batch only (Costs, the Batch
navigator, Home's last batches).

## Decisions carried from 02-answers.md

| Answer | Decision | Section |
| --- | --- | --- |
| ui-night | batch-30; questions answered by a Fable advisor; the goal is a working UI | all |
| ui-night act | the board edits no batch and messages no agent (AGENTS.md stands) | 2 |
| Q1 | a new read-only view "History" / "Historique": the period's events grouped by day, newest day first, totals above | 3 |
| Q2 | History: list and plain figures only; no chart, curve, median, cycle time, spend by source, ranking | 3, Out of scope |
| Q3 | periods: day, week, month; no year, no free range | 2, 3 |
| Q4 | previous, next, Today; opens on today in the day view; next is off when the period holds today; previous never off | 3 |
| Q5 | the browser's local day (UTC times converted); week Monday to Sunday; calendar month; header in the board's language | 2, 3 |
| Q6 | the period kind and date are in the address; reload, shared link, Back walk the periods | 3 |
| Q7 | one line per event: CR merged, CR dropped (with where it went when recorded), PR opened (the first ship), release; time, kind, CR number and one-line title, batch, rounds and cost for an ended CR | 2, 3 |
| Q8 | a PR made ready is not shown: a known gap, nothing guessed | Known gaps |
| Q9 | a release is the merge of a release CR's version PR, from the record's own mark (`kind`), version when recorded; no tag or forge publication; an unmarked record shows a plain merged CR | 1, 2 |
| Q10 | sources: the closed records, the archived and trashed CRs they name, the running batch; no forge, no git, nothing written | 2 |
| Q11 | the close adds what a line needs (end time, release mark) to the record from now on, additions only; old records not rewritten; the page reads the archived CR's steps | 1, 2 |
| Q12 | a CR with no recorded time is in no period; one quiet foot line counts them and links to Costs; never dated from the archive folder's name | 2, 3 |
| Q13 | totals: CRs merged, CRs dropped, PRs opened, releases, cost; no comparison, no trend | 2, 3 |
| Q14 | cost: sum of the recorded costs of the CRs that ended in the period, labelled as the CRs' cost, a note under it (steering and grill not spread over days) linking to Costs; partial when a CR has no price | 2, 3 |
| Q15 | week and month: the same list grouped by day, each day with a small head (date, counts); an empty day not drawn; no calendar grid | 3 |
| Q16 | empty period: totals at zero, "Nothing done in this period" | 3 |
| Q17 | a line opens its CR in the side panel; the PR number links to the forge in a new tab; the batch name opens the Batch page on it | 3 |
| Q18 | no filter, no search | Out of scope |
| Q19 | one project at a time; no "All projects" view (opens on the last real project) | 3 |
| Q20 | live: today's period follows the board's live state; a past period does not move | 2, 3 |
| Q21 | Home, Costs, the Batch navigator unchanged; History in the sidebar after PRs, before Costs | 3 |
| Q22 | existing components and tokens only, i18n in English and French, no new protected feature or colour, DESIGN.md kept true, readable on a narrow screen | 3, 4 |
| Q23 | data read on demand, not added to every page's state; served to any API client (an addition to protocol 1); a month of a hundred CRs shows without a visible wait; unreadable files skipped and counted | 2 |
| Q24 | screenshots of a day, a week, a month and an empty period on the real surface; tests of the local day, the week's limits, the totals | Evidence |
| Q25 | out: charts and comparisons, year, PR ready time, forge tags, CRs that never entered a batch, export, any edit | Out of scope |

## What changes

### 1. The close records what a line needs (Q9, Q11)

`history.py:cr_entry` (written by `close_record`, called from `commands/close_archive.py:_close_files`)
adds four keys to each CR of `5-archives/batches/batch-NN.json`, after the existing ones, every key
always present (the record's habit: `null` until known):

- `kind`: the CR's `CrEntry.kind` as it is (`change`, `fix` or `release`). This is the record's own
  mark of a release CR (Q9).
- `ended`: the UTC instant the CR ended, merged or dropped, or `null` when no event says it. Use the
  same rule as `board/times.py:_ended` (the merged CR's `merged_at`, else the latest of its
  `handback` with result `merged` and its `order merged`; a cancelled CR: the latest of its `cancel`
  and its `order drop`). Move `_ended` (and the `_last` it uses) to a place both `board/times.py` and
  `history.py` import (for instance `core/records.py` or a small `core/cr_times.py`): one rule, not
  two copies.
- `shipped`: the `t` of the CR's first `ship` event (its PR opened), or `null`.
- `version`: `CrEntry.released` (the version a release CR's hand-back recorded), or `null`.

`cr_entry` needs the batch's events: `_close_files` reads them once
(`core/records.read_events(k.repo.store, k.folder)`) before the batch's own files move, and passes
them to `close_record`, which passes each CR's own events to `cr_entry`. `tests/test_order_drop_to.py`
calls `cr_entry(c, {})`: give the events parameter a default of no events so that call still works.

Nothing else changes in the record; the records already written are not touched (no migration).
`docs/planning-folder.md` (the sentence on what `chantier close --yes` keeps in each CR of the record,
"keeps in each CR of the record its `order` and its `after` list") adds: its kind, when it ended,
when its PR was first opened, and the version of a release.

### 2. The server: `history.get` and the `history` topic (Q5, Q7, Q10, Q12, Q13, Q14, Q20, Q23)

A new module, `board/history_page.py` (not `chantier/history.py`, which is the close's), reads
only; it never reads the forge, never runs git, writes nothing.

**The index.** One list of dated events per project, built from:

1. The closed records: the state's `history` list (`board/state.py:_history`, already read by
   `reads.state_of`), the records whose `state` is `closed`, each CR of `crs`:
   - with the new keys (section 1): `shipped` gives a `opened` event; `ended` gives a `release` event
     when `kind` is `release` and the result is `merged`, a `merged` event for another merged CR, a
     `dropped` event for a dropped one;
   - without them (an older record): read the CR's `archive` folder's `STATUS.json` (through the
     project's store, `repo.store`, like the rest of the board), its `steps`: the first step named
     `Shipped` with an `at` gives the `opened` event; for a merged CR, the step named `Merged` with
     an `at` gives the `merged` event. No release is told (Q9: an unmarked record shows a plain
     merged CR). A dropped CR of an older record has no recorded end (no step says it).
2. The running or paused batch (`4-batch/batch.json` and its `events.jsonl`, through
   `core/records.read_batch_json` and `read_events`, as `board/state.py` reads them): for each CR,
   `_ended` (section 1) gives its `merged`, `release` (when `kind` is `release`) or `dropped` event,
   and its first `ship` event its `opened` event.

Never a date from an archive folder's name, a batch's `opened` or `closed`, a file's time or
`delivery.md` (Q12). An event with no time is not in the index.

Each event: `kind` (`merged`, `dropped`, `opened`, `release`), `at` (UTC ISO), `cr`, `title` (one
line, `core/files.subject`), `batch` (the batch id), `pr` (the CR's PR link or `null`), `folder`
(the CR's folder relative to the planning folder: the record's `archive`, the running CR's row
folder; `null` when unknown, for instance a CR dropped back to the inbox or the backlog), and for the
three ending kinds `rounds`, `cost_usd`, `cost_unpriced`; `to` for `dropped` (the record's `to`, or
the running CR's `left_to` or `6-trash`; `null` when an older record has none); `version` for
`release` (or `null`).

Two counts come with the index:

- `undated`: the CRs of the records (closed and running) that ended (merged or dropped) with no
  recorded end time. An archived folder with no `STATUS.json` counts here (no time recorded), as do
  most of batch-01 to batch-20 today.
- `unreadable`: the records (`batch-*.json`) and the archived `STATUS.json` files present but not
  readable (an `OSError` or invalid JSON); each is skipped (Q23). `_history` today skips an
  unreadable record silently: count it there too (return the count beside the list, or recount in
  this module; the state's shape does not change).

The index is kept in `board/context.py:Context` (a new field, like `prs_done`), per project, with the
state's print it was built from (`reads.state_of(ctx, project, ask=False)` gives `(state, print)`;
with CR-429's change the print is the kept fingerprint, the same call). The same print: the index is
reused, no file is read again. So the archived `STATUS.json` files (more than three hundred today)
are read once per change of the planning folder, never per page or per push.

**A period.** Arguments: `period` (`day`, `week` or `month`), `date` (`YYYY-MM-DD`, optional: absent
means today), `tz` (an IANA time zone name, the browser's
`Intl.DateTimeFormat().resolvedOptions().timeZone`). The server works in that zone with
`zoneinfo.ZoneInfo(tz)`: the period's local limits (a day; a week from the Monday of `date`'s week to
its Sunday; the calendar month of `date`), as UTC bounds `[from, to)`; each event placed in its local
day; today read in that zone. An unknown zone or a bad date is a 400 naming the argument (the
checked-arguments path of `board/api/ops.py:call`), never a guessed zone. `zoneinfo` needs the time
zone data on Windows: add `tzdata` to `pyproject.toml`'s dependencies (pinned like the others, a
pure wheel for every system) and lock it (`uv lock`), see open question 3.

**The answer** (`board/history_page.py:answer(...)`, the same for the op and the topic):

```json
{
  "period": "week", "date": "2026-11-16", "end": "2026-11-22", "tz": "Europe/Paris",
  "from": "2026-11-15T23:00:00Z", "to": "2026-11-22T23:00:00Z",
  "today": "2026-11-21", "holds_today": true, "prev": "2026-11-09", "next": null,
  "totals": {"merged": 0, "dropped": 0, "opened": 0, "releases": 0, "cost_usd": 0.0, "cost_partial": false},
  "days": [{"day": "2026-11-21", "counts": {"merged": 0, "dropped": 0, "opened": 0, "releases": 0}, "items": []}],
  "undated": 0, "unreadable": 0, "now": "..."
}
```

- `date` is the period's first local day (the Monday, the first of the month), `end` its last.
- `next` is `null` when the period holds today or is later (Q4); `prev` is always given.
- `days`: only the days with an event (Q15), newest first; in a day, the events newest first.
- `totals`: the counts of the period's events by kind; `cost_usd` the sum of `cost_usd` of the
  period's `merged`, `dropped` and `release` events (Q14: the CRs that ended; a `opened` event adds
  nothing); `cost_partial` true when one of them has `cost_usd` `null` or a non-empty
  `cost_unpriced`. A release is counted under `releases` only, not under `merged` (open question 4);
  its cost is in `cost_usd`.

**The protocol** (an addition to protocol 1, nothing changed, Q23):

- `board/api/protocol.py`: a `HistoryArgs(_Model)` with `project: str`, `period: Literal["day",
  "week", "month"]`, `date: str | None = None`, `tz: str`; `"history.get": HistoryArgs` in `OP_ARGS`
  and `"history": HistoryArgs` in `TOPIC_ARGS`. Regenerate `board/api/protocol.json` with
  `just protocol-schema` and commit it.
- `board/api/ops.py`: `"history.get": _on_project(_history)`, which returns 200 with the answer.
- `board/api/topics.py`: the `history` topic, read like `_costs`: `rev` is a hash of the state's
  print, the arguments and today's date in `tz` (so the value is computed only when one of them
  changes, and a client watching today gets the new day after midnight); a past period's value does
  not change while no record or step of it changes (Q20).
- The project state (`project.state`, the `project` topic) gains nothing (Q23).
- `docs/server-api.md`: a row `history.get` | `project`, `period`, `date`?, `tz` | the period's
  events by local day, its totals, `undated`, `unreadable` (the answer's keys) in "The ops", and a row
  `history` | the same arguments | what `history.get` gives in "The topics", with one sentence: read
  only from the records and the archived CRs' steps, never the forge.

AGENTS.md does not change: the server already serves "the record and the planning folder's files";
this reads them and publishes them through the same API.

### 3. The web client: the History view (Q1, Q3 to Q7, Q12 to Q22)

- **`clients/web/js/views/registry.js`**: import `* as history from './history.js'`; one entry
  `{ id: 'history', icon: 'history', word: 'nav.history', module: history }` placed right after the
  `prs` entry and before `costs` (Q21; open question 2). No `count`, no `overview` (Q19: on "All
  projects" it opens on the last real project, the router's existing rule).
- **`clients/web/js/ui/icons.js`**: a `history` icon in the style of the others (a stroke path, for
  instance a clock with a back arrow); `clock` stays.
- **`clients/web/js/core/router.js`**: the History view's place in the address (Q6):
  `HISTORY_PERIODS = ['day', 'week', 'month']`; `hp=<period>` (absent: `day`) and `hd=<YYYY-MM-DD>`
  (absent: today), read by `resolve` only when `view === 'history'` (a value not in the list, or not
  a date, reads as absent), written by `href` only on that view and only when not the default, kept
  in the state as `historyPeriod` and `historyDate` (added to `apply`, `go` through a `historyOf`
  helper like `prsOf`, and to `reset`). The browser's Back walks the periods because each move is a
  `go(...)` (a `pushState`). Update the file's head comment, which lists the address's keys.
- **`clients/web/js/views/history-feed.js`** (like `prs-feed.js`): subscribes to the `history` topic
  with `{project, period, date?, tz}` through `core/transport.js`'s `subscribe` (DESIGN.md "One
  transport"), keeps the answer in the store (`historyPage`, reset with the project), drops the
  subscription when the page is hidden and takes it back when shown, starts a new feed when the
  period changes, and on a refused read keeps the last good answer with the error. So a CR merged
  while the page shows today appears without a reload (Q20).
- **`clients/web/js/views/history.js`** draws, top to bottom:
  - the head: the period's name in the board's language (Q5), formatted with `Intl.DateTimeFormat`
    in the board's language (`model/words.js:language()`): a day as its full date, a week as
    `history.week_of` ("Week of {date}" / "Semaine du {date}") with the Monday's date, a month as
    "<month> <year>"; then the three period choices (day, week, month: the existing chip used as a
    toggle, DESIGN.md "One card, one column, one chip"), the previous arrow, the next arrow
    (disabled when `next` is `null`), and the Today button (it removes `hd`, keeps `hp`); previous
    and next go to the answer's `prev` and `next`;
  - the totals: five plain figures (`history.merged`, `history.dropped`, `history.opened`,
    `history.releases`, `history.cost`), the cost labelled as the CRs' cost, with `~` or the board's
    existing partial mark as Costs shows it when `cost_partial`, and under it one short note
    (`history.cost_note`: the steering and grill costs of a batch are not spread over days) with a
    link to the Costs view (`go({ view: 'costs' })`);
  - the list: for each day of `days`, a small head (the local date and the day's counts), then one
    row per event: the local time (`core/format.js:hhmm`), the kind as a chip (merged, dropped, PR
    opened, release; the state chip's existing variants and tints only: merged, blocked or queued for
    dropped, draft or working for opened, ready for release, no new colour), the CR's number, its
    title on one line with an ellipsis and its full text in `title` (DESIGN.md "One-line titles"),
    the batch's name, and for an ended CR its rounds and cost; a dropped CR says where it went
    (`history.to_trash`, `history.to_inbox`, `history.to_backlog` with the priority) when `to` is
    known; a release shows its version when known;
  - an empty period: the totals at zero and, in place of the list, the board's usual empty line with
    `history.empty` ("Nothing done in this period" / "Rien de fait sur cette période") (Q16);
  - the foot: when `undated` > 0, one quiet line (`history.undated`, plural through `tn`: "{n} CRs
    have no recorded date" / "{n} CR sans date enregistrée") with a link to Costs (Q12); when
    `unreadable` > 0, one line `history.unreadable` ("{n} files could not be read and were skipped").
  - while the first answer is not there: the existing `stats.loading` empty line.
- **What a row opens (Q17)**, through `ui/open.js`'s `opener` and `bindOpen` on the view's root: a
  click (or Enter, Space) on a row opens its CR in the side panel. A CR of the running batch uses the
  existing key `c:<CR>`; any other uses a new key `h:<CR>` that `model/targets.js:targetFor` resolves
  from `state.historyPage`'s events to a `done` target whose `folder` is the event's `folder`. A row
  whose `folder` is `null` is not an opener (plain row, nothing to open). The PR number
  (`core/format.js:prNumber`, the forge's word through the existing forge-aware keys, as the PRs page
  does) is an `<a target="_blank" rel="noopener">` to `safeUrl(pr)`, its click not opening the
  panel. The batch's name is a button that goes to the Batch view on that batch
  (`go({ view: 'batch', batch })`).
- **Words**: new files `clients/web/js/i18n/en-history.js` and `fr-history.js`, merged into
  `en.js` and `fr.js` like the other parts, with every `history.*` key above, plus `nav.history`
  ("History" / "Historique") in `en.js` / `fr.js` beside the other `nav.*` keys. French uses "tu" as
  the other files do. Data (titles, ids, versions) is shown as it is.
- **The sheet**: `clients/web/css/views/history.css`, linked in `clients/web/index.html` after
  `prs.css`: layout only (grid or flex, gaps, sizes), tokens only, no literal, no new token, no side
  border, never restyling the chip (DESIGN.md "Tokens", "Components"). On a narrow screen (below
  `--phone-max`) the row wraps like the PRs page's rows (`css/views/prs.css`): the title takes the
  line, the batch and cost go under it.
- **Unchanged (Q21)**: Home (`views/home-history.js` and the rest), the Costs page's batch list
  (`views/costs-history.js`), the Batch navigator. The phone's bottom bar and the sidebar list the new
  view through the registry, with no change of their own.

### 4. DESIGN.md (Q22)

`clients/web/DESIGN.md` gains a section after "Waits on a card", **"History"**: a read-only view,
fed by the `history` topic only (no field of the project state); its rows are words, the existing
chip and one-line titles; no chart (charts are not this page's); no new token, component or colour;
its every word an i18n key of `en-history.js` / `fr-history.js`. The Tokens and Components tables do
not change; no protected feature is added. `tests/test_board_design.py` keeps passing.

### 5. The user docs

`docs/web-board.md`: a short "History" section (what the page shows, the period selector, where the
data comes from, the CRs with no recorded date, the PR ready time not shown). `docs/server-api.md`:
section 2.

## Out of scope

Charts, curves, medians, cycle times, spend by source, rankings and any comparison with another
period (the Dashboard pages CR's, Q2, Q13); a year view or a free date range (Q3); a PR's ready time
(Q8); the forge's tags and publications (Q9); CRs that never entered a batch (trashed from the
backlog) (Q25); filters and search (Q18); "All projects" (Q19); an export; any edit; any change to
Home, Costs or the Batch navigator (Q21); rewriting the records already written (Q11); a link to the
Dashboard page, and from it (open question 1); no change to the CR board pane (`hooks/`,
`STATUS.json`), the cards, the agents or AGENTS.md.

## Known gaps

- A PR made ready (out of draft) is not shown: no record keeps that time once its batch is closed
  (the batch's events are not archived). Nothing is guessed in its place (Q8).
- A CR of an older record whose end has no recorded time (most of batch-01 to batch-20, and the
  dropped CRs of every record written before this change) is in no period; the foot line counts
  them (Q12). Its first ship still shows as a `opened` line when its steps date it.
- A CR dropped back to the inbox or the backlog has no folder in the record: its row opens nothing.

## Overlaps in batch-30 and the UI night

- **`js/views/registry.js`, `js/i18n/en.js` / `fr.js` (`nav.*`), `js/ui/icons.js`, `index.html`**:
  also edited by CR-439 (Help: `help` after `inbox`), `board-user-inbox` (Inbox second, after Home)
  and `dashboard-pages` (Dashboard after Costs, before Configuration). Each adds its own line; no
  dependency, whichever lands second rebases. The intended order once all have landed: Home, Inbox,
  Help, Triage, Kanban, Batch, PRs, History, Costs, Dashboard, Configuration.
- **`js/core/router.js`**: CR-434 (the Batch page's tab) and `board-batch-view` may touch it; this
  CR adds its own keys and a `historyOf` helper beside `prsOf` and `tabOf`.
- **`DESIGN.md`**: CR-427 and CR-440 edit the "One card, one column, one chip" rule, CR-434 other
  lines, CR-439 a Help section, `dashboard-pages` a chart component; this CR adds only its own
  section after "Waits on a card".
- **`board/api/protocol.py`, `protocol.json`, `docs/server-api.md`**: CR-427 edits `docs/server-api.md`
  (`backlog.move`), CR-429 its "The topics" paragraph (how the server looks); this CR adds one op row
  and one topic row. Whoever lands second regenerates `protocol.json` with `just protocol-schema`.
- **`board/reads.py:state_of` and `board/context.py`**: CR-429 changes how the print is computed;
  this CR only reads the print `state_of` returns and adds a field to `Context`, so it works on
  either side of CR-429.
- **`board/times.py`**: `_ended` moves (section 1); CR-433, CR-434 and CR-435 (the Batch page) read
  `cr_times`, whose output does not change.
- **CR-440 (Triage polish)**, **board-griller**: no shared file expected.

## Evidence

Tests (`tests/test_board_history.py`, in-process, prepared planning folders, parametrized, fast):

1. **Local day placement** (Q5), zone `Europe/Paris`: an event at `2026-11-20T23:30:00Z` is in the
   day `2026-11-21`; on the DST change, an event at `2026-10-25T22:30:00Z` is in `2026-10-25` and one
   at `2026-10-25T23:30:00Z` in `2026-10-26`; the day `2026-10-25` has bounds
   `2026-10-24T22:00:00Z` to `2026-10-25T23:00:00Z` (25 hours). One case in `America/New_York`.
2. **Week and month limits** (Q5, Q4): `period=week, date=2026-11-21` (a Saturday) gives `date`
   `2026-11-16`, `end` `2026-11-22`, `prev` `2026-11-09`, `next` `2026-11-23`; a week holding today
   gives `next` `null`; `period=month, date=2026-11-21` gives `2026-11-01` to `2026-11-30`, `prev`
   `2026-10-01`; `period=day` with no `date` is today in the zone.
3. **Totals and cost** (Q13, Q14): a prepared closed record with the new keys (a merged CR, a dropped
   CR with `to: 2-backlog/P2`, a release CR with `version`, one CR with `cost_usd: null`) gives the
   expected counts, the release under `releases` only, `cost_usd` the sum of the ended CRs, an
   `opened` event adding nothing, `cost_partial` true.
4. **Older records** (Q9, Q11, Q12): a closed record without the new keys whose archived
   `STATUS.json` has `Shipped` and `Merged` steps gives `opened` and `merged` events at those times
   and no release even for a CR titled "release"; a dropped CR and a merged CR with no `STATUS.json`
   count in `undated` and are in no period; a `STATUS.json` with invalid JSON and an invalid
   `batch-*.json` count in `unreadable`.
5. **Running batch** (Q10, Q20): a CR merged in `4-batch/` (an `order merged` event) and a first
   `ship` show today; after a new event is written, the topic's `rev` changes; for a past period it
   does not.
6. **The index is reused** (Q23): a second `history.get` with the same print reads no `STATUS.json`
   (count the reads with a monkeypatched store read); a change of the planning folder rebuilds it.
7. **The protocol**: `history.get` with `period: "year"`, a bad `date` or an unknown `tz` is 400
   naming the argument; the existing test that checks `protocol.json` against the models passes on
   the regenerated file; `project.state`'s keys are unchanged.
8. **The close** (section 1): `cr_entry` with events gives `kind`, `ended`, `shipped`, `version`;
   `tests/test_order_drop_to.py` still passes with its call without events.
9. **The shipped client files**, read from the repository as they ship at the head under test (not a
   prepared copy): `js/views/registry.js` has a `history` entry right after `prs`;
   `js/i18n/en-history.js` and `fr-history.js` define the same keys, and the existing language check
   covers them; `css/views/history.css` passes the design tests (`tests/test_board_design.py`); the
   biome check of `just check` passes on the new JS.

The scenario (`scenario/run_scenario.py`, the close check "its CRs carry the result, an archive that
exists, the PR, the rounds and the cost"): add that every CR of the record has a `kind`, every
merged CR an `ended` and a `shipped` instant, and a dropped CR an `ended` instant. The CR changes the
CLI, so the pipeline's `just scenario (ubuntu-latest)` job is green at the PR's head before the PR
(AGENTS.md); `just check` and `just eval-dry-run` before the first push.

Measures and screenshots in the PR's Deliverables (Q23, Q24), on the real planning surface
(`gsemet-foss-planning-surface`, project `chantier`), the board served from the PR's head:

- `history.get` for the month of November 2026 (`curl` on `api/v1/call/history.get`, as
  `docs/server-api.md` shows), first call and second call, each time printed; the page shows the
  month with no visible wait.
- Screenshots: a day (today), a week, a month, and an empty period (a day of batch-05's time, for
  instance, with the foot line), in English, and one in French.

Host and default matrix: none (the page does not depend on the host or on a configured value).

## Open questions (built as A)

1. **History and Dashboard links.** History's grill (Q2) says Dashboard links to History; the
   Dashboard pages CR's grill (dashboard-Q14) says neither links to or depends on the other.
   A (recommended, built): no link either way; History draws none, and Dashboard is not asked for
   one. B: Dashboard links to History (its own CR builds it). C: links both ways.
2. **Sidebar order.** History's grill (Q21) puts History after PRs and before Costs; Dashboard's
   (dashboard-Q2) says "Costs, History, Dashboard". A (recommended, built): History after PRs,
   before Costs, as its own grill says; Dashboard stays after Costs. B: Costs, History, Dashboard.
3. **Where the local day is computed.** A (recommended, built): on the server, in the browser's
   IANA zone (`tz`), with `zoneinfo` and the `tzdata` dependency added and locked (needed on
   Windows), so the tests of Q24 run in pytest. B: in the browser, with no new dependency, but the
   client has no test runner, so Q24's tests of the local day and the week's limits cannot be
   written. C: the browser sends a fixed UTC offset: wrong across a DST change.
4. **A release in the totals.** A (recommended, built): a release CR's merge counts under
   `releases` only, not under CRs merged; its cost is in the period's cost. B: it counts under both.
5. **A missing archived STATUS.json.** A (recommended, built): an archived folder with no
   `STATUS.json` counts as "no recorded date" (most old batches); only a file present but unreadable
   counts as unreadable. B: a missing file counts as unreadable too (about two hundred today, a
   loud line on every page).
