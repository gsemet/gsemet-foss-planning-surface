# Change Specification: a batch navigator on the Costs and Batch pages, and the receipt copied as an image

## Goal

The user, 2026-11-17: on the web board, move through the batches from the Costs page and the Batch
page with one simple navigator (previous, next, latest); copy the cost receipt as an image into the
clipboard; and say "Change Request" in full in the receipt's per-CR heading.

This CR absorbs the inbox item `cost-receipt-batch-chooser` (choosing a batch other than the running
or last closed one on the Costs page) and the batch history navigation (previous / next) of the
inbox item `board-batch-view` (scope-Q1). `board-batch-view` keeps its connected cards, their
arrowheads and the tooltip on the batch mode: none of those is done here.

No issue: the request is verbal.

## Decisions carried from `02-answers.md`

- scope-Q1: this CR holds the four points of `intake/request.md`; it absorbs
  `cost-receipt-batch-chooser` and the previous / next navigation of `board-batch-view`, nothing
  else of that item.
- nav-Q2: the navigator is two arrows around the batch's id and a "Latest" pill, in the page header
  next to the title, on the Costs page and on the Batch page: `‹ batch-04 ›` then the pill
  "Latest" (French "Dernier"), shown only when the page is not on the last batch. `‹` is greyed out
  on the first batch, `›` on the last. The batch shown is in the URL (`&b=batch-04`), so a link
  opens the same batch.
- receipt-Q7: the image copy needs a secure origin (`127.0.0.1` or `localhost`). From another
  machine of the local network over http the button is greyed out and its tooltip says why ("image
  copy only works on this machine"); no download and no other replacement.
- nav-Q9: a past batch keeps the order of its CRs and the dependencies between them. `close`
  records each CR's order and `after` list in the batch's record, and the Batch page draws a
  closed batch's graph from it, with its arrows. For a batch closed before this change, what its
  archived files still give is used; where nothing gives the dependencies, the page says so and
  invents no arrow.
- Settled by the Chief of Staff (nav-Q9): `b=` stays between Costs and Batch and is cleared on
  any other view or project; an abandoned record that is neither closed nor the live batch is left
  out of the navigator.
- receipt-Q14: the board listens on every address by default and prints its LAN link, plain http,
  so the copy would be greyed out even on the user's machine. The board also prints the
  `http://127.0.0.1:<port>/?k=...` link next to the LAN one (same key), and the greyed button's
  tooltip links to that 127.0.0.1 address.
- Settled by the Chief of Staff (round 2): the image method and the content security policy change
  (`blob:` or `data:` in `img-src`) are what the Driver proves in Chrome, Edge and Firefox,
  recorded in the PR.

## What changes

All paths below are under `skills/chantier/scripts/cli/src/chantier/board/` unless named in full.

### 1. The batches the navigator moves through (`web/js/model/history.js`)

Add one pure function, `batchSequence(data)`: the ids of the batches the navigator walks, oldest
first. It holds every record of `data.history` whose `state` is `closed`, plus the running or
paused batch (`data.batch.id`) when there is one; ordered by the record's `number` (the live
batch's number is the digits of its id). A record that is neither closed nor the live batch (an
abandoned `running` record such as `batch-20.json` of this project, with no CR and no folder) is
not in the sequence. The last id is "the latest batch": the live batch when there is one, else the
newest closed record; it is what the pages show today with no choice.

### 2. The address (`web/js/core/router.js`, `web/js/core/store.js`)

- The place gains a third part, the chosen batch: the store's new key `batchId` (`null` = the
  latest batch; comment it in `store.js` like the other keys). The address carries it as `b`:
  `href()` writes `b=<id>` only when `batchId` is set; `resolve()` reads `b`; `go()` takes
  `place.batch` (`undefined` keeps the current one, `null` clears it).
- `b` survives a move between the Costs and the Batch pages (the same navigator, the same batch);
  a move to any other view or to another project clears it. The back and forward buttons restore
  it with the rest of the place (`listen()` already re-resolves the address).
- An unknown `b` (no such id in `batchSequence`, or the data not read yet) shows the latest batch,
  as if absent; the navigator then shows the latest batch with no "Latest" pill.
- The header comment of `router.js` names the new part (`?p=<project>&v=<view>&b=<batch>`).

### 3. The navigator (new `web/js/ui/batch-nav.js`, `web/css/batch-nav.css`, `web/index.html`, `web/js/main.js`)

