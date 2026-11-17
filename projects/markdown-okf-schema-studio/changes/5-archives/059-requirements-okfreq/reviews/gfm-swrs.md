Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: gfm StRS and SwRS

Scope `gfm`: 4 StRS, 36 SwRS, reviewed against `inventory/gfm.md`, the requirements guidelines and
the sources at `markdown-okf-schema-studio-wt-059`. `okfreq validate --prose --check-links`: 246
requirements, 0 errors, 0 warnings.

Verdict: REVISE

## What passed

- Coverage: F-GFM-001..036 map 1:1 to SwRS-GFM-001..036 (no duplicates, no placeholders, every
  `derives_from` points to the right UC/StRS, titles equal the first `##` heading). The two
  descriptions rewritten without angle brackets (029 details/summary, 030 kbd) stay faithful.
- F-GFM-037 skip: valid (a page-wide no-overflow check on a composite gallery is owned by
  layout-width per the guideline, atomic parts are F-001, 008, 009, 014, 015, 016, 029, 031).
  Caveat: `requirements/tiers/swrs/layout-width` does not exist yet in this worktree; the critic of
  that scope must confirm a no-overflow SwRS exists, and the visual scenarios `gfm/v02..v04` should
  carry that SwRS marker, not a GFM one.
- StRS 001-004: user-observable, no implementation detail (minor wording: StRS-003 "exactly that
  character" is acceptable).
- Spot check (13 of 36 against inventory and source: 002, 004, 009, 010, 011, 018, 022, 024, 027,
  029, 030, 034, 036): `www.localhost` undotted (BARE_URL_HOST requires a dot), unknown `[!FOO]`
  stays plain quote, legacy bold marker alone on the line, `[ ]` toggled gives lowercase `x`,
  `ownUndoStep: true`, summary regex `[^<]*` (markup not recognised), `kbd` regex `^<kbd>$` (no
  attributes) all match the SwRS text.

## Defects (5)

1. SwRS-MDOKFSTUDIO-GFM-022: scenario 2 ("Re-checked uppercase marker", `[X]` written back as `x`)
   is not a boundary of "one undo step" and its GIVEN/WHEN is muddled (unchecked then re-checked,
   then toggled). Fix: move the `[X]` -> `x` case to SwRS-021 (toggle writes lowercase `x`), and
   make 022 scenario 2 the real boundary from F-GFM-022: no visible editor shows the document, the
   edit is still applied as one step (workspace edit), or uncheck gives one undo back to `[x]`.
2. SwRS-MDOKFSTUDIO-GFM-020: scenario 2 ("input of type text in raw HTML is removed") has no
   evidence: `html-sanitizer.ts` has no input/checkbox rule and the test only covers the kept
   checkbox. Fix: replace by a verified boundary (e.g. checkbox without line/column attributes, or
   state `checked`/`disabled` kept) or cite the code that drops other inputs.
3. SwRS-MDOKFSTUDIO-GFM-012: two behaviours in one SHALL (fenced markers literal AND alert ends at
   first unquoted line). Fix: split into two SwRS, or keep one and move the other to its own SwRS
   with its scenario (and note the optional one-line shift edge in the inventory as out of scope).
4. SwRS-MDOKFSTUDIO-GFM-031: two behaviours (cell attributes rowspan/colspan 1-999/align/scope/
   class/title kept, and active content removed with its content, comments dropped); the boundary
   1 and 999 (and 0/1000 refused) is not exercised. Fix: split in two SwRS and add a span-limit
   boundary scenario.
5. SwRS-MDOKFSTUDIO-GFM-024: the SHALL covers all host refusal reasons but only stale and marker
   gone are scenarios, and scenario 2 shows the refusal reason, not the revert. Fix: add the open
   Markdown edit reason ("Save or cancel the open Markdown edit before toggling a checkbox.") and the
   apply failure reason ("VS Code could not apply the checkbox edit."), or narrow the SHALL; keep one
   scenario asserting the box returns to its previous state.

## Advisory (no revision needed)

- SwRS-004 (schemes + dotted host) and SwRS-034 (kept grammar + removed forms) are borderline
  bundles; acceptable as families, split if a test needs them apart.
- SwRS-014 scenario 2 (undefined `[^2]`) and SwRS-007 scenario 2 are not backed by inventory
  evidence; confirm with a test when writing the markers.
- SwRS-033 has no existing test (F-GFM-033 untested): needs a new test before traceability.

## Re-check

Verdict: FIX-REQUIRED

`okfreq validate --prose --check-links`: 264 requirements, 0 errors, 0 warnings (GFM-029/030 pass).

Defects 1 (022), 2 (020), 4 (split, span-limit boundary), 5 (024 four reasons) and 3 (037 added with 2
scenarios, derives_from StRS-002, inventory column F-GFM-012/031 lists 037/038) are fixed in substance.
GFM-029 and GFM-030 descriptions equal their normative sentences. GFM-020 scenario 2 keeps checked/line/
column attributes: the sanitizer has no input rule and passes attributes through, so it is plausible.

Remaining defects (split left the frontmatter `description` unsplit, so description != body, and the
index.md summary inherits it):

1. SwRS-MDOKFSTUDIO-GFM-012: `description` still reads "When an alert marker appears inside a fenced
   code block or the quoted lines end, ... SHALL keep fenced markers literal and end the alert at the
   first unquoted line." The body (and scenarios) only cover fenced markers; the alert-end behaviour
   now lives in GFM-037. Fix: description = "When an alert marker appears inside a fenced code block,
   the extension SHALL keep it as literal code." (also in gfm/index.md).
2. SwRS-MDOKFSTUDIO-GFM-031: `description` still ends with "and SHALL remove script, style, iframe,
   svg, form, embed and object elements with their content", now owned by GFM-038. Fix: description =
   "When a document contains a raw HTML table, the extension SHALL render its cells with rowspan and
   colspan from 1 to 999, align, scope, simple class names and title." (also in gfm/index.md).

Advisory: GFM-022 "No visible editor" path and GFM-024 host refusals remain untested (noted in
verification notes, acceptable).
