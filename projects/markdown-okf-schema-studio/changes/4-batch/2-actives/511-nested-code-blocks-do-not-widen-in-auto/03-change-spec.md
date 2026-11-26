# Requirements: only top-level blocks widen in Auto

Short name: `nested-wide`. Destination: running batch batch-09 (stack). No tracker issue.

## Goal

In Auto width mode, a code block (or a table, figure, image or Mermaid diagram) inside a list
item, admonition, block quote, tab set, dropdown or card does not widen: it keeps the layout it has
in Margin, with its scroll bar. The owner decided this stays (answer 1): the requirements must
state it as the rule ("only top-level blocks widen") instead of carrying it as a Known issue.
Widening nested blocks would be a later, separate request with its own specification.

What the user sees does not change. No file under `src/` changes.

## Decisions carried from `02-answers.md`

- Answer 1 (nested-wide-Q1): the specification encodes that only top-level elements widen in
  Auto; changing that later needs a new specification. Carried in "What changes", item 1.
- Answer 2 (Q2): not applicable; nothing to carry.
- Answer 3 (Q3): "not yet", given on a restatement that widened nested blocks; replaced by
  answer 1. Nothing of the widening design of `intake/request.md` is carried.
- Answer 4 (Q4): grilled enough on the requirements-only restatement; this CR goes to batch-09.
- Header answers: the CR joins the running batch-09 stack and ships in the next release with the
  other three inbox anomalies.
- Spec critic: none (requirements wording only).

## Current state (origin/main)

