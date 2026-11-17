---
type: cr-answers
description: The user's answers on reading the large-screen feedback screenshots of the web board.
---

# Answers

## ui-feedback-Q1: the multi-project home (home-multiproject.png)

2026-11-16, the user chose: the selector is the surface. The selector at the top left shows the
surface (name and path, a multi-project surface) instead of "All projects"; each project's line
shows where the project is declared (its path).

## ui-feedback-Q2: the compressed side panel (compressed-sidepanel.png)

2026-11-16, the user chose: too narrow. On a large screen the panel is too narrow; its content
(a round file's table) is compressed and overflows.

## ui-feedback-Q3: the other three screenshots

2026-11-16, the user confirmed the Chief of Staff's reading: the side panel stays open when the
view changes; hovering a Triage card makes a horizontal scroll bar appear; the Triage backlog
cards are far wider than on other pages, and a card's preview shows the raw frontmatter.
The request is written in intake/request.md.

## The specification's open questions (first run), 2026-11-16

- Q4, the user chose the recommended answer: each project's line shows both paths: its folder
  in the surface (`projects/<name>/`, relative to the surface the selector shows) and its code
  repository as `checkout.yml` names it.
- Q5, the user chose the recommended answer: the selector shows, under the surface's name and
  path, "Planning surface · N projects", without opening the menu.

## The spec critic's questions, 2026-11-16

- Q6: the inbox item board-triage-polish asks for the same fix differently ("the items in the
  middle column are too wide: give them the same width as in the Inbox column, several per row
  (a grid)"). The user chose: the grid here. This CR caps the Triage cards and lays the backlog
  out as a grid of several capped cards per row; board-triage-polish no longer owns the width.
- Q7, the user chose the recommended answer: two CRs. This CR (ui-feedback-large-screen): the
  large-screen fixes (the panel closes on a view change, no hover scroll bar, the Triage card
  width and grid, the wider panel) and the raw frontmatter in a card's preview. The surface in
  the selector and each project's two paths (point 5, its docs and pictures, Q1, Q4, Q5) are
  their own CR, `board-surface-selector`.

## Grilled enough

2026-11-16, the user: grilled enough; the spec-writer writes the specification.

- Spec critic: yes.
