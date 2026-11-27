# Mark frontmatter rows that carry an error or a warning

Short name: `field-error`. Destination: the running batch batch-09 (stack). Style only: no spec
critic (`02-answers.md`). No tracker issue (verbal origin).

## Goal

In a document whose frontmatter has a schema, a field with a validation error (for example
`status: publshed` against an enum) must be visible in the properties table at a glance, not only
through the small badge in the table title.

- field-error-Q1, answer A ("Comme les infos"): the field **name** in red on a light red
  background, as the whole-document error row already looks, and a **wavy underline under the
  value**. A field with a warning gets the same look in the **warning colour**.
- field-error-Q3, answer A ("Les colorer aussi"): the **whole-document warning rows**
  (`.okf-info-row.okf-warning`, for example "Schema could not be parsed: ...") take the warning
  colour on a light background, as the whole-document error row does in red.

The gap is confirmed (the request asked for that): on `origin/main` the classes are in the DOM but
no rule styles them.

- `src/core/frontmatter/propertiesTable.ts` (`renderPropertiesTable`, the `rows` map) puts the
  worst severity of the field's issues (`SEVERITY_CLASS`: `okf-error`, `okf-warning`, `okf-info`)
  on the `<tr data-okf-field=...>` and on its value cell `<td ... data-okf-value-cell>`; the
  whole-document rows are `<tr class="okf-info-row okf-<severity>">` with one `<th colspan>`.
- `src/core/preview/styles/propertiesStyles.ts` (`PROPERTIES_CSS`) styles only
  `.okf-info-row.okf-error th` (around line 183: `--studio-errorForeground` text on
  `--studio-inputValidation-errorBackground`, `white-space: normal`, `overflow-wrap: anywhere`).
  No selector targets `tr[data-okf-field].okf-error`, `td.okf-error`, `.okf-warning` or
  `.okf-info-row.okf-warning`.
- SwRS-MDOKFSTUDIO-FMSCHEMA-084 S1 (which superseded FMSCHEMA-035, the requirement the intent
  names) already says "both rows are underlined in red": the code does not do it, and no test
  checks it.

## What changes

### 1. Stylesheet: `src/core/preview/styles/propertiesStyles.ts`

Add these rules to `PROPERTIES_CSS`, next to the `.okf-info-row.okf-error th` rule (same
`#sphinx-myst-preview-content [data-okf-properties]` scope, so they rank the same way). The warning
colour is `var(--studio-editorWarning-foreground, #bf8803)`, the token and fallback the frontmatter
editor's warning status uses (`src/core/preview/styles/frontmatterEditorStyles.ts`). Its light
background is written as the admonitions do ("fallback first"), as `code.okf-frontmatter-missing`
does in `src/core/preview/styles/frontmatterValueStyles.ts`: a plain `rgba(191, 136, 3, 0.14)`
line, then `color-mix(in srgb, var(--studio-editorWarning-foreground, #bf8803) 14%, transparent)`.
There is no `inputValidation-warningBackground` theme token in `src/core/preview/themeTokens.ts`;
do not add one.

- **Error field row, name cell:** `tr[data-okf-field].okf-error > th` takes the same colour and
  background as the whole-document error row: `color: var(--studio-errorForeground, #f14c4c)` and
  `background: var(--studio-inputValidation-errorBackground, rgba(235, 80, 80, 0.12))`. Do not copy
  the info row's `white-space` / `overflow-wrap`: the key column keeps its own wrapping and
  ellipsis rules (SwRS-MDOKFSTUDIO-FMSCHEMA-005, long keys).
- **Error field row, value cell:** `tr[data-okf-field] > td.okf-error` gets a wavy underline in
  the error colour: `text-decoration: underline wavy var(--studio-errorForeground, #f14c4c)` (a
  `text-underline-offset` is allowed so the wave does not cut the descenders). The value text keeps
  its own colour.
- **Warning field row, name cell:** `tr[data-okf-field].okf-warning > th` in the warning colour on
  the light warning background.
- **Warning field row, value cell:** `tr[data-okf-field] > td.okf-warning` gets
  `text-decoration: underline wavy var(--studio-editorWarning-foreground, #bf8803)`.
