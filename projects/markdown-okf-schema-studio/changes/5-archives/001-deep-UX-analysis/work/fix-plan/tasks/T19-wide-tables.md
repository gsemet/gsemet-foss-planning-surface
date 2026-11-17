# T19 — Wide tables keep identifiers whole and show that they scroll

| Field | Value |
| --- | --- |
| Fixes | [UX-15](../../02-table-editing/UX-15-wide-table-layout.md) |
| Decisions | D-19 |
| Depends on | T03, T18 |
| Gate | `unit trusted visual` |
| Risk | Low (visual only) |
| Commit message | `fix(vscode): keep short table cells on one line and signal horizontal overflow` |

## Goal

When a content table is wider than the preview:

- cells whose text is a short identifier (≤ 24 characters, no whitespace) do not wrap;
- the overflow side shows a shadow cue, so mouse users see that the table scrolls.

Tables that fit are unchanged. The frontmatter properties table (`.okf-properties`) is excluded.

## Context to read first

- `src/preview/previewStyles.ts` → `#sphinx-myst-preview-content :where(table, .table-wrapper)`.
  The **table itself** is the horizontal scroll container (`display: block; overflow-x: auto;
  max-width: 100%`).
- `src/webview/scrollSync.ts` → `stabilizeLayout`, `measure`, and the initial `measure()` call at
  the end of the runtime.

## Allowed files

- `src/webview/scrollSync.ts`
- `src/preview/previewStyles.ts`
- `test/webview/scrollSync.test.ts`
- `test/webview/previewStyles.test.ts`
- `test/visual/scenarios.ts` (`machineChecks` on the wide-table scenario at narrow width)

## Steps

1. Runtime function `markWideTables()`. For each `#sphinx-myst-preview-content table` not inside
   `[data-okf-properties]`:
   - Mark short cells once: for every `th`/`td` whose trimmed `textContent` matches `^\S{1,24}$`,
     set `data-sphinx-short-cell="true"`.
   - Compute `overflowing = table.scrollWidth > table.clientWidth + 1`. Set or remove
     `data-sphinx-table-overflow="true"`, and **only touch the attribute when the value changes**:
     the ResizeObserver must not loop.

   Call it before `measure()` in `stabilizeLayout` and before the initial `measure()`.
2. CSS:

   ```css
   #sphinx-myst-preview-content table[data-sphinx-table-overflow="true"] :where(th, td)[data-sphinx-short-cell="true"] {
     white-space: nowrap;
   }
   #sphinx-myst-preview-content table[data-sphinx-table-overflow="true"] {
     background:
       linear-gradient(to right, var(--vscode-editor-background, Canvas) 30%, transparent) left center / 2rem 100% no-repeat local,
       linear-gradient(to left, var(--vscode-editor-background, Canvas) 30%, transparent) right center / 2rem 100% no-repeat local,
       radial-gradient(farthest-side at 0 50%, rgba(0, 0, 0, 0.28), transparent) left center / 0.75rem 100% no-repeat scroll,
       radial-gradient(farthest-side at 100% 50%, rgba(0, 0, 0, 0.28), transparent) right center / 0.75rem 100% no-repeat scroll;
   }
   ```

   Check in the dark and white themes that the cue is visible. Adjust the shadow alpha if the
   reviewer finds it invisible, and note it in the report.
3. In `scenarios.ts`, add `machineChecks: ["identifier-split"]` to the narrow-width wide-table
   scenario(s) (fixture `04-code-and-tables`, width ≤ 640).

## Tests

- **Unit** (fake DOM): `markWideTables` sets the overflow attribute only when `scrollWidth >
  clientWidth + 1`; marks only short cells; skips the properties table; is idempotent (a second
  call changes no attribute; count `setAttribute` calls).
- **`previewStyles.test.ts`:** both rules exist.
- **Visual:** the wide-table narrow scenario passes `identifier-split`. The screenshot shows
  `nw-02` and `North` on one line, and a visible right-edge shadow.

## Expected changes to existing tests

None expected. If a visual check asserts that wide-table cells wrap, STOP and report.

## Must not change

- Tables that fit; the properties table; table cell editing (the editor overlay sits inside the
  cell).
- The horizontal-access visual check (`check_horizontal_access`) must still pass.

## Done when

- The `unit`, `trusted` and `visual` gates pass; `identifier-split` is required and passing on the
  wide-table narrow scenario.
