## Summary

The preview's change column marks lines changed since the last commit with green bars, but the bars gave no detail, and lines that were removed were not shown at all (VS Code's editor gutter shows both). This adds a tooltip on each bar, a red marker where lines were removed, and a click that opens the side-by-side diff card for just that block.

## Deliverables

- Hovering a green bar shows a small tooltip, in the page's tooltip style: `Changed lines 12–14 since last commit` (or `Changed line 12 since last commit`). It appears only over the bar itself, never while Diff is off, and never in edit mode.
- A red marker (the existing side-by-side diff's removed colour, no new palette) sits where lines were removed, between the blocks around them, with the tooltip `Removed lines 12–14 since last commit` (line numbers of the last commit). It follows the same rules as the bars.
- Clicking a bar or a removed marker opens the existing side-by-side diff card for that block or hunk only, in place; a second click or Escape closes it. The global Side-by-side button works as before.

Before/after captures, light and dark: tooltip, removed marker and open card (files `v31` to `v36`, attached to the review).

## Changes

- `src/page/modules/incomingChanges.ts`: tooltip, removed marker, click targets; styles in `commentStyles.ts`.
- Host data of incoming changes gains the pure-removal hunks; the page asks the host once for the baseline when a single card is opened (new page message).
- `sideBySide.ts` reuses the existing card code for a single block.
- Three new requirements (tooltip, removed marker, click to diff) in the review-annotations scope, with markers in code and tests; dated entry in the requirements log.

## Impacts

Visible in the preview only; the Markdown file is never written. No new setting.

## Blast radius

Grade: **2**. The page-to-host protocol gains one message and the incoming-changes payload an optional field, and the side-by-side styles gained a single-card variant; revert is a plain `git revert`.

## Test plan

- [ ] New or changed tests (they fail on the previous code): page unit tests, host test, CSS test, visual scenarios
- [ ] Requirements: SwRS added, markers in code and tests, `just requirements-update`
- [ ] Changelog: one user-facing line under `## Unreleased`
- [ ] Local gates: `just check`, visual render and capture of the review-annotations group
- [ ] Review
- [ ] CI green

## Internal references

CR-463; SwRS-MDOKFSTUDIO-REVIEW-220, -221, -222, derived from StRS-MDOKFSTUDIO-REVIEW-017.
