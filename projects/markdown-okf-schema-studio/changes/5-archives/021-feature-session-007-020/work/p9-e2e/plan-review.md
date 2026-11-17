# P9 plan review (critical, read-only on src/test/images)

Reviewer: Sonnet 5.5, 2026-10-22. Inputs: post-plan.md P9/P10, findings, plan, migration, STATE,
inventory, `test/visual/scenarios.ts`, `capture.py`, `renderFixtures.ts`, `themes.ts`,
`test/integration/*`, `test/site/*`, `scripts/generate-readme-images.py`, `out/reports/`.
Method for the safety audit: a scratch script (outside the repo) compared every D/M scenario to the
survivors on (fixture, theme, preview theme, width, scroll, flags) and on each flag value.

## Verdict: GO WITH CHANGES

The analysis (findings, groups, inventory) is solid and the direction is right. But as written the
plan (a) deletes 43 scenarios whose checks have no equal elsewhere, (b) would silently disable one
check on rename, (c) has a batch gate (B1) that fails by itself, (d) cannot verify README images
until the last batch, and (e) schedules gap-fill scenarios whose harness plumbing does not exist.
All of it is fixable inside the plan; the required changes below are already applied to `plan.md`
(new section 0 plus rewritten sections 2-7), `migration.md`, `STATE.md` and the generator
(`tools/overrides.mjs`, `tools/build_inventory.mjs`; `inventory.md`/`migration.md` regenerated).

## Required changes (R) and where they were applied

### R1. Deleting a scenario deletes its assertions: delete only exact aliases (plan 0.1, overrides)

`capture.py` runs, per scenario, the page checks (scroll independent), the flag checks and
`check_final_frame` at the final scroll (bottom padding, named landmark visible, sticky band vs
toolbar). A "D" scenario therefore loses more than a screenshot. The audit found:

- Flags with NO surviving owner: `editTarget="title"` + `topSpacingChecks="first-block"`
  (`edit-first-block-top-wide/-narrow`), `topSpacingChecks="empty-start"`
  (`edit-empty-document-start-writing`), `hideDescriptionColumn` (`okf-schema-narrow`, planned as
  M but the merge needs new code in another scenario). "Superseded by `firstElementGap`" holds
  for the 40 px gap and the toolbar overlap, not for the title-editor path (`check_preview_edit_mode`
  title branch) nor the "exactly one visible" test.
- Final-frame checks with no equal: `handbook-dark-bottom` (bottom padding on the handbook),
  `handbook-light-failures`, `admonitions-dark-titled/-nested`, `chapter-dark-quarter/
  -three-quarters` (landmark selectors that must exist and land in the viewport).
- Width/mode/theme combinations that vanish: `toc-column-dark-1600` and `-auto` (the 1600 px
  Margin/Auto TOC geometry exists nowhere else), `nested-list-typing-light` (900 px; the kept one
  is 460), `edit-paragraph-forced-cream` (cream + 08-okf-schema), toolbar white 900/360 (forced
  white on the toolbar fixture; the plan relied on real-window checks, which are skipped on a
  locked screen), `width-modes-dark/cream`, `diff-*-edit` (edit mode over code fences: the plan
  asked for a NEW toggle check, i.e. new test code to review), `frontmatter-scroll-feedback-edit`.
- Safe to remove: only the 4 exact aliases `syntax-light-shell`, `preview-toolbar-dark`,
  `edit-mode-dark`, `edit-table-cell-dark` (identical fixture, theme, width, scroll, flags).

Change: every other former D (39) and M (4) row becomes **A** (scenario kept, `capture: false`,
screenshot gone, all checks kept). Result: 245 -> 241 scenarios (137 with PNG, 104 assertion-only),
PNG count unchanged (167 after B2). Runtime does not grow versus today. Pruning assertion-only
scenarios is explicitly out of P9. Applied: plan 0.1, B2a/B2b, section 7; `tools/overrides.mjs`
(43 rows, slugs chosen); `migration.md`/`inventory.md` regenerated (K 137 / A 104 / M 4).
Dropped step PNGs are safe because the step name stays in a `STEP_NAMES` registry and the check
that wrote it still runs (plan section 3, `steps` semantics: skip silently, fail on an unknown name).

Real-window "A" rows (15) are fine: the assertion and note stay, only the PNG goes (T1.2). Their
registry flag `capture: false` must exempt them from "registered but not captured" (applied).

### R2. An id-keyed check dies on rename (plan 0.3, B1.2)

`check_mermaid_theme_switch` starts with `if scenario["id"] != "mermaid-map-dark": return`.
After the rename (`diagrams/v01-mermaid-map-dark-900`) it returns silently: no failure, no check.
Change: B1 replaces it with a `mermaidThemeSwitch` flag before any rename and greps for other id
literals (the audit found no other one in capture.py, renderFixtures, test/site, scripts).

### R3. B1 cannot pass its own duplicate gate (plan B1.4)

