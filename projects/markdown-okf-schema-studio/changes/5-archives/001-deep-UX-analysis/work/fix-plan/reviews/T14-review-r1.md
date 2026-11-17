# T14 review — round 1

Base: 433bbd8 · Reviewed diff: 6 extension files (scrollSync.ts, textEditing.ts, realInput.test.ts,
capture.py, scrollSync.test.ts, textEditing.test.ts), about +230/-12. (`book/chapters/05-skills.md`
is a pre-existing unrelated working-tree change, not part of this task.)

## Gates
- compile/unit/types: PASS (orchestrator summary; logs/T14-impl-unit.log)
- trusted: PASS, exit 0, RI-T14 included (logs/T14-trusted.log)
- visual: PASS vs T00 baseline, 0 new failure lines (logs/T14-visual.log), after the
  orchestrator-authorised capture.py check change.

## Done-when
- [x] `unit` and `trusted` gates pass — logs above.
- [ ] RI-T14 proves "X landed on source line 1, within `bravo` or immediately next to it" — the
  assertion does not prove it (Finding 1).
- [x] Fallback to end of block when mapping is not confident (D-21) — `focusTextControlAtLastContent`
  keeps `trimEnd().length` unless `mapRenderedCaret` returns a valid integer; unit test
  "without caretRangeFromPoint a click opens the editor with the caret at the end of the block".
- [x] Keyboard/arrow navigation keep "start"/"end" — object contexts only come from the mouse click
  listener; `rememberPendingBlockNavigation` coerces objects to `"end"`;
  `resumePendingBlockNavigation` unchanged.
- [x] Mapper unit cases (paragraph, emphasis, link label, list, heading, ambiguous, no match) —
  `textEditing.test.ts` "mapRenderedCaret …".

## Protected features checked
- P-E2: editors still open the same ranges; `openMappedEditor` logic unchanged, only its caret arg
  differs. Covered by existing scrollSync tests + visual `check_preview_edit_mode` (PASS).
- P-E3: commit/autosave paths untouched; trusted suite PASS.
- P-E4: arrow navigation passes strings; `pendingBlockNavigation` persists strings only. Existing
  "arrow boundaries transfer block editing…" passes.
- P-E5: `clickCaretContext` returns `undefined` for `td, th`, so table cells keep their own caret.
- P-E7 / P-N6 / UX-22/24/34: properties table excluded (`[data-okf-properties]`), nothing touched.
- P-E8: the path is behind `if (editMode)`; read-only previews unaffected.
- Conventions §2: the new runtime code has no backtick/`${` in the template; `textEditing` is
  injected via `toString()` interpolation, so its backtick literal is safe (trusted run proves it).
  Browser APIs are feature-tested and wrapped in try/catch. No new messages (P-S2 n/a).

## Findings
1. [MAJOR] test/integration/realInput.test.ts:`scenarioCaretAtClick` — the assertion
   `/Alpha .*X?bravo|Alpha bXravo|Alpha brXavo/u` matches any line containing "Alpha … bravo",
   because `X?` is optional and `.*` is unanchored; combined with the second check (line starts
   with "Alpha " and contains X) it passes for `Alpha bravo charlieX` — a caret at the end of
   line 1 would not be caught. Fix: replace both assertions with one exact check:
   `assert.match(firstLine, /^Alpha (?:Xbravo|bXravo|brXavo|braXvo|bravXo|bravoX) charlie$/u, "X lands in or next to bravo: " + firstLine);`
   Re-run the trusted gate and confirm RI-T14 still passes.
2. [MINOR] src/webview/scrollSync.ts:`clickCaretContext` — the editing-element choice
   (`closest("ul, ol") || closest("pre") || target`) is duplicated from `openMappedEditor`
   instead of factored out as the task asked; it also diverges when `sourceRangeForList` returns
   undefined (editor opens on `target`, context comes from the whole list). Harmless today (the
   mapper falls back to end on miss), so logging as a follow-up: extract
   `editingElementFor(target)` used by both.
3. [MINOR] textEditing.ts:`mapRenderedCaret` — code blocks: `*`, `_`, `~`, backticks inside
   fenced code and backslash escapes (`\*`) are stripped/kept differently from the rendered text,
   so clicks near them fall back to end-of-block. Acceptable under D-21; follow-up: add a unit
   case for a fenced code block (` ```py\nfoo_bar = 1\n``` `, before `"foo_b"`) documenting the
   result.

## Existing assertions changed
- test/visual/capture.py `check_preview_edit_mode` block-editor caret check — OK: matches the
  orchestrator amendment exactly (word captured at the target centre via `caretRangeFromPoint`,
  >= 3 chars, ±40-char window; `None` keeps the D-21 end-of-block assertion; focus, collapsed
  selection and visible caret kept; renamed message with diagnostics). The added
  `scroll_into_view_if_needed()` is justified (makes the measured centre the clicked point).
  No other capture.py change.
- No unit/integration assertion modified or deleted.

VERDICT: CHANGES REQUESTED
