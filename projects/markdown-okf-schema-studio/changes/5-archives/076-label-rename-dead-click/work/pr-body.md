## Summary

- Labels written `(_draft)=`, `(.hidden)=` or `(-dash)=` show an anchor icon, and in edit mode
  clicking it now opens the rename field. Before, the click did nothing.
- A rename sent while the preview is behind the document is answered with
  "The label is no longer on that line. Refresh the preview." instead of leaving the field
  to time out after 6 s.

## Deliverable showcase

```text
before:  click icon of (_draft)=   -> nothing (click swallowed)
after:   click icon of (_draft)=   -> "Rename label" field, name selected

before:  rename from an older render -> "The editor did not answer. Try again." (after 6 s)
after:   rename from an older render -> "The label is no longer on that line. Refresh the preview."
```

One pattern (`LABEL_NAME`, letters, digits and `_ . : -`, 100 characters at most) is now used by the
renderer, the rename field and the host. The invalid-name message no longer asks for a leading
letter or digit. Labels starting with a symbol are also listed as `{ref}` targets in the palette.

## Changes

- `LABEL_NAME` in `src/core/mapping/labelRename.ts` is the single pattern, imported by the
  anchor renderer, the page rename field and the host validator.
- `src/session/pageMessages.ts`: a rename from an older render gets the stale-line refusal.
- Requirements and tests updated accordingly.

## Impacts

No visual change. Labels starting with `_`, `.` or `-` become renamable; the invalid-name message
no longer mentions a leading letter or digit.

## Blast radius

Grade: 1

Local to the label rename and the shared name pattern (palette target list included); a plain
`git revert` restores the previous behaviour.

## Test plan

- [x] `just check` (unit 2596 passed, contracts 2, security 44, requirements validate/lint/coverage)
- [x] Unit: pattern parity; page click on `_draft`, `.hidden`, `-dash`; stale rename answered,
  other document and disposed preview not answered
- [ ] Window suite not run (no visual change)

## Internal references

- CR 076 label-rename-dead-click

🤖 Generated with [Claude Code](https://claude.com/claude-code)
