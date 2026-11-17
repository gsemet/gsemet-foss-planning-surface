---
title: Change spec - a table inside a quote or an admonition gets the cell editor
cr: 291
date: 2026-11-11
issue: none
priority: P3
source: QA campaign 271, QA271-11 (Low)
blast_radius: 2 (the open and save path of every table cell edit, and the reopen after a save)
inspector: Opus
stack: 290 (bottom), 289, 293, 292, 291, 288 (top)
---

# Change spec: a table inside a quote or an admonition gets the cell editor

> [!NOTE]
> Source: QA campaign 271, finding QA271-11. Sheet:
> `.agents/changes/4-archives/271-qa-campaign-tables-2026-11-10/02-table-structure/c3-3.md`,
> evidence `../evidence/c3-3-currently.jpg` and `../evidence/c3-3-expected.jpg`. Owner's answers:
> `02-answers.md` (run now, fifth from the bottom of the stack, under 288; no GitHub issue).
> Owner's decision: a table inside a quote or an admonition (Note, etc.) gets the same cell editing
> as a top-level table, instead of the raw block editor. Read code on `origin/main` (`33fb65ef`).
> Rules: `.agents/constitution.md`, `AGENTS.md`, `requirements/guidelines/project.guidelines.md`.

## Problem

A click on a cell of a pipe table inside a blockquote (`> | Q1 | Q2 |`) or a GFM alert
(`> [!NOTE]` then `> | N1 | N2 |`) opens the raw block editor with the `>` prefixes, with no table
bar and no handles. The click target is the top-level mapped block (the quote or the alert), so
the host sends the source of the whole container; `tableTools.parse(originalText)` fails on the
`>` prefixes, and `blockSourceEditor.ts` falls back to the raw editor
(`edit.selectedCell = undefined`, "Raw Markdown editor").

## Target behaviour

