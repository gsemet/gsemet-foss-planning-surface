Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: frontmatter-schema SwRS (P10.3)

Reviewer: Sonnet critic, scope `frontmatter-schema` (FMSCHEMA), 18 StRS + 74 SwRS, worktree
`markdown-okf-schema-studio-wt-059`.

Verdict: REVISE

Method: read all 18 StRS and 74 SwRS; scripted the inventory mapping (49 F-FMSCHEMA rows, all map to
at least one SwRS; all 74 SwRS are referenced; OK). Spot-checked about 60% of the SwRS against
`src/core/frontmatter/{frontmatterParse,okfFrontmatter,propertiesTable,fileLinks,stemIndex,
frontmatterValidate,schemaValidator}.ts`, `src/session/features/{frontmatter,links}.ts`,
`src/session/hostEvents.ts`, `src/page/features/pageInput.ts`, `settingsRegistry.ts` and the tests
under `test/core/frontmatter/`. Ran `yaml.parseDocument` on three broken YAML strings to check one
claim (D3). The batch-1 defect classes (unbounded SHALL, bundled behaviours, false boundary
scenarios, glued headings, placeholders) are mostly absent: headings equal the titles, no
placeholder, derives_from is correct except D21. The defects below are the ones left.

## Defects (numbered, with fix)

### Code-contradicting claims and missing Known issues (anchored-to-code)

1. SwRS-024 / StRS-007, `$ref` JSON-pointer claim. StRS-007 says "with JSON-pointer fragments".
   Code (`okfFrontmatter.ts` `inlineRef` + `lookupJsonPointer`): the pointer is `#/defs/s`,
   `pointer.slice(1)` is `/defs/s`, `split("/")` gives an empty first segment, the lookup returns
   `undefined` and the property holding the reference is emptied. The SwRS-024 Known issue is TRUE
   (verified), but the StRS wording is false. Fix StRS-007 bullet: "...a fragment written without
   the leading slash (`base.schema.yaml#defs`) selects that key; Known issue: a standard JSON
   pointer (`#/defs/s`) empties the property that holds the reference." Remove "with JSON-pointer
   fragments". Also add a scenario to SwRS-024 for each form (no test exists for either).

