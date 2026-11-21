## Summary

The preview's change column marks lines changed since the last commit with green bars, but the bars gave no detail, and lines that were removed were not shown at all (VS Code's editor gutter shows both). This adds a tooltip on each bar, a red marker where lines were removed, and a click that opens the side-by-side diff card for just that block.

## Deliverables

- Hovering a green bar shows a small tooltip, in the page's tooltip style: `Changed lines 12–14 since last commit` (or `Changed line 12 since last commit`). It appears only over the bar itself, never while Diff is off, and never in edit mode.
- A red marker (the existing side-by-side diff's removed colour, no new palette) sits where lines were removed, between the blocks around them, with the tooltip `Removed lines 12–14 since last commit` (line numbers of the last commit). It follows the same rules as the bars.
- Clicking a bar or a removed marker opens the existing side-by-side diff card for that block or hunk only, in place; a second click or Escape closes it. The global Side-by-side button works as before.

These are new in this change, so there is no before capture (the base shows no tooltip, no marker and no card). After, light then dark:

![Bar tooltip, light](./v31-change-bar-tooltip-light-900.png)
![Bar tooltip, dark](./v32-change-bar-tooltip-dark-900.png)
![Removed marker, light](./v33-removed-marker-light-900.png)
![Removed marker, dark](./v34-removed-marker-dark-900.png)
![Single-block card, light](./v35-change-bar-card-light-900.png)
![Single-block card, dark](./v36-change-bar-card-dark-900.png)

## Changes

- `src/page/modules/incomingChanges.ts`: tooltip, removed marker, click targets; styles in `commentStyles.ts`.
- Host data of incoming changes gains the pure-removal hunks; the page asks the host once for the baseline when a single card is opened (new page message).
- `sideBySide.ts` reuses the existing card code for a single block.
- Three new requirements (tooltip, removed marker, click to diff) in the review-annotations scope, with markers in code and tests; dated entry in the requirements log.

## Impacts

Visible in the preview only; the Markdown file is never written. No new setting.

## Blast radius

Grade: **2**. The page-to-host protocol gains one message and the incoming-changes payload an optional field, and the side-by-side styles gained a single-card variant; revert is a plain `git revert`.

## Known gaps

- The real VS Code window behaviour of the bars, marker and card is not proved: the heavy integration run fails at an existing step (diff-preview-scroll, a timeout) that fails the same way on main.

## Test plan

- [x] New or changed tests (they fail on the previous code): page unit tests, host test, CSS test, visual scenarios
- [x] Requirements: SwRS added, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased`
- [x] Local gates at 1dd3e76: `just preflight` (static stage on Windows) pass
- [x] Review: inspector approved at 1dd3e76 (carried), verifier VERIFIED at 1dd3e76
- [x] CI green: gh pr checks 474 at 1dd3e76: static, static-windows, viewer-graph, visual pass

## Internal references

CR-463; SwRS-MDOKFSTUDIO-REVIEW-220, -221, -222, derived from StRS-MDOKFSTUDIO-REVIEW-017.
