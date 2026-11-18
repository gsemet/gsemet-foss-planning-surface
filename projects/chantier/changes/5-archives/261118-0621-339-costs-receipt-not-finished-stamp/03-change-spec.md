# Change Specification: the Costs receipt of a batch that is not closed carries a red "NOT FINISHED" stamp

## Goal

On the web board's Costs page, the receipt of a running batch looks today like the receipt of a
closed one: only a small teal pill says "running". The user wants it plain at a glance, "like a red
stamp on the receipt": a red stamp, set at an angle on the ticket, reading "NOT FINISHED" in
English and "PAS FINI" in French, on the receipt of every batch that is not closed. The stamp is
part of the ticket, so the receipt's "Copy as image" carries it too. A closed batch's receipt is
unchanged.

## Decisions carried from `02-answers.md`

- stamp-Q1: a red stamp, at an angle, on the receipt of a batch that is not closed; translated
  ("PAS FINI" in French, "NOT FINISHED" in English); on the page and on the receipt's copied image.
- stamp-S1 (settled by the Chief of Staff): the stamp shows exactly when the shown batch's state is
  not `closed` (running, paused, closing or any other value): `r.stateName !== 'closed'` on the
  receipt object. A closed record, the default one or one chosen in CR-327's navigator, never
  carries it.
- stamp-S2 (settled by the Chief of Staff): the words are the user's own, "NOT FINISHED" and "PAS
  FINI", nothing else.
- The user put this CR in batch-24 (2026-11-17).

## What changes

All paths are under `skills/chantier/scripts/cli/src/chantier/board/web/`. No Python, no server,
no record and no card changes.

### 1. The words (`js/i18n/en-costs.js`, `js/i18n/fr-costs.js`)

One new key in each, beside the `costs.receipt_state_*` keys:

- `en-costs.js`: `'costs.receipt_stamp': 'NOT FINISHED'`
- `fr-costs.js`: `'costs.receipt_stamp': 'PAS FINI'`

The text is written in capitals in the dictionary (not by `text-transform`), so the copy, a screen
reader and the image all read the same words.

### 2. The ticket (`js/views/costs-receipt.js`)

- A small function, `stamp(r)`, returns `''` when `r.stateName === 'closed'`, else one element with
  the stamp's text, `t('costs.receipt_stamp')`, as real text (not CSS `content`, which neither the
  dictionaries nor the image clone would carry reliably), e.g.
  `<div class="stamp">${t('costs.receipt_stamp')}</div>`.
- `receipt(r)` puts it inside the `<section class="ticket">`, so the image clone carries the
  element (`boxed` in `costs-image.js` removes only `.r-act` and `button`; the stamp must be
  neither, and must not sit inside `.r-act`).
- The stamp is not interactive and takes no click; it stays readable text for a screen reader (no
  `aria-hidden`).
- `model/receipt.js` does not change: `stateName` is already `rec.state` for the live batch and
  `'closed'` for a record (`headOf`).

### 3. The look: a new sheet, `css/views/costs-stamp.css`

`css/views/costs-receipt.css` is at 299 lines and `tests/test_code_targets.py` caps a sheet at
`MAX_STYLE_LINES = 300`, so the stamp's rules go in a new sheet of their own,
`css/views/costs-stamp.css` (a one-line header comment, then `.ticket .stamp`, and its phone-width
rule). `costs-receipt.css` does not change.

- `index.html`: one `<link rel="stylesheet" href="css/views/costs-stamp.css" />`, right after the
  `costs-receipt.css` link.
- `js/views/costs-image.js`: `'css/views/costs-stamp.css'` added to `SHEETS`, after
  `'css/views/costs-receipt.css'`, so the copied image draws the stamp with its styles. Nothing else
  in that file changes.
- A rubber-stamp look: red text in capitals, bold, letter-spaced, a red border (a double or thick
  border, rounded corners), a transparent background so the ticket shows through, rotated by a
  small angle (around -10 to -15 degrees), slightly translucent ink, so it reads as a stamp laid on
  the paper.
- Tokens only, no raw values, so `board-design-realign`'s token test (it lands after this CR and
  will check this sheet) passes on it:
  - colour: an existing token of `css/tokens.css`, `--bad-ink` (or `--red`); no new colour;
  - font size: a type token (`--text-badge` 11, `--text-small` 12, `--text` 14, `--title` 24, or a
    16 px type token if `tokens.css` has one by then) or the ticket's own tokens;
  - radius: `--radius-s` (it exists today, 6 px);
  - padding, offsets and any gap: `--space-*`.
  The rotation angle and the ink's opacity have no token in `tokens.css`: declare each once as a
  custom property of `.ticket .stamp` at the top of the rule (e.g. `--stamp-tilt: -12deg`), and use
  it through `var()`. No change to `tokens.css`.
- Placed with `position: absolute` inside the ticket (the ticket is `position: sticky` on the page
  and `position: relative` in the image, both of which anchor it), with `pointer-events: none`,
  above the ticket's content (`z-index` as needed).
