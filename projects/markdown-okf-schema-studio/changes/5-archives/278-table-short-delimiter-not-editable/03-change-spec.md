---
title: Change spec - tables with a 1 or 2 dash delimiter get table editing
cr: 278
date: 2026-11-10
issue: none
blast_radius: 1 (one parse rule in the page; no rendering change)
---

# Change spec: tables with a 1 or 2 dash delimiter get table editing

> [!NOTE]
> Source: QA campaign 271, finding QA271-04 (Medium, reproduced, measured). Sheet:
> `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/4-archives/271-qa-campaign-tables-2026-11-10/02-table-structure/c3-1.md`.
> Owner's answers: `02-answers.md` (P2, part of the stack 277 to 282, no GitHub issue). Read code
> and guidelines from `origin/main`. Rules: `.agents/constitution.md`, `AGENTS.md`,
> `requirements/guidelines/project.guidelines.md` ("During a change").

## What ships

- A pipe table whose delimiter cells have one or two dashes (`-`, `--`, `:-`, `-:`, `:--`, `--:`,
  `:-:`) is editable like the three-dash form: a click on a cell in edit mode opens the cell editor,
  the table bar shows, the row and column handles work, the palette table actions (Column alignment,
  conversion to list-table) find the table.
- A cell edit leaves the delimiter row byte for byte as written (minimal diff, `:--` stays `:--`).
- Generation is unchanged: a new delimiter cell (new column, new table) is still `---`, and Column
  alignment still writes at least three dashes (TABLE-111): `:--` aligned right becomes `---:`.
- Nothing changes for tables that are already editable, nor for blocks that are no table.

## Root cause (confirmed by reading, not by running)

`src/page/modules/markdownTable.ts`, `createMarkdownTableTools().parse` (line 219 on `origin/main`):

```ts
|| !rows[1].every((cell) => /^:?-{3,}:?$/u.test(cell.replace(/\s/gu, "")))
```

GFM (and markdown-it / markdown-it-py, which render the preview) accept `:?-+:?`; this rule asks for
three dashes, so `parse` returns `undefined`. Every editing path goes through `parse`:

- `src/page/features/blockSourceEditor.ts` (around line 80): `tableTools.parse(originalText) ??
  tableTools.parseListTable(...)` is `undefined`, so the clicked cell falls back to the raw Markdown
  editor (`.sphinx-preview-block-editor`): exactly what the sheet measured.
- `src/page/modules/tableEditActions.ts` `tableAtCaret` (line 71): palette Column alignment and
  conversion see no table.
- `src/page/features/tableRowMove.ts` (line 233) and `src/page/modules/tableStructure.ts` /
  `tableConversion.ts` (via the injected `parse`): handles and conversions.

The rendering side already reads short delimiters (`test/core/render/mystTablesTree.test.ts` line 18
renders `|:--|--:|`), so this is a page-only fix.

### The fix

In `parse`, accept a delimiter cell matching `/^:?-+:?$/u` (spaces removed). One guard keeps today's
behaviour for pipe-less two-line blocks: a delimiter row with a cell of fewer than three dashes is
accepted only when the delimiter line contains a `|`. Without it, a setext heading (`Title` over
`-` or `--`) would start to parse as a one-column table in `tableAtCaret` and offer Column
alignment on a heading. (`Title` over `---` already parses as a one-column table today; leave that
as is, out of scope.) Write the rule as one named constant with a comment saying why, not as a
second inline regex.

No change to `newSegment` (`"---"`), `alignColumn` (`Math.max(3, ...)`), `toHtmlTable` or the
conversion `aligns` (they read colons with `startsWith`/`endsWith`, length-independent).

Out of scope, noted: `src/core/comments/anchoring.ts` `TABLE_RULE` asks for two dashes (`-{2,}`),
so a one-dash delimiter row is indexed as text for comment anchoring. Harmless (the line holds no
words) and in `core/comments`, which CR 280 may touch: do not change it here.

## Requirements (okfreq)

Both are `req_lifecycle: proposed` (status `stable` by projection, not approved): no owner approval
needed.

- **SwRS-MDOKFSTUDIO-TABLE-001** (amend). Its boundary scenario "Only a well-formed pipe table opens
  a cell editor" pins the old rule: the prose says "at least three dashes ... /^:?-{3,}:?$/" and the
  table has the row `a delimiter cell of two dashes ("--") | parse returns no table`. Change to:
  delimiter cells of at least one dash with optional colons (`/^:?-+:?$/`), the delimiter line holds
  a pipe when a cell has fewer than three dashes. Table rows: replace the `"--"` refusal row by
  `"| a | b |\n| :-- | --: |\n| c | d |"` and `"| a | b |\n|-|-|\n| c | d |"` parse and open a cell
  editor; add a refusal row `a line over a "--" line, no pipe (a setext heading)` returns no table.
  Keep the title and the description (no index or StRS text change). Add the new tests to
  Verification notes.
- **SwRS-MDOKFSTUDIO-TABLE-111** (amend, one boundary row). Short delimiters are newly reachable by
  Column alignment: add the row `a short cell ":--", right | "---:" (the cell grows to three
  dashes)` to "Width of the delimiter cell and replacing an alignment". Normative text unchanged.
