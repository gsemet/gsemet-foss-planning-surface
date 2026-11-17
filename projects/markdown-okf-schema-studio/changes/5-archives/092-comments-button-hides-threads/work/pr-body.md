## Summary

The toolbar Comments button, labelled "Hide comments", hid only the gray comment chips and left
inline thread chips on the page, while the `preview.showComments` setting hid both. The button now
behaves like the setting.

## Deliverables

Pressing the Comments button, before and after (the TODO chip always stays):

| Chip | Before | After |
| --- | --- | --- |
| gray comment | hidden | hidden |
| inline thread | visible | hidden |
| TODO | visible | visible |

```css
html[data-sphinx-preview-comments="off"] #sphinx-myst-preview-content
  .okf-comment[data-okf-comment-kind="comment"],
html[data-sphinx-preview-comments="off"] #sphinx-myst-preview-content
  .okf-comment[data-okf-comment-kind="thread"] { display: none; }
```

## Changes

- Stylesheet: the button's "off" rule also covers thread chips (`commentStyles.ts`).
- The requirement for the setting and the button states the new behaviour and loses its Known
  issue line; the requirements log has an entry.
- Tests: a stylesheet test (fails on the previous code) and a new real-window scenario that
  presses the button on a page with a gray, a thread and a TODO chip.

## Impacts

Users who hide comments with the button no longer see inline threads. No other visual change.
The assertion of the button test changed intent: it used to pin that the button hides the gray
kind only, and now pins the gray and thread kinds.

## Blast radius

Grade: 1. One CSS selector; a plain `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code: verified with the source stashed)
- [x] Requirements: SwRS updated, Known issue removed, markers in code and tests, coverage regenerated
- [x] Local gates: `just check` (2640 unit tests, requirements validate/lint/coverage clean),
      `just ci-visual` (351 scenarios, passed)
- [ ] Review
- [ ] CI green

## Internal references

CR 092 (comments-button-hides-threads), SwRS REVIEW-152.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
