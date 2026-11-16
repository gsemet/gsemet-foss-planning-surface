# Change Specification: the board's Refresh button and refresh period

## Goal

The user asked how often the `/chantier-board` pane refreshes and how to force it (2026-11-12).
Today nothing in the pane says the period, the only way to force a check is `/chantier-board`
twice (which drops the page being read), and the header's "read Ns ago" is the age of the last
time the file *changed*, so it shows "read 45s ago" on a quiet batch although a check ran under
15 seconds before.

This CR gives the pane:

1. a **Refresh** button, on every view, that checks at once without hiding the pane and without
   losing the page or the folds, and that visibly does something (the age returns to 0);
2. a **note of the period** in the header, from the same constant as the timer, worded so that it
   does not contradict the age beside it.

No tracker issue: no `issue:` line.

## What changes

### 1. The Refresh button (`hooks/register.tsx`, the `ui.render` handler of the `Pane`)

- One button, label `Refresh`, key `refresh`, a plain `Button` like `< Back`.
- **Where:** at the top right of the pane, on every view, where the mod's layout allows it (the
  user's word: "en haut a droite si possible"). If the mod's `Box` can lay out a row with the
  button pushed to the right (for example a `flexDirection="row"` box whose props align it right),
  the button sits on the pane's first line, at its right. If it cannot, the button is the pane's
  first line, at its top; the PR says which was possible and why.
- **Every view:** the board (one project or a surface's several projects: one button for the
  whole pane, not one per project), a CR's sheet, an inbox or backlog item's file list, a folder,
  a document, a page that can show nothing (`top.note`), and each one-line view: `where.error`
  (e.g. "Cannot look for the main checkout: ..."), "Looking for the chantier files...", a
  `fatal` schema line, "No chantier status here: ... not found.", and "Reading the status...".
  On a page view the button sits on the same top line as `< Back`, `< Back` at the left.
  A one-line view stays one line of text, with the button above it or beside it.

### 2. What a press does

A press runs, at once:

1. **Looks for the planning folders again**, as opening does (`findRoot`, then `findBases`): a
   project added to a surface, or a `.agents/changes/` created after the pane opened, appears; a
   view whose folder is still found keeps its state; a new folder gets a new view; a folder no
   longer found drops its view. A `findRoot` failure is shown as today (`where.error`).
2. **Checks every planning folder and the top page, reading each file again even when its
   modification time did not change** (a forced read; the periodic check keeps its skip). The
   parse failure, wrong schema and missing file cases behave exactly as in the periodic check.
3. Records the time of the check (`checkedAt`), as every check does.

A press does **not**:

- reset or drop the pages (`pages`): the page shown (a CR's sheet, a document, a file list) stays,
  read again; unlike `begin()`, which empties them at opening;
- change the folds (`turned`);
- close, hide or reopen the pane, or start, cancel or restart the timer (exactly one timer while
  the pane is open, as today);
- write any file, call `$CHANTIER`, price the batch, or run any process but the `git rev-parse` of
  `findRoot`: the pane stays read-only. The cost on the board moves when the steering session
  refreshes the status (`status --refresh`), not on a press.

Presses are **unthrottled**: a press while a check runs, or many presses in a row, are harmless
(a check reads a few local files). A failure shows in the board's existing note line
(`feed.note`, or the view's `note`), as for the periodic check; the press adds no new message
kind.

The implementation shape is the Driver's (for example `check($, { force: true })` with
`checkIndex` and `checkPage` taking the flag, and a `refresh($)` that re-finds the bases and
merges the views by `dir` without touching `pages`), within the behaviour above. Navigation
handlers already wrap their work in `guarded()`; the press does the same.

### 3. The periodic check: unchanged

`EVERY_MS = 15000` stays; the timer still calls `check($)`, which still reads a file again only
when its modification time changed. The period is not configurable (no setting in `chantier.yaml`,
no pause of the timer).

### 4. The header: the age of the last check, and the period

The board's header line of each project (`Board`, today
`` `${index.active_crs} live · ${waitingCount} waiting for you · read ${age}s ago` ``) becomes:

```text
5 live · 0 waiting for you · checked 3s ago, every 15 s
```

- `checked Ns ago` is the age of the **last check** (the `checkedAt` atom, set at the end of every
  check, periodic or pressed), no longer the age of the last read (`View.readAt`). It is therefore
  under 15 s on a quiet batch, and 0 right after a press.
