# Change Specification: a CR's title is its plain subject, without the "Change Specification:" lead

## Goal

The user, 2026-11-20: "Dans la board, dans les items de la colonne Subject, je vois que chaque item
commence par "Change Specification: ". ca prend de la place pour rien".

Every CR's title on the board's PRs views starts with "Change Specification: ", which takes room and
says nothing. The cause is at the root: when a CR joins a batch, the CLI records as its title the
specification's first heading as written (`# Change Specification: <subject>` →
`Change Specification: <subject>`). batch.json, STATUS.json, STATUS.md, the pane, the Driver's
prompt, the CR's branch name and the closed batch records all carry it. The board strips it in some
views only, and case-sensitively (`Change specification:` escapes it).

Wanted (`01-intent.md`, `02-answers.md`): the CLI records the plain subject; every place that shows
a CR's title shows it plain, old records included, through one shared function; nothing already
written is rewritten.

## What changes

All paths below are under `skills/chantier/scripts/cli/src/chantier/` unless they start with
`skills/`, `tests/` or `hooks/`.

### 1. One shared function: `subject()` in `core/files.py`

- Move `subject()` from `board/backlog.py` to `core/files.py`, next to `markdown_title()`, and
  make it case-insensitive. It removes, at the start of a title only: an optional byte-order mark,
  any `#` and blanks, then an optional `Change Specification` lead followed by a colon (any case,
  blanks allowed around the colon), then strips the result:

  ```python
  LEAD = re.compile(r"^﻿?[#\s]*(?:change\s+specification\s*:\s*)?", re.I)

  def subject(title: str) -> str:
      """A title without its byte-order mark, its `#` and its "Change Specification:" lead,
      in any case."""
      return LEAD.sub("", title or "").strip()
  ```

- It removes only that one lead. A title with no colon after "Change Specification" stays as it
  is, and so does a lead in the middle of a title. It leaves "Intent:" alone: the board's JS
  `title()` keeps stripping that one (section 4).
- `board/backlog.py` imports it from `core/files.py` instead of defining it. `board/crs.py` keeps
  importing it from `board/backlog.py` or imports it from `core/files.py` (Driver's choice). There
  is no second copy in Python.

### 2. The root: the recorded title (`lifecycle/stages.py`, `prepared_cr`)

- `prepared_cr` sets the title as `subject(markdown_title(text)) or directory.name`. A heading that
  is only the lead (`# Change Specification:`) falls back to the folder's name, as an empty heading
  does today.
- Every path that records a CR goes through `prepared_cr` → `add_cr` (`commands/opening.py`): `open`,
  `order add`, a fix CR (`orders_apply.py`), a release CR (`orders_release.py`), and an automatable
  CR in `3-ready` whose `intake/request.md` serves as its specification (`triage --ready`, then
  `open`). They all get the plain subject: in `CrEntry.title`, in the `add` event's `title`, and in
  the closed record (`history.py`, `close_record`) that `close` writes from it.
- **Consequence, intended:** the CR's branch name, `chantier/<batch>/<cr>-<slugify(title)>`, loses
  its `change-specification-` prefix. Its 40 characters now hold the subject. Branches already
  created are not touched.

### 3. Shown titles: `status/views.py`

- `shown_title(recorded, folder)` returns `subject(...)` of what it returns today (the recorded
  title, or the folder's title when the record holds none or `---`). `_title(folder)` returns
  `subject(markdown_title(...))`, so the backlog rows (STATUS.md's backlog table, the pane's
  backlog, the board's backlog fallback) do not show the lead taken from a `03-change-spec.md`
  heading either.
- This is display only (answer 2): batch.json, events.jsonl and the closed records already written
  keep their text. What `shown_title` serves reaches STATUS.json and STATUS.md (each CR's page, the
  batch's table, the merged rows, the past CRs), the pane, `facts`, the Driver's prompt
  (`commands/driver.py`) and the batch's end archive (`close_archive.py`). All of them get the
  plain subject for a running batch recorded before this change too (batch-29's titles, for
  instance).
- `board/crs.py`'s `subject(shown_title(...))` becomes redundant. It may stay or be reduced to
  `shown_title(...)`.

### 4. The board: every view strips (`board/*.py`, `board/web/js/`)

The board strips both on the server side and in the page, as a guard for records written before
this change (closed records and running batches).

- **Server, `board/prs.py`:** `row_of` (`"title": subject(c["title"])`) and `_closed_rows`
  (`"title": subject(c.get("title", ""))`).
- **Server, `board/state.py`:** `_entry` (`"title": subject(c["title"])`). `_history` keeps serving
  the closed records "as they are" (answer 2: no rewrite). The page strips their titles
  (next bullet).
- **Page, `board/web/js/core/format.js`:** `title()` becomes case-insensitive and also accepts an
  optional byte-order mark and `#` before the lead:
  `String(text ?? '').replace(/^﻿?[#\s]*(?:Change\s+Specification|Intent)\s*:\s*/i, '')`.
  It still strips "Intent:" too.
- **Page, the views that show a title raw today** call `title()`: `views/prs-row.js` (`row.title`,
  the PRs page's list), `views/home-prs.js` (`c.title`, the home page's PR list),
  `views/batch-pr-card.js` (`title: title(c.title)`) and `views/overview.js` (the `title="..."`
  tooltip of the PR link). A view that already calls `title()` (kanban, gantt, graph, timecards,
  costs, receipt, home backlog, item card, panel head) stays as it is.
- The Driver reads `board/web/DESIGN.md` first (AGENTS.md) and keeps it true. No layout or style
  changes, so it is expected to need no edit. Biome (`just lint`) passes on the touched JS.

### 5. What stays

- The heading of `03-change-spec.md` stays `# Change Specification: <subject>`, as the cards
  prescribe (answer 3). No card changes.
- `idea_slug` (filing a request) is not touched. A request's first line is not a specification
  heading.
- The pane's code (`hooks/register.tsx`) is not touched. Only the values of the STATUS.json
  `title` fields it shows change (section 3).

## Out of scope

- Rewriting records already written: batch.json of a running batch, events.jsonl, the
  `5-archives/batches/batch-NN.json` and `.md` files, `summary.json` titles (answer 2).
- Renaming existing branches.
- Any other lead ("Intent:" in Python, other heading words).

## Evidence

- **New test**, in `tests/test_titles.py` (next to the existing title tests, in-process, small and
  parametrized, answer 4):
  - `subject()` over parametrized cases: `"Change Specification: Fix it"`,
    `"change specification: Fix it"`, `"CHANGE SPECIFICATION : Fix it"`, `"# Change Specification: Fix it"`,
    `"﻿# Change Specification: Fix it"` → `"Fix it"`; `"Fix it"` → `"Fix it"`;
    `"Change Specification"` (no colon) → unchanged; `"Fix the Change Specification: lead"` →
    unchanged.
  - At join: one parametrized test writes `03-change-spec.md` with a heading
    `# Change Specification: Real title` and a case variant (`# change specification: Real title`),
    runs `open` with `prepared` and `FROM_AGENTS_MD` as
    `test_a_title_behind_a_frontmatter_is_found_recorded_and_shown` does, and asserts
    `record(repo)["crs"][0]["title"] == "Real title"` and that the CR's `branch` does not contain
    `change-specification`.
  - `shown_title("Change Specification: Old", None) == "Old"`: an old record is shown plain and
    not rewritten.
- **Board server:** one assertion in an existing board test (`tests/test_board_prs.py` or
  `test_board_prs_batches.py`) that a record title `"Change Specification: X"` comes out of
  `row_of` / `_closed_rows` as `"X"`. A parametrized case added to an existing test, no new
  fixture.
- **Board page:** `just lint` (Biome) on `board/web/`. The JS `title()` has no unit-test harness in
  this repository, so nothing new is added for it. The Driver checks it by hand: one look at the
  PRs page on a running board over a record with the lead, named in the PR's evidence.
- `just check` on the worktree's rebased head. `just eval-dry-run`, since the change is under the
  CLI's `src/`. `just scenario (ubuntu-latest)` green at the PR's head, since the change touches the
  CLI (AGENTS.md). `just test` stays within its time budget: the new cases are in-process.

## Known gaps

- The values of STATUS.json's `title` fields, which the CR board pane shows (`hooks/register.tsx`),
  change: the lead goes. Under AGENTS.md's pane rule, the PR's Deliverables carry one screenshot of
  the pane from a real Claude Code session running the PR's head, captioned with the head's short
  SHA. Until it is there, the PR's Known gaps names it ("no screenshot of the pane from a real
  session"), and the Chief of Staff asks the user for one.

## Open questions

None. Choices made by the spec-writer, within the answers:

- `shown_title` and `_title` also strip (section 3), so STATUS.* and the pane show running batch-29
  and older records plain without rewriting them. This follows answer 1 ("STATUS.* and the pane
  get the plain subject") and answer 2.
- The shared Python function lives in `core/files.py`, because the CLI's record path and the
  status views use it, not only the board. The JS `title()` stays the page's own guard and keeps
  its "Intent:" case.
- The branch name losing its `change-specification-` prefix is accepted as a consequence.
