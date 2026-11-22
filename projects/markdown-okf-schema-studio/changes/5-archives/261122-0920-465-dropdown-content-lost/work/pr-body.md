## Summary

A MyST dropdown written as a directive (`:::{dropdown} Title`, colon or backtick fence) rendered as an empty, unmapped `<details></details>` in the side preview: its body was lost, so it could not be read, edited or commented. The body now renders, mapped to its source lines like any other block.

## Deliverables

A dropdown directive now renders as the same dropdown the admonition form (`:class: dropdown`) already produced:

| Source | Before | After |
| --- | --- | --- |
| `:::{dropdown} Title` + body | empty `<details>`, no line mapping | `<details class="admonition dropdown">` with title summary and body, `data-line` / `data-end-line` set |
| `:open:` | lost | opens by default |
| no title | lost | title "Details" |

The source is never rewritten. Screenshots at 18a2ea9 (before is the base, drawn without the Sphinx admonition CSS):

| | Light | Dark |
| --- | --- | --- |
| Before | ![before, light](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/edabe18c1a682a832369d8132edd5777e8434fdf/before-light.png) | ![before, dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/edabe18c1a682a832369d8132edd5777e8434fdf/before-dark.png) |
| After | ![after, light](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/edabe18c1a682a832369d8132edd5777e8434fdf/after-light.png) | ![after, dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/edabe18c1a682a832369d8132edd5777e8434fdf/after-dark.png) |

## Blast radius

Grade: **1**: one new normalizer rule for the `details` node and a range fallback; `{admonition}` with `:class: dropdown` is untouched. `git revert` restores the previous behaviour.

## Autonomous decisions

- Reused the admonition dropdown rendering (classes, title style, block mapping) instead of new styles, so blank-run and line-marker features apply unchanged.
- Added the default title "Details" for an untitled dropdown.
- Added two missing `CHANGELOG.md` lines (PR #475, #469) in their own commit, as requested.

## Known gaps

- No visual fixture baseline was added; a simulated-window page test covers the dropdown opening and its line marker. HTML export was not run separately (same `details` element as the admonition dropdown).

<details>
<summary>Details</summary>

## Changes

- `src/core/render/mystNormalize.ts`: new rule for the `details` node of the dropdown directive (admonition classes, summary as title, body kept, `open` only with `:open:`, source position properties).
- `src/core/render/mystBlockTransforms.ts`: a bare `details` node takes the range of its directive.
- `test/page/runtimeLineMarkerPlacement.test.ts`: real render of a dropdown directive, then a simulated window reveals a body line: the dropdown opens and one marker is drawn.
- `test/core/render/mystFeatures.test.ts`: colon fence, backtick fence with `:open:`, untitled, body text and line mapping.
- Requirements: SwRS-MDOKFSTUDIO-MYST-006 extended, log entry; writing skill note; `CHANGELOG.md` lines.

## Impacts

Dropdown content is visible and mapped in the preview; no other visual change. Before: three empty `<details>`; after: a closed, an `:open:` and an untitled dropdown with their bodies (see Deliverables).

## Test plan

- [x] New or changed tests (they fail on the previous code), pass at 18a2ea9
- [x] Requirements: SwRS-MDOKFSTUDIO-MYST-006 updated, markers in code and tests, `just requirements-update`
- [x] Changelog: one line under `## Unreleased`
- [x] Local gates: `just check` and `just preflight` pass at 18a2ea9
- [x] Review: approved at 4a1ced2 (the later commit only adds the PR number to the changelog line)
- [x] CI green: PR checks and the heavy run at 18a2ea9

## Internal references

CR-465.

</details>
