Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.1 critic review: diagrams (DIAG)

## Missing rows

None. Scripted: 30 checklist rows carry scope `diagrams` (`diagrams?` included); all 30 are cited in
`inventory/diagrams.md`. The rows the inventory leaves with another scope were checked in the target
inventory: C-AR-038 (table-editing.md), C-CL-025 (palette-slash.md), C-VIS-019/020 (myst.md),
C-AR-141 (review-annotations.md), C-CL-082/083, C-AR-138/139 (trust-security.md), C-PKG-032
(lifecycle-sync.md) are all cited there.

## Missing behaviours

Minor only (below the 3-behaviour threshold):
- `plantumlDiagram.ts` (~line 370): a built-in PlantUML diagram with empty source is skipped and left
  blank, like the Mermaid case noted in F-DIAG-001; not listed for PlantUML.
- `plantUml.ts:apply`: no-op when the injected HTML equals the current page and there are no
  diagnostics; also the fallback to a full `setPanelHtml` when incremental updates are off or the
  status lines do not fit a patch. F-DIAG-050 states only the in-place path.
- The Mermaid `initialize` only when theme variables changed (`initializedTheme`) is implicit in
  F-DIAG-007 but not stated.

## Wrong/unverifiable evidence

Spot-checked 50+ symbols and test names by grep in the worktree (renderer, normalize, mermaid and
plantuml page modules, controller, hostEvents, settingsRegistry, test titles in mystFeatures,
mermaidCache, mermaidError, contentPatch, editActions, plantumlDiagram, plantUmlRenderer,
plantUmlFile, plantUmlIncludes, package-contract, rendererBridge, pageToHost). All exist, and the
coverage states (F-DIAG-009, 019, 031, 042, 045, 049, 052, 055 untested) match: no test names them.
One location slip: `check_mermaid_error_theme_switch` (F-DIAG-011) is defined in
`test/visual/capture_final_checks.py`, not `capture_support.py` (fix the file name if it is given
that way in the row).

## Count check

Table has 55 F-DIAG ids (001..055, all unique). Counts row: 55 = 45 tested + 10 untested; the
untested list (009, 014, 019, 021, 031, 042, 045, 049, 052, 055) has 10 entries and matches the
rows marked untested. Undocumented list has 13 ids. Checklist 30/30 plus 5 claimed: consistent.

## Verdict

No uncited rows, no false evidence, fewer than 3 substantive missing behaviours.

Verdict: APPROVE
