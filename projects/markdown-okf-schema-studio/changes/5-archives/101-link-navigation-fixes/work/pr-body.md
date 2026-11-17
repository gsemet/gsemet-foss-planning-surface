## Summary

A link to a file that is missing or blocked now shows a small warning icon next to it, and the
Back and Next buttons and percent-encoded link paths behave correctly in the cases below. The
link keeps its text and colour; only the icon is added.

## Deliverables

**Warning icon on broken links.** The icon follows the link and its tooltip names the problem.

```text
before:  see the [deployment guide](docs/guid.md)        (looks like any link)
after:   see the [deployment guide](docs/guid.md) ⚠      (tooltip: "File not found: docs/guid.md")
```

For a blocked target the tooltip holds the refusal reason (for example "The navigation target is
outside the workspace."). The icon is hidden from screen readers, and the link carries the same
reason as its description (`aria-describedby`), so the information is not lost. Link tooltips are
looked up again when the preview regains focus, so a file created or deleted in the meantime is
reflected.

| Light | Dark |
| --- | --- |
| ![Warning icon after two broken links, light theme](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/9720be44a64f44c6f5b79a03790cc1bc612a0604/v35-link-warning-light-900.png) | ![Warning icon after two broken links, dark theme](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/9720be44a64f44c6f5b79a03790cc1bc612a0604/v36-link-warning-dark-900.png) |

**Back and Next.**

- Within the same document they now scroll the preview to the stored line, also when the preview
  does not follow the editor (before, the history moved but the preview stayed put).
- When the target document cannot be opened, the history position no longer moves: Back and Next
  keep the state they had, and the warning is still shown.

**Percent signs in link paths.** A link path is decoded once, like a URL path.

| Link | Before | After |
| --- | --- | --- |
| `100%25.md` | refused as undecodable | opens `100%.md` |
| `a%2541.md` | decoded twice to `aA.md` | opens `a%41.md` |

An anchor whose text still holds an escape after four decoding rounds (for example `%41`) is now
refused by the page as the host already did.

## Changes

- Warning icon, its description and the "File not found" reason for missing files.
- History moves restore the position when the open fails; a history move carries a `reveal` flag
  so the page scrolls even when it does not follow the editor.
- One decoding round for link paths; the leftover-escape check of the page uses `[\da-f]`.
- Link targets are asked again on focus or when the preview becomes visible.
- Requirements, changelog and two visual scenarios (light, dark).

## Impacts

- Existing assertions whose intent changes: the page requirement test "a missing or blocked target
  is shown only in the tooltip" now checks that the link keeps its look and gains the icon; the
  session test of the discovery answer now expects "File not found: gone.md" instead of "The
  navigation target is unavailable."; the "Decoding at most four times" scenario of the link
  classification requirement becomes "Decoding once" (a doubly encoded path is no longer decoded
  twice).
- Known issue that remains: while the preview stays focused and visible, a file created or deleted
  meanwhile is not noticed until the focus or the visibility comes back. It is recorded in the
  requirement.
- Image and resource references keep their own decoding rules; only links changed.

## Blast radius

Grade: **medium**. The preview page (link marking, scroll message), the link and history
controllers of the session, and the link classification used by every followed link. A `reveal`
field is added to the existing `sourceScroll` message; older pages ignore it.

## Test plan

- `npm test`: 2667 unit tests, 2 contract tests, 47 security tests, all passing.
- New or changed tests fail on the previous code (checked by stashing `src`): link path decoding,
  warning icon and description, refresh on focus, scroll on a history move with Anchor mode off,
  history position after a failed open, discovery reason.
- `just check` passes; requirements validate, lint and coverage checks pass (1013 requirements).
- `just ci-visual`: 359 scenarios passed, including the two new link warning scenarios.
- Window suites (`just preflight` integration stage) were not run for this change.

## Internal references

- CR 101, backlog item link-navigation-fixes.
- Requirements: SwRS-MDOKFSTUDIO-TOOLBAR-054, -059, -079, -085, -090, -117 and
  StRS-MDOKFSTUDIO-TOOLBAR-011.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
