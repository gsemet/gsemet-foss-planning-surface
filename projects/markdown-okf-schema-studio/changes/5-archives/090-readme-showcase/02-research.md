# 090 research: features and competitor comparison

Check date for every external claim: **2026-10-25**. Method: WebFetch of Marketplace pages, READMEs
and the official VS Code release notes (1.119 to 1.142). Vocabulary: "documented" = the page
states it; "not documented" = the page was read and does not mention it (weak evidence of absence,
NOT proof); "unknown" = page not retrievable or too sparse. The README may state "not documented"
only as "we found no mention", never as "does not support".

## 1. Inventory of current features (code and SwRS)

SwRS paths are under `requirements/tiers/swrs/<scope>/`. IDs are examples, the scope holds the rest.
Version: package.json 0.3.1, 881 SwRS files.

| # | Feature | Evidence (code / SwRS) |
|---|---------|------------------------|
| F1 | Custom editor + side preview for `*.md` (Open With, book icon, Ctrl/Cmd+K Shift+V) | `package.json` customEditors/commands; scope `lifecycle-sync` |
| F2 | Themes: VS Code current, Dark, White, Cream (default), cycle button, per workspace | SwRS-MDOKFSTUDIO-THEME-001; scope `theme-zoom` |
| F3 | Width modes Margin / Auto / Full; Auto lets wide tables, figures, images, code break out of the column, centred | SwRS-MDOKFSTUDIO-LAYOUT-023; scope `layout-width` |
| F4 | Floating 3-row toolbar, back/next history, zoom 70-200, sticky heading band, TOC column with folding | scope `toolbar-navigation` (TOOLBAR-013) |
| F5 | Incoming-changes marks: green bar on blocks whose lines changed since the last commit, toolbar toggle | `src/page/modules/incomingChanges.ts`, `incomingToggle.ts`, `src/host-api/vcsInfo.ts`; TOOLBAR-013 |
| F6 | Mermaid built in (fences, theme-following, cache) | SwRS-MDOKFSTUDIO-DIAG-001; `src/page/modules/mermaidPreview.ts` |
| F7 | PlantUML built in (`@plantuml/core`, no Java, offline, Restricted Mode ok), `{uml}`/`{plantuml}` files, local `!include`; optional JAR | SwRS-MDOKFSTUDIO-DIAG-023, DIAG-024; `plantumlDiagram.ts` |
| F8 | MyST rendering: directives, admonitions (nested/titled), `{grid}`, `{toctree}`, `{list-table}`, figures, math, labels/refs, `{include}` | scope `myst` (MYST-031, MYST-064), `src/core/myst`, `src/core/directives` |
| F9 | WYSIWYG-style block editing of the Markdown source: click a block, Done/Cancel, one undo step, edits applied to raw source only (no document rewrap) | scope `block-editing`; `src/page/features/blockSourceEditor.ts` |
| F10 | Edition palette (Strict/GFM/MyST sets), colours, emoji, links panel, rich paste to Markdown, image paste to file | scope `palette-slash` (PALETTE-052, 196, 203, 240); `editPalette.ts`, `pasteHtml.ts`, `pasteImage.ts` |
| F11 | Slash menu with filter/aliases | scope `palette-slash`; PALETTE-240 |
| F12 | Table editing (cell editor, row/column bar, size grid), pipe table to/from `{list-table}` conversion | scope `table-editing`, MYST-064; `markdownTable.ts` |
| F13 | Figure form (Browse, alt, caption, legend, width, align, name) | MYST-031/032/035; `figurePanel.ts`, `figureDirective.ts` |
| F14 | Block selection, multi-block copy/cut/paste, Alt+Up/Down move | `src/page/modules/blockSelection.ts`, `blockEditActions.ts`; scope `block-editing` |
| F15 | OKF frontmatter properties table, JSON-Schema validation diagnostics, enum controls, typed scalar editors, YAML editors for arrays/objects | scopes `frontmatter-schema`, `frontmatter-editing` (FMEDIT-062/063) |
| F16 | `x-okf-link` linked evidence: tooltip/preview fields, source line numbers | FMSCHEMA-046, FMSCHEMA-047 |
| F17 | Review comment threads: `<name>.comments.json`, highlights, popover, reply/resolve/delete, orphaned list, follows edits/renames | scope `review-annotations`; `commentThreads.ts`, `commentCompose.ts` |
| F18 | Inline `<!-- THREAD -->` comments, TODO toggle, gray comment chips + toggle | `inlineThread.ts`, `commentsToggle.ts`; scope `review-annotations` |
| F19 | Sphinx awareness: warns when syntax needs a `myst_enable_extensions` entry missing in `conf.py` | `src/core/mapping`..., `confLocator.ts`, `confParser.ts`; scope `myst` |
| F20 | Editable task-list checkboxes, GFM alerts, footnotes, collapsibles | scope `gfm`; palette GFM mode |
| F21 | Source navigation: links, fragments, wikilinks, scroll sync both ways, cursor-block outline | scope `toolbar-navigation`, `src/core/navigation`, `src/core/scroll` |
| F22 | Code blocks with copy button, language | scope `code-blocks`; `codeCopy.ts` |
| F23 | Workspace Trust safety (read-only in untrusted workspace, bounded file reads) | scope `trust-security` |
| F24 | Motion: short fades, change glow, reduced-motion respected | `motion.ts`; README "Motion" |

