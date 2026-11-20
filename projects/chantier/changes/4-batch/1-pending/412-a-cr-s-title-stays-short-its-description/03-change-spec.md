# Change Specification: A CR's title stays short

## Goal

The user, 2026-11-20, on the refreshed board: seven inbox items filed by a Griller had no `#`
heading and no `summary.json`, so the board showed their whole one-paragraph request (330 to 770
characters) as their title. Nothing checks a title's length today. The user wants a linter that
forces the agent to write a short title with the longer description below it, a `chantier file`
that never files a CR without one, cards that say it, and a board that never draws more than one
line of title.

Four parts, one limit: **a CR's title is at most 72 characters** (`TITLE_MAX`).

## What changes

### 1. The limit: one constant, 72

- `skills/chantier/scripts/cli/src/chantier/core/records.py`: `TITLE_MAX = 120` becomes
  `TITLE_MAX = 72`. It stays the one constant; not configurable.
- `skills/chantier/scripts/cli/src/chantier/declare/summary.py` repeats it (so the start-up
  imports no pydantic): its copy becomes `72` too, and a test asserts the two are equal (if no
  test does yet), so they cannot drift.
- Effect, already wired through `summaries/edit.py`'s `one_line`: `summary set --title` refuses a
  title over 72 characters (`title is N characters: the limit is 72`); its `--title` help says
  "72 characters at most".

### 2. The title checked, and where it comes from

A CR's **shown title** is what the board and `status` show, in this order:

