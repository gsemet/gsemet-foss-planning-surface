## Summary

The board's design rules were written nowhere, so cards, columns and chips drifted from page to page: Triage and Kanban had different columns, cards differed between pages, and a coloured left border bent round each card's rounded corner. This change writes the rules once, in `board/web/DESIGN.md`, and refactors the board so every page lays out shared components built on tokens.

## Deliverables

After this change the board has one column, one card and one chip, the same on every page:

| Piece | Sheet | Builder |
| --- | --- | --- |
| card | `css/components/card.css` | `js/ui/card.js` |
| column | `css/components/column.css` | `js/ui/column.js` |
| chip | `css/components/chip.css` | `js/ui/parts.js` |

- Triage's priority chip is the priority chip of every card (top left), and the Kanban priority filters are the same chips (filled when on, outlined grey when off).
- No element has a coloured accent border on one side; the sidebar and drawer-tree separators stay, and the Batch stack rail is a plain 1 px hairline (**UNVERIFIED:** not seen in a run).
- Every length of `font-size`, `border-radius`, margin, padding and gap in the sheets is a token of `css/tokens.css`; values with no token became named tokens at their current values.
- `DESIGN.md` holds the rules, the token and component tables and the protected features (the Costs receipt and its stamp first).
- A test in `just check` (`tests/test_board_design.py`) refuses a side accent border, a raw value, a component class styled outside its sheet, a card built outside the card builder, and a token table that disagrees with `tokens.css`.

- The documentation's board pictures (`docs/web-board/*.png`) are refreshed with the new look.

Before/after screenshots, from the same demo data (1440x900, phone 375x812). Before at `1690ec4`. The after pairs below are carried from `6f63bab` (Kanban, Costs) and `cd01544` (the other pages): that is the same change before it was rebased onto the PRs page filter. The pages the rebase touched were captured again at `03ee16d` in the section after the pairs.

Triage: the Backlog is one column holding the P1 to P4 lanes, each lane headed by its priority chip; every column has a sub-line.