## 2. Comparison matrix

Legend: Y = documented, N? = not documented on the page read, P = partial, ? = unknown.
Columns: VSC = VS Code built-in (1.142, 2026-10-14), MAIO = Markdown All in One 3.6.3, MPE =
Markdown Preview Enhanced 0.8.40, WYS = other WYSIWYG extensions (zaaack Markdown Editor 0.1.22,
Office Viewer 4.2.2, Markdown Pro), MYST = MyST extension (ExecutableBookProject.myst-highlight 0.11.0).
"Mark Sharp" could not be found by search (unknown, dropped).

| Feature | VSC | MAIO | MPE | WYS | MYST |
|---------|-----|------|-----|-----|------|
| Themes (several built-in) F2 | N? (only `markdown.styles` CSS) [1] | N? (light export theme) [2] | ? (page silent) [3] | Y zaaack "multi-theme" [5]; Markdown Pro "32 built-in palettes" [8]; Office Viewer N? | N? (light/dark by OS) [4] |
| Cream/paper warm theme specifically | N? | N? | ? | ? (palette lists of Markdown Pro not verified for a paper theme) | N? |
| Auto-margin wide table/figure breakout F3 | N? | N? | N? | N? | N? |
| Diff of changes in rendered view F5 | **Y** preview renders diffs, changes highlighted [1]; hybrid editor has Git change markers and Markdown diffs (experimental, 1.132) [1][6] | N? | N? | N? | N? |
| Mermaid F6 | **Y** built-in since 1.121 (2026-05-20), pan/zoom [1][7] | N? ("separate extension") [2] | Y [3] | Y zaaack [5], Markdown Pro [8]; Office Viewer N? | N? |
| PlantUML without Java/server F7 | N? | N? | P: needs PlantUML server or local `.jar` [3][9] | zaaack N? [5]; Office Viewer: npm list mentions PlantUML, details ? [10]; Markdown Pro N? | N? |
| MyST directives/admonitions rendered F8 | N? (GitHub alerts not documented either) [1] | N? | N? / ? | N? (zaaack: "Markdown extensions", unnamed) [5] | **Y** in preview (directives, roles; optional amsmath, deflist, dollarmath, tasklist) [4] |
| MyST `{grid}` / `{list-table}` / `{figure}` rendering | N? | N? | ? | N? | ? (README says "directives"; per-directive list not verified) |
| WYSIWYG editing of any Markdown F9 | P: experimental Markdown Editor (edit rendered, Locked mode) [1] | N? | N? | Y [5][8][10] | N? |
| WYSIWYG editing of MyST (grid, admonitions, figures, list-table) F9, F12, F13 | N? | N? | N? | N? | N? ("Not mentioned": WYSIWYG) [4] |
| Raw-source-preserving edits (no reformat) F9 | ? | n/a | n/a | P: Markdown Pro says source pane "preserves comments, directives, HTML" [8]; others ? | n/a |
| Slash menu F11 | N? | N? | N? | Y Markdown Pro [8]; zaaack N?; Office Viewer N? | N? |
| Table toolbar / cell editing F12 | N? | P: GFM table formatter (source) [2] | N? | Y Markdown Pro [8]; Office Viewer ? | N? |
| Frontmatter display | Y table / codeBlock / hide (`markdown.preview.frontMatter`, 1.121) [7] | P: syntax supported [2] | N? | N? | N? |
| Schema-aware OKF frontmatter (JSON Schema validation, typed editors) F15 | N? | N? | N? | N? | N? |
| `x-okf-link` linked evidence F16 | N? | N? | N? | N? | N? |
| Review comment threads (sidecar JSON, resolve, orphan) F17 | N? | N? | N? | N? | N? |
| Agent/hybrid comments | P: hybrid editor "add comments that an agent can act on" (experimental, Agents window) [6] | N? | N? | N? | N? |
| Block selection + move (Alt+Up/Down) F14 | ? | N? | N? | ? | N? |
| Sphinx `myst_enable_extensions` check F19 | N? | N? | N? | N? | N? |
| Math F8 | Y KaTeX [1] | Y KaTeX [2] | Y KaTeX/MathJax [3] | Y zaaack KaTeX [5] | Y dollarmath [4] |
| Image paste F10 | Y in Markdown Editor (1.142) [11] | ? | Y upload (opt-in) [3] | Y zaaack saves to `assets` [5] | N? |
| Code copy button F22 | Y (preview 1.132, editor 1.142) [11][12] | N? | ? | ? | N? |
| Works offline/no network | Y | Y | P: optional CDN math, server PlantUML | ? | Y |

