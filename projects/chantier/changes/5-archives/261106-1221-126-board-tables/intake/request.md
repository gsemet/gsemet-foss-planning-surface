# The board draws its CRs as tables, like the textual status

The user, on the desktop board: "il est assez moche. j'aime bcp le format tableau du status textuel
et les collapsable section." They saw an HTML approximation of the PoC with the batch's real data
and accepted the direction: "Oui, dépose la CR".

Why it looks bad today: every CR id and every fold is a `Button`, and "a desktop draws its native
button either way", even with `plain`. Rows are flex boxes, so nothing lines up in columns. The
desktop surface has no Table or Disclosure element; only `Markdown` draws a table, and it should
draw it as the app draws one in a reply.

The PoC: branch `poc/board-table`, commit 68e58dd, in the worktree
`C:\Users\gaeta\Projets\chantier.worktrees\poc-board-table`. It touches `hooks/register.tsx` and
`hooks/register.test.tsx` only; 19 tests and `plugin validate` pass, `just check` and
`just scenario` were not run. It is based on origin/main at e21df21, and CR-125 changes the command
part of the same file.

What it does:

- CRs in GFM tables through `Markdown`, columns CR | Subject | State | PR | Cost, the same for a
  batch, Landed and Trashed.
- Backlog: one table, Priority | Item | Title | Files, sorted by priority; the nested priority folds
  are gone.
- A batch's sections are folds: Waiting for you (n), Why (n), In progress (n). Why is closed by
  default and holds the long `blocked` texts, kept out of the table.
- The State cell drops a repeated word ("blocked Blocked 2/3") and says a silence only past the
  threshold. The branch leaves the row.
- A CR id is a Markdown link with a `file:` URL, listed in `pressableLinks`; `onLinkPress` opens the
  sheet when the path is inside the checkout. Only the folds stay buttons.
- The CR sheet page does not change.

Not proved, and to prove on the desktop app before this is called done:

- A press on a `file:` link reaches `onLinkPress` with the href as written. The types guarantee
  `PressedLink.href` as written only for https; the mock proves nothing here. If the press does not
  arrive, the surface may open the folder instead, and the CR id needs another way to the sheet.
- Five columns in a narrow pane. The PoC does not adapt to `bodyColumns`.
- The real look: the PoC was seen only as an HTML approximation, never in the pane. The dev-mod copy
  `chantier-board-poc` (command `/chantier-board-poc`) is written in this session's dev-mods folder
  and did not load: the user's Mods question was declined or not answered.