B1 adds a hash check over ALL PNGs but only fixes H2-H4. Four step PNGs remain byte copies of
primaries and are not covered by those fixes: `palette-mode-myst-light/dark-palette`
(= `edit-palette-light/dark`) and `slash-menu-strict/myst-light-open` (= primaries). The 76-step
target needs them dropped in B1 (via `steps`). Applied.

### R4. README images cannot be verified until the last batch (plan 5, B0, B2a, T1, F)

`gallery:generate` runs curateGallery, which requires a passing full `test:e2e` (`review.json`
passed and the real-input run identity), so README sources are untested per batch; the crops are
pixel boxes tuned to the current PNG geometry. Change: B0 baseline snapshot of the 15 sources and
15 outputs; `generate-readme-images.py --check` (visual sources, temp dir, pixel compare) required
in B2a/B3, real-window ones in T1; `readme` flag becomes a locked invariant (unit test: not
assertion-only, crop present); crops copied verbatim; `images/` committed only for intended
changes; `images/gallery.json` timestamp noise discarded. README.md untouched (verified: all 14
`images/...` links keep their paths; `images/01-paragraph-blur-commit.png` is curated but
unreferenced, keep).

### R5. Harness plumbing for `/` in ids and for partial runs (plan section 2)

- Ids with `/`: only the main screenshot path is covered by "capture.py creates parent folders";
  steps, sidecars, `first-gap/<id>.json`, width-margin reports, TOC reports and the stale-file
  cleanup (`glob("*.png")` is flat) also need it, plus a one-time purge of the legacy flat files
  or `buildSite.ts` (which lists every nested PNG) would show old and new side by side.
- Fixed locations: the plan and migration.md disagreed (`screenshots/visual/<group>` vs
  `screenshots/<group>`). Now `visual/<group>/` for PNG/JSON; `run-manifest.json`, `INDEX.md`,
  `MACHINE-CHECKS.md` stay at `screenshots/` (review-index.ts reads them there).
- A partial run (`--scenario`) rewrites `run-manifest.json` with a subset today (root cause of H9);
  a gallery built from it would list one scenario. Partial runs now write
  `run-manifest.partial.json`.

### R6. B2 is too big for one reviewable commit: split (plan 6)

B2 mixed rename, move, deletion, merge with new check code, step pruning, content fixes, 198
`locks` lines and README-generator edits. Now: B2a pure rename/move (PNGs byte-identical to the
B0 baseline, ids edited in place in `scenarios.ts` without reordering, so `git blame`/diff stay
readable), B2b assertion-only conversion + step pruning + three small content fixes, B2c `locks`
text plus invariants unit test (parallelisable per group). Each is one revertible commit.
Rename churn is a non-issue for git history because PNGs live in git-ignored `out/`; the churn is
the id strings in `scenarios.ts`, kept as in-place edits.

### R7. Gap-fill batches (B4/B5) rely on harness features that do not exist (plan B4, B5)

`renderFixtures.ts` hard-codes `trusted: true`, `strictAdditionalProperties: false`,
`renderPreviewToolbar()` (editing on), always renders the properties table, caches pages by
fixture/theme/sticky/plantuml only, and the mock `postMessage` handles only `previewEditOpen`.
So read-only, strict-field warning, `propertiesTable=false`, `maxContentWidth`, zoom clicks,
incoming-change bars and review threads all need new per-scenario options and a wider cache key
(otherwise a new scenario silently reuses an old page). Change: harness commit first, with a
"existing 241 scenarios render byte-identical HTML" check; B5 split in two commits.
Also: the B4/B5 tables hard-coded ids that now collide with real numbers (`layout-width/v19`,
`block-editing/v14`, `palette-slash/v15`, `theme-zoom/v07`, `myst/v15..v17`...). Replaced by
"next free number in the group" (current values listed); numbers are permanent after B2a.
High-contrast: `src/` has no high-contrast handling at all, so invented HC variables assert
nothing real. Now exploratory (human review, `knownIssue` when unreadable). The conf.py warning
and the huge document are flagged as possibly host-only / generated. New rule (0.4): a failing
gap-fill scenario is a product defect, not a P9 fix (`knownIssue`, followups).

### R8. Real-window batches need an unlocked screen and keep their contracts (plan T1, T2, gates)

T1/T2 touch the keyboard suites (realInput, checkboxToggle) that are skipped on a locked screen,
so TL/FL cannot close them. Changes: gate T = unlocked screen only (otherwise "pending-unlock",
batch not ticked); T1 ported one suite per sub-commit; the five LATEST pointer files, their link
text, `INDEX.md`, the manifest fields read by curateGallery/`reviewEvidence`/generate-readme-images
and the run-folder prefixes (`real-input-`, `scroll-e2e-`, `frontmatter-e2e-`) stay unchanged;
`clip: "preview"` has a full-window fallback and README/workbench shots keep `clip: "window"`;
"registered id missing" only fails when the suite ran completely (not `--scroll-only`).
T2 items are spikes, abandonable without blocking F: the untrusted runner spawns Code directly with
no debug port (needs `--remote-debugging-port` + env); `standalone-suite.js` is not in the CDP
suite list; the incoming-changes positive test needs git discovery of a temp repo (use the
fixtures folder, clean in `finally`; it is not git-ignored).

