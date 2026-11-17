# T28 review — round 1

Base: da76908 · Reviewed diff: 7 files, +516/-6

## Gates
- compile/unit/types: PASS (logs/T28-impl-unit.log, logs/T28-impl-types.log)
- trusted: PASS incl. RI-T28 (logs/T28-impl-trusted.log)
- scroll: PASS
- visual: PASS vs baseline, 0 new failure lines. Remaining failures (preview-sticky-headings-*) are
  T00 baseline failures.

## Done-when
- [x] Insertion points after each top-level block with correct N, none in reading mode — unit T28
  tests in scrollSync.test.ts ("points after each block… none in reading mode", recreated not duplicated).
- [x] Empty / frontmatter-only body shows one `Start writing` (N=0) — unit tests + RI-T28 screenshot 24.
- [x] Click posts `previewEditOpen` with `insertAfterLine`; empty reply → empty textarea with the
  placeholder; Done posts `previewEditSave` with `insertAfterLine` and `originalText: ""` — unit tests.
- [x] `insertAfterLine` in save (autosave and final) and cancel — unit test "autosave/Revert carry insertAfterLine".
- [x] RI-T28: exact buffers `# Incident review checklist\n\nFirst paragraph.\n` then
  `# Incident review checklist\n\n- check logs\n\nFirst paragraph.\n`; scrollHeight / last paragraph
  top within 2 px on edit-mode toggle — realInput.test.ts, screenshot 25 confirms the order.
- [x] README sentence added verbatim.
- [x] Insertion points never appear in `topLevelMappedBlocks()` (no source attributes; selector
  is `mappingsSelector`).

## Protected features checked
- T16 no-reflow: point has height 0, margin/padding/border 0, only an absolutely positioned child,
  so margins collapse through it. Mappable tags (admonition, lists, figure, table…) are mapped as a
  whole, so points are only inserted between siblings at section level; no `:last-child`/`+`
  selectors in previewStyles.ts or sphinx/_static/css target section children (checked by grep;
  existing `li > p:last-child`, `figure > p:last-child`, admonition `> :last-child` are never
  affected because their parents are mapped). RI-T16 and the new RI-T28 measurement pass.
- P-E4 arrow navigation / `adjacentMappedBlock`: uses `topLevelMappedBlocks()`, unaffected.
- Scroll sync / sticky band: mapping queries use `mappingsSelector`; points carry no source
  attributes; scroll gate PASS; sticky visual failures are baseline-only.
- T14 caret mapping: operates inside the mapped target; untouched.
- Table/frontmatter editors, checkbox toggling: click early return only triggers for targets inside
  `.sphinx-preview-insert-point`; the button's own listener stops propagation anyway, so the document
  handler change is purely defensive. Keydown early return only for focus inside a point (a BUTTON,
  which the next line already excluded). Nothing else is swallowed.
- Reading mode copy/selection: points removed in `applyEditMode(false)` via `refreshInsertPoints`,
  plus `display:none` CSS outside edit mode.
- P-S2/P-S4: no new incoming message types; labels set via `textContent`/`setAttribute`.
- Conventions §2: new runtime code has no backtick or `${`, no unescaped backslash, no global setTimeout.

## Deviations judged
- `New block · …` hint: correct; "Line 1" would be wrong for N=0. Accepted.
- Start writing only on a rendered preview: sensible (a failed render body is not "empty"). Accepted.
- `+` while another editor is open commits first and needs a second click: consistent with the
  one-editor rule; no data loss. Accepted (MINOR follow-up below).
- Visual scenario reuses the list-hover step: screenshot shows the `+` revealed in the left gutter
  below the hovered top-level list, not clipped, no text covered, no layout shift. Accepted.

## Findings
1. [MINOR] src/webview/scrollSync.ts:createInsertPoint — the `+` buttons are in the Tab order while
   invisible (opacity 0); a keyboard user tabs through one per block. They become visible on
   `:focus-visible`, so it is usable. Follow-up option: none required now.
2. [MINOR] src/webview/scrollSync.ts:createInsertPoint click — with another editor open the first
   click only commits it. Follow-up: after the commit, open the insertion editor (e.g. defer via
   the existing pending-navigation mechanism). Not required for this task.
3. [NIT] test/integration/realInput.test.ts RI-T28 — the document is named `smoke.md` in a
   `realinput-t28-*` fixture folder rather than `scratch.md`; behaviour tested is identical.

## Existing assertions changed
- "activating a centered block editor preserves scroll…": `insertedElements[0]` →
  `blockEditorOf(mappings[1])` — OK. Same element (found by `data-sphinx-preview-block-editor`);
  if absent the helper returns undefined and the test throws, so it is not weaker.
- "fenced Markdown editors sit outside the rendered pre…": `pre.insertedElements[0]` →
  `blockEditorOf(pre)` — OK, same reasoning; `code.insertedElements.length === 0` kept.

VERDICT: PASS