2. SwRS-024, undocumented behaviour: `seen` is one Set shared by the whole resolution and entries
   are never removed. A second `$ref` to a file that was already inlined (a different property, no
   cycle at all) is replaced by `{"$ref": "#"}`, i.e. a reference to the schema root, so the field
   is validated against the whole schema. The "Reference cycle" scenario hides this. Add a Known
   issue and a scenario ("two properties refer to base.schema.yaml: the first is inlined, the
   second becomes a reference to the schema root"). Same family: a missing target also becomes
   `{"$ref": "#"}` (or the fragment alone), not "unresolved" as StRS-007 says; reword StRS-007 and
   add a Known issue to SwRS-024.

3. SwRS-025 / StRS-008, YAML parse errors are not reported. `parseSchemaFile` does
   `parseDocument(raw).toJS()` and never checks `document.errors` (checked: `type: [a` gives
   1 error and still returns `{"type":["a"]}`; an empty file gives `null`). A YAML schema with a
   syntax error is applied partially and silently, no "Schema could not be parsed" row; an empty
   YAML schema reaches `effectiveProperties(null)`. StRS-008 and SwRS-025 promise the warning for
   "a schema file that cannot be parsed" and only JSON/JSON5 can. Add a Known issue to SwRS-025 and
   StRS-008 (and a scenario for the YAML case), and narrow the description to JSON and JSON5.

4. SwRS-070 / StRS-017, false Known issue. `linkedFileDetails` returns `tooltipFields` and
   `previewFields` (as `{}` when empty) whenever tooltip fields, preview fields OR
   `show_line_number` is set, and the watcher condition is `tooltipFields !== undefined ||
   previewFields !== undefined`. So a target shown only with its line number DOES get its own
   watcher. Only a link whose annotation has none of the three gets none. Rewrite the Known issue:
   "a link whose annotation lists no tooltip field, preview field and no `show_line_number` gets no
   watcher of its own and relies on the preview-wide watcher". Same in StRS-017.

5. SwRS-065 / StRS-016, "without any tooltip" is false. A pending link carries the native
   `title="Loading linked file"` and its spinner `title="File links are being resolved"`. Only the
   Studio tooltip (`LINK_TOOLTIP_SELECTOR` excludes pending) is absent. Reword the SHALL and
   scenario 2: "...without the Studio link tooltip", and add the two native titles as a Known issue
   or criterion.

6. SwRS-022 / StRS-006, garbled Known issue. `readOnly = workspaceFolder === undefined ||
   !trusted` (`previewManager.ts` l.245, 459). A file inside a trusted workspace folder is NOT told
   it needs a trusted workspace. The real issue: a file outside every workspace folder in a trusted
   workspace gets the message "requires a trusted workspace", which is misleading. Rewrite both
   Known issues accordingly. Also state in the SwRS that the info row appears only when the
   frontmatter has a string `type` (untyped documents get no row in Restricted Mode), with a
   scenario.

7. SwRS-018 verification note is untrue: "Unit test of the frontmatter extraction... returns
   present = true, no mapping and the message". No test contains "not a mapping" (the inventory
   review already lists F-005 as untested). Replace the Method by "No dedicated test today" and add
   the Known issue "the not-a-mapping branch has no test". The same applies to SwRS-017 ("Unit test
   of the analysis and of the table renderer"): the only unit test is `extractFrontmatter reports
   invalid YAML` (extraction level); the row text "Invalid frontmatter YAML: ..." and the badge of
   1 are asserted only by the visual scenario. Fix the Method.

8. SwRS-023 / SwRS-025 / SwRS-024 verification notes overclaim. SwRS-025 says the parse-failure
   branch is "exercised only through the JSON5 trailing-comma case": no test contains that case or
   the text "could not be parsed". SwRS-023 "Trailing comma" scenario and SwRS-024 "Reference cycle"
   scenario (no `cycle` test in `test/core/frontmatter/`) are likewise untested, as are
   SwRS-037 (`minProperties`) and the tooltip "Allowed:" line is tested only in propertiesTable
   tests (check SwRS-031 Method, it says table renderer: fine). Correct the Method line of 023,
   024, 025 and 037 to say which scenarios have no test, and add "Known issue: untested" lines
   where the batch convention requires them.

9. SwRS-003 / StRS-001, empty frontmatter. StRS-001 says "an empty block is valid" and SwRS-018
   Known issue says "valid fence but still gets this error row": the user-visible truth is an error
   row "Invalid frontmatter YAML: Frontmatter is not a mapping." (`extractFrontmatter`: empty body
   parses to `null`). Propose StRS-001 wording: "...a document whose block is empty (two adjacent
   fences) is recognised as frontmatter but shows the error row 'Frontmatter is not a mapping.'
   instead of an empty table (Known issue)". Move the empty-block scenario out of SwRS-003 (title
   is about Windows line endings; the "CRLF empty block" scenario plus Known issue bundles two
   topics) into SwRS-018, keeping only the CRLF field/value scenario and one CRLF-empty-block line
   if wanted.

10. StRS-002 says a list or scalar "shows 'Frontmatter is not a mapping.'"; the row text is
    "Invalid frontmatter YAML: Frontmatter is not a mapping." (verified in `analyzeFrontmatterCore`
    and SwRS-018). Fix the StRS bullet.

11. SwRS-005 description and criteria claim the generic table is shown "without ... diagnostics"
    and "no row carries a diagnostic". False once a type is present: SwRS-021 (info row), SwRS-022
    (info row) and SwRS-025 (warning row) all use the generic table with a diagnostic row. Scope
    the claim to "no string type" or drop "diagnostics". Also add the boundary `type: ""` (empty
    string is falsy in `typeValue`, so it is generic with no lookup message), currently
    unspecified.

12. SwRS-033 / StRS-010: the displayed label is `datetime` (`TYPE_NAME_LABELS`), the SwRS scenario
    says "datetime" but the description and StRS-010 say "date-time". Pick the code's text:
    "enum, datetime, date, time, boolean, number, list, text or unknown". Note too that the format
    test precedes the type test, so `type: string` with `format: date` shows "date"; say so in the
    criteria.

13. SwRS-047: `parseAnnotation` also rejects a MISSING `resolution` or `syntax` (both are
    required: `FILE_LINK_RESOLUTIONS.includes(undefined)` is false). The SwRS and StRS-014 speak of
    "unknown" values only. Add "missing or unknown" and a scenario "annotation without syntax".

14. SwRS-069 / SwRS-073 boundaries: (a) identity: when `id_marker` is set but the document has no
    string value for it, there is NO fallback to the file-name stem (`frontmatterLinkIdentity` and
    `linkedFileDetails` return no identity, so no line); the criterion "the id_marker value, else
    the file name stem" reads as a fallback. Reword "else" to "when no id_marker is annotated" and
    add a scenario. (b) The match is `marker`, whitespace, `identity`, followed by end of line or a
    character that is not a letter, digit, `_` or `-` (so `Evidence dd` does not match
    `Evidence ddx`): add as a criterion/scenario. (c) SwRS-073: when no marker line is found the
    target still opens (at the top); state it.

15. SwRS-007 says "disabled checkbox"; the input has `aria-disabled="true"` and `tabindex="-1"` but
    NOT the HTML `disabled` attribute. Reword to "a checkbox marked aria-disabled and removed from
    the Tab order" (scenario and description).

16. SwRS-050 description: "accept it only when it names an existing file inside a workspace
    folder" is unconditional, but SwRS-062 lets it leave the workspace when
    `allowOutsideWorkspaceLinks` is true. Add "unless allowOutsideWorkspaceLinks is true" (or say
    "inside the navigation roots"; with no workspace folder the root is the document's folder).

17. SwRS-020 criteria "Only the part before `.schema` is case-folded" is wrong: `matchSchemaFile`
    lowercases the whole name for the suffix test too, so `Note.SCHEMA.YAML` matches. Fix the
    criterion (and the comment-derived wording in StRS-006: "stem equals the type,
    case-insensitively" is fine).

18. SwRS-045 / StRS-005: `onSettingsChanged` refreshes the frontmatter of every session only when
    the active editor's document is the session's document (`document.id === session.documentUri`
    with `host.editors.active()?.document ?? session.document`); a preview whose document is not
    the active editor is not re-analysed by this path. Also any change in the `preview` or
    `plantuml` section triggers the same frontmatter refresh (the SwRS only says "other section ->
    no refresh" and omits these). Narrow "every open preview" or add a Known issue after checking
    the else-branch (`updatePreview(lastGood)`), and mention the two other sections.

### Form (bounded single SHALL, headings, derives_from)

19. Nine SwRS carry more than one SHALL: 004, 017, 022, 027, 041, 060, 061, 062, 074 (074 has
    three). Split or reduce each to one bounded SHALL: 004 (hide table / still render body), 017
    (error row / body still renders), 022 (no lookup / info row), 027 (content comparison / 64
    cache cap, the cap deserves its own SwRS), 041 (error row / section flag, the editor's "no
    custom key" flag is an editing behaviour and belongs in FMEDIT), 060 and 061 (configured root /
    convention root, one SwRS each), 062 (false refuses / true allows, one SwRS each), 074 (not
    followed / warning text / malformed request text). After splitting, renumber through
    `okfreq new` and update the inventory Req column.

20. Other bundled SwRS under one SHALL: 035 (red underline + tooltip + JSON Schema 2020-12 + all
    errors; the engine/draft claim has no scenario, add one with a `$defs`/`prefixItems` 2020-12
    keyword or drop it), 039 (counts of errors, warnings and the infos-only rule), 064 (mark, label,
    focus, tooltip, badge), 046 (nine annotation positions in one SHALL; acceptable only if each
    position has a scenario: today only items and oneOf have). Add scenarios for patternProperties,
    additionalProperties, prefixItems, local `$ref`, allOf, anyOf, if/then/else, or split.

21. SwRS-006 derives from StRS-001 but its subject (nested values in YAML form) is StRS-003
    ("Property values read like YAML ... nested values"). Re-point `derives_from` to
    StRS-MDOKFSTUDIO-FMSCHEMA-003 and drop the "Names / Values ... nested mappings as YAML code"
    sentence from StRS-001 or keep it in both.

22. SwRS-040 criterion: the jump focuses the value cell only when the row has `data-okf-edit-cell=
    "value"`; otherwise it focuses the row's `th` (and the row selector includes `.okf-info` field
    rows). Add the fallback to the criteria; the Known issue is correct (info-ROWS carry no
    `data-okf-field`).

### Coverage gaps (behaviour without requirement)

23. Stem index: stems are matched case-sensitively, only for files ending in lowercase `.md`, and
    symbolic-link DIRECTORIES are not entered (`entry.isDirectory()` is false for them). Add a
    scenario/criterion to SwRS-055 or 058 (or a Known issue): `Same.md` does not satisfy stem `same`.

24. `findSchemaDirectory` documents its stop directory as exclusive but the loop includes it (the
    workspace root IS searched, which SwRS-019 scenario 1 assumes). Add that boundary explicitly
    to SwRS-019 criteria, and note that without a workspace root the walk runs to the file-system
    root.

25. Settings: `bundleRoot` / `projectRoot` accept an absolute path (used as is) and the
    configured root, when specified but missing, does NOT fall back to the convention root. The
    second part is in the SwRS Known issue; add the absolute-path case to SwRS-060/061 criteria.

## StRS wording fixes (summary of proposals)

- StRS-001: replace "an empty block is valid" by "an empty block (two adjacent fences) is
  recognised but shows the 'Frontmatter is not a mapping.' error row (Known issue)".
- StRS-002: row text "Invalid frontmatter YAML: Frontmatter is not a mapping."; add the
  empty-block Known issue.
- StRS-007: replace "with JSON-pointer fragments; ... a missing target stays unresolved" by the
  text of D1/D2.
- StRS-008: add D3 (YAML syntax errors).
- StRS-010: `datetime` label (D12).
- StRS-006 and StRS-017: Known issue rewrites (D6, D4).

## Checks that passed

- Inventory: 49/49 rows mapped, 74/74 SwRS referenced, no orphan SwRS.
- Known-issue claims verified true: BOM (regex anchored at `^---`), formatValue unused (em dash),
  "Names / Values" vs "Name / Value", `../../x.yaml` read outside the schema folder, sibling
  keyword next to `$ref` not inlined (`keys.length === 1`), `anyOf`/`oneOf` merged, `type: object`
  labelled unknown, root `additionalProperties: false` error unattached (instancePath empty ->
  info row), badge does nothing for info rows only, stem index of a root outside the workspace
  refreshed only by root mtime/ctime/size, one `projectRoot` for the whole workspace, alias limit
  100, 300 ms and 150 ms timers, 50-item list cap, 200-entry state map, 64-entry registry, 640 px
  (`<=`) thresholds, 480 px tooltip, 1.5 s highlight, label table of link problems, E10/W15
  message texts.
- Boundary scenarios checked true: 50 vs 52 list items, 640 vs 641 px, fence `...` closing, value
  ending in `...`, `constructor`/`toString` names, absolute POSIX/drive/UNC targets, ghost symlink
  W15.

## Re-check

Critic re-check after the revision (87 SwRS, 18 StRS). Method: read all 18 StRS and 87 SwRS, compared
every one of the 25 listed defects with `okfFrontmatter.ts`, `fileLinks.ts`, `stemIndex.ts`,
`propertiesTable.ts`, `pageInput.ts`, `hostEvents.ts`, `previewNavigation.ts`, `schemaRegistry.ts`
and the tests under `test/core/frontmatter/`. Scripted checks: every SwRS has one `derives_from`,
all of them exist and are listed in the parent's `derived_by` (and the reverse), frontmatter
`description` equals the Normative behavior text for the 105 files, no placeholder, inventory
Req column maps 49/49 rows to existing SwRS. Probed with the repo's `ajv` and `yaml` (scratch
script only): `properties: {a: undefined}` does not compile; `parseDocument("").toJS()` is `null`.

D1-D18 and D20-D25 are fixed and correct against the code (including: `#defs` vs `#/defs/s`, second
reference to a file, missing target, YAML parse errors, empty YAML schema, watcher condition, native
`title` of pending links, Restricted Mode wording, `aria-disabled`, `datetime` label, missing
`syntax`, no identity fallback, `allowOutsideWorkspaceLinks`, `Note.SCHEMA.YAML`, settings refresh
limited to the active editor's document, stem case and symlinked folders, stop directory included,
absolute bundle/project root). D19 is only partly fixed (item 3). The Known issue "an empty YAML
schema file makes the analysis throw a TypeError" is accurate: `parseDocument("").toJS()` is
`null`, `effectiveProperties(null)` and the compile `try` do not throw, and the final
`schema.additionalProperties` in `analyzeFrontmatterCore` (outside any `try`) throws.

