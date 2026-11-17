<h1 align="center">Markdown OKF-Schema Studio 1.0</h1>

<p align="center">
  <b>Read, annotate and edit rich Markdown documents: a beautiful, rich and collaborative surface between you and your coding agents.</b><br>
  <sub>297 changes since 0.3.1 · VS Code 1.95 or later · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from the Marketplace</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.0.0/CHANGELOG.md">Full changelog</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.0.0/docs/VISION.md">Vision</a>
</p>

---

## Why the Studio

We read less code and more Markdown: coding agents write the code, and we review their plans,
analyses and reports all day long. Agents already write rich Markdown well (MyST cards and
admonitions, Mermaid and PlantUML diagrams, Vega-Lite charts, large tables), but most Markdown
previews stop at GitHub Flavored Markdown, look plain, or reformat your text when you edit it. An
HTML report from the agent looks great, but you cannot annotate it.

The Studio is the missing surface, built on plain local files:

1. The agent writes a plan in Markdown, with advanced syntax where it helps.
2. You read it as a real page, at a comfortable width.
3. You annotate it: a `TODO` note, a review thread on a sentence, or a direct fix in a block.
4. You ask the agent to react. It re-reads the file and its review comments, answers and edits,
   and the diff only shows what changed.

No account, no server, no vault: the document, its comments and its schema are files in your
repository. Read the full [vision](https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.0.0/docs/VISION.md).

## 🌟 Awesome rich Markdown preview

<img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/release-showcase.png" width="860" alt="A long engineering page in the preview: prose, a captioned figure, a small and a wide table, a Vega-Lite chart and a Mermaid diagram">

## ✍️ Edit where you read

Click a block and edit it in place. An edition palette sits on the editor: headings, bold, italic,
links (<kbd>Cmd</kbd>+<kbd>K</kbd>), images, figures, tables, colours, emoji, alerts, admonitions,
cross-references and citations. Type <kbd>/</kbd> for the slash menu. Paste a screenshot and it is
saved next to the document; paste from Google Docs or Word and you get clean Markdown.

| | |
| :--: | :--: |
| <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/showcase-myst-edit.png" width="430" alt="Editing a MyST block with the edition palette"> | <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/slash-menu.png" width="430" alt="Slash menu in the block editor"> |
| The edition palette on an open block | <kbd>/</kbd> opens the slash menu at the caret |

## 🧩 MyST that looks like MyST

MyST is an underrated extension of Markdown for rich documents.

Cards, grids, tabs, list tables, figures with size and alignment, rich admonitions, version notes,
`{toctree}` and `{include}` render as Sphinx would. When a page uses MyST syntax that its `conf.py`
does not enable, the preview warns you.

