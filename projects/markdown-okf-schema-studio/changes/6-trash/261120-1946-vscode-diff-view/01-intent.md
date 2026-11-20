# Studio in VS Code's diff views

The owner asked (2026-11-20) to test how Studio behaves in the diff views VS Code opens: the
search-and-replace preview, the Git diff (Source Control, "Open Changes"), the timeline, "Compare
with Saved" and a two-file compare.

The exploration (`work/01-findings.md`, real VS Code 1.147.0, Studio 1.10.0) found that nothing
breaks: every diff stays VS Code's own text diff, even when Studio is the user's default `.md`
editor, and the replace preview and Replace All work with Studio open. The gaps are around the
side preview next to a diff:

- it does not follow the diff's scroll (it does follow a text editor's);
- "Open Preview to Side" from the replace preview refuses with "Open a Markdown file to use
  Markdown OKF-Schema Studio.";
- Studio's "Open Preview to Side" title button is hidden on diff editors.

The intent is to decide what Studio does in each diff view (stay out and keep the text diff,
render alongside, or render a diff), close the gaps the owner keeps, and pin the chosen behaviour
with real-window tests so a VS Code update cannot break it silently.
