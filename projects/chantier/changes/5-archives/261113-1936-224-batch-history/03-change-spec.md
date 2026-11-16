# Change Specification: each batch leaves a record of its own in `5-archives/batches/`

## Goal

The user's words (2026-11-13): a short history of the batches in the archive folder, "if only
to know which batch we are at", kept and shown in the UI. Today the batch counter lives in
`.batch-number`, which git ignores, so a new clone, another machine or another user of a surface
starts again at `batch-01`. The archive keeps no tracked link from a CR to its batch: that link
is only in each archived `STATUS.json`, which git ignores too. The retro sits in the folder of
the batch's last merged CR.

After this CR, every batch has two files in `5-archives/batches/`: `batch-NN.json` for the UI
and `batch-NN.md` for a person. Both are published with the planning folder. `open` reserves the
number by writing the JSON; `close` completes it and writes the Markdown, which also holds the
retro. The next number is read from these records. Batches 1 to 16 are backfilled once.

The CR has no issue.

## Decisions carried from the grill (`02-answers.md`)

| Answer | Where it lands |
| --- | --- |
| 1. Shape B: one file per batch in `5-archives/batches/`, never written by another batch (no git conflict between users of a surface, none with an autosync). A and C are rejected. | "The records", "Concurrency" |
| 2. Two-digit padding in every id and file name: `batch-01`, `batch-02`, … | "The records" (file names follow `normalize_batch`) |
| 3. `batch-NN.json`, read by the UI: number, open and close dates, shape, steering, budget, final cost; for each CR its archive folder, PR, result (merged, dropped), rounds and cost | "`batch-NN.json`" |
| 4. `batch-NN.md`, for a person: the Completion report and the retro. The retro leaves the last merged CR's folder. | "`batch-NN.md`", "`close`" |
| 5. `open` reserves the number by writing `batch-NN.json` as `running`; `close` completes it; the next number is the highest of the records, the live batch and `.batch-number`, plus one | "`open`", "The next number", "`close`" |
| 6. CLI impact: `open`, `close`, the next number, and one line in `status` naming the last closed batch. The UI shows the history from these files (the board CRs). | "CLI changes"; the UI itself is out of scope |
| 7. Batches 1 to 16 are backfilled once, from the archived `STATUS.json` still on this machine; a batch with no trace left is named as such | "The backfill" |

The user accepted every default of the proposal ("Ok pour tout"). Points the answers did not
settle are taken at the default they imply and listed under "Open points".

## The records

Folder: `<planning folder>/5-archives/batches/`, i.e. `.agents/changes/5-archives/batches/`
in-project and `<surface>/projects/<name>/changes/5-archives/batches/` in external mode. One pair
per batch:

- `batch-NN.json`, where `NN` is the batch number on at least two digits, the same spelling as
  `normalize_batch` (`batch-07`, and `batch-123` past 99).
- `batch-NN.md`, written at `close` (or by the backfill).

They are published. Neither name matches an entry of `IGNORED` in `state.py`, and nothing is
added to `IGNORED`. `.batch-number` stays ignored and is still written (see "The next number").

Every writer writes by `write_file`/`write_json` (atomic rename, plain UTF-8, `\n`), with
`indent=2` and `ensure_ascii=False`, under the lifecycle lock (`changes_lock`).

### `batch-NN.json`

The UI parses these fields exactly. Each is always present; a value that is not known is `null`
(an empty object for `cost_unpriced`).

