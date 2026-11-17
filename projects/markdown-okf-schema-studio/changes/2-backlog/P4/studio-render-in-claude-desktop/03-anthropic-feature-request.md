# Feature request for anthropics/claude-code (posted 2026-10-31: https://github.com/anthropics/claude-code/issues/106384)

Follows the repository's `.github/ISSUE_TEMPLATE/feature_request.yml` (fetched 2026-10-31): title
prefix `[FEATURE] `, label `enhancement`, one feature per issue, duplicates searched first. Blank
issues are disabled: post it through the "Feature Request" form, one field per section below.

Duplicate search (2026-10-31, `gh search issues --repo anthropics/claude-code`): "custom editor",
"webview plugin", "open with markdown desktop", "file viewer extension desktop", "plugin html pane",
"markdown preview desktop plugin", "desktop file pane", "Files pane open with", "plugin custom
viewer". No request for Claude desktop. Related, not duplicates:

- #74336 (closed, not planned): plugin UI contribution in the **VS Code** extension.
- #81482 (open): VS Code extension chat links bypass custom editors.
- #83693 (closed, not planned): desktop "Open in" menu for other IDEs.
- #101866 (open): desktop file pane Markdown layout.

---

## Title

[FEATURE] Desktop: let a plugin open matching files in its own sandboxed viewer (custom editors)

## Preflight Checklist

- [x] I have searched existing requests and this feature hasn't been requested yet
- [x] This is a single feature request (not multiple features)

## Problem Statement

I maintain a VS Code extension, Markdown OKF-Schema Studio, a schema-aware Markdown editor and live
preview (MyST directives, frontmatter forms, Mermaid/PlantUML/Vega diagrams, comments). In VS Code
it is a custom editor for `*.md`: the extension hosts its own HTML page in a webview, with a message
bridge to read and write the document.

More and more of my Markdown work happens in the Claude Code tab of Claude desktop. There, a click
on a `.md` file, in the conversation or in the Files pane, always opens the built-in file viewer.
OKF/MyST content then shows as plain Markdown or raw text, and I have to switch to VS Code to read
it as it is meant to look.

I checked the plugin (mod) API of Claude Code 2.1.309 for a way to plug the existing editor in:

- no event fires when the user opens a file in the Files pane or from a link in the conversation;
- the desktop surface's elements (`Box`, `Text`, `Button`, `Input`, `Select`, `Svg`, `Link`,
  `Code`, `Markdown`, `Client`) cannot host HTML: no webview or iframe element;
- the built-in browser pane can show a local page, but only Claude opens it, never a file click.

So a plugin cannot offer a viewer for a file type without rewriting its renderer on top of the
app's `Markdown` element, which defeats the purpose.

## Proposed Solution

A plugin contribution that registers a **viewer for a file pattern**, hosted by Claude desktop in a
sandboxed webview, like VS Code's custom editors:

1. In the plugin manifest, something like:

   ```json
   "viewers": [{
     "id": "okf-studio",
     "displayName": "Markdown OKF-Schema Studio",
     "filenamePattern": "*.md",
     "entry": "./viewer/index.html",
     "priority": "option"
   }]
   ```

2. Clicking a matching file in the conversation or in the Files pane opens it in that viewer
   (`priority: "default"`, or a user setting choosing the default per pattern), with an
   "Open with… → Built-in viewer" escape, as in VS Code.
3. The page runs in a sandboxed webview with a strict CSP and a `postMessage` bridge to the plugin's
   hooks module (or MCP server): the file's text and URI, theme changes, and, when the session's
   permissions allow it, writing the file back through the normal edit flow so Claude sees the
   change.

## Alternative Solutions

- **Re-render with the app's `Markdown` + `Svg` elements in a mod pane**: a second renderer to keep
  in sync, and it loses the editor's interactions. Not viable for a real editor.
- **A local web server opened in the built-in browser pane**: works only when Claude opens it (a
  skill), not on a file click; it is a browser tab, not a viewer of the file, with port management
  on the plugin side (the workaround described in #74336 for VS Code).
- **MCP Apps** (`ui://` pages) could host the page if the Code tab renders them for any MCP server,
  but they open from a tool call inside the conversation, not from a file click. Letting a viewer
  contribution point at an MCP App resource would be an acceptable implementation of this request.
- **Today**: I switch to VS Code to read the files Claude writes.

## Priority

Low - Nice to have

## Feature Category

Other

## Use Case Example

1. I ask Claude, in the desktop Code tab, to update a requirements bundle written in MyST Markdown
   (frontmatter forms, admonitions, Mermaid diagrams, cross-references).
2. Claude edits `requirements/tiers/swrs/.../SwRS-…-018.md` and links it in its reply.
3. I click the link: the file opens in the Studio viewer contributed by the plugin, rendered as in
   VS Code, with frontmatter validation against the bundle's schema.
4. I fix a field in the frontmatter form; the plugin writes the file, and Claude sees the change in
   its next turn.
5. This saves the round trip to VS Code for every file Claude touches, and lets non-developers
   (who use only Claude desktop) review these documents at all.

## Additional Context

- VS Code API this mirrors: `contributes.customEditors` (`viewType`, `selector`, `priority`) and
  `CustomTextEditorProvider` with `WebviewPanel`.
- The extension's page already runs outside VS Code (its visual tests load it in plain Chromium
  with a stubbed `acquireVsCodeApi`), so the porting cost on the plugin side is a host bridge, not a
  rewrite.
- Security expectations: the viewer page gets no network access by default, no Node, only the
  bridge; writes go through the session's permission rules.
- Repository: https://github.com/gsemet/markdown-okf-schema-studio
