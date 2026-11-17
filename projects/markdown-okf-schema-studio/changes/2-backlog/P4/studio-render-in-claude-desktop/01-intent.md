# Show .md files in Studio inside Claude desktop

Type: feat · Priority: P4 · Filed 2026-10-31 at the user's request ("je veux ouvrir par défaut mes
md dans cette extension"). Decisions: [02-answers.md](02-answers.md).

Status: **blocked, waiting for a Claude desktop extension point** (2026-10-31). Feature request
drafted below; the user sends it.

## Intent (user decision)

When the user clicks a `.md` file in Claude desktop (a link in the conversation, or the file
browser / file pane), it opens in **Studio itself**, integrated as in VS Code: Studio's own page
(the webview bundle) in a panel of the app, with its host bridge. No re-implementation of the
renderer, no approximation with the app's Markdown. If Claude desktop cannot host it, the item stays
blocked.

## Verification (2026-10-31, Claude Code 2.1.309, the full mod API: 22,559 lines of types)

What a VS Code-like integration needs, and what the API offers:

| Need | VS Code | Claude Code mod API | Verdict |
| --- | --- | --- | --- |
| Be told a `.md` is opened by the user | `customEditors` selector `*.md` | No event for the file pane or the file browser. The full event list (`agent.*`, `command.*`, `config.*`, `fs.*`, `prompt.*`, `session.*`, `tool.*`, `turn.*`, `ui.*`…) has no file-open event; the file pane is drawn by the desktop app, outside the engine the mods hook | **missing** |
| A panel running our HTML/JS | `WebviewPanel` | Desktop elements are `Box`, `Text`, `Button`, `Input`, `Select`, `Svg`, `Link`, `Code`, `Markdown`, `Client`. `Client` is a surface module drawing those same elements (no DOM). `Image`/`Raster` (pixels, `$.ui.blit`) exist on the terminal only. No webview, iframe or HTML element | **missing** |
| A message bridge page ↔ host | `postMessage` / `acquireVsCodeApi` | Only between a `Client` module and the hooks module (`ui.message`), for element trees | **missing** (no page to bridge) |
| Clicks on `.md` links in the conversation | — | A mod can redraw an assistant reply (`ui.render` on `AssistantMessage`) as its own `Markdown` with `onLinkPress`, but a link that is not `https:`, `http:` or `file:` draws as text, and presses are documented for the fullscreen terminal; even caught, there is no webview to open | partial, useless alone |

Other routes checked and rejected by the intent:

- Built-in browser pane: shows any local page, but only Claude opens it (`preview_start`), never a
  click on a `.md`; it is a browser tab, not an editor of the file.
- Artifacts: publish the content to claude.ai.
- Native mod pane drawing the file with the app's `Markdown` + `Svg`: a second renderer (refused).

One lead not settled: Claude desktop draws HTML widgets from MCP servers in the conversation (the
`visualize` server's `show_widget` in this session). If the Code tab renders **MCP Apps** (`ui://`
resources in a sandboxed iframe, with a JSON-RPC bridge to the server) from any user MCP server, a
Studio MCP server could host the real page, bridged like a webview. Even then it opens on a tool
call, inline in the chat, not on a click of a `.md`. To check only if the user wants a partial
version (see the grill).

Facts in the repository that matter once unblocked:

- Studio's page already runs outside VS Code: `test/visual/renderFixtures.ts:266` stubs
  `window.acquireVsCodeApi`; `test/visual/capture.py:292` loads the pages through `file://`.
- `src/host-memory/` is a host without VS Code; a Claude desktop host would sit beside
  `src/host-vscode/`.
- The repository already ships a Claude plugin (`.claude-plugin/`): the integration would ship there
  (user decision).

## Feature request for Anthropic

Draft following their issue template: [03-anthropic-feature-request.md](03-anthropic-feature-request.md).
Posted 2026-10-31: https://github.com/anthropics/claude-code/issues/106384

## Expected (once unblocked)

- A click on a `.md` (conversation link, file browser) opens Studio in a Claude desktop pane, as
  `Open With` does in VS Code, with editing when the workspace is trusted.
- Same page bundle as the VSIX; a new host layer for Claude desktop; the requirements of
  `lifecycle-sync` extended to that host.

## Open questions (for the grill)

1. Spike on MCP Apps in the Code tab (one hour: does a user MCP server's `ui://` page render, can it
   load a large bundle, can it call back), for a partial "open in Studio" on request? → **no** while
   the intent is "on click only"; yes if a tool-triggered version is acceptable.
2. Recheck date for the platform (new Claude Code release notes, mod API types)? → **at each minor
   release**, by the CoS.