| Field | Type | Meaning |
| --- | --- | --- |
| `schema` | int | `1`. The record's own schema, separate from `STATUS.json`'s `SCHEMA`; it moves when a field changes meaning |
| `batch` | string | `batch-NN`, as `normalize_batch` spells it |
| `number` | int | `NN` as a number |
| `state` | string | `running` (written by `open`, or by the backfill for the live batch), `closed` (by `close`, or by the backfill for a batch with traces), `unknown` (by the backfill, for a number with no trace left) |
| `opened` | string or null | UTC `YYYY-MM-DDTHH:MM:SSZ`: `batch.json`'s `created` |
| `closed` | string or null | the time `close --yes` ran |
| `mode` | string or null | the shape: `parallel`, `series` or `stack` (`batch.json`'s `mode`) |
| `steering` | string or null | `foreman` or `direct` (`batch.json`'s `steering`, as it is at the time of writing: a Foreman that took a direct batch over makes it `foreman`) |
| `host` | string or null | `batch.json`'s `host` |
| `budget_usd` | number or null | `batch.json`'s `budget_usd` |
| `cost_usd` | number or null | the final cost, rounded to 4 places: the `Total` that `close` prints (`sum(r["usd"] for r in rows)` of `_final_rows`). `null` until `close` |
| `cost_unpriced` | object | model id -> calls not priced (`_sum_unpriced(rows)`); when it is not empty, `cost_usd` is a floor |
| `crs` | array | the batch's CRs, in `order` (see below). `[]` until `close` |
| `report` | string or null | `batch-NN.md` once written, else `null` |
| `backfill` | object or null | `null` for a record written by `open` or `close`; for a backfilled one, see "The backfill" |

Each entry of `crs`:

| Field | Type | Meaning |
| --- | --- | --- |
| `cr` | string | `CR-<n>` |
| `title` | string | the CR's title, as `batch.json` keeps it |
| `result` | string | `merged` (status `merged`) or `dropped` (status `cancelled`) |
| `archive` | string or null | the CR's folder after `close`, relative to the planning folder, in `/` form (`Repo.rel`): `5-archives/<YYMMDD-HHMM>-<number>-<slug>` for a merged CR, `6-trash/<...>` for a dropped one; `null` when the CR has no recorded folder |
| `pr` | string or null | the PR's or MR's URL (`c["pr"]`) |
| `rounds` | int or null | the rounds used (`c["round"]`) |
| `cost_usd` | number or null | the CR's final cost, as `_final_pages` gives it (`round(by_cr[id][1], 4)`); `null` when the CR has none |
| `cost_unpriced` | object | as `_final_pages` gives it, or `{}` |

### `batch-NN.md`

Written by `close --yes`, in this order:

1. `# batch-NN`
2. One line: opened `<opened>`, closed `<closed>`, the shape in `shape_word`'s words, the
   steering in `steering_word`'s words, the budget (or "no budget"), the final cost (`usd_text`,
   so a floor reads "at least …"), and a link to `batch-NN.json`.
3. `## Completion`: the table with the Completion report's columns (`status-layout.md`): CR,
   subject, result, PR, rounds, cost. Each CR links to its archive folder, relative to
   `5-archives/batches/` (`../<YYMMDD-HHMM>-…/` for a merged CR, `../../6-trash/…/` for a dropped
   one). The PR column follows `forge_word` ("PR" or "MR").
4. `## Cost`: the lines of `_cost_summary` that `close` prints under "final cost", one bullet
   each.
5. `## Retro`: the bytes of `4-batch/retro.md`, verbatim, when it is a retro (`_retro_target`'s
   rule: present and not whitespace only); otherwise the one line `No retro was written.`. When a
   release CR of the batch has a `work/retro.md`, one more line links it at its archive
   (`Release retro: ../<archive>/work/retro.md`). It is not copied.

The Chief of Staff's own prose Completion report, a chat message, is not copied (see "Open
points").

## CLI changes

The file names below are those of today's tree. If python-inline-deps
(`2-backlog/P2/python-inline-deps/03-change-spec.md`) has merged first, each piece lands in the
module that spec gives its function, as listed under "Where the code lands after the module
split". This CR depends on that one in neither direction.

### A new module: `skills/chantier/scripts/cli/src/chantier/history.py`

The batch records, in one place, in standard-library Python:

- `RECORDS = Path("5-archives") / "batches"` and `records_dir(repo)`, i.e.
  `repo.changes / RECORDS`.
- `record_path(repo, number) -> Path` (`batch-NN.json`) and the `.md` beside it.
- `open_record(data: dict) -> dict`: the record of a batch at `open` (`state: running`; `crs: []`;
  `cost_usd`, `closed`, `report`, `backfill` null).
- `close_record(repo, d, rows, by_cr, closed) -> dict` and `close_markdown(...) -> str`: what
  `close` writes.
- `backfill_history(repo) -> None`: see "The backfill".
- `last_closed(repo) -> dict | None`: the record with the highest `number` whose `state` is
  `closed`.

The record of a running batch is written inside `Batch.__exit__` (`state.py`), which cannot
import `history.py` at module level without a cycle. Either put the small `open_record` and
`record_path` in `state.py`, or import them inside the function, as `__exit__` already does for
`status`. Choose by what keeps the code plain.

### The next number: `Repo.next_batch_number` (`state.py`)

The highest of these, plus one:

- the numbers in the file names `batch-(\d+)\.json` in `5-archives/batches/`. Only the names are
  read, not the contents, so the scan stays cheap.
- the live batch's number (`batch_ids()`, as today);
- `.batch-number`, as today.

`Batch.__exit__` keeps writing `.batch-number` on `open`. A machine whose records are not pulled
yet still does not reuse a number it has seen, and the scenario's `.batch-number` seeding
(`scenario/run_scenario.py`, "no branch of the other batches is reused") keeps working.

### `open` (`commands.open_batch`, `state.Batch`)

In `Batch.__exit__`, when the batch is being created (`self._number` is set): before
`batch.json` is written, create `5-archives/batches/` if needed and write `batch-NN.json` from
`open_record(self.data)`. The record must not already exist: check under the lifecycle lock that
`open` already holds (`changes_lock` in `open_batch`). If it exists, raise
`ChantierError("batch-NN is already recorded in 5-archives/batches/batch-NN.json; pull the
planning folder and open again", EXIT_CONFLICT)`; nothing is written. If anything later in
`__exit__` fails before the state is written (`state_written` false), the record is removed with
`.lock` and `brief.md`, so a failed `open` leaves no record. `open`'s output is unchanged (it is
capped at ten lines and the scenario reads its first line).

