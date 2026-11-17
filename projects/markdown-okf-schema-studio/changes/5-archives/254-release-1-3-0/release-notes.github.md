<h1 align="center">Markdown OKF-Schema Studio 1.3</h1>

<p align="center">
  <b>Write MyST without looking up the syntax, keep tables in the column, find your way in a narrow pane.</b><br>
  <sub>40 changes since 1.2.0 · VS Code 1.95 or later · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from the Marketplace</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.3.2/CHANGELOG.md">Full changelog</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.0.0">1.0 showcase</a>
</p>

---

## 🧩 Write MyST without looking up the syntax

Agents write MyST cards, grids, admonitions and captioned code blocks. Now you can too, without
remembering a single option name:

- **Card and Grid** buttons in the MyST edit bar, and `/card` and `/grid` in the slash menu, open a
  small form: the grid columns and gutter, the number of cards, and the title, header, footer and
  link of each card.
- A **Code-block** button opens a form for the language, line numbers, emphasized lines, caption and
  name. With the caret in an existing `{code-block}`, it edits that block's options and leaves the
  code untouched.
- Put the caret on the type of an admonition (`:::{note}`) or a GitHub alert (`> [!NOTE]`) and the
  **types are listed with their icons** right there: arrows move, <kbd>Enter</kbd> picks, only the
  type changes.
- The slash menu now has **every admonition** (including `versionadded`, `versionchanged` and
  `deprecated`), **Content tabs** (`/tab-set`) and, in the Full palette, **PlantUML** (`/plantuml`).
  Every syntax the preview renders can now be inserted from the slash menu or the edit bar.

<p align="center">
  <img src="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.3.2/images/readme/release-1-3-showcase.png" width="860" alt="A plan in edit mode: a three-card grid and a captioned code block rendered, and the list of admonition types open at the caret of a note">
</p>

The page keeps rendering around the block you edit, so you see the result as you write it.

## 📐 Tables that stay in the column

In Auto width, a table now stays in the reading column when its columns fit: short columns (names,
dates, numbers, code) keep their text on one line and the prose column wraps. It only breaks out of
the column when it really needs the room, for example a cell with a code block.

| | |
| :--: | :--: |
| <img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/change-requests/242-bug-margin-breaking-assets/table-case-04-four-columns-one-prose-column-three-short-before-light.png" width="430" alt="Before: a four-column table breaks out of the column"> | <img src="https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/change-requests/242-bug-margin-breaking-assets/table-case-04-four-columns-one-prose-column-three-short-after-light.png" width="430" alt="After: the same table stays in the column, the notes wrap"> |
| 1.2: the table leaves the column | 1.3: it stays, the notes wrap |

A page reads as one column again, and a wide table still gets its room when it needs it.

## 🧭 Find your way in a narrow pane

When the preview sits in a narrow side pane, the table of contents no longer disappears: a thin rail
on the right shows one tick per heading, the current section highlighted. Hover or focus the rail to
open the table of contents above the text, click a tick to jump to its heading. The rail keeps the
text clear, and <kbd>Esc</kbd> closes the overlay without stealing the key from a field.

## 🛠 Smoother editing

- **Preview first**: a document always opens in preview mode, a new one or another one in the same
  panel; reloading the same document keeps the mode you were in. Press <kbd>E</kbd> in the preview
  to start editing.
- **Option lists**: a new Option button turns the selected lines into a `- ( )` choice list and
  back; <kbd>Enter</kbd> continues the list, and <kbd>Enter</kbd> on an empty option ends it.
- **Collapse the properties**: a button next to "Frontmatter properties" folds the table away while
  you read, and it comes back when the document opens again.
- **Table handles** follow the table's real edges, also once it breaks out of the column or after a
  row or column move.
- **Find and replace fields** keep their shortcuts: select all, copy, paste, undo and word moves act
  on the field, not on the page behind the bar.
- **Writing skill in GitHub Copilot**: the agent skill that teaches Studio's Markdown now has its
  own Copilot catalog, so `copilot plugin marketplace add gsemet/markdown-okf-schema-studio` then
  `copilot plugin install markdown-okf-schema-studio@markdown-okf-schema-studio` installs it, with
  its version.

<details>
<summary><b>🐞 All fixes</b></summary>

- A `+++` line inside a directive, a quote, a list item or an alert no longer breaks the render of
  the whole document: it shows as text.
- In Restricted Mode, images next to the document or in the workspace folder display again,
  including file names with spaces; includes, non-image files and hidden folders such as `.ssh`
  stay refused.
- A schema file added to the schema folder right after another change is found on the next render.
- On Windows, a PlantUML include named by a drive path (`C:\diagrams\a.puml`) now says it must be a
  relative path to a local file.
- A cell editor opened in a table that breaks out of the column stays in view when the table goes
  back into the column for the edit.

</details>

<details>
<summary><b>🛠 For contributors</b></summary>

- The development checks and the static CI job run on Windows too.
- New end-to-end and visual scenarios: a table row drag, the slash menu admonitions, the type list,
  the Card, Grid and Code-block forms, the narrow-pane rail.
- A unit test fails when a rendered syntax has no slash menu entry (with a documented list of
  exceptions).
- The release process (notes, announcement, hero image) is written down in
  `.agents/guidelines/release-process.guidelines.md`.

</details>
