## Summary

On a planning surface that holds several projects, the board's project picker lists the surface itself ("All projects") as its first item. Clicking it did nothing unless the board already showed Home, because only Home has an overview page and the router moved the choice straight back to the last real project. The surface item also looked like one more project row, although it is the umbrella of the projects under it.

This PR makes the click open the overview from any page, and turns the surface item into the menu's header, set apart from the project rows.

## Deliverables

- **Click fix.** Choosing the surface item from Costs, Triage, Kanban, Batch, PRs or Configuration now opens `?p=*&v=home`. Back returns to the page left. The router is untouched: an address typed by hand, or restored at boot, still resolves as before.
- **Header look.** The menu opens with the surface as a header (grid icon, its name in bold, a grey line "overview · N projects"), then a separator, then the projects slightly indented with regular-weight names. The old "Planning surface · N projects" caption is gone.

| Before (base `33a2305`) | After (`carried from 18d82a0`) |
| --- | --- |
| ![Before, PC](./verifier/evidence/before-picker-pc.png) | ![After, PC](./verifier/evidence/after-picker-pc.png) |
| ![Before, phone](./verifier/evidence/before-picker-phone.png) | ![After, phone](./verifier/evidence/after-picker-phone.png) |

The menu open on a project's Kanban page in a real browser, at PC and phone width, on the demo planning surface.

## Blast radius

Grade: 1. Web frame only (one click handler, one menu template, its CSS and one new word in both languages). A plain `git revert` restores the previous picker.

## Autonomous decisions

None.

## Known gaps

- A surface with a single project (no menu) was not run in a browser; it rests on the unchanged `canPick` guard.

<details>
<summary>Details</summary>

## Changes

- `js/main.js`: the picker's `[data-project]` click goes to `{ project: ALL, view: overviewIds()[0] }` when the surface is chosen from a view that has no overview; otherwise as before.
- `js/ui/picker.js`: the menu draws the surface header button, a separator, then the project rows; the caption is removed.
- `css/picker.css`: header, separator and project indent rules; the `.cap` rule is removed.
- `js/i18n/en.js`, `js/i18n/fr.js`: one new key, `project.overview`.
- `docs/web-board.md`: the picker's description updated.

## Impacts

The picker's menu looks different on PC and phone (header, separator, indented projects); the screenshots above show it. No change to the trigger button or to the overview page.

## Test plan

- [x] No behaviour change in Python; the web frame's checks cover the word files' shared keys
- [x] Local gates: `just check` (pass at 33a2305 plus the change, before the commit)
- [x] Evidence: before at `33a2305`, after at `carried from 18d82a0`
- [x] Review: approved at `carried from 18d82a0`
- [x] Verified at `carried from 18d82a0`: steps 1-5 of the manual check in a real browser; step 6 not run
- [x] CI green at `carried from 18d82a0`: all 5 jobs pass, `just scenario (ubuntu-latest)` included

## Internal references

- CR-324 board-picker-surface-item

</details>
