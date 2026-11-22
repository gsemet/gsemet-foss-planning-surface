# Batch graph: transitive reduction, merged CRs folded, fewer crossings

This change makes the board's batch Graph tab readable on a real batch. It draws only the waits that
no chain of other waits already implies, folds the merged and cancelled CRs behind one "N merged"
chip, orders the cards within a level to cut crossings, and fits the graph to the central column
with no empty canvas below it. It touches the web client only, in English and French. No server,
protocol, CLI, card or record change.

## Goal, in the user's terms

The user, 2026-11-22, looking at batch-30's Graph tab (`intake/request.md`):

- CR-447 declares 30 waits, and each one is drawn as a long edge across the graph, though most are
  implied by a chain (CR-447 → CR-458 → CR-457 → CR-456). Draw the transitive reduction only.
- The merged CRs take most of the columns, while the dozen CRs in flight are what matter. Fold the
  merged ones.
- The cards within a level are not ordered to reduce crossings.
- With the "PR à revoir" side panel, only two and a half levels fit and the graph scrolls
  sideways, while a large empty area sits below it.

"Oui met la dans le batch en cours": batch-30, before CR-447 docs-gardening, one Driver within 3
rounds.

## Decisions carried (02-answers.md)

| Answer | Decision | Where |
| --- | --- | --- |
| Point 1 | Only the transitive reduction of the waits among the drawn CRs is drawn. The hidden waits stay discoverable: hover lights every declared wait's card, and the card's wait count names them all. | 1, 3 |
| Point 2 | The merged and cancelled CRs of a live batch are folded behind one chip, "N merged", which expands them back into their levels. | 2, 3 |
| Point 3 | A barycentre ordering within each level, deterministic. | 1, 3 |
| Point 4 | The levels share the central column's width, so a normal batch does not scroll sideways at desktop width with the PR column. The canvas is as tall as its tallest drawn level and no taller. | 4, 5 |
| Placement | batch-30, before CR-447; 3 rounds. | Overlaps |
| No further grill | The detail below is settled here. The behaviour choices made without the user are listed in Decisions, each with the option built (A). | Decisions |

## What the code shows today

Read at `dce2c644`. All paths below are under
`skills/chantier/scripts/cli/src/chantier/clients/web/` unless named in full.

- `js/model/semantics.js`:
  - `levels(rows)` puts each CR one level after its deepest declared wait among `rows`;
  - `edges(rows)` returns one `[from, to]` per declared `after` whose row is there;
  - `related(rows, id)` returns the CR, its declared waits and its declared dependants, which is
    what a hover lights.
- `js/views/batch-graph.js`:
  - `graphBlock(rows, batch, now, recorded)` draws every row: merged ones included, in record order
    within each level (`levels`);
  - `drawEdges(root, rows)` draws one path per `edges(rows)` pair and one head per waiting CR;
  - `light` / `lightEdges` light the CR, its related cards and the paths in the DOM that touch it.
- `css/views/batch-graph.css`: each `.lvl` is a fixed `width: 300px` (250px on a phone), with
  `gap: var(--space-off-90)` between levels. `.graph` has `min-width: max-content`, inside
  `.gscroll` (`overflow-x: auto`).
- `css/views/batch.css`: `.bwrap` is `minmax(0, 1fr) 380px` with a 20px gap, and `--side-width` is
  248px with `--gap-main` 32px each side. At a 1600px viewport the central column is about 870px
  wide, which holds two levels and a fraction (one level costs 390px). This is the user's "two and a
  half levels".
- Height:
  - in batch-30 about 19 CRs have no wait, so level 0 is a column of about 19 cards, and the other
    levels sit beside a tall, mostly empty canvas;
  - also, `drawEdges` sets both SVG layers' `height` to `graph.scrollHeight`. That value already
    includes the layers' previous height (they are absolutely placed children of `.graph`), so the
    canvas can only grow, never shrink, until a re-render. The Driver confirms this with a measure
    (Evidence), and the fix below holds whether it shows or not.
- The Gantt (`js/views/batch-gantt.js`) uses `edges(rows)` and `badge(c)` too.

## What changes

### 1. The model: reduction and order (`js/model/semantics.js`)

Two new pure exports, beside `edges`. `edges`, `levels` and `related` stay as they are, so the
Gantt keeps every declared wait.