- `every 15 s` is written from `EVERY_MS` (`EVERY_MS / 1000`), never a literal `15`, so the note
  and the timer cannot drift.
- While no check has finished yet (`checkedAt` null), the line ends `· every 15 s` with no age.
- One line, one wording, on each project's view of a surface too (they share the one `checkedAt`).

`View.readAt` may stay or go; it is no longer drawn. The `checkedAt` atom keeps its shape
(`number | null`, tag `checked-1`): no atom's shape changes, so no shape tag changes.

### 5. `types/index.d.ts`

No shape change is needed. If the Driver touches it, only the comment of `checkedAt` ("The time
of the last check, drawn as the age of the read") changes, to say it is drawn as the header's
"checked Ns ago". Correcting the file's other drift from the code (`site` without `bases`, `feed`
as `ChantierFeed` rather than `{ views, note }`) is not this CR.

### 6. `docs/boards.md`, section "The CR board (Claude Code)"

Replace the sentence "It refreshes every 15 seconds while open, writes nothing, and runs no
process but `git rev-parse` to find the main checkout from a worktree." with wording that says:

- it checks every 15 seconds while open, and reads a file again only when it changed; the header
  says when it last checked and the period (`checked 3s ago, every 15 s`);
- a **Refresh** button at the top of the pane checks at once: it reads the files again, even
  unchanged ones, and looks for the planning folders again (a project added to a surface, a
  `.agents/changes/` created after opening), keeping the page shown and the folds;
- it does not refresh the batch's cost or record: that moves when the steering session refreshes
  the status;
- it writes nothing and runs no process but `git rev-parse` (kept as today).

Only this sentence's place changes; `boot-mode-by-surface` also edits `docs/boards.md` (the
README and the board's documentation page with screenshots). No `depends.json`: whichever merges
second rebases. Screenshots taken before this CR lack the button; retaking them is not this CR.

### 7. Tests (`hooks/register.test.tsx`)

New tests, in the file's style (`mock.clock`, `world`, `skill`, `board`, `words`, `ui.press`):

- **The note and the age:** with an unchanged index, after `clock.advance(45000)`, the header
  contains `every 15 s` and `checked 0s ago` (not an age of 45 s); it no longer contains
  `read ` ... `s ago`.
- **A press re-reads an unchanged file:** the read count of `INDEX` grows by one on
  `ui.press({ key: 'refresh' })` with the file unchanged, and the header shows `checked 0s ago`.
- **A press keeps the page and the folds:** open a CR's sheet (as the existing navigation test
  does), press `refresh`: the sheet is still shown and its `STATUS.json` was read again; back on
  the board, a fold turned before the press is still turned.
- **A press finds a planning folder created after opening:** with no index the pane says "No
  chantier status here: ..."; put the index (and, for a surface, a new `projects/<name>/changes/`)
  then press `refresh`: the board shows without waiting for the timer.
- **The button is on every view:** the board, a sheet, a document and the one-line "No chantier
  status here" view each hold a `Button` with key `refresh`.
- **No second timer:** after several presses, `clock.advance(15000)` runs one periodic check (the
  `stat` count of `INDEX` grows by one), and closing the pane still stops it (the existing "a
  closed pane runs no timer" test passes unchanged).

Existing tests that compare the whole text must be updated for the button's label, notably
"without an index the pane says so in one line" (its `toBe` on `words(ui)`, which includes
button labels): the line itself stays one line.

## Out of scope

- Pricing or refreshing the batch's record, calling `$CHANTIER`, any write by the pane.
- A configurable period, a pause of the timer, any `chantier.yaml` setting; any change to the
  periodic check's period or skip.
- The remote board (`chantier board`, the web page reloading every 30 seconds): no button, no
  note.
- The README and the board's documentation page with screenshots (`boot-mode-by-surface`).
- The CLI, the cards, the agents and the scenario: untouched.

## Evidence

- `just mod` (it runs `claude plugin validate .` then `claude plugin test .`, which runs
  `hooks/register.test.tsx`), run by the agent itself at the pushed head, passing with the new
  tests; an agent that cannot run it stops and says so, with no workaround (`AGENTS.md`).
- `just check`, passing.
- `just scenario`: not needed (no change to the CLI, the cards or the scenario).
- In the PR: one line saying whether the button sits at the top right or at the top, and why.
