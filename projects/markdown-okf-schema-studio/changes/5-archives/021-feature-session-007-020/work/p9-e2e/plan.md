# P9 e2e campaign — target organisation and work plan

Inputs: `findings.md` (defects, duplicates, gaps), `inventory.md` (every capture, generated),
`migration.md` (old id → new id, generated, authoritative; regenerate after any change to
`tools/decisions.mjs` / `tools/overrides.mjs`). `plan-review.md` lists the review changes. Requirements are NOT
written in P9: each scenario only gains a one-line `locks` statement that P10 (okfreq, scopes =
the groups below) turns into SwRS/StRS.

## 0. Safety rules (added by plan-review.md; they override anything below)

1. No assertion is lost. A screenshot may be dropped only by setting `capture: false`; the
   scenario and every check it runs stay. A scenario is removed (D/M) only when it is an exact
   alias of a surviving scenario (same fixture, theme, preview theme, width, scroll and flags):
   `syntax-light-shell`, `preview-toolbar-dark`, `edit-mode-dark`, `edit-table-cell-dark`. All
   other former D/M rows are now A (`tools/overrides.mjs`; `migration.md` is regenerated). Pruning
   assertion-only scenarios is out of P9 (optional later batch with a coverage proof).
2. Before touching anything (batch B0), snapshot the baseline outside the repo: the full visual
   run (`run-manifest.json`, all PNG hashes), the 15 README source PNGs, and the 15 generated
   `images/readme/*.png`. Every batch compares against it: the same set of checks must run
   (scenario/check counts in the manifest never decrease) and renamed PNGs must be byte-identical
   to their old files (migration.md gives the pairing).
3. Ids are keyed in code: `check_mermaid_theme_switch` runs only for the id `mermaid-map-dark`.
   Renaming it would silently disable the check. B1 replaces every id comparison by a scenario flag
   (`mermaidThemeSwitch`) BEFORE any rename; the implementer greps capture.py, renderFixtures.ts
   and test/site for old ids before B2.
4. Rule "never widen or weaken an existing test" stays in force: P9 changes where evidence is
   written, never what is asserted. A new gap-fill scenario that fails exposes a product defect:
   do not fix `src/` in P9; mark the scenario `knownIssue: "<followups id>"` (its failure is
   reported, not gating) and add it to `followups.md`.
5. Numbers in ids (`v12`, `r07`) are permanent identifiers from the end of B2a; new scenarios take
   the next free number of their group (see B4/B5), nothing is renumbered, ids never change. P10
   markers may therefore reference ids. Group order is the only ordering guarantee.
6. `.agents/changes/` is git-ignored: everything P10 needs later (group list, `locks`, the
   integration-test-to-group map) must live in tracked files (`test/shared/e2eGroups.ts`,
   `scenarios.ts`, `captureRegistry.ts`), not only in this folder.

## 1. Feature groups (= future okfreq scopes)

Order is the gallery order. Group ids are kebab-case and never renamed after P9.