- No new SwRS. `@implements_req SwRS-MDOKFSTUDIO-TABLE-001` already sits on `parse`; keep it.
- `just requirements-update`, its generated files committed, and a dated entry (`## 2026-11-10`,
  `### ...` sub-heading) in `requirements/tiers/log.md`.

## Tests first (each must fail on unchanged code)

1. Unit, `test/page/modules/markdownTable.test.ts`, `@tests_req SwRS-MDOKFSTUDIO-TABLE-001`:
   - `| A | B |\n| :-- | --: |\n| a1 | b1 |` (the replay fixture's table), `| A | B |\n| :- | -: |\n...`,
     `| A | B |\n| -- | -- |\n...`, `|A|B|\n|-|-|\n|a|b|` and `| A |\n| :-: |\n| a |` all parse, with
     the right rows.
   - Round trip: edit `a1` to `x` and `serialize`: only the `a1` line changes; the delimiter line is
     identical to the source (same for a CRLF source: line endings kept).
   - Refusal: `Title\n--\n` and `Title\n-\n` return `undefined`; `| A |\n| invalid |` still does.
2. Unit, `test/page/modules/editActions.test.ts`, `@tests_req SwRS-MDOKFSTUDIO-TABLE-111`: caret in
   column B of the `:-- | --:` table, Column alignment left gives `:---`; right on `:--` gives `---:`;
   only the delimiter line changes.
3. Unit, structure: inserting a column into a `:-- | --:` table writes `---` for the new delimiter
   cell and keeps `:--` and `--:` verbatim (existing column tests in `markdownTable.test.ts`).
4. Headless page test, `test/page/fmtableReqTable.requirements.test.ts` (next to the existing
   fallback test), `@tests_req SwRS-MDOKFSTUDIO-TABLE-001`: click a body cell, answer
   `previewEditSource` with the two-dash table: a `[data-sphinx-preview-table-cell-editor]` region
   with a text box holding `a1` opens, not the raw Markdown editor.
5. Real input (promotes the QA replay): new `test/integration/realInput/tableShortDelimiter.ts`,
   scenario `table-short-delimiter`, registered in `test/integration/realInput/run.ts` (import, the
   named map, the sequential run list), on the content of `structure-twodash-lf.md`: open the side
   preview, edit mode on, click cell `a1`: cell editor and `[data-sphinx-table-menu]` present; type,
   Enter: the buffer has the new text and the delimiter line `| :-- | --: |` unchanged.
   `@tests_req SwRS-MDOKFSTUDIO-TABLE-001`. Runs in CI (heavy run), not locally (brief: no real
   window locally during the QA campaign).

### Replay promoted

From local branch `qa/271-table-campaign-replays` (commit 87307e8f, not pushed; read with
`git show 87307e8f:<path>`, never merge that branch), add to this PR:

- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c3-1-two-dash-delimiter-table-has-no-cell-editor.json`
- its fixture `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/structure-twodash-lf.md`
  (its three-dash twin `structure-crlf-3dash.md` is not needed by the replay; leave it to the CR
  that uses the CRLF fixtures).

## Files expected to change (for stack ordering)

- `src/page/modules/markdownTable.ts` (the `parse` delimiter rule)
- `test/page/modules/markdownTable.test.ts`
- `test/page/modules/editActions.test.ts`
- `test/page/fmtableReqTable.requirements.test.ts`
- `test/integration/realInput/tableShortDelimiter.ts` (new)
- `test/integration/realInput/run.ts` (shared: any stack CR adding a real-input scenario edits it)
- `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-001.md`
- `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-111.md`
- `requirements/tiers/log.md` and generated requirement files (shared by the whole stack)
- `CHANGELOG.md` `## Unreleased` (shared by the whole stack)
- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c3-1-two-dash-delimiter-table-has-no-cell-editor.json` (new)
- `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/structure-twodash-lf.md` (new)

Not touched: `blockSourceEditor.ts`, `tableCellEditor.ts`, `tableEditActions.ts`, rendering,
`core/comments`, the writing skill (it does not state a dash count; no rendered syntax changes).

## Blast radius

Small. One predicate widened in the page model, guarded so pipe-less blocks behave as today. Tables
that parsed before parse the same (the new rule is a superset for piped lines). Newly editable
tables follow the existing minimal-diff writers. Risk to watch: a piped two-line block whose second
line is only dashes and pipes now counts as a table; markdown-it renders it as a table too, so the
page and the preview agree.

## Gates

- `just check` (format, types, boundaries, unit, contract, requirements links).
- `just requirements-update`; `okfreq validate --check-links --project-root .` as CI runs it.
- Headless visual of the group: `npm run visual:render && uv run --no-sync --group docs python
  test/visual/capture.py --group table-editing` (no screenshot change expected).
- Heavy CI run on the branch: `gh workflow run ci.yml --ref <branch> -f heavy=true` (runs the new
  real-input scenario). No local real VS Code window.
- `CHANGELOG.md` `## Unreleased` line, e.g. "A table whose delimiter row uses one or two dashes
  (`:--`, `--:`) can now be edited cell by cell, like one written with three."
- PR opened as a draft, ready only when PR CI and the heavy run are green and the Inspector approved.

## Open questions

None.