### `close` (`commands.close`, `_retro_target`, `_batch_files`, `_archive_and_delete`)

- The retro no longer goes to a CR's archive or to a `5-archives/<stamp>-<batch>/` folder.
  `_retro_target` becomes the test "is there a retro" (same rule: present and not whitespace
  only). `4-batch/retro.md` is always among the batch's own files that `close` removes
  (`_batch_files` no longer keeps it). Its bytes are carried into `batch-NN.md` first.
- The check without `--yes` prints the same lines, with the retro line now
  `retro: 4-batch/retro.md goes into 5-archives/batches/batch-NN.md` (or `retro: no retro`), and
  one more line after it: `record: 5-archives/batches/batch-NN.json and batch-NN.md`. It touches
  nothing, the record included. It refuses (exit 3, nothing touched) when `batch-NN.md` already
  exists or `batch-NN.json` says `closed`.
- `--yes`, inside `_archive_and_delete`'s all-or-nothing: after the CRs are renamed into
  `5-archives` (so that `record["crs"]` holds their archive paths), and before the batch's own
  files go:
  1. keep the bytes of `batch-NN.json` if it exists (a batch opened by an older CLI and not
     backfilled has none: it is created);
  2. write `batch-NN.md` (refused, exit 3, if it exists: "refusing to overwrite …, nothing was
     closed"), then `batch-NN.json` from `close_record` (`state: closed`, `closed: now()`, the
     settings re-read from `d`, the final cost, the CRs);
  3. on any later failure, the rollback removes `batch-NN.md` and puts the JSON's old bytes back
     (or removes it if it was created), along with the renames it already undoes.
- After `--yes`, the output's lines are `retro: kept in 5-archives/batches/batch-NN.md` (or
  `retro: no retro`) and `record: 5-archives/batches/batch-NN.json closed`.
- The `close` docstring and the `_archive_and_delete` docstring say where the retro goes now.

### `status` (`commands.status`, `state.resolve_batch`)

- One line, the second of the output (right after the head line, before the CR rows):
  `last closed: batch-15, closed 2026-11-13, 18 merged, 2 dropped, $123.45`. For a backfilled
  record with no close date: `last closed: batch-15 (backfilled, no close date), 18 merged,
  0 dropped`. With no closed record: `last closed: none`. The figures come from `last_closed`
  (counts of `result`, `cost_usd` through `usd_text` with `cost_unpriced`); the cost is left out
  when `null`.