| # | Group id | Title | Scope (what its requirements will cover) | src/ anchors (for P10 scopes) |
| --- | --- | --- | --- | --- |
| 01 | rendering-core | Rendering core | CommonMark blocks, inline code, long docs, CJK/RTL, missing images (admonition colours and layouts belong to `myst`, where their captures are) | src/render, src/security/html-sanitizer, src/preview/previewStyles |
| 02 | code-blocks | Code blocks | Fences, highlighting, diff fences, unknown grammar, copy button | src/render, src/webview (copy) |
| 03 | gfm | GitHub Flavored Markdown | Autolinks, task lists/toggles, strikethrough, alerts, footnotes, raw HTML, colour spans | src/render, src/mapping (checkbox) |
| 04 | myst | MyST syntax | Directives, roles, admonitions, context tags, math, figures/labels, citations, conf.py checks, label rename | src/render, src/mapping/labelRename, src/myst* |
| 05 | diagrams | Diagrams | Mermaid (themes, fallback, errors), PlantUML (success, unconfigured, not found) | src/render/plantUmlRenderer, mermaid bundle |
| 06 | frontmatter-schema | Frontmatter and OKF schema | Properties table, schema validation/errors, generic YAML, x-okf-link details, field editing | src/frontmatter |
| 07 | layout-width | Layout and width | First-element gap, Margin/Auto/Full, max width, overflow, narrow/wide panes | src/preview/previewStyles, src/webview/scrollSync |
| 08 | theme-zoom | Theme and zoom | Host themes, forced white/cream/dark, high contrast, zoom 70–200 % | src/preview/previewStyles, toolbar |
| 09 | toolbar-navigation | Toolbar and navigation | Toolbar rows/collapse, sticky headings, TOC, Back/Next, anchor, title-bar/Quick Open | src/preview/previewToolbar, src/webview |
| 10 | block-editing | Block editing | Edit mode, block editors, keyboard, undo, insert points, move, selection, clipboard | src/webview, src/mapping |
| 11 | palette-slash | Edition palette and slash menu | Palette modes, popups, shortcuts, link panel, figure form, slash menu, image pick/paste | src/webview/editPalette, editActions |
| 12 | table-editing | Table editing | Cell editors, cell bar, Tab/Enter, minimal diffs | src/webview, src/mapping |
| 13 | review-annotations | Review annotations | Comment/TODO chips, review threads, sidecar, orphans, incoming changes | src/comments, src/webview/incomingChanges |
| 14 | lifecycle-sync | Lifecycle and sync | Open/refresh/reload/restore, Open With, scroll sync, incremental patches, status pages, coexistence | src/extension.ts, src/preview, src/webview/scrollSync |
| 15 | trust-security | Trust and security | Restricted Mode, read-only/standalone, refused messages, CSP, resource policy | src/security, src/preview/previewMessages |

## 2. Naming scheme

- Visual scenario id: `<group>/vNN-<slug>-<theme>-<width>`; e.g.
  `layout-width/v12-break-auto-light-900`. `v` = mock host, `NN` two digits per group in
  gallery order, `<theme>` ∈ dark, light, fallback, white, cream, hc-dark, hc-light,
  `<width>` = pane px. File: `out/reports/e2e/screenshots/visual/<group>/vNN-….png`, sidecar
  `.json` beside it. Step PNGs: `vNN-…--<step>.png` (double dash).
- Real-window capture id: `<group>/rNN-<slug>`; file
  `out/reports/e2e/screenshots/<suite>-<run>/<group>/rNN-<slug>.png` + `.md` note. Numbers come
  from one registry (below), so suites never collide.
- Fixed locations (the plan and migration.md previously disagreed): PNG/JSON under
  `screenshots/visual/<group>/`; `run-manifest.json`, `INDEX.md`, `MACHINE-CHECKS.md` stay at
  `screenshots/` (review-index.ts, REVIEW.md and the validators read them there); first-gap and
  width-margin reports at `out/reports/visual/first-gap/<group>/vNN-….json` (mkdir parents).
  The `/` in an id must be handled in every writer of capture.py (screenshot, sidecar, steps,
  first-gap, width-margins, TOC reports), in the stale-file cleanup (recursive over
  `screenshots/visual/`, plus a one-time purge of the legacy flat PNG/JSON/TXT) and in `--scenario`
  (also accept the old id through an alias table during B2a-B2b, remove it in B2c).
- A partial run (`--scenario`, `--group`) must not overwrite `run-manifest.json`: it writes
  `run-manifest.partial.json` and the gallery/REVIEW ignore it (root cause of H9).
- `--scenario <id>` keeps working (ids contain `/`; capture.py creates parent folders).
- Slugs say the state, not the test technique (`toc-hidden-narrow`, not `toc-column-460`).

## 3. Per-scenario metadata

