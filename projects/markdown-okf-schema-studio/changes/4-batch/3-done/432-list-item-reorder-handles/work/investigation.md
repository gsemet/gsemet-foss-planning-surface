# CR-432 investigation (before round 1)

Base: worktree `batch-06-CR-432` at `e05f0b51` (origin/main, CR-424 merged). Read only; no project
file changed.

## 1. Precondition probe

**precondition: holds for all** (plain quote, GitHub alert, MyST admonition in backtick and colon
form, two nested MyST admonitions in backtick and colon form, plus an ordered loose list in an
alert).

### How it was run

- Renderer: the real one, `renderMyst` (`src/core/render/mystRenderer.ts`, the one
  `renderPipeline.ts` calls), then `rewriteSphinxHtml` with the source mapping, parsed with parse5:
  exactly `renderMappedPage` of `test/session/mappedHtmlDom.ts`, the path CR-424's
  `test/session/listItemEditOpen.test.ts` uses with `createMappedBlocks`.
- `test/page/runtimeHarness.ts` does **not** render: it is a fake DOM fed by hand-built
  `RuntimeElement`s (as `runtimeTableRowMove.test.ts` does). So the spec's "first runtime test,
  rendered with the real renderer" cannot run on the harness: put it in a `test/session/` test on
  `renderMappedPage` + `createMappedBlocks(...).listRange(list)` (see section 2, MappedBlocks).
- `sourceRangeForList` is a closure inside `createMappedBlocks`, not exported, and
  `editingElementFor` never reaches it for a list in a container (the alert/admonition branch wins
  first). The probe used a verbatim copy of its body and of `spanOf`.
- Scratch files: `work/scratch/probe.ts`, `work/scratch/build.mjs` (esbuild bundle, packages kept
  external at their worktree path so the MyST patch hooks apply), run with
  `node --import <worktree>/scripts/register-myst-patches.mjs probe.mjs`; full output
  `work/scratch/probe-output.log` (exit 0).

### Results (items `line-endLine`, range of `sourceRangeForList`)

| Container | `li` lines (outer list) | inner `li` | list range | lines covered |
| --- | --- | --- | --- | --- |
| plain quote `> ` (list at 3..7) | 3-3, 4-6, 7-7 | 5-5, 6-6 | 3-7 / 5-6 | list only |
| GitHub alert `> [!NOTE]` (list 6..10, `>` at 11, tail 12) | 6-6, 7-9, 10-11 | 8-8, 9-9 | 6-11 / 8-9 | list + its trailing `>` line |
| MyST ```` ```{note} ```` (list 6..10) | 6-6, 7-9, 10-11 | 8-8, 9-9 | 6-11 / 8-9 | list + trailing blank |
| MyST `:::{note}` | same as above | same | 6-11 / 8-9 | list + trailing blank |
| two nested ```` ````{note} ```` / ```` ```{warning} ```` (list 9..13) | 9-9, 10-12, 13-14 | 11-11, 12-12 | 9-14 / 11-12 | list + trailing blank |
| two nested `::::{note}` / `:::{warning}` | same | same | 9-14 / 11-12 | list + trailing blank |
| ordered loose list in `> [!TIP]` (3./4./5.) | 2-3, 4-7, 8-8 | 6-7 | 2-8 / 6-7 | list only (+ `>` after nested) |

Every `ul`, `li` and inner `p` carries `data-sphinx-source-file`, `data-sphinx-source-line` and
`data-sphinx-source-end-line`. The admonition title `p.admonition-title` is unmapped. The range never
reaches the container's marker line, its lead text or its tail text.

Markup excerpt, GitHub alert:

```text
<aside class="admonition note simple" data-sphinx-source-line="3" data-sphinx-source-end-line="12" data-okf-github-alert="true">
  <p class="admonition-title">"Note"
  <p data-sphinx-source-line="4" data-sphinx-source-end-line="4">"Lead text."
  <ul data-sphinx-source-line="6" data-sphinx-source-end-line="11">
    <li data-sphinx-source-line="6" data-sphinx-source-end-line="6"><p 6-6>"Alpha"
    <li data-sphinx-source-line="7" data-sphinx-source-end-line="9"><p 7-7>"Beta"
      <ul data-sphinx-source-line="8" data-sphinx-source-end-line="9">
        <li 8-8><p 8-8>"Beta one"   <li 9-9><p 9-9>"Beta two"
    <li data-sphinx-source-line="10" data-sphinx-source-end-line="11"><p 10-10>"Gamma"
  <p data-sphinx-source-line="12" data-sphinx-source-end-line="12">"Tail text."
```

Two nested admonitions (backtick form):

