# CR-447 garden inventory

Rounds 1 and 2 of 3. Baseline = the last commit that touched the file before this round (from `git log -1`), or a dated reason. Verdicts: holds, fixed, new, kept, out of scope.
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

Every pair passes `work/check_svgs.py` (XML parse, `<desc>` equal to the texts paragraph, visible text equal to the fenced blocks); changed ones rendered to `verifier/evidence/svg/` and looked at.

| Pair | Baseline | Verdict |
| --- | --- | --- |
| batch-lifecycle (.svg, -texts.md) | 99fa847f 2026-11-21 | fixed: the SVG was invalid XML (the `<defs>` open tag was missing); desc and texts now name the join destination (running or next batch), the 1-pending restart, and the close refusal for a parked, held or blocked CR |
| batch-modes | d6836e43 2026-11-15 | fixed (texts only): H1 now equals the SVG title; no factory mode drawn |
| cr-folder-lifecycle | ab2e44cf 2026-11-21 | fixed: desc drift (planning folder or external surface, archive in the PR). docs-garden-Q6 Kanban check: it already draws `1-pending`, `2-actives`, `3-done`; no SVG change owed, the Kanban is shown by the screenshot |
| cr-lifecycle | ab2e44cf 2026-11-21 | fixed: note box for the "grilled enough?" destination choice (next batch `3-ready/` or running batch `1-pending/`); `status --refresh` with no `--epoch`; park and `order hold` in desc and paragraph |
| cr-lifecycle-line | f8b33348 2026-11-14 | holds |
| cr-lifecycle-simple | ab2e44cf 2026-11-21 | fixed: Backlog box says P1..P4 set by you, then next batch or running batch as you choose |
| how-chantier-works | f7c18f1a 2026-11-20 | fixed: surface server block (board, hub, writer) pointing to surface-server.svg; spec critic text no longer clipped |
| how-chantier-works-simple-direct | f024c3bf 2026-11-14 | holds |
| how-chantier-works-simple-foreman | f024c3bf 2026-11-14 | holds |
| planning-modes | 4ed0d56c 2026-11-20 | fixed (texts only): H1 equals the SVG title |
| release-driver | ca3213f4 2026-11-14 | holds |
| surface-server (.svg, -texts.md) | none | new: the server's jobs (board and API with two keys, forge hub, writer), how it reads (fingerprint, watchfiles, 1 s / 5 s / 5 s check), session watchers, forge, remote; words from the code and AGENTS.md; linked from README, docs/web-board.md and CONTRIBUTING.md "How the project is built" |
| batch-pace.svg | ca3213f4 2026-11-14 | out of scope: the user said on 2026-11-07 it stays untouched, and no page links it |

## Pictures (round 2)

`just docs-screenshots` run once. `panel-phone.png` came out identical (nothing to restore). Every other changed picture differs because the sidebar now has the Inbox and Help entries (or, on the phone, the bottom bar does): a real change of the view, so all are kept.

| Picture | Verdict |
| --- | --- |
| web-board/help-pc.png, help-phone.png | new: the Help page, concept cards then role cards; linked from docs/web-board.md (cures round 1's missing-file failure) |
| web-board/home-pc, home-phone, writer-pc, writer-phone | kept: tiny diffs, the sidebar with Inbox and Help |
| web-board/batch-pc.png | kept: Batch page on its Kanban tab (1-pending, 2-actives, 3-done, PRs to review and in draft); README caption already says "its CRs in the Kanban tab by stage": holds. docs-garden-Q6 Kanban check: done |
| web-board/batch-cards, batch-gantt, batch-graph, batch-phone, costs, editor, inbox, kanban, new, picker, project, triage, triage-selection, panel-pc, config (pc, phone) | kept: new sidebar (and phone bottom bar); config-pc shows the role table with the board-griller and retro-critic rows |
| web-board/panel-phone.png | unchanged by the run (identical) |
| web-board/history-pc.png, history-phone.png | not made: the History section has no picture in the docs; out of this CR's scope (finding for the Foreman) |
| docs/board-mod-*.png, direct-mode-session.png, status-report-done.png | kept: not touched, the pane did not change in batch-30 |
