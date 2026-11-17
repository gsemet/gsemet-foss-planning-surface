# Parity grill — decisions (2026-10-27)

The three parity items below were reviewed with the user, feature by feature, against what the
extension does today. Accepted features became one P1 backlog item each (user decision: "un P1 par
feature"); rejected ones must not be proposed again without a new request.

Sources: [parity-with-mark-o-down](parity-with-mark-o-down/01-indent.md) (do not name that project
in plans, CRs or PRs), [parity-with-markdown-studio-extension](parity-with-markdown-studio-extension/01-request.md),
[parity-with-obsidian](parity-with-obsidian/intent.md).

## Accepted → `02-backlog/P1/`

| Item | Feature | Notes from the user |
| --- | --- | --- |
| [extended-syntax-modes](../../2-backlog/P1/extended-syntax-modes/01-intent.md) | Strict, GFM, Extended (tick MyST, Obsidian, Pandoc, Typora) | Pastel background on the icons links each toolbox option to its family. Base of the syntax items. |
| [highlight-sup-sub](../../2-backlog/P1/highlight-sup-sub/01-intent.md) | `==x==`, `^x^`, `~x~` | |
| [wiki-links-full](../../2-backlog/P1/wiki-links-full/01-intent.md) | Wiki links with name resolution and autocompletion | |
| [embeds-transclusion](../../2-backlog/P1/embeds-transclusion/01-intent.md) | `![[note]]` embeds | |
| [obsidian-comments](../../2-backlog/P1/obsidian-comments/01-intent.md) | `%%…%%` | |
| [tags](../../2-backlog/P1/tags/01-intent.md) | `#tag` chips | Click opens VS Code search. |
| [block-references](../../2-backlog/P1/block-references/01-intent.md) | `^id` | |
| [toc-marker](../../2-backlog/P1/toc-marker/01-intent.md) | `[[toc]]` | Document only. |
| [readme-html-guaranteed](../../2-backlog/P1/readme-html-guaranteed/01-intent.md) | README HTML (`<div align="center">`…) | |
| [heading-folding](../../2-backlog/P1/heading-folding/01-intent.md) | Fold sections | |
| [find-in-preview](../../2-backlog/P1/find-in-preview/01-intent.md) | Ctrl+F | |
| [replace-from-preview](../../2-backlog/P1/replace-from-preview/01-intent.md) | Replace | |
| [paste-url-as-link](../../2-backlog/P1/paste-url-as-link/01-intent.md) | URL paste → link / image | |
| [drop-file-as-link](../../2-backlog/P1/drop-file-as-link/01-intent.md) | Drop from Explorer → link | |
| [rich-diff-side-by-side](../../2-backlog/P1/rich-diff-side-by-side/01-intent.md) | Per-block side-by-side diff | Bar by default; toolbar toggle; "que en mode …" cut off — confirm the mode. |
| [spell-check-edit-mode](../../../2-backlog/P3/spell-check-edit-mode/01-intent.md) | Spell check | Edit mode only; toolbar toggle + language; dedicated CR. |

Ctrl+D multi-caret: merged into [raw-editor-bold-italic-styling](../../../2-backlog/P3/raw-editor-bold-italic-styling/01-intent.md)
(CodeMirror 6 block editor).

## Rejected

Right-hand TOC panel, backlinks, hover preview of links, Markdown shortcuts while typing
(`# `, `- `), YouTube/GitHub cards, custom CSS, HTML/PDF export and print.

## Not proposed (VS Code or the extension already covers it)

Tabs, sessions, file tree, workspaces, external change detection, slash menu, sticky headings,
GitHub alerts, math, Mermaid, emoji picker, image paste, rich paste, lossless editing.

## Second triage by the user (2026-10-27)

The user removed the Extended-mode syntax items (extended-syntax-modes, highlight-sup-sub,
wiki-links-full, embeds-transclusion, obsidian-comments, tags, block-references) and moved
spell-check-edit-mode to P3. Precisions: README HTML renders final in read mode and shows its tags
as blocks in edit mode; new P1 [edit-mode-tag-in-block-title](../../2-backlog/P1/edit-mode-tag-in-block-title/01-intent.md);
the `[[toc]]` marker gets a palette icon, a `[[toc]]` block in edit mode and the clickable table in
read mode.