- **`reducedEdges(rows)`**: the pairs of `edges(rows)` that no other path among `rows` implies.
  - A pair `[a, b]` is dropped when some `c ≠ b` with a pair `[a, c]` reaches `b` through pairs of
    `edges(rows)`.
  - Order: the pairs kept come in `edges(rows)`'s order.
  - Cycle: if the waits among `rows` hold a cycle (which `levels` already tolerates), it returns
    `edges(rows)` whole. A reduction of a cycle could drop both of a pair.
  - The reduction is computed over the rows given, that is the drawn ones. A wait is never hidden
    for a reason the user cannot see.
- **`orderLevels(cols, pairs)`**: `cols` is `levels(rows)`'s output and `pairs` is
  `reducedEdges(rows)`. It returns new columns with the same CRs in each level, reordered:
  - a CR's position is its index in its column;
  - pass 1 (down): for levels 1 to the last, sort each column by the mean position of the CR's
    sources in `pairs`. A CR with no source keeps its current position as its key;
  - pass 2 (up): for the last level but one down to 0, sort each column by the mean position of
    the CR's targets in `pairs`. A CR with no target keeps its current position;
  - pass 3: pass 1 again;
  - each sort is stable: ties keep the current order, so the record's order breaks them;
  - the order depends only on the rows drawn and their waits, never on a state or a time. A repaint
    that changes no wait and no fold moves no card;
  - a card's place does change when a wait is added or removed, and, while folded, when a CR merges
    or is cancelled (it leaves the graph, and the levels and orders are computed again without it).
    This replaces today's rule that each CR keeps one place for its whole life.

### 2. The fold of the done CRs (`js/views/batch-graph.js`)

- A **done** CR is one whose `state` is `merged` or `cancelled`.
- A module-level `unfolded` flag, `false` at load, with `toggleFold()` exported.
- Live batch (`recorded` false), when at least one row is done and at least one is not:
  - folded (the default): `graphBlock` draws the rows that are not done. Its levels are
    `levels(shown)`, so a CR whose only waits are done moves to level 0. A wait on a done CR is met
    and is not drawn;
  - unfolded: every row is drawn, in today's levels (`levels(rows)`).
- A live batch with no done row, or with every row done: every row is drawn, and there is no chip.
- A closed record (`recorded`): no fold. Every row is drawn, as today, with reduction and ordering.
- The chip, in a bar above `.gscroll` and inside the tab panel:
  `<div class="gbar"><button type="button" class="tag st merged[ off]" data-fold aria-expanded="<bool>" title="<hint>">…</button></div>`.
  - It is the chip in its toggle form, as the Inbox's kind filters build it (`tag st <state>[ off]`;
    DESIGN.md: filled when on, outlined grey `.tag.st.off` when off), in the merged state's colour
    (`.tag.st.merged`). Folded is `off`, unfolded is on.
  - Its text is `t('batch.fold_merged', { n })` ("12 merged"). When the batch holds cancelled CRs,
    it adds ` · ` and `t('batch.fold_cancelled', { n })` ("· 1 cancelled").
  - Its `title` is `t('batch.fold_show')` when folded and `t('batch.fold_hide')` when unfolded.
