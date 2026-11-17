## Summary

This PR adds 14 backlog features and a set of post-plan fixes to Markdown OKF-Schema Studio. Each feature has a report under `.agents/changes/archives/NNN-*/report.md`.

### Features (archives 007–020)

| # | Feature |
|---|---|
| 007 | Settings rework |
| 008 | Copy button on code blocks |
| 009 | Edit inline images |
| 010 | Fix the missing top margin on one-line documents |
| 011 | Width-mode-aware margin breaks (Margin / Auto / Full width) |
| 012 | Table of contents column in the preview |
| 013 | TODO comment chips |
| 014 | Show incoming (Git) changes as a diff |
| 015 | MyST auto-detection (`conf.py`, syntax heuristics) |
| 016 | Block editing palette (GFM and MyST groups, table grid, emoji, image, colour) |
| 017 | Move blocks up and down |
| 018 | Paste images in edit mode |
| 019 | Multi-block selection, copy, cut and paste |
| 020 | Local comment threads: sidecar file, resolve, reopen and delete, orphaned comments, re-anchoring |

### Post-plan fixes

- **P1:** test-only check that the TOC column is captured in screenshots.
- **P2 and P7:** a 16 px content gutter in Full width; scenarios for width-mode breaks.
- **P3:** a uniform 40 px top gap; each element clears the toolbar.
- **P4:** the palette sits above the edit box and stays visible (sticky); the caret is scrolled into view.
- **P5 and P6:** the "MyST" label; screenshots of the palette modes.
- **P8:** a 3-row toolbar with a collapse button; the collapsed state is saved as a preference.
- **P9 (part):** the e2e campaign was reorganised into 16 behaviour groups, with:
  - one "locks" line per scenario;
  - a product-owner gallery (`npm run review:gallery`);
  - pruning of old reports (`npm run review:prune`);
  - content and error-state scenarios.
- **P11:** a `/` slash menu with completion, in the style of Notion and Obsidian.

## Screenshots

Taken from the e2e campaign on 3b6e8f4: the headless visual run, and the real VS Code window run for the keyboard features. The images live on the `pr-assets/11-png` branch, which is not part of this PR.

<details><summary><b>007 — Settings rework (theme, width, toolbar settings)</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/007-settings-toolbar-theme.png" width="520" alt="007-settings-toolbar-theme">

</details>

<details><summary><b>008 — Copy button on code blocks</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/008-copy-button.png" width="520" alt="008-copy-button">

</details>

<details><summary><b>009 — Edit inline images and figures</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/009-figure-editor.png" width="520" alt="009-figure-editor">

</details>

<details><summary><b>010 — Top margin on one-line documents (uniform top gap)</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/010-top-gap.png" width="520" alt="010-top-gap">

</details>

<details><summary><b>011 — Width-mode-aware breaks: Margin / Auto / Full width</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/011-break-margin.png" width="360" alt="011-break-margin"> <img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/011-break-auto.png" width="360" alt="011-break-auto"> <img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/011-break-full.png" width="360" alt="011-break-full">

</details>

<details><summary><b>012 — Table of contents column</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/012-toc.png" width="520" alt="012-toc">

</details>

<details><summary><b>013 — TODO comment chips</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/013-todo-chips.png" width="520" alt="013-todo-chips">

</details>

<details><summary><b>014 — Incoming Git changes as a diff</b></summary>

_No screenshot: covered by integration tests only (needs a real Git repository or clipboard)._

</details>

<details><summary><b>015 — MyST auto-detection (palette switches to MyST)</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/015-myst-mode.png" width="520" alt="015-myst-mode">

</details>

<details><summary><b>016 — Block editing palette (menu, table grid, emoji)</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/016-palette-menu.png" width="360" alt="016-palette-menu"> <img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/016-palette-grid.png" width="360" alt="016-palette-grid"> <img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/016-palette-emoji.png" width="360" alt="016-palette-emoji">

</details>

<details><summary><b>017 — Move blocks up and down (after Alt+Down twice)</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/017-move-alt-down.png" width="520" alt="017-move-alt-down">

</details>

<details><summary><b>018 — Paste images in edit mode</b></summary>

_No screenshot: covered by integration tests only (needs a real Git repository or clipboard)._

</details>

<details><summary><b>019 — Multi-block selection</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/019-block-selection.png" width="520" alt="019-block-selection">

</details>

<details><summary><b>020 — Local comment threads and orphaned comments</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/020-comment-thread.png" width="360" alt="020-comment-thread"> <img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/020-orphaned-box.png" width="360" alt="020-orphaned-box">

</details>

<details><summary><b>P4 — Sticky palette above a tall editor</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/P4-sticky-palette.png" width="520" alt="P4-sticky-palette">

</details>

<details><summary><b>P8 — 3-row toolbar, expanded and collapsed</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/P8-toolbar-expanded.png" width="360" alt="P8-toolbar-expanded"> <img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/P8-toolbar-collapsed.png" width="360" alt="P8-toolbar-collapsed">

</details>

<details><summary><b>P11 — `/` slash menu (MyST, filtered)</b></summary>

<img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/P11-slash-myst.png" width="360" alt="P11-slash-myst"> <img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/425102c258801b65d57549cb2097244ff7dbbdc5/P11-slash-filtered.png" width="360" alt="P11-slash-filtered">

</details>

## Test plan

- [x] Locally on 3b6e8f4: `just check` (types, unit, contracts, security, release tests) and `just sphinx-check` are green.
- [x] CI: full `just preflight` (e2e under xvfb) green on 8c55e48 (run 39753045267).
- [x] Each feature was gated during development, including the real-window keyboard suites on an unlocked, idle machine (see the archive reports).
- [ ] Manual checks in real VS Code:
  - [ ] Cmd+K in an open block opens the link panel.
  - [ ] Cmd+Shift+M focuses the palette and does not toggle the Problems panel.
  - [ ] The native open dialogs (Document link, Image, Figure) keep the block editor open.
  - [ ] Figure form: Cmd+A and then typing loses no character.
  - [ ] Block move: Alt+Down twice on a focused block; Cmd/Ctrl+Alt+Up inside the text box reopens the editor at the same caret.
  - [ ] Multi-block copy, cut and undo, and paste after a focused "+" bar.
  - [ ] Paste a screenshot into an open block editor.
  - [ ] The collapsed toolbar stays collapsed after a reload.
  - [ ] The slash menu works.

## Known issues (not fixed here)

These are tracked by `knownIssue` scenarios:

- **K1:** a long unbroken word or URL overflows the pane.
- **K2:** Hebrew and Arabic paragraphs are not aligned right-to-left.
- **K3:** the error line of an invalid Mermaid diagram is duplicated on each re-render.
- **K4:** the GFM Caution alert uses the Warning colour.

## Open questions

- **T30:** should the GFM `<kbd>` button be hidden in MyST mode?
- **T39:** should Shift+Arrow select the focused block alone first?
- **D30:** should a comment become orphaned when its quote is gone, even if a block still exists at its line?

🤖 Generated with [Claude Code](https://claude.com/claude-code)