Visual (`Scenario` in `test/visual/scenarios.ts`, replaces `scenarioGroup()` and aliases):

| Field | Type | Meaning |
| --- | --- | --- |
| `group` | GroupId | One of the 15 ids. `GROUPS` (order, title, scope, src anchors) lives in a tracked shared module `test/shared/e2eGroups.ts`, imported by `scenarios.ts` and `captureRegistry.ts` and exported as JSON for capture.py and the gallery script. The same module maps each integration test file to its group with a one-line `locks` (the 26 files without screenshots), so P10 has a tracked base |
| `locks` | string | One sentence, present tense, observable: "The TOC column is hidden under 760 px while the preference stays on." Raw material for P10 |
| `capture` | `false`? | Assertion-only scenario: every check runs exactly as before (including the final-frame checks), no PNG, no step PNG, no sidecar; the manifest result has no `capture` and the gallery lists it as a text row. `capture.py` must still write its first-gap/width reports |
| `steps` | string[] | Step PNG names to write. Semantics: capture.py holds a `STEP_NAMES` registry of every step name its checks can emit; `save_step()` writes a PNG only if the name is in `steps`, silently skips the other registered names (the check still runs), and FAILS on a name missing from the registry (typo). Each written step is recorded in the manifest |
| `knownIssue` | string? | Followup id: the scenario exposes a product defect; its failure is reported but not gating (rule 4) |
| `mermaidThemeSwitch` | `true`? | Replaces the id comparison `scenario["id"] != "mermaid-map-dark"` (rule 3) |
| `gallery` | `"key"`? | Shown first in its group page and in the index thumbnails |
| `readme` | `{ file, crop: [x0, y0, x1, y1], width, step? }`? | Source of an `images/readme/*.png` |
| `description` | string | Kept: what to look at in the PNG |

Real window: `test/shared/captureRegistry.ts` maps each id to `{ group, suite, locks, gallery?,
readme?, clip: "preview" | "window" }`. `Evidence.capture(page, frame, id, note)` (shared writer
used by realInput, checkbox, frontmatter, scroll, reload) rejects unknown ids, writes the PNG
(`clip: "preview"` crops to the webview frame, default for everything except README/workbench
shots), the note, and a `captures` entry in the run `manifest.json`; at suite end it fails if a
registered id of that suite was not captured.

## 4. PO gallery

- Naming: `npm run gallery:generate` ALREADY exists and means "curate README images" (it runs
  curateGallery.ts + generate-readme-images.py and rewrites tracked `images/`); `test/site/buildSite.ts`
  already builds an HTML screenshot gallery. The PO gallery is a third thing: call it
  `npm run review:gallery` / "PO gallery" everywhere, never "gallery" alone, and never run
  `gallery:generate` as a batch gate except in F (it rewrites `images/gallery.json` with a new
  timestamp: do not commit that noise; commit `images/` only if a README image changed on purpose).
- Generator: a TypeScript module `test/site/poGallery.ts` (compiled with the rest, unit-testable
  from `test/site/*.test.ts`, which `test:unit` runs) plus a 5-line `scripts/generate-e2e-gallery.mjs`
  wrapper; called by `review:finish` (review-index.ts) and runnable alone (`npm run review:gallery`).
- Inputs: `screenshots/run-manifest.json` (never the partial manifest), the run manifests named by
  the LATEST pointers (real window), and the tracked `e2eGroups` module (groups, integration-test
  rows). Within a group the order is: visual scenarios by number, real captures by number,
  integration-only rows. Missing evidence is shown as missing, never invented.
- Outputs under `out/reports/e2e/`: `GALLERY.md` (one section per group: scope, counts
  visual/real/assertion-only, key thumbnails) and `gallery/<group>.md` (every capture: id, locks,
  source mock/real, status, `<img src=… width="360">` thumbnail linking to the full PNG,
  note link, step PNGs inline, assertion-only scenarios as text rows).