- `batch.js`'s `graphTab.mount` adds `delegate(root, 'click', '[data-fold]', …)`, which calls
  `toggleFold()` then `update({})` (the store's re-render), and returns its stop with the others. A
  keyboard Enter or Space works because the chip is a `<button>`.
- The fold is not kept across reloads (Decision 1).

### 3. The graph view (`js/views/batch-graph.js`)

- `graphBlock`:
  - computes `shown` (section 2), `cols = orderLevels(levels(shown), reducedEdges(shown))`, and
    draws `cols`;
  - the fold bar comes first when section 2 says so;
  - the rest of the markup stays: `.gscroll`, `.graph`, both `svg.edges` layers, `.lvl`, `.lvlh`,
    and the hint.
- `drawEdges(root, rows)`:
  - draws the reduction of the CRs present in the DOM:
    `const shown = rows.filter((c) => found(c.cr))`, then `reducedEdges(shown)` in place of
    `edges(rows)`;
  - the DOM is therefore the one truth for what is folded, and `batch.js`'s `rowsNow()` does not
    change;
  - heads: one per waiting CR of the reduced pairs, as CR-441 made them.
- Canvas size, in `drawEdges`:
  - before it measures, it sets both layers' `width` and `height` to `0`;
  - it then reads `graph.scrollWidth` and `graph.scrollHeight` and sets them;
  - so the canvas is the levels' size, with no growth carried from an earlier draw.
- `light` is unchanged:
  - `related(rows, id)` still reads the declared `after`, so a hover lights the cards of every
    declared wait, the implied ones included, while only the reduced arrows are drawn and lit;
  - this is how a hidden wait shows on hover.
- The wait count on a node (`deps(c)`):
  - it keeps the declared count, `c.after.length`, all waits included;
  - its span gets `title="${t('batch.waits_for', { list: c.after.join(', ') })}"` ("Waits for
    CR-435, CR-438, …"), on live and recorded nodes alike;
  - so the card names every wait, drawn or not, folded or not.
- The file's head comment: its first sentence's "each CR in its place for its whole life (its
  level, then the record's order)" is rewritten to say that a CR sits in its level, ordered by a
  barycentre pass of the drawn arrows, and that its place changes when a wait changes or, while
  folded, when a CR merges or is cancelled. One more sentence: only the transitive reduction is
  drawn, and done CRs are folded on a live batch.

### 4. Fit to the width (`css/views/batch-graph.css`)

- `.batch .graph`:
  - `min-width: max-content` becomes `min-width: min-content`;
  - `gap: var(--space-off-90)` becomes `gap: var(--space-off-30)`.
- `.batch .lvl`:
  - `width: 300px` becomes `flex: 1 1 0; min-width: 180px; max-width: 300px;`;
  - it also gets `container: graph-level / inline-size;`.
  - The levels then share the column's width, up to 300px each. When even 180px each does not fit,
    `.graph` grows past `.gscroll`, which scrolls sideways as today.
- Phone (`@media (max-width: 760px)`):
  - `.batch .lvl { flex: none; width: 250px; }`, as today;
  - the gap stays `var(--space-off-50)`;
  - the graph scrolls sideways inside its box, and the page does not.
- The target. At 1600 × 900 with the PR column, the demo's four levels (section 7) fit with no
  sideways scroll: about 810px of levels and gaps in about 840px. A narrower window, or a batch of
  more levels, scrolls inside the box (Decision 4).
- The arrows:
  - `path()` already caps its tail at a third of the span (`Math.min(TAIL, …)`), so a 30px gap
    keeps a level tail and a whole head;
  - `TAIL` and `HEAD` do not change.

### 5. The state badge on a narrow level (`js/views/batch-graph.js`, `css/components/chip.css`)

At 180px a node's top row cannot hold the folder chip, the CR tag, the badge's icon and its word
(the top row does not wrap; the slug label already shrinks to nothing, `.card-compact .lbl`).

- `badge(c)` becomes
  `<span class="sb <state>" title="<word>">${stateIcon(c)}<span class="sbw"><word></span></span>`.
  The Gantt keeps calling it, and nothing changes there (no `graph-level` container).
- `css/components/chip.css` gets `@container graph-level (max-width: 239px) { .sb .sbw { display: none; } }`.
  - On a level narrower than 240px the badge shows its icon only, in the state's colour, and its
    word stays in the `title`;
  - the legend pill keeps telling each icon's state;
  - this is the chip's own sheet styling its own variant (DESIGN.md, "Components"), with no new
    token (Decision 3).

### 6. Words (`js/i18n/en.js`, `js/i18n/fr.js`, beside the `batch.*` keys)

| Key | en | fr |
| --- | --- | --- |
| `batch.fold_merged` | `{n} merged` | `{n} mergé(s)` |
| `batch.fold_cancelled` | `{n} cancelled` | `{n} annulé(s)` |
| `batch.fold_show` | `Show the merged CRs in their levels` | `Afficher les CRs mergés dans leurs niveaux` |
| `batch.fold_hide` | `Fold the merged CRs` | `Replier les CRs mergés` |
| `batch.waits_for` | `Waits for {list}` | `Attend {list}` |

The counts take the plural with `(s)` in one key, as `home.merged` does (`{n} mergé(s)`); no `tn()`. Five new keys. `batch.arrow` (the legend's arrow
line) changes:

- en: `an arrow goes from a CR to the one that waits for it; a wait already implied by a chain of arrows is not drawn`;
- fr: `une flèche va d'un CR à celui qui l'attend ; une attente déjà impliquée par une chaîne de flèches n'est pas dessinée`.

No other key changes.

### 7. DESIGN.md, the demo and the docs

- **DESIGN.md**:
  - section `## The Batch graph's arrows`, new bullets:
    - only the transitive reduction of the waits among the drawn CRs is drawn (`reducedEdges`), and
      the Gantt keeps every declared wait;
    - a hover still lights every declared wait's card;
    - a node's wait count holds every declared wait, and names them in its `title`.
  - a new short section, `## The Batch graph's layout`:
    - the levels share the central column (`flex: 1 1 0`, 180px to 300px, 30px apart), and the box
      scrolls sideways only when they do not fit;
    - the canvas is measured from zero at each draw, so it is as tall as the tallest drawn level;
    - within a level, cards follow a three-pass barycentre order of the drawn arrows, ties in record
      order, never a state or a time;
    - a card's place changes when a wait changes or, while folded, when a CR merges or is cancelled;
      the rule that each CR keeps one place for its whole life no longer holds;
    - on a live batch the merged and cancelled CRs are folded behind the "N merged" toggle chip
      (`.gbar`), unfolded back into today's levels, with no fold on a closed record;
    - on a level narrower than 240px the state badge shows its icon only (`graph-level`
      container, `chip.css`);
    - no new colour, size or token.
- **Demo** (`docs/demo/projects/shop-api/changes/4-batch/`):
  - CR-148's `after` becomes `["CR-141", "CR-142", "CR-143", "CR-145", "CR-146"]`, in `batch.json`
    and in `1-pending/148-localised-receipts/depends.json` alike;
  - CR-142 and CR-143 are implied (CR-148 → CR-145 → CR-143 → CR-142), and CR-141 is merged.
- What the demo then shows:
  - folded: four levels, `CR-142 CR-146 CR-144 CR-149` (the up pass sorts level 0 by its arrows' targets:
    CR-142 and CR-146 point at the first card of a later level), then `CR-143 CR-147`, `CR-145`, `CR-148`,
    with five arrows, two of them into CR-148 (from CR-145 and CR-146);
  - unfolded: CR-141 is back in level 0 with its arrow to CR-148 (three arrows into CR-148);
  - CR-148's count reads 5.
- **`docs/web-board.md`**, the Batch graph paragraph:
  - the sentence "Each CR stays in one place for its whole life, merged ones included." becomes:
    "A CR keeps its place while the batch's waits do not change; it moves when a wait changes, or
    when a CR merges or is cancelled while the merged CRs are folded. The merged and cancelled CRs
    are folded behind a chip, "N merged", above the graph; click it to show them in their
    levels.";
  - after the arrow sentences, add: "Only the waits that no chain of arrows already implies are
    drawn: hover a CR to light every CR it waits for, and its wait count lists them all.".
- **Screenshots** (`scripts/docs_screenshots.py`, unchanged):
  - `docs/web-board/batch-graph-pc.png` is retaken with `just docs-screenshots` and committed. The
    script takes it at 1400 × 860, where the demo's four levels still scroll sideways inside the
    box (about 690px of column for about 810px of levels); the 1600 × 900 fit is proved by the
    one-off run (Evidence), not by this picture;
  - no new committed picture: the phone picture is PR evidence only;
  - the other pictures the demo change alters (batch, Kanban, panel) are not retaken here: CR-447
    retakes them (its table names this CR's row).

## Overlaps

batch-30, this CR before CR-447.

- **CR-447 docs-gardening** waits for this CR. It owns the final pass on `docs/web-board.md` and the
  batch pictures. This CR writes its own sentences and commits `batch-graph-pc.png` only. Its row is
  in CR-447's table of the batch's CRs ("What they edit themselves"): `docs/web-board.md` "Batch",
  `batch-graph-pc.png`, `docs/demo/` (CR-148's waits), with the retake of the other pictures left
  to CR-447.
- **CR-439 board-help-page** and **CR-449 board-griller** (active, web client): they share
  `en.js` / `fr.js` and DESIGN.md as text only, with no shared behaviour. Whichever lands later
  rebases its lines.
- **CR-441** (merged): its one head per waiting CR and its top layer stay. This CR feeds `drawEdges`
  fewer pairs and keeps `light`, `lightEdges` and the heads whole.
- **CR-435** (merged): `batch-head.js`'s legend reads `batch.arrow`, and only that word changes.
- The other batch-30 CRs touch neither the graph nor the Batch page.

## Out of scope

- The Gantt's arrows (still every declared wait), the Kanban, the Time cards, the PR column and its
  width, the figures and the title row.
- Routing arrows around cards, drawing the implied waits on hover, and a pinned light.
- Keeping the fold across reloads.
- Any server, protocol, record or CLI change. The CR board pane (`hooks/`) is untouched, so its
  screenshot rule does not apply.

## Evidence

Every check reads the shipped files from the repository at the head under test. No prepared text
stands in for a shipped file.

**Test** (`skills/chantier/scripts/cli/tests/test_board_graph_arrows.py`, one new test beside
CR-441's; `just test` within its limit). It reads the shipped files:

- `js/model/semantics.js` exports `reducedEdges` and `orderLevels`;
- `js/views/batch-graph.js`:
  - `drawEdges` calls `reducedEdges(` and not `edges(`;
  - `graphBlock` calls `orderLevels(` and builds `data-fold` with `aria-expanded`;
- `js/views/batch-gantt.js` still calls `edges(` (the Gantt is unchanged);
- `css/views/batch-graph.css`:
  - `.batch .lvl` declares `flex: 1 1 0`, `min-width` and `max-width`, and a `graph-level`
    container;
  - `.batch .graph` declares no `max-content`;
- `css/components/chip.css` holds `@container graph-level` hiding `.sbw`;
- `en.js` and `fr.js` both hold the five new keys, and `batch.arrow` names the implied waits.

`test_sheets`, `test_components` and `test_token_table` pass unchanged: tokens only, and the chip
rule lives in the chip's sheet.

**Pictures and measures** (in the PR's Deliverables, each captioned with the head's
seven-character SHA). They are taken on the demo by a one-off Playwright run that is not shipped
(the committed `batch-graph-pc.png` comes from `just docs-screenshots` at 1400 × 860 and is not the
fit's proof):

- Desktop 1600 × 900, the shop-api batch's Graph tab:
  - before (the base) and after;
  - after, three pictures: folded and unlit; folded with CR-148 hovered; unfolded.
- Phone 375 × 812, the Graph tab after, folded.
- Measured after, and stated in the PR:
  - folded, the reduction:
    - no `.node[data-id="CR-141"]`;
    - the chip reads "1 merged", with `aria-expanded="false"`;
    - exactly 2 `svg.edges:not(.top) path[data-from][data-to="CR-148"]` (from CR-145 and CR-146);
    - 5 arrows in all;
  - folded, the fit:
    - `.gscroll`'s `scrollWidth ≤ clientWidth` at 1600 × 900;
    - its `scrollHeight ≤ clientHeight + 1`;
    - both SVG layers no taller than `.graph`'s tallest `.lvl` bottom plus its padding;
  - unfolded:
    - CR-141 drawn, 3 arrows into CR-148, `aria-expanded="true"`;
    - after folding again, `.gscroll`'s height is within 1px of the first folded measure (no
      growth carried over);
  - with CR-148 hovered: CR-142, CR-143, CR-145 and CR-146 carry `highlight`, and the top layer
    holds the 2 lit arrows and 1 head;
  - CR-148's wait count reads 5, and its `title` names the five CRs;
  - a keyboard Tab to the chip, then Enter, unfolds;
  - phone: `document.documentElement.scrollWidth ≤ innerWidth`, while the graph box may scroll.
- A closed record (`?p=mobile-app&v=batch&b=batch-01&t=graph`): no chip, every CR drawn, the page
  as before.
- The order's determinism: two loads of the same state give the same `data-id` order in each `.lvl`
  (measured in the same run).

**Gates.** `just check`, `just eval-dry-run` (a change under the CLI's `src/`), and the pipeline's
`just scenario (ubuntu-latest)` green at the PR's head. If this CR is the top of the stack, it also
owes the local `chantier gate` at its head before the user merges. No scenario step is added: the
scenario drives no browser.

**Rounds.**

- Round 1: sections 1 to 6 and the test.
- Round 2: DESIGN.md, the demo, the docs, the pictures and the measures.
- Round 3: the review's fixes.

## Decisions (Chief of Staff, 2026-11-22, option A; the user may change any)

Each one is stated with its options. A is the one built.

1. **Keeping the fold.**
   - A: folded at every page load; a click unfolds until the next load.
   - B: kept on this device, like the last tab (`pref`).
2. **Cancelled CRs.**
   - A: folded with the merged ones; the chip names both ("12 merged · 1 cancelled").
   - B: only the merged ones fold, and a cancelled CR stays in its level.
3. **The badge on a narrow level.**
   - A: below 240px the state badge shows its icon only (its word in the `title`), so four levels
     fit at 1600px.
   - B: keep the word always, and accept sideways scroll for four levels below about a 1900px
     window.
4. **The desktop target.**
   - A: four levels with the PR column at 1600 × 900. At 1440 × 900, four levels still scroll
     inside the box (about 730px for about 810px of levels).
   - B: aim at 1440, which takes cards near 150px wide and drops the folder chip from the node (a
     DESIGN.md rule, so a change of its own).
5. **Showing the hidden waits.**
   - A: hover lights every declared wait's card, and the wait count's `title` names them.
   - B: also draw a CR's implied waits on hover, in the top layer (a new line style).
6. **The Gantt.**
   - A: it keeps every declared wait.
   - B: it draws the same reduction (a follow-up CR).
