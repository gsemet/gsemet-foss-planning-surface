Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.1 critic review: myst inventory

Scope `myst`, reviewed against `inventory/myst.md`, the checklist rows with scope `myst`, and the mapped sources at
`markdown-okf-schema-studio-wt-059`.

## Missing rows

Scripted: 61 distinct checklist rows have scope `myst` or `myst?`; all 61 ids appear in `inventory/myst.md`
(49 kept in F-MYST rows, 12 in "Checklist corrections" as moved out). The 8 "moved in" rows are all cited by F-MYST rows.

Moved-out rows are handled only if the target scope's inventory cites them. Checked by grep:

| Row | Moved to | Cited by target? |
| --- | --- | --- |
| C-AR-049, C-AR-084, C-AR-092, C-CL-044 | rendering-core, table-editing, lifecycle-sync, rendering-core | yes |
| C-AR-001, C-AR-008 | block-editing | NO (0 hits in `inventory/block-editing.md`; C-AR-008 only in trust-security) |
| C-AR-019, C-AR-030 | layout-width | NO (0 hits in `inventory/layout-width.md`) |
| C-CL-060, C-CL-070, C-CL-078 | rendering-core | NO (0 hits in `inventory/rendering-core.md`; C-CL-060 only in block-editing) |

These 7 rows are therefore orphaned: they leave myst, but no inventory owns them. Fix: either have the target critics/authors cite
them (preferred, the move reasons are sound), or keep them in myst with a note.

## Missing behaviours

Nothing of substance; the inventory is unusually complete (73 rows, error paths, Restricted Mode, CRLF, stale gate, timeouts all present).
Optional additions to Notes:
- `normalizeAnchors`: several consecutive `(a)=` `(b)=` targets before one block each get their own anchor icon (loop over `mystTarget` run); not stated in F-MYST-033.
- `warningBannerState` counts every `myst-extension` line (`count: warnings.length`) but the key is built from the unique messages: two lines with the same message show "2 warnings" yet one key (F-MYST-068/071).
- Label rename success: the field stays disabled and auto-closes after 5 s (noted in findings, not in F-MYST-039/040 row text).

## Wrong/unverifiable evidence

Scripted check of 206 `file` / `file:symbol` citations: every file exists; all plain symbols found; the 5 dotted member refs
(`SourceEditController.handleLabelRename`, `PAGE_TO_HOST_VALIDATORS.previewLabelRename`, `DiagnosticsController.publish`,
`PAGE_MESSAGE_GATES.previewShowProblems`, `ADMONITION_DIRECTIVE.style`, `FIGURE_DIRECTIVE.style`) exist as members.
Test-name check of 141 cited `test(...)` titles: 140 found verbatim; the 1 miss ("detects colon_fence") is a table-driven test
(`detects ${name}` in `mystSyntaxDetect.test.ts:28`, case present at line 13): acceptable. Visual ids `myst/v01`..`v33` all exist in
`test/visual/*.ts` and in the checklist. Coverage states spot-checked (F-MYST-018 untested, F-MYST-044 untested, F-MYST-064 untested,
F-MYST-031 and F-MYST-066 no unit test) agree with the sources; the `{ref}` to a plain label becoming `#name` (F-MYST-017) and the
line clamp in diagnostics (F-MYST-066) match the code. No false evidence found.

## Count check

Counts table: 73 behaviours = 73 `F-MYST` rows; 70 tested + 3 untested (F-MYST-018, 044, 064) = 73 matches the Cov. column
(tested variants 70, `untested` 3). Undocumented 19 matches the 19 rows whose Notes say "undocumented" (list identical).
Checklist "57 / 57 (61 rows, 12 moved out, 8 moved in)": 61 - 12 + 8 = 57, consistent, but see Missing rows (7 of the 12 moved-out rows are not owned by their target yet).

## Verdict

REVISE only for the 7 orphaned moved-out rows: C-AR-001, C-AR-008 (block-editing), C-AR-019, C-AR-030 (layout-width),
C-CL-060, C-CL-070, C-CL-078 (rendering-core). Add them to the target inventories (or keep them in myst); everything else is sound.

Verdict: REVISE

## Re-check

(1) The 7 orphaned moved-out rows (C-AR-001, C-AR-008, C-AR-019, C-AR-030, C-CL-060, C-CL-070, C-CL-078) are now each cited in an `| F-` line of block-editing, layout-width and rendering-core; C-AR-049, C-AR-084, C-AR-092 and C-CL-044 too; C-AR-118 is listed as n/a: process.
(2) All 61 checklist ids with scope `myst`/`myst?` are cited in an F-MYST row or listed in Checklist corrections (0 uncovered).
(3) 8 spot-checked claims hold (enabledMystExtensions, inlineDollarLine, renameLabelLine and countRefUses, warningBannerState, initializeContent, 3 test titles, visual id v29, the "MyST extension check" pass).
(4) Counts match the F-rows: 73 rows = 70 tested (2+62+6 variants) + 3 untested; 19 undocumented, identical to the listed ids.

Re-check verdict: APPROVE
