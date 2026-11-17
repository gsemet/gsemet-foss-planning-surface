# S8a, round 1: page runtime split (CODER report)

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-056`
(branch `changes-requests/056-refactor-host-neutral-core`, base HEAD `0d94248`). Nothing was
committed, pushed or stashed.

## Result

- `src/page/runtime.ts`: 4 965 lines with `@ts-nocheck` → 374 lines, fully type-checked. It only
  composes the page now: it installs the page modules and the new features in their original order,
  then binds the listeners in their original order.
- No `@ts-nocheck`, `@ts-ignore` or `@ts-expect-error` left in `src/`. There is no `any` in
  `runtime.ts` or `src/page/features/`, and no `as unknown as` double casts.
- The suppression allowlist is gone from `scripts/check-file-sizes.mjs`. A suppression in `src/` now
  fails without exception. CONTRIBUTING.md is updated to match.
- `test/page/runtime.test.ts` (10 225 lines) is split into 12 files, each at most 1 172 lines, plus a
  shared helper module. The assertions are identical.
- 10 page-module tests now import their module directly instead of running it through `vm` and
  `.toString()`.
- `chipToggle.ts` reads `readPreviewBootSettings(context).showComments`.
- The stale "injected with `.toString()`" doc comments are removed.

## Module map (`src/page/features/`, new files)

| File | Lines | Holds |
|------|------:|-------|
| `pageRuntime.ts` | 599 | The contract: `PageRuntime`, `PageRuntimeState`, the edit records (`BlockEdit`, `FrontmatterEdit`, pending navigation/move/frontmatter), `PageParts`, and the feature API interfaces |
| `mappedBlocks.ts` | 119 | Mapped and top-level blocks, the editing element of a block, `normalizeSourcePath` |
| `scrollCore.ts` | 523 | State snapshot, mappings, anchor and pins, restore, scroll posting, wide tables, layout stabilization, reading line, source scroll, anchor navigation (the S5 regex `/%[da-f]{2}/iu` is unchanged) |
| `textControls.ts` | 264 | Boundary navigation, Home/End, caret line probe |
| `blockEditor.ts` | 481 | Block editor life cycle: open, close, save, autosave, flush, cancel, pending navigation, page-hide flush |
| `blockSourceEditor.ts` | 341 | `previewEditSource`: builds the text box editor once the source arrives |
| `editorChrome.ts` | 415 | Palette placement and sticky behaviour, caret reveal, link and figure panels, figure editor |
| `tableCellEditor.ts` | 431 | Table cell editor and toolbar; pointerdown capture and Escape-cell keys |
| `frontmatterEditor.ts` | 391 | Frontmatter key editor, open, flush, close, results, the properties table update, pending edit |
| `frontmatterMenu.ts` | 227 | Field actions and the field picker |
| `frontmatterListEditor.ts` | 317 | List editor |
| `frontmatterValueEditor.ts` | 299 | Value editor (enum, boolean, text, YAML, list) |
| `blockSelectionView.ts` | 277 | Shift+click and Shift+Arrow selection, clipboard keys, blocks results |
| `insertPoints.ts` | 125 | Insertion points, Enter on an empty document |
| `blockMoves.ts` | 315 | Block and span moves (buttons, Alt+Arrow), move results |
| `editMode.ts` | 202 | Edit-mode toggle, edit hover, `openMappedEditor`, resuming navigation |
| `contentPatch.ts` | 156 | `applyContentPatch`, `initializeContent`, `postPreviewReady` |
| `pageInput.ts` | 245 | Document clicks and keys, Refresh, Description column, the two edit-mode capture clicks |
| `hostHandlers.ts` | 88 | The remaining `hostMessages.on` registrations, with the same bodies and return forms |

## Typing approach

- **One shared object.** Every feature gets one `PageRuntime` object (`rt`). It holds:
  - the services: document, window, context, host, pageHost, settings, anchorPolicy, diagnostics,
    bus, hostMessages;
  - the tools: tableTools, textEditing, blockSelection, editActions, figureTools;
  - a mutable `state: PageRuntimeState`, which replaces the closure `let`s;
  - `parts: PageParts`, the installed page modules;
  - one late-bound API slot per feature (`rt.scroll`, `rt.blockEditor`, …).
- **No cycles, no wiring order.** Features call each other only through `rt`, at call time. Installs
  register no listeners. Each feature exposes `bind*()` methods, and `runtime.ts` calls them where
  the old listener was added.
- **One cast in `runtime.ts`.** The cast is `{…} as Partial<PageRuntime> as PageRuntime`, made while
  the feature slots are still empty. No feature runs before `rt.parts` and every slot are filled.
- **Narrow DOM casts.** About 45 casts across `runtime.ts` and the features, mostly
  `querySelector<T>` results and the fake-DOM tolerant `childNodes ?? childElements` reads. The only
  stacked one is `as HTMLElement as FrontmatterControl`.
- **Small signature changes:**
  - `createEditActions(languages: readonly string[])`, because `HIGHLIGHT_LANGUAGES` is readonly.
  - `previewState` (Description toggle) now takes `documentId` from the snapshot by destructuring.
    The posted object is unchanged: the same keys, the same order and the same values. The snapshot
    used to overwrite that key anyway.

## Behaviour preservation

- Function bodies are moved verbatim; closure variables became `rt.state.*`.
- Listener registration order is unchanged for every event on every target. The two edit-mode
  capture clicks are still bound before link navigation; the checkbox click handler is still bound
  first among the document clicks.
- DOM elements are still created in the same order (the harness tests find elements with
  `createdElements.find`).
- The saved state is still read at the same point.
- Router handlers return the same values (for example `labelRename.receive` and
  `plantUmlFileRequests.receive` are still expression arrows).
- The S1 `EXPECTED_TRACE` (`test/page/runtimeBundle.test.ts`) passes unchanged, and so does the
  startup trace in `runtimeContentPatch.test.ts`.

## Tests moved

- **Direct imports instead of `vm` and `.toString()`:** chipToggle, codeCopy, commentCompose,
  commentsToggle, commentThreads, incomingChanges, inlineThread, labelRename, linkNavigation,
  motion. The `vm` sandboxes supplied only one non-standard global, `Element`. It is now set with
  `provideGlobalElement()` (new in `test/page/modules/fakeDom.ts`); each test file runs in its own
  process. Fakes are passed with `as never`. Assertions are unchanged; 120/120 pass.
- **`runtime.test.ts` split.** Each new file keeps the original test order and the helpers only it
  uses. The 44 helpers used by several files moved to `test/page/runtimeTestSupport.ts` (456
  lines), exported, with TSDoc.
  - Check: a line-multiset comparison against `HEAD:test/page/runtime.test.ts` finds no line
    missing. The only added lines are imports, file doc comments and `export` prefixes.
  - Test count: 450 tests before and after (459 with runtimeBundle).

| File | Lines | Covers |
|------|------:|--------|
| runtimeScroll.test.ts | 1 001 | scroll sync, sticky band, Description column, theme, anchoring, tooltips, pins |
| runtimeBlockEditor.test.ts | 1 150 | block editor, keys, autosave, marker wrapping, top spacing, empty document |
| runtimeTableCellEditor.test.ts | 1 021 | table cell editor and toolbar |
| runtimeFrontmatterEditor.test.ts | 1 071 | frontmatter key and value editors |
| runtimeFrontmatterFields.test.ts | 557 | okf links, list editor, picker, custom keys, properties table |
| runtimePageControls.test.ts | 645 | checkboxes, pairing, edit-mode toggle, pending overlay, toolbar view controls |
| runtimeBlockMoves.test.ts | 465 | insertion points and block moves |
| runtimeContentPatch.test.ts | 1 172 | startup trace and content patches |
| runtimeEditPalette.test.ts | 1 165 | palette, link panel, palette mode, table grid, emoji |
| runtimePaletteActions.test.ts | 753 | MyST, file dialogs, figure form, colours, cell bar, paste |
| runtimeBlockSelection.test.ts | 556 | block selection, clipboard keys, selection moves |
| runtimeEditorFlush.test.ts | 495 | slash menu, flushes (CR 025), editor trace (CR 041) |

## Baseline changes (`scripts/file-size-baseline.json`)

Generated with `node scripts/check-file-sizes.mjs --update`. Two entries were removed and nothing
was added or raised:
- `src/page/runtime.ts: 4965`
- `test/page/runtime.test.ts: 10225`

## Gates (foreground, Node 24 via `fnm exec --`, nothing left running)

- `npx tsc -p .`: clean.
- `npm run test:unit`: 2 302 tests, 2 302 pass, 0 fail.
- `UV_NO_CONFIG=1 UV_OFFLINE=1 just check`: exit 0.
  - format, compile;
  - boundaries: no violations, 271 modules;
  - check-limits: passed, 560 files, 9 on the baseline;
  - check-settings: passed, 18 settings;
  - unit 2 302/2 302, contracts 2/2, security 28/28, release-tests 31 passed.
- `UV_NO_CONFIG=1 UV_OFFLINE=1 just visual`: exit 0. 320 scenarios passed, 0 failed, 210
  screenshots, and no baseline PNG changed (`git status -- '*.png'` is empty).
- `npm run bundle`: done, `out/bundle/preview.js` is 287.9 kB.
- Not run: real VS Code integration and `just preflight` (forbidden by the CR rules).

## Open points

1. **Process conflict.** AGENTS.md says to run `just preflight` before a commit; the CR rules forbid
   it. I followed the CR rules.
2. **One "self-contained" comment kept.** The comment on `createHostMessageFilter` in
   `src/core/protocol/hostToPage.ts` still says "Every constant it uses is declared in its body".
   It stays true because `test/core/protocol/hostToPage.test.ts` and `router.test.ts` still rebuild
   their functions with `.toString()`. Those two tests were not in the S8a list.
3. **Remaining large files.** `src/page/features/pageRuntime.ts` (599 lines) and
   `src/page/modules/editActions.ts` / `editPalette.ts` (on the baseline) are the largest files
   left. They are not in this step.
4. **Doc references updated.** References to `runtime.test.ts` and `runtime.ts` were stale in
   `.agents/glossary/common.md`, `docs/scroll-anchoring.md` and
   `docs/feasibility-source-mapping.md`. They now point to the new files.
5. **`.venv`.** `.venv` shows as untracked: it is the symlink to the main checkout. Do not stage it.

## Paths to stage

Modified:
```
.agents/glossary/common.md
CONTRIBUTING.md
docs/feasibility-source-mapping.md
docs/scroll-anchoring.md
scripts/check-file-sizes.mjs
scripts/file-size-baseline.json
src/core/scroll/anchorPolicy.ts
src/core/security/spanColors.ts
src/page/modules/blockSelection.ts
src/page/modules/caretRect.ts
src/page/modules/chipToggle.ts
src/page/modules/codeCopy.ts
src/page/modules/commentCompose.ts
src/page/modules/commentsToggle.ts
src/page/modules/commentThreads.ts
src/page/modules/contentMorph.ts
src/page/modules/editActions.ts
src/page/modules/editorKeys.ts
src/page/modules/editorTrace.ts
src/page/modules/figureDirective.ts
src/page/modules/figurePanel.ts
src/page/modules/figureSizes.ts
src/page/modules/firstClearance.ts
src/page/modules/historyControls.ts
src/page/modules/hostRequests.ts
src/page/modules/incomingChanges.ts
src/page/modules/incomingToggle.ts
src/page/modules/inlineThread.ts
src/page/modules/labelRename.ts
src/page/modules/linkPanel.ts
src/page/modules/motion.ts
src/page/modules/pasteHtml.ts
src/page/modules/pasteImage.ts
src/page/modules/plantumlFileRequests.ts
src/page/modules/selectAllKey.ts
src/page/modules/slashMenu.ts
src/page/modules/spanColors.ts
src/page/modules/stickyBar.ts
src/page/modules/textEditing.ts
src/page/modules/tocColumn.ts
src/page/modules/toolbarCollapse.ts
src/page/modules/viewControls.ts
src/page/modules/warningBanner.ts
src/page/modules/widthMode.ts
src/page/runtime.ts
test/page/modules/chipToggle.test.ts
test/page/modules/codeCopy.test.ts
test/page/modules/commentCompose.test.ts
test/page/modules/commentsToggle.test.ts
test/page/modules/commentThreads.test.ts
test/page/modules/fakeDom.ts
test/page/modules/incomingChanges.test.ts
test/page/modules/inlineThread.test.ts
test/page/modules/labelRename.test.ts
test/page/modules/linkNavigation.test.ts
test/page/modules/motion.test.ts
```

Added:
```
src/page/features/blockEditor.ts
src/page/features/blockMoves.ts
src/page/features/blockSelectionView.ts
src/page/features/blockSourceEditor.ts
src/page/features/contentPatch.ts
src/page/features/editMode.ts
src/page/features/editorChrome.ts
src/page/features/frontmatterEditor.ts
src/page/features/frontmatterListEditor.ts
src/page/features/frontmatterMenu.ts
src/page/features/frontmatterValueEditor.ts
src/page/features/hostHandlers.ts
src/page/features/insertPoints.ts
src/page/features/mappedBlocks.ts
src/page/features/pageInput.ts
src/page/features/pageRuntime.ts
src/page/features/scrollCore.ts
src/page/features/tableCellEditor.ts
src/page/features/textControls.ts
test/page/runtimeBlockEditor.test.ts
test/page/runtimeBlockMoves.test.ts
test/page/runtimeBlockSelection.test.ts
test/page/runtimeContentPatch.test.ts
test/page/runtimeEditorFlush.test.ts
test/page/runtimeEditPalette.test.ts
test/page/runtimeFrontmatterEditor.test.ts
test/page/runtimeFrontmatterFields.test.ts
test/page/runtimePageControls.test.ts
test/page/runtimePaletteActions.test.ts
test/page/runtimeScroll.test.ts
test/page/runtimeTableCellEditor.test.ts
test/page/runtimeTestSupport.ts
```

Deleted:
```
test/page/runtime.test.ts
```

Renamed: none; git sees the test split as a deletion plus additions.
