# CR-447 garden inventory

Round 1 of 3 (text half). Baseline = the last commit that touched the file before this round (from `git log -1`), or a dated reason. Verdicts: holds, fixed, new, kept, out of scope. Every picture and SVG row is "round 2".
Post-spec merges checked on every text row: CR-449 Griller from the board, CR-456 `serve`/`webui` rename, CR-457 public read-only key, CR-458 remote CLI (`cli.run`, `login`), CR-460 paste field and cookies, CR-459 graph.

## Text pages

| File | Baseline | Touched by | Verdict |
| --- | --- | --- | --- |
| README.md | f7171e1f 2026-11-22 | CR-425 (running vs next batch), init/long-gate CRs, CR-458 branch | fixed: board caption said "stack mode, its CRs by level" but `batch-pc.png` is the Kanban tab; CR board paragraph names `webui`, the Griller and the read-only key; "Use" drop row names the destinations and `order hold`; "More" has one link per page (13, none added) |
| docs/web-board.md | bb8765a4 2026-11-22 | CR-449, 457, 459, 460 | fixed: `chantier board` (split over two lines) now `serve`; new `### Help` (picture `help-pc.png`, phone `help-phone.png`, round 2 makes both); read-only key and `chantier webui` added to "Starting the board"; Batch section says the picture is the Kanban tab, Graph tab holds the levels |
| docs/server-api.md | 29428f5d 2026-11-22 | CR-457, CR-458 | holds: read key, `cli.run`, griller ops, topics and terminal client all current |
| docs/boards.md | f7171e1f 2026-11-22 | CR-456 | holds |
| docs/planning-folder.md | dda590d9 2026-11-22 | CR-425, waits | fixed: new paragraph on typed waits, leases and `chantier access` (merged before batch-30, in no page); `board@1` row names the Griller's turns |
| docs/planning-modes.md | f7171e1f 2026-11-22 | CR-456 | holds |
| docs/use-cases.md | 3b3eba06 2026-11-21 | CR-425 | fixed: "Choose your configuration" said a direct-mode CR joins only once paused, against use-cases-direct and the README |
| docs/use-cases-direct.md | 99fa847f 2026-11-21 | CR-425 | fixed: Griller CRs "join once paused" contradicted `order add`; `order hold` and `unhold` added |
| docs/use-cases-foreman.md | 99fa847f 2026-11-21 | CR-425 | fixed: "Drop CR-104" row said `6-trash/` only (destination is yours, never the inbox); `order hold` / `unhold` row added |
| docs/tutorial-claude-code.md | 2a19b7de 2026-11-22 | CR-425 | fixed: "twelve agents" (`agents/` holds fifteen); drop row said `6-trash/` only |
| docs/agents-and-models.md | 86fe6966 2026-11-22 | model CRs | fixed: model table lacked the retro critic (Opus 5.5, as `config/chantier.defaults.yml`); "other keys" lacked `specifying.parallel`, `batch.slots`, `events.wake_every` |
| docs/gates.md | 2a19b7de 2026-11-22 | gate CRs | holds |
| docs/forge-connectors.md | 8330879a 2026-11-21 | issue/hub CRs | holds |
| docs/hosts.md | 0e36d1f8 2026-11-22 | host CRs | holds |
| docs/costs.md | 7dcf5a5a 2026-11-17 | none since | holds (a line on the Griller's tokens could not be verified; left out) |
| docs/release-process.md | 27fb50d9 2026-11-21 | release CRs | holds (read in part: first 40 lines; no term of the checks found) |
| CONTRIBUTING.md "How the project is built" (lines 6-213 only) | bb8765a4 | many | fixed: "There is no configuration file" was false (`chantier.yaml`); keys, `webui`, `login`, `cli.run` and the board's Griller added to the CLI paragraph. The rest holds. Outside the scope: not read |
| clients/web Help texts (`en-help.js`, `fr-help.js`, `help-topics.js`) | bb8765a4 | CR-449 | holds: no topic is made false (the "three ways" topic, the Griller topic and every `doc` link, checked by `work/check_anchors.py`); not edited, so no Help gate |

## Diagram pairs (round 2)

| Pair | Baseline | Verdict |
| --- | --- | --- |
| batch-lifecycle (.svg, -texts.md) | 99fa847f 2026-11-21 | round 2 |
| batch-modes | d6836e43 2026-11-15 | round 2 |
| cr-folder-lifecycle | ab2e44cf 2026-11-21 | round 2: docs-garden-Q6 check: it already draws `1-pending`, `2-actives`, `3-done`; the Kanban is shown by the screenshot, no SVG change owed for it |
| cr-lifecycle | ab2e44cf 2026-11-21 | round 2 |
| cr-lifecycle-line | f8b33348 2026-11-14 | round 2 |
| cr-lifecycle-simple | ab2e44cf 2026-11-21 | round 2 |
| how-chantier-works | f7c18f1a 2026-11-20 | round 2 |
| how-chantier-works-simple-direct | f024c3bf 2026-11-14 | round 2 |
| how-chantier-works-simple-foreman | f024c3bf 2026-11-14 | round 2 |
| planning-modes | 4ed0d56c 2026-11-20 | round 2 |
| release-driver | ca3213f4 2026-11-14 | round 2 |
| batch-pace.svg | ca3213f4 2026-11-14 | out of scope: the user said on 2026-11-07 it stays untouched, and no page links it |

All eleven pairs: round 2 reads each against the removed-words list (no hit found by round 1's search) and against the post-spec merges; a new `docs/surface-server.svg` pair is a round 2 candidate.

## Pictures (round 2)

| Picture | Baseline | Verdict |
| --- | --- | --- |
| docs/web-board/*-pc.png, *-phone.png (29 files: batch, batch-cards, batch-gantt, batch-graph, config, costs, editor, home, inbox, kanban, new, panel, picker, project, triage, triage-selection, writer) | 2026-11-17..22, see `git log` per file | round 2: retake all from the real board; Inbox, sidebar and Batch pictures are the ones the merges changed |
| web-board/help-pc.png, help-phone.png | none | new, round 2: referenced now in docs/web-board.md (`### Help`, "On a phone"); `check_anchors.py` reports `help-pc.png` as a missing file until round 2 |
| web-board/history-pc.png, history-phone.png | none | new, round 2: the History section has no picture (the view exists); add to the run |
| docs/board-mod-batch.png, board-mod-batch-done.png, board-mod-batch-prs-light.png, board-mod-merged-light.png, board-mod-waiting-light.png | not touched by this CR | kept: the pane's own pictures; no change to the pane in batch-30 |
| docs/direct-mode-session.png | not touched | kept |
| docs/status-report-done.png | not touched | kept |