- **Whole-document warning row:** `.okf-info-row.okf-warning th` in the warning colour on the light
  warning background, with the same `white-space: normal` and `overflow-wrap: anywhere` as the
  error row (the message spans every column and wraps). Simplest: one rule with both selectors
  for the wrapping, one per severity for the colours.
- An `okf-info` field row and an `.okf-info-row.okf-info` row are left as they are (not styled).

The file is 566 lines on `origin/main`: it stays under the 800-line limit.

Requirement markers: a CSS template string cannot hold a comment marker, so add to the companion
`src/core/preview/styles/propertiesStyles.markers.ts` two lines (the name after the em dash must
occur as text in the host file, which the new selectors do):

- `// @implements_req SwRS-MDOKFSTUDIO-FMSCHEMA-084 — tr[data-okf-field].okf-error`
- `// @implements_req SwRS-MDOKFSTUDIO-FMSCHEMA-023 — .okf-info-row.okf-warning`

### 2. Requirements

Both requirements are `proposed` (not `approved`): no owner agreement is needed to edit them. Read
`requirements/guidelines/requirements.guidelines.md` and `project.guidelines.md` ("During a
change") first.

`requirements/tiers/swrs/frontmatter-schema/SwRS-MDOKFSTUDIO-FMSCHEMA-084.md`:

- **S1** THEN: say how the row is marked: each of the two rows shows its name in the error colour
  on a light red background and a wavy underline in the error colour under its value; every
  violation is reported (not only the first) and the tooltips keep their texts.
- **S6** THEN: the row `titel` carries the warning (unchanged text) and is shown with its name in
  the warning colour on a light background of that colour and a wavy underline in the warning
  colour under its value; the badge counts one warning.
- **Criteria:** add that an error or warning field row is marked like the whole-document error row
  (name cell in the severity colour on a light background of that colour, wavy underline in that
  colour under the value), that an info-severity field row keeps the plain look, and that the value
  text keeps its colour.
- **Verification notes:** add the new unit test (section 3) and the visual scenarios v32 and v33
  (section 4) as Methods for S1 and S6.
- The known issue "the must NOT have additional properties error is not attached to the field row"
  stays as it is (out of scope).

`requirements/tiers/swrs/frontmatter-schema/SwRS-MDOKFSTUDIO-FMSCHEMA-023.md`:

- **S5** outcome of the first table line: the warning row is shown in the warning colour on a light
  background of that colour, spans every column and wraps its text; the badge counts one warning.
- **Verification notes:** add the new unit test (section 3) and the visual scenarios v34 and v35
  (section 4) as Methods for S5.

For both: do not hand-edit generated fields (`implemented_in_files`, `tested_in_files`, link
blocks); run `just requirements-update` and commit what it writes. Add one dated entry to
`requirements/tiers/log.md` naming both.

### 3. Unit test on the shipped stylesheet

New `test/core/preview/fieldIssueStyles.test.ts` (or tests added to
`test/core/preview/fmtableReq.requirements.test.ts`, which already imports the shipped stylesheet),
reading `PREVIEW_THEME_CSS` from `src/core/preview/previewStyles.ts` as it ships (no copied or
prepared CSS text). It asserts:

- a rule whose selector holds `tr[data-okf-field].okf-error > th` sets `color` with
  `--studio-errorForeground` and `background` with `--studio-inputValidation-errorBackground`;
- a rule whose selector holds `td.okf-error` (under `tr[data-okf-field]`) sets a `text-decoration`
  with `wavy` and `--studio-errorForeground`;
- the same pair for `okf-warning` with `--studio-editorWarning-foreground`, and the warning
  background with a plain `rgba(` fallback before the `color-mix(`;
- a rule whose selector holds `.okf-info-row.okf-warning th` sets `color` with
  `--studio-editorWarning-foreground`, the same warning background (`rgba(` then `color-mix(`), and
  `white-space: normal` with `overflow-wrap: anywhere`;
- every one of these `var(...)` reads carries a fallback value (the token-unset cell of the matrix
  below);
- no rule styles `tr[data-okf-field].okf-info` or `.okf-info-row.okf-info` (info rows stay plain).

Markers in the tests: `@tests_req SwRS-MDOKFSTUDIO-FMSCHEMA-084#S1` on the field error test,
`@tests_req SwRS-MDOKFSTUDIO-FMSCHEMA-084#S6` on the field warning test,
`@tests_req SwRS-MDOKFSTUDIO-FMSCHEMA-023#S5` on the whole-document warning test (at most 3 IDs per
marker block). These tests fail on `origin/main` (no such rule), as the constitution (section 3)
asks.

### 4. Visual scenarios (rendered page, computed style)

These checks read the stylesheet as it ships, rendered by the visual harness at the head under
test. Fixture numbers and scenario numbers are the next free ones on `origin/main` (fixtures 98
and 99; scenarios v32 to v35 of the `frontmatter-schema` group); ids are permanent, so check them
at implementation and take the next free ones if batch-09 used them.

**Field rows.**

- New fixture `test/visual/fixtures/98-field-issue-rows.md`, `type: swrs` against the existing
  `test/visual/fixtures/_schema/swrs.schema.yaml`: every required field present and valid
  (`title`, `owner`, `annotation_exemption: false`), `status: publshed` (enum error, the case of the
  report) and one undeclared field `bonus_field: "not declared in the schema"` (warning with the
  strict setting), then a short heading and paragraph.
- Two new scenarios in `test/visual/scenarioDefinitions2.ts`, next to
  `frontmatter-schema/v21-unknown-field-strict-light-900`, with `render: { strictAdditionalProperties:
  true as const }`, `...WIDE`, `scroll: { kind: "top" }`:
  `frontmatter-schema/v32-field-issue-rows-light-900` (theme `light`) and
  `frontmatter-schema/v33-field-issue-rows-dark-900` (theme `dark`). Each carries
  `// @tests_req SwRS-MDOKFSTUDIO-FMSCHEMA-084#S1` and `#S6`, and a description.
- Their assertion list (new constant in `test/visual/scenarioAssertions.ts`, `ContentAssertion`
  of `test/visual/scenarios.ts`):
  - the badge reads one error and one warning (`data-okf-errors="1"`, `data-okf-warnings="1"`);
  - `[data-okf-properties] tr[data-okf-field="status"].okf-error > td.okf-error`:
    `css: { textDecorationLine: "underline", textDecorationStyle: "wavy" }`;
  - the same on `tr[data-okf-field="bonus_field"].okf-warning > td.okf-warning`;
  - an `expr` on `tr[data-okf-field="status"] > th`: computed `color` and `backgroundColor` are
    red (red channel above 1.25 times green and blue, background alpha not 0), the heuristic of
    `check_okf_schema_rendering` in `test/visual/capture_page_checks.py` for the info row;
  - an `expr` on `tr[data-okf-field="bonus_field"] > th`: computed `color` and `backgroundColor`
    are of the warning hue (blue channel below 0.6 times red and green, background alpha not 0);
  - an `expr`: the underline colour (`textDecorationColor`) of each marked value cell equals the
    computed `color` of its name cell (the same severity colour);
  - a valid field row (`tr[data-okf-field="title"]`) has a transparent name-cell background and
    `textDecorationLine` `none` on its value cell.

**Whole-document warning row.**

- New schema file `test/visual/fixtures/_schema/unparsable.schema.json5` holding a small object
  schema with a trailing comma after its last property (FMSCHEMA-023 S5, second table line: minimal
  JSON5 support fails on it), and new fixture `test/visual/fixtures/99-unparsable-schema.md` with
  `type: unparsable` and two or three plain fields, then a short heading and paragraph. Before
  adding the schema file, check that no existing scenario or test lists every schema of
  `test/visual/fixtures/_schema/` (for example a type suggestion list); if one does, add the new
  type to its expected list in the same change and say so in the PR (an added item, not a changed
  intent).
- Two new scenarios next to the field-row ones, `...WIDE`, `scroll: { kind: "top" }`:
  `frontmatter-schema/v34-schema-warning-row-light-900` (theme `light`) and
  `frontmatter-schema/v35-schema-warning-row-dark-900` (theme `dark`), each with
  `// @tests_req SwRS-MDOKFSTUDIO-FMSCHEMA-023#S5` and a description.
- Their assertion list:
  - one `[data-okf-properties] tr.okf-info-row.okf-warning` whose text starts with
    "Schema could not be parsed:"; the badge reads one warning (`data-okf-warnings="1"`);
  - an `expr` on its `th`: computed `color` and `backgroundColor` of the warning hue (same
    heuristic as above, background alpha not 0);
  - an `expr`: the `th` spans every visible column (`colSpan` equals the visible `thead th` count),
    its width equals the table's within 2 px, and its text does not overflow
    (`scrollWidth <= clientWidth + 1`), as `check_okf_schema_rendering` checks for the error row.

**Ids and pictures.** `test/visual/scenarioIds.ts`: a `LOCKS_BY_ID` line per new id (v32 to v35),
one present-tense sentence naming only what the assertions check. The four scenarios keep their
screenshot (not in `ASSERTION_ONLY_IDS`): the picture is the evidence the owner looks at.

### 5. CHANGELOG

One `## Unreleased` line in `CHANGELOG.md`, as `.agents/guidelines/pull-request.guidelines.md`
("CHANGELOG line") says, for example: "A frontmatter field with a schema error now shows its name
in red on a light red background and a wavy red underline under its value; a field with a warning
shows the same in the warning colour, and a whole-table warning row (such as "Schema could not be
parsed") now shows in the warning colour too (CR-<n> field-error, PR #<n>)". Commit type `fix`.

## Host and default matrix

The colours come from theme tokens, mapped from VS Code in the editor and absent where no token is
set; the look depends on that, not on a setting.

| Cell | Evidence |
| --- | --- |
| Tokens set, light theme | visual scenarios v32 (field rows) and v34 (whole-document warning row): computed styles and screenshots |
| Tokens set, dark theme | visual scenarios v33 and v35: computed styles and screenshots |
| Tokens unset (fallback values) | unit test of section 3: every new `var(...)` has a fallback, the warning background has a plain `rgba` line before `color-mix` |

## Out of scope

- The title badge's own look (it stays as it is; the intent mentions it only as the current sole
  signal).
- Info-severity rows, field (`tr[data-okf-field].okf-info`) and whole-document
  (`.okf-info-row.okf-info`): unchanged.
- The whole-document error row: its look is unchanged (it is the model of this change).
- The validation itself, the messages, the tooltips, the badge counts and the issue highlight
  outline (`data-okf-issue-highlight`): unchanged.
- The undeclared field of a closed schema (`additionalProperties: false`): its error stays at the
  document root, as FMSCHEMA-084's known issue says.
- FMSCHEMA-023's known issues (minimal JSON5 support, YAML syntax errors not reported): unchanged;
  the new visual fixture relies on the first one as it behaves today.
- The writing skill: no rendered syntax changes, so `skills/writing-for-markdown-okf-schema-studio/`
  is not touched.

## Evidence

- `just check` (TypeScript, file size, marker companions, unit tests including section 3).
- `just ci-visual` (or the visual stage of `just preflight`): scenarios v32 to v35 pass their
  assertions. In the screenshots, the status row is red with the wavy underline, the bonus_field row
  is in the warning colour, and the "Schema could not be parsed" row is in the warning colour across
  the table.
- `just requirements-update`, then `uv run --no-sync --group requirements okfreq validate
  --check-links --project-root .` clean; FMSCHEMA-084 and FMSCHEMA-023 list the new test files.
- `just preflight` passes (on Windows the static stage; CI runs the others).
- Scenario to walk in the editor (PR screenshots):
  1. Open a document of a bundle with a schema and set `status: publshed` against an enum: the
     status row shows its name in red on a light red background and a wavy red underline under
     `publshed`.
  2. With `markdownOkfSchemaStudio.frontmatter.strictAdditionalProperties` on and an undeclared
     field, that row shows the same in the warning colour.
  3. Fix the value and remove the field: both marks go.
  4. Give a document a type whose `.schema.json5` has a trailing comma: the "Schema could not be
     parsed" row shows in the warning colour on a light background across the table.

## Open questions

None. The question on whole-document warning rows is answered (field-error-Q3, answer A) and
folded in above.