1. `summary.json`'s `title`, when set;
2. else the folder's own title as `status/views.py`'s `_title` reads it: the first `#` heading
   (after any front matter, without a "Change Specification:" lead, through
   `core/files.py`'s `markdown_title` and `subject`) of `03-change-spec.md`, else `01-intent.md`,
   else `intake/request.md`, else that file's first non-blank line.

`_title` becomes public (`folder_title`, same module, same behaviour) so the checks read the same
title the board shows; its callers in `status/views.py` follow the rename.

For a CR in `4-batch`, `status` and the board show the title recorded at `open` instead, which is
out of scope; the check covers the summary title or the title taken from its files.

Two rules, on every CR folder (their severity in `validate` is part 3's):

- **Long title:** the shown title is over `TITLE_MAX`. The finding names the file the title comes
  from (`summary.json`, or the Markdown file whose heading or first line it is).
- **No heading:** `intake/request.md` exists and has no `#` heading (`core/files.py`'s
  `HEADING_LINE`, after any front matter). It applies even when `summary.json` has a title: the
  request is the CR's source and the board's description reads below its heading.

The messages, `<cr>` the CR's path in the planning folder as `validate` prints paths today:

- From `summary.json`:
  `<cr>/summary.json: title is N characters: the limit is 72 → summary set <cr> --title "<at most 72 characters>"`
- From a Markdown file:
  `<cr>/<file>: title is N characters: the limit is 72 → write a short "# Title" line (at most 72 characters) at its top, the text below it`
- No heading:
  `<cr>/intake/request.md: no "# " heading → write a short "# Title" line (at most 72 characters) at its top, the text below it`

### 3. `validate` refuses

- `commands/validate.py`'s `findings` adds the two rules above as **errors** for every CR not yet
  in a batch (`1-inbox`, `2-backlog/P1`..`P4`, `3-ready`): `validate` then exits 3
  (`EXIT_CONFLICT`), its head line counting them. For a CR in `4-batch` (any of its stage folders,
  `3-done` included), in `5-archives` or in `6-trash`, the same findings are **gaps** (they fail
  nothing): a merge in the middle of a batch must not turn the batch's own in-flight or merged
  CRs into errors, and history is not rewritten. The checks live in one small function (for
  instance `summaries/title.py`, `title_findings(repo, cr, severity) -> list[Finding]`),
  read-only like the rest of `validate`.
- `summaries/format.py`'s `summary_findings` no longer reports the title's length (the new check
  reports it once, with the severity above).
- The new gap kinds of `summary lint` (below) are left out of the gaps `validate` takes from
  `gap_of`, as `unreadable` already is, so no finding prints twice.

### 4. `summary lint` refuses

- `summaries/gaps.py`: `GapKind` gains `"no heading"` and `"long title"`. `gap_of` returns, in this
  order: `unreadable`, `no summary`, `late`, `no heading`, `long title`: the two new kinds rank
  after `late`, so the board's late clock (`summaries/view.py`, which reads `gap_of`) still shows
  on a late CR. `long title` is the
  summary's own title over `TITLE_MAX` (a title written under the old 120 limit); a CR with no
  summary is already its `no summary` gap, whose hint now reads
  `--title "<at most 72 characters>"`.
- `gap_line` prints the messages of part 2 for the two new kinds. `summary lint` exits 2 when it
  lists any gap, as today.

### 5. `chantier file` never files a CR without a short title

`declare/intake.py`: `file` gains `--title "<short title>"`. `commands/intake.py`'s `file_cr` and
`lifecycle/backlog.py`'s `file_idea` (shared with the board) take it. The request's title is read
with `markdown_title` (after any front matter):

| The text                                                | `--title`  | Filed as                                                                    |
| ------------------------------------------------------- | ---------- | --------------------------------------------------------------------------- |
| starts with a `#` heading of at most 72 characters      | not given  | as received, byte for byte (today's behaviour)                              |
| anything                                                | given      | `# <title>`, a blank line, then the text as received, byte for byte         |
| one line of at most 72 characters, no `#` heading       | not given  | `# <that line>` and a newline                                               |
| anything else (a long heading, several lines, no `#`)   | not given  | refused, exit 2 (`EXIT_USAGE`), nothing written                             |

- `--title` goes through `one_line(title, "title", TITLE_MAX)`: one line, not empty, at most 72.
- The refusal: `the request has no short title (its title is N characters; the limit is 72): give --title "<at most 72 characters>", the text goes below it as its description, or start the text with a short "# Title" line`
  (for a text with several lines and no heading, the same with its first line's length).
- The slug comes from `--slug`, else the title as filed (the `--title`, else the heading), as
  `idea_slug` does today.
- `commands/crs.py`'s `filed_fix` (a release's fix file filed as an inbox CR) gets the same check
  on the fix file's title, before anything is written, so the CLI never makes an inbox CR that
  `validate` rejects: a fix file with no `#` heading, or one over 72 characters, is refused with
  `the fix <path> has no short "# Title" heading (at most 72 characters) → write one at its top`
  (exit 2). One shared helper (for instance `short_heading(text) -> str | None`, next to
  `markdown_title`) serves `file_idea`, `filed_fix` and the `validate` check.
- `commands/orders.py`'s QA folder is unchanged: it writes `# QA`.

### 6. The board's New dialog

`board/write_api.py`'s `_new` reads an optional `title` string from the JSON body (refused, as
`slug` is, when it is not a string) and passes it to `file_idea`. `board/web/js/edit/new-idea.js`
adds an optional one-line Title field above the text area, sent as `title` when not empty
(`board/web/js/api/backlog.js`'s `newIdea` carries it); its label and hint are new i18n keys in
every language file (en, fr), for instance `new.heading` and `new.heading_hint` ("A short title,
at most 72 characters; the text below is its description"). A refusal keeps the dialog open with
the CLI's message, as today. The file's head comment ("the title and the slug come from the
text") says the title comes from the field, else the text's heading.

### 7. The board draws a title on one line

Read `skills/chantier/scripts/cli/src/chantier/board/web/DESIGN.md` first and keep it true.

- `css/components/card.css`: `.card-title` shows one line, cut with an ellipsis
  (`white-space: nowrap; overflow: hidden; text-overflow: ellipsis`) in place of its three-line
  clamp; the `.card-clamp .card-title, .card-compact .card-title` two-line rule loses its title
  selectors (the description's clamp is unchanged).
- `js/ui/card.js`'s `heading()` puts the full title in the heading element's `title` attribute
  (escaped as the builder escapes data), so the full text shows on hover.
- Tables and rows that draw a CR's title: the costs tables' Title cells
  (`js/views/costs-tables.js`'s `crRow` and `mergedRow`, `js/views/costs-history.js`), the Home
  rows already cut with `.ell` (`js/views/home-backlog.js`, `js/views/home-prs.js`) and the PR
  row's `.nt` (`js/views/prs-row.js`): one line, ellipsis, full text in a `title` attribute. A
  table cell's style goes in that view's sheet (it is not a component).
- Not changed: the side panel's head (`js/panel/head.js`, where the full title is read) and the
  Costs receipt (`js/views/costs-receipt.js`, a protected feature of `DESIGN.md`).
- `DESIGN.md`, "Rules", gains one rule: **One-line titles.** A CR's title in a card, a row or a
  table cell is drawn on one line, cut with an ellipsis, its full text in the element's `title`
  attribute; the side panel shows it whole (test).

### 8. The cards

Each says, in its own words and once: "a short title (at most 72 characters), the description
below it".

- `skills/chantier/references/chief-of-staff.md`, "Backlog and grill": the command line becomes
  `$CHANTIER file "<raw request>" [--title "<short title>"] [--slug <slug>]`, with one sentence:
  a CR is filed with a short title (at most 72 characters), the description below it; `file`
  refuses a request without one unless `--title` is given. The split paragraph ("the parts split
  off are filed as new inbox items") says each part is filed with its own short title.
- `skills/chantier/references/griller.md`, "What you do": the same sentence, next to `file`.
- `skills/chantier/references/spec-writer.md`, "Output": the specification's `#` heading and the
  summary's title are short (at most 72 characters), the description below.
- `skills/chantier/references/concepts.md`, "A CR's summary": "its title (one line)" becomes
  "its title (one line, at most 72 characters)".
- The cards' size budgets checked by the tests hold.

## Decisions carried from `02-answers.md`

- 2026-11-20, the user: this CR joins the current batch (batch-29, factory on).

## Dependencies

No `depends.json`: nothing here needs another CR's result. One overlap to know: CR-402
(plan-store-interface) rewrites `file_cr` → `file_idea` → `new_request`, the same lines as part 5.
Whichever of the two merges second rebases onto the other.

## Out of scope

- A configurable limit.
- `open` refusing a long specification heading (the batch's recorded title): `validate` reports
  it beforehand on the CR in the backlog.
- Rewriting archived or trashed CRs, and the planning surface's own files (see Known follow-up).
- The CR board pane (`hooks/register.tsx`): unchanged, so no pane screenshot is owed.
- The Costs receipt and the side panel's head.

## Evidence

All checks read the shipped code and files at the head under test, in-process, as the tests do
today; few and parametrized (`just test` stays within its budget).

- `tests/test_validate.py`:
  - extend `ERRORS` (parametrized) with: an inbox CR whose `summary.json` title is 73
    characters; an inbox CR with no `summary.json` whose `intake/request.md` heading is 73
    characters; an inbox CR whose `intake/request.md` has no `#` heading (one paragraph); each
    asserting the exact error line of part 2 and exit 3.
  - a 72-character title passes (no finding).
  - the same long title and missing heading in a `4-batch` stage folder, in `5-archives` and in
    `6-trash` are gaps and `validate` exits 0 (parametrized); the existing `GAPS["title"]` and
    trash cases move to the new limit (73 characters, "the limit is 72").
  - `test_a_planning_folder_made_by_the_cli_validates_and_nothing_is_written` still ends with
    `no error, no gap`.
- `tests/test_summary_lint.py`: parametrized over `no heading` and `long title`: the gap line
  and its hint, exit 2; the `no summary` hint names "at most 72 characters"; a late CR whose
  request has no heading is still `late` (the ranking of part 4).
- `filed_fix`: a fix file with no heading, and one with a 73-character heading, is refused with
  nothing filed (in the test file that already covers the release's fixes).
- `chantier file` (in the test file that already files, for instance `tests/test_triage_moves.py`
  or `test_cli_runs.py`), parametrized over the four rows of part 5's table: the bytes of
  `intake/request.md` (as received; `# <title>\n\n` + text; `# <line>\n`), the refusal's exit 2
  and message with no folder created, and `--title` of 73 characters refused by `one_line`.
- The board: one test through the write API's `new` with `title` (the filed bytes), and a refusal
  without it for a long paragraph.
- `tests/test_board_design.py` reads the shipped `css/components/card.css` and `js/ui/card.js`:
  `.card-title` declares `white-space: nowrap` and `text-overflow: ellipsis` and no line clamp;
  `heading()` writes a `title` attribute. The design rules' tests pass with the new `DESIGN.md`
  rule.
- `TITLE_MAX` of `core/records.py` equals `declare/summary.py`'s.
- `just check` passes; `just eval-dry-run` (the change is under the CLI's `src/`); `just scenario`
  as `AGENTS.md` asks for a CLI and cards change. Any fixture or scenario step that files a
  multi-line request with no heading is given a heading or `--title`.
- The board change: screenshots of a Triage post-it and a costs table with a long title cut on one
  line, in the PR's Deliverables (the visual record `DESIGN.md` names).

## Known follow-up (not a code change)

The Chief of Staff's session runs the CLI live from chantier's main checkout, so the new rules
apply to the surface as soon as this CR merges. Right after recording this CR's merge, the Chief
of Staff fixes the surface's not-yet-batched CRs that break the rules (a short `# Title` heading,
a short summary title), in the surface, before its next `validate`. CRs in chantier's own
repository that break them (fixtures, if any) are fixed in this CR's work.

A surface follow-up outside this CR: have the surface's `scripts/validate-bundles.py` run
`chantier validate` too (today it runs only `summary lint`, which fails nothing).

## Settled questions

Settled by the Chief of Staff (2026-11-20, the user asks no questions):

1. **The limit:** 72 characters, the existing `TITLE_MAX` lowered from 120, not configurable.
2. **The title checked:** the brief's order (summary title, else the request's heading, else its
   first line) is refined to what the code shows the board actually draws: summary title, else
   the first heading of `03-change-spec.md`, `01-intent.md`, then `intake/request.md`, else the
   first line. Checking only the request would let a long specification heading through to the
   board.
3. **A request with no `#` heading** is refused by `validate` (an error) and `summary lint` (a
   gap, exit 2), naming the file and the fix, even when `summary.json` has a title.
4. **Only CRs not yet in a batch refuse:** in `validate`, the two rules are errors (exit 3) on
   CRs in `1-inbox`, `2-backlog/P1`..`P4` and `3-ready`. In `4-batch` (any of its stage folders,
   `3-done` included), `5-archives` and `6-trash` they are gaps that fail nothing: a merge in the
   middle of a batch must not turn the batch's in-flight CRs (today 402, 404, 406, 408, 411) or
   merged ones into errors, and history is not rewritten.
5. **`file` with a one-line short text and no heading** is filed as `# <that line>`: the code shows
   the CLI's tests, the scenario and the board's New dialog file such texts, and refusing them
   would break each for no gain; the line already is a short title.
6. **The board's New dialog** gains an optional Title field: without it, the board (which files
   through the same `file_idea`) could no longer file a paragraph.
7. **The board's one-line title** covers cards, rows and table cells; not the side panel (where
   the full title is read) nor the Costs receipt (protected in `DESIGN.md`).
8. **The surface's own files** are fixed by the Chief of Staff right after recording this CR's
   merge, before the surface's next `validate`, not in this CR (the CLI runs live from the main
   checkout, so the rules apply at once). Having the surface's `validate-bundles.py` run
   `chantier validate` is a surface follow-up outside this CR.
9. **Gap ranking:** `no heading` and `long title` rank after `late` in `gap_of`, so the board's
   late clock still shows on a late CR.
10. **`filed_fix`** gets the same 72-character heading check, so the CLI never files an inbox CR
    that `validate` rejects.
11. **The "Intent:" lead:** not added; `subject` strips only "Change Specification:", as today.
12. **Bundle:** the board's one-line titles stay in this CR: the user asked for all four parts in
    one request.

No open question.
