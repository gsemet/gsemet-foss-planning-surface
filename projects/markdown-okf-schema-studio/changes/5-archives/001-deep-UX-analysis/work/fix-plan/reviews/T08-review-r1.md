# T08 review — round 1

Base: 0ffd6ba · Reviewed diff: 5 files, +194/-16 (extension tree only; `book/chapters/05-skills.md`
is a pre-existing unrelated working-tree change, not part of T08)

## Gates
compile: PASS · unit: PASS · types: PASS · trusted: PASS (logs/T08-trusted.log, RI-T08 screenshots
13/14 captured) · visual: PASS vs baseline, 0 new failure lines (logs/T08-visual.log; the updated
"Escape in a table cell did not commit" check does not appear in logs/T08-visual-failures.txt).
Pre-fix evidence: logs/T08-impl-prefix-trusted.log (RI-T08 timed out on the Escape commit).

## Done-when
- [x] unit and trusted gates pass; RI-T08 passes — evidence: gate logs above, scenario
  `scenarioEscapeKeepsText` in realInput.test.ts.
- [x] `rg -n "closeBlockEdit\(true\)" src` finds no caller — verified, zero matches.
- [x] Escape in block textarea commits — unit "Escape in a changed Markdown block editor saves the
  text and never cancels"; RI-T08 part 1; screenshot 13 shows `Second paragraph. KEEP ME PLEASE.` in
  buffer and preview, no editor.
- [x] Unchanged + Escape → no message, editor removed — unit "Escape in an unchanged Markdown block
  editor closes it without a message" (`postBlockEditSave(true)` → `closeBlockEdit()` path).
- [x] Table cell Escape commits — unit "Escape in a changed table cell…"; RI-T08 part 3; screenshot
  14 shows `| beta | two2 |`.
- [x] Edit mode off commits (changed) / silent (unchanged), not-loaded → `closeBlockEdit(false)` —
  unit "turning edit mode off saves a changed block editor and ignores an unchanged one"; RI-T08
  part 2 (` B` kept).
- [x] Cancel branch of `closeBlockEdit` kept with Revert comment; `handlePreviewEditCancel` untouched.
- [x] README Edit-mode sentence replaced; other sentences kept.

## Protected features checked
P-E3: blur and Cmd/Ctrl+Enter handlers unchanged (only the Escape branch edited); existing
"raw Markdown block edits autosave…" tests green. P-E4: `navigateBlockEdit` still runs before the
Escape branch; "arrow boundaries transfer block editing…" green. P-E5: table switching/finalize tests
green, Escape now finalizes via the same `postBlockEditSave(true)`. P-E6: save message carries
documentVersion/requestId/editId as before; no new message type (P-S2 unaffected). P-E7: frontmatter
Escape handlers untouched; frontmatter tests unchanged and green. P-E8: no new interactive surface;
the `applyEditMode(false)` change only acts on an existing `activeBlockEdit`. P-S4: no innerHTML.
Conventions §2: no backticks or `${` added in the template.

## Findings
1. [MINOR] README.md "Edit mode" paragraph — the new line `clicking elsewhere, or Cmd/Ctrl+Enter
   keeps your changes. The frontmatter properties table also becomes editable. Schema-backed enums use
   dropdowns,` exceeds the 100-character wrap rule. Fix: rewrap that paragraph at clause boundaries
   to ≤100 chars (text unchanged).
2. [MINOR] test/visual/capture.py `check_preview_edit_mode` — `original_cell_html` is now unused
   (report acknowledges). Fix: remove the assignment, or leave for T15 Revert check; log as followup.
3. [NIT] No unit test covers `applyEditMode(false)` with an open *table cell* editor, nor with a
   block whose source has not loaded yet (`closeBlockEdit(false)` branch). Code path is trivially
   correct (`postBlockEditSave` handles `tableInput`); optional test for followups.

## Existing assertions changed
- scrollSync.test.ts "fenced Markdown editors sit outside the rendered pre…" — OK (listed in the
  task's expected changes; now asserts a stronger final-save + no-cancel).
- scrollSync.test.ts "table cell editing exposes row and column operations…" — OK (same).
- scrollSync.test.ts "table editing switches cells without losing changes…" — OK (same; also checks
  `edited q` in the saved text).
- capture.py table-cell journey — OK (task allows; mock host never re-renders, so asserting the
  final save is the correct replacement, not a weakening).

VERDICT: PASS
