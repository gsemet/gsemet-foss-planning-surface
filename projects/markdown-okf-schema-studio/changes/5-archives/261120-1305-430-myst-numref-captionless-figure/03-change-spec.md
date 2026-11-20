# Change Specification: CR-430 `{numref}` to a captionless figure or table shows its number

## Goal

SwRS-MDOKFSTUDIO-MYST-019 is right (owner, 02-answers.md): a `{numref}` to a figure or table
without a caption shows its number (`Figure 1`, `Table 1`), as Sphinx does. The code must do so,
and a test must prove it, so that the SwRS and the code no longer disagree and the `{numref}` case
is no longer untested.

## What was found while writing this specification

The contradiction reported by CR-348 (PR 419) comes from two different targets, not from the code:

- `test/core/render/renderReq.myst.requirements.test.ts`, test "doc and download roles render as
  plain links and numref as an inert placeholder" (marked SwRS-MDOKFSTUDIO-MYST-017), renders
  ``{numref}`fig-x` `` where `(fig-x)=` labels a **heading**. That placeholder (a
  `span.reference.role.unhandled` with text `{numref}fig-x`) is MYST-017's own documented
  behaviour ("`{numref}` to a heading label is never resolved to a number").
- MYST-019's scenario is about a `{numref}` to a captionless **figure or table**. Rendering that
  case through the compiled pipeline of main (`out/`, built 2026-11-06; no reference or caption code
  in `src/core/render` changed since) already gives the number:

  ```text
  {numref}`fig-empty`            -> <a href="#fig-empty">Figure 1</a>
  {numref}`tbl-empty`            -> <a href="#tbl-empty">Table 1</a>
  {numref}`Fig %s <fig-empty>`   -> <a href="#fig-empty">Fig 1</a>
  {ref}`fig-empty`               -> <a href="#fig-empty">fig-empty</a>
  diagnostics: []
  ```

  (`node --import ./scripts/register-myst-patches.mjs` with `renderPreviewDocument` and
  `inlineDocument` from `out/test/core/render/mystFeaturesSupport.js`; the figure is a
  `{figure} image.svg` with `:name: fig-empty` and no body, the table a `:::{table}` with
  `:label: tbl-empty` and no title.)

So the expected code change is none: the work is the missing test, the requirement's verification
notes and the log. The Driver confirms this first on a fresh build (step 1 below); only if the test
fails does the code change (step 2).

## What changes

### 1. Test (always)

File: `test/core/render/mystFeatures.test.ts`, test "references to captionless figures and tables
stay readable" (around line 111).

- Put `// @tests_req SwRS-MDOKFSTUDIO-MYST-019` directly above it (today only the test before it,
  "figure references render figures whose body supplies the caption", carries the marker).
- Extend its document so it also holds ``{numref}`fig-empty` `` and ``{numref}`tbl-empty` `` next to
  the existing ``{ref}`fig-empty` `` and ``{ref}`tbl-empty` ``, against the same captionless figure
  (`:name: fig-empty`) and captionless table (`:label: tbl-empty`).
- Assert, on the `a` elements of the rendered HTML:
  - the hrefs: `#fig-empty`, `#tbl-empty` for both roles;
  - the texts: `fig-empty` and `tbl-empty` for `{ref}`, `Figure 1` and `Table 1` for `{numref}`;
  - no link has empty text;
  - no `span.reference.role.unhandled` is rendered (the numref is resolved, not a placeholder);
  - `result.diagnostics.length === 0` (kept).
- Either extend the existing test or add one next to it named, for example, "a numref to a
  captionless figure or table shows its number"; the file is at 1342 lines, under the 1500 limit of
  `scripts/check-file-sizes.mjs`, so a separate test fits.
- Leave `renderReq.myst.requirements.test.ts` and its MYST-017 heading placeholder test unchanged.

### 2. Code (only if step 1 fails on a fresh `just compile`)

The pass is `normalizeCaptionlessReferences` in `src/core/render/mystBlockTransforms.ts` (marked
MYST-019; run as the "caption-less references" pass in `src/core/render/mystRenderer.ts`). It only
fills a `crossReference` of kind `ref` with the identifier. If a captionless `{numref}` then renders
without its number, make the pass (or the `{numref}` path it leaves to the MyST writer) give the
enumerator text: `Figure <n>` / `Table <n>`, or the role's explicit `%s` template filled with the
number. A `{numref}` to a heading label stays MYST-017's inert placeholder.

### 3. Requirement

File: `requirements/tiers/swrs/myst/SwRS-MDOKFSTUDIO-MYST-019.md` (`req_lifecycle: proposed`, so no
owner re-approval).

- Normative text and scenarios unchanged.
- Verification notes: the second Method line names the new or extended test and drops "which
  checks `{ref}` only; the `{numref}` case is untested".
- `tested_in_files` and `implemented_in_files` stay as they are unless step 2 touches another file.

### 4. Log and generated files

- `requirements/tiers/log.md`: a dated entry (the day of the change) saying the MYST-019 `{numref}`
  contradiction reported on 2026-11-18 (line 64-65 of the log) was a numref to a heading label
  (MYST-017's placeholder) read as a captionless figure; the captionless case already numbers, and
  is now tested in `test/core/render/mystFeatures.test.ts`. No normative change (or, if step 2 ran,
  the code fix named).
- `just requirements-update`, then `node scripts/check-marker-companions.mjs --update` if the marker
  baseline changes.

## Decisions carried from 02-answers.md

- The SwRS MYST-019 is right; the code follows it: a captionless figure or table shows `Figure 1` /
  `Table 1` for `{numref}` (carried in sections 1 and 2).
- The missing test is added (section 1).

## Out of scope

- `{numref}` to a heading label, and MYST-017's wording and test (its inert placeholder stays).
- `{numref}` to equations, code blocks or other numbered targets; numbering across documents.
- Any change to `{ref}` behaviour.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/`: no rendered syntax changes
  (only if step 2 changes what a `{numref}` renders does the skill need checking).

## Evidence

- The new assertions pass in `just check` (unit suite, `out/test/core/render/mystFeatures.test.js`),
  and fail if the `{numref}` text is changed to the placeholder (the Driver states how it saw the
  test fail once, e.g. by asserting `{numref}fig-empty` temporarily, or that step 2 was needed).
- `just requirements-lint` and `uv run --no-sync --group requirements okfreq validate --check-links
  --project-root .` pass; `just requirements-report` lists the new test under MYST-019.
- `just preflight` (on Windows, the static stage) passes.
- No host or default matrix: the behaviour is the same core render on every host and has no setting.

## Open questions

None.
