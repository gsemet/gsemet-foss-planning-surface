# Edit mode: HTML blocks, comments and TODOs show their literal tag as the block title

Type: feat · Priority: P1 · Filed 2026-10-27 from the parity grill with the user ([decisions](../../../4-archives/136-parity-grill/decisions.md))

## Problem

In edit mode an HTML comment or a TODO comment is shown as an admonition-like block, but its title
is a word ("TODO"), not the syntax that produced it. The user wants to see the "tag" itself:

![The edit-mode block of a TODO comment titled "TODO"; the user's note: replace it with <!-- TODO -->](evidence/image-todo-title.png)

The user also doubts that TODO comments are detected correctly: a TODO is **an HTML comment whose
text starts with `TODO`** (`<!-- TODO: cite the slop zone below -->`, case and the `:` optional,
single or multi-line). Check the current detection against that rule first and fix it.

## Expected

In edit mode, the title of the block is the literal opening syntax, in code font:

| Source | Edit-mode title |
| --- | --- |
| `<div align="center">` … `</div>` | `<div align="center">` (the real opening tag, attributes included, shortened with `…` when long) |
| any other HTML block element (`<details>`, `<p align>`, `<picture>` …) | its opening tag |
| `<!-- text -->` | `<!-- -->` |
| `<!-- TODO … -->` | `<!-- TODO -->` |

- The body of the block shows the content (comment text, or the inner Markdown/HTML) as today.
- Read mode is unchanged: comments stay hidden (or as today), HTML renders as final output (see
  [readme-html-guaranteed](../readme-html-guaranteed/01-intent.md)).
- Same rule for any other "tag-like" block shown this way in edit mode (for example the `[[toc]]`
  marker of [toc-marker](../toc-marker/01-intent.md) is titled `[[toc]]`).

Proof: unit tests of the parser/renderer, a webview or e2e test of the interaction, and before/after real-window screenshots (cream + one dark theme). The source file is never rewritten outside the edited span.