```text
<aside class="admonition note" 3-19>
  <p class="admonition-title">"Note"  <p 4-4>"Outer text."
  <aside class="admonition warning" 6-16>
    <p class="admonition-title">"Warning"  <p 7-7>"Inner text."
    <ul 9-14>
      <li 9-9>  <li 10-12> (<ul 11-12> <li 11-11> <li 12-12>)  <li 13-14>
```

Plain quote: `<blockquote 3-7><ul 3-7><li 3-3><li 4-6>(<ul 5-6>…)<li 7-7>`.

### Consequence for module A (flag to the Coder)

When the list is followed by more content in the same container or document, the range **ends on
a trailing blank line** (`>` in a quote/alert, an empty line in an admonition), and the last `li`
ends there too (`10-11`). The same holds in a plain document (CR-424's test: `UL 3-18` for items
ending at 17). Spec rule A.4 speaks of gaps *between* items; `moveListItem` must also keep a
**trailing gap** after the last item in place (strip it from the last item before moving, write it
back at the end), or a move of the last item would carry the blank line up and glue the list to
what follows. A blank `>` line (no space) must count as carrying the `> ` prefix (rule A.2 already
says so).

## 2. Map for the Coder (names at this base)

All names of the spec exist at the base unless flagged **(mismatch)**.

- `src/page/features/tableRowMove.ts` (610 lines), `installTableRowMove(rt)`:
  `MOVE_TIMEOUT_MS = 5000` (l.21), `busy(table?)` (l.149), `postEditClosed` (l.156, calls
  `rt.blockEditor.postEditClosed`), `endPending` (160), `armSettle` (166), `requestMove` (193),
  `movedText` (227, `containedTable` at 236), `receiveSource` (248, `rt.scroll.anchorField()` at
  274), `showDrop` (282), `updateDropIndicator` (293), `zoneTarget` (324), `dragOverZone` (355),
  `dropInZone` (367), `drop` (375), `commitDrop` (382), `moveByKey` (395), `startDrag` (408),
  `addHandle` (423: class `okf-list-editor-handle okf-table-row-handle` at 429, `aria-label` 432,
  `rt.blockMoves.moveChordDirection(event, false)` 440), `bindDropTargets` (457), `position` (491),
  `schedulePosition` (538, `requestAnimationFrame`), `refresh` (545, layer
  `data-okf-row-handle-layer` 560, `ResizeObserver` 585), `reposition` (605).
- Wiring (line numbers confirmed):
  - `src/page/features/blockSourceEditor.ts:47` `if (rt.tableRowMove.receiveSource(message)) return;`
  - `src/page/features/pageInput.ts:262` the click skip on `[data-okf-row-handle]` /
    `[data-okf-col-handle]`.
  - `src/page/features/editMode.ts:77` `rt.tableRowMove.refresh();` in `applyEditMode`.
  - `src/page/runtime.ts:297` `rt.tableRowMove?.reposition();`, `:414`
    `rt.tableRowMove = installTableRowMove(rt);` (import at 44).
  - `src/page/features/pageRuntime.ts`: `TableRowMove` interface at 640, member `tableRowMove` at
    721, `MappedBlocks` interface at 391..417, `MAPPINGS_SELECTOR` at 728. **The file is 728 lines
    (limit 800, `scripts/check-file-sizes.mjs`)**: the `ListItemMove` interface, the
    `listItemMove` member and `listRange` add about 20 lines; fine, but keep doc comments short.
- `src/page/modules/tableInContainer.ts:22` `const QUOTE_PREFIX = /^(?:[ ]{0,3}>[ ]?)+/u;` (not
  exported) and `prefixOf(text)` at 35, `splitLines` at 26 (also private). To share it, export
  `QUOTE_PREFIX`/`prefixOf` or move them to a small module (spec A.2).
- `src/page/modules/listTableMove.ts`: `readListTable` (l.35) is **private** (exports are
  `moveListTableRow` 113 and `moveListTableColumn` 164); its line split with kept endings and its
  `gaps: string[][]` (29, 72..84) are the pattern to copy, not to import.
- `src/page/features/mappedBlocks.ts`: `sourceRangeForList(list, reference)` (l.93) and
  `spanOf(elements, reference)` (l.102) are closures of `createMappedBlocks`; the returned object
  (l.204..214) does not expose them. Add `listRange(list: Element)` to the returned object and to
  the `MappedBlocks` interface, calling `sourceRangeForList(list, list)`: every rendered `ul`/`ol`
  carries its own `data-sphinx-source-file` (probe), so the list is its own reference. Tag it
  `@implements_req` for the new SwRS.
