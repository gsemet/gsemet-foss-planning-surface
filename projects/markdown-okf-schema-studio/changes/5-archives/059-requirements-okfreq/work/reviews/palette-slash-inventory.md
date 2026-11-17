Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: palette-slash inventory (P10.1)

## Missing rows

All 168 checklist rows scoped `palette-slash` (168 distinct ids, scripted from `checklists/*.md`) are cited
in `inventory/palette-slash.md`: 161 in the behaviour table, 7 only in "Checklist corrections".
Of the 7 moved rows, the target inventory must cite them to count as handled:

- C-CL-023, C-AR-039 -> myst: cited in `inventory/myst.md` (ok).
- C-CL-090 -> table-editing: cited in `inventory/table-editing.md` (ok).
- C-CL-074, C-CL-084, C-AR-142 -> lifecycle-sync: NOT cited in `inventory/lifecycle-sync.md`.
- C-AR-079 -> toolbar-navigation: NOT cited in `inventory/toolbar-navigation.md`.

The 14 palette/slash rows that the checklists already give to other scopes (C-PAL-012/014/020/021/033/037/038,
C-SLASH-019/021/032/033/056/060/061, all `scope?` guesses) are not part of the 168; not verified in the targets.

## Missing behaviours

None of substance. Spot-checked against the source: host refusals of image paste/pick (all messages incl.
"Too many pasted images" = F-PALETTE-093 ">1000 suffixes"), 6/30 s/10 s/10 min request timeouts (F-087),
bib scan caps (20 files, 2 MB, 5 s), mystTargets caps (500 / 1000), paste HTML 1,000,000 char cap and
Shift+Cmd/Ctrl+V plain paste, htmlToMarkdown sanitising, read-only / untrusted / standalone refusals, stale
refusals, slash menu close on blur, mode precedence and setting fallback are all present. Minor, not counted:
the exact refusal text "Too many pasted images next to this document." and the sticky-bar/caret-reveal
details are only summarised.

## Wrong/unverifiable evidence

Scripted check over every F-PALETTE row: 141 `file:symbol` citations, 0 missing files, 0 missing symbols.
115 test-name citations (editActions.test, editPalette.test, slashMenu.test, runtimeEditPalette,
runtimePaletteActions): 108 found verbatim, 7 are abbreviated describe names ("editActions heading …",
"linkEdit …") that exist as describe/test prefixes (9 matches); none false. F-PALETTE-090 (untested):
confirmed, the refusal string "Citations are read from the workspace, which needs trust." appears only in
`src/session/features/hostRequests.ts`, no test. F-PALETTE-103 (untested, blur wiring): plausible. No
false evidence found.

## Count check

Behaviours 105 = 105 F-PALETTE ids (ok). Cov. column: 102 tested + 2 untested (F-PALETTE-090, 103) + 1 row
whose Evidence cell contains a pipe-free shift in my parse but is tested = 105; matches the Counts table.
Undocumented 21 = 21 rows mentioning "undocumented" (ok). Rows 161 + 7 = 168 (ok).

## Verdict

One real gap: 4 moved rows (C-CL-074, C-CL-084, C-AR-142 -> lifecycle-sync; C-AR-079 -> toolbar-navigation)
are not cited by their target inventories. Fix: have those two inventories cite the rows (as `n/a`
contributor tooling / VS Code Command Palette false positive), or keep them in palette-slash with an
`n/a` reason instead of moving them. Everything else is sound.

Verdict: REVISE

## Re-check

- Fix requested (4 moved rows): resolved by keeping C-CL-074, C-CL-084, C-AR-142 (now cited in F-PALETTE-071), C-AR-079 here as `n/a` in Checklist corrections; moved rows C-CL-023, C-AR-039 are cited in `| F-` lines of myst.md and C-CL-090 in table-editing.md (scripted).
- Checklist coverage: all 168 palette-slash ids are cited in F-PALETTE rows (162) or in Checklist corrections (6: 3 moved, 3 n/a); none missing. Spot-checked 8 evidence claims (syncPaletteSticky, bindPaletteSticky, handleListCitations text, GROUP_LABELS, menuEntries, blur close/destroy in blockSourceEditor, P11 and T35 test names, v04 lock id): all found.
- Remaining defect: Counts table says Tested 102, but the 105 F-rows are 103 tested + 2 untested (Cov. column; undocumented 21 and 162+6=168 are correct). Fix: set Tested to 103.

Re-check verdict: REVISE

Orchestrator note: Counts Tested corrected to 103 after the re-check. Re-check verdict: APPROVE (fixed)
