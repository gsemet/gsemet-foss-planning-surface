# Mark frontmatter field rows that carry an error or a warning

Short name: `field-error`. Destination: the running batch batch-09 (stack). Style only: no spec
critic (`02-answers.md`). No tracker issue (verbal origin).

## Goal

In a document whose frontmatter has a schema, a field with a validation error (for example
`status: publshed` against an enum) must be visible in the properties table at a glance, not only
through the small badge in the table title. The owner chose (field-error-Q1, answer A, "Comme les
infos"): the field **name** in red on a light red background, as the whole-document information
rows already look, and a **wavy underline under the value**. A field with a warning gets the same
look in the **warning colour**.

The gap is confirmed (the request asked for that): on `origin/main` the field row carries the
class but no rule styles it.

- `src/core/frontmatter/propertiesTable.ts` (`renderPropertiesTable`, the `rows` map) puts the
  worst severity of the field's issues (`SEVERITY_CLASS`: `okf-error`, `okf-warning`, `okf-info`)
  on the `<tr data-okf-field=...>` and on its value cell `<td ... data-okf-value-cell>`.
- `src/core/preview/styles/propertiesStyles.ts` (`PROPERTIES_CSS`) styles only
  `.okf-info-row.okf-error th` (around line 183: `--studio-errorForeground` text on
  `--studio-inputValidation-errorBackground`). No selector targets `tr[data-okf-field].okf-error`,
  `.okf-warning` or `td.okf-error`.
- SwRS-MDOKFSTUDIO-FMSCHEMA-084 S1 (which superseded FMSCHEMA-035, the requirement the intent
  names) already says "both rows are underlined in red": the code does not do it, and no test checks
  it.

## What changes

### 1. Stylesheet: `src/core/preview/styles/propertiesStyles.ts`

Add these rules to `PROPERTIES_CSS`, next to the `.okf-info-row.okf-error th` rule (same
`#sphinx-myst-preview-content [data-okf-properties]` scope, so they rank the same way):

- **Error field row, name cell:** `tr[data-okf-field].okf-error > th` takes the same colour and
  background as the error information row: `color: var(--studio-errorForeground, #f14c4c)` and
  `background: var(--studio-inputValidation-errorBackground, rgba(235, 80, 80, 0.12))`. Do not copy
  the info row's `white-space: normal` / `overflow-wrap: anywhere`: the key column keeps its own
  wrapping and ellipsis rules (SwRS-MDOKFSTUDIO-FMSCHEMA-005, long keys).
- **Error field row, value cell:** `tr[data-okf-field] > td.okf-error` gets a wavy underline in
  the error colour: `text-decoration: underline wavy var(--studio-errorForeground, #f14c4c)` (an
  offset with `text-underline-offset` is allowed so the wave does not cut the descenders). The value
  text keeps its own colour.
- **Warning field row, name cell:** `tr[data-okf-field].okf-warning > th` in the warning colour,
  `color: var(--studio-editorWarning-foreground, #bf8803)` (the token and fallback the frontmatter
  editor's warning status uses, `src/core/preview/styles/frontmatterEditorStyles.ts`), on a light
  background of the same colour (as `code.okf-frontmatter-missing` does in
  `src/core/preview/styles/frontmatterValueStyles.ts`). There is no
  `inputValidation-warningBackground` theme token in `src/core/preview/themeTokens.ts`; do not add
  one. Write the background as the admonitions do ("fallback first"): a plain
  `rgba(191, 136, 3, 0.14)` line, then
  `color-mix(in srgb, var(--studio-editorWarning-foreground, #bf8803) 14%, transparent)`.
- **Warning field row, value cell:** `tr[data-okf-field] > td.okf-warning` gets
  `text-decoration: underline wavy var(--studio-editorWarning-foreground, #bf8803)`.
- An `okf-info` field row is left as it is (not styled).

The file is 566 lines on `origin/main`: it stays under the 800-line limit.

Requirement marker: a CSS template string cannot hold a comment marker, so add to the companion
`src/core/preview/styles/propertiesStyles.markers.ts` one line
`// @implements_req SwRS-MDOKFSTUDIO-FMSCHEMA-084 — tr[data-okf-field].okf-error` (the name after
the em dash must occur as text in the host file, which the new selector does).

### 2. Requirement: `requirements/tiers/swrs/frontmatter-schema/SwRS-MDOKFSTUDIO-FMSCHEMA-084.md`

FMSCHEMA-084 is `proposed` (not `approved`): no owner agreement is needed to edit it. Read
`requirements/guidelines/requirements.guidelines.md` and `project.guidelines.md` ("During a
change") first.

- **S1** THEN: say how the row is marked: each of the two rows shows its name in the error colour
  on a light red background and a wavy underline in the error colour under its value; every
  violation is reported (not only the first) and the tooltips keep their texts.
- **S6** THEN: the row `titel` carries the warning (unchanged text) and is shown with its name in
  the warning colour on a light background of that colour and a wavy underline in the warning
  colour under its value; the badge counts one warning.
- **Criteria:** add that an error or warning field row is marked like the error information row
  (name cell coloured on a light background of the severity colour, wavy underline under the
  value), that an info-severity field row keeps the plain look, and that the value text keeps its
  colour.
- **Verification notes:** add the new unit test (section 3) and the new visual scenarios
  (section 4) as Methods for S1 and S6.
- Do not hand-edit generated fields (`implemented_in_files`, `tested_in_files`, link blocks):
  run `just requirements-update` and commit what it writes. Add a dated entry to
  `requirements/tiers/log.md`.
- The known issue "the must NOT have additional properties error is not attached to the field row"
  stays as it is (out of scope).

### 3. Unit test on the shipped stylesheet

New `test/core/preview/fieldIssueStyles.test.ts` (or a test added to
`test/core/preview/fmtableReq.requirements.test.ts`, which already imports the shipped stylesheet),
reading `PREVIEW_THEME_CSS` from `src/core/preview/previewStyles.ts` as it ships (no copied or
prepared CSS text). It asserts:

- a rule whose selector holds `tr[data-okf-field].okf-error > th` sets `color` with
  `--studio-errorForeground` and `background` with `--studio-inputValidation-errorBackground`;
- a rule whose selector holds `td.okf-error` (under `tr[data-okf-field]`) sets a `text-decoration`
  with `wavy` and `--studio-errorForeground`;
- the same pair for `okf-warning` with `--studio-editorWarning-foreground`, and the warning
  background with a plain `rgba(` fallback before the `color-mix(`;
- every one of these `var(...)` reads carries a fallback value (the token-unset cell of the matrix
  below);
- no rule styles `tr[data-okf-field].okf-info` (info rows stay plain).

Markers in the test: `@tests_req SwRS-MDOKFSTUDIO-FMSCHEMA-084#S1` on the error test and
`@tests_req SwRS-MDOKFSTUDIO-FMSCHEMA-084#S6` on the warning test. This test fails on
`origin/main` (no such rule), as the constitution (section 3) asks.

### 4. Visual scenarios (rendered page, computed style)

- New fixture `test/visual/fixtures/98-field-issue-rows.md` (98 is the next free number on
  `origin/main`; take the next free one if batch-09 used it), `type: swrs` against the existing
  `test/visual/fixtures/_schema/swrs.schema.yaml`: every required field present and valid
  (`title`, `owner`, `annotation_exemption: false`), `status: publshed` (enum error, the case of the
  report) and one undeclared field `bonus_field: "not declared in the schema"` (warning with the
  strict setting), then a short heading and paragraph.
- Two new scenarios in `test/visual/scenarioDefinitions2.ts`, next to
  `frontmatter-schema/v21-unknown-field-strict-light-900`, with `render: { strictAdditionalProperties:
  true as const }`, `...WIDE`, `scroll: { kind: "top" }`, taking the next free numbers of the group
  (`v32`, `v33` on `origin/main`; ids are permanent, check at implementation):
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
  - an `expr`: the underline colour (`textDecorationColor`) of the status value cell equals the
    computed `color` of its name cell, and likewise for bonus_field (the same severity colour);
  - a valid field row (`tr[data-okf-field="title"]`) has a transparent name-cell background and
    `textDecorationLine` `none` on its value cell.
- `test/visual/scenarioIds.ts`: a `LOCKS_BY_ID` line per new id, one present-tense sentence naming
  only what the assertions check. The scenarios keep their screenshot (not in
  `ASSERTION_ONLY_IDS`): the picture is the evidence the owner looks at.

These checks read the stylesheet as it ships, rendered by the visual harness at the head under
test.

### 5. CHANGELOG

One `## Unreleased` line in `CHANGELOG.md`, as `.agents/guidelines/pull-request.guidelines.md`
("CHANGELOG line") says, for example: "A frontmatter field with a schema error now shows its name
in red on a light red background and a wavy red underline under its value; a field with a warning
shows the same in the warning colour (CR-<n> field-error, PR #<n>)". Commit type `fix`.

## Host and default matrix

The colours come from theme tokens, mapped from VS Code in the editor and absent where no token is
set; the look depends on that, not on a setting.

| Cell | Evidence |
| --- | --- |
| Tokens set, light theme | visual scenario `v32-field-issue-rows-light-900` (computed styles and screenshot) |
| Tokens set, dark theme | visual scenario `v33-field-issue-rows-dark-900` (computed styles and screenshot) |
| Tokens unset (fallback values) | unit test of section 3: every new `var(...)` has a fallback, the warning background has a plain `rgba` line before `color-mix` |

## Out of scope

- The title badge's own look (it stays as it is; the intent mentions it only as the current sole
  signal).
- Info-severity field rows (`tr[data-okf-field].okf-info`): unchanged.
- Whole-document warning and info rows (`.okf-info-row.okf-warning`, `.okf-info-row.okf-info`):
  unchanged (see the open question).
- The validation itself, the messages, the tooltips, the badge counts and the issue highlight
  outline (`data-okf-issue-highlight`): unchanged.
- The undeclared field of a closed schema (`additionalProperties: false`): its error stays at the
  document root, as FMSCHEMA-084's known issue says.
- The writing skill: no rendered syntax changes, so `skills/writing-for-markdown-okf-schema-studio/`
  is not touched.

## Evidence

- `just check` (TypeScript, file size, marker companions, unit tests including section 3).
- `just ci-visual` (or the visual stage of `just preflight`): scenarios v32 and v33 pass their
  assertions; their screenshots show the status row red with the wavy underline and the
  bonus_field row in the warning colour.
- `just requirements-update`, then `uv run --no-sync --group requirements okfreq validate
  --check-links --project-root .` clean; FMSCHEMA-084 lists the new test files.
- `just preflight` passes (on Windows the static stage; CI runs the others).
- Scenario to walk in the editor (PR screenshot): open a document of a bundle with a schema, set
  `status: publshed` against an enum; the status row shows its name in red on a light red
  background and a wavy red underline under `publshed`. With
  `markdownOkfSchemaStudio.frontmatter.strictAdditionalProperties` on and an undeclared field, that
  row shows the same in the warning colour. Fix the value: both marks go.

## Open questions

1. Whole-document warning rows (`.okf-info-row.okf-warning`, for example "Schema could not be
   parsed") have no style on `origin/main` either. After this change a field warning is coloured
   while a whole-document warning is not. Should this CR also give them the warning colour on a
   light background, or stay with the field rows only (as specified)?