- With no running batch, `resolve_batch` refuses today with "no running batch: run `chantier
  open` first". The message now ends with `; last closed: batch-NN` (or `; no batch closed yet`),
  so the question "which batch are we at" has an answer when nothing runs.

### The index and the readers of `5-archives`

`5-archives/batches/` is not a CR folder. Every reader that lists `5-archives` skips it by name:

- `status._past`: neither listed in `merged` nor counted in `merged_total`. The existing skip of
  the old retro-only folders `\d{6}-\d{4}-batch-\d+` stays for the folders already written.
- `commands.archived_merged`: `cr_slug("batches")` is `batches`, so a `depends.json` naming
  `batches` would otherwise match it.
- `next_cr_number`: its name regex already ignores it. Leave it as it is.

No field of `STATUS.json` changes, at any level. The CR board pane (`hooks/register.tsx`) is
untouched, so the pane screenshot rule of `AGENTS.md` does not apply.

## The backfill

`backfill_history(repo)` runs once per planning folder, the way `convert_old_tree` does: from
`Repo.find`, right after the conversion, never with `readonly=True` (`board`). It is called again
under `changes_lock`, so two commands started together do it once.

- **Trigger:** `5-archives/batches/` does not exist and there is at least one trace: an archived
  or trashed `STATUS.json` with a `batch` field, `.batch-number`, or a live `4-batch/batch.json`.
  With no trace (a new project) it writes nothing and creates no folder. `open` then creates the
  folder with the first record.
- **Sources** (read only; nothing in an archive moves or changes):
  - each folder of `5-archives/` and `6-trash/` whose `STATUS.json` has a `batch`. Its number is
    the leading digits of that id, which covers `batch-07` and the older ids such as
    `01-eval-real`, `02-eval-heavy`, `04-cr-board`, `05-batch-folder` (regex
    `^(?:batch-)?(\d+)`). A folder of `5-archives/` gives `result: merged`, one of `6-trash/`
    gives `result: dropped`. The other fields come from its `STATUS.json`: `cr`, `title`,
    `pr.url` (or `pr` when it is a string), `round` -> `rounds`, `cost_usd`, `cost_unpriced`.
  - the live batch's `4-batch/batch.json`: its record as `open` would write it (`state:
    running`).
  - `.batch-number` and the live batch's number. The highest of all numbers found is the last
    number to backfill.
- **What it writes:** one `batch-NN.json` and one `batch-NN.md` for each number from 1 to that
  highest, except the live batch, which gets its JSON only. Written into
  `5-archives/.batches.tmp/` and then renamed to `5-archives/batches/` in one rename, so it is all
  or nothing. A leftover `.batches.tmp` from a killed run is removed first.
  - A number with traces: `state: closed`. `opened`, `closed`, `mode`, `steering`, `host`,
    `budget_usd` and `cost_usd` are `null`, because a CR's `STATUS.json` does not carry them.
    `crs` comes from the sources, in CR number order. `report: "batch-NN.md"`. `backfill` is:

    | Field | Type | Meaning |
    | --- | --- | --- |
    | `written` | string | when the backfill ran (UTC) |
    | `former_id` | string or null | the id the archives carry when it is not `batch-NN` (`01-eval-real`) |
    | `first_step` | string or null | the earliest `steps[].at` among its CRs' `STATUS.json` |
    | `last_merge` | string or null | the latest archive-name time among its merged CRs (`status._when`) |
    | `retros` | array of strings | paths, relative to the planning folder, of the retros found for it: a `retro.md` at the top of one of its CRs' archives, `work/retro.md` of one of its CRs, and an old `<YYMMDD-HHMM>-batch-NN/retro.md` folder |

  - A number with no trace: `state: unknown`, `crs: []`, everything else `null`, and `backfill`
    with only `written` set (the other fields `null` or `[]`).
  - `batch-NN.md` of a backfilled batch: the title, the line "Backfilled on <date> from the
    archived STATUS.json files on this machine: no open or close date, shape, steering, budget or
    final cost was kept." (or, for `unknown`: "No trace of this batch was left on the machine
    that wrote this record."), the Completion table from `crs`, and `## Retro` linking each path
    of `retros` (or "No retro found."). Retros are linked, never moved, so the links to the
    archives stay valid.
- One line on stderr, like the conversion's:
  `backfilled 5-archives/batches: batch-01 to batch-NN (<k> with no trace)`.

On this machine, today's planning folder gives batches 01 to 15 from 103 archives and the trashed
CRs of `02-eval-heavy` and `batch-10`, and batch 16 from the live batch or its archives. By the
time this CR merges, the main checkout will hold a later live batch, opened by the older CLI. The
backfill writes that batch's record as `running`, and its `close` completes it.

## Concurrency

- Each batch writes only its own two files, so two users of a surface, or an autosync, never
  edit the same file.
- `open` reads the records it has. Two machines that open before either one's record is pulled
  take the same number and meet as an add/add conflict on `batch-NN.json` at the push. This CR
  does not prevent that; with an autosync the record is pushed within seconds. The refusal of an
  existing record covers the case where the pull came first.