- `src/core/preview/styles/editModeStyles.ts`: **650 lines**; `TABLE_HANDLES_CSS` at 545..630,
  joined in `EDIT_MODE_CSS` at 649. A list block of about 60 lines keeps it under 800, so it can
  stay in this file. Note: the table block is **not** scoped to
  `html[data-sphinx-preview-edit-mode="on"]` (only its menu rule is); the spec asks the list block
  to be scoped, which is stricter and fine. Rules to mirror: layer (549), transform
  `translate(-100%, -50%)` (560), dot lift `translate(-2.5px, -5px)` (564), push
  `table[data-okf-row-shift="true"]` (590: `width: max-content`, `max-width: calc(100% - 2.2em)`,
  `margin-inline-start: 2.2em`), dragging opacity 0.45 (603), drop lines inset 2px
  `var(--studio-focusBorder, Highlight)` (607..613). For a list, the drop line is on the `li`, not on
  cells: `box-shadow: inset 0 2px 0 …` on an `li` is drawn inside its box, under its marker
  column only if the `li` box covers it; a `border-top`/outline or a pseudo-element may be needed.
  The `width: max-content` of the table push does not suit a `ul`/`ol` or an `aside`: use only
  `margin-inline-start: 2.2em` and `max-width: calc(100% - 2.2em)`.
- Handle mark: `src/core/preview/styles/frontmatterEditorStyles.ts` (461 lines),
  `.okf-list-editor-handle` at 249, 282, `::before` 293, `:active` 303, `:hover` 328,
  `:focus-visible` 337 (global, as the table handles already reuse it).
- Attribute names: the frontmatter list editor already uses `data-okf-list-item="true"` and
  `data-okf-list-item-input` (`frontmatterListEditor.ts:200, 210`). The new
  `data-okf-list-item-handle`, `-line`, `-dragging`, `-drop` do not collide (exact attribute
  selectors), but no code may select `[data-okf-list-item^=…]`.
- Tests:
  - `test/page/runtimeHarness.ts` (1153 lines, limit 1500): fake DOM; `querySelectorAll` and
    `closest` answer **only exact selector strings** (l.140..268: `"ul, ol"`, `"li"`, `"table"`,
    `[data-okf-row-handle]`…). Every new selector the feature uses (`[data-okf-list-item-handle]`,
    `[data-okf-list-handle-layer]`, `aside.admonition`…) must be added there, plus a
    `contentLists` feed like `contentTables` (464).
  - `test/page/runtimeTableRowMove.test.ts` (771 lines): model (`pipeTable` fake, `handleOf`,
    `dragEvent`, `altKey` and `sourceReply` from `runtimeTestSupport.ts`).
  - The real-renderer precondition test: `test/session/listItemEditOpen.test.ts` +
    `test/session/mappedHtmlDom.ts` (selector subset: tag, classes, attributes only).
  - `test/core/preview/previewStyles.test.ts`: has no `TABLE_HANDLES_CSS` assertion today; add the
    list one.
- Visual:
  - Fixtures: highest number is **89** (`89-maths-offline.md`; two `88-*`). Next: **`90-list-item-handles.md`**.
  - Block-editing scenario ids: highest `block-editing/v35`; next **v36**.
  - **(mismatch)** `test/visual/scenarioDefinitions2.ts` is at **1500 lines (the test limit)** and
    `scenarioDefinitions1.ts` at 1459: do not add there. Follow `tableInContainerScenarios.ts`: a new
    `test/visual/listItemHandleScenarios.ts` exporting an array, spread in
    `scenarioDefinitions1.ts` (as `TABLE_IN_CONTAINER_SCENARIOS`, imported at l.51). Ids live inline
    in the scenario file; `scenarioIds.ts` (947 lines) holds the older id map.
  - Real drag capture: `test/visual/capture_table_move.py` (`check_table_move`, imported by
    `capture.py:112`) is the model for a held mouse drag.
- Real window: **(mismatch)** `tableMoves.ts` is `test/integration/tableMoves.ts`, not under
  `realInput/`; it is registered in `test/integration/realInput/run.ts:16`
  (`import { scenarioTableMoves } from "../tableMoves"`). Add `test/integration/listItemMoves.ts`
  beside it and register it the same way.
