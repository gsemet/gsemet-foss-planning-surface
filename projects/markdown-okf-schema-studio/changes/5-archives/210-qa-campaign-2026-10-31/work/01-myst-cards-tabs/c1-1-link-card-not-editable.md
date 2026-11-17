# c1-1 — A link card (`:link:`) cannot be edited in the preview: every click follows the link

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (single click, then double click; two runs) |
| Area | Inline editing, MyST grid cards |
| Modes | Side preview |
| Evidence | none needed (buffer and active editor) |
| Related | #230, #236 |
| Replay | `scenarios/c1-1-link-card-not-editable.json` |

## Use case

An author fixes the header, body or footer of a card that has `:link:` set (fixtures-visual/46-grid-cards.md, "Linked card").

## Steps to reproduce

1. Open `fixtures-visual/46-grid-cards.md`, open the preview to the side, switch edit mode on.
2. Click (or double click) the title, the header text, or the body of "Linked card".

## Expected

Same as the card without link: a block editor opens on the clicked part (title line, header, body, footer).

## Observed

The click navigates to `targets/alpha.md` (the group-1 editor switches to it). No textarea opens. The whole card acts as a stretched link, so no part of a link card is reachable by mouse in edit mode. Clicking a later key (End, text) then types into the link target file (dirtied `alpha.md` in my run).

## Impact

Link cards can only be edited in the source; typed keystrokes after the unexpected jump land in another file.

## Where it comes from

Card markup: `a.myst-grid-card-link[data-sphinx-preview-navigation]` inside `.myst-grid-card-title`, stretched over the card. Edit-mode click handling gives navigation priority.

## Suggested direction

In edit mode, open the editor on a click and keep navigation for a modifier click (Cmd/Ctrl) or a small link affordance.

## Test to add

Real-input E2E: edit mode on, click a link-card header, assert a block editor is open and the active file is unchanged.

## Done when

Replay passes: editor opens on the header, the visible editor stays on the edited file.

**Coordinator triage (2026-10-31).** QA210-02. Also covers
[c0-1](../10-noop-sweeps/c0-1-link-only-paragraph-not-editable.md)
(link-only paragraph, e.g. the "Next:" line of every chapter). Not mapping `:link:` cards is the
designed behaviour of #236 (SwRS-MDOKFSTUDIO-BLOCK-258); the finding is that no edit path is left.
