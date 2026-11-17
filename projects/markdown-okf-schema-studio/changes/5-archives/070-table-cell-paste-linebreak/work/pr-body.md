## Summary

A line break pasted into a table cell no longer splits the table row. The cell turns each line
break (LF, CR or CRLF) into a space and keeps the caret where it was, so the table keeps
rendering as one row and the List table button keeps working.

The List table button also loses a refusal branch that could never run.

## Deliverable showcase

```text
clipboard "a\nb" pasted in a cell
before:  | a        after:  | a b | y |
         b | y |
```

## Test plan

- [x] Unit: a pasted `a\r\nb\nc` becomes `a b c` and the saved row is one line
- [x] Unit: List table converts after a pasted line break (`{list-table}` holds `a b`)
- [x] `npm run test:unit`: 2596 passed, 0 failed
- [x] `just check` (okfreq validate, lint, coverage) passes

## Internal references

CR 070 (table-cell-paste-linebreak); SwRS TABLE-091, TABLE-070.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
