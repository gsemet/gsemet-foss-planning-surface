## Summary

The block edit bar was inconsistent: some buttons had no tooltip, the horizontal-rule button used
an icon that looked like centered text, and a horizontal rule was hard to click because only its
thin line was a click target. This PR fixes all three.

## Deliverables

- Every button of the block edit bar now shows a tooltip, using the same component and slide-in
  animation as the main floating toolbar (reused, not duplicated).
- The horizontal-rule button shows a `---`-style icon.
- A horizontal rule has an invisible hit area of about 12px above and below, so a click starts
  editing it.

Captured in a real VS Code window (Default Dark Modern theme, Cream preview, edit mode):

| | Before | After |
| --- | --- | --- |
| Hover on an edit bar button | `reports/shots/before-vscode-dark-cream-hover.png` (no tooltip) | `reports/shots/after-vscode-dark-cream-hover.png` (tooltip slides in) |
| Rule button | `reports/shots/before-vscode-dark-cream-rule-icon.png` | `reports/shots/after-vscode-dark-cream-rule-icon.png` |
| Click near a rule | `reports/shots/before-vscode-dark-cream-rule-click.png` (nothing opens) | `reports/shots/after-vscode-dark-cream-rule-click.png` (rule editor opens) |

Tests: two new visual scenarios (cream and dark) that fail on the previous code; unit tests for the
palette runtime and styles; requirements, user docs and changelog updated.

## Autonomous decisions

- Reused the floating toolbar's tooltip component for the edit bar instead of building a new one.
- Drew the rule icon as `---` and enlarged the rule hit area to about 12px above and below.

## Internal references

- CR 112 (`.agents/changes/03-requests/112-edit-toolbar-tooltips-and-rule`); new requirements
  SwRS-MDOKFSTUDIO-PALETTE-002 and SwRS-MDOKFSTUDIO-BLOCK-002.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
