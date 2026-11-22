## Summary

The README, the user docs, the diagrams and the board screenshots still described chantier as it was days ago: the old board command name, a factory mode that no longer exists, an `order drop` that sends a CR to the inbox, no Help or Inbox page, and no picture of the surface server. This brings them in line with what the batch delivers, and with what merged since each page was last reviewed.

## Deliverables

- A new diagram, `docs/surface-server.svg` (with its `-texts.md`): the planning folder as the only truth, the one server process (web board and API, forge hub, writer), the sessions' watchers and the clients. Linked from the web-board page, the contributing guide and the README; `how-chantier-works.svg` gains a small server box that points to it.
- Wrong diagrams fixed, SVG and `-texts.md` together: `batch-lifecycle.svg` was invalid XML (a missing `<defs>`), `cr-lifecycle` and `cr-lifecycle-simple` show the destinations of the "grilled enough" step and of `order drop`, `cr-folder-lifecycle`'s description matches its texts file.
- Pages corrected: README, `docs/web-board.md` (a new Help section, `serve`/`webui`, keys), `docs/planning-folder.md` (waits, leases, `access`), the three use-case pages, the tutorial, `docs/agents-and-models.md`, and the "How the project is built" part of CONTRIBUTING.md.
- Pictures: `just docs-screenshots` was run once; two new pictures (`help-pc.png`, `help-phone.png`) and the existing board pictures retaken, which differ only by the sidebar's new Inbox and Help entries or the phone's bottom bar.
- Choices: the board's Help texts needed no edit (none was made false), so there is no code change; the batch Kanban gets no new diagram (`cr-folder-lifecycle` already draws its three folders); `docs/batch-pace.svg` is left untouched, as the user asked earlier.

## Blast radius

Grade: 1. Documentation, pictures and one screenshot script step; no behaviour change. A plain revert restores the previous pages.

## Autonomous decisions

- The retaken board pictures that differ only by the new sidebar entries are kept, since the sidebar is part of what the picture shows.
- No `history-pc.png` / `history-phone.png` were added: no page uses them.

## Known gaps

- `docs/costs.md`'s figure for the board's Griller tokens is still unverified; left as is.
- `docs/direct-mode-session.png` and `docs/status-report-done.png` are real session captures this change does not retake.
- The retaken board pictures are in the diff (`docs/web-board/`), not uploaded as before/after attachments.

<details>
<summary>Details</summary>

## Changes

- `README.md`, `CONTRIBUTING.md` (its "How the project is built" part), `docs/web-board.md`, `docs/planning-folder.md`, `docs/use-cases*.md`, `docs/tutorial-claude-code.md`, `docs/agents-and-models.md`.
- `docs/*.svg` and `docs/*-texts.md` of the diagrams above; new `docs/surface-server.svg` and its texts.
- `scripts/docs_screenshots.py`: a Help step after the Inbox's; `docs/web-board/*.png` retaken.

## Impacts

Readers see the commands, states, roles and board views of the current release. No behaviour change.

## Test plan

- [x] No behaviour change; `just check` passes (links, anchors, board design tests)
- [x] Local gates at `4c99436`: `just check` pass (2140 passed); local `just scenario` failed one step (the `webui` check) because the user's own board holds port 8765 on this machine; the pipeline's scenario passed at the head
- [x] Evidence at `4c99436`: anchors (186 links, 0 problems), SVG parse, description equality and renders, removed-words search, a privacy pass over the pictures (no path, name, email or key)
- [x] Review: approved at `4c99436` (reviewed at bfdf5a2, carried over a clean rebase)
- [x] Verified at `4c99436`
- [x] CI green at `4c99436`: all 5 checks pass

## Internal references

CR-447 docs-gardening.

</details>
