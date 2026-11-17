Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Review: layout-width inventory (P10.1 critic)

## Missing rows

None. All 94 checklist ids whose scope column is `layout-width` (1 C-PKG, 1 C-TB, 5 C-CL, 2 C-AR,
85 C-VIS) are cited in `inventory/layout-width.md`. C-CL-037 is listed as moved to
toolbar-navigation and `inventory/toolbar-navigation.md` (F-TOOLBAR-018 area) cites it: handled.
C-CL-098 is cited here (F-LAYOUT-014) and in table-editing / palette-slash.

## Missing behaviours

None of substance (fewer than 3). Minor, optional notes:
- `contentLayoutStyles.ts` resets Shibuya containers (`.sy-page`, `.sy-container`, `article` ...
  to block, no max-width): not listed. Rendering-level, no user-visible rule beyond F-LAYOUT-002.
- Column bottom padding (`min(80vh, ...)`, end of document reachable) is in F-CORE-030
  (rendering-core), not here; acceptable cross-scope.
- `firstClearance.ts` settle caps (60 quiet frames, 300 max) and the `describe()` diagnostics
  object are only implied by F-LAYOUT-015 ("until quiet"); tooling-level.
- `widthMode.ts` leaves a code block (`pre`) uncentred when narrow and also treats an element
  containing a `textarea` as under edit: covered by F-LAYOUT-022 / 024 in substance.

## Wrong/unverifiable evidence

Spot-checked 20+ claims, all hold: the three mapped source files and six test hosts exist;
symbols `normalizePreviewContentWidth`, `MAX_PREVIEW_CONTENT_WIDTH` (2400), default 960 (rounding,
negative falls back, clamp as stated), `markWideTables` / `data-sphinx-short-cell`, `viewWidthMode`,
`check_first_element_gap`, `check_top_spacing`, `check_width_modes`, `check_width_mode_break`,
`NO_HORIZONTAL_SCROLL`, `MAX_WIDTH_ASSERTIONS`, `layout-width/v84...`, `v85...`; test names
T10 (width button cycles; only elements wider than the column flagged), T10b (TOC open; fractional
width rounded up; paragraph holding only an image is a figure), P7 full-width gutter, K1, P4
toolbar bottom, burst of skipped updates, "nothing is pushed when the toolbar is beside the
column", `identifier-split passes`, geometry-checks definition test. Package.json step 50 and
min/max match. Coverage states (F-LAYOUT-004 untested; 022/025 partial) are plausible.

## Count check

Table has 28 rows; Counts say 28 = 27 tested + 1 untested (F-LAYOUT-004): matches the Cov column.
Undocumented 6 (001, 004, 015, 022, 025, 028): matches the list. Checklist rows 93 cited + 1 moved
= 94 (1+1+4+2+85 = 93; the 5th C-CL is C-CL-037, moved): matches the extracted ids.

## Verdict

No uncited rows, no substantive missing behaviours, no false evidence.

Verdict: APPROVE
