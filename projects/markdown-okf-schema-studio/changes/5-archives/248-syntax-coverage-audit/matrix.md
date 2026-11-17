# Syntax coverage matrix: slash menu and toolbar (CR 248)

Derived from `src/core/palette/paletteActions.ts` (the registry both surfaces are built from), `src/page/modules/editPalette.ts` (additive modes: Strict < GFM < MyST < Full) and the "What renders" table of the writing skill. Strict lists only the Strict actions; its column is omitted because every Strict action also shows in GFM, MyST and Full.

Cells: `yes` = listed; `no` = not listed; `n/a` = no insert form by design (see the note). A single row is a syntax; its entry is the slash command the test `test/page/modules/slashSyntaxCoverage.test.ts` checks.

| Syntax | Entry | Slash GFM | Slash MyST | Slash Full | Toolbar GFM | Toolbar MyST | Toolbar Full |
|---|---|---|---|---|---|---|---|
| Headings `#`..`#####` | `/h1`..`/h5`, `/heading` (variants) | yes | yes | yes | yes | yes | yes |
| Bold, italic, `~~strike~~`, inline code is typed | `/bold`, `/italic`, `/strike` | yes | yes | yes | yes | yes | yes |
| Colour spans, emoji | `/color`, `/emoji` | yes | yes | yes | yes | yes | yes |
| Links `[t](u)` | `/link` | yes | yes | yes | yes | yes | yes |
| Autolinks | n/a: a typed URL links by itself; `/link` for an explicit one | n/a | n/a | n/a | n/a | n/a | n/a |
| Images `![alt](path)` | `/image` | yes | yes | yes | yes | yes | yes |
| Bulleted / numbered lists | `/bullet`, `/numbered` | yes | yes | yes | no (menu-only entry) | no (menu-only entry) | no (menu-only entry) |
| Blockquote, horizontal rule | `/quote`, `/hr` | yes | yes | yes | yes | yes | yes |
| Fenced code with a language | `/code` | yes | yes | yes | yes | yes | yes |
| Tables (pipe) | `/table` (size grid) | yes | yes | yes | yes | yes | yes |
| Column alignment `:--` `--:` | `/align` | yes | yes | yes | yes | yes | yes |
| Task list `- [ ]` | `/checkbox` | yes | yes | yes | yes | yes | yes |
| Radio group `( ) (x)` | `/option` | yes | yes | yes | yes | yes | yes |
| Footnote `[^1]` | `/footnote` | yes | yes | yes | yes | yes | yes |
| GitHub alerts `> [!NOTE]`..`[!CAUTION]` | `/note alert`.. (5 variants) | yes | yes | yes | yes | yes | yes |
| HTML table | `/html table` | yes | yes | yes | yes | yes | yes |
| `<details>` collapsible | `/details` | yes | yes | yes | yes | yes | yes |
| `<kbd>` | `/kbd` | yes | yes | yes | yes | yes | yes |
| `<sub>`, `<sup>` | `/sub`, `/sup` (write the MyST `{sub}` / `{sup}` roles) | no | yes | yes | no | yes | yes |
| `<div align>`, `<p align>`, `<img width>`, `<picture>` | no: gap (README presentation HTML, written by hand) | no | no | no | no | no | no |
| YAML front matter | n/a: edited in the properties table | n/a | n/a | n/a | n/a | n/a | n/a |
| `[TOC]` / `[[_TOC_]]` | `/toc` | yes | yes | yes | yes | yes | yes |
| `{contents}` | no: `/toc` writes `[TOC]`, same result (documented exception) | no | no | no | no | no | no |
| TODO comment | `/todo` | yes | yes | yes | yes | yes | yes |
| Review thread comment | `/thread`; comment toggle is shortcut-only | yes | yes | yes | yes | yes | yes |
| MyST admonitions `note` `tip` `important` `warning` `caution` `danger` `attention` `error` `hint` `seealso` + custom | `/note admonition`.. (11 variants) | no | yes | yes | no | yes | yes |
| Version admonitions `versionadded` `versionchanged` `deprecated` | `/versionadded`.. (3 variants, with version) | no | yes | yes | no | yes | yes |
| Dropdown (`:class: dropdown`) | `/dropdown` | no | yes | yes | no | yes | yes |
| `{card}` (header, footer, link) | `/card` (form) | no | yes | yes | no | yes | yes |
| `{grid}` + `{grid-item-card}` | `/grid` (form) | no | yes | yes | no | yes | yes |
| `{tab-set}` + `{tab-item}` | `/tab-set` (Content tabs) -- ADDED by this CR | no | yes | yes | no | yes | yes |
| `{figure}` | `/figure` (file pick / form) | no | yes | yes | no | yes | yes |
| `{list-table}` | `/list-table` only with the caret in a pipe or HTML table (convert); no empty insert (documented exception) | no | no | no | no | no | no |
| Pipe table from `{list-table}` / HTML | `/pipe` with the caret in such a table | no | yes | yes | no | yes (button only with the caret in a table) | yes (button only with the caret in a table) |
| Table with caption | `/caption` | no | yes | yes | no | yes | yes |
| `{code-block}` (caption, linenos, emphasize, name) | `/code-block` (form) | no | yes | yes | no | yes | yes |
| Math `$..$`, `$$..$$`, `{math}`, aligned | `/math` (3 forms) | no | yes | yes | no | yes | yes |
| `{kbd}` role | `/kbd` (Key (MyST)) | no | yes | yes | no | yes | yes |
| `{ref}` + `(name)=` label | `/ref`, `/label` | no | yes | yes | no | yes | yes |
| `{doc}`, `{cite}` roles | `/doc`, `/cite` | no | yes | yes | no | yes | yes |
| Definition lists | `/deflist` | no | yes | yes | no | yes | yes |
| `{toctree}` | no: project navigation, hand-written, not in the writing skill (documented exception) | no | no | no | no | no | no |
| `{uml} file.puml` | no: needs a `.puml` file picker (larger gap, see report) | no | no | no | no | no | no |
| `mermaid` fence | `/mermaid` | yes | yes | yes | yes | yes | yes |
| `plantuml` fence | `/plantuml` -- ADDED by this CR | no | no | yes | no | no | yes |
| `vega-lite` fence | `/vega-lite` | no | no | yes | no | no | yes |
| `vega` fence | `/vega` | no | no | yes | no | no | yes |

Notes: the Strict mode lists Strict rows in every column. Contextual actions (`colorCode`, `listTable`, `pipeTable`) are listed only with the caret in what they act on, in both surfaces. Checks of the test: each covered row has its entry from its first mode up and not below; each exception has a reason; every directive and fence language of the skill table has a row.
