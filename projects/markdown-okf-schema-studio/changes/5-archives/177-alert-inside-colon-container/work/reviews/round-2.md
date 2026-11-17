# Review round 2: alert inside a colon container

Re-review of the uncommitted change in `markdown-okf-schema-studio-wt-177` against
[round 1](round-1.md).

**Verdict: approve.**

## What runs

- `npm run compile`: ok.
- `npm run test:unit`: 3159 / 3159 pass (one new test since round 1).
- `npm run test:contracts`, `check:markers`, `check:limits`: ok.
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
  1065 requirements, 0 errors, 0 warnings.

## Round 1 required items

1. **Closing fences of 4 or more colons counted as openers: fixed.** `COLON_OPEN` is now
   `/^\s*(:{3,})(?!:)\s*\S/u`. The round 1 probe (an alert after a closed `::::{grid}`) now gives
   `:::{note}`. The "outside" test adds an alert after a closed `::::{tab-set}` and a closed
   `:::::{grid}` and asserts a colon fence, so a regression would fail.
2. **Backtick fence longer than the body's backtick fences: fixed.** Inside a colon container the
   fence is `` "`".repeat(longest + 1) ``, with `longest` the longest backtick run (at least 3)
   opening a line of the quoted body, after `stripQuote`. The new test (a four-backtick block in
   an alert inside a card) checks the structure and the exact `data-line` / `data-end-line`
   tuples, including `["p", 7, 7]` for the paragraph after the alert. That catches the old failure,
   where the paragraph was swallowed into a code block. Extra probes that pass: a
   five-backtick body holding a four-backtick line, and the four-backtick case with CRLF line
   endings. Both keep `after` as a paragraph in the card with exact lines.

## Round 1 minor items

- Dead `GITHUB_BOLD_ALERT_MARKER` guard: removed.
- `innermostWith` doc mismatch and the unused `tab`: the helper and the variable are removed.
- GFM-009 Criteria: now covers the boundary (a backtick directive whose fence is longer than any
  backtick fence of its body).
- Not changed, acceptable: the colon regexes accept any indentation, which only over-counts
  (harmless). A few test lines are over 120 characters (cosmetic; no linter enforces it).

## Line maps

The output keeps the same number of lines as before (only the fence text changes), so
`sourceLines` stays exact; `alertSourceLines.test.ts` and `crlfAlerts.test.ts` pass unchanged.
