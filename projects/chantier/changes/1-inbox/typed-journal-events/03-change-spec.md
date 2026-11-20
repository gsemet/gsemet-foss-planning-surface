# Change Specification: typed journal events, `name@N` (Part A of seven)

Origin: verbal (2026-11-10, Beads study; grilled 2026-11-20). No tracker issue.

This CR is Part A, typed events, of the seven-part work the user split into seven CRs
(planning-server-Q7, 2026-11-20). Its reference is
`../../2-backlog/P3/planning-server/experiments/03-change-spec-all-parts.md` (§1 to §4, "Part A.
Typed events", the docs map of §2, §5 to §9), with every answer of
`../../2-backlog/P3/planning-server/02-answers.md` folded in, and the five answers of this CR's own
`./02-answers.md` (2026-11-20, settled by the Chief of Staff: the open questions of this
specification's first pass). Part C, the writer, is specified and
approved in `../../2-backlog/P3/planning-server/03-change-spec.md`; its §2 table names what it needs
from this CR (§2 below). This file is self-contained: a Driver needs nothing else.

## 1. Goal, in the user's terms

Among the five ideas the user took from Vercel Board, built in chantier with no Board dependency
("tout", 2026-11-20, Q3): **typed journal events, `name@N`, a published version never changing.**
Each line of a project's event journal (`forge-journal.jsonl`) carries a type `name@N` whose
published schema never changes; a change is a new `name@N+1`. So an older session reads what a
newer one writes: it knows the types it knows, and counts and skips the others without waking
anyone.

The journal stays chantier's own channel between sessions (Q1-Q2: messages and plan storage are two
things; chantier's journal, surface server and watchers stay the channel; no Board dependency,
hosted or local). This CR extends that journal; it adds no new channel.

## 2. Dependencies and neighbours

This CR needs nothing merged first (the reference's §2 table: Part A, "Needs: none").

Three CRs need it, and build on it as follows:

| CR | What it takes from this one |
| --- | --- |
| `2-backlog/P3/planning-server` (Part C, the writer, approved) | its §2 table, word for word: "the journal's version 2 line, `type: "name@N"`, `hub/schemas.py`'s `PUBLISHED` and the shipped `hub/schemas.json` checked by `test_event_types.py`; `journal.append` validating each payload". Part C then adds the source `writer` and publishes four types: `sync-conflict@1`, `sync-blocked@1`, `sync-late@1` (each wakes a watcher) and `sync-resumed@1` (wakes no one). |
| `1-inbox/driver-leases` (Part D) | publishes `lease-expired@1` (written by the hub, wakes a watcher). |
| `1-inbox/typed-waits` (Part E) | publishes `wait-cleared@1` (written by the hub, wakes a watcher). |

So that each of them adds a type with no change to this CR's design, a published type is, in one
place (`hub/schemas.py`): its model, its `PUBLISHED` entry, whether it wakes a watcher (yes, no, or
by a field of its payload, as `board@1`'s `wakes`), and its text (`event_text`); plus its entry in
the shipped `hub/schemas.json`. A new source is one more value of `SOURCES`. The test of §6 covers
every type in `PUBLISHED` with no change when a later part adds one.

Not a neighbour: `board-journal.jsonl` (`board/journal.py`, the board's own toast journal, with its
own `kind` field: `new`, `move`, ..., `rescan`) is another file and does not change.

## 3. Decisions carried from the answers

| Decision (date) | Where it lands |
| --- | --- |
| Messages and plan storage are two things; no Board dependency, hosted or local; chantier's journal, surface server and watchers stay the channel (11-20, Q1-Q2) | §1; this CR extends the existing journal (`hub/journal.py`), one file, one append function |
| All five Board ideas go in this work, among them typed journal events `name@N`, a published version never changing (11-20, Q3, "tout") | §4 to §6 |
| "Not studied enough, specify everything"; go into the detail of every state and every message (11-20, Q6 and the answer before it) | every line form, refusal and text of §5 |
| Q7: seven separate CRs; A and B first (A needs none), then C, then D to G (11-20) | §2 |
| A coherent split, docs and SVGs included: each part changes the docs and diagrams (with their `-texts.md`) its change makes false, in the same CR as the behaviour (11-20) | §7 (docs; no diagram is made false, searched) |
| Part C approved, staying in the backlog until Parts A and B are specified; the three go to `3-ready` on the user's word (11-20) | §2; this specification is one of the two Part C waits for |
| Mixed versions: an earlier chantier reading version 2 lines counts them and wakes no one (the reference's §8, carried into Part C's §8) | §5.4, §9 |
| This CR's answer 1: each model fixes each field's JSON type and only the formats that cannot change (`cr` is `CR-<n>`, `head` a 40-character hex SHA); the open sets (`board@1.action`, `config@1.key`) stay plain strings, so a new board action or configuration key forces no new published version (11-20) | §5.1, §6 |
| This CR's answer 2: "`config` line" and "`board` line" become `config@1` / `board@1`, and AGENTS.md's `by: board` becomes `source: board`, in AGENTS.md, `chief-of-staff.md`, `hosts/claude-code.md` and `hosts/copilot.md`, so that no text names the old words (11-20) | §8, §6 |
| This CR's answer 3: `docs/web-board.md`, "The signal": its wording fixed too (`config@1`, `source:`) (11-20) | §7 |
| This CR's answer 4: `test_event_types.py` compares a normalized form of each schema (the properties, their JSON types, `required`, the patterns), not pydantic's raw output; a generator-only change regenerates nothing and publishes nothing (11-20) | §5.2, §6 |
| This CR's answer 5: a `just` recipe writes the missing entries of `schemas.json` from `model_json_schema()` and never changes an existing one; the test checks the file (11-20) | §5.2, §6, §9 |

## 4. Words

- **Event type:** `name@N`, the name and the published version of a journal line's payload
  (`merged@1`). The name is lower-case words joined by `-`; `N` is a whole number from 1.
- **Published type:** a type in `hub/schemas.py`'s `PUBLISHED`, with its JSON Schema in the shipped
  `hub/schemas.json`. A published `name@N` never changes (its fields, their types, which are
  required); a change is a new `name@N+1`, published beside it.
- **Effective type:** the type `read` gives a line: its `type` for a version 2 line, `<kind>@1` for
  a version 0 or 1 line.
- Unchanged words: `seq`, `source` (who wrote a line, never what it is), `audience` (for whom),
  "wakes a watcher".

## 5. What changes

### 5.1 New: `hub/schemas.py`

`skills/chantier/scripts/cli/src/chantier/hub/schemas.py`:

- One pydantic model per published type, each with `model_config = ConfigDict(extra="forbid",
  frozen=True)` (pydantic 2.14.3 is already the CLI's dependency, `pyproject.toml`).
- `PUBLISHED`: a mapping `"name@N" -> model`.
- `validate(type, payload)`: checks the payload (the line's fields after the header) against its
  model; raises `ValueError` on a type not in `PUBLISHED` or a payload its model refuses (an extra
  field, a missing required field, a field of a wrong JSON type).
- Each type's wake rule and text, as §2 says (one place per type).

The four types this CR publishes are the version 1 kinds frozen as they are today; their payloads
do not change (the fields as `hub/journal.py`'s docstring and its writers give them today):

| Type | Payload | Written by (today's writer) | Wakes a watcher |
| --- | --- | --- | --- |
| `merged@1` | `batch`, `cr`, `pr`, `into`, `into_cr`, `merged_at`, optional `landed_with`, `landed_at` (both present once the base landed, else both absent) | hub (`hub/cycle.py`), board (its PRs page, `board/prs.py`), through `journal.merged_events` | yes |
| `checks-red@1` | `batch`, `cr`, `pr`, `head` (the PR head's full SHA) | hub, through `journal.red_event` | yes |
| `config@1` | `key` (a dotted path: `batch.slots`, `specifying.parallel`, `hosts.<host>.roles.<role>.<agent\|model\|escalation>`), `old`, `new` (effective values, null for inherited), `batch` (the batch running or paused at the save, or null) | board (its Configuration page, `board/config_api.py`'s `_event`) | yes |
| `board@1` | `action` (the board journal's kind: `new`, `move`, `edit`, `label`, `group`, `ungroup`, `next-batch`), `items` (slugs), `text`, `wakes` (true for `new`, `move` and `edit`) | board (its backlog writes, `board/write_api.py`, through `journal.board_event`) | when `wakes` is true |

How strict a model is (this CR's answer 1). Each field's JSON type is what today's writers put in
it, null included where a writer may write null (`into_cr` of a merge into a branch that is no
CR's, `into` when the read gives no branch, `old`, `new` and `batch` of `config@1`). Beyond the
type, a model fixes only the formats that cannot change:

- a CR id matches `^CR-[0-9]+$`: `cr` of `merged@1` and `checks-red@1`, and, being CR ids too,
  `into_cr` and `landed_with` of `merged@1` when they are not null;
- `head` of `checks-red@1` matches `^[0-9a-f]{40}$` (the full SHA the hub writes today).

Every other field is a plain string (or its JSON type), with no enum and no pattern:
`board@1.action` and `config@1.key` above all (open sets: a new board action or configuration key
needs no new published version), and `batch`, `pr`, `into`, the times, `text`, `items`' slugs.

### 5.2 New: `hub/schemas.json`, shipped

`skills/chantier/scripts/cli/src/chantier/hub/schemas.json`: the JSON Schema
(`model_json_schema()`) of every published type, keyed by `name@N`, keys sorted, UTF-8 without
BOM, LF line ends, a final newline. It is the published record: the test of §6 fails when a
model's schema differs from its entry in normalized form (below). It ships in the wheel with the package (hatch packages the
non-Python files of `skills/chantier/scripts/cli/src/chantier`, as it does
`playbook/copilot-models.json`). The CLI does not read it at run time: validation uses the models.

The file is written by a new recipe, `just journal-schemas` (this CR's answer 5), run by hand and
not part of `just check` (as `copilot-models` is). It runs `scripts/journal_schemas.py` through
`{{run-cli}}`, as the justfile's other script recipes do. For each type in `PUBLISHED` that the file
lacks, it adds the entry from the model's `model_json_schema()`; it keeps every existing entry as it
is (never rewritten, never removed, even when its model's schema now differs from it); it writes the
file in its canonical form (keys sorted, UTF-8 without BOM, LF, a final newline; the indentation is
the Driver's choice, fixed by the test). It prints one line per entry added (`schemas.json: added
<name@N>`), and one per existing entry whose normalized form (below) differs from its model's, which
it leaves unchanged (`schemas.json: <name@N> differs from its model: publish <name@N+1> instead`);
with neither, it prints nothing. The function that merges the entries lives in `hub/schemas.py`, so
the test calls it in-process; the script only reads, merges and writes the file. This CR writes its
four entries with that recipe; a later part (C, D, E) adds its model to `PUBLISHED` and runs it.

The **normalized form** of a schema (this CR's answer 4) is what the test and the recipe compare:
for each property, its JSON type or types (null included), its `pattern` when it has one, and, for
an array, the same of its items; plus the set of `required` properties. Titles, descriptions, the
naming of `$defs`, the order of keys and of `anyOf` branches, and any other output of the generator
are not part of it. So a pydantic upgrade that only changes how a schema is written fails nothing,
regenerates nothing and publishes nothing; a change of a property, a type, a required property or a
pattern fails the test.

### 5.3 The line, version 2

`hub/journal.py`'s `VERSION` becomes 2. A version 2 line holds, in this order: `v` (2), `seq`, `t`,
`type`, `source`, `audience`, then the payload of its type. No `kind` field.

```json
{"v":2,"seq":41,"t":"2026-11-18T10:02:03Z","type":"merged@1","source":"hub","audience":["project"],"batch":"batch-29","cr":"CR-12","pr":"#88","into":"main","into_cr":null,"merged_at":"2026-11-18T10:01:40Z"}
```

`source` is one of `hub`, `board`, `cli` (as today; Part C adds `writer`). `audience` is as in
version 1 (a non-empty list of `project`, `role:<name>`, `cr:<id>`, `session:<key>`, `user`;
every writer of today writes `["project"]`). `seq`, `t`, the lock and the encoding are unchanged.

### 5.4 Writing: `journal.append(repo, events, source)`

- An event is `{"type": "name@N", "audience"?: [...], ...payload}`. `merged_events`, `red_event`,
  `board_event` (`hub/journal.py`) and `_event` (`board/config_api.py`) build `type` in place of
  `kind`: `merged@1`, `checks-red@1`, `board@1`, `config@1`.
- Before it takes the lock, `append` checks every event and raises `ValueError` (a code fault, as
  today) on: a source not in `SOURCES`; a type not in `PUBLISHED`; a payload its model refuses; an
  audience of a wrong form. Nothing is written when one event of the call is refused (as today: the
  checks run before any write). The message starts `journal ` as today's do (`journal source ...`,
  `journal type ...`, `journal payload <type>: <pydantic's first error>`, `journal audience ...`).
  The table's "Written by" column describes today's writers: `append` does not refuse a published
  type from another valid source (as today, where any source may write any kind).
- It keeps its lifecycle lock (`changes_lock`), its `seq` (the highest readable `seq` plus one), its
  duplicate rule and its single write per call.
- The duplicate rule (`_key`) dispatches on the effective type's name, with today's keys: `merged`
  by batch, CR and landed-or-not; `checks-red` by batch, CR and head; `config` and `board` never
  duplicates (each line its own event). So a version 1 `merged` line written by an older board or
  hub and a version 2 `merged@1` line of the same batch, CR and landed-or-not are one event: the
  second is skipped. A line of a newer version, of an unknown type or with a refused payload
  (§5.5) is never a duplicate of anything.
- It stays the one writer path: every writer (hub, board, CLI, and Part C's writer later) goes
  through it; `test_event_audience.py`'s `test_no_role_is_named_and_the_journal_has_one_writer`
  keeps holding.

### 5.5 Reading: `journal.read(changes)`

`read` keeps its signature and its three results (the lines that are JSON objects, the numbers of
the lines listed as unreadable, the `(number, version)` of the newer lines). Every line it returns
carries an effective `type`:

- **Version 0** (no `v`): `type` is `<kind>@1`, `source` its `by`, audience `["project"]` (as today
  for source and audience). Never rewritten.
- **Version 1**: `type` is `<kind>@1`; source and audience as today (`project` when it has none).
  Never rewritten. A version 0 or 1 line is not checked against the models: it is read as today.
- **Version 2, published type, payload its model accepts**: as written.
- **Version 2, type not in `PUBLISHED`** (a newer chantier wrote it) **or payload its model
  refuses**: it is returned with an empty audience (so it is for no one and wakes no one, as a
  newer line is today), it counts for `seq` (`last_seq` reads it), and its number is in the second
  result, with the lines that are not JSON objects. `status` names it as it names them today:
  `forge-journal.jsonl: line <n> unreadable`.
- **`v` above 2**: as today's newer line: counts for `seq`, empty audience, in the third result;
  `status` prints `forge-journal.jsonl: line <n> is version <v>, newer than this chantier: update
  it`.

The readers dispatch on the effective type, never on `kind`:

- `waking(e)`: by the type's wake rule (§5.1): `merged@1`, `checks-red@1`, `config@1` wake;
  `board@1` wakes when `wakes` is true; a line of no published type wakes no one.
- `lines(...)` (the `status` lines): the `merged@1` lines of the batch's open CRs (the landed one
  wins), then the newest `batch.slots` `config@1` line, by today's rules (`_slots_line`).
- `watch` (`hub/watch.py`) and `watch --once --after <seq>` print the lines for them through
  `event_text`, as today; the cursor passes every line, those of an unknown type and the refused
  ones included.

### 5.6 Texts: `event_text`

`event_text` dispatches on the type's name (`merged`, `checks-red`, `config`, `board`). The texts of
the four existing kinds do not change, character for character (`merged_text`, `red_text`,
`config_text`, `board_text`). The texts of the later types are their parts' (Part C's C.10, Part
D's D.7, Part E's E.5).

### 5.7 Docstrings

The module docstring of `hub/journal.py` is rewritten for version 2: the line's fields in order,
`type` as `name@N`, the four published types and their payloads (or a pointer to `hub/schemas.py`
for them), the rule "a published `name@N` never changes, a change is a new `name@N+1`, its schema
in `hub/schemas.json`", the reading of versions 0 and 1 (`<kind>@1`, never rewritten), and of a
version 2 line of an unknown type or a refused payload (counts for `seq`, wakes no one, listed by
number). The docstrings that say `kind` of a forge-journal line (`hub/journal.py`'s functions,
`board/config_api.py`'s `_event`: "The forge journal's `config` line") say the type.

### 5.8 What does not change

The file's name and place, its local status (ignored by git), the lock, `seq`, the audience values
and the watcher's filter, the watcher's end rule (`events.wake_every`, 20 s after the last waking
event), the texts, who writes which line and when, `status`'s and the watcher's outputs for the
four existing types, `board-journal.jsonl`, the batch's `events.jsonl` (no type there: §10).

## 6. Evidence

All under `skills/chantier/scripts/cli/tests/`, calling the CLI in-process (AGENTS.md: few,
parametrized, fast).

- `test_event_types.py` (new):
  - reads the shipped `hub/schemas.json` from the repository at the head under test (the file in
    `src/chantier/hub/`, as `test_event_audience.py` reads `SRC`), never a copy or a prepared text,
    and compares the normalized form (§5.2) of each entry with that of `model_json_schema()` of
    every model in `PUBLISHED`: an entry whose normalized form differs, or a published entry with
    no model, fails with `published schema <name@N> changed: publish <name@N+1> instead`; a model
    with no entry fails with `schema <name@N> not published in schemas.json: run just
    journal-schemas`. It also checks the file's text is its canonical form (keys sorted, UTF-8
    without BOM, LF, the final newline);
  - the normalized form, on prepared schemas (a case the shipped file cannot hold, named as such):
    two schemas that differ only in what the generator writes (a title, a description, the order of
    keys or of `anyOf` branches) normalize the same; a changed type, a property added or removed, a
    `required` change and a pattern change each normalize differently;
  - the recipe's merge (§5.2), in-process: on a prepared file (a case the shipped file cannot hold)
    with one published entry missing and one existing entry that differs from its model, it adds the
    missing entry from its model, keeps the differing one and every other one byte for byte, names
    the differing one, and writes the canonical form; on the shipped file it adds nothing and
    changes nothing;
  - the formats of answer 1, on the shipped models: `merged@1` and `checks-red@1` with `cr`
    `CR-1` accepted, with `cr` `x` refused; `merged@1` with `into_cr` `x` refused; `checks-red@1`
    with a 40-character hex `head` accepted and a 7-character one refused; `board@1` with an
    `action` no board writes today (`archive`) and `config@1` with a `key` no configuration holds
    today (`x.y`) accepted;
  - parametrized over every published type (from `PUBLISHED`, so the later parts' types join with
    no change to the test): a valid payload appends one version 2 line with `v`, `seq`, `t`,
    `type`, `source`, `audience` first and in that order; a payload with an extra field, and one
    with a required field missing, each raise `ValueError` and write nothing (the journal file
    absent or unchanged);
  - a prepared journal (a case the shipped file cannot hold, named as such): a version 0 line, a
    version 1 line of each of the four kinds, a version 2 line of an unknown type
    (`nothing-known@1`) and a version 2 `merged@1` line with a refused payload. `read` gives the
    effective types (`<kind>@1`), the unknown and refused lines are listed by number in the second
    result, `last_seq` counts them, and `watch --once --after 0` prints only the known lines;
    `status` names the two lines by number;
  - the duplicate rule across versions: on a prepared version 1 `merged` line, an `append` of the
    same merge as `merged@1` writes nothing; `checks-red@1` likewise by head.
- `test_event_audience.py`: its version 1 expectations become version 2 (`HEAD` with `type` in
  place of `kind`, `v` 2; the refused-kind case becomes a refused type; its "newer line" case uses
  `v` 3, since 2 is now known). It keeps passing.
- `test_watch_events.py`: its event dicts use `type`; it keeps passing.
- The other tests that build events or read the journal's `kind` switch to `type` (event dicts)
  or the effective type (read lines): `forge_world.py`, `test_board_config.py`,
  `test_board_journal.py`, `test_board_prs.py`, `test_forge_hub.py`, `test_surface_server.py`,
  `test_watcher_autostart.py` (it builds events with `red_event`). Their behaviour is unchanged; a
  prepared value the formats of answer 1 now refuse (a `cr` that is not `CR-<n>`, a `head` that is
  not 40 hex characters) becomes a valid one.
  Their docstrings that name a line by its kind word (`test_board_journal.py`'s "one `board`
  line", `test_watch_events.py`'s "`config` lines") say the type (`board@1`, `config@1`).
- The renames of §8, checked by the Driver before the push: a search of `AGENTS.md` and
  `skills/chantier/references/` for `` `config` line``, `` `board` line``, `` role `config` ``,
  `` two-key `config` `` and `by: board` finds nothing. The tests that read the shipped cards
  (`test_plugin_files.py`, `test_startup_manifest.py`, and any other that holds one of the renamed
  texts: the Driver searches `tests/` for them) are updated where they hold them, and stay green.
- `just journal-schemas` run at the PR's head prints nothing and leaves `git status` clean.
- Scenario (`scenario/run_scenario.py`): the `surface-board` checks that read
  `forge-journal.jsonl` by hand (today `(e["v"], e["source"], e["audience"], e["kind"], ...) ==
  (1, "board", ["project"], "board", ...)` and `e["kind"] == "merged"`) read version 2 lines:
  `v` 2 and `type` `board@1` / `merged@1`. `scenario/README.md` changes only if a text it holds
  names the line's `kind` or version (the Driver checks).
- Host and default matrix: none. What this CR changes depends neither on the host nor on a
  configured value (the reference's §5 has no Part A row).
- No CI job is added or changed.
- The project's gates (AGENTS.md): `just check`; `just test` within its budget (at most 30 s
  above 18.5 s); `just eval-dry-run` (the change is under the CLI's `src/`); `just scenario` green
  on the pipeline's `just scenario (ubuntu-latest)` job at the PR's head, and, when this CR is on
  top of its batch's stack, locally on Windows too (`chantier gate`).

## 7. Docs

Each change in this CR, with its behaviour.

`docs/planning-folder.md`, "The event journal" (only these; Parts C, D and E add their own rows and
sentences later, the reference's docs map):

- The example line becomes a version 2 line (`"v": 2, ..., "type": "merged@1", "source": "hub",
  ...`).
- The field table: `v` (2; 0 and 1 still read); `type` (`name@N`, in place of the `kind` row: the
  published type, then the fields of that type); `source` and `audience` as today.
- One sentence: a published `name@N` never changes, a change is a new `name@N+1`, and every type's
  JSON Schema ships in `hub/schemas.json`.
- The older-lines paragraph: a version 0 or 1 line's `kind` is read as `<kind>@1` and never
  rewritten (version 0's `by` is its source and it is for the project, as today); a version 2 line
  of an unknown type or a refused payload counts for `seq`, wakes no one and `status` names it by
  number; a line of a newer version, as today.
- The sentence "Every line written today is for `["project"]`: `merged` and `checks-red` ..." names
  the types: `merged@1` and `checks-red@1` by the hub or the board's PRs page, `config@1` by the
  Configuration page, `board@1` by the backlog writes.
- A new table, "Type | Written by | Wakes a watcher", with this CR's four rows: `merged@1` (the
  hub, the board's PRs page; yes), `checks-red@1` (the hub; yes), `config@1` (the board's
  Configuration page; yes), `board@1` (the board's backlog writes; when `wakes`, true for `new`,
  `move` and `edit`). Parts C, D and E each add their rows to it.

`docs/web-board.md` (the behaviour these describe does not change; only the names follow the
published types):

- "PRs", "The signal" (this CR's answer 3): the line it appends is a `merged@1` line; "a line of
  its own kind (`config`, `by: board`)" becomes "a line of its own type (`config@1`, `source:
  board`)"; "(`by: hub`)" becomes "(`source: hub`)".
- "Configuration", Limits: "one `config` line" becomes "one `config@1` line".
- "Starting the board", its first paragraph: "one `board` line" becomes "one `board@1` line".

Searched and unaffected:

- Diagrams: no diagram names the journal. Every `docs/*-texts.md` and `docs/*.svg` searched for
  journal, hub, watch and `kind`: the only hits are "GitHub" and a CI "watch"
  (`release-driver-texts.md`); no SVG, `-texts.md` or `<desc>` changes.
- `README.md` names no journal.
- `docs/release-notes/` is history and is never edited.

## 8. Cards and project rules

The behaviour the cards and AGENTS.md describe (who writes a line, when it wakes, what `status`
prints) does not change; their words follow the published types, so that no text names the old
words (this CR's answer 2). Each text, where it is today:

- `AGENTS.md`, the surface server's third exception (its Configuration page): "a save appends one
  `config` line to the same journal (`by: board`)" becomes "a save appends one `config@1` line to
  the same journal (`source: board`)"; and "each write it makes to the backlog also appends one
  `board` line to that project's `forge-journal.jsonl`" becomes "... one `board@1` line ...". The
  change goes through this CR's PR; the user's merge is their approval of it.
- `skills/chantier/references/chief-of-staff.md`, the pull path: "its `board wrote` and role
  `config` lines as above, and act on its merge and two-key `config` lines" becomes "its `board
  wrote` and role `config@1` lines as above, and act on its merge and two-key `config@1` lines"
  (`board wrote` is a line's text, unchanged).
- `skills/chantier/references/hosts/claude-code.md` and `hosts/copilot.md`, the "Run the watcher"
  row: "A `config` line the board writes (a limit saved on its Configuration page) wakes the
  watcher" becomes "A `config@1` line the board writes ...". Both host files change together.
- No agent file changes (`agents/`, `com.github.copilot/agents/`: they name no journal line).
  `startup-manifest.json` and `routing.md` change only if they hold one of these texts (the Driver
  checks).

The line numbers today: AGENTS.md 62 and 65, `chief-of-staff.md` 1385-1386, `hosts/claude-code.md`
52, `hosts/copilot.md` 45 (the Driver finds them by text, not number).

## 9. Rollout

- Mixed versions on one journal (one surface, several sessions of different chantier versions): a
  chantier of an earlier version reads a version 2 line as a newer line: it counts it for `seq`,
  wakes no one and its `status` says `line <n> is version 2, newer than this chantier: update it`.
  This chantier reads the earlier one's version 1 lines as `<kind>@1`. An earlier hub or board does
  not see a version 2 `merged@1` line as a duplicate, so it may append the same merge once more as
  a version 1 line; `status` still prints one line per CR (`lines` keeps one merge per CR) and the
  Chief of Staff records the merge once. A board of another version is already named by `status`
  and the watcher (`board: chantier <v> serves this surface ...`).
- Nothing to migrate: no line is rewritten.
- No configuration key and no new CLI command. New files: `hub/schemas.py` and `hub/schemas.json`
  in the CLI's package; `scripts/journal_schemas.py` and the `journal-schemas` recipe in the
  `justfile` (run by hand, not part of `just check`).

## 10. Out of scope

- The types of the later parts (`sync-*@1`, `lease-expired@1`, `wait-cleared@1`) and the source
  `writer`: Parts C, D and E publish them, with their texts.
- Typed versions for the batch's own `events.jsonl` (the record's log): out of scope of the whole
  work (the reference's §9).
- `board-journal.jsonl` and its `kind`.
- Any new channel, a Board dependency, hosted or local (Q1-Q2).
- Validating version 0 and 1 lines against the models.
- A CLI command to read, print or write the schemas (the CLI's scope: no new tool without a
  measured cost). The `journal-schemas` recipe is a development script of the repository, not a CLI
  command.
- Enums or patterns on the open sets (`board@1.action`, `config@1.key`, answer 1).

## 11. Open questions for the user

None. The five questions of this specification's first pass are settled in `./02-answers.md`
(2026-11-20).
