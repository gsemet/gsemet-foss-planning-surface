Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.1 critic review: gfm inventory

Scope `gfm`, reviewed against `inventory/gfm.md`, the checklists (scope column) and the five mapped
source files at `markdown-okf-schema-studio-wt-059`.

## Missing rows

None. Scripted: 16 checklist rows have scope `gfm` (C-CL-043/048/050/056/066/069, C-MSG-031/037,
C-AR-013/028/037/045, C-VIS-126/246/247/248); all 16 are cited in the inventory (11 kept, 5 in
"Checklist corrections"). Moved-row handling: C-CL-056 and C-AR-013 are cited by
`inventory/rendering-core.md` (F-CORE-024, line 105); C-AR-011 (rendering-core?) is cited there as
moved to gfm and kept in gfm. Minor: C-CL-048/050/069 are "n/a: release process" and no other
inventory cites them (acceptable as n/a, but make sure the SwRS column gets that n/a). C-AR-037
(part) is said to go to palette-slash, but `inventory/palette-slash.md` does not cite it yet; gfm still
cites it, so it is handled.

## Missing behaviours

Nothing of substance. Small gaps (optional additions to Notes):
- `GITHUB_BOLD_ALERT_MARKER` is case-insensitive (`> **note**`) and takes no title; F-GFM-011 only
  lists the capitalised form.
- `isSafeOkfColor` accepts comma-separated `rgb()` only (space syntax `rgb(0 0 0)` refused), at most
  3 integer / 3 decimal digits per channel, and trims whitespace; F-GFM-034 does not state the
  comma-only rule.
- `toggleCheckbox` also drops (preventDefault) a click when the line/column attributes are missing or
  invalid; only the busy case is listed (F-GFM-023).
- `applySpanColors` only touches elements under `#sphinx-myst-preview-content`.

## Wrong/unverifiable evidence

Spot-checked 70+ claims by grep: all 33 cited test names (bareUrlAutolink, mystFeatures,
mystPaletteRendering, checkboxMarkers, checkboxRendering, crlfAlerts, runtimePageControls,
runtimeContentPatch, core/edits/sourceEdits, both spanColors tests) exist; all cited symbols exist
(autolinkBareUrls, trimBareUrl, markTaskList, convertCheckboxPlaceholders, INERT_CHECKBOX_PARENTS,
collectTableAlignments, normalizeRawHtmlTable, RAW_DETAILS_HEAD, rawColourSpan, handleCheckboxToggle,
postCheckboxResult, planCheckboxToggle, CHECKBOX_GONE, EDIT_REQUEST_TYPES, sanitizeTableStyle,
blocked-event-attribute, ...); visual ids gfm/v01-v04, gfm/r01..r04 and fixtures `21-bare-urls`,
`37-gfm-gallery` exist; `pageStateMessages.test.ts` holds one valid toggle sample (coverage
"untested" for F-GFM-027 is right). Source behaviours match (alert regexes, fence handling, lone
`aria-busy`, tooltip-only reason, "Editing requires a trusted workspace.").
Weak points (not false):
- F-GFM-033 evidence is "myst-to-html" with no test name, yet marked "tested (unit, indirectly)";
  name a test or mark it untested.
- Counts "Undocumented" lists F-GFM-012, 026, 032, but their Notes do not use the word
  "undocumented" (only 9 rows do); align wording.

## Count check

37 rows (F-GFM-001..037) = 37 behaviours; 35 tested + 2 untested = 37; 0 doc-only. Undocumented list
has 12 ids, matching the count (see wording remark above). Checklist 11 + 5 = 16 matches the 16
scripted rows; "12 listed ids = 11 own + 1 incoming" is correct.

## Verdict

Verdict: APPROVE
