# Triage: fold each priority row, explain the writes-since-rescan count

On the web board's Triage page, each of the four priority rows of the Backlog column (P1 to P4)
can be folded with a click on its head, and the "N writes since your last 'rescan'" button's
panel says in plain words what the count is, why the Chief of Staff may not know of those writes,
and what to tell it. Both board languages. Web client only.

## Goal, in the user's terms

The user (2026-11-15, `intake/request.md`, translated): "Add a collapse for each priority (P1, P2,
P3, P4) that hides all the items of that priority" and "'5 writes since your last rescan': explain
what it is and why the user must ask something of the Chief of Staff (say what to ask, in the
board itself)". Both board languages (English, French). On the UI night (2026-11-21) the user
asks for a working UI; the grill was answered by a Fable advisor in the user's place.

## Decisions carried (02-answers.md)

| Answer | Decision | Where |
| --- | --- | --- |
| Scope notes (2026-11-16, 2026-11-17), Q1 | Two points only: the fold per priority row and the count's explanation. The cards' width and grid (ui-feedback-large-screen) and the sticky header's border and shadow (board-visual-refresh) are done on `main` and not reopened. | Out of scope |
| UI night, act | The board edits no batch and messages no agent (AGENTS.md stands). | 2, Out of scope |
| Q2 | Only the rows P1 to P4 of Triage's Backlog column fold, each on its own. Not the Inbox, not `3-ready`, not CR-427's halves, not Kanban, not Home. | 1 |
| Q3 | A folded row keeps its head (priority chip, count, grill-state counts, a chevron saying open or closed); its post-its, groups and empty-row text are hidden. | 1 |
| Q4 | A click on the row's head folds or unfolds it; the chevron is a real button (keyboard, `aria-expanded`, a label in both languages). No "fold all" or "open all". | 1 |
| Q5 | All rows open by default. The choice is kept on the device (the browser's storage, as CR-434 keeps the Batch tab), one choice per row, the same for every project, across reloads. Nothing on the server or in the planning folder. | 1 |
| Q6 | A folded head is a drop target: a post-it or a group dropped on it goes to that priority; the row stays folded and its count changes. The selection bar's "→ P<n>" works the same. | 1 |
| Q7 | Selected post-its of a row being folded leave the selection. | 1 |
| Q8 | The label filter and the counts are unchanged: a folded row's counts are those of the open row under the same filter. An empty row folds like any other; no row folds or opens by itself. | 1 |
| Q9 | The explanation is the journal panel's first lines, above the list (today's bottom note is replaced), and the button's one-sentence tooltip. The button keeps its place, count and two tones. No new page, dialog or Help link. | 2 |
| Q10 | The explanation says, in order: what (the board's changes since the user last pressed the panel's button, each already saved, nothing lost or pending); why (the board never messages the Chief of Staff; a session whose watcher runs learns of them by itself, one without a watcher or that planned before them does not); what to do (type "rescan" in the Chief of Staff's chat, it reads the backlog again and says what moved; then press the button to count from zero). | 2 |
| Q11 | The count, the list, the "I said 'rescan' to the CoS" button, the post-its' "modified" mark and Home's "Written by the board" tile behave as today; only words change. The board does not show whether a watcher runs. | 2 |
| Q12 | English and French for every new or changed text, the same keys in both; French says "tu". | 1, 2 |
| Q13 | Nothing outside the web client: no server, protocol, CLI, card or AGENTS.md change. DESIGN.md read first and kept true; Triage's screenshots retaken; the pane screenshot rule does not apply. | 3, Evidence |
| Q14 | Same fold and text at phone widths; the head is large enough to tap. | 1 |
| Q15 | No behaviour overlap with batch-30; shared files with CR-427, no `depends.json`; written on the lanes as CR-427 leaves them, the stack's order settles the rebase. | Overlaps |
| Q16 | Risks: the head's counts and the open default answer a forgotten folded row; an unknown or broken stored value reads as "open". | 1 |

## What changes

All paths below are under `skills/chantier/scripts/cli/src/chantier/clients/web/`. Read
`DESIGN.md` there first and keep it true (AGENTS.md).

### 1. Fold a priority row

**The stored choice: a new module `js/triage/fold.js`** (small, under the 300-line limit of
`tests/test_code_targets.py`).

- The kept value is the store preference `triageFolded` (`localStorage` key
  `chantier.triageFolded`), read with `pref('triageFolded')` and written with
  `setPref('triageFolded', ...)` from `js/core/store.js`. The store's helpers stay the only writers
  of `localStorage`. The key has no project in it: one choice per row, the same for every project
  (Q5).
- Its value is the folded rows, comma-separated, in `LANES` order (`P2,P4`). An empty string means
  none folded.
- Reading (`readFolded(text)`, pure): split on commas, keep only the names in `LANES`
  (`js/model/triage.js`), drop duplicates. A missing key, an unknown name or any other broken value
  gives no folded row for that part: what cannot be read reads as "open" (Q16).
- In the store, `js/core/store.js` gains the field `triageFolded: null` ("Triage: the rows P1..P4
  folded, read from the device's preference on first use"). `foldedOf(state)` in `fold.js` returns
  `state.triageFolded ?? readFolded(pref('triageFolded'))`. The first render then already shows
  the kept choice (no flash of open rows).
- `toggleFold(row)`:
  - computes the new list;
  - writes it with `setPref`;
  - on a fold, removes from `state.selection` the slugs of every item of that row, whatever the
    label filter (`itemsIn(backlog, row)`) (Q7);
  - makes one `update({ triageFolded, selection })`.
- `bindFold(root)`: one delegated `click` on `[data-fold]` (the lane's head) that calls
  `toggleFold(el.dataset.fold)`. The chevron button sits inside the head and has no handler of its
  own. Enter or Space on the focused button fires its `click`, which reaches the head's delegate
  once. `js/views/triage.js` adds `bindFold(root)` to `mount`'s list.

**The lane: `js/ui/column.js`.**

- `lane(parts)` gains two optional parts:
  - `fold`: the row's name, for a foldable lane;
  - `folded`: a boolean.
- With no `fold` (CR-427's named halves, any other lane), the markup is today's.
- With `fold`, the head `div.column-head` gets `data-fold="<row>"`. The head starts with a
  `<button type="button" class="column-fold" data-key="fold-<row>" aria-expanded="<true|false>"
  aria-label="<label>">`. The button holds `icon('chev')` (`js/ui/icons.js`, the chevron the picker
  and the writer pill already draw). After the button come the chip, the count and the states, as
  today.
- The label is `t('triage.fold', { row })` when open and `t('triage.unfold', { row })` when folded.
  `column.js` receives it as a part (`foldLabel`), so the module stays free of words, as today.
- A folded lane adds the class `column-folded` to `column-lane`. The section keeps its
  `data-col="<row>"` and `aria-label`, so it stays a drop target (Q6).
- `data-key="fold-<row>"` lets `js/core/paint.js` give the focus back to the same button after the
  redraw.
- The comment at the top of `column.js` names the two new parts.

**The row: `js/triage/columns.js`.** `laneOf` passes `fold: key`, `folded` (from
`foldedOf(state)`, carried into the context by `contextOf` in `js/views/triage.js` as
`ctx.folded`, a list), and `foldLabel`. Counts, grill-state counts and `empty` are computed exactly
as today, from `shownIn(backlog, key, ctx.filter)`, folded or not (Q8). Nothing folds or opens a
row except the user's click: no rule ties `folded` to `empty` or to a write.

**The sheet: `css/components/column.css`** (the component's own sheet; DESIGN.md "Components").

- `.column-folded`: the same thin strip as `.column-empty` (its padding), and
  `.column-folded .column-body { display: none; }`. This hides the post-its, the groups' frames and
  the drop zone's text (Q3).
- `.column-head[data-fold]` gets `cursor: pointer`. The whole head toggles (Q4).
- `.column-fold`:
  - a plain button: no border, transparent background, `--ink3` colour, padding
    `var(--space-1)`, radius `var(--radius-s)`, `--hover` fill on hover;
  - a visible focus ring as the board's buttons have;
  - its `svg` rotated `-90deg` when `aria-expanded="false"`, so the chevron points right when
    folded and down when open.
- `.column-lane.over` already lights a folded lane during a drag: no change.
- At phone widths (`@media (max-width: 760px)`, the board's breakpoint), `.column-head[data-fold]`
  gets `min-height: var(--nav-height)`, so the head is tap-sized (Q14). Same fold, same behaviour.
- Tokens only, no new token. DESIGN.md's token table does not change.

**Drops and the selection bar.** No change to `js/triage/drag.js` or `js/triage/move.js`.
`targetOf` finds the folded lane by `closest('[data-col]')` from its head. The drop calls
`moveTo([slug], 'P<n>')` or `moveWhole(group, 'P<n>')` as on an open row. The row stays folded,
since only `toggleFold` changes `triageFolded`. The selection bar's "→ P<n>" is unchanged (Q6).

**The selection never acts on hidden post-its** (Q7). `selectedNow(state)` in
`js/triage/selection.js` also drops the slugs whose column (`columnOf`) is a folded row. This
covers a selected post-it that another write moves into a folded row. Open question 4 names this
choice.

**Words** (`js/i18n/en-write.js`, `js/i18n/fr-write.js`, beside the other `triage.*` keys):

| Key | English | French |
| --- | --- | --- |
| `triage.fold` | `Hide the {row} post-its` | `Masquer les post-its de {row}` |
| `triage.unfold` | `Show the {row} post-its` | `Afficher les post-its de {row}` |

### 2. Explain the writes count

**The panel: `js/journal/journal.js`, `journalPanel`.**

- New order: the heading `<b>` (`journal.heading`, unchanged), then three paragraphs
  `<p class="note">`: `journal.what`, `journal.why`, `journal.todo`. Then the list (`ul`), then the
  row of buttons.
- The bottom `<p class="note">${t('journal.note')}</p>` is removed, and so is the key
  `journal.note` from both word files (Q9).
- The list, its entries, the "nothing" line, the "I said 'rescan' to the CoS" button (still
  disabled with no entry), "Close", `said()` and the toast stay as they are (Q11).

**The button: `journalButton`.** It gains `title="${t('journal.tip')}"`. The label
(`journal.button`, `journal.button.one`), the count, the classes `drafts` and `drafts.has` (the
two tones), `data-key` and `aria-expanded` stay. The label keeps its words (open question 2).

**The sheet: `css/journal.css`.** `.dlist .note` gets `margin: 0 0 var(--space-2)`, so the three
paragraphs read as separate lines above the list. Tokens only.

**Words** (`js/i18n/en-write.js`, `js/i18n/fr-write.js`; French says "tu"; quotes as the files
already write them):

| Key | English | French |
| --- | --- | --- |
| `journal.what` | `What it counts: the changes made from this board (for example moves, new ideas, labels, groups) since you last pressed the button below. Each one is already saved in the planning folder: nothing is lost or waiting.` | `Ce que ça compte : les changements faits depuis ce board (par exemple déplacements, nouvelles idées, labels, groupes) depuis la dernière fois que tu as appuyé sur le bouton ci-dessous. Chacun est déjà enregistré dans le dossier de planification : rien n’est perdu ni en attente.` |
| `journal.why` | `Why tell the Chief of Staff: the board never sends it a message. A Chief of Staff session whose watcher runs learns of these changes by itself; one without a watcher, or one that planned before them, does not.` | `Pourquoi le dire au Chief of Staff : le board ne lui envoie jamais de message. Une session Chief of Staff dont le watcher tourne apprend ces changements toute seule ; une session sans watcher, ou qui a planifié avant eux, ne les connaît pas.` |
| `journal.todo` | `What to do: type ‘rescan’ in the Chief of Staff’s chat; it reads the backlog again and says what moved. Then press the button below to count again from zero.` | `Quoi faire : tape « rescan » dans le chat du Chief of Staff ; il relit le backlog et dit ce qui a bougé. Puis appuie sur le bouton ci-dessous pour recompter à partir de zéro.` |
| `journal.tip` | `Changes saved by this board since your last ‘rescan’: open to see them and what to tell the Chief of Staff.` | `Changements enregistrés par ce board depuis ton dernier « rescan » : ouvre pour les voir et savoir quoi dire au Chief of Staff.` |

"For example" keeps `journal.what` true. The board's journal (`board/journal.py`, `record`) also
counts Markdown edits, the "next batch is ready" declaration and configuration saves, so the four
kinds are examples, not the whole list (open question 3).

These words match the Chief of Staff card's "rescan" line: it reads the backlog again and says
what moved, and with a watcher the writes already came. They also match `docs/web-board.md`'s
Triage bullet. The board shows nothing about whether a watcher runs (Q11).

### 3. DESIGN.md and the docs

- **`DESIGN.md`**: add a section after "Waits on a card", **"Triage: folded rows and the writes
  count"**, saying:
  - each Backlog row P1 to P4 folds on a click on its head (`lane(parts)`'s `fold`, the
    `column-folded` variant, the `column-fold` chevron button with `aria-expanded`);
  - a folded row keeps its chip, count and grill-state counts, stays a drop target, and is open by
    default;
  - the choice is the device's preference `triageFolded`, the same for every project, and a value
    that cannot be read reads as open;
  - no other column or lane folds, and nothing folds by itself;
  - the journal panel opens on three lines (what the count is, why the Chief of Staff may not
    know, what to type), and the button carries a one-sentence tooltip;
  - no new colour, size or token.

  The Components table is unchanged (still `column`, `column-*`, `js/ui/column.js`). This is a
  section of its own, apart from the "One card, one column, one chip" rule that CR-427 edits, so
  the two CRs touch different lines.
- **`docs/web-board.md`**, Triage section (open question 1):
  - add one bullet: "Click a priority's head (or its chevron) to fold it: its post-its hide, its
    counts stay, and it still takes drops; the board remembers it on this device.";
  - in the button's bullet, add that its panel says what the count is and what to tell the Chief
    of Staff.
- **Screenshots**: `just docs-screenshots` retakes `docs/web-board/triage-pc.png`,
  `triage-phone.png` and `triage-selection-phone.png`, which now show the chevrons (all rows open,
  the default). The script `scripts/docs_screenshots.py` is not changed.

## Out of scope

- The Triage cards' width and grid (ui-feedback-large-screen) and the sticky header's border and
  shadow (board-visual-refresh): done on `main`.
- Folding the Inbox, `3-ready`, CR-427's "running batch" and "next batch" halves, Kanban's
  columns, Home. A "fold all" or "open all" control.
- Any server, protocol, CLI, card, hook or AGENTS.md change. Storing the fold anywhere but the
  browser.
- Removing or reworking the writes count, its list, its button, the "modified" mark or Home's
  "Written by the board" tile. Showing whether a watcher runs. A link to the Help page
  (board-help-page may explain more; neither CR needs the other).
- The CR board pane (`hooks/register.tsx`): untouched, so the pane screenshot rule does not apply.

## Overlaps in batch-30

- **CR-427 (board-running-batch-lane)** shares `js/ui/column.js`, `js/triage/columns.js`,
  `css/components/column.css`, `css/views/triage.css` (this CR does not change the last one) and
  DESIGN.md.
  - CR-427 adds a named-lane variant (`name`, `sub`) to `lane(parts)` and removes
    `triage.running` / `triage.idle`.
  - This CR adds `fold`, `folded` and `foldLabel` to the same function, used only by `laneOf` for
    P1 to P4. Its new DESIGN.md section does not touch CR-427's lines.
  - Whichever lands second rebases onto the other's `lane()`. No `depends.json`: a shared file is
    not a dependency (Q15).
- **CR-433, CR-434, CR-435** (the Batch page) and **CR-429** (the server's watching) share no file
  or behaviour with this CR. CR-434 adds the store preference `batchTab` through the same
  `pref`/`setPref`; `triageFolded` is a different key.
- **board-help-page, board-batch-view, board-history, board-griller, board-user-inbox,
  dashboard-pages**: none touches Triage's lanes or the journal panel, as their answers stand
  today. board-help-page may explain the count at more length. That needs no change here.

## Evidence

**No host or default matrix.** The behaviour depends on neither the host nor a configured value;
the kept choice is the browser's own `localStorage`, the same on every OS.

**Checks in `just check`** (all read the shipped files at the head under test, from the
repository):

- `tests/test_code_targets.py`, `test_the_web_frame_has_small_scripts_and_both_word_files_share_their_keys`:
  `en*.js` and `fr*.js` have the same keys, and every script stays under 300 lines. It passes
  unchanged.
- `tests/test_board_design.py`: the token table, the sheets' rules (no literal, no side accent, a
  component styled in its own sheet only, `column-*` classes written by `js/ui/column.js` only)
  pass with the new `column-folded` and `column-fold` classes and the `journal.css` margin.
- One new test in `tests/test_board_design.py`, parametrized over `en` and `fr`, reading the
  shipped `js/i18n/<lang>-write.js`, `js/ui/column.js`, `js/journal/journal.js` and DESIGN.md from
  the repository as they ship:
  - each word file defines `triage.fold`, `triage.unfold`, `journal.what`, `journal.why`,
    `journal.todo` and `journal.tip`;
  - no shipped file under `js/` contains `journal.note`;
  - `js/ui/column.js` writes `data-fold`, `aria-expanded` and `column-folded`;
  - in `js/journal/journal.js`, `journal.what` comes before `<ul` in `journalPanel`, and the
    button writes `journal.tip` in a `title`;
  - DESIGN.md has the heading "Triage: folded rows and the writes count".

  This test is a guard on shipped text. The behaviour itself is proved in the browser (below),
  since the project has no JavaScript test runner.
- Biome (`just check`'s web frame step) passes on the new and changed scripts.

**In a browser** (the Driver, on a board serving a surface with items in at least P1, P2 and P4,
for instance the demo surface `just docs-screenshots` builds, or `chantier board` on a test
surface; Chromium at PC and phone widths). The PR's Deliverables carry the screenshots named
below, captioned with the head's SHA (seven characters):

1. On first load, all four rows are open, each head showing a chevron pointing down.
2. Click P2's head: its post-its hide. Its chip, count and grill-state counts stay, the chevron
   points right, and `aria-expanded` is `false`. Screenshot (PC, English).
3. Reload: P2 is still folded. Switch to another project's Triage: P2 is folded there too. Back.
4. Tab to P2's chevron and press Enter, then Space: it opens and folds again. The focus stays on
   the button.
5. Select two post-its of P2 (open), then fold P2: the selection bar disappears (both left the
   selection). Open P2: they are not selected.
6. Drag a post-it from P1 onto folded P2's head: the head lights while over it, the post-it moves
   to P2, P2 stays folded and its count goes up by one. Drag a group by its handle onto it: same.
7. Select a post-it of P4 and press "→ P2" in the selection bar: it moves, and P2 stays folded.
8. Set a label filter: folded P2's counts equal those P2 shows when opened under the same filter.
9. Empty P3 (or use an empty row): its chevron folds and opens it. A write landing in a folded row
   does not open it.
10. In the browser's console, set `localStorage['chantier.triageFolded'] = 'P9,,{x'` and reload:
    all rows are open, and the page shows no error. Set it to `'P1,P4'`: P1 and P4 are folded.
11. Hover the journal button: the tooltip shows `journal.tip`. Click it: the panel opens on the
    heading, then the three lines (what, why, what to do), then the list and the buttons. No note
    sits at the bottom. Screenshot (PC, English).
12. Switch the board to French: the same panel in French (with "tu"), the chevron's label in
    French (`Masquer les post-its de P2`). Screenshot (PC, French).
13. At a phone width (390 px): fold and open a row by a tap on its head. The head is at least
    `--nav-height` tall. The panel's text wraps and reads whole. Screenshot (phone).
14. Press "I said 'rescan' to the CoS": the count goes back to zero and the toast says so, as
    today. Home's "Written by the board" tile follows, as today.

**Screenshots in docs**: `just docs-screenshots` run, its three Triage pictures committed.

**Gates** (AGENTS.md): the web client sits under the CLI's `src/`, so the Driver runs `just check`
and `just eval-dry-run` in the worktree at the rebased head before the first push. The pipeline's
`just scenario (ubuntu-latest)` job must be green at the PR's head. The scenario itself does not
change: it drives no browser. `just mod` is not owed (no `hooks/` or `types/` change).

## Open questions (each built as A)

1. **`docs/web-board.md`.** Q13 says "nothing outside the web client" but retakes the docs'
   screenshots. A (recommended, built): update the Triage section's two bullets so the user docs
   stay true. B: leave `docs/web-board.md` as it is.
2. **The button's label.** Q11 allows a clearer label "if one fits the same place". A
   (recommended, built): keep "✎ N writes since your last 'rescan'"; the tooltip and the panel
   carry the explanation. B: a shorter label, such as "✎ N board writes to tell the CoS".
3. **The kinds the explanation names.** Q10 lists moves, new ideas, labels and groups; the journal
   also counts edits, the next-batch declaration and configuration saves. A (recommended, built):
   name Q10's four "for example". B: name every kind.
4. **A selected post-it moved into a folded row by another write.** Q7 covers a fold; it is silent
   on a post-it that lands in an already folded row. A (recommended, built): `selectedNow` leaves
   it out too, so the selection bar never acts on a hidden post-it (Q7's reason). B: only the fold
   itself clears the selection.