- **Containers**: a blockquote, a GFM alert (`> [!NOTE]`, `> [!TIP]`, ...), nested quotes
  (`> > `), and a MyST admonition directive (```` ```{note} ````, `:::{note}`, any admonition
  name). For each kind the coder first confirms, in the page, which element the click resolves to
  (`openMappedEditor`'s `target`) and what source the host sends for it.
- A click on a cell of a pipe table inside such a container opens the **cell editor and its table
  bar**, as for a top-level table: typing, Tab and Shift+Tab, the arrows, Escape (TABLE-025 and
  CR 293's empty-row removal), Done, Enter, the inline palette, the row and column buttons of the
  bar, a grid paste (CR 292).
- **Writing back**: every table line keeps the exact container prefix it had (`> `, `>`, `> > `,
  the directive's indentation). A new row or column line gets the same prefix as the table's
  lines. The lines of the container outside the table (`> [!NOTE]`, the directive fence and
  options, other paragraphs of the quote) are byte for byte unchanged. One save is one edit of the
  container, so one undo step, as today for a block.
- **Which table**: when a container holds several tables, the clicked table is found by its rank
  among the container's rendered tables, matched to the rank of the pipe-table runs in the
  container's source with the prefix removed. When the counts differ, or the table's lines do not
  share one prefix (a lazy continuation line without `>`, mixed `>` and `> `), or the stripped
  table does not parse, the click opens the raw block editor as today. Never a wrong table.
- **Reopen after a save** (Tab in the last cell, a structural button, a grid paste): the editor
  reopens in the same table of the same container, in the cell the action selects.
- **Out of scope, unchanged**: the row and column drag handles (TABLE-002) do not appear on a
  contained table; "Convert to list-table" is disabled on a contained table with a title that says
  why ("Not available for a table inside a quote or an admonition"). See Open questions.
- Top-level tables: no change at all.

## Code anchors (origin/main)

- `src/page/features/editMode.ts`: `openMappedEditor` (lines 130-171) computes `selectedCell`,
  `table`, and calls `rt.blockEditor.openBlockEditor(target, selectedCell, ...)`;
  `resumePendingBlockNavigation` (lines 173-196) finds the reopened cell with
  `target.closest?.("table")`, which is `null` when the target is a quote: the reopen after Tab or a
  structural button needs the table's rank instead.
- `src/page/features/blockSourceEditor.ts` (466 lines), lines 78-104: `tableTools.parse(originalText)
  ?? tableTools.parseListTable(originalText)`, the row and column bounds check, and the fallback to
  the raw editor.
- `src/page/features/blockEditor.ts` (541 lines), around line 344: the save text is
  `tableTools.serialize(edit.tableModel)` (or `edit.convertedText`).
- `src/page/modules/markdownTable.ts` (486 lines): `MarkdownTableModel` (the `listTable.write` hook
  at line 30 is the pattern: a model that knows how to write itself back into its wrapper);
  `serialize` (around line 265: `model.listTable ? model.listTable.write(pipe) : pipe`).
- `src/page/features/tableCellEditor.ts`: the Convert to list-table action (around lines 396-415,
  `tableFigure` already disables it for a `{table}` figure).
- `src/page/features/pageRuntime.ts`: `PendingBlockNavigation` (line 238), `BlockEdit`.
- Fixture of the replay: `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/structure-tables.md`
  (already on `origin/main`): the quoted table `qa | qb` and the Note table `na | nb`.

## Recommended approach

1. A new pure module `src/page/modules/tableInContainer.ts`:
   `containedTable(sourceText, tableRank) → { tableText, write(tableText) → containerText } |
   undefined`. It splits the container into lines (line endings kept), takes the common prefix of
   each candidate pipe-table run (`^(?:[ \t]*>[ ]?)+` for quotes, leading spaces for a directive's
   body), checks that every line of the run has that exact prefix, and `write` puts the prefix back
   on every line of the new table text (new lines included) and splices it into the container.
   `@implements_req SwRS-MDOKFSTUDIO-TABLE-121` (provisional ID).
2. `MarkdownTableModel` gets an optional `container?: { write(text: string): string }`, applied
   in `serialize` after `listTable` (so every save path writes the container). The conversion
   action, which reads `serialize`, is disabled when `container` is set.
3. `blockSourceEditor.ts`: when `parse` and `parseListTable` both fail and a cell was clicked, try
   `containedTable(originalText, rank)`, with `rank` = the index of the clicked table among
   `edit.target.querySelectorAll("table")`; parse `tableText`, set `model.container`, and go on as
   for a top-level table.
4. `PendingBlockNavigation` gets an optional `tableRank`; `resumePendingBlockNavigation` takes the
   table as `target.closest("table") ?? target.querySelectorAll("table")[tableRank]`.
5. File sizes: `markdownTable.ts` 486, `blockSourceEditor.ts` 466, `editMode.ts` 261,
   `tableCellEditor.ts` 609 plus 293 and 292 (limit 800).

## Requirements

No `approved` requirement is touched (none in the bundle carries `approved_by`): no owner
agreement needed.

- **New SwRS, provisional ID SwRS-MDOKFSTUDIO-TABLE-121** (scope `table-editing`, `okfreq new ...
  --lifecycle proposed`, derives from `StRS-MDOKFSTUDIO-TABLE-001`, the parent of TABLE-001): "A
  pipe table inside a quote or an admonition is edited cell by cell, its container prefix kept".
  Normative: When the writer clicks a cell of a pipe table inside a blockquote, a GFM alert or a
  MyST admonition in edit mode, the extension SHALL open the cell editor and the table bar, write
  every table line back with its container prefix, leave the other lines of the container
  unchanged, and fall back to the raw block editor when the table cannot be located safely.
  Scenarios: (nominal) quote; (nominal) GFM Note; (nominal) MyST `{note}`; (nominal) Tab in the
  last cell adds a prefixed row and reopens there; (boundary) nested quote `> > `; (boundary) `>`
  without a space kept as is; (boundary) two tables in one quote, the second edited; (refusal) a
  lazy continuation line, mixed prefixes, rendered and source table counts that differ: raw
  editor; (boundary) Convert to list-table disabled with its reason; (boundary) no drag handles.
  Provisional: the stack assigns the next free `TABLE` IDs bottom to top (292 takes 120 at the time
  of writing, this CR 121); `okfreq new` allocates the real one at rebase.
- **SwRS-MDOKFSTUDIO-TABLE-001** (`proposed`, `stable`; amend lightly): a related-requirements line
  "a table inside a quote or an admonition: SwRS-MDOKFSTUDIO-TABLE-121". No normative change.
- **SwRS-MDOKFSTUDIO-TABLE-035** and **TABLE-070** (`proposed`, `stable`): only if the coder's
  change touches their marked code (the reopen after Tab; the disabled conversion): add one
  boundary row each, no normative change.
- `just requirements-update`, generated files committed, a dated entry in `requirements/tiers/log.md`.
- Writing skill: no change (no rendered syntax changes; the skill does not say these tables are
  read-only).

## Tests first (each fails on origin/main)

1. **Unit, pure**: a new `test/page/modules/tableInContainer.test.ts`, `@tests_req
   SwRS-MDOKFSTUDIO-TABLE-121`: the quote and Note tables of `structure-tables.md`; `> > ` nested;
   `>` without a space; a MyST `{note}` with an option line; two tables in one quote (rank 1);
   CRLF line endings kept; a new row written with the prefix; refusals (lazy continuation, mixed
   prefixes, rank out of range) return `undefined`; round trip without change gives the container
   text byte for byte.
2. **Unit, page**: in `test/page/fmtableReqTable.requirements.test.ts` (414 lines) next to the
   existing fallback test, or in a new `test/page/runtimeTableInContainer.test.ts`: click a cell of
   a table inside a `blockquote` target, answer `previewEditSource` with the quoted source: a
   `[data-sphinx-preview-table-cell-editor]` opens (not the raw editor) and the table bar is there;
   type and Enter: one final save whose text is the container with only the edited line changed;
   Tab in the last cell: the pending navigation carries the rank and the reopen finds the cell;
   Convert to list-table is disabled. `@tests_req SwRS-MDOKFSTUDIO-TABLE-121`.
3. **Real input**, promoting the replay: a new `test/integration/realInput/tableInContainer.ts`
   (scenario `table-in-container`, registered in `test/integration/realInput/run.ts`), on the
   content of `synth/structure-tables.md` plus a MyST `{note}` table: click `qa`: the cell editor
   and `[data-sphinx-table-menu]` are there; type, Enter: the buffer line is `> | qaX | qb |` and no
   other line changed; click `nb` in the Note, Tab: a row `> |  |  |` is added and the editor
   reopens in it; Escape: the row is removed (CR 293); the `{note}` table: one cell edit keeps the
   fence and options. `@tests_req SwRS-MDOKFSTUDIO-TABLE-121`. Runs in the heavy CI run.
4. **Visual**: `table-editing/v33-cell-editor-in-quote-light-900` and
   `table-editing/v34-cell-editor-in-note-dark-900` (next free numbers after 292's v32; re-check at
   rebase), in a new file `test/visual/tableInContainerScenarios.ts`, on a new fixture
   `test/visual/fixtures/86-table-in-quote-and-admonition.md` (a quoted table, a GFM Note table, a
   MyST `{note}` table). A capture module `test/visual/capture_table_in_container.py`, imported by
   `test/visual/capture.py`, clicks a cell and asserts the cell editor (not
   `.sphinx-preview-block-editor`) and the table bar. Save an `open` step shot.

### Replay promoted

From local commit `87307e8f` (branch `qa/271-table-campaign-replays`, not pushed; read with
`git show 87307e8f:<path>`, never merge or push that branch), add to this PR:

- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c3-3-table-in-quote-or-note-has-no-cell-editor.json`

Its fixture `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/structure-tables.md`
is already on `origin/main`, identical: do not copy it.

## Acceptance checks (the Verifier runs each at the pushed head)

| # | Claim | Command (from the worktree root) |
| --- | --- | --- |
| A1 | The new unit tests pass | `fnm exec -- npm run compile && fnm exec -- node scripts/node-test.mjs unit "out/test/page/modules/tableInContainer.test.js" "out/test/page/*TableInContainer*.test.js" "out/test/page/fmtableReqTable.requirements.test.js"` |
| A2 | They fail on the base | the page test copied into a detached worktree of the base fails (raw editor opens) |
| A3 | Top-level tables unchanged | `fnm exec -- node scripts/node-test.mjs unit "out/test/page/runtimeTable*.test.js" "out/test/page/modules/markdownTable*.test.js"` passes |
| A4 | Cell editor and bar on a quoted and a Note table, light and dark | `fnm exec -- npm run visual:render && uv run --no-sync --group docs python test/visual/capture.py --group table-editing` passes, v33 and v34 included |
| A5 | Real window: prefix kept, other lines unchanged, Tab and Escape work | the heavy CI run at the head is green and its integration log names `table-in-container` |
| A6 | Traceability | `uv run --no-sync --group requirements okfreq validate --check-links --project-root .` passes; the new SwRS lists `src/page/modules/tableInContainer.ts` and its tests |
| A7 | Replay in the PR | `git diff --stat <base>...HEAD -- .agents/skills/markdown-studio-exploratory-qa-claude/scenarios/` lists the c3-3 replay |
| A8 | Gates | `just check` and `just preflight` pass |

## Screenshots expected in the PR

- Before (base) and after (head): light, 900 px, a click on `qa` in the quoted table: before, the
  raw block editor with `>` prefixes; after, the cell editor with the table bar. Dark, the same in
  the Note table. Use the `open` step shots of v33 and v34 and the same captures on a detached
  worktree of the base (the QA evidence `c3-3-currently.jpg` shows the "before" too).

## CHANGELOG line (`## Unreleased`)

- A table inside a quote, a GitHub alert (Note, Tip, ...) or a MyST admonition now opens the
  cell editor and the table bar, like any other table, instead of the raw Markdown editor. The
  `>` prefixes and the rest of the quote are kept as written.

## Files expected to change

- `src/page/modules/tableInContainer.ts` (new)
- `src/page/modules/markdownTable.ts` (`container` hook in the model and `serialize`)
- `src/page/features/blockSourceEditor.ts` (the contained-table open path)
- `src/page/features/editMode.ts` (`resumePendingBlockNavigation`, the rank)
- `src/page/features/blockEditor.ts`, `src/page/features/pageRuntime.ts` (pending navigation rank)
- `src/page/features/tableCellEditor.ts` (conversion disabled; the rank in `structural` and on Tab)
- `test/page/modules/tableInContainer.test.ts` (new), a page test (see test 2)
- `test/integration/realInput/tableInContainer.ts` (new), `test/integration/realInput/run.ts`
- `test/visual/fixtures/86-table-in-quote-and-admonition.md` (new),
  `test/visual/tableInContainerScenarios.ts` (new), `test/visual/capture_table_in_container.py` (new),
  `test/visual/capture.py`, `test/visual/scenarios.ts`, `test/visual/scenarioIds.ts`,
  `test/visual/scenarioAssertions.ts` (only for a flag)
- `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-121.md` (new, provisional ID),
  `SwRS-MDOKFSTUDIO-TABLE-001.md` (related line), `requirements/tiers/log.md` and the generated
  requirement files
- `CHANGELOG.md`
- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c3-3-table-in-quote-or-note-has-no-cell-editor.json` (new)

## Shared with the other CRs of the stack

- `src/page/features/tableCellEditor.ts` (293 hint and Escape, 292 paste listener),
  `src/page/features/pageRuntime.ts`, `blockEditor.ts` and `editMode.ts` (293 adds the
  `addedRow` mark to `PendingBlockNavigation` and its resume): this CR is above both and rebases
  on them; the `tableRank` field sits next to `addedRow`.
- `test/integration/realInput/run.ts`, `test/visual/capture.py`, `scenarios.ts`, `scenarioIds.ts`,
  `scenarioAssertions.ts`, the fixture numbers (86 here) and `table-editing/vNN` numbers (v33-v34),
  the new SwRS ID (after 292's), `requirements/tiers/log.md` and the generated requirement files,
  `CHANGELOG.md`.
- 288 (top of the stack, export to HTML) touches none of these source files as far as its intent
  says.

## Blast radius

2. The open path, the save text and the reopen after a save are shared by every table edit. The
contained path only runs when the top-level parse fails, and the `container` hook only exists on
those models, so top-level tables take today's code; but a wrong rank or prefix would write the
wrong lines of a container. The refusal rules (counts must match, one prefix, parse must succeed)
and the byte-for-byte round-trip test are the guard.

## Open questions

- Row and column drag handles, and Convert to list-table, on a contained table. **Recommended
  answer: out of scope here** (the owner asked for cell editing; the bar's row and column buttons
  give the same structure changes). The handles stay absent and the conversion button is disabled
  with its reason; a follow-up backlog item can add them.
