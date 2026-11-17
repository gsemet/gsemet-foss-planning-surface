---
type: cr-answers
description: The user's answers to the grill of the web board's visual refresh.
---

# Answers

Mock-ups: `prototypes/01-mockups/index.html` (13 options on one base, plus today's look).

## visual-refresh-Q1: the layout

2026-11-17, the user chose the recommended answer: layout A, the light sidebar (`prototypes/01-mockups/layout-a-sidebar-light.html`): a white sidebar with a hairline, the active item a grey pill, section captions in small capitals, a breadcrumb header.

## visual-refresh-Q3: colours and states

2026-11-17, the user chose the recommended answer: one deep accent, states as small dots or icons, the legend in a tooltip (`prototypes/01-mockups/colour-one-accent-dots.html`).

## visual-refresh-Q2: spacing

2026-11-17, after the three screenshots, the user chose the recommended answer: comfortable (`prototypes/01-mockups/spacing-comfortable.html`): an 8px rhythm on a 4px base, nav rows 36px, card padding 10/12px, text 14px.
## visual-refresh-Q5: cards

2026-11-17, the user chose the recommended answer: two-tone cards (`prototypes/01-mockups/cards-two-tone.html`): a white body, a grey band at the bottom for the metadata (rounds, PR, cost, folder, long gate), radius 14px, a diffuse shadow.

## visual-refresh-Q6: scope

2026-11-17, the user chose the recommended answer: every view (Home, Triage, Kanban, Batch, PRs, Costs with its receipt, Configuration), the docs screenshots redone; cost-receipt's ticket follows this style.

## visual-refresh-Q4: typography

2026-11-17, the user asked to see each choice visually first (screenshots sent), and to be shown every choice visually from now on. After the screenshots, the user chose the recommended answer: one sans-serif (Inter, shipped with the board), two weights (regular and medium), page titles 24px medium (`prototypes/01-mockups/type-inter-two-weights.html`).

## visual-refresh-Q7: every choice at once, and the critique

2026-11-17, the user asked for one mock-up with every choice on at least two pages; after it, the user asked: on the Batch page, drop the Merged column's "For information." label and the earlier batches' CRs (they add nothing), and a design critique of everything. The critique (`prototypes/01-mockups/critique.md`) was applied: one PR column (to review, then merged) so the graph is not clipped; no "Batch" figure card nor counters line under the title (the crumbs and the mode strip, "Stack · Foreman", say it); one "nothing to review" sentence; the picker's subtitle names the batch, not a cut path. The user approved the result as the specification's reference, to compare at delivery: `prototypes/01-mockups/final-batch.html`, `prototypes/01-mockups/final-costs.html`, `prototypes/01-mockups/final-costs-phone.html`, `prototypes/01-mockups/final-config.html`, with `prototypes/01-mockups/critique.md`.

Spec critic: yes, it changes what the user sees on every view of the board.

## Spec questions (2026-11-17)

- visual-refresh-Q8 (order): cost-receipt waits for this CR (`depends.json`); timing-settings runs in parallel (shared files only), whichever lands second takes the other's changes.
- visual-refresh-Q9 (board-batch-view, the user's inbox item): this CR follows it on three points: no Merged PR section, no grouping by state (each CR keeps one position; its state shows by its colour plus a badge in the top right corner), no ": after level 0". The rest of board-batch-view (history navigation, arrowheads, mode tooltip) stays in that item.
- visual-refresh-Q10 (split): no, one CR; the approved mock-up covers the restyle and the Batch view's content.
- visual-refresh-Q11 (sticky header): this CR takes it: the breadcrumb bar stays sticky with its hairline and a light shadow when the page scrolls; the point is removed from board-triage-polish.

## 2026-11-17, during batch-23

- The user, with a screenshot of the board's picker: a long project name (gentic-planning-surface) runs into the chevron, and the chevron sits low. Fix it in this CR: the name ends in an ellipsis with a gap before the chevron, the chevron centred. Folded into 03-change-spec.md (Picker, and Evidence).