| Before (`1690ec4`) | After (carried from `cd01544`) |
| --- | --- |
| ![Triage before](https://github.com/user-attachments/assets/d9074d52-8d3b-4e47-b101-fecc7b5b41cb) | ![Triage after](https://github.com/user-attachments/assets/bad6358f-d520-4535-9c19-c9256929988d) |

Kanban: the priority filters are the priority chips (filled when on, outlined grey when off); the cards are the same cards as on Triage, at full height.

| Before (`1690ec4`) | After (carried from `6f63bab`) |
| --- | --- |
| ![Kanban before](https://github.com/user-attachments/assets/a8a3f11b-efb2-4407-ad6e-b192b115e75f) | ![Kanban after](https://github.com/user-attachments/assets/bb86355d-a49e-4d49-bc44-02623d7e4ffc) |

Batch: graph nodes and the PR column's cards now draw the shared card, with no visible change.

| Before (`1690ec4`) | After (carried from `cd01544`) |
| --- | --- |
| ![Batch before](https://github.com/user-attachments/assets/e59b5baf-2b30-4fc0-b903-fe11668ba768) | ![Batch after](https://github.com/user-attachments/assets/7ac1fb30-b9c8-4cf0-985f-5ccfb9c2c91e) |

Costs: the receipt, a protected feature, is unchanged on a closed batch; on a running batch it keeps its "NOT FINISHED" stamp and the "Copy as image" button (after only, carried from `6f63bab`).

| Before (`1690ec4`) | After (carried from `6f63bab`) |
| --- | --- |
| ![Costs before](https://github.com/user-attachments/assets/13b9d74f-2db6-4f12-9aa9-75d5be794a06) | ![Costs after](https://github.com/user-attachments/assets/2d729e6b-df85-4f2c-9550-87bd540b7668) |

![Costs on a running batch, after](https://github.com/user-attachments/assets/add6d8f3-5cb5-4c44-8ed9-19293c411052)

Configuration's Timing tab: the host cards draw the shared card's border, radius and shadow.

| Before (`1690ec4`) | After (carried from `cd01544`) |
| --- | --- |
| ![Configuration timing before](https://github.com/user-attachments/assets/28661071-bd96-40c9-8410-49d4cbc6bbd5) | ![Configuration timing after](https://github.com/user-attachments/assets/b3d1f947-0a24-4a2c-add1-e67c88188692) |

Home, on a computer and on a phone: unchanged in look.

| Before (`1690ec4`) | After (carried from `cd01544`) |
| --- | --- |
| ![Home before](https://github.com/user-attachments/assets/793c356f-22d9-4edf-b6fe-324b52b42b46) | ![Home after](https://github.com/user-attachments/assets/2f682a8a-283c-4d22-9dde-7a6743083626) |
| ![Home on a phone before](https://github.com/user-attachments/assets/4ec3046f-c269-4d76-8ae0-543c85114aae) | ![Home on a phone after](https://github.com/user-attachments/assets/425411f5-4407-490f-94b3-d1e31fb2a831) |

After the rebase onto the PRs page filter (at `03ee16d`, the same demo data): the PRs page's state and sort filters are the shared chips with no stray mark before them; the Batch graph's cards are the shared card and keep the PR tag; the planning surface's Home keeps its forge note and draws each project as the shared card; Kanban cards keep their full height.

| PRs (`03ee16d`) | Batch (`03ee16d`) |
| --- | --- |
| ![PRs page after the rebase](../evidence/after-prs-03ee16d.png) | ![Batch after the rebase](../evidence/after-batch-03ee16d.png) |

| Home of the planning surface (`03ee16d`) | Kanban (`03ee16d`) |
| --- | --- |
| ![Planning surface Home after the rebase](../evidence/after-overview-03ee16d.png) | ![Kanban after the rebase](../evidence/after-kanban-03ee16d.png) |

## Blast radius

The change touches every page's markup and styles but no data, server or record.

Grade: 2

Rolling back is a revert, with the board looking as before.

## Autonomous decisions

- Configuration's host cards now draw the shared card's border, radius and shadow (the specification has the card draw them); a card variant would restore the old look if wanted.
- The Batch PR card's title keeps its two-line clamp through a `card-clamp` variant of the shared card.
- A Kanban column taller than the page now scrolls its body under a fixed head (before, the whole column scrolled).

## Known gaps

- The Costs page's "Copy as image" output was not run; its button shows on a running batch. Running it and comparing the copied image with the receipt would close it.
- The Batch stack rail as a straight hairline is not proved in a run: the demo data shows no stacked PR under a rail. A capture of a batch with a stacked PR would close it.
- The PR tag reading MR on a GitLab forge is not proved on the shared card: the demo data is on GitHub. A capture of the Batch page on a GitLab project would close it.
- The PRs page's rows were not seen after the rebase: the demo's forge cannot be read, so only its filter and sort chips were checked. A capture with a readable forge would close it.

<details>
<summary>Details</summary>

## Changes

- `board/web/DESIGN.md` (new), `tests/test_board_design.py` (new), one line in `AGENTS.md`, `CONTRIBUTING.md` and `docs/web-board.md` updated.
- `css/components/{card,column,chip}.css`, `js/ui/{card,column}.js`; `cards.css` and `tags.css` removed; page sheets keep layout only.
- Triage's Backlog is one column holding the P1 to P4 lanes; two new words (`triage.inbox_sub`, `triage.backlog_sub`) in both languages.

- `docs/web-board/*.png` refreshed with `just docs-screenshots`.

## Human decisions

- `tokens.css` stays the single source of every value; `DESIGN.md` holds the rules, and a test fails when its token table and `tokens.css` disagree. No build step.
- Scope: one card everywhere, no side border on any element, one shared Triage and Kanban column, plus `DESIGN.md`, the shared component sheets and the test; the rest of the UX review stays out.
- The rules are enforced by a blocking test in `just check`.
- A card shows its priority with Triage's priority chip, on every card and every page.
- A coloured accent border on one side of an element is forbidden; a plain straight hairline separating two regions of a page stays allowed.

## Impacts

Cards, columns and chips look the same on Triage and Kanban; the priority shows on its chip only. The screenshots in Deliverables show Triage's single Backlog column, the Kanban filter chips and the unchanged Costs receipt.

## Test plan

- [x] New or changed tests (they fail on the previous code: 4 failed at `1690ec4`): `tests/test_board_design.py`
- [x] Local gates at `03ee16d`: `just check` (549 passed)
- [x] Evidence: before at `1690ec4`; after carried from `6f63bab` (Kanban, Costs) and `cd01544` (the other pages); PRs, Batch, Home of the planning surface and Kanban again at `03ee16d`
- [x] Review: approved at `03ee16d` (the rebase's resolved conflicts)
- [x] Verified at `03ee16d`
- [x] CI green at `03ee16d`: `just check` (ubuntu, macos, windows), `just eval-dry-run`, `just scenario (ubuntu-latest)`

## Internal references

- CR-344 board-design-system

</details>

