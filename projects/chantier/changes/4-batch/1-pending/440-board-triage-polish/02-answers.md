---
type: cr-answers
description: A scope note on the Triage card width, now owned by ui-feedback-large-screen.
---

# Answers

## Scope note from ui-feedback-large-screen (2026-11-16)

The user chose (ui-feedback-large-screen, Q6): the Triage cards' width and the backlog's grid of
several cards per row are done in the P1 CR ui-feedback-large-screen. This item no longer owns
"the items in the middle column are too wide ... several per row (a grid)"; its other points
stand.

## Scope note from board-visual-refresh (2026-11-17)

The user chose (board-visual-refresh, visual-refresh-Q11): the sticky header's thin border and
light shadow on scroll are done in the P1 CR board-visual-refresh. This item no longer owns the
"Every page" point; its Triage points (the collapse per priority, the "writes since your last
rescan" explanation) stand.

## UI night (2026-11-21)

- ui-night (2026-11-21, the user's words): "rajoute dans le batch tout ce qui dans le backlog ou inbox concerne la UI. tu grille avec un fable, tu peux me demander les directions generales et les regles que tu penses que fable peut ne pas avoir compris, mais le but est d avoir une UI fonctionnelle". Destination: batch-30. The grill's questions are answered by a Fable advisor in the user's place; the goal is a working UI.
- ui-night scope (2026-11-21, the user): "Tout": the six web-board items (Batch view, Triage polish, Help page, History page, the user's Inbox, Dashboard pages), board-griller and the live TUI.
- ui-night act (2026-11-21, the user): the user's Inbox "act" opens links only (the PR on the forge, the question in its session, the CR); snooze, later and discard are kept by the board; AGENTS.md's rule stands (the board edits no batch, messages no agent).

## Grill by the Fable advisor (2026-11-21)

Read on the code of `main` (3b3eba06): the lanes' grid is there (`column-grid`), the sticky head has
its shadow on scroll (`.head.scrolled`), no collapse exists, and the rescan explanation exists only
as a small note at the bottom of the journal panel, after a click (`journal.note`).

6. triage-polish-Q1 (2026-11-21, Fable advisor): **What is left.** Two points only: the collapse per priority row, and the explanation of the writes count. The cards' width and the sticky header are done on `main` and are not reopened. Reason: least scope; the two scope notes above already say so.
7. triage-polish-Q2 (2026-11-21, Fable advisor): **Which rows collapse.** The four rows P1 to P4 of Triage's Backlog column, each on its own. Not the Inbox, not `3-ready`, not CR-427's "running batch" half, not the Kanban page, not Home. Reason: it is what the user asked ("for each priority"), and the other columns are what the user acts on.
8. triage-polish-Q3 (2026-11-21, Fable advisor): **What a collapsed row shows.** Its head stays: the priority chip, the count, the grill-state counts, and a chevron that says open or closed. Its post-its, its groups and its empty-row text are hidden. Reason: the user must still see how much a hidden row holds.
9. triage-polish-Q4 (2026-11-21, Fable advisor): **How to collapse.** A click on the row's head (the chevron is a real button: keyboard, `aria-expanded`, a label in both languages). No "collapse all" or "open all" control. Reason: four rows; one more control is not worth its place.
10. triage-polish-Q5 (2026-11-21, Fable advisor): **Default and memory.** All four rows open by default. The choice is kept on the device (the browser's own storage, as the batch page's view in CR-434), one choice per row, the same for every project, across reloads. Nothing is written in the planning folder or on the server. Reason: a view preference, not project data; the simplest thing that survives a reload.
11. triage-polish-Q6 (2026-11-21, Fable advisor): **A drop on a collapsed row.** The collapsed head is a drop target: a post-it or a group dropped on it goes to that priority, as on the open row; the row stays collapsed and its count changes. The selection bar's "move to P<n>" works the same. Reason: no surprise; a collapsed row must not become a place nothing can reach.
12. triage-polish-Q7 (2026-11-21, Fable advisor): **Selected post-its in a row being collapsed.** They leave the selection. Reason: the selection bar must never act on post-its the user does not see.
13. triage-polish-Q8 (2026-11-21, Fable advisor): **The label filter and the counts.** Unchanged: a collapsed row's count and grill-state counts are those of the open row under the same filter. An empty row collapses like any other; no row collapses or opens by itself (not when empty, not when a write lands in it). Reason: consistent with today; nothing moves without the user.
14. triage-polish-Q9 (2026-11-21, Fable advisor): **Where the writes count is explained.** In the journal panel that the button opens, as its first lines, above the list (today's small note at the bottom is replaced), and as the button's tooltip in one sentence. The button keeps its place, its count and its two tones. No new page, no dialog, no link to the Help page (board-help-page may explain more; neither CR needs the other). Reason: "in the board itself", where the user looks when the count puzzles them.
15. triage-polish-Q10 (2026-11-21, Fable advisor): **What the explanation says.** Three things, in plain words, in this order. What: the count is the changes made from this board (moves, new ideas, labels, groups) since the user last pressed the panel's button; each is already saved in the planning folder, nothing is lost or pending. Why: the board never messages the Chief of Staff (AGENTS.md); a Chief of Staff session whose watcher runs learns of these changes by itself; one without a watcher, or one that planned before the changes, does not. What to do: type "rescan" in the Chief of Staff's chat, it reads the backlog again and says what moved; then press the button to count again from zero. Reason: the user's three asks (what it is, why ask, what to ask), and true to the Chief of Staff card's "rescan" line, which says the watcher already brings the writes.
16. triage-polish-Q11 (2026-11-21, Fable advisor): **The count and its button stay.** The count, the list, the "I said 'rescan' to the CoS" button, the "modified" mark on post-its and Home's "Written by the board" tile behave as today; only words change (the panel's text, the tooltip, and the button's label if a clearer one fits the same place). The board does not show whether a watcher runs. Reason: the user asked to explain it, not to remove or rework it; removing it is its own decision.
17. triage-polish-Q12 (2026-11-21, Fable advisor): **Languages.** English and French for every new or changed text, the same keys in both; French says "tu" as the board does. Reason: the request, and the board's rule.
18. triage-polish-Q13 (2026-11-21, Fable advisor): **Outside the web client.** Nothing: no server, protocol, CLI, card or AGENTS.md change. `DESIGN.md` is read first and kept true (the lane's collapsed state, the panel's text); the board's screenshots of Triage are retaken if they show the changed parts. The pane's screenshot rule does not apply (the CR board pane is not touched). Reason: both points are drawing and words.
19. triage-polish-Q14 (2026-11-21, Fable advisor): **Phone widths.** The same collapse and the same text at phone widths; the head is large enough to tap. Reason: one behaviour everywhere.
20. triage-polish-Q15 (2026-11-21, Fable advisor): **Batch-30 neighbours.** No overlap of behaviour: CR-427 changes the last column (its two halves) and removes `triage.running` / `triage.idle`; CR-433, 434 and 435 are the batch page; CR-429 is the server's watching. This CR shares files with CR-427 (`js/ui/column.js`, `js/triage/columns.js`, `css/components/column.css`, `css/views/triage.css`, the same DESIGN.md paragraph) and is written on the lanes as CR-427 leaves them; a shared file is no dependency (no `depends.json`), the stack's order settles the rebase. Reason: the user's rule, use the slots, depend only on a real need.
21. triage-polish-Q16 (2026-11-21, Fable advisor): **Risks.** A collapsed row forgotten with urgent items in it: answered by the head's count and grill-state counts (Q3) and the open default (Q5). A stored choice from an older page: an unknown or broken stored value reads as "open". Reason: the safe side is to show.

Restatement (2026-11-21, Fable advisor): on Triage, each of the four priority rows P1 to P4 collapses on a click on its head, which keeps its chip, count, grill-state counts and a chevron; open by default, the choice kept on the device for all projects; a collapsed row still takes drops and moves, and its selected post-its leave the selection; no other column collapses and nothing collapses by itself. The "N writes since your last 'rescan'" button keeps its count and behaviour; its panel opens on a plain explanation (what the count is and that all is already saved, why the Chief of Staff may not know, what to type: "rescan", then the button to count from zero), with a one-sentence tooltip on the button. English and French. Web client only, DESIGN.md kept true; no server, CLI, card or AGENTS.md change; no dependency on CR-427, whose lanes it is written on. The cards' width and the sticky header are already done and stay out.

Grilled enough (Fable advisor): yes; destination batch-30.

Spec v1 (2026-11-21): written (`03-change-spec.md`); four open questions, each built as its option A: `docs/web-board.md` updated, the button label kept, the explanation names the kinds "for example", `selectedNow` also drops post-its in a folded row.

Q17 (2026-11-21, the Chief of Staff, from Q7's reason): folding a row removes from the selection only the post-its drawn in that row, never a marked CR drawn in CR-427's 'Running batch' half (the selection loses only what the user no longer sees).

Spec v2 (2026-11-21): `03-change-spec.md` revised on the spec critic's seven findings: `toggleFold` deselects only what is drawn in the folded row (`columnOf`, Q17); `journal.why` says "watcher (or pull path)" and drops "or one that planned before them"; `journal.what` says "already saved in the planning folder on this machine"; DESIGN.md's lane sentence gains "and its fold chevron" (rebase on that line); overlaps name `docs/web-board.md`, the three Triage screenshots (whichever lands second reruns `just docs-screenshots`) and CR-434's DESIGN.md lines; `lane()` names CR-427's `name`, `sub`, `idle`, `foot` and the three new parts; test paths in full. The four open questions stand.

Spec final (2026-11-21, the Chief of Staff): v2 applies the critic's findings 1 to 7 (Q17 from Q7's reason; Q10's wording corrected to match docs/web-board.md); destination batch-30.
