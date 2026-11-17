## Summary

Checks how the preview renders dollar amounts and pins the result. The preview typesets the text
between two dollar amounts as maths (`$5 and $6`), where Sphinx keeps it as text. This change
documents that behaviour and adds visual scenarios that lock it, with a real `$x$` span as control.

## Deliverable showcase

```text
Between $5 and $6 each.   ->   Between [5 and ]6 each.   (preview: "5 and " typeset as maths)
A real span: $x$          ->   A real span: [x]          (maths, as expected)
```

New visual scenarios (light and dark) render a page with the three price sentences of the
white paper and the control span, and assert the typeset spans.

## Test plan

- `just ci-visual`: 327 scenarios passed (2 new), 217 screenshots
- `just check`: passed (scenario count test updated to 327)
- okfreq validate, lint and update-coverage checks: 1010 requirements, 0 errors

## Internal references

- CR 069 (currency-dollar-preview-check); follow-up backlog item dollarmath-align-sphinx (P2)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
