# Feature session — expected changes

What users will see once the session lands. Decisions referenced as U#/D# are in `decisions.md`.

## Reading the preview

| Feature (backlog item) | Before | After |
| --- | --- | --- |
| Copy code (copy-code-block) | No way to copy a code block except selecting it by hand | A copy icon appears top-right when the pointer is over any code block, in preview and edit mode; a check mark confirms; the raw code goes to the clipboard (U7, D27) |
| Top gap (bug-one-line-top-margin-missing) | 0 px above text, 17–34 px above a heading depending on level, 24 px above "Start writing" | The same ~40 px gap above the first element in every case (U6) |
| Margins (clever-margin-break + P1 margin button) | Fixed column (`maxContentWidth`); wide tables scroll inside the column; images capped to the column | Toolbar button cycles Margin → Auto (wide tables/figures break out to the pane width) → Full width; remembered per workspace (U5) |
| Zoom (P1) | Only VS Code's global zoom | Zoom −/+ in the toolbar, 70–200 %, per workspace, text and column scale together (U16) |
| Back / Next (P1) | After following a link there is no way back except reopening the file | Back/Next buttons per preview panel, covering document jumps and in-page anchors (U16) |
| Table of contents (toc-in-vscode-markdown-studio) | None in the preview (`{toc}` is ignored) | Optional right column, off by default, h1–h4, each node collapsible, current section highlighted, hidden on narrow panes (U8) |
| Toolbar | One row: Refresh, Anchor, Edit, Theme | Two rows: Refresh/Anchor/Edit/Theme, then Back/Next/Zoom−/Zoom+/Margin/TOC/Diff (U16) |
| Comment and TODO chips (todo-comments) | `<!-- -->` comments invisible; TODO is plain text | Gray chip for comments that expands into an admonition-like box; green chip for TODO and `<!-- TODO … -->`; tool comments stay hidden; setting to turn comment chips off (U9) |
| Incoming changes (show-incoming-diff) | Not shown | Blocks changed since the last commit get a green left bar, on by default, toolbar toggle and setting; needs VS Code's built-in Git, nothing shown for untracked files (U11, D18–D19) |
| MyST checks (myst-autodetect) | Every MyST syntax always on, no hint about `conf.py` | When a `conf.py` is found, using a syntax whose extension is not enabled shows a warning in the preview and in the Problems panel; no `conf.py` = no change (U17, D20–D23) |

## Editing in the preview

| Feature | Before | After |
| --- | --- | --- |
| Edition palette (P1 block-edition-palette) | Raw text box with Done/Cancel only; `*`/`_` wrap the selection | A palette above the edited block: heading level, bold, italic, strikethrough, code with language, link (Cmd/Ctrl+K), quote, rule, table grid 9×9, image picker, emoji, colour; GFM: alerts, checkbox, HTML table; MyST: admonitions, footnotes, definitions, math, sub/sup, figure, anchors. Mode select strict/GFM/MyST per workspace with a default setting. Merged into the table-cell bar in tables (U2, U3, D10–D17) |
| Strikethrough rendering (prerequisite) | `~~x~~` shows the tildes | Rendered as struck-through text (palette button needs it) |
| Colour (palette) | Inline styles stripped | Text and background colour via a restricted `<span style>` (hex/rgb only) that the sanitizer keeps (U14) |
| TODO shortcut | Ctrl+/ does nothing | Ctrl+/ toggles `<!-- TODO: … -->` around the line or selection (U15) |
| Move blocks (move-block-up-down) | Only cut/paste in the text editor | ↑/↓ buttons on the "+" insert bar and Alt+↑/↓; one undo step; refused for blocks from `{include}` or across non-blank unmapped text (U13, D1–D4) |
| Multi-block selection (multibloc-selection) | One block at a time | Shift+click / Shift+↑/↓ selects contiguous blocks; Cmd/Ctrl+C, X, V copy, cut, paste the raw Markdown; Alt+↑/↓ moves the selection (U13, D5) |
| Paste image (paste-image-in-edit-mode) | Pasting an image does nothing | Saved next to the `.md` as `image.png` (`image-1.png`… on conflict), `![image.png](image.png)` inserted with the alt text selected; 10 MB cap, png/jpeg/gif/webp (U12, D6–D8) |
| Images (edit-inline-image) | Mostly fixed by `2af0afa` | Remaining gaps closed: image inside a link, raw HTML `<img>`, ArrowUp into the properties table no longer closes the editor (D9) |

## Comments (local-comment-mode)

| Before | After |
| --- | --- |
| None | Select text in the preview, a floating button adds a comment thread (reply, resolve, delete), saved in `<name>.comments.json` next to the document; author from a setting, then `git config user.name`, then the OS user; threads whose text disappeared are kept and listed (D25) |

## Settings (vscode-setting-rework)

| Before | After |
| --- | --- |
| 13 one-line descriptions, one of them inverted (`scrollPreviewWithEditor`), one wrong ("Absolute" `jarPath`), no grouping | Clear descriptions of what each setting does and the effect of each value, grouped and ordered; same keys, so nothing breaks; new settings from this session documented the same way (D26) |

## Project files

- `.agents/glossary/common.md`: shared vocabulary (chip, palette, insert point, block editor,
  toolbar, …), referenced from `AGENTS.md` (U10).
- Each backlog item lands in `.agents/changes/archives/NNN-<name>/` with its intent and a
  `report.md` (status, delivered commits, proof of completion, open items), numbering from 007.

## Not in this session

- rendering-difference-on-windows: the screenshot is an empty file; needs a new capture (D28).
- Process items: okfreq-layer, parity-with-obsidian, parity-with-markdown-studio-extension,
  animation-markdown-studio, record-demo-video, create-dedicated-project.
- deep-analysis-review SEC-01–04 and PERF refactors (left out earlier as too risky).
