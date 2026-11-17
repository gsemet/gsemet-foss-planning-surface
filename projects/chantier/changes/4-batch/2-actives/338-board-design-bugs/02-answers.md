# Answers

The request: `intake/request.md`, with the user's screenshots `intake/detail-drawer.png` and
`intake/kanban-priorities.png`. The QA report: `../board-design-realign/intake/ux-qa.md` (P0 and the
"CR drawer" and "Kanban" findings), with its screenshots.

- design-Q1 (split, the user, 2026-11-17, recorded in `board-design-realign/02-answers.md`): two
  CRs. The quick fixes go first, in this CR: the drawer's file list (the `.nm` class collision
  with the card band rule, the `.ind` collision with Triage's pill), the Kanban priority chips
  (the browser's button border, the meaningless grey square), the front matter rendered as a
  paragraph in `panel/markdown.js`, and the "---" titles from `status/views.py` `_title()`.
  `board-design-realign` then does the full realignment.
- The user put this CR in the running batch (batch-24), 2026-11-17.

## Settled by the Chief of Staff

- bugs-S1 (the title rule, 2026-11-17): a CR's title comes from the document's first heading,
  after any front matter. A front matter is a block at the very start of the file (an optional
  BOM, CRLF or LF) opened by a `---` line and closed by the next `---` line: the regex of
  `board/backlog.py` (`FRONTMATTER`). The first heading is the first line, after it, that starts
  with one to six `#` and a space; the title is its text without the `#`s. A file with no heading
  gives its first non-blank line after the front matter, as a heading-less file does today. A
  file that holds nothing after its front matter gives no title, and the next file, then the
  folder's name, is used, as today. The same rule serves the board and the record: `_title`
  (`status/views.py`) and `prepared_cr` (`lifecycle/stages.py`, the title `open` and `add` record).
- bugs-S2 (titles already recorded, 2026-11-17): the record is not rewritten. A recorded title
  that is a front matter's opening fence (`---` after trimming) is shown as the title bugs-S1 reads
  from the CR's folder, wherever a recorded title is served: the CR and batch views and the
  `STATUS.json` files, the archived CRs' list, the board's CR rows, and the closed batch's record
  written at `close`. So batch-24's entries read right on the board without a record edit, and its
  close record holds real titles.
- bugs-S3 (the drawer's file list, 2026-11-17): only the tree's own classes are renamed: the
  name's `<span class="nm">` becomes `fname`, the nested file's button class `ind` becomes
  `nested`, and `panel.css` follows. The card band rule keeps its `.nm` alias for the Batch cards
  that use it; scoping or removing it is `board-design-realign`'s.
- bugs-S4 (the filter chips, 2026-11-17): the reset goes on the toggle class `.lbtn` (no border,
  the page's font), so the label filter, which uses the same button, loses its outset border too.
  A priority toggle draws no colour square; a label toggle keeps its label's square. The on and off
  looks stay as they are; the one filter-chip style is `board-design-realign`'s.
- bugs-S5 (front matter in the drawer, 2026-11-17): a front matter (bugs-S1's definition) is drawn
  above the document as a muted key/value list: one row per `key: value` line, the key and the
  value as text, in the small size and the muted inks, no box, no fill, no chip, a gap before the
  document. A line that is not `key: value` (an indented continuation, a `- item`) joins the
  previous value. An opening `---` with no closing `---` is no front matter: the file renders as
  today. Every value is escaped as the rest of the document is. The editor ("Modifier") still shows
  and saves the whole file, front matter included. The `type:` chip and the `description:` lead
  paragraph of the report's target are `board-design-realign`'s.
- bugs-S6 (the pane, 2026-11-17): the fix changes the titles that the CR board pane draws from
  `STATUS.json`, so the AGENTS.md rule on the pane applies: the PR carries one screenshot of the
  pane from a real Claude Code session running the PR's head, captioned with the head's SHA, and
  until it is there, Known gaps names it.
- bugs-S7 (evidence, 2026-11-17): before and after screenshots, on the same data, of the drawer
  (a file with a front matter open, its file list in view), of the Kanban's priority chips, and of
  a page that showed "---" titles (Batch, on batch-24); they go in the PR's Deliverables, before and
  after side by side, with made-up or planning-folder paths only.

- Settled by the Chief of Staff (spec critic's note): `lifecycle/backlog.py:39` builds a filed request's slug from the first non-blank line, the same "---" bug; the Driver fixes it with the same shared title helper, or names it in Known gaps if it does not fit.