- `REVIEW.md` gets item 0 "[Product-owner gallery by feature](GALLERY.md)", its counts are read
  from the manifests (fix H9: it also prints the visual run revision and flags a visual run older
  than the campaign), and "TXT" becomes "JSON or Markdown note" (H12).
- Pruning (H8): `review:finish` keeps the 3 newest run folders per suite prefix and deletes older
  ones; drop the legacy scroll move (H10).

## 5. README mapping

README.md is not edited and the paths `images/readme/*.png`, `images/21-edit-hover.png`,
`images/38-edit-mode-remembered.png` do not change (all are tracked; README.md also links
`images/38-edit-mode-remembered.png`; `images/01-paragraph-blur-commit.png` is curated but not
referenced, keep it). Only the SOURCES move.

- Today the images come from `out/` files through hard-coded names and pixel crops in
  `scripts/generate-readme-images.py` (15 crops, pixel boxes tuned to the 1800/2400 px source
  geometry) and `test/site/curateGallery.ts` (3 files looked up flat in the `real-input-*` run
  folder through `REAL-INPUT-LATEST.md`). `gallery:generate` only works after a passing full
  `test:e2e` (curateGallery checks `review.json`), so README sources cannot be verified per batch.
- Safe path: (1) B0 snapshots the 15 source PNGs and the 15 generated outputs. (2) B1/B2a add a
  `--check` mode to `generate-readme-images.py` that reads only the visual sources, writes to a temp
  directory and compares pixel-for-pixel with a given baseline directory; B2a is not done until it
  reports 0 differences for the 9 visual-sourced images (the 6 real-window ones are checked in
  T1). (3) B3 makes the script read the `readme` metadata (file, crop, width) instead of names;
  the crops are copied verbatim, never "improved". (4) A README source scenario must keep its
  viewport, fixture, theme, scroll and `fullPage`: the `readme` flag in `scenarios.ts` is a lock
  (a unit test fails if a `readme` scenario has `capture: false`, lacks its crop or is renamed
  without updating the map). (5) `images/` is committed only when F shows a deliberate difference.
- The `readme` set (15 + 3 files) is listed in `inventory.md` "README and docs images"; the
  gallery marks them "README" and the key set uses the same flag.

## 6. Work breakdown (each batch gate-able and revertible alone, in this order)

Gates: B = `npm run compile && npm run test:unit` + `npm run test:visual` (full run, not
`--scenario`); T = `npm run test:integration` on an UNLOCKED screen (T1 and T2 cannot be closed
with the TL/FL levels: the keyboard suites realInput, checkboxToggle, labelRename, blockMove are
the ones that capture and are skipped when locked; record them pending-unlock and do not tick the
batch); G = `npm run test:e2e` (then, once, `npm run gallery:generate`). Every batch ends with: gate
green, `inventory.md` regenerated, `STATE.md` ticked with the commit, no process left running, and
is ONE commit that `git revert` undoes entirely (no batch edits files owned by another batch's
concern except where named). Compare with the B0 baseline: scenarios and executed checks never
decrease except by the 4 alias removals.

### B0 — Baseline (no code; orchestrator or implementer, gate: none)

Full `npm run test:visual` at HEAD. Copy outside the repo (scratchpad): `run-manifest.json`,
`MACHINE-CHECKS.md`, every PNG with sha256, the 15 README source PNGs, `images/readme/*`. Record
the per-scenario check count if the manifest has it (else the `actions` list). Everything below is
compared to this. Also write `tools/old_to_new.json` from `migration.md` (used by `--scenario`
aliasing, by the PNG byte-compare and by the gallery for "was" links).

### B1 — Visual harness infrastructure (gate B; no id changes, no PNG content change)

