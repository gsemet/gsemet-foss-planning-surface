# T16 review — round 1

Base: 1bf9c8a · Reviewed diff: 4 files, +58/-25

## Gates
- compile: PASS (logs/T16-compile.log); types: PASS (logs/T16-types.log)
- unit: PASS (logs/T16-unit.log)
- trusted: PASS incl. RI-T16 (logs/T16-trusted.log)
- scroll: PASS, edit-mode scenarios included (logs/T16-scroll.log)
- visual: PASS vs T00 baseline with normalized signatures (logs/T16-visual.log,
  logs/T16-visual-failures-normalized.txt vs logs/T16-visual-baseline-normalized.txt). The only
  textual differences are 4 baseline "table action bar is not aligned with its active cell" lines
  (08-okf-schema dark/light) whose coordinates move by 0.39 px, an expected effect of paragraphs
  no longer reflowing. 4 baseline edit-paragraph lines now pass.

## Done-when
- [x] unit, trusted, scroll, visual gates pass — logs above.
- [x] RI-T16 passes — `scenarioEditModeNoReflow` in test/integration/realInput.test.ts; it failed
  before the fix (`scrollHeight changed from 982 to 1117`, logs/T16-impl-pre-trusted.log).
  Fixture wraps at ~40 chars instead of ~60; justified (60-char lines fit one rendered line in
  the side preview, so the test would not fail before the fix). Accepted.
- [x] Both CSS rules deleted (previewStyles.ts), nothing else in the file changed.

## Protected features checked
- P-N1 (scroll anchoring R1–R9, incl. line-level R3): `measureLineTops` untouched; scroll gate
  PASS. No capture.py check of edit-mode scroll mapping was modified.
- P-E3 (raw editor keeps line breaks): the editor textarea rules are untouched; screenshot
  logs/visual-T16/edit-admonition-dark.png shows the warning source on its own lines in the editor.
- Sticky headings: untouched; sticky visual results unchanged vs baseline except sub-pixel
  coordinates noted above.
- P-E8 / P-S*: no protocol or runtime change.

## capture.py changes — explicit judgement
1. `check_preview_edit_mode`, paragraph style check: old check required `pre-wrap` +
   `overflow-wrap: anywhere`; this asserted the removed rule exactly. In scope. New check asserts
   no non-table paragraph is `pre-wrap`, which is the new behaviour; the horizontal-overflow
   check is kept. OK.
2. `check_preview_edit_mode`, 08-okf-schema warning paragraph: old check "spans at least 2
   rendered line tops / did not expand to its source lines". The warning body ("This warning must
   be acknowledged before calibration.") is one short sentence that fits on one rendered line at
   the capture width; it only spans 2 tops because `pre-wrap` honoured the source newline. So it
   asserted the pre-wrap expansion, not scroll mapping (it reads no anchor map, no scroll
   position). In scope. The replacement (computed `white-space` is not `pre-wrap`) checks the
   new behaviour at the style level. It is weaker than a layout assertion, but the layout
   guarantee is covered by RI-T16 (height and top within 2 px). Accepted; see MINOR 1.

## Findings
1. [MINOR] test/visual/capture.py:check_preview_edit_mode — the warning-paragraph replacement
   only checks computed style. Fix (follow-up, optional): keep the style check and additionally
   assert the rect-top count of the warning body (same `range.getClientRects()` snippet as the old
   code) equals 1, with failure text "warning paragraph reflowed in edit mode". This makes the
   visual check prove layout, not just CSS.

## Existing assertions changed
- previewStyles.test.ts edit-mode pre-wrap `assert.match` → task's `doesNotMatch` regex: OK
  (listed in task).
- previewStyles.test.ts table exception `assert.match` → `doesNotMatch` that no such rule exists:
  OK (task: "same for the table exception rule").
- capture.py paragraph style check: OK (pre-wrap assertion, in scope).
- capture.py warning paragraph line-count check: OK (pre-wrap expansion, in scope; not P-N1).

VERDICT: PASS
