# Remove the opening watcher: the raw text stays text

The owner's report of 2026-11-23, on the published 1.12.0: "Open With... > Text Editor" on a
Markdown file opens Studio at once, so the raw text cannot be read; "ce qui n'est pas du tout
acceptable". The cause is by design: 1.12.0's opening watcher (`src/host-vscode/openingWatcher.ts`,
commits e883dfb6, 60036628) replaces every new text tab of a `.md` file with Studio while
`open.markdownFilesInStudio` is on (documented in `docs/known-limitations.md`, "Opening Files"), and
VS Code gives the extension no signal that a text tab came from "Open With". The first activation of
1.12.0 moved the owner's `workbench.editorAssociations` entry `*.md` to that setting, so it is on.

Intent: remove the opening watcher and its two `open.*` settings. Opening every Markdown file in
Studio goes back to VS Code's native editor association, as in 1.11, so "Open With... > Text
Editor" and "Reopen Editor With... > Text Editor" stay text. A 1.12.0 user whose association was moved to
`open.markdownFilesInStudio` gets the association back on the first activation of the fixed version.
The side preview's jump marker and "Open as Text" stay. Shipped at once as 1.12.1.

Opening Studio at a searched line comes back later, by a better design, in its own CR
(`studio-at-searched-line`, P1).
