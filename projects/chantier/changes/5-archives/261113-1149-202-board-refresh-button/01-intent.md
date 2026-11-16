# Board mod: a Refresh button and the refresh period

## The request

The user asked how often the `/chantier-board` pane refreshes and how to force it, then asked for
(2026-11-12): a **Refresh button** in the pane, and a **note** saying how often it refreshes
("refreshed every ..."), as a CR of its own, apart from `boot-mode-by-surface`.

## The problem

- The pane checks its files every 15 seconds (`EVERY_MS`, `hooks/register.tsx`) and nothing in
  the pane says so: the period is written only in `docs/boards.md`.
- The only way to force a check is `/chantier-board` twice (hide, then show), which also drops the
  page the user was reading (a CR's sheet, a document) since opening resets the pages.
- The header's "read Ns ago" is the age of the last *read*, and the file is read again only when
  its modification time changed. So on a quiet batch it shows "read 45s ago" (the
  `board-mod-batch-done.png` screenshot of `boot-mode-by-surface`) although a check ran less than
  15 seconds before. A note "refreshed every 15 s" beside "read 45s ago" would look like a
  contradiction, and a Refresh press on an unchanged file would change nothing on screen.

## Where it shows

- `hooks/register.tsx`: `check()` (the indexes, then the top page), `checkIndex()` (skips an
  unchanged file), the timer in `begin()`, the header line of `Board` ("N live · N waiting for
  you · read Ns ago"), the page views with their "< Back" button, the single-line views (missing
  or wrong-schema `STATUS.json`).
- `hooks/register.test.tsx`: the pane's tests, run by `just mod`.
- `types/index.d.ts`: the mod's contract, if the state it keeps changes shape.
- `docs/boards.md`: "It refreshes every 15 seconds while open".

## What would fix it

- A **Refresh** button in the pane that runs a check at once, keeps the pane open, and keeps the
  page and the folds as they are.
- A press shows that it did something: the age in the header returns to 0.
- A **note** that states the period, from the same constant as the timer, worded so that it does
  not contradict the age beside it.
- `docs/boards.md` says the button exists and what it does not do.

## Out of scope

- Pricing or refreshing the batch's record: the button reads files again and nothing more. The
  cost on the board moves when the steering session refreshes the status (`status --refresh`);
  the pane writes nothing and runs no process but `git rev-parse`, and that stays.
- A configurable period, a pause of the timer, a setting in `chantier.yaml`.
- The remote board (`chantier board`, the web page that reloads every 30 seconds): a browser has
  its own reload.
- The README and the board's documentation page with screenshots: `boot-mode-by-surface`.

## Gates

A change under `hooks/` (and `types/` if the state changes): `just mod` before the PR, run by the
agent itself, which stops and says so if it cannot (`AGENTS.md`); `just check` as always. No
change to the CLI, the cards or the scenario: `just scenario` does not apply.