Sources:
[1] https://code.visualstudio.com/docs/languages/markdown (read 2026-10-25)
[2] https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one (v3.6.3)
[3] https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced (0.8.40);
    https://github.com/shd101wyy/vscode-markdown-preview-enhanced
[4] https://marketplace.visualstudio.com/items?itemName=ExecutableBookProject.myst-highlight (0.11.0);
    https://github.com/executablebooks/myst-language-support
[5] https://marketplace.visualstudio.com/items?itemName=zaaack.markdown-editor (0.1.22);
    https://github.com/zaaack/vscode-markdown-editor
[6] https://code.visualstudio.com/updates/v1_131 (2026-07-29, hybrid editor, comments for agents) and
    https://code.visualstudio.com/updates/v1_132 (2026-08-05, Markdown diffs in the hybrid editor,
    gutter markers; baseline of the diff NOT stated)
[7] https://code.visualstudio.com/updates/v1_121 (2026-05-20: built-in "Mermaid Markdown Features",
    front matter as table)
[8] https://github.com/AshishSalaskar1/Markdown-Plus-Vscode (Markdown Pro, id
    `AshishSalaskar.markdown-pro`; an earlier search snippet said "11 themes", the README fetch said
    "32 built-in palettes": do not quote a number)
[9] https://raw.githubusercontent.com/shd101wyy/vscode-markdown-preview-enhanced/master/README.md
[10] https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-office (4.2.2; 1.6M installs;
    Markdown WYSIWYG via Vditor per search results, not the listing)
[11] https://code.visualstudio.com/updates/v1_142 (2026-10-14, Markdown editor: paste images, rename
    links, outline, copy button)
