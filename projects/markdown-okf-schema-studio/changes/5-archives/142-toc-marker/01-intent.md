> **Superseded in part (2026-10-27):** the marker is `[TOC]` / `[[_TOC_]]` (and MyST `{contents}`), not `[[toc]]`. See "Scope change" in [00-request.md](00-request.md).

# `[[toc]]` marker: a table of contents of the document where the marker is

Type: feat · Priority: P1 · Filed 2026-10-27 from the parity grill with the user ([decisions](../../../4-archives/136-parity-grill/decisions.md))

## Expected

- `[[toc]]` on a line of its own renders the document's headings as a nested, clickable list;
  `[[toc depth=2]]` limits the depth. Document scope only (user decision). Generated, never
  written into the file: only the marker is saved.
- The list updates when headings change.
- **An icon** in the edition palette and a slash command (`/toc`) insert the marker.
- **Edit mode**: the marker is shown as an admonition-like block titled `[[toc]]` (see
  [edit-mode-tag-in-block-title](../edit-mode-tag-in-block-title/01-intent.md)), not the generated list.
- **Read (preview) mode**: the rendered table of contents, every entry a clickable link to its
  heading.

Proof: unit tests of the parser/renderer, a webview or e2e test of the interaction, and before/after real-window screenshots (cream + one dark theme). The source file is never rewritten outside the edited span.