Agents already write MyST, so let them. The
[`writing-for-markdown-okf-schema-studio`](https://github.com/gsemet/markdown-okf-schema-studio/tree/v1.0.0/skills/writing-for-markdown-okf-schema-studio)
skill tells your agent which syntax the preview renders (see [Usage with coding agent](https://github.com/gsemet/markdown-okf-schema-studio/tree/v1.0.0#usage-with-coding-agent)).

| | |
| :--: | :--: |
| <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/myst-cards-tabs-cream.png" width="430" alt="MyST cards and tabs"> | <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/myst-admonitions.png" width="430" alt="MyST admonitions and GitHub alerts"> |
| Cards, grids and tabs | Admonitions and GitHub alerts |

## 📊 Diagrams and charts, out of the box

Mermaid, **PlantUML without Java**, and **Vega-Lite and Vega charts** from inline data or a CSV next
to the document. Code blocks use VS Code's own TextMate grammars, with line numbers and a copy button.

| | |
| :--: | :--: |
| <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/showcase-diagrams-cream.png" width="430" alt="Mermaid and PlantUML diagrams"> | <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/charts-dark.png" width="430" alt="Vega-Lite chart in the Dark theme"> |
| Mermaid and PlantUML, no Java needed | Vega-Lite charts follow the theme |

## 💬 Review in the page

Select text and comment: threads are anchored to the text and follow it as you edit, with Reply,
Resolve, Reopen and Delete. Inline `<!-- THREAD -->` comments and TODO chips show where they sit.

Inline comments let you leave visible notes for your coding agent, and pave the way for
collaborative editing.

<img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/showcase-comment-thread.png" width="860" alt="A review comment thread in the preview">

Every block changed since the last commit gets a green bar in the margin, unsaved edits and front
matter rows included, so you see at a glance what an agent or a colleague just rewrote.

<img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/showcase-diff-cream.png" width="860" alt="Green change bars next to the blocks changed since the last commit">

## 🗂️ OKF front matter, readable and editable

YAML front matter shows as a properties table, and each value is edited in place. The field
descriptions and allowed values come from **OKF-Schema**, which adds JSON Schema validation to the
front matter of the
[Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).

Your agent learns which values each field accepts and can check its work with a CLI. The extension
shows and edits the front matter; validation is done by the
[OKF-Schema](https://github.com/gsemet/okf-schema) CLI (`uv tool install okf-schema`).

| | |
| :--: | :--: |
| <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/showcase-schema-cream.png" width="430" alt="Properties table with schema hints"> | <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/edit-frontmatter.png" width="430" alt="Editing a front matter value"> |
| Schema hints on every field | Edit a value in place |

## 🧭 Find your way in long documents

A floating toolbar gives you a table of contents, Back and Next, three width modes, zoom, find and
replace (<kbd>Cmd</kbd>+<kbd>F</kbd>), folding sections and sticky headings. Wide tables and
figures leave the reading column and stay centred. In edit mode the whole page works from the
keyboard, down into tables, cards and tabs.

<img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/margin-break-cream.png" width="860" alt="A wide table and diagram leave the reading column; the floating toolbar sits top right">

## 🎨 Three themes

| Cream | White | Dark |
| :--: | :--: | :--: |
| <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/theme-cream.png" width="280" alt="Cream theme"> | <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/theme-white.png" width="280" alt="White theme"> | <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.0.0/images/readme/theme-dark.png" width="280" alt="Dark theme"> |

## 🤖 Usage with coding agent

Ask your agent for a plan, a report or a design note, and get a page that looks good in the preview.
The **`markdown-okf-schema-studio` plugin** ships the skill `writing-for-markdown-okf-schema-studio`:
it tells the agent what the preview renders and how to choose between diagrams, charts, cards, tabs
and tables. Add this repository as a plugin marketplace, then install the plugin.

#### Claude Code

```text
/plugin marketplace add gsemet/markdown-okf-schema-studio
/plugin install markdown-okf-schema-studio@markdown-okf-schema-studio
```

#### GitHub Copilot in VS Code (Local Harness)

Add `gsemet/markdown-okf-schema-studio` to the
`chat.plugins.marketplaces` setting, then search
`@agentPlugins` in the Extensions view and install **markdown-okf-schema-studio**.

#### GitHub Copilot in VS Code (Copilot CLI Harness)

In a Copilot CLI session inside VS Code, type the terminal commands as `/plugin` commands:

```text
/plugin marketplace add gsemet/markdown-okf-schema-studio
/plugin install markdown-okf-schema-studio@markdown-okf-schema-studio
```

#### GitHub Copilot CLI

This makes the plugin available in Copilot CLI and in the Copilot SDK.

```text
copilot plugin marketplace add gsemet/markdown-okf-schema-studio
copilot plugin install markdown-okf-schema-studio@markdown-okf-schema-studio
```

VS Code also picks up plugins installed with Copilot CLI. OpenAI Codex and any
[Agent Plugins](https://agent-plugins.org/) client read the same plugin. The plugin version always
matches the extension version.

---

> [!IMPORTANT]
> **Upgrading from 0.3.1**
> - **PlantUML:** diagrams now use the built-in engine. If you had set `plantuml.jarPath`, tick
>   `markdownOkfSchemaStudio.plantuml.useJar` to keep using Java.
> - **Removed setting:** `markdownOkfSchemaStudio.preview.doubleClickToSwitchToEditor` had no effect;
>   delete it from your `settings.json`.
> - **New defaults** for a workspace that never chose: Cream theme, toolbar collapsed to its first
>   row, GFM palette buttons. Choices you already made are kept.

<details>
<summary><b>✍️ Editing</b></summary>

- Edition palette above every open block editor: heading level, bold, italic, strikethrough, code
  block with a language list, quote, rule, TODO; each button is one undo step.
- Palette modes Strict, GFM, MyST and Full choose the buttons; rendering is the same in every mode.
- <kbd>Cmd</kbd>+<kbd>B</kbd> / <kbd>I</kbd> toggle bold and italic, <kbd>Cmd</kbd>+<kbd>/</kbd>
  toggles an HTML comment.
- Link panel (<kbd>Cmd</kbd>+<kbd>K</kbd>), pre-filled when the caret is in a link; Save replaces it.
- Image and Figure buttons open the file dialog in the document's folder.
- Edit figure form: source, alt text, caption, legend, width, align and name.
- Colour picker for text and background, with 16 swatches and a hex field.
- Emoji picker (about 150 emoji) and a Table button with a 9 × 9 size grid.
- GFM buttons: alert, checkbox, HTML table, collapsible, footnote, Mermaid, column alignment, key.
- MyST buttons: admonition, definition list, math, sub/superscript, label, reference, document
  link, citation from your `.bib` files, dropdown, captioned table, key.
- Slash menu: <kbd>/</kbd> at a line start lists the palette's commands with completion (`/h2`,
  `/table`, `/note`).
- Paste a screenshot: saved as `image.png` next to the document and inserted on its own line.
- Paste rich text (Google Docs, Word, web pages) as Markdown; paste a URL over text to make a link.
- Select blocks with <kbd>Shift</kbd>+click or <kbd>Shift</kbd>+<kbd>↑</kbd>/<kbd>↓</kbd>; copy,
  cut, paste and move them (<kbd>Alt</kbd>+<kbd>↑</kbd>/<kbd>↓</kbd>) in one undo step.
- Up and down arrows on the "+" bar move a block.
- Keyboard-only editing: arrows select blocks, Enter opens, Escape closes; Right walks into
  tables, admonitions, cards and tabs.
- VS Code's undo, redo, select-all and delete-line keys work in the text boxes, rebinding included.
- Rename a `(label)=` from its anchor icon; the remaining `{ref}` uses are counted.
- Text you type is no longer lost when you follow a link, go Back or switch tab right after typing.
- An editor stays open, text and caret kept, when you save, switch theme or a diagram finishes.
- Blocks after a GitHub alert now open, move and save on their own lines.

</details>

<details>
<summary><b>▦ Tables</b></summary>

- Row above, Row below, Col left, Col right and delete buttons in the table bar.
- Drag handles move rows and columns (also <kbd>Alt</kbd>+arrows); the whole table is the drop zone.
- Formatting buttons inside a cell; pipes and line breaks are escaped so the table never splits.
- Convert a table between pipe, `{list-table}` and HTML in one step, refused when content would
  be lost.
- Col + and Col − keep your padding, indentation and outer pipes.
- Columns never narrow below 5em; wide tables scroll or break out in Auto width.

</details>

<details>
<summary><b>🧩 Rendering</b></summary>

- MyST cards with header and footer, grids, tabs with sync groups, version notes.
- `{list-table}` with title, header rows, widths and alignment.
- Figure `:width:` and `:align:`; `(name)=` labels show an anchor, and `{ref}` jumps there.
- `{toctree}` lists its documents as links, with `:caption:`, `:hidden:` and `:glob:`.
- `{code-block}` caption as a title bar; TextMate highlighting on a dark background with line
  numbers (two new settings turn them off).
- README HTML like on GitHub: `<div align>`, `<picture>` following the theme, `<details>`, `<kbd>`,
  badges.
- `[TOC]`, `[[_TOC_]]` and `{contents}` render a live table of contents.
- `~~strike~~`, red `[!CAUTION]` alerts, coloured `<span style="color">`, inline images in text.
- Hebrew and Arabic text is right-aligned; long words and URLs wrap instead of scrolling.
- An unclosed fence or a broken directive shows as code with a warning; the rest renders.
- Warnings for MyST syntax missing from `myst_enable_extensions` in the nearest `conf.py`.
- Dropdown admonitions show a chevron for their state.

</details>

<details>
<summary><b>📊 Diagrams and charts</b></summary>

- PlantUML renders with a bundled engine: no Java, no network, also in Restricted Mode.
- `{uml} file.puml` and local `!include` files, redrawn when they change.
- Vega-Lite and Vega charts (JSON or YAML) with inline data or a local CSV, TSV or JSON file.
- An invalid Mermaid diagram shows one error line with the parser's reason folded below.
- Copy button on every code block.

</details>

<details>
<summary><b>💬 Reviewing</b></summary>

- Comment threads stored in `<name>.comments.json`: select text, press Comment (or
  <kbd>Cmd</kbd>+<kbd>Alt</kbd>+<kbd>M</kbd>).
- Reply, Resolve, Reopen, Delete; orphaned threads are listed at the end, never dropped.
- Threads follow their lines as you edit and follow a renamed document.
- Inline `<!-- THREAD -->` comments with authors and dates, from the Thread button or `/thread`.
- HTML comments and TODOs as chips that open on click; a toolbar button hides the comments.
- Green change bars since the last commit, unsaved edits and front matter fields included.
- Changes made by another tool or an agent glow briefly in the preview.

</details>

<details>
<summary><b>🧭 Navigating and layout</b></summary>

- Floating toolbar in five rows, collapsible to the first one.
- Table of contents column with folding entries and the current section highlighted.
- Back and Next across documents and anchors, one history per preview.
- Width modes Margin, Auto and Full; zoom from 70 % to 200 %.
- Find and replace in the rendered text, writing to the Markdown source in one undo step.
- Fold sections from a heading chevron, a shortcut or the toolbar; folds are kept per document.
- Sticky heading band; the same 40 px top gap on every page.
- A link to a missing file keeps its text and shows a warning icon that names the problem.
- Light, short animations: tooltips slide in, the toolbar unfolds and, collapsed, briefly shows
  its rows when a preview opens; the system's "reduce motion" setting turns them off.

</details>

<details>
<summary><b>⚡ Speed and reliability</b></summary>

- The MyST render runs in a background thread; stale renders stop.
- Long documents are faster: unchanged blocks and diagrams stay in place while you type.
- Linked-file excerpts refresh right away on save, and reliably on Linux.
- Background failures are written to the extension's Output channel.
- Link search by name skips `node_modules`, `.git`, `_build` and virtual environments.

</details>

<details>
<summary><b>🔒 Security</b></summary>

- A read-only preview never reads your home folder or dot-directories such as `.ssh`.
- In Restricted Mode, path settings are ignored, and the edit button is greyed out with the reason.
- PlantUML through Java runs with the `ALLOWLIST` profile and refuses URL includes.

</details>

<details>
<summary><b>🤖 For agents</b></summary>

- New plugin `markdown-okf-schema-studio` for Claude Code, GitHub Copilot, OpenAI Codex and Agent
  Plugins clients, installed from this repository as a marketplace; its version follows the
  extension's.
- Its skill `writing-for-markdown-okf-schema-studio` tells the agent what the preview renders, how to
  choose between diagrams, charts, cards and tables, and how to install the extension.

</details>

<details>
<summary><b>🛠 For contributors</b></summary>

- The source is split into layers whose import boundaries are checked, and files have a size limit.
- Settings, palette actions and MyST directives each come from one registry.
- Pull request CI runs the simulated tests; the real VS Code window tests run on demand.
- Python 3.11 or later for the build and documentation tools.

</details>