1. `test/shared/e2eGroups.ts`: `GROUPS` (+ JSON export for Python/Node) and the integration-file
   map (26 files, group + `locks`). `scenarios.ts`: fields `group`, `locks`, `capture`, `steps`,
   `knownIssue`, `mermaidThemeSwitch`, `gallery`, `readme`; fill `group` for all 245 from
   `tools/decisions.mjs` + `tools/overrides.mjs` (old ids unchanged in B1); remove
   `scenarioGroup()`; `renderFixtures.ts` sorts by group then declaration order (do NOT reorder
   `scenarios.ts` itself: keeps diffs reviewable) and exports `GROUPS`.
2. Rule 3: add `mermaidThemeSwitch: true` to `mermaid-map-dark` and test the flag instead of the id;
   grep for any other id literal.
3. `capture.py`: `save_step(page, scenario, step, **opts)` replaces the 24 direct
   `page.screenshot` step calls (see the `steps` / `STEP_NAMES` semantics in section 3); records
   `{file, step}` in `result["captures"]`; short step sidecar. The duplicate check covers ALL PNGs
   of the run (H1). Partial runs write `run-manifest.partial.json`.
4. Fix H2 (alias scenarios write no step PNGs), H3 (`-end` is not written when identical to
   `-open`; the End-key assertion stays), H4 (no `-insert-point` when it equals the final frame).
   Four more byte-identical step PNGs are NOT covered by H2-H4 and must also stop here or the new
   duplicate gate fails on its own batch: `palette-mode-myst-{light,dark}-palette` (= `edit-palette-*`
   primaries) and `slash-menu-{strict,myst}-light-open` (= their primaries): drop them through `steps`.
5. Sidecar `actions`: only checks whose flag applied (H5). Support `capture: false` (section 3).
6. `generate-readme-images.py --check` (section 5).
Expected after B1: 245 scenarios, 240 primary PNGs, 76 step PNGs, 0 duplicate pairs, the same
executed checks as B0; every PNG pair-for-pair identical to B0 except the removed duplicates.

### B2a — Pure rename and move (gate B; mechanical, zero behaviour change)

Rename ids to `<group>/vNN-…` exactly as `migration.md` says, edit ids IN PLACE in `scenarios.ts`
(no reordering, no reformatting), move outputs to `screenshots/visual/<group>/` with the `/`
handling of section 2, purge the legacy flat files once, keep the old-id alias for `--scenario`.
The 4 exact aliases are removed here (their ids stay in `old_to_new.json`). Update
`generate-readme-images.py` and the unit/gallery tests that name old ids (`gallery.test.ts` uses a
synthetic name; `cleanup.test.ts` is flat-path only). Docs: CONTRIBUTING lines 44-45, 76-81.
Gate extras: every renamed PNG byte-identical to its B0 file (script over `old_to_new.json`);
`--check` README run: 0 differences; scenario count 241; executed checks equal to B0 minus the
4 aliases. Revert = `git revert` of this single commit.

### B2b — Assertion-only conversion and step pruning (gate B)

Set `capture: false` on the 104 A rows (61 original + 43 converted by plan-review; nothing is
deleted). Apply the `steps` lists of `migration.md` (30 kept, 65 dropped; a dropped step name stays
in `STEP_NAMES`, so the check that produced it still runs). Content fixes, each a separate small
change inside the commit so it can be bisected:
- `orphan-box-document-end`: keep a short box in place for the capture AFTER the check (the check
  currently removes the box and asserts the height is restored: re-add it once all asserts ran).
- `toc-column-light-900-auto` / `-light-460`: add a wide table to `30-toc.md` so Auto differs from
  Margin, but FIRST list every scenario on that fixture (toc-margin/auto/full/hidden, dark-1600
  and dark-460 assertion rows): their `tocChecks` must still pass unchanged, and the new TOC
  PNGs are new baselines (they are not README sources). Rename `toc-column-light-460` ->
  `toc-hidden-narrow` (already in the table).
- `width-modes-*` rows are assertion-only, so the cycle PNG problem disappears with them; keep
  one captured key image per mode through the existing `width-mode-break-*` PNGs.
