---
type: cr-answers
description: A scope note: three points of this item are done in the P1 CR board-visual-refresh.
---

# Answers

## Scope note from board-visual-refresh (2026-11-17)

The user chose (board-visual-refresh, visual-refresh-Q9): the P1 CR board-visual-refresh follows
this item on three points and delivers them: no "Merged PR" column, no grouping by state (each CR
keeps one position; its state shows by its colour plus a badge in the top right corner), and no
": after level 0". This item keeps the rest: the batch history navigation (previous / next), the
connected cards and their arrowheads, and the tooltip on the batch mode. The P1 CR
cost-receipt's batch chooser was split off as the inbox item cost-receipt-batch-chooser, to move
through batches the same way as this item's navigation.

## Scope note from board-batch-navigator (2026-11-17)

The user chose (board-batch-navigator, scope-Q1): the batch history navigation (previous /
next) is done in board-batch-navigator, with the same navigator as the Costs page. This item
keeps the connected cards, their arrowheads and the tooltip on the batch mode.


## UI night (2026-11-21)

- ui-night (2026-11-21, the user's words): "rajoute dans le batch tout ce qui dans le backlog ou inbox concerne la UI. tu grille avec un fable, tu peux me demander les directions generales et les regles que tu penses que fable peut ne pas avoir compris, mais le but est d avoir une UI fonctionnelle". Destination: batch-30. The grill's questions are answered by a Fable advisor in the user's place; the goal is a working UI.
- ui-night scope (2026-11-21, the user): "Tout": the six web-board items (Batch view, Triage polish, Help page, History page, the user's Inbox, Dashboard pages), board-griller and the live TUI.
- ui-night act (2026-11-21, the user): the user's Inbox "act" opens links only (the PR on the forge, the question in its session, the CR); snooze, later and discard are kept by the board; AGENTS.md's rule stands (the board edits no batch, messages no agent).

## Grill (2026-11-21, Fable advisor, in the user's place)

1. batch-view-Q1 (2026-11-21, Fable advisor): **What is left to do.** Two points only: the arrows of the graph when a CR waits for several others (with what makes a CR's dependencies readable), and the tooltip on the three modes. Checked on the code at `3b3eba06`: the navigator is there (`js/ui/batch-nav.js`), the PR column has no Merged section, each CR keeps its place in its level with a state badge, and the level heads say "Level N" (`batch.level`); those four points are dropped. Reason: the scope notes above, confirmed on the code.
2. batch-view-Q2 (2026-11-21, Fable advisor): **Redesign of the connected cards, or repair.** Repair. The graph keeps its shape from board-visual-refresh (levels as columns, one place per CR, white cards, grey arrows, the hover light); no new layout, no new view, no new library. Reason: the user asked to keep the purpose and make it work, and the goal tonight is a working UI with the least scope.
3. batch-view-Q3 (2026-11-21, Fable advisor): **A CR that waits for several others.** All its arrows arrive at one point, the middle of its card's left edge, level, and show one arrowhead there, whole and touching the card; no head floats apart, sits under a card or points across another. The same holds for two sources and for seven. Reason: this is the user's complaint (CR-275), and one shared entry point is the simplest picture that reads right.
4. batch-view-Q4 (2026-11-21, Fable advisor): **Following a CR's dependencies.** Hover or focus on a CR lights it, what it waits for and what waits for it, as today; the lit arrows are then drawn whole, above the cards they cross, so an arrow that skips a level can be followed from end to end. Unlit, the arrows stay behind the cards as today. Nothing else is added (no list of dependencies on the card, no click to pin). Reason: it is the one place where the picture still hides a dependency, and it reuses the light the page already has.
5. batch-view-Q5 (2026-11-21, Fable advisor): **The Gantt's arrows.** Not changed. Reason: the user's complaint is about the connected cards; the Gantt gets no new rule.
6. batch-view-Q6 (2026-11-21, Fable advisor): **Where the mode tooltip sits.** On each of the three words of the Stack / Series / Parallel switch, as CR-435 (board-batch-compact) leaves it in the title row. It is a tooltip of the page's own kind (the legend pill's: shown on hover and on keyboard focus), not a browser title. The mode pill's own tooltip (the mode's sentence, CR-435) is not changed. Reason: the user named the three words, and the page has one tooltip pattern.
7. batch-view-Q7 (2026-11-21, Fable advisor): **The tooltip's words.** On a mode the batch is not in: `To switch, ask the Chief of Staff to "change the batch to <mode>"`, the mode named in the sentence (stack, series, parallel). On the batch's own mode: "This batch's mode." Both in English and in French, the quoted order in the board's language. Reason: the user's sentence; asking to switch to the mode already on would be noise.
8. batch-view-Q8 (2026-11-21, Fable advisor): **The switch stays words only.** A click on a mode does nothing, as today: the board edits no batch and messages no agent (AGENTS.md); the Chief of Staff switches, on the user's word (`order mode`). Reason: the project's rule.
9. batch-view-Q9 (2026-11-21, Fable advisor): **A closed batch.** Its three mode words carry no switch tooltip (a closed batch cannot change mode); its graph gets the same arrows and light as a live one. Reason: no promise the board cannot keep.
10. batch-view-Q10 (2026-11-21, Fable advisor): **The phone.** Nothing new: the switch is hidden at phone width (as today and in CR-435), so its tooltip is too; the graph's arrows follow the same rules at every width. Reason: least scope; the mode pill and its sentence stay on the phone.
11. batch-view-Q11 (2026-11-21, Fable advisor): **Evidence.** batch-18's record (`5-archives/batches/batch-18.json`) keeps no dependencies (no `after` on its CRs), so CR-275 cannot be shown from it. The proof is a Batch graph with a CR that waits for at least three others in different rows, and one arrow that skips a level: the board's demo data, extended if it has no such CR, with before and after pictures in the PR, and the tooltip in English and French. If the pictures at the head already show Q3 right (board-visual-refresh redrew the arrows' ends on 2026-11-17), that point costs no code and the PR says so. Reason: the complaint was seen on a picture, so a picture settles it.
12. batch-view-Q12 (2026-11-21, Fable advisor): **Place in batch-30 and overlaps.** Queued after CR-435 (board-batch-compact), which it builds on (the title row's slot and its tooltip rules); it takes CR-433 and CR-434 as landed: they touch the same page (the card's chip, the Kanban tab) and none of this CR's points. CR-427 and CR-429 do not touch the Batch page. Web client only, with its `DESIGN.md` and `docs/web-board.md` kept true; no server, CLI, card or record change. Reason: one page, several CRs: the last one in takes the others as landed.
13. batch-view-Q13 (2026-11-21, Fable advisor): **Out of scope.** The Kanban, Gantt and Time cards views, the PR column, the figures, a clickable mode switch, any routing of the arrows around the cards, the CR board pane (`hooks/`), and every point delivered elsewhere (Q1). Reason: least scope, no overlap with batch-30.

Restatement (2026-11-21, Fable advisor): of the seven points filed, four are done (navigator, no Merged column, one place per CR with a badge, "Level N"); this CR delivers the last two on the Batch page of the web client, in English and French. One, the graph: a CR that waits for several others gets all its arrows at one point of its left edge under one whole arrowhead, and on hover or focus the lit arrows are drawn above the cards so a dependency across a level can be followed; the layout, the Gantt and the rest stay. Two, the modes: each of the three words of the switch in the title row (as CR-435 leaves it) carries a tooltip, `To switch, ask the Chief of Staff to "change the batch to <mode>"` on the two other modes and "This batch's mode." on its own, none on a closed batch, none on a phone where the switch is hidden; the switch stays words only, the board edits no batch. Proof by pictures on demo data with a CR waiting for at least three others. Queued in batch-30 after CR-435.

Grilled enough (Fable advisor): yes; destination batch-30.

## Spec v1 (2026-11-21, spec-writer)

- Spec v1 written (`03-change-spec.md`): one arrowhead per waiting CR (no marker per arrow on the graph), the lit arrows copied into a layer above the cards (`svg.edges.top`), a tooltip on each word of the mode switch (`mode.switch_to`, `mode.current`, none on a closed batch), the demo's CR-148 made to wait for CR-141, CR-145 and CR-146. Two open questions, A built: the French wording (A: « passe le batch en {mode} », "tu", French mode word) and a shipped graph picture (A: `batch-graph-pc.png` added to `docs_screenshots.py`).

## Spec v2 (2026-11-21, spec-writer)

- Spec v2 written (`03-change-spec.md`), on the spec critic's five non-behavioural findings: the lit head declares `stroke: none` (`path.hl`'s stroke outranks `.head`); the copies and the class loops take the base layer only (`svg.edges:not(.top)`), and the measure selects `path[data-from][data-to="CR-148"]` there; the before and after pictures are taken unlit and with CR-148 hovered; the closed batch's arrows rest on the live graph and the shared `graphBlock` / `drawEdges` / `light` path (mobile-app's closed records hold no `after`), batch-01 serves only the switch's check; overlaps name CR-439, CR-440 and docs-gardening, and section 6 says the demo loses its next CR to start (CR-148's "next" tag and the "queued, next CR-148" line). No behaviour changed.

Spec final (2026-11-21, the Chief of Staff): v2 applies the critic's five non-behavioural findings; destination batch-30 after CR-435.
