# The board and the CR sheet draw tables under folds

## Problem

The desktop board is ugly. Every CR id and every fold is a `Button`, and a desktop draws its native
button even with `plain`; rows are flex boxes, so nothing lines up. The desktop surface has no Table
element: only `Markdown` draws a table, as the app draws one in a reply. The user likes that table
and the folds.

## Change

Start from the PoC: branch `poc/board-table`, commit 68e58dd, which holds the board's part of
`hooks/register.tsx` and `hooks/register.test.tsx`. Bring it onto the batch's base.

The board, as in the PoC:

- CRs in Markdown tables, columns CR | Subject | State | PR | Cost, the same for a batch, Landed and
  Trashed. Always five columns, at any pane width.
- Backlog: one table, Priority | Item | Title | Files, sorted by priority. The nested priority folds
  go.
- A batch's sections are folds: `Waiting for you (n)` and `In progress (n)` open, `Why (n)` closed.
  `Why` holds the long `blocked` texts as a list, out of the table, and is drawn only when a
  waiting CR has one.
- The State cell drops a repeated word ("blocked Blocked 2/3" reads "blocked 2/3") and says a silence
  only past `SILENT_MINUTES`. The branch leaves the row.
- A CR id is a Markdown link to a `file:` URL, listed in `pressableLinks`; `onLinkPress` opens the
  sheet when the path is inside the checkout, and nothing otherwise. A PR link stays an https link
  left to the surface. Only the folds and the way back stay buttons.

The pages above the board, new here:

- The CR sheet keeps its title, state and cost, `Now`, `Next` and `Blocked` lines, and a PR link.
- Its steps become a table, Step | Done | Verdict, instead of the one-line chain; a step's note stays
  out, as today.
- Its documents become a table, Document | Kind, whose names are `file:` links opening the document
  in the pane, like a CR id. A document outside the checkout is plain text in its cell.
- A folder's or an item's list of files is a table of the same kind, with one column, File.
- The document page does not change.

A cell escapes `\` and `|` and folds its whitespace, so a title never breaks a table.

`hooks/register.test.tsx` follows: it presses links through `ui.press({ key, link })`, and proves that
a link out of the checkout opens nothing, on the board and on the sheet.

## Out of scope

Columns that adapt to `bodyColumns`, unless the user's trial shows five unreadable. The Remote Control
view. `STATUS.json` and `status.py`: the fields stay. The command part of `register.tsx`, which CR-125
changes.

## Done when

- The board and the pages draw as above, and the tests pass.
- `just check` and `just scenario` pass.
- Proved by the user on the PC with the PoC: a press on a CR's `file:` link opens its sheet in the
  pane. Left to the user on the delivered head: a document link on the sheet opens the document, and
  five columns read well in the pane.
