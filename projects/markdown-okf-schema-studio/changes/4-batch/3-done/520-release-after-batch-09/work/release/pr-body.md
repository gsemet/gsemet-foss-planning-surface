## Summary

Everything merged since 1.12.1 is on `main` but reaches no user before a release. This is version 1.13.0, a minor release because it adds new features. Merging it publishes it.

## Deliverables

- The version commit `chore: version 1.13.0`, with the changelog heading and a commit reference on each line.
- The release notes, the announcement thread draft and their images in `docs/releases-notes/2026-11-27-v1.13.0/`, shown below.

## Changes

- Version 1.13.0 in the npm manifest, the lock file, the two plugin manifests and the plugin catalog.
- `CHANGELOG.md`: the `Unreleased` lines move under `1.13.0 - 2026-11-27`.
- Pictures: `admonition-block-edit-before-after.png` joins the before and after captures of the merged change, both cropped to the same region at the same scale (composed with Pillow); `chart-hover.png` is a crop of a capture of the hover box. `comment-render-speed.png` is a chart of the real-window measures reported in #549 and #550 (3,109 to 4 elements restyled by one new comment; highlight drawn in 53 ms before, 46 ms with #549, the further effect of #550 within runner noise). The clip's GIF and MP4 are copies of the approved clip `raw-copy-balance-edges`.
- No dedicated hero scenario, to keep code out of the version commit. The clip is the picture of the thread.

## Impacts

Users get the changes listed in the release notes below. This pull request itself changes no behaviour.

## Blast radius

A merge publishes to both extension registries; a published version cannot be withdrawn by a revert, only followed by a new version.

Grade: 3

## Test plan

- [ ] New or changed tests (they fail on the previous code): none, version and notes only
- [x] Requirements: no behaviour change
- [x] Changelog: the lines move under the version heading
- [ ] Local gates: `just release-notes-check` and the release tests passed at `4222c324`; `just preflight` running
- [x] Heavy CI of the released code: run [45958381383](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45958381383) on `b1e23cc`, every job green
- [ ] Review: the owner reviews the notes folder
- [ ] CI green: running at `4222c324`; the real VS Code jobs are skipped there and run on the version push

## Internal references

CR-520.

---

# 📰 Release notes (rendered)

<h1 align="center">Markdown OKF-Schema Studio 1.13</h1>

<p align="center">
  <b>Render comments faster on large documents, copy a selection as Markdown, edit one block inside an admonition.</b><br>
  <sub>96 changes since 1.12.1 · VS Code 1.95 or later · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from VS Code Marketplace</a> ·
  <a href="https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio">Install from Open VSX</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.13.0/CHANGELOG.md">Full changelog</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.0.0">1.0 showcase</a>
</p>

---

## ⚡ See comments rendered faster on large documents

On a large test document, a new comment now restyles 4 elements of the page instead of about 3,100, and its highlight appears about 14% sooner. Adding, answering, resolving or deleting a comment updates only the marks that change, and the **Comment** button, the copy button and the edit mode outline follow the selection or the pointer at most once per frame.

![Bar chart: elements restyled by one new comment drop from 3,109 to 4, and the time until its highlight is drawn from 53 ms to 46 ms](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/4222c324a362490a23e6d735644075a46390fc35/docs/releases-notes/2026-11-27-v1.13.0/comment-render-speed.png)

## 📋 Copy a selection as Markdown

Select text in the preview and press <kbd>Ctrl</kbd>/<kbd>Cmd</kbd>+<kbd>C</kbd> to paste its Markdown in a text editor, or the rendered text in a rich editor. Turn on the setting `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges` (off by default, in the VS Code settings) to also get the markers and fence lines of what the selection cuts through, as in this clip.

![A selection copied from the preview and pasted as Markdown, with the fence lines of an admonition and a warning added](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/4222c324a362490a23e6d735644075a46390fc35/docs/releases-notes/2026-11-27-v1.13.0/raw-copy-balance-edges.gif)

## ✏️ Edit one block inside an admonition or alert

In edit mode, a click or <kbd>Enter</kbd> on a paragraph, a list item or a directive inside an admonition or a GitHub alert edits that block only. The title or the frame still opens the whole box.