- Requirements:
  - CR-424's item SwRS is **SwRS-MDOKFSTUDIO-BLOCK-014** ("A click or Enter on a mapped block opens
    its editor"), tagged on `sourceRangeForList`/`sourceRangeForItem`; also BLOCK-254 (inner block
    from the keyboard). Note the ids clash only in tier: **StRS**-MDOKFSTUDIO-BLOCK-014 ("A writer
    reorders blocks with arrows, keys and selections", `req_lifecycle: proposed`) is the one to
    amend; **SwRS**-BLOCK-014 goes under "Related requirements". Write the tier prefix every time.
  - Model: `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-002.md`.
  - **SwRS-MDOKFSTUDIO-BLOCK-130 vs Decision 1 (mismatch, to report, not to fix here):** its
    normative text and scenario tables say the chord in a block editor's text box "moves the block"
    and never name the list item editor. "In a list item editor the chord moves the whole list" is
    only in "Verification notes" (T37 of `test/page/runtimeBlockMoves.test.ts`). The behaviour
    matches Decision 1; the requirement does not state it as a scenario row.
  - `requirements/tiers/log.md`: heading `## 2026-11-20` exists (CR-424 entry "A click on a list
    item edits that item…" under it); add `### List item handles`.
- Docs: `docs/user/editing.md:45` CR-424's item paragraph; `CHANGELOG.md:3` `## Unreleased`;
  glossary `.agents/glossary/common.md:36` "List item editor" (the new "List item handle" goes right
  after it).

## 3. Smallest change

As the spec: `src/page/modules/listItemMove.ts` (pure, `moveListItem`), the shared quote-prefix
reader out of `tableInContainer.ts`, `src/page/features/listItemMove.ts`
(`installListItemMove`), `ListItemMove` + `listItemMove` + `MappedBlocks.listRange` in
`pageRuntime.ts`/`mappedBlocks.ts`, four one-line wirings, `LIST_ITEM_HANDLES_CSS` in
`editModeStyles.ts`. No host, protocol or session change.

## 4. Risks

- Trailing blank line in the list range (section 1): rule A.4 must cover a trailing gap.
- Placement: the handle column for a list in containers is the outermost container's left edge;
  a top-level `aside`/`blockquote` must then get the push attribute, not the `ul`. Every box read
  before any write (issue 420), in the next frame (issue 423), as `position()` does.
- `li` heights: an item whose list or container is open as raw Markdown has height 0 → hide.
- Nested lists inside a moved item are re-rendered: the focus-back uses the list's first line and
  the new index, not the old element.
- Harness selectors are exact strings: a selector written differently in the feature silently
  finds nothing in the tests.
- The `{list-table}` uses `ul` source for its rows: a `{list-table}` renders a `table`, so its `ul`
  never reaches the page; nothing to exclude, but the spec's out-of-scope note on lists inside
  list-table cells applies.
- No element other code measures from changes size, except the pushed block (`margin-inline-start:
  2.2em`), as for tables; the existing table push values are not changed.

## 5. Questions only the user can answer

None blocking. The spec's "Design choices" stand unless the Chief of Staff raises them.

## 6. Evidence plan

Kind: a page feature (edit mode, drag and keys) with a pure text module, styles and requirements.

- Unit/contract (`just check`, Windows and Linux CI):
  - `test/page/modules/listItemMove.test.ts` (new): as the spec lists, **plus a trailing blank line
    (`>` and empty) after the last item staying at the end**.
  - Precondition, real renderer: a new test in `test/session/` (e.g. `listItemRange.test.ts`) on
    `renderMappedPage` + `createMappedBlocks(...).listRange(list)`, for the quote, the alert, both
    admonition forms and two nested admonitions: each `li` carries its lines and the range covers
    only the list (the table of section 1). Not in `runtimeHarness` (no renderer there).
  - `test/page/runtimeListItemMove.test.ts` (new) on `runtimeHarness.ts`: handles, drag, keys,
    move, refusals, push, reads-before-writes and next-frame, as the spec lists.
  - `test/core/preview/previewStyles.test.ts`: the shipped `LIST_ITEM_HANDLES_CSS`.
  - Each new behaviour test fails at `e05f0b51` (constitution section 3): run them once on the base.
- Visual (`just ci-visual`, heavy CI): fixture `test/visual/fixtures/90-list-item-handles.md`,
  scenarios `block-editing/v36…` in a new `test/visual/listItemHandleScenarios.ts` spread in
  `scenarioDefinitions1.ts`; light, dark, cream at 900 px, one at 360 px for the push; a held drag
  modelled on `capture_table_move.py`; the rectangle assertion of the spec.
- Real window (heavy CI, `gh workflow run ci.yml --ref <branch> -f heavy=true`): new
  `test/integration/listItemMoves.ts` registered in `test/integration/realInput/run.ts` beside
  `scenarioTableMoves`; the six checks of the spec (Linux, macOS for the Alt chord).
- PR before/after: screenshots from the visual captures (light and dark): handles on a list, handles
  outside an admonition, the drag line, an ordered list before and after a move (the "before" of a
  move is the same capture without the drop).
- Gates: `just check`, `just requirements-lint`, `just preflight` (static stage on Windows), then
  the heavy CI dispatch.
- Cannot be shown locally on Windows: the visual and real-window jobs (they run on CI).
