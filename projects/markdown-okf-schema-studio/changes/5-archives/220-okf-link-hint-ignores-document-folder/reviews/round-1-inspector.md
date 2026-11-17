# CR 220 — Inspector review, round 1

Worktree: markdown-okf-schema-studio-wt-220 (uncommitted changes over 0b4ede78).

## Verdict: APPROVE

No blocking findings. The fix matches the approved behaviour note (choices 1–5).

## What was checked

- **Known = table index.** `filenameStemSuggestions` (src/core/frontmatter/fileLinks.ts:166-173)
  uses `getCachedMarkdownStemIndex(resolveFrontmatterLinkRoots(options).filenameRoots)`, the same
  roots and cache as `resolveFilenameStem` (fileLinks.ts:244). `analyzeFrontmatter` passes the same
  `linkInspectionOptions` to both and computes the stems after link inspection, so a stale-index
  rebuild done by the table is the index the editor gets. No `stemIndex` injection on this path.
- **Distance and dedupe** (src/core/frontmatter/stemIndex.ts:35-39, 77-87). Roots and the document
  folder both go through `canonicalRoot` (realpath), so macOS `/var` vs `/private/var` and symlinked
  roots agree (the test runs in `os.tmpdir()` and passes). Up and down steps count alike (`..` = 1,
  child = 1). Other drive on Windows: `path.relative` returns an absolute path → `MAX_SAFE_INTEGER`,
  sorted last; `path.sep` split is platform-correct. Several roots, bundle root inside a workspace
  root (same file indexed twice): `Math.min` over candidates, one entry per Map key, so no duplicate.
  Document at a workspace root: its folder is the root, distance 0 for root files. Symlinked
  sub-folders are not traversed by the index (pre-existing), so no mismatch there.
- **Cost.** No extra file-system walk: one `realpathSync` for the document folder, then O(n) `path.relative`
  plus one O(n log n) sort; `stems()` one sort. Computed once per analysis (`stems ??=`).
- **Escaping.** `escapeHtml(JSON.stringify(...))` like the existing attribute; the page reads it with
  `getAttribute` + `JSON.parse`. The new propertiesTable test covers a `"` in a stem.
- **Editor fallback** (src/page/features/frontmatterListEditor.ts:60-81). Missing/invalid
  suggestions → no datalist, no warning (unchanged). Missing/invalid known → falls back to the
  suggestions (old behaviour). Known ∪ suggestions, so a truncated or partial known set cannot add
  false warnings.
- **Tests fail before the fix.** before-tests.txt shows the 3 new tests failing on the old code
  (0 !== 606; alphabetical vs nearest order; `aria-invalid` 'true' !== null). Reasoned check agrees:
  old `filenameStemSuggestions` returned an alphabetical array and set no `linkKnownStems`; old
  editor ignored `data-okf-link-known`. Expected values recomputed by hand (6 near stems + a-000…a-493
  = 500). No existing assertion changed; only `openListEditor` gained an optional parameter and the
  e2eGroups count went 410 → 412 with its reason appended.
- **Requirements.** Only SwRS-MDOKFSTUDIO-FMEDIT-010 touched, `req_lifecycle: proposed`. Statement,
  new scenarios and verification notes match the code. `implemented_in_files` / `tested_in_files`
  match the `@implements_req` / `@tests_req` markers. No stale "500 alphabetical" text elsewhere.
- **Gates.** `rtk proxy just check`: exit 0, unit 3324/3324, security 71/71, check-markers,
  requirements-lint and coverage clean (W2 broken cross-link warnings are pre-existing).
  `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
  1072 requirements, 0 errors, 21 warnings (pre-existing). The four T220 tests pass.
- **Screenshots** (/private/tmp/claude-502/cr220-driver/shots/). Before (cream, dark): the full
  warning 'No Markdown file named "gen-related-target.md" was found. It will be saved as typed.' under
  the item. After (cream, dark): no warning, the item not marked invalid. Same viewport, scroll and
  edit state; the collapsed toolbar sits top right, clear of the editor and status line. The table
  layout differs slightly (the long warning widens the Value column and shifts the heading by about
  18 px in the before shot); that comes from the warning itself, not a different framing.

## Findings

1. **Non-blocking — redundant payload when the workspace holds at most 500 stems.**
   src/core/frontmatter/propertiesTable.ts:252-255. When `linkKnownStems.length <= 500`, the known set
   equals the suggestions (same stems, other order) and the second attribute doubles the row's HTML.
   In large vaults the uncapped attribute is repeated on every filename-stem field row and on every
   re-render (for 20k files, about 0.6 MB per row). Expected fix: set `linkKnownStems` (or emit
   `data-okf-link-known`) only when `known.length > suggestions.length`; the editor already falls back
   to the suggestions. Optional follow-up for very large vaults: the "list incomplete" flag from the
   behaviour note, choice 1.
2. **Non-blocking — `nearestStems(Infinity)` returns nothing while `stems(Infinity)` returns all.**
   src/core/frontmatter/stemIndex.ts:78 vs :67. Not reachable today (the caller passes 500), but the
   two methods of the same class read a non-finite limit in opposite ways. Expected fix: use the same
   rule as `stems()` (`limit > 0 ? size : 0` for a non-finite limit).
3. **Non-blocking — the fallback for a missing or invalid `data-okf-link-known` has no test.**
   src/page/features/frontmatterListEditor.ts:71. The existing T22 tests cover it implicitly (they set
   no known attribute), but an invalid JSON value (`"not json"`) is not exercised. Expected fix:
   optional one-line case in the T220 page test: an invalid known attribute still warns on a stem
   outside the suggestions and does not throw.
4. **Non-blocking (note only) — the known set is the index's raw stems.** fileLinks.ts:171. A stem
   whose only file is a broken symlink or a symlink escaping its root is "known" to the editor while
   the table reports E10/W15. This follows the approved "same index" choice and was already true of
   the suggestions; no change expected in this CR. It could become a FMEDIT-010 known issue if the
   owner wants it written down.