Expected after B2b: 241 scenarios (137 with a PNG, 104 assertion-only), 137 primary + 30 step PNGs
= 167 visual PNGs (from 335), the same executed checks as B2a, 9 visual README images identical.

### B2c — `locks` and index data (gate B + unit test)

Write the `locks` sentence for every one of the 241 scenarios (observable present-tense rule; start
from the description). A unit test fails on a scenario without `locks`, without `group`, with a
duplicate id/number, a `readme` scenario that is assertion-only, or a `steps` name not in the
registry. No behaviour change. This batch is text only: it may be split per group among several
implementers and reviewed by a Sonnet critic for "observable, one behaviour, no technique".

### B3 — PO gallery, README metadata, report hygiene (gate B + `review:finish`)

`test/site/poGallery.ts` + wrapper + unit test (fake manifests: missing step, assertion-only row,
partial manifest ignored, group with only integration rows); REVIEW.md item 0 and counts from the
manifests (H9, H12); pruning (H8): keep the 3 newest run folders per suite prefix, NEVER delete the
folder named by a LATEST pointer or the one a manifest of the current campaign references, drop the
legacy scroll move (H10); `readme` metadata drives `generate-readme-images.py` (verbatim crops,
`--check` equal). Gate: B, then `npm run review:finish` on the existing manifests, then
`npm run review:gallery`; gallery lists all 241 visual rows + 117 real rows + 26 integration rows.
`gallery:generate` is not part of this gate.

### T1 — Real-window evidence harmonisation (gate T, unlocked screen only)

1. `test/shared/captureRegistry.ts` + shared `Evidence` writer (H7); port realInput harness,
   checkboxToggle, previewEditing (frontmatter), scroll-sync-suite, reload-suite to it, ONE suite
   per sub-commit (realInput last: 202 KB, 10 direct `evidence.capture` sites plus the helper at
   line 151). Keep unchanged in shape: the five LATEST pointer files and their link text
   (`[Ordered captures](…/INDEX.md)`), `INDEX.md`, `manifest.json` fields that curateGallery,
   generate-readme-images and `reviewEvidence` read (`runId`, `status`, `startedAt`...), and the run
   folder prefixes (`real-input-`, `scroll-e2e-`, `frontmatter-e2e-`). New files are added beside
   them; per-group subfolders live INSIDE the run folder.
2. Rename the 117 captures per `migration.md` "Real window"; for the 15 A rows keep the
   assertion and the note, write no PNG, and do not count them as "registered but not captured"
   (registry flag `capture: false`).
3. `clip: "preview"` for frontmatter description/links captures (H11): implement with a fallback to
   the full-window capture if the frame rectangle cannot be resolved, and keep `clip: "window"` for
   every README source and workbench shot (those crops are pixel boxes on the window geometry).
4. Content fixes: `t20` after Ctrl+/ before undo, `t21` with the language list open, `t22` with the
   link panel open, `t41-escape-on-picker` before Escape, `links-*-saved-target` clipped to the
   changed excerpt. Each adds a capture before an action; none removes an assertion.
5. `curateGallery.ts` and `generate-readme-images.py` read the registry flags and the new
   per-group paths; the 6 real-window README images are compared (`--check`) against B0.
Expected after T1: 102 real PNGs (+0 new), all registered by group; a suite fails if a registered
capture of that suite is missing (only when the suite ran completely, not with `--scroll-only`).

### B4 — Visual gap fill: content and error states (gate B)

Harness work first (own commit inside the batch): `renderFixtures.ts` currently hard-codes
`trusted: true`, `strictAdditionalProperties: false`, `renderPreviewToolbar()` (editing enabled),
the properties table always on, and keys its page cache by fixture/theme/sticky/plantuml only.
B4/B5 need per-scenario render options (`readOnly`, `strictAdditionalProperties`,
`propertiesTable`, `maxContentWidth`, `zoomClicks`, `hostMessages` for the mock host, generated
fixtures) AND those options in the page-cache key, otherwise a new scenario silently reuses an old
page. The existing 241 scenarios must produce byte-identical pages (diff the rendered HTML before
and after this harness commit).

