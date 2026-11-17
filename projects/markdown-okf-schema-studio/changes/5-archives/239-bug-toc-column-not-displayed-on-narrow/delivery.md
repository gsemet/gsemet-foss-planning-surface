# Report: CR 239

Status: **done** (2026-11-03, branch `change-requests/239-bug-toc-column-not-displayed-on-narrow`, PR [#287](https://github.com/gsemet/markdown-okf-schema-studio/pull/287), merged by the owner as 25161145 and ac32bda4, top of stack #288).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 round 1 | With the TOC toggle on and a pane narrower than 760 px, a thin rail on the right shows one tick per heading with the current section highlighted; hover or focus opens the TOC as an overlay (closes 300 ms after the pointer leaves, or on Escape); a click on a tick goes to the heading. Wide panes unchanged. | 25161145 |
| T1 round 2 | The log entry moved under the single `2026-11-03` heading with a sub-heading (CI lint W5 on a non-ISO heading). | ac32bda4 |

Requirements: SwRS TOOLBAR-037 updated, scope index regenerated, dated entry in `requirements/tiers/log.md`.

## Proof of completion

- Six new tests fail on the old code; `toolbar-navigation` simulated visual group passed. CI run 41636767261 green on the final head (round 1 run 41635067225 failed on the log lint only).
- Reviews: APPROVE in rounds 1 and 2 (2 of 3 rounds). Real-window jobs not run (manual).
- Screenshot (light, 460 px) on branch `change-requests/239-bug-toc-column-not-displayed-on-narrow-assets`; no dark PNG exists.

## Open items

- Scenario ids v28 and v29 still say "hidden-narrow".
- `capture_layout_checks.py` is at 1499 of 1500 lines.
- The overlay's top edge touches the open toolbar tooltip at 460 px; content is not padded for the 16 px rail; the window-level Escape handler could swallow another handler's Escape while the overlay is open.
