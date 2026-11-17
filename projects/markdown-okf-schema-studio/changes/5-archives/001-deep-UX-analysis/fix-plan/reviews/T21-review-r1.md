# T21 review — round 1

Base: 28ac5b8 · Reviewed diff: 4 files, +335/-0

## Gates
compile: PASS (logs/T21-compile.log) · unit: PASS (logs/T21-unit.log) · types: PASS (logs/T21-types.log)
trusted: PASS (logs/T21-trusted.log; RI-T21 frames 27-list-click-edits / 28-list-enter-adds PASS) ·
visual: PASS vs T00 baseline, 0 new failure lines (logs/T21-visual-failures-normalized.txt).

## Done-when
- [x] Edit-mode plain click on okf link opens the field editor, no `previewLink` — unit "T21: in edit mode a plain click..." (failed before: `0 !== 1`), RI-T21 (documentUri unchanged).
- [x] Cmd/Ctrl+click navigates in edit mode — unit T21 Cmd/Ctrl test, RI-T21 (`StRS-A.md` becomes active editor).
- [x] Reading mode navigates — unit T21 reading-mode test; listener returns first on `!editMode`.
- [x] Enter inserts an empty item after the current one, focused, no save — unit T21 Enter test.
- [x] Enter on empty last item removes it and saves once — unit test + RI-T21 (buffer delta exactly `+ - StRS-B`).
- [x] Backspace on empty item removes it and focuses previous / next / add button — 3 unit tests; non-empty Backspace untouched test.
- [x] Cmd/Ctrl+Enter saves — unit test.
- [x] README sentence — README.md Edit mode paragraph.

## Protected features checked
- P-N6: reading-mode navigation untouched (`linkNavigation.ts` not modified; capture listener exits on `!editMode`); Cmd/Ctrl+click in edit mode falls through to `installLinkNavigation` (unit + RI-T21). Marker-line selection and UX-22 resolution are in `linkNavigation`/host code, untouched.
- Capture listener scope: only intercepts when target is inside `a[data-sphinx-preview-navigation^="okf-link:"]` inside a `[data-okf-edit-cell]` value cell of a `tr[data-okf-field]` with `data-okf-editable="true"`. Body links (no edit cell), the name cell, non-editable rows and the table toolbar (no okf link) are not swallowed. When another editor is open, `openFrontmatterEditor` is a no-op (line 954 guard) — the click is swallowed but that matches the task spec.
- P-E8 read-only: no edit mode → listener inert; list editor only exists in edit mode.
- List editor: focus moves before row removal so the editor `focusout` (relatedTarget inside editor) does not save; the empty-last Enter path calls `saveValue()` exactly once. The control-level Enter handler is skipped for list editors (`!useListEditorValue`), so no double save. Escape still handled by `control` keydown (item keydown does not stop propagation). Drag/keyboard reorder and remove button code unchanged.
- Webview template rules (§2): no backticks or `${` added inside the runtime; optional calls guarded.

## Findings
1. [MINOR] scrollSync.ts: `installLinkNavigation` keydown — Enter on a focused okf link in edit mode still navigates, while a click edits. D-07 only specifies click, so this is consistent with the decision, but keyboard users have no way to open the editor from the link itself. Follow-up: log in `followups.md`; optionally make Enter on a focused okf link in an editable value cell open the editor in edit mode (Cmd/Ctrl+Enter navigates), with a unit test mirroring the click test.
2. [NIT] The `data-okf-editable` / name-cell guard is an extra beyond the task text; it is correct and consistent with D-07 (a non-editable row's link keeps navigating rather than becoming a dead click). No change needed.

## Existing assertions changed
None. Only the fake DOM `closest` gained the two okf-link selectors — OK.

VERDICT: PASS
