## Summary

The preview had no find of its own: Cmd/Ctrl+F opened VS Code's generic webview find, with no options
and no way to replace. This PR adds a find bar and a replace field to the preview.

## Deliverables

Find: Cmd/Ctrl+F opens the bar (match case, whole word, regular expression, match count, all matches
highlighted; Enter, Shift+Enter and F3 move between matches; Escape closes). Matches are found in
rendered text, including tables and admonitions, and folded sections unfold for the current match.
The shortcut is left alone when the text editor or a field of an open editor has focus.

| Before | After |
| --- | --- |
| ![before cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/0710d3d9cf1ae2bd7135ca00466e35f105f009ea/before-cream-find.png) | ![after cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/0710d3d9cf1ae2bd7135ca00466e35f105f009ea/after-cream-find.png) |
| ![before dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/0710d3d9cf1ae2bd7135ca00466e35f105f009ea/before-dark-find.png) | ![after dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/0710d3d9cf1ae2bd7135ca00466e35f105f009ea/after-dark-find.png) |

Replace: Replace and Replace all, with `$1`, `$&`, `$<name>` and `$$` in regular expression mode.
Only the matched source span is edited, and Replace all is one undo step. Matches that do not map
one-to-one to the source (formulas, link targets, generated text, front matter, includes) are skipped
and counted in the bar. Replace is disabled, with the reason, in read-only previews and during an open edit.

![replace](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/0710d3d9cf1ae2bd7135ca00466e35f105f009ea/after-cream-replace.png)

## Autonomous decisions

- Find and replace ship together in one PR, because replace builds on the find bar.
- No toolbar button was added; the shortcut is the entry point.
- Occurrence mapping is conservative: a block whose rendered and source match counts differ skips all matches of that text.
- The "before" screenshots were taken from a copy of the unchanged code.

## Internal references

CR 144; backlog items find-in-preview and replace-from-preview.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