![A click in a note that opened the whole directive source, then the same click opening only the second paragraph inside the note](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/4222c324a362490a23e6d735644075a46390fc35/docs/releases-notes/2026-11-27-v1.13.0/admonition-block-edit-before-after.png)

## 📊 Hover a chart to read its values

Hover a mark of a Vega-Lite chart in the preview to see its values.

![A grouped bar chart with a box showing the quarter, revenue and product line of the hovered bar](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/4222c324a362490a23e6d735644075a46390fc35/docs/releases-notes/2026-11-27-v1.13.0/chart-hover.png)

## 🛠 Smoother editing

- **Open a file in Studio at the caret's line.** The command **Open in Studio at This Line**, in the Command Palette and the title bar menu of a Markdown text editor, opens a Studio tab, marks the line and keeps the text tab.
- **Links, Back and Next keep your place.** In a Studio tab, a link to another Markdown file and Studio's Back and Next open the target at its heading or line, in a Studio tab when the file opens as one.
- **Chart text follows your page text.** Vega-Lite and Vega legends, axes and titles scale with the Markdown font size and the zoom, and the preview no longer shows the **Chart source** section under a chart.
- **Front matter errors stand out.** A field with a schema error shows its name in red with a wavy underline under its value; a warning, also on a whole table, shows in the warning colour.

<details><summary><b>🐞 All fixes</b></summary>

- In Auto width, a code block whose longest line is a little wider than the column widens until the line fits, instead of keeping a scroll bar, with or without a caption.

</details>

<details><summary><b>🔎 Details</b></summary>

- The comment speed figures come from a generated test document in VS Code on a Linux CI runner, so your times depend on your document and your machine. The time to select text did not change measurably.
- The raw Markdown copy works in reading and edit mode.
- Inside an admonition or an alert, a diagram, a formula or a code block opens whole. <kbd>Enter</kbd> on the admonition selected as a whole opens all of it.
- <kbd>Alt</kbd>+<kbd>Up</kbd> and <kbd>Alt</kbd>+<kbd>Down</kbd> move a block of the body inside its box, the arrow keys keep the caret at the edges of its lists, and erasing a block of an alert keeps the alert.
- **Open in Studio at This Line** shows the Studio tab of a file that is already open in another group, instead of opening a second one.
- `"tooltip": null` on a chart mark turns its hover box off. A Vega chart shows only the tooltips it defines.
- A chart specification's own `config` still wins over the page's text sizes. Discrete labels on the x axis are horizontal.
- The HTML export keeps each chart as a static drawing, with its **Chart source** section.

</details>

<details><summary><b>🛠 For contributors</b></summary>

- Each screenshot of the published gallery has its own link, `gallery.html#<capture id>`, which stays the same from one CI run to the next and follows Back and Forward.
- The published docs site plays a feature clip as a looping video where a page shows its GIF. `just clip` builds a clip from its storyboard.
- The behaviour scenarios of the requirements have IDs, shown in the requirements viewer, and a new How we test page links the test levels to the requirements.
- The trust and security use cases are accepted in a real VS Code, and the visual checks run as two parallel CI jobs.

</details>

---

# 🐦 Announcement thread (rendered)

# Announcement thread for 1.13.0

## 1/

A coding agent had written a runbook, and I wanted to send one part of it back with a question. A copy from the preview gave me the rendered text, so the table and the warning lost their Markdown. In 1.13, Ctrl+C in the preview gives the Markdown under the selection, and one setting adds the fence lines and markers that the selection cuts through. Commenting renders faster too: on a large test document, a new comment restyles 4 elements instead of about 3,100, and its highlight shows up about 14% sooner. I can also edit a single paragraph inside a note without opening the whole box.

Video: [raw-copy-balance-edges.mp4](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/4222c324a362490a23e6d735644075a46390fc35/docs/releases-notes/2026-11-27-v1.13.0/raw-copy-balance-edges.mp4)

## 2/

The details are in the release notes:
https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.13.0

## 3/

Install or update it from the Marketplace, or from Open VSX for VSCodium and Cursor; it is free and MIT:
https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio
https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
