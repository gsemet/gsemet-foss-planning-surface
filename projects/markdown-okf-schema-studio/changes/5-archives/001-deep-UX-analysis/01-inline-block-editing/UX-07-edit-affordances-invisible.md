# UX-07 — Edit mode gives no visible affordance: no block outline, no Save/Cancel, no shortcut hint

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Observed on every block type |
| Area | Inline block editing |
| Evidence | [u05-click-paragraph.jpg](../evidence/u05-click-paragraph.jpg), [adm3-8.jpg](../evidence/adm3-8.jpg) |

## Use case

A first-time user toggles the pencil button and wants to understand what is editable, what they
are editing, and how to finish.

## Observed

- Hovering a block in edit mode changes only the cursor (`cursor: text`). There is no outline that
  shows which source range a click will open (a list item opens the whole list; an admonition
  title opens the whole directive with its `:::` fences).
- The open editor is a borderless textarea with a 2 px blue left rule. Raw Markdown sits at the
  same margin and in the same font as rendered text, so the boundary between "editing" and
  "rendered" is hard to see ([adm3-8](../evidence/adm3-8.jpg): the whole "Important" admonition
  panel disappears and is replaced by raw text).
- The README promises "Save applies changes … Cancel discards them", but no Save or Cancel
  control exists. The only exits are blur (save), Cmd/Ctrl+Enter (save), and Escape (discard,
  [UX-01](UX-01-escape-discards-autosaved-text.md)). None is shown.
- The status line under the textarea is empty while editing.

## Expected

A visible editing frame with a short hint, for example "Editing lines 134-138 · Enter newline ·
Cmd+Enter done · Esc revert", plus hover outlines that preview the editable range.

## Where it comes from

`src/preview/previewStyles.ts` L352-L375 (edit-mode styles: cursor only, editor has no frame);
`src/webview/scrollSync.ts` `receiveBlockEditSource` (L1657-L1738) leaves the status empty.

## Suggested direction

Add a hover outline on `[data-sphinx-source-line]` blocks in edit mode, a framed editor with a
background and a monospace font ([UX-08](UX-08-proportional-font-for-raw-source.md)), a status line
with the source range and the shortcuts, and explicit Done/Revert buttons.

## Test to add

Visual scenario: edit mode, hover a list item, capture; open the block, capture. An agent-reviewed
checklist item: "the edited block is visually distinct and shows how to finish".

## Done when

A first-time user can tell what a click will edit and how to finish without reading the README.
