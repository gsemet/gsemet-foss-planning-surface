## Summary

A `{grid}` written inside a quote (`>`) whose body starts with a blank quoted line mapped each of its cards one source line too early. Clicking a card title or body in edit mode opened the block editor on the line above the card. The editor now opens on the card's own line, as for the same grid outside a quote.

## Deliverables

Before and after, for `> ::::{grid} 2`, `>`, `> :::{grid-item-card} A`, `> Body.`, `> :::`, `> ::::`:

| | Card and title line | Body line |
| --- | --- | --- |
| Before | one line above the card | one line above the body |
| After | the card's directive line | the body's own line |

```ts
// directiveBody: strip the quote prefix of the opener from every line of the directive,
// then run the same fence tests and slice as for an unquoted directive.
const prefix = quotePrefix(openerLine);
const lines = rawLines.map((l) => stripQuotePrefix(l, prefix));
```

## Changes

- `directiveBody` (grid, card, item and tab-set parsing) reads the source lines through the quote prefix, so the fences are found behind `>` and `> >`; the old fallback stays for any case the fences cannot be located.
- The same fix corrects a quoted backtick-fenced card with a blank first body line and a quoted card with an option line.
- Render tests check the card, title and body lines for quoted, doubly quoted and unquoted grids and cards.
- The requirement for editing a card gains a boundary scenario, with the requirements log and the changelog.

## Impacts

No visual change: only the source line a click opens the editor on. The render test is the proof.

## Blast radius

Grade: 1. The change is local to one function of the renderer's directive parsing; a plain `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code: 4 rows fail on main)
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Local gates: `just check` passes, `just requirements-lint` passes, 22 of 22 tests in the grid card line test file; the local preflight only failed on the locked-screen real-window stage, covered by the green heavy run
- [x] Review
- [x] CI green (pull request jobs and the heavy run with integration and stress, all green at this head)

## Autonomous decisions

- A grid inside a list item is also one line early but needs a different fix: filed as a follow-up, left out of this PR.
- A grid inside a GitHub alert is out of scope, as specified.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
