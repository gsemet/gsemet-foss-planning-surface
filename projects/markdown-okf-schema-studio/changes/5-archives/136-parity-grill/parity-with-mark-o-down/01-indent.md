Look in https://github.com/Harveyhase68/mark_o_down

I basically wants to support everything mark-o-down supports, with proof as screenshots. do not mention this project during planning and fixing

---

## What's new in 0.7.0

- 🍎 **New in 0.7.2: better on the Mac** – a real menu bar with all shortcuts (⇧⌘B, ⇧⌘M …), and
  older Macs (macOS 12 / older Safari) no longer show an empty window.
- 📚 **New in 0.7.1: Save workspace as PDF** – all documents of a workspace in one PDF, links
  jump to the right page. Plus: F5 / F6 no longer reload or crash the window.
- 🗂️ **Workspaces and a folder tree** – a `.modw` file for a folder of documents, the tree beside
  the editor (left or right, search, paste a path), favourites in *Open workspace …*.
- 📑 **Tabs** – every document in its own tab with its own undo history; the session keeps them all.
- 🔗 **Linked documents** – `[[wiki links]]` like Obsidian (found by name in the workspace),
  `Ctrl+click` follows any link, `Alt+←` goes back; drag a file from the tree into the text → a link.
- 📖 **`[[toc]]`** – a table of contents of the whole workspace (or the document), also in HTML and PDF.
- ✏️ **Split editor** – the Markdown source beside the document can be edited, with an HTML check.
- 📄 **Save as PDF** and **spell checking** with the system's own checker.
- New in 0.6.0: Mermaid diagrams and the extended syntax – see the [changelog](#changelog).

## Features

- **True WYSIWYG** for CommonMark + GitHub Flavored Markdown: headings, bold/italic/strikethrough,
  inline code, code blocks, bullet/numbered/task lists, quotes, links, images, horizontal rules, tables,
  footnotes – plus superscript, subscript and highlight as the HTML tags GitHub renders
  (`<sup>`, `<sub>`, `<mark>`).
- **Folder tree** (`Ctrl+Shift+B`) beside the editor – on the left or right, width by dragging its
  edge, can be hidden; the last folder is remembered. The field on top finds files and folders
  below the current folder by part of their name (`liz` → `Lizenz.md`, `Blizzard.md`); a pasted
  path (file or folder, also with quotes from *Copy as path*) goes straight there. Arrow keys,
  `Enter`, type the first letters to jump, double-click a folder to show only it, `Backspace` /
  ↑ for the parent folder, a small drive selector on Windows.
  **Drag a file from the tree into the document** to link it where you drop it: `[[kapitel1]]`,
  `[[teil 2/Kapitel 2]]` (relative to the document) – or `[Kapitel 2](teil%202/Kapitel%202.md)`
  without wiki links.
- **Workspaces** (`.modw`) for a folder of Markdown documents: *Open → New workspace …* saves
  `<Name>.modw` in the folder (JSON: `version`, `name`, `root` – the documents' folder relative
  to the file, `../` allowed – and `wikiLinks`). Opening one (also by double-click in Explorer)
  shows its folder in the tree and finds `[[Link]]` by name anywhere in it, like Obsidian.
  *Open → Open workspace …* lists every workspace Mark O Down has seen, favourites on top,
  each list sortable by name or last opened. The last workspace is opened again at start.
- **Table of contents** `[[toc]]` (or `[[toc depth=2]]`) on a line of its own: in a workspace it
  lists all its documents folder by folder with their headings, otherwise the document's own
  headings. Generated, never saved (only the marker is); in the HTML / PDF export and print too.
- **Mermaid diagrams** like on GitHub: ` ```mermaid ` blocks are drawn (flowcharts, sequence,
  class, state, Gantt, pie … diagrams); click a diagram to edit its source below it. Also in the
  HTML export and print. Mermaid is loaded only when a document has a diagram.
- **Extended syntax** (Pandoc / Typora / Obsidian, switchable under *Help*, on by default):
  `^superscript^`, `~subscript~`, `==highlight==` and definition lists (`Term` / `: Definition`).
  **Wiki links** like Obsidian: `[[Link]]`, `[[Link|Text]]`, `[[Link#Heading]]`, `[[#Heading]]`,
  `[[sub/Link]]`, `[[../sub/Link]]` (`.md` may be left out).
  GitHub shows these as plain text; switched off, Mark O Down reads Markdown exactly like GitHub
  (then `~text~` is strikethrough).
- **Math** like on GitHub: `$E=mc^2$` inline, `$$ … $$` and ` ```math ` blocks, shown as formulas
  (LaTeX via [Temml](https://temml.org), rendered as MathML – no math fonts to ship). Prices stay
  text: `from $5 to $10` is not a formula (Pandoc's rule). Loaded only when a document has math.
- **Syntax highlighting** in fenced code blocks (` ```js `, ` ```rust ` …, ~40 languages), in GitHub's
  colours – also in the HTML export and when printing. Loaded only when a document has code.
- **Lossless round-trip** – open → save without edits is byte-identical. When you edit, only the
  changed blocks are rewritten, in their original style (`*` vs `-` bullets, `__bold__` vs `**bold**`,
  `~~~` vs ```` ``` ```` fences, compact `|---|` vs aligned tables …). BOM and CRLF/LF line endings are kept.
- **Everything else is preserved** – other HTML, front matter and constructs the editor
  doesn't edit visually are kept verbatim and shown as editable raw blocks.
- **README-friendly HTML** – `<div align="center">`, `<br>` and `<img width="…">` / `<a><img></a>`
  logos are rendered and editable.
- **Badge & icon picker** – [shields.io](https://shields.io), [badgen.net](https://badgen.net),
  [forthebadge.com](https://forthebadge.com), all [Simple Icons](https://simpleicons.org), your own images.
  Sources and templates are configurable (`badges.json`), icon lists are cached for offline use.
- **Emoji & symbol picker** – every Unicode emoji and ~9,700 symbols with names and keywords in
  English plus the UI language. Search matches inside words (`ross` → 😵 *face with crossed-out eyes*). Skin tones,
  recently used, full 4-byte Unicode support.
- **Images like on GitHub** – relative paths resolve from the document's folder, `/path` from the
  repository root. Drag & drop images and `.md` files into the window.
- **Spell checking** in the language of the text (chosen separately from the interface language),
  using the system's dictionaries.
- **Find & replace** with match case, whole word and regular expressions (`$1` groups).
- **Safe** – changes by other programs are detected (reload or ask, never overwritten silently),
  unsaved work is recovered after a crash, recently opened files in the Open menu.
- **Tabs** – every document in its own tab, each with its own undo history and position;
  drag to reorder, middle-click or × to close, right-click for *Close others / to the right /
  all*, *Copy path*, *Show in file tree*. A file that is open already just comes to the front.
- **Sessions like Notepad++** – closing the app keeps all tabs as they are, unsaved changes
  included, and the next start continues with them. The files are only changed when you save.
- **Open HTML** – converted to Markdown; a dialog lists exactly what Markdown can't keep.
- **Export** – standalone HTML file, PDF, HTML to the clipboard, print. Document zoom 50–300 %.
- **Paste images and links** – `Ctrl+V` of a screenshot saves it next to the document (`images/`)
  and inserts it; a pasted URL becomes a link, an image URL an image.
- **Five languages** – German, English, French, Spanish and Italian; follows the system language,
  switchable any time under *Help → Language*.
- Markdown shortcuts while typing (`# `, `- `, `1. `, `> `, `**bold**`, `[text](url)` …).

---

but also this should also be supported

````md

<div align="center">

<img src="app-icon.svg" alt="Mark O Down" width="96" height="96">

....

</div>


````
