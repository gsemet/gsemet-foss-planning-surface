<!-- Proof A — "Showcase": hero image, six highlights with one picture each, full list folded. -->

<p align="center">
  <img src="images/showcase-hero.png" width="860" alt="Markdown OKF Schema Studio: a styled Markdown preview you can edit in place">
</p>

<h1 align="center">Markdown OKF Schema Studio 1.0</h1>

<p align="center">
  <b>Read, review and edit Markdown and MyST in one page, without leaving the preview.</b><br>
  <sub>297 changes since 0.3.1 · VS Code 1.9x+ · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from the Marketplace</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/main/CHANGELOG.md">Full changelog</a>
</p>

---

## ✍️ Edit where you read

Click a block and edit it in place. An edition palette sits on the editor: bold, italic, links
(<kbd>Cmd</kbd>+<kbd>K</kbd>), images, figures, tables, colours, emoji, admonitions, cross-references.
Type <kbd>/</kbd> for the slash menu. Paste a screenshot and it is saved next to the document; paste
from Google Docs or Word and you get clean Markdown.

<img src="images/slash-menu.png" width="720" alt="Slash menu in the block editor">

## 🧩 MyST that looks like MyST

Cards, grids, tabs, list tables, figures with size and alignment, version notes, `{toctree}`,
`{include}`: rendered as Sphinx would, in three themes (Cream, White, Dark).

<img src="images/myst-cards-tabs-cream.png" width="720" alt="MyST cards and tabs">

## 📊 Diagrams and charts, out of the box

Mermaid, **PlantUML without Java**, and **Vega-Lite / Vega** charts from inline data or a CSV next to
the document. Code blocks use VS Code's own TextMate grammars.

<img src="images/charts-cream.png" width="720" alt="Vega-Lite chart in the preview">

## 💬 Review in the page

Comment threads anchored to the text (Resolve, Reopen, Delete), `<!-- THREAD -->` and TODO chips, and
a green bar on every block changed since the last commit, front matter included.

<img src="images/showcase-comment-thread.png" width="720" alt="Review comment thread">

## 🧭 Find your way in long documents

A floating toolbar with a table of contents, Back / Next, width modes, zoom, find and replace
(<kbd>Cmd</kbd>+<kbd>F</kbd>), folding sections and sticky headings. Full keyboard navigation in edit
mode, down into tables, cards and tabs.

## ⚡ Fast and safe

The MyST render runs off the extension host and stops renders made useless by newer edits. Restricted
Mode renders everything but runs nothing; PlantUML through Java runs with the `ALLOWLIST` profile.

---

> [!IMPORTANT]
> **Upgrading from 0.3.1**
> - The setting `markdownOkfSchemaStudio.preview.doubleClickToSwitchToEditor` is removed (it had no
>   effect).
> - The Python documentation tools need Python 3.11 or later.

<details>
<summary><b>Everything else in 1.0 (127 entries)</b></summary>

<!-- generated from CHANGELOG.md "Unreleased", grouped by theme -->

</details>