- `index.html`: a new element in `.titlerow`, right after `h1#title`: `<nav class="batchnav"
  id="batch-nav" hidden></nav>`, with an `aria-label` set by the code; link `css/batch-nav.css`
  with the other frame stylesheets. (The id `bnav` is the bottom bar's: do not reuse it.)
- `batch-nav.js` exports `navigator(state)`: empty unless the project is not "All projects", the
  project's data is read, the view is `costs` or `batch`, and `batchSequence` is not empty. Its
  markup: a button `‹` (`data-batch-go="<previous id>"`, `aria-label` "Previous batch"), the shown
  batch's id as text, a button `›` (`data-batch-go="<next id>"`, "Next batch"), then, only when the
  shown batch is not the latest, a pill button "Latest" (`data-batch-go=""`). `‹` has `disabled` on
  the first batch of the sequence, `›` on the latest. The shown batch is `batchId` when it is in
  the sequence, else the latest.
- `main.js`: `drawFrame` paints `#batch-nav` with `navigator(state)` and sets its `hidden` when the
  markup is empty; `listenToFrame` delegates `click` on `[data-batch-go]` to
  `go({ batch: el.dataset.batchGo || null })`, through the same `guarded` wrapper as the other
  moves. Clicking "Latest" clears `b` (the address then follows the latest batch as it changes).
- `batch-nav.css`: the arrows as small ghost buttons, the id in the title's font at the stats'
  size, the pill in the accent tint the receipt's `.pill` uses (`--accent-tint-2`, `--accent`); a
  disabled arrow in `--ink3` with no hover. On a phone (`max-width: 760px`) the navigator wraps
  under the title.
- Words, in `web/js/i18n/en-board.js` and `fr-board.js` (English, French):
  `batchnav.label` "Batches" / "Batches", `batchnav.prev` "Previous batch" / "Batch précédent",
  `batchnav.next` "Next batch" / "Batch suivant", `batchnav.latest` "Latest" / "Dernier".

### 4. The Costs page on the chosen batch (`web/js/model/receipt.js`, `web/js/views/costs.js`)

- `shownBatch(data, chosen)`: with `chosen` the id of a closed record, `{ live: false, rec }` of
  that record; with `chosen` null, unknown, or the live batch's id, today's answer (the live batch,
  else the newest closed record). `receiptOf(state)` passes `state.batchId`. Update both modules'
  header comments ("the running batch, else the last closed one" becomes "the batch the navigator
  shows; by default the running batch, else the last closed one").
- `costs.js` needs no other change: `ageLine`, `figures` and `rowsOf` already draw a closed record
  by its id. The Earlier batches table and the Last merged CRs card stay as they are.

### 5. A past batch's order and dependencies

#### 5a. `close` records them (`chantier/history.py`)

`cr_entry` (called by `close_record`, itself called by `commands/close_archive.py`'s
`_close_files`) adds two keys to each CR of the record: `"order": c.order` and
`"after": list(c.after)` (the CR ids the CR waited for at close, as `order after` and
`depends.json` left them in `batch.json`, the release CR's list included). `close_record`
already writes the CRs sorted by `order`; that stays. `blank_record` and `open_record` do not
change (a running batch's record lists no CR). `batch-NN.md` does not change.

#### 5b. What a batch closed before this change still gives (new `board/archived.py`, `board/state.py`)

What this project's archives hold, checked on 2026-11-17: the batch's own files
(`batch.json`, `events.jsonl`) are deleted at close, so the dependencies set during a batch
(`order after`, the `depends` events) are gone; an archived CR's `STATUS.json`, when there is
one, has `waits: []` at merge. What remains is the `depends.json` an archived CR folder still
holds (31 of 214 folders here): its `after` names the CRs it was planned after, by folder slug
(`{"after": ["fast-scenario"]}`), sometimes by CR id. Example: in `batch-18`, CR-254, CR-255,
CR-265, CR-266 and CR-267 give their links that way, while CR-275's wait on CR-268..CR-274 (an
`order after`) is lost.

- `archived.py`, one function `recovered_after(changes, record)`: for a closed record whose CRs
  have no `after` key, it reads, for each CR with an `archive` path whose folder exists (in
  `5-archives/` or `6-trash/`), that folder's `depends.json` (`backlog.depends_of`), and
  maps each name to a CR of the same record: a CR id as is, a slug to the CR whose archive folder's
  name ends in `-<slug>` after its `<YYMMDD-HHMM>-<number>-` prefix. A name that matches no CR
  of the record (a CR of an earlier batch) is dropped. It returns the record with each CR's
  `after` set to what it found and the record's new key `after_source`: `"archives"` when at
  least one CR folder could be read, `"none"` when none could (an older back-filled record with
  no archive path, or folders gone). A record that already has `after` on its CRs gets
  `after_source: "record"` and is not touched. It reads only; it writes nothing.
- `state.py`'s `_history` passes each closed record through `recovered_after`. Its order
  needs nothing: the record's CRs are already in their order, and `order` is read when present.

#### 5c. The Batch page on a closed batch (`web/js/views/batch.js`, `web/js/views/batch-graph.js`, `web/js/ui/header.js`, `web/js/model/history.js`)

With `batchId` naming a closed record, the Batch page draws that record; with none (or the live
batch's id), it draws the live batch as today.

- `history.js`, a pure function `recordRows(record)`: each CR of the record as the row the graph
  reads: `{ cr, title, folder: <archive's last part>, state: result === 'merged' ? 'merged' :
  'cancelled', round: rounds, cost_usd, pr, after, order }`, sorted by `order` when present,
  else in the record's order.
- The graph: `graphBlock` and `drawEdges` take those rows, so `levels()` places the CRs by
  their dependencies and the arrows are drawn as for a live batch (the same hover light). A node
  shows the CR, its folder name, its title, the badge `merged` or `cancelled` (the existing
  `state.*` words), its rounds, its cost and "PR" when it has one; it carries no opener (a click
  does nothing). `batch.js`'s `mount` and `after` redraw the edges from the rows shown, live
  or recorded.
- A line above the graph, from `after_source`, in both languages: `"record"` none;
  `"archives"` `batch.deps_partial` "Dependencies from the archived CR folders only: those set
  during the batch were not kept." / "Dépendances tirées des dossiers archivés des CRs seulement :
  celles posées pendant le batch n'ont pas été gardées."; `"none"` `batch.deps_none`
  "Dependencies not recorded for this batch: no arrow." / "Dépendances non enregistrées pour ce
  batch : aucune flèche." With `"none"` every CR stands in level 0, in its order.
- The figures: CRs merged out of the total, the dropped ones, the rounds summed, spent against the
  budget (`cost_usd`, `budget_usd`), from the record only.
- The mode strip: the record's `mode` and `steering`, the mode's sentence, the three modes with
  the record's lit.
- No PR column: a closed batch has no PR to review.
- `header.js`, `crumbs()`: on the Batch page the crumb shows the shown batch's id. For a closed
  record its chip has the grey `queued` look (`stateIcon('queued')`, the grey `--chip`
  background) with the word `state.closed` ("closed" / "clos", new key); for the live batch it
  keeps today's chip. The CR `board-kanban-priority-colours` edits `crumbs()` too: whichever of
  the two merges second rebases and keeps both changes (its colours, this chip and its grey
  `--chip` background).
- The sidebar's Batch count (`views/registry.js`) keeps the live batch's id.
### 6. Copy the receipt as an image (`web/js/views/costs.js`, new `web/js/views/costs-image.js`, `reply.py`, `board/command.py`, `board/routes.py`)

- A button "Copy as image" / "Copier en image" (`costs.copy_image`) in the Costs page's `.age` line
  (`ageLine` in `costs.js`), for the live batch and for a closed record alike; it is not inside the
  ticket, so it is never in the image. It carries `data-copy-receipt` and `data-key="copy-receipt"`.
- Disabled, in two cases. Its tooltip is a `span` that wraps it (`tabindex="0"`, so it opens on
  hover and on focus; a disabled button gets no pointer events), drawn like the Batch legend's
  `.lgpill .tip` (`views/batch-graph.js`), so it can hold a link:
  - not a secure origin (`!window.isSecureContext`): `costs.copy_insecure` "Image copy only works
    on this machine, at {link}" / "La copie en image ne marche que sur cette machine, à {link}",
    `{link}` an `<a>` to the board's 127.0.0.1 address (`local_url` of `api/board`, below)
    that opens the same page there (the same `?p=&v=&b=` appended after the key). When the board
    gives no `local_url` (it listens on one non-loopback address only), the text is
    `costs.copy_insecure_nolink` "Image copy only works on this machine, at a 127.0.0.1 address" /
    "La copie en image ne marche que sur cette machine, à une adresse 127.0.0.1", with no link;
  - a secure origin whose browser lacks `navigator.clipboard.write` or `ClipboardItem`:
    `costs.copy_unsupported` "This browser cannot copy an image" / "Ce navigateur ne sait pas copier
    une image".
  No download link and no other replacement in either case (receipt-Q7).
- `costs-image.js` exports `copyReceipt(root)`: it builds a PNG of the `.ticket` element as drawn,
  with no third-party code:
  1. Clone the ticket, drop from the clone any interactive part (the `.r-act` Recompute button of a
     receipt "not computed yet").
  2. Read the text of the stylesheets the ticket uses (`css/tokens.css`, `css/base.css`,
     `css/fonts.css`, `css/components.css`, `css/views/costs-receipt.css`) with `fetch` (same
     origin), and the two Inter fonts as `data:` URLs in an `@font-face` that replaces the
     `fonts.css` one, so the image draws with the board's font.
  3. Wrap the clone, at the ticket's rendered width, in an SVG `<foreignObject>` with those styles,
     with a margin of 24 px on the page's background colour so the shadow and the scalloped bottom
     edge show; load it in an `Image` from a `blob:` URL (`URL.createObjectURL`) or a `data:`
     URL, draw it on a canvas at `Math.max(2, devicePixelRatio)` times the size, and
     `canvas.toBlob('image/png')`.
  4. `navigator.clipboard.write([new ClipboardItem({ 'image/png': <the promise of that blob> })])`,
     called at once from the click handler (a promise inside the `ClipboardItem`, so a browser that
     wants the user's gesture still has it). Revoke a `blob:` URL after.
  This method is not proved yet (a canvas may be tainted by a `foreignObject` image, a font may
  not load inside it). The Driver proves it first in Chrome, Edge and Firefox, on `127.0.0.1`,
  and keeps the one form that works in all three (`blob:` or `data:`); the PR's body says which,
  and what each browser did. When the method fails in one of them the Driver stops and says so to
  the Chief of Staff: no other route without the user (no library, no canvas redraw).
  Success: the toast `costs.copied` "Receipt copied as an image" / "Ticket copié en image"
  (`ui/toast.js`, `toast()`). Failure: the error toast `costs.copy_failed` "The image could not be
  copied: {error}" / "L'image n'a pas pu être copiée : {error}", with the browser's message.
- While the copy runs the button is disabled and reads `costs.copying` "copying…" / "copie…".
- `reply.py`, `HTML_POLICY`: `img-src 'self'` gains the one source step 3 proved, `blob:` or
  `data:`.
- The 127.0.0.1 link (receipt-Q14):
  - `board/command.py`: after its `board on <link> over <folder>` line (unchanged: the scenario
    parses it), when the board listens on every address (`host in EVERYWHERE`, `address.py`) and
    that link is not already a loopback one, it prints a second line
    `on this machine: http://127.0.0.1:<port>/?k=<key>` (`[::1]` for `::`: `_loopback_of`);
    `board already running at <link>` gets the same second line in the same case. A board bound to
    one address prints none (127.0.0.1 does not answer there). A new function in `address.py`,
    `local_url(host, port, key)`, gives that link or `None`.
  - `board/routes.py`, `board()`: `api/board` gains `"local_url"`, that link or `null`
    (the page holds no key in script: the key is in a cookie, `core/api.js`; the route is
    already behind the key).
  - `skills/chantier/references/session-start.md`, the `board on <URL> over ...` bullet: the
    Chief of Staff gives the user both links when the board prints the second one, the 127.0.0.1 one
    named as the one where the receipt's image copy works. A card change: `just scenario` before
    the PR (it already is required).- `mount` in `costs.js` delegates `click` on `[data-copy-receipt]` to `copyReceipt(root)`.

### 7. The receipt's per-CR heading (`web/js/i18n/en-costs.js`, `fr-costs.js`)

`costs.receipt_detail`: "Detail · per CR" becomes "Detail · per Change Request"; "Détail · par CR"
becomes "Détail · par Change Request". No other word changes ("Per CR, {batch}", the table heads
and "Sum of the CRs" stay).

### 8. Documentation (`docs/web-board.md`)

- Costs: the page shows the batch the navigator chose, by default the running batch, else the
  newest closed one; the navigator (`‹ batch-04 ›`, Latest) and the `b=` of the address; the
  "Copy as image" button and its greyed state off this machine, with its link to the 127.0.0.1
  address.
- The board's start (`docs/web-board.md`, "Starting the board"): the second line,
  `on this machine: http://127.0.0.1:<port>/?k=...`, when the board listens on every address.
- Batch: the same navigator, and what a closed batch shows: its graph from the record, the line
  when its dependencies come from the archives only or are not recorded.
- `docs/costs.md` (or wherever the record's keys are named): each CR of `batch-NN.json` now
  carries its `order` and its `after` list.
- The screenshots in `docs/web-board/` are not retaken in this CR (`just docs-screenshots` is by
  hand, before a release).

## Out of scope

- `board-batch-view`'s connected cards, their arrowheads with several sources, and the tooltip on
  the batch mode.
- Rewriting the existing records: `batch-01.json`...`batch-23.json` stay as they are; the board
  reads what their archives give, at each read.
- Any other new key in the record than each CR's `order` and `after`.
- Any other page (Home, PRs, Kanban, Triage, Configuration): no navigator there.
- A download of the receipt, or a copy from a non-secure origin.
- Any other route or field of the board's server than `local_url` in `api/board`: the page
  already receives every record in `data.history`.

## Sequencing with the other CRs of the next batch

- `board-kanban-priority-colours` also edits `crumbs()` in `web/js/ui/header.js`: the second
  to merge rebases and keeps both (section 5c).
- `board-picker-surface-item` also edits `web/js/main.js`: an ordering point only (the second
  to merge rebases); neither changes what the other does. No `depends.json` is needed for either.

## Evidence

- `just check` green on Linux, macOS and Windows (ruff, mypy, Biome on `board/web`, the tests).
- One test line: in `skills/chantier/scripts/cli/tests/test_board.py`, `test_the_frame_is_shipped_with_the_package` asserts
  `img-src` in `reply.HTML_POLICY` holds the one source the Driver proved (`blob:` or `data:`), and lists `css/batch-nav.css` and
  `js/ui/batch-nav.js` among the shipped files. The page's behaviour is proven in a browser, below.
- In the same file, one parametrized test of
  `recovered_after` on a prepared planning folder: a record whose CRs carry `after` (untouched,
  `"record"`), one whose archived folders hold a `depends.json` by slug and by CR id with a
  name of an earlier batch (mapped, the stranger dropped, `"archives"`), and one with no archive
  path (`"none"`). And in `test_board.py`: `address.local_url` gives the 127.0.0.1 link for
  `0.0.0.0`, the `[::1]` one for `::`, and `None` for one specific address.
- `just scenario` (ubuntu-latest) green at the PR's head, its close check (`run_scenario.py`,
  "its CRs carry the result, an archive that exists, the PR, the rounds and the cost") extended:
  each CR of the closed record carries an integer `order` and an `after` list, the CR the unit
  made wait on another (by `order after` or `depends.json`) lists it, and the list is sorted
  by `order`.
- A browser check by the Driver on the board served over `127.0.0.1` against this project's
  planning surface (closed records `batch-01`...`batch-23`), with screenshots kept in the CR's
  `evidence/`:
  1. Costs, no `b`: the latest batch, no "Latest" pill, `›` greyed.
  2. `‹` twice: the address shows `&b=<id>`, the receipt, figures and Per CR table are that
     batch's; the pill "Latest" shows; reloading the address opens the same batch.
  3. `‹` down to `batch-01`: `‹` greyed; a pre-receipt record reads "roles not recorded".
  4. Switch to the Batch page: same batch, crumb chip "closed"; on `batch-18` the arrows CR-253 →
     CR-254 → CR-255, CR-265 → CR-266 (from `depends.json`) and the "archived CR folders only" line;
     on a back-filled record with no archive path the "not recorded" line and no arrow; "Latest" goes back to the live or newest batch and drops `b`; the browser's back
     button returns to the previous batch.
  5. Another view, then back to Costs: `b` is gone. An unknown `b=batch-99` shows the latest.
  6. Copy as image on `127.0.0.1`: paste in an image editor or a chat; the image is the ticket with
     its font, its cut line, its scalloped edge and no button; in Chrome, Edge and Firefox each,
     the PR's body naming the source kept (`blob:` or `data:`) and what each browser did.
  7. The board started with its default (every address): it prints the LAN line and the `on this
     machine: http://127.0.0.1:...` line. Opened at the LAN address: the button is greyed, its
     tooltip opens on hover and on focus and its link opens the same page at 127.0.0.1, where the
     copy works.
  8. The heading reads "Detail · per Change Request" in English and "Détail · par Change Request"
     in French; the navigator's words in both languages.
  9. A phone width (760 px or less): the navigator wraps under the title and stays usable.

## Open questions

None: nav-Q9 and receipt-Q14 settled the last ones.