- Where: on the ticket, rotated, entirely inside the ticket's box, in its upper half, so it is seen
  at once without scrolling, and it does not hide the batch id, the pill or the Total's figure. The
  image is cut to the ticket's measured box plus a 24 px margin (`ticketPng` in `costs-image.js`):
  a stamp overflowing the ticket would be clipped in the image, so it must stay inside, rotation
  included.
- A `@media (max-width: 760px)` rule in the same sheet: the stamp stays inside the narrower ticket
  and keeps the batch id and the Total readable (a smaller type token there if needed).

### 4. The docs (`docs/web-board.md`)

In the "Costs" section, the paragraph on the ticket (the one that begins "A closed batch's ticket
is the `cost_receipt` its record kept at close"): one sentence that a batch that is not closed
(running, paused) carries a red "NOT FINISHED" stamp on its ticket, and on its copied image, so it
is not taken for a final receipt. `docs/web-board/costs-pc.png` and `costs-phone.png` show the
demo's `mobile-app` project, whose batches are closed: they do not change, and `just
docs-screenshots` is not owed.

## Out of scope

- No change to the pill (`.pill`, `costs.receipt_state_*`), the dates line ("→ now"), the receipt's
  figures or `model/receipt.js`; in `costs-image.js`, only the one `SHEETS` entry.
- No stamp anywhere else: not in the Costs side column (`views/costs.js`), the Batch, Board or PRs
  pages, the CR board pane, `status`, the `cost` command or `batch-NN.md`.
- No new colour token, no change to `tokens.css`, `costs.css`, `costs-receipt.css` or
  `components.css`.
- No new test file, no JavaScript test runner.

## Shared files in batch-24

Two other CRs of batch-24 touch the same page: `board-cost-by-model` (a new card on the Costs page,
in `views/costs.js`, `model/receipt.js`, `en-costs.js`, `fr-costs.js`, `costs.css`,
`docs/web-board.md`) and `board-design-realign` (the board's design and its CSS, with a token test
over the sheets; it lands after this CR). They are not a dependency (no `depends.json` for a shared
file): this CR adds one key per dictionary, one small function and one line in `receipt(r)`, one
link in `index.html`, one `SHEETS` entry and a new sheet, so a rebase over either is a small, local
merge.

- `board-design-realign`, rebasing after this CR, finds `costs-stamp.css` under its token test: the
  sheet uses tokens only (section 3), and if that CR renames a token, it renames it here too. The
  stamp's sheet stays its own file, linked in `index.html` and listed in `SHEETS`.
- `docs/web-board.md`: whichever of this CR and `board-cost-by-model` rebases second keeps both
  CRs' sentences in the "Costs" section.

## Evidence

- `just check` (ruff, mypy, `uv lock --check`, Biome on `board/web`, `just test`, including
  `test_code_targets.py`'s sheet length cap), green on Linux, macOS and Windows (CI); the Driver
  runs it in the worktree at the rebased head before the first push. Biome must pass on both changed
  JS files and the new CSS file.
- `just eval-dry-run` in the worktree before the first push: the change is under the CLI's `src/`
  (`skills/chantier/scripts/cli/src/`).
- `just scenario (ubuntu-latest)` green at the PR's head: AGENTS.md's long gate for a change to the
  CLI. Locally (`chantier gate`, Windows) when this CR's PR is the top of batch-24's stack, as
  AGENTS.md asks.
- `just mod` is not owed (no change to `hooks/` or `types/`), nor the CR board pane's screenshot
  (the pane, `hooks/register.tsx`, and `STATUS.json` do not change).
- By hand, on the board served on the demo (`chantier board` on a copy of `docs/demo`, or the board
  `just docs-screenshots` serves), in English and in French, at a desktop width and at a phone width
  (under 760 px). Three screenshots go in the PR's Deliverables, each captioned with the head's SHA
  (seven characters):
  1. The receipt of a batch that is not closed, carrying the red stamp: the demo's `shop-api`
     project (its `4-batch/batch.json` runs a batch), Costs page.
  2. The receipt of a closed batch, with no stamp: the demo's `mobile-app` project, Costs page (its
     latest closed record), and one older record reached with the navigator's `‹`.
  3. The copied image of the receipt in screenshot 1: "Copy as image" on the board at a 127.0.0.1
     address, then the PNG pasted (in an image viewer or a document): the stamp is in it, red, at
     its angle, whole, not clipped (this proves the `SHEETS` entry).
  Also checked by hand, not owed as screenshots: the French page reads "PAS FINI"; a paused batch
  carries the stamp too; at the phone width the stamp stays inside the ticket and the batch id and
  the Total stay readable.
- Until the three screenshots are in the PR's Deliverables, its Known gaps names them ("no
  screenshot of the stamped receipt, the closed receipt or the copied image").

## Open questions

None.