### R9. Naming collision "gallery" and tracked artefacts for P10 (plan 4, 0.6, section 3)

`npm run gallery:generate` already means "curate README images" and rewrites tracked `images/`;
`test/site/buildSite.ts` is another gallery. The PO gallery is now always "PO gallery" /
`review:gallery`, written as a compiled, unit-testable `test/site/poGallery.ts` (the plan's plain
`.mjs` under `scripts/` could not be covered by `test:unit`), and `gallery:generate` is a gate only
in F. `.agents/changes/` is git-ignored: the group list, `locks` and the integration-test-to-group
map (26 files, currently only in `inventory.md`) now live in a tracked module
`test/shared/e2eGroups.ts`, otherwise P10 would start from an untracked base.

## Recommendations (not applied; decide before B1 because group ids are frozen after P9)

1. **Split `frontmatter-schema`** (decide now): it would hold 18+ visual + 43 real captures plus
   previewEditing/genericMarkdown. Suggest `frontmatter-schema` (table, validation, links, generic
   YAML) and `frontmatter-editing` (field edit, add/remove/rename, title, boolean, list, picker).
   It costs one `GROUPS` row and moving real rows r01-r17 and visual v03-v06 in `decisions.mjs`.
   Similar but milder: `block-editing` (23 real + 13 visual: selection, move, clipboard, undo) and
   `lifecycle-sync` (scroll sync vs reload/restore vs status pages). With 16-17 scopes, P10
   scope sizes stay even. If you keep 15, accept very large scopes for P10.
2. `rendering-core` scope text mentioned "admonition colours", but the admonition captures sit in
   `myst`; the scope text is fixed (applied). Keep admonitions in `myst` or move `admonitions-*`
   to `rendering-core`: pick one before B1.
3. After P9, a separate optional batch can prune assertion-only scenarios, but only with proof
   (mutation-style: temporarily break the product behaviour and see another scenario fail).
4. Stale evidence: 739 run folders / 2.2 GB. Pruning (H8) is safe only if it never deletes a
   folder named by a LATEST pointer or by the current campaign's manifest (applied in B3).
5. `locks` quality is the P10 raw material: have a Sonnet critic review B2c per group
   ("observable, one behaviour, no test technique, no theme/width unless it is the point").
6. Orphan-box fix: the check deletes the box and asserts the height is restored; keep a box for
   the capture by re-adding it after all asserts (applied in B2b), not by dropping the assertion.
7. TOC fixture change (`30-toc.md` wide table) alters every TOC scenario; list them and keep
   `tocChecks` unchanged (applied in B2b). The new PNGs are new baselines; none is a README source.

## Ambiguities an implementer would have tripped on (all resolved in plan.md)

- Where the PNGs live (`visual/<group>/` vs `<group>/`), and where the manifests stay.
- What `save_step` "refuses": now skip-if-not-listed, fail-if-unknown.
- Whether numbers can change after B2 (no), and whether new scenarios renumber (no, append).
- What `capture: false` still does (all checks, final frame, reports; no PNG/sidecar).
- Which "gallery" command is meant, and that `gallery:generate` rewrites tracked files.
- That "the TL/FL gate" is not enough for T1/T2.
- B1 "old ids unchanged" while the duplicate gate runs (R3).
- That the migration table in plan.md was a stale copy: removed, `migration.md` is authoritative.

## Checked and fine

- Counts: 245 = 137 K + 61 A + 39 D + 8 M; B4 +15 / 14 PNGs and B5 +21 / 18 PNGs add up.
- The 15 README sources all survive as K (theme-dark, forced white/cream, slash-menu-gfm-light,
  edit-frontmatter-value-dark, okf-schema-dark, toolbar cream x2, readme-margin-break-cream).
- `renderFixtures` page names do not use the scenario id, so `/` in ids only affects capture.py
  writers. `review-index.ts` and `reviewEvidence` need the `visual.duplicateImages` empty (kept).
- `first-element-gap` A rows (51) keep running the 40 +/- 4 px measurement; only the pictures go.
- Group assignment is mostly sensible; trust-security is empty today and gets T2/B5 content.

## Edits made (all inside p9-e2e/)

1. `plan.md`: new section 0 (safety rules); section 2 locations, `/` handling, partial manifest;
   section 3 `steps`/`STEP_NAMES`, `capture`, `group` (tracked `e2eGroups`), `knownIssue`,
   `mermaidThemeSwitch`; section 4 gallery naming/generator; section 5 rewritten (README safety);
   section 6 rewritten (B0, B1, B2a/b/c, B3, T1, B4, B5, T2, F); section 7 counts (241/256/277);
   section 8 embedded migration copy replaced by a pointer.
2. `migration.md`, `inventory.md`: regenerated (43 rows D/M -> A; 4 alias M kept).
3. `tools/overrides.mjs` (new) and `tools/build_inventory.mjs` (import + header text).
4. `STATE.md`: batch list updated (B0, B1, B2a/b/c, ...).
5. Not touched: `findings.md`, `tools/decisions.mjs` (kept as the original audit; overrides win).
