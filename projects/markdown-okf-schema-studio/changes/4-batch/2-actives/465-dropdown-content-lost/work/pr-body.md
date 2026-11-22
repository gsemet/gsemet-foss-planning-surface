## Summary

A MyST dropdown written as a directive (`:::{dropdown} Title`, colon or backtick fence) rendered as an empty, unmapped `<details></details>` in the side preview: its body was lost, so it could not be read, edited or commented. The body now renders, mapped to its source lines like any other block.

## Deliverables

A dropdown directive now renders as the same dropdown the admonition form (`:class: dropdown`) already produced:

| Source | Before | After |
| --- | --- | --- |
| `:::{dropdown} Title` + body | empty `<details>`, no line mapping | `<details class="admonition dropdown">` with title summary and body, `data-line` / `data-end-line` set |
| `:open:` | lost | opens by default |
| no title | lost | title "Details" |

The source is never rewritten. Screenshots before/after: **UNVERIFIED:** not captured yet.

## Blast radius

Grade: **1**: one new normalizer rule for the `details` node and a range fallback; `{admonition}` with `:class: dropdown` is untouched. `git revert` restores the previous behaviour.

## Autonomous decisions

- Reused the admonition dropdown rendering (classes, title style, block mapping) instead of new styles, so blank-run and line-marker features apply unchanged.
- Added the default title "Details" for an untitled dropdown.
- Added two missing `CHANGELOG.md` lines (PR #475, #469) in a separate commit, as requested.

## Known gaps

- No simulated-window or visual fixture was added for this change (unit tests cover the rendering and the mapping).

<details>
<summary>Details</summary>

## Changes

- `src/core/render/mystNormalize.ts`: new rule for the `details` node of the dropdown directive (admonition classes, summary as title, body kept, `open` only with `:open:`, source position properties).
- `src/core/render/mystBlockTransforms.ts`: a bare `details` node takes the range of its directive.
- `test/core/render/mystFeatures.test.ts`: colon fence, backtick fence with `:open:`, untitled, body text and line mapping.
- Requirements: SwRS-MDOKFSTUDIO-MYST-006 extended, log entry; writing skill note; `CHANGELOG.md` lines.

## Impacts

Dropdown content is visible and mapped in the preview; no other visual change.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Requirements: SwRS-MDOKFSTUDIO-MYST-006 updated, markers in code and tests, `just requirements-update`
- [ ] Changelog: one line under `## Unreleased`
- [ ] Local gates: `just check` pass, mystFeatures unit test 47/47
- [ ] Review
- [ ] CI green

## Internal references

CR-465.

</details>
