## Summary

Long preview documents are hard to skim. Each heading can now be folded to hide its section (up to the next heading of the same or a higher level) and unfolded again.

## Deliverables

- A chevron next to each heading, shown on hover and for the focused heading.
- Shortcut `Cmd+Alt+[` / `Ctrl+Alt+[` toggles the current section; a toolbar Fold button and the "Fold All" / "Unfold All" palette commands act on the whole document.
- Fold state is view state kept per document across reloads; the Markdown file is never rewritten.
- Search and anchor navigation unfold the target; blocks inside a folded section cannot be edited until unfolded. Works in read and edit mode.

| | Cream | Dark |
| --- | --- | --- |
| Before | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/a9fa0443a6cba2aa93153bef47110bbfb624b6e5/before-cream.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/a9fa0443a6cba2aa93153bef47110bbfb624b6e5/before-dark.png) |
| After | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/a9fa0443a6cba2aa93153bef47110bbfb624b6e5/after-cream.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/a9fa0443a6cba2aa93153bef47110bbfb624b6e5/after-dark.png) |

```ts
// src/core/state/headingFold.ts, src/page/modules/headingFold.ts
// per-document fold keys in webview state; hidden="until-found" + beforematch unfolds on find
```

## Autonomous decisions

- Fold state lives in the webview state (same key scheme as the table of contents), not in a workspace preference.
- `hidden="until-found"` with `beforematch` makes search unfold the target.
- One toolbar Fold button toggles fold all / unfold all; the two commands are separate palette entries.
- Shortcut matches VS Code's own fold keys on the physical key.
- Folding is refused while a block or front matter editor is open, rather than closing the editor.
- Known limit: fold keys are lost when a heading is renamed.

## Internal references

CR 143 (heading-folding), request: backlog item heading-folding.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
