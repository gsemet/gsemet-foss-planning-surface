# Round 1 Coder report (summary)
Fix: refused state in frontmatterEditor.ts (edit.refusedText, refocus after refusal only when focus on body/control/inside cell,
holdsRefusedText, closeRefusedEditorFor); pageRuntime.ts types; frontmatterValueEditor.ts 4 lines (focusControl for list editor,
holdsRefusedText early return on blur and list focusout); pageInput.ts calls closeRefusedEditorFor(cell) before opening a field
(capture click, click, Enter/Space). Real-input E2E scenarioRefusedValueKeepsEditorUsable (RI-T44) in frontmatterFields.ts + run.ts,
not run locally. Unit: 3 round-0 tests + 2 new (changed text saved once by blur; key editor refocus), 5/39 failed before fix.
FMEDIT-019 and BLOCK-041 (proposed) updated, known issues removed; coverage via okfreq update-coverage. No approved req changed.
Gates: just check green (one unrelated flake on first run, toolbarReq wikilink search, 3/3 alone); okfreq validate 0 errors.
Shots after-refused-{dark,cream}, after-click-other-{dark,cream}. Open: no focus ring in shot (programmatic focus no :focus-visible);
Enter on unchanged refused text still retries (only blur suppressed); list editor refocus untested.
