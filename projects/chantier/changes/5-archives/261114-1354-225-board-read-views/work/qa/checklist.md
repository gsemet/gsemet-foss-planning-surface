# QA checklist (head 5e64960 plus the uncommitted round 3)

Shots: `shots/board-<view>-<pc|phone>.png`, `proto-...`, and `compare-<view>-<pc|phone>.png`
(prototype left, board right). Data: a scratch surface with a running batch (batch-17, 4 working,
8 handed back). Reason classes: S = the spec says so, L = live data against the snapshot,
O = out of this CR (another CR or the actions), P = prototype example data.

| View | Difference | Class |
|---|---|---|
| all | prototype lists example projects (exemple-web paused with PR links, exemple-api); the board lists the surface's own (api, chantier, web), sorted by name | P |
| all | board header says "0 PRs to review"; the prototype's count comes from its examples | P |
| home, kanban, batch | "+ New" button and Triage view absent: they act or belong to the Triage CR | O |
| home, batch | spent $109.28 against the snapshot's $98.64; "33 min ago" against "31 min": time passes | L |
| home, kanban | prototype is French, board English (language button; same keys in both) | S |
| home | no Autosync card or "Prototype" footer: simulated in the prototype only | S |
| kanban | no "Labels" filter row: it filters, a write of the page's own state, not in the read views | O |
| kanban, home | CR titles drop the "Change Specification: " prefix | S |
| costs | no v6 shot of Costs to compare against | P |
| phone | all views match the v6 phone layout (bottom bar, tinted All projects cards, full-screen panel with a 150 px tree) | none |

Fixed during QA: the first project read waited one 5 s poll (the page showed "Loading..."): the
refresh now asks at once on start (`core/refresh.js`). "1 batches running" and similar on All
projects: the four counts now have singular words in both languages.