[12] https://code.visualstudio.com/updates/v1_132

Other release notes read: 1.119 (2026-05-06, preview/source toggle button), 1.122-1.130, 1.133-1.141:
no Markdown item except 1.137 (2026-09-09, rich GitHub links in the Markdown editor, experimental)
and 1.141 (preview link fix). 1.135 and 1.143 do not mention Markdown.

Not verified / dropped: "Mark Sharp" (no result); Markdown Preview Enhanced themes, admonitions,
frontmatter (page silent: unknown); MyST extension per-directive list.

## 3. Ranked differentiators

Honest outcome: two of the headline items in the intent are NOT safe claims any more.

Not safe (do not claim as unique):
- **Diff since last commit**: VS Code renders Markdown diffs in the preview and has Git change
  markers and Markdown diffs in its experimental hybrid editor [1][6]. Studio's version is a
  green bar on changed blocks in the live preview, vs HEAD (code). Claim only the specific form
  ("changed blocks marked in the live preview, toggled from the toolbar"), not "nobody has it".
- **Built-in Mermaid**: VS Code has it natively since 1.121 [7], and WYSIWYG tools have it. Not a
  differentiator; only the pair with PlantUML is.
- **Themes** and **slash menu**: Markdown Pro documents both [8], zaaack documents themes [5].
  Still defensible: the *Cream paper theme as default* and the quality of the three-theme set,
  as taste, not as "only one".

Verified or best-supported differentiators (all compared tools lack a documented equivalent;
"documented" caveat applies to all):
1. **WYSIWYG editing of MyST**: grid cards, nested admonitions, figures (with form), `{list-table}`
   and pipe-table conversion (F8, F12, F13). The MyST extension is preview-only [4]; VS Code's
   Markdown Editor and the Vditor/Milkdown tools document no MyST [1][5][8]. Strongest claim.
2. **Schema-aware OKF frontmatter** (JSON Schema diagnostics, enum/typed editors) and
   `x-okf-link` evidence (F15, F16). VS Code only shows front matter as table/code/hidden [7].
   Nothing equivalent found elsewhere.
3. **Review comment threads** stored in a sidecar JSON, with resolve/orphan handling (F17), plus
   inline `<!-- THREAD -->` (F18). Closest: VS Code hybrid editor "comments that an agent can act
   on" (experimental, Agents window, storage unknown) [6]. Phrase as "human review threads in
   plain files next to the document".
4. **PlantUML with no Java, no server, offline, Restricted Mode** next to Mermaid (F6, F7).
   MPE needs a server or `.jar` [3][9]; VS Code, MAIO, zaaack, MyST list no PlantUML [1][2][5][4];
   Office Viewer's PlantUML support is unknown [10] (check before publishing).
5. **Auto-margin width mode**: narrow reading column with wide tables/figures breaking out and
   centred (F3). No compared page documents anything similar. Low evidence strength (absence), but
   visual and easy to show.
6. **Raw-source-preserving WYSIWYG** (edits touch only the edited block; one undo step each; no
   rewrap) (F9). Markdown Pro claims preserving unsupported syntax [8]; others unknown. Phrase as
   Studio's guarantee, not as a comparison.
7. **Block selection and move, rich paste to Markdown, Sphinx `conf.py` extension check** (F14,
   F10, F19): nothing documented elsewhere; secondary.
8. **Cream default theme + three-theme cycle** (F2): taste item, show but do not compare.

## 4. Suggested README comparison rules

- A comparison table is only safe for items 1-4 and must be dated "checked 2026-10-25".
- Wording: "No equivalent found in ..." with the tool list and version numbers, linked to this file
  or the sources; never "only extension that".
- Re-run the VS Code check before each release: its Markdown Editor moves every few weeks
  (1.131, 1.132, 1.137, 1.142 in 4 months), and diff/comment features may converge.