Ids: `<group>/vNN-<slug>-<theme>-<width>` with NN = next free number of the group in
`migration.md` (rendering-core from v17, gfm v02, myst v20, diagrams v08, frontmatter-schema v26).
The suggested slugs below are the contract, the numbers are not.

| New scenario (slug, theme, width) | Fixture (new unless stated) | Locks |
| --- | --- | --- |
| rendering-core cjk-rtl light 900, light 460 | 35-cjk-rtl.md (CJK, Hebrew, Arabic, long word/URL) | Wraps without page overflow; RTL paragraphs right-aligned |
| rendering-core missing-image dark 900 | 36-missing-image.md | A missing local image shows its alt text and no broken layout |
| rendering-core huge-document-bottom dark 900 | generated 6000-line fixture (a build-time generator in renderFixtures, nothing committed) | Renders, bottom sentinel reachable, sticky band correct |
| gfm gfm-gallery-full dark 900, light 900, light 460 | 37-gfm-gallery.md (alerts x5, task list, strikethrough, footnotes, aligned table, raw HTML table/img, colour spans) | Each GFM construct renders as on GitHub |
| myst myst-gallery-full dark 900, light 900 | 38-myst-gallery.md (dropdown, deflist, sub/sup, footnotes, roles, glossary, label/ref) | Each MyST construct renders |
| myst conf-extension-warning dark 900 | 39-myst-conf/ | Warning line names syntax and extension. The warning is produced by the host (`mystDiagnostics`), not by the static page: this scenario is mock-injected via `hostMessages` only if the runtime renders such a message; otherwise drop it here and rely on T2 |
| diagrams mermaid-syntax-error light 900, dark 900 | 40-mermaid-error.md | Failure keeps the source visible with an error message |
| frontmatter-schema invalid-yaml dark 900 | 41-invalid-yaml.md | Parse error shown, body still rendered |
| frontmatter-schema unknown-field-strict light 900 | 08 + `strictAdditionalProperties` | Undeclared field warning when strict is on |
| frontmatter-schema properties-hidden light 900 (A) | 07 + `propertiesTable: false` | No table when the setting is off |
Check the fixture prefixes 35-41 are free (today 01-34 are used). Expected: +15 scenarios (14 PNGs)
-> 256 scenarios, 151 primary PNGs. Several scenarios may expose real defects (huge document, RTL,
CJK): apply safety rule 4.

### B5 — Visual gap fill: extension states (gate B)

Needs the B4 harness plus: high-contrast themes in `themes.ts`, forced-dark on a light host,
zoom clicks, `readOnly` toolbar/page state, mock-host messages for incoming changes and review
threads (the mock `postMessage` handles only `previewEditOpen` today). Split in two commits:
(a) trust/theme/zoom/layout/toolbar/block/palette rows, (b) review-annotations rows.
High contrast: `src/` has NO high-contrast handling (no `vscode-high-contrast` selector); invented
HC variables would test nothing real. Do HC as an exploratory pair: capture, review by a human; if
the page is unreadable file a followup and mark `knownIssue`. Do not claim "readable" as a lock
until the product handles HC.

