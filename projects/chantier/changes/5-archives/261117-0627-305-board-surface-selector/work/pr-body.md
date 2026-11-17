## Summary

On a planning surface with several projects, the web board's selector said "All projects" and gave no hint of where anything lived. It now shows the surface itself (its name and path, with "Planning surface · N projects" under them, menu closed), and each project's line shows where the project is declared: its folder in the surface and its code repository as the project's `checkout.yml` names it. A single project, in a folder or on a surface, shows no change.

## Deliverables

- The picker's button on the overview shows the surface's name in bold, its path, and "Planning surface · N projects"; the menu's first line shows the name and path; the view's title is the surface's name. "All projects" and "overview · N PRs to review" no longer show anywhere (the number of PRs to review stays in the overview's stats line).
- Each project's line (menu, overview table, phone cards) shows two labelled paths, `folder` (`projects/<name>/`) and `repo` (the `repo:` value as written in `checkout.yml`, `.repo` when there is none). A path too long for its place is cut with an ellipsis and shown whole on hover; the left bar and the table's first column are no wider than before.
- The board's answer (`GET /api/board`) gives each project line `folder` and `repo`; sketch:

```python
{"served": "<surface root>",
 "projects": [{"id": "alpha", "folder": "projects/alpha/", "repo": "../../../code/", ...}]}
```

Before (at `f11132b`, from a live board) and after (carried from `f3af2c0`, the repository's own docs pictures, which show a made-up surface path), English, picker closed at 1400 x 860 then 375 x 812, then the open menu at 1400:

| Before | After |
| --- | --- |
| ![before, desktop](./verifier/evidence/before-surface-pc-en-closed.png) | ![after, desktop](https://github.com/gsemet/chantier/blob/main/docs/web-board/home-pc.png) |
| ![before, phone](./verifier/evidence/before-surface-phone-en-closed.png) | ![after, phone](https://github.com/gsemet/chantier/blob/main/docs/web-board/home-phone.png) |
| ![before, menu](./verifier/evidence/before-surface-pc-en-menu.png) | ![after, menu](https://github.com/gsemet/chantier/blob/main/docs/web-board/picker-pc.png) |

## Blast radius

Grade: 1. The change is read-only and confined to the board's page, its payload and the docs; a plain `git revert` restores the previous picker.

## Autonomous decisions

- The docs pictures show a made-up surface path (`/home/demo/planning-surface`): the screenshot script rewrites only the `served` field of the board's answer, so the pictures are identical on every run and reveal nothing of the machine.
- The new styles are in a new stylesheet, `css/paths.css`, because `shell.css` is at the linter's line cap.
- All 18 pictures the screenshot script rewrote are committed, not only the four the picker and home change.

## Known gaps

- In the overview table the first column may not widen, so the folder path is cut early at 1400 px (shown whole on hover).
<details>
<summary>Details</summary>

## Changes

- `board/state.py` (`project_paths`) and `board/routes.py` (`board()`): the two paths per project line, `repo:` read read-only with `read_keyed`.
- `board/web/js/ui/picker.js`, `ui/header.js`, `views/overview.js`: the surface in button, menu and title; the paths in menu, table and cards.
- `board/web/js/i18n/en.js`, `fr.js`: `project.all` and `project.all_sub` removed; `project.folder` and `project.repo` added.
- `board/web/css/paths.css` (new), `css/views/overview.css`, `index.html`.
- `docs/web-board.md`, `docs/demo/README.md`, the pictures in `docs/web-board/`, `scripts/docs_screenshots.py`.
- `tests/test_board.py`: a two-project surface (one project with `repo:`, one without) and an in-project folder.

## Human decisions

- The selector shows the surface (name and path) instead of "All projects", with "Planning surface · N projects" under them on the button itself.
- Each project's line shows two paths, its folder in the surface and its repository as `checkout.yml` names it.

## Impacts

The board's selector, the overview and the docs pictures change on a multi-project surface; nothing else.

## Test plan

- [x] New or changed tests (they fail on the previous code): two tests on `GET /api/board`'s payload.
- [x] Local gates at `51a3c8e`: `just check` pass (367 tests), `just scenario` (Windows, local) pass.
- [x] Evidence: before at `f11132b`, after carried from `f3af2c0`
- [x] Review: carried from `f3af2c0`; the restack move approved at `51a3c8e`
- [x] Verified at `51a3c8e`
- [x] CI green at `51a3c8e`

## Internal references

- CR-305 board-surface-selector; its grill is `ui-feedback-large-screen`'s `02-answers.md` (Q1, Q4, Q5).

</details>
