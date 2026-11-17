# CR 221, round 1: Inspector review

Worktree: `markdown-okf-schema-studio-wt-221` (uncommitted, base origin/main 0b4ede78).

## Verdict: APPROVE

The change does what the owner approved. In edit mode, the `:header:` and `:footer:` option editors
and the unlinked card title editor are one-line editors. Plain Enter saves and closes them through
the same path as Cmd/Ctrl+Enter (`finishEditorWithSelection("save", saveBlockEdit)`). Shift+Enter
is prevented and the editor stays open. The hint reads exactly
"Line N · Enter: done · Esc: cancel · ⌘↩: done", with "Ctrl+Enter" on other platforms. Detection
uses the renderer's `data-single-line` marker and never `line == endLine`. Linked cards are
unchanged: a linked title still gets no line properties and no marker.

## Checks run

- New tests fail on the old code. I reverse-applied the `src/` diff, recompiled and ran the three
  test files. 7 tests failed: the renderer marker test, the header, footer and title Enter tests,
  the Shift+Enter test, the hint test and the sanitizer test. The 3 guard tests passed, as they
  should: the linked-title test and the one-line paragraph and heading tests. I then re-applied the
  diff. The `git diff` is byte-identical to the one before (`cmp`).
- `just check`: exit 0, unit 3329/3329, 72/72 in the later suite, coverage and index checks report
  0 changes.
- `okfreq validate --check-links`: 1072 requirements, 0 errors. All 21 warnings are W2 warnings
  that were already there, in palette-slash files. None is in BLOCK-033 or BLOCK-258.
- Approved requirements: none edited. Of the changed SwRS, BLOCK-033 and BLOCK-258 are both
  `req_lifecycle: proposed` on origin/main.
- Visual scenario `block-editing/v27-card-header-enter-commits-line-cream-900` uses real Playwright
  input: `locator.click()` and `page.keyboard.press` for End, Space, Q and Enter. It uses no
  `force` and raises no timeout. `waitMs: 500` after the click matches v25 and v26. Id v27 is the
  next free number in block-editing. It is registered in `scenarioIds.ts`, and e2eGroups goes from
  410 to 411 with a reason in the message.
- Screenshots: `before-header-enter-cream.png` shows the bug, the caret on a new blank line under
  `:header:`. `after-header-enter-cream.png` shows the editor closed and the header rendered with
  " Q". `after-header-hint-cream.png` shows the new hint.
- No existing assertion was weakened. The only existing assertion that changed is the e2eGroups
  count, a plain +1.

## Edge cases reviewed

| Case | Result |
| --- | --- |
| IME composition | Both new branches require `!event.isComposing`, so Enter during composition commits the IME as before |
| Slash menu / palette popup open | `slashMenu.handleKey` and `palette.handleKey` run first and take Enter as before |
| Image alt-text exit | Still checked before the single-line branch, same as the SwRS table says |
| Autosave pending, source not yet arrived | Same `saveBlockEdit` path as Cmd/Ctrl+Enter; no keydown listener exists before the source arrives |
| Cmd/Ctrl+Enter, Ctrl+Enter on macOS | Unchanged existing branch: save |
| grid-item-card title | Marked (render test `div:12-12`) |
| Card inside tab item | Line attributes and marker are removed by `unmapPlainBlocks`; the tab item is the edited block, no marker |
| Card inside alert / admonition / list | `editingElementFor` returns a `sourceRange`, so `singleLine` is never set (guard `sourceRange === undefined`) |
| Table cell, insert point | Guarded by `!selectedCell` and `sourceRange === undefined` |
| Text already holding a newline (paste) | Enter saves it as it is: multi-line paste is out of scope per the owner |
| Linked card | Title not mapped, not marked; unchanged |

Sanitizer: `data-single-line` is added to the exact allowlist (`src/core/security/html-sanitizer.ts:94-96`).
The value is never read; only its presence is (`getAttribute(...) !== null`). It is not a URL,
style or event attribute, so it adds no script or resource surface. The only effect of an author
setting it by hand in raw HTML is that Enter means done in that block's editor. I see no XSS risk.

## Findings

### Blocking

None.

### Non-blocking

1. **Alt+Enter and Alt+Shift+Enter still reach the textarea** (`src/page/features/blockSourceEditor.ts:351-357`, `:359-361`).
   Both branches exclude `altKey`, so in a one-line editor Option/Alt+Enter falls through to the
   browser. In Chromium (the VS Code webview), Alt+Enter and Alt+Shift+Enter run `InsertNewline`
   in a textarea. That is the same blank line this CR removes, just reached by a rarer key. The
   owner spec only names Enter and Shift+Enter, so this is not a defect against the spec. Suggested
   fix: in a single-line editor, prevent any Enter that has no Meta or Ctrl and no composition in
   progress. I did not confirm this in a real browser.
2. **Tab still indents in a one-line editor while the hint no longer lists it** (`src/page/features/blockEditor.ts:474`, Tab branch in `blockSourceEditor.ts`).
   The approved hint drops "Tab: indent", but Tab still runs `indentSelection` and can indent the
   `:header:` or `:footer:` line. Consider ignoring Tab in single-line editors, or noting it as a
   follow-up.
3. **BLOCK-258 now covers two behaviours under a title that names only the first** (`requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-258.md:9-15, 45`).
   The title is "A click on a card title opens the editor on the directive line…". The new SHALL,
   Enter commits a one-line card editor, is a separate observable behaviour, joined to the old one
   with a semicolon. The guideline (Granularity: "One SwRS is one observable behaviour") points to
   a separate proposed SwRS, or at least a broader title. This is acceptable while the requirement
   is `proposed`.
4. **One row of the BLOCK-258 scenario table is not tested** (`SwRS-MDOKFSTUDIO-BLOCK-258.md`, table row "Enter while the slash menu, a palette popup or the alt text of an image takes the key").
   The code order makes this true, but no test sends Enter to a single-line editor while the slash
   menu or a palette popup is open. A runtime test would pin the order.
5. **Removing the marker in tab items is untested** (`src/core/render/mystGridToctree.ts:380`).
   It is defensive: without `data-line`, the element is not mapped anyway. A render test of a card
   inside a tab item would cover the line.
6. **The E2E covers the `:header:` line only.** The footer and the title (directive line) are
   covered at runtime-harness level only. That is enough for this fix. A title scenario would
   guard the directive-line path with real input.
7. **Style nit:** the existing `data-okf-` prefix allowlist would have avoided widening the exact
   allowlist (`data-okf-single-line`). The current choice is consistent with
   `data-line` / `data-end-line`, and either is fine.