| New scenario (slug, theme, width) | Locks |
| --- | --- |
| theme-zoom hc-dark-handbook hc-dark 900, hc-light 900 | Exploratory: borders and text visible with HC variables |
| theme-zoom forced-dark-handbook light 900 | Forced dark on a light host |
| theme-zoom zoom-70 light 900, zoom-200 light 900, zoom-150 light 460 | Zoom scales text and column together, no horizontal scroll |
| trust-security read-only-page dark 900, light 460, read-only-no-hover-outline (A) | Read-only toolbar has no pencil; no edit affordance |
| review-annotations incoming-bars light 900, dark 900, incoming-diff-off (A) | Changed blocks get a green left bar; Diff toggle hides them |
| review-annotations review-thread-open light 900, review-thread-resolved light 900, orphaned-list light 900, comment-chips-hidden (A) | Threads, resolved state, orphan list with entries, chips off |
| toolbar-navigation back-enabled-after-anchor light 900, mark-editor-selection light 900 | Back enabled after an in-page jump; editor line marker |
| block-editing block-selection light 900 | Selected blocks outlined, no editor open |
| palette-slash slash-gfm light 360 | Menu stays inside a 360 px pane |
| layout-width max-width-setting light 2000 | `maxContentWidth` other than 960 honoured on a wide pane |
Numbers: next free in each group (theme-zoom v08, trust-security v01, review-annotations v05,
toolbar-navigation v30, block-editing v15, palette-slash v18, layout-width v85 in the current
migration.md). Expected: +21 scenarios (18 PNGs).

### T2 — Real-window gap fill (gate T, unlocked screen; spike first)

Spikes (one commit each, may be abandoned and listed as deferred without blocking F):
- Untrusted capture: `runUntrustedScenario` spawns Code directly and passes no debug port and no
  `STUDIO_CDP_PORT`; add `--remote-debugging-port` and the env, and check a webview is reachable
  in Restricted Mode before writing the registry rows.
- Standalone: add `standalone-suite.js` to the browser-suite list (CDP port) in `run-tests.ts`.
- Incoming changes: positive test needs a tracked file with a working-tree change in a git repo
  the built-in git extension discovers; create the temp repo under the workspace root's fixtures
  folder, `git init` + commit + edit, wait for the repository to appear, and clean up in `finally`
  (the folder is not git-ignored). If git discovery is flaky, keep the unit-level assertion and
  skip the capture.
Captures (ids `<group>/rNN-…`, next free number per group after T1): untrusted read-only window
and standalone read-only (`trust-security`), incoming positive (`review-annotations`), MyST conf.py
warning in preview + Problems (`myst`), review thread create/reply/resolve (`review-annotations`,
3), image paste result (`palette-slash`), label rename (`myst`), Back/Next across documents
(`toolbar-navigation`), `refreshPreview` command and the Cmd/Ctrl+K Shift+V keybinding
(`lifecycle-sync`, assertions + 1 capture), `doubleClickToSwitchToEditor` (`toolbar-navigation`,
assertion). Expected: <= +12 real PNGs (about 114); whatever a spike drops is listed in
`followups.md`, not forced.

### F — Final pass (gate G)

Full `npm run test:e2e` on an unlocked screen, `review:finish`, `review:gallery`, then
`gallery:generate` once; README images byte-compared with B0 (differences reviewed, `images/`
committed only if intended; `images/gallery.json` timestamp noise discarded); regenerate
`inventory.md`; reviewer (Sonnet) checks: every capture has group + locks, no duplicate PNG, every
group has >= 1 gallery key, every finding of `findings.md` closed or listed as deferred, no
scenario of B0 missing from `old_to_new.json`, executed checks >= B0 minus the 4 aliases.

## 7. Expected counts

| Stage | Visual scenarios | Visual PNGs (primary + steps) | Real PNGs |
| --- | --- | --- | --- |
| Now | 245 | 240 + 95 = 335 | 117 |
| B1 | 245 | 240 + 76 = 316 | 117 |
| B2a/B2b | 241 | 137 + 30 = 167 | 117 |
| T1 | 241 | 167 | 102 |
| B4 | 256 | 151 + 30 = 181 | 102 |
| B5 | 277 | 169 + about 32 = about 201 | 102 |
| T2 | 277 | about 201 | about 114 |

## 8. Migration table

`migration.md` is the single authoritative old id -> new id table (generated by
`tools/build_inventory.mjs` from `tools/decisions.mjs` + `tools/overrides.mjs`). The copy that was
embedded here is removed so the two cannot drift.
