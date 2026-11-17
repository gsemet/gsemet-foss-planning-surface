# T14 review — round 2

Base: 433bbd8 · Reviewed diff: 6 extension files, about +258/-39 (scrollSync.ts, textEditing.ts,
realInput.test.ts, capture.py, scrollSync.test.ts, textEditing.test.ts). `book/chapters/05-skills.md`
is a pre-existing unrelated working-tree change, not part of this task.

## Gates
- compile/unit/types: PASS (orchestrator summary).
- trusted: PASS, exit 0; `PASS real-input screenshot: 20-caret-at-click` present (logs/T14-trusted.log).
  The "CodeWindow: failed to load" lines are VS Code host noise, also present in the baseline.
- visual: PASS vs T00 baseline, 0 new failure lines (logs/T14-visual.log).

## Done-when
- [x] `unit` and `trusted` gates pass — logs above.
- [x] RI-T14 proves X lands on line 1 in or next to `bravo` — now one anchored assertion
  `/^Alpha (?:Xbravo|bXravo|brXavo|braXvo|bravXo|bravoX) charlie$/u`; an end-of-line caret
  (`Alpha bravo charlieX`) no longer matches. Trusted gate passes with it.
- [x] Fallback to end of block when mapping is not confident (D-21) — unchanged from r1, unit tests.
- [x] Keyboard/arrow navigation keep "start"/"end" — unchanged from r1.
- [x] Mapper unit cases, plus the new fenced-code case (`foo_b|ar = 1`).

## Protected features checked
- P-E1/P-E2: `editingElementFor(target)` returns `{list, range}` only when `sourceRangeForList`
  returns a range, otherwise `{target, undefined}`. `openMappedEditor` calls
  `openBlockEditor(editing.element, undefined, editing.sourceRange, caret)`, which is exactly the
  base behaviour (list + innermost range, else target with no range). Table-cell, active-edit and
  properties branches before it are untouched. The base `openMappedEditor` had no `pre` branch;
  code blocks open on `target` as before. The r1 `closest("pre")` in `clickCaretContext` is gone,
  so the caret context now uses the same element the editor opens on.
- P-E3, P-E4, P-E5, P-E7, P-E8, P-N6, UX-22/24/34: as in r1, no change this round outside the
  helper extraction.
- Conventions §2: helper has no backtick or `${`; uses optional chaining only.

## Findings
None blocking. Round-1 findings 1 (MAJOR), 2 and 3 (MINOR) are fixed.

## Existing assertions changed
- RI-T14 (new test of this task) tightened per r1 finding 1 — OK.
- capture.py caret check — unchanged since r1 approval of the orchestrator amendment — OK.
- No other unit/integration assertion modified or deleted.

VERDICT: PASS