### Remaining defects

1. SwRS-024 (scenario "Standard JSON pointer", Known issue 2) and StRS-007: the stated consequence
   of `$ref: base.schema.yaml#/defs/s` is wrong. The lookup returns `undefined`, the property is
   kept as a key with an `undefined` value (it is still listed in `availableKeys` and `known` is
   true, so "no longer declared" is false) and Ajv then refuses the whole schema ("schema is
   invalid: data/properties/a must be object,boolean", probed), so the table shows the red row
   "Schema validation failed to run: ..." and every validation is lost. Fix: scenario THEN "the
   property that holds the reference is left without a schema, the schema does not compile and the
   red row 'Schema validation failed to run: schema is invalid: ...' is shown"; same text in the
   Known issue and in StRS-007 (replace "empties the property that holds the reference").
2. SwRS-078 (Method) overclaims: "Unit test of the schema registry" for the 64-entry cap, but
   `test/core/frontmatter/schemaRegistry.test.ts` has no test reaching `MAX_ENTRIES` (no 64/65
   case). Fix: Method "No test today", add Known issue "the 64-entry cap has no test". Same family:
   SwRS-058 scenario "Case of the stem" is untested (`stemIndex.test.ts` covers the excluded folders
   only): state it in the Method.
3. One-SHALL rule (D19, partly open): SwRS-022 ("SHALL not look up a schema ... and SHALL show the
   generic table"), SwRS-074 ("SHALL not follow it and SHALL open nothing", the same outcome twice)
   and SwRS-084 ("SHALL apply JSON Schema 2020-12 ... and SHALL report all errors") still carry two
   SHALLs. Fix: 022 and 074 become one SHALL (the second half as a criterion); 084 either split
   into two SwRS (2020-12 keywords; all errors reported) or reduced to "SHALL report every
   violation of the 2020-12 schema, not only the first" with the keyword scenario kept.
4. SwRS-072 and SwRS-084: the first `##` heading is not the frontmatter `title` verbatim (072 title
   lacks the final word "click"; 084 title lacks "is reported"). Fix: make title and heading
   identical (shorten the heading or lengthen the title, then `okfreq` regenerates the index).
5. StRS-017 (third bullet) still reads "the document identity (the `id_marker` field value, else the
   file name stem)", which suggests a fallback when `id_marker` names a missing field (D14a asked
   for a rewrite; SwRS-069 is right). Fix StRS-017: "the document identity: the `id_marker` field
   value, or the document's file name stem when the annotation names no `id_marker`; an
   `id_marker` naming a missing field gives no line". SwRS-069 criteria: add that the marker must
   start the line or follow whitespace (`(?:^|\s)` in `markdownMarkerLine`: `xEvidence dd` does not
   match) and that the stem is the document's, not the target's.