- `requirements/tiers/swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-023.md` ("Auto width lets wide
  blocks break out of the column", `proposed`, scenarios S1 to S8):
  - The normative statement and `description:` say "a table, figure, image, code block or Mermaid
    diagram that is wider than the text column" with no restriction to top-level blocks.
  - Scenario S8 ends with the row `| A code block inside a list item, wider than the item | Not
    marked; scrolls inside the item (Known issue) |`.
  - `### Known issues` holds the line "Known issue: Only top-level blocks, or the paragraph holding
    only an image, break out; a code block in a list item, admonition, block quote, tab set or card
    scrolls inside it."
- The code already does this: `wrapperOf` in `src/page/modules/widthMode.ts` returns an element
  only when its parent is `#content`, or for an `IMG` whose parent `P` (with no text) is a child of
  `#content`; `eligibleWrappers` skips every other candidate (`table, figure, img, pre,
  .myst-mermaid-diagram`).
- Tests that check the nested case today, both tagged `@tests_req SwRS-MDOKFSTUDIO-LAYOUT-023#S8`:
  - `test/page/runtimePageControls.test.ts`: `T10b: a code block inside a list item is not
    measured` (fake DOM, the `codeColumn()` helper).
  - `test/page/codeBlockBreakout.test.ts`: the six `checkCell` tests (real Chromium, rendered page,
    shipped stylesheet) check the `listed` kind: "a code block in a list item is marked" /
    "no longer scrolls as in Margin" fail the test, and `listed scrolls` must be seen.
- `StRS-MDOKFSTUDIO-LAYOUT-003` (the parent StRS) is `approved`; it is not touched (see "Out of
  scope").

## What changes

### 1. SwRS-MDOKFSTUDIO-LAYOUT-023 states the top-level rule

In `requirements/tiers/swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-023.md`:

- Normative statement and `description:` (kept identical, as okfreq requires): restrict the widened
  element to a top-level one. Wording to use, adjusting only the line wrapping of the frontmatter:
  "When the width mode is Auto, the extension SHALL widen a top-level table, figure, image, code
  block or Mermaid diagram (a direct child of the page content, or an image alone in a top-level
  paragraph) that is wider than the text column to the width it needs (a code block until its
  longest line fits, its border and a caption bar included, so that it scrolls only beyond the
  available area), up to the available area, centred on that area, measuring it again whenever the
  layout may have changed; a block nested in a list item, admonition, block quote, tab set,
  dropdown or card keeps the layout it has in Margin."
- New scenario `### Scenario S9 (refusal): Nested blocks keep their Margin layout`, appended after
  S8 and declared in the frontmatter `scenarios:` as `- id: S9` / `title: Nested blocks keep their
  Margin layout`. A table, in the S4 style:

  | Input | Outcome |
  | --- | --- |
  | Auto, a code block inside a list item, wider than the item | Neither the block, the item nor the list is marked wide or shifted; the block scrolls inside the item as in Margin |
  | Auto, a wide table inside an admonition | Neither the table nor the admonition is marked wide |
  | Auto, a wide image alone in a paragraph inside a block quote | Neither the image, the paragraph nor the block quote is marked wide |
  | Auto, a wide code block inside a card or a tab panel | Not marked wide |

- Scenario S8: remove its last row (the list-item row, now in S9). S8 keeps its title and its other
  rows unchanged.
- `### Known issues`: remove the "Only top-level blocks ... scrolls inside it." line. The other two
  Known issues stay.
- `### Verification notes`:
  - In the `runtimePageControls.test.ts` "A code block fits its longest line" method line, move
    `T10b: a code block inside a list item is not measured` out to a new method line for S9, with
    the new unit test of item 2.
  - In the `codeBlockBreakout.test.ts` method line, say that the list-item blocks check S9.
  - In `Criteria`, after "for a code block (a top-level `pre`, or a `figure` whose direct child is
    a `pre`)", add that only a direct child of the content, or an image alone in a top-level
    paragraph, is ever measured; a nested element and its containers are never marked.
- `req_lifecycle` stays `proposed`. No new requirement ID; no requirement is superseded.

### 2. Markers and one unit test

- `test/page/runtimePageControls.test.ts`:
  - `T10b: a code block inside a list item is not measured`: its marker becomes
    `@tests_req SwRS-MDOKFSTUDIO-LAYOUT-023#S9` (S8 no longer holds the list-item row).
  - Add one test after it, `T10b: a wide block nested in a container is not measured`, tagged
    `@tests_req SwRS-MDOKFSTUDIO-LAYOUT-023#S9`, using the existing `codeColumn()` helper (its
    `make(tag, box, scrollWidth, parent)` and `code(...)`), in a 700 px column: a `table` 900 px
    wide inside a container element standing for an admonition, an `img` 900 px wide alone in a `p`
    inside a `blockquote`, and a `pre` 900 px wide inside a container standing for a card. After
    the Width button click (Auto), no element of the three groups (the block, its paragraph if any,
    its container) has `data-sphinx-preview-wide`, and none has a breakout. The test fakes the
    containers by tag (the harness does not render directives); it checks the rule of `wrapperOf`,
    which keys on the parent, not on the container's class.
- `test/page/codeBlockBreakout.test.ts`: each of the six `checkCell` tests that sees `listed
  scrolls` gets a second marker line `@tests_req SwRS-MDOKFSTUDIO-LAYOUT-023#S9` under its `#S8`
  line (one ID per line, as the marker rules ask). No assertion changes. The file header comment
  already describes the list-item case and needs no change.
- No `@implements_req` changes: `wrapperOf` / `eligibleWrappers` in `src/page/modules/widthMode.ts`
  already sit under `@implements_req SwRS-MDOKFSTUDIO-LAYOUT-023`; `src/` is not touched.

### 3. Generated files and log

- Run `just requirements-update` and commit what it regenerates (indexes, links, coverage).
- Add a dated entry at the top of `requirements/tiers/log.md` (under the date the change is made,
  heading naming the CR), in the style of the CR-508 entry: "Changed (`proposed`):
  SwRS-MDOKFSTUDIO-LAYOUT-023: the normative text states that only a top-level block, or an image
  alone in a top-level paragraph, widens in Auto, and a nested block keeps its Margin layout (new
  scenario S9; the list-item row moves from S8 to S9; the Known issue is removed). Reason: the
  owner decided nested blocks stay in their container; widening them would be a new
  specification. No behaviour change."

### 4. Changelog

No user-visible change, so no CHANGELOG entry and no release note line. (If the project's
changelog rule asks for an entry for a requirements-only change, the Driver follows that rule.)

## Out of scope

- Any change under `src/` or the stylesheet: no nested block widens; no change to `wrapperOf`,
  `eligibleWrappers`, the `#content > [wide]` CSS rule, `.myst-grid-card` clipping, the export or
  the overlays (the design points of `intake/request.md` are not carried, answer 1).
- `StRS-MDOKFSTUDIO-LAYOUT-003` (approved): its text is not changed, so no re-approval is needed.
  Its rationale ("In Auto, a table, figure, image, code block or Mermaid diagram wider than the
  column uses the available width") stays as is; the SwRS refines it.
- The deprecated `StRS-MDOKFSTUDIO-LAYOUT-007` and `SwRS-MDOKFSTUDIO-DIAG-021`: untouched.
- `SwRS-MDOKFSTUDIO-LAYOUT-044` (Auto tables that fit) and `SwRS-MDOKFSTUDIO-LAYOUT-022` /
  `LAYOUT-030` (figure mark Known issue): untouched.
- A real-browser check of nested blocks in admonitions, tabs, dropdowns or cards
  (`codeBlockBreakout.test.ts` covers the list item only): not added.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/`: no rendered syntax changes.

## Evidence

No host or default matrix: the rule does not depend on the host or on a setting value.

1. `uv run --no-sync --group requirements okfreq validate --check-links --project-root .` passes
   (the `description:` equals the normative statement; S9 is declared and has its heading).
2. `just check-markers` (in `just check`) passes: every `#S9` fragment names a declared scenario,
   and S8 and S9 both keep at least one `@tests_req`.
3. `just requirements-update` leaves no diff after its output is committed; the coverage report
   lists `SwRS-MDOKFSTUDIO-LAYOUT-023#S9` with `test/page/runtimePageControls.test.ts` and
   `test/page/codeBlockBreakout.test.ts`.
4. The new unit test `T10b: a wide block nested in a container is not measured` passes, and fails
   when `wrapperOf` is changed to accept any element (shown once by the Driver locally, then
   reverted; noted in the PR body's Tests section).
5. `test/page/codeBlockBreakout.test.ts` passes unchanged in its assertions (it reads the shipped
   stylesheet and the page runtime built from `src/` at the head under test).
6. `git diff origin/main --stat -- src/` is empty.
7. `just preflight` passes (on Windows its static stage; CI runs the others).
8. The PR body's Tests section names SwRS-MDOKFSTUDIO-LAYOUT-023 (changed, scenario S9 added) with
   its source file `src/page/modules/widthMode.ts` and its test files.

## Open questions

None.
