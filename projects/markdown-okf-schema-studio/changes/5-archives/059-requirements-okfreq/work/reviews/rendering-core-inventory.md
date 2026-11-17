Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: rendering-core inventory

## Missing rows

Scripted (parse of `checklists/*.md`, scope column starts with `rendering-core`): 66 rows
(25 plain, 41 guessed `rendering-core?`). The inventory header counts 53. 23 rows are cited nowhere
in `inventory/rendering-core.md` and are absent from "Checklist corrections":

- 19 guessed archive rows, none confirmed or moved: C-AR-112, 116, 117, 119, 120, 121, 122, 124,
  125, 126, 130, 131, 132, 133, 136, 137, 143, 146, 148 (CI/process notes, "See PR" rows, coder
  report pointers, orchestration rules). Each needs a decision (n/a: process, or moved) in the
  corrections table; no other existing inventory cites them either.
- 4 visual rows of scope `rendering-core`: C-VIS-273 (v21 long words 900), C-VIS-274 (v22 long
  words 460), C-VIS-318 (v23 inline image in text), C-VIS-319 (v24 inline image edit dark).
  F-CORE-033/035 (long words/URL) and F-CORE-007/inline image should cite them. C-VIS-318 is
  cited only by `inventory/trust-security.md`, which does not make it handled here.

Moved rows not cited by the target scope inventory (grep of the id in the target file):
C-CL-068 (trust-security), C-AR-002 and C-AR-051 (block-editing), C-AR-015 (trust-security).
The other moved rows (AR-011, 065, 072, 089, 090, 095, 099, 101, CTL-021/026..039) are cited by
their target.

## Missing behaviours

Mapped files with no row at all (grep of the keywords in the inventory returns 0):

- `src/core/render/mystTables.ts`: raw HTML tables rebuilt from a tag/attribute allow-list
  (`SAFE_HTML_TABLE_TAGS`, `BLOCKED_HTML_TABLE_TAGS`, `normalizeRawHtmlTable`); `{list-table}`
  `:header-rows:` re-laid into thead/th, `:widths:` as colgroup, directive table alignment
  (`applyTableAlignments`), and list-table cells carrying no source line so a click edits the
  whole table. Tested in `mystFeatures.test.ts` / `test/page/modules/listTable.test.ts`.
- `src/core/render/mystBlockTransforms.ts`: figure captions and captionless `{numref}`/`{ref}`
  targets (`normalizeFigureCaptions`, `normalizeCaptionlessReferences`), `versionadded`/
  `versionchanged`/`deprecated` admonition titles (`expandVersionAdmonitions`), and raw
  `<details>`/`<summary>` and `<kbd>` conversion (`normalizeRawDetailsAndKbd`); F-CORE-037
  only mentions `<details>`/`<kbd>` as "supported subset".
- `src/core/render/mystNormalize.ts`: figure/image size and alignment (`normalizeImageSize`,
  `data-okf-width`, `FIGURE_ALIGNMENTS`).
- `src/core/render/renderPipeline.ts`: per-file MyST extension gating
  (`enabledMystExtensions`, diagnostic code `myst-extension`), and resource-policy diagnostics
  surfaced as `warning` items (only partly in F-CORE-007).
- Minor: `MAX_INCLUDE_DEPTH = 8` (nesting limit, F-CORE-010 says "nested" only); `preloadMystEngine`
  swallows an import failure (F-CORE-020).

## Wrong/unverifiable evidence

Scripted check of all 106 `file`/`file:symbol` references in the Evidence column against the
worktree (file exists, symbol text present) and of all 19 `:test name` follow-ups (name present in
the named test file): all found. `RenderingController.updatePreview` (F-CORE-017) exists as a
class method. Spot-checked by hand F-CORE-001..012, 014, 017, 048, 049: symbols, test names and
coverage states are right. Doc-only/untested states look right (F-CORE-014, 020, 023, 038 have no
test). No false evidence found.

## Count check

The table has 49 F-CORE rows, matching "49". Tested 44 / Untested 4 / Doc-only 1 matches the Cov.
column. "Undocumented 15" does not match: the Undocumented list in the text names 14 ids
(F-CORE-004, 005, 007, 008, 009, 014, 016, 017, 020, 030, 033, 036, 037, 038) and the table
Notes mark 14 rows `undocumented` (it carries F-CORE-049 and not F-CORE-014). Reconcile. The
"27 cited + 26 moved / 53" row total must be redone after fixing the missing rows (66 scripted).

## Verdict

Fixes needed:
1. Add the 23 uncited rows (19 C-AR guessed rows to corrections as n/a or moved; C-VIS-273, 274,
   318, 319 cited by F-CORE-033/035/007 or a new row).
2. Make C-CL-068, C-AR-002, C-AR-051, C-AR-015 cited in their target inventories (or keep them here).
3. Add rows for mystTables (HTML table allow-list, list-table header rows/widths/alignment),
   figure captions/captionless refs, version admonitions, `<details>`/`<kbd>`, image size/align,
   MyST extension gating and resource warnings.
4. Fix the Undocumented count (14 vs 15) and the checklist total in Counts.

Verdict: REVISE

## Re-check

- Fixes 1, 3, 4 done: scripted parse gives 66 rows of the scope, 36 cited in `| F-` lines and 30 in
  Checklist corrections (0 missing); the new rows (F-CORE-050..058) cover mystTables, figure
  captions, version admonitions, details/kbd, image size, extension gating, include depth;
  C-VIS-273/274/318/319 are cited. Counts table matches: 58 rows, Tested 53 / Untested 4 /
  Doc-only 1, Undocumented 17 (the 17 `undocumented` Notes equal the listed ids).
- Spot-check of 12 evidence claims by grep (SAFE_HTML_TABLE_TAGS, applyTableAlignments,
  normalizeFigureCaptions, expandVersionAdmonitions, normalizeImageSize, FIGURE_ALIGNMENTS,
  MAX_EXTENSION_WARNING, isPageToHostMessage, MAX_GLOB_MATCHES, MAX_INCLUDE_DEPTH, the figure test
  name, the inline-image CSS selector): all present.
- Remaining gap (fix 2): C-AR-124 is listed as "moved to block-editing, target does not cite it
  yet", but `inventory/block-editing.md` has no mention; it is cited in F-PALETTE-012
  (`inventory/palette-slash.md`). Change the corrections row to palette-slash. All other moved ids
  (27) are cited by their target inventory.

Re-check verdict: REVISE

Orchestrator note: the re-check found two small defects (C-AR-124 target, palette Counts); both fixed by the orchestrator after the re-check. Re-check verdict: APPROVE (fixed)
