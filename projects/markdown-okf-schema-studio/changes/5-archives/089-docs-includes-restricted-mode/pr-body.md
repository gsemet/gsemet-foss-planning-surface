## Summary

The known-limitations page said file includes work only in a trusted workspace. The preview
actually reads them in Restricted Mode too, within a narrower folder. The page now says so.

## Deliverables

| Context | Include next to or below the document | Include elsewhere in the workspace | Include outside |
| --- | --- | --- | --- |
| Trusted workspace | read and shown | read and shown | refused, warning |
| Restricted Mode / standalone file | read and shown | refused, warning | refused, warning |

## Changes

- `docs/known-limitations.md`: rewrote the include sentence from the resource policy
  (`createPreviewResourcePolicy`; the read-only preview roots at the document folder).

## Impacts

Documentation only. No visual change.

## Blast radius

The change is one paragraph; a plain revert restores the old text.

Grade: 1

## Test plan

- [ ] New or changed tests: none, docs only
- [x] Requirements: No behaviour change
- [x] Local gates: `just check` (31 pytest passed, okfreq validate/lint/update-coverage clean,
      1013 requirements, 0 errors)
- [ ] Review
- [ ] CI green

## Internal references

- CR 089 (docs-includes-restricted-mode)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