- Two machines that each backfill before pulling the other's `batches/` conflict the same way, on
  identical or near-identical files.

## Cards and docs

The cards say where things are; the CLI's messages are as above.

- `skills/chantier/references/concepts.md`:
  - **Batch**: the number counts all batches and is read from the records in
    `5-archives/batches/` (each batch's `batch-NN.json` and `batch-NN.md`), the live batch and
    `.batch-number`.
  - **Planning folder**: the records are published (no change to the ignored list).
  - **Lifecycle**: `5-archives/batches/` holds the records and is not a CR.
  - **Batch lifecycle**, Paused: `close` keeps the retro in `5-archives/batches/batch-NN.md`,
    replacing "in the archive of the batch's last merged CR, or in `5-archives/<date>-<batch>/`
    when none merged".
- `skills/chantier/references/chief-of-staff.md`:
  - the `open` step (line ~432): `open` records the batch in `5-archives/batches/batch-NN.json`;
  - the pause (lines ~656-658) and **Closing** (~675-676): `close` writes the batch's record and
    `batch-NN.md` (the Completion table, the final cost, the retro), and the retro leaves no file
    in a CR's archive;
  - "which batch are we at": `status` names the last closed batch.
- `skills/chantier/references/status-layout.md` (line ~117): the Retro is offered before the
  close, which keeps `4-batch/retro.md` in `5-archives/batches/batch-NN.md`.
- `skills/chantier/references/foreman.md`: no change. It names only `4-batch/retro.md`, which
  stays where the Foreman writes it. `driver.md` (a release's `work/retro.md`) is unchanged too.
- No agent file changes (`agents/`, `com.github.copilot/agents/`).
- `docs/planning-folder.md`: in the tree, `5-archives/batches/batch-NN.json, .md` with one line
  of meaning, and `retro.md`'s note ("`close` keeps it in `5-archives/batches/batch-NN.md`"); the
  close paragraph (line ~70) the same.
- `docs/cr-folder-lifecycle-texts.md` and `docs/cr-folder-lifecycle.svg`: the 5-archives box no
  longer shows "new: retro.md" / "♻️ retro.md Retro / status" in a CR's archive. It shows the
  batch's `batches/batch-NN.json · .md`. Also the description (the svg's line 3, "where it gains
  retro.md").
- `docs/cr-lifecycle-texts.md` (line ~512) and `docs/cr-lifecycle.svg`: "the retro kept in the
  last CR's archive" becomes "the batch's record and retro kept in 5-archives/batches/".
- `scenario/README.md`: the lines describing the retro cases (~111-115) follow the new place.

## Where the code lands after the module split

Only if python-inline-deps merged first:

| Piece | Today | After the split |
| --- | --- | --- |
| `history.py` | new module | `lifecycle/history.py` (layer 2); its record model in `core/records.py` beside the others, if the records are models by then |
| `next_batch_number` | `state.Repo` | `core/repo.py` (`Repo`) |
| the record written at `open` | `state.Batch.__exit__` | `core/batch.py` (`Batch`), through the callback or layer-2 function that spec uses for the STATUS rewrite |
| the backfill's call | `state.Repo.find`, after `convert_old_tree` | wherever the conversion's call goes |
| `resolve_batch` message | `state.py` | `core/batch.py` |
| `open_batch` | `commands.py` | `commands/opening.py` |
| `close`, `_retro_target`, `_batch_files`, `_archive_and_delete` | `commands.py` | `commands/closing.py` |
| `status` | `commands.py` | `commands/batch_status.py` |
| `archived_merged` | `commands.py` | `commands/opening.py` |
| `_past` | `status.py` | `status/views.py` |

Each new or changed module must stay within that spec's targets (400 lines, no import cycle).

## Out of scope

- The UI that shows the history: the board CRs (`board-read-views`, and the CR board pane) read
  these files. No `STATUS.json` field and no board code change here.
- Moving or rewriting any existing archive: past retros are linked, not moved; the old
  `<stamp>-batch-NN/` folders stay.
- Preventing two machines from taking the same number without a sync.
- Updating the record on `pause`, `order add` or a reopened batch: only `open`, `close` and the
  backfill write it.
- A new CLI command: the backfill is automatic, like the tree's conversion.

## Evidence

- `just check` passes on Linux, macOS and Windows.
- `just scenario` passes, with these steps added or changed in `scenario/run_scenario.py`:
  1. `open` writes `5-archives/batches/batch-NN.json` with `schema 1`, `state running`, `opened`
     equal to `batch.json`'s `created`, `mode`, `steering`, `host`, `budget_usd` as given, `crs`
     `[]`, and `.batch-number` is still written. The refusal of an existing record cannot be
     reached from one machine (the next number is past every record), so it is proved by reading
     the code, not by a step.
  2. The next number: with `batch-03.json` in `5-archives/batches/` and `.batch-number` at 1,
     `open` makes `batch-04`. The existing `.batch-number` 80 case still makes `batch-81`.
  3. `close` without `--yes` prints the `retro:` and `record:` lines and changes no byte of the
     record, `4-batch/retro.md` or the archives.
  4. `close --yes` on a batch with two merged CRs and a dropped one: `batch-NN.json` is `closed`,
     `closed` set, `cost_usd` equal to the printed `Total`, three `crs` with `result`, `archive`
     paths that exist (`5-archives/…` and `6-trash/…`), `pr`, `rounds` and `cost_usd`.
     `batch-NN.md` holds the table, the `## Cost` lines and the retro's two pause sections byte
     for byte. `4-batch/retro.md` is gone and no `retro.md` is in any CR archive (replacing the
     checks at lines ~2106-2170).
  5. The cases of `retro_cases` (only cancelled CRs, no retro, whitespace-only retro):
     `batch-NN.md` is written. It says `No retro was written.` when there is none. No
     `<stamp>-batch-NN/` folder is created.
  6. A planted `batch-NN.md` makes `close --yes` exit 3. Every rename is put back, and
     `batch-NN.json` and `4-batch/retro.md` are unchanged byte for byte.
  7. After a close and a new `open`, `status` prints `last closed: batch-NN, closed …` as its
     second line. With no batch, `status` refuses with `; last closed: batch-NN`.
  8. The backfill: in a world with archived `STATUS.json` of ids `01-eval-real` and `batch-03`, a
     trashed CR of `batch-03`, `.batch-number` at 4 and no `5-archives/batches/`, the first
     command writes `batch-01`, `batch-02` (`unknown`), `batch-03` (one merged, one dropped,
     `former_id` null) and `batch-04` (`unknown`, no live batch). `batch-01`'s `former_id` is
     `01-eval-real`. A top-level `retro.md` in a `batch-03` archive is in `retros` and linked from
     `batch-03.md`, and still in place. A second command writes nothing. The stderr line is
     printed once.
  9. The index: `STATUS.json`'s `merged` does not list `batches` and `merged_total` does not
     count it.
  10. External mode (the case at line ~5227): the records are in the surface's
      `projects/<name>/changes/5-archives/batches/`. The CR's archive in its PR holds no
      `retro.md` and no record.
- On this machine, once merged into the main checkout: the first command writes
  `.agents/changes/5-archives/batches/` with `batch-01` to the last closed batch, and the live
  batch as `running`. Check `batch-01.json`'s `former_id` (`01-eval-real`), the `dropped` rows of
  `batch-02` and `batch-10`, and that the board's merged count is unchanged.
- No `just mod`: neither `hooks/` nor `types/` changes.

## Open points (defaults taken, for the Chief of Staff to confirm with the user)

1. **The backfill is automatic** in the CLI, once per planning folder, the first command after
   the update (like the tree's conversion). It is not a one-time script for this repository. Any
   project with old archives gets its history; on a machine without the archives' `STATUS.json`
   it writes `unknown` records up to `.batch-number`.
2. **Past retros are linked, not moved** into `batch-NN.md`, to keep the links to the archives
   valid. Only retros from this CR on leave the CR's archive.
3. **The Completion part of `batch-NN.md` is built by the CLI** from the record (the table with
   the Completion report's columns, and the final cost lines). The Chief of Staff's prose report
   is not copied.
4. **The record's states are `running`, `closed`, `unknown`.** `pause` does not touch it, and
   the live state stays in `4-batch/STATUS.json`. `crs` is empty until `close`, so a running
   batch's record is not a stale list.
5. **`title` is in each CR entry**, beyond answer 3's list, so the UI can show a CR on a machine
   where the archive's `STATUS.json` (ignored by git) is absent.
6. **`.batch-number` is still written** by `open`, beside the record.
7. **`status` with no running batch** names the last closed batch in its refusal, besides the
   new line when a batch runs.
8. **Two machines that open, or backfill, before a sync** get the same number and a git
   conflict. It is named as a limit, not prevented.