6. Open point confirmed (partly uncovered). Dropped from FMSCHEMA-041: "the section is flagged so
   the editor offers no custom key". frontmatter-editing has SwRS-MDOKFSTUDIO-FMEDIT-035 (picker
   offers "Custom key..." when extra properties are allowed) but its scenarios do not include the
   refusal (schema root `additionalProperties: false`: no "Custom key..." option; its boundary
   scenario is "no schema field left"), and nothing states that the table renderer emits
   `data-okf-additional-properties="false"` (`propertiesTable.ts:267`, read in
   `frontmatterMenu.ts:104`; unit tests "T25 ..." in okfFrontmatter and propertiesTable tests).
   Fix: add a third scenario to FMEDIT-035 (schema with `additionalProperties: false` and one
   field left: the select lists the field and no "Custom key..." entry), and add one criterion line
   to FMSCHEMA-041 ("a closed schema also flags the section `data-okf-additional-properties`, which
   the editing picker reads; see FMEDIT-035"), with the T25 tests in its Method.
7. Coverage gap (minor, F-FMSCHEMA-018): the contrast thresholds checked by the visual scenarios
   (title badge 2.5:1, description text 2.2:1, value text 4:1, description smaller than value) are
   in no SwRS (SwRS-010 covers the frame only; no other scope mentions the properties table
   contrast). Fix: add a criterion line and a scenario to SwRS-010 or one page-wide SwRS in
   theme-zoom for the properties table contrast, or record the gap as a Known issue.

Verdict: FIX-REQUIRED

## Re-check 2

Checked in the worktree (`okfreq validate`: 0 errors, 0 warnings) against `fileLinks.ts`, `previewNavigation.ts` (`markdownMarkerLine`), `propertiesTable.ts` (line 267), `frontmatterMenu.ts` (line 104) and the T25 tests.

Re-check 1 defects:

1. SwRS-024 scenario "Standard JSON pointer", its Known issue and StRS-007: fixed (property left without a schema, schema does not compile, red row "Schema validation failed to run: schema is invalid: ..."; no "no longer declared" text left).
2. SwRS-078 (Method "No test today", Known issue "the 64-entry cap has no test") and SwRS-058 (Method says the "Case of the stem" scenario has no test): fixed.
3. One SHALL: 022, 074 and 084 are now one SHALL each; 084 keeps the 2020-12 keywords and the new SwRS-089 holds "every violation is reported" (one SHALL, two scenarios). 088 (generic table when no lookup) split from 022 cleanly. Fixed.
4. Title = first heading for 072 and 084: fixed (both identical to the frontmatter title).
5. StRS-017 now reads "the `id_marker` field value, or the document's file name stem when the annotation names no `id_marker` (an `id_marker` naming a missing field gives no line)"; SwRS-069 has the "Identity field missing" scenario and the criteria on `(?:^|\s)` and on the document's own stem. Matches `markdownMarkerLine` and `fileLinks.ts` lines 372-381. Fixed.
6. "Closed schema" coverage: FMSCHEMA-041 criteria now state the `data-okf-additional-properties="false"` flag, cite the T25 tests in the Method and point to FMEDIT-035; FMEDIT-086 (new) states the flag; FMEDIT-035 has the refusal scenario. See the frontmatter-editing re-check 2 for the cross-check against the code. Fixed.
7. Contrast thresholds: SwRS-010 has a "Contrast" scenario (2.5:1, 2.2:1 and smaller than the value, 4:1) and a Criteria line citing `capture_page_checks.py` (lines 1090-1098 confirm 2.5 and 2.2). Fixed.

Remaining defects: none. (Advisory, outside the requirement files: inventory row F-FMSCHEMA-023 still maps only to FMSCHEMA-041; add FMEDIT-086 and FMEDIT-035 in its last column.)

Verdict: APPROVE
