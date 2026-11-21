# Web board: an Inbox page of what needs the user

Spec v2 (2026-11-21), after the spec critic's nine findings (user-inbox-Q17 to Q20 and five fixes
that need no user). Short name: `inbox`. A new view of the web client, and one read-only field on
each project line of the server's `board` topic; no write, no CLI command, no card, no agent change.

## Goal

The user (2026-11-21): "Dans la UI donc j'aimerais une inbox juste après le home. [...] Le but
c'est que je serais tjs sur cette page et elle va me notifier de ce qui arrive, si un agent a une
question, si un PR est à revoir ou prête à merger. Il faudra des action facile snooze, rappeler
plus tard, discard, ou un act." Then (ui-night act): "act" opens links only; snooze, later and
discard are kept by the board; the board edits no batch and messages no agent.

The board gets an **Inbox** view, second in the navigation, right after Home: one list of what needs
the user (a CR's question, an approval asked on a PR, a PR ready to merge, a blocked CR), each entry
one card with **Open**, **Snooze** (1 hour), **Later** (next 08:00) and **Discard** (while its fact
lasts). It is not the planning inbox (`1-inbox`). The page notifies by a count beside its navigation
entry, the count in the browser tab's title, a "new" mark, and, on the user's yes on that device, a
browser notification while a board page is open. It shows on a project and on "All projects".

Every path below is under `skills/chantier/scripts/cli/src/chantier/` unless it starts with
`docs/`, `scripts/` or `tests/` (`tests/` is `skills/chantier/scripts/cli/tests/`); the web
client's paths start with `clients/web/`. Read `clients/web/DESIGN.md` first and keep it true
(AGENTS.md).

## Decisions carried from 02-answers.md

| Answer | Carried as |
| --- | --- |
| ui-night | the CR joins batch-30; a working UI is the goal |
| ui-night scope | this CR is the "user's Inbox" item of the six web-board items |
| ui-night act | Open is a link or the side panel only; hides kept on the device (sections 3, 4); no write anywhere (section 7) |
| user-inbox-Q1 | view `inbox`, second in the registry, sidebar and bottom bar; word "Inbox" / "Boîte de réception"; lead line "What needs you" and a sub-line saying it is not `1-inbox`; Home stays the opening page; the address `?v=inbox` keeps it (sections 2, 4) |
| user-inbox-Q2 | four kinds, `question`, `approval`, `merge`, `blocked`, built from the published record only; nothing from `asks_unread`, pipeline or merge waits, events or journal lines (section 1) |
| user-inbox-Q3 | `merge` is the record's `to_review`; no forge read added (section 1) |
| user-inbox-Q4 | an entry exists only while its fact does: it is rebuilt from each push; the page clears nothing (sections 1, 3) |
| user-inbox-Q5 | one Open per entry: PR or MR in a new tab (the CR's folder when no web address); question and blocked open the CR's folder in the side panel; a question names the seat's session title; no answer, merge or approve control; Open does not hide (section 4) |
| user-inbox-Q6 | Snooze 1 h, Later until the next 08:00 local, Discard while the fact lasts; a new occurrence is a new entry (sections 1, 3) |
| user-inbox-Q7 | marks kept in the browser's storage through `core/store.js`; the server stores nothing; marks of gone entries dropped (section 3) |
| user-inbox-Q8 | a folded "Hidden (n)" under the list, each with until when and Restore (section 4) |
| user-inbox-Q9 | navigation count, "(n)" in the tab's title, a "new" mark, and an off-by-default "Notify me on this device" button shown only where the browser offers notifications; no sound (sections 2, 5) |
| user-inbox-Q10 | one list, newest first, each entry the one card with its kind chip, CR and one-line title, the question or reason, age, actions; a kind filter with the board's filter chips; "Nothing needs you" when empty (section 4) |
| user-inbox-Q11 | on "All projects": every project's entries in one list, each naming its project; Open leads into that project; the count is the sum (sections 2, 4) |
| user-inbox-Q12 | read-only towards server, planning folder, batch and agents; no AGENTS.md clause; DESIGN.md kept true; `docs/web-board.md` gets the page's section and its two pictures; no CR board pane change (sections 6, 7) |
| user-inbox-Q13 | the other pages are unchanged; the only way in is the navigation entry (section 2) |
| user-inbox-Q14 | no behaviour overlap; the field "All projects" needs is added to the published state, read-only, on top of CR-429; Inbox second, the other new views after it (section 1, "Batch-30 neighbours") |
| user-inbox-Q15 | tests on a prepared state for the four kinds and an entry leaving, the design checks; the PR's screenshots and written check (Evidence); the hides' tests narrowed by Q19 |
| user-inbox-Q16 | the out-of-scope list (below) |
| user-inbox-Q17 | the `approval` kind reads "Approval asked" / "Approbation demandée"; the `merge` kind keeps "Ready to merge" / "Prête à fusionner"; a CR both ready to merge and with an open approval wait shows both cards, each hidden on its own (sections 1, 6) |
| user-inbox-Q18 | the batch in `4-batch/`, running or paused, feeds the Inbox, as Home reads it (section 1) |
| user-inbox-Q19 | no Node run in the tests; `tests/test_board_inbox_marks.py` is not written; the hides and their return are proved by the PR's written check; the design test checks statically that `js/model/inbox.js` is pure (no DOM, no store, no `localStorage`) (Evidence, open question 2) |
| user-inbox-Q20 | the `merge` key's time is `times.state_at`, else `handed_back_at`, never `updated` (with neither, no time); `blocked` the same, `times.state_at`, never `updated`; the entry's age follows the same rule (section 1) |

## What changes

### 1. The server: one read-only field per project line (Q2, Q3, Q4, Q6, Q11, Q14, Q17, Q18, Q20)

Today the `board` topic's project lines (`board/state.py:project_line`) carry `to_review` and
`blocked` as `{cr, title, pr}` only, and no wait; "All projects" cannot build the entries from them.
The project page could build them from `project.state`, but two builders would drift. So the server
builds the entries once, from the facts it already reads, and every page reads them from the `board`
topic, which the page always subscribes to (`clients/web/js/core/refresh.js`). No new source: the
batch rows (`board/crs.py:_row`), the backlog items (`board/backlog.py:backlog_items`, their
`open_waits`) and the seat (`board/state.py:_seat`) of the same `project_state`.

- **New `board/needs.py`**, `needs_you(state: dict[str, Any]) -> list[dict[str, Any]]`, pure (no
  read), from the dict `_project_state` returns. Kinds, in the words of `KINDS = ("question",
  "approval", "merge", "blocked")`:
  - `question`: each open wait of type `answer` of a batch row (`row["open_waits"]`, already empty
    for a merged or cancelled CR) and of a backlog item of any stage (`item["open_waits"]`). `text` is
    the wait's `ref` (the question, as `wait add answer --ref` recorded it), `note` its `note`,
    `since` its `since`, `session` the seat's title (`state["seat"]["title"]`, else `None`).
  - `approval`: each open wait of type `approval`, from the same two places; `pr` is the wait's
    `link` (else the row's `pr`), `text` the wait's `note` (else `None`), `since` its `since`.
  - `merge`: each batch row with `to_review` true, `pr` its `pr`, `since` its `times["state_at"]`,
    else its `handed_back_at`, **never its `updated`** (Q20: `updated` moves on any touch of the
    record, a heartbeat or a cost write, and would show a discarded entry again); with neither,
    `since` is `None`. `merge_place` its 1-based place in `batch["merge_order"]` and `merge_total`
    the length of that list.
  - `blocked`: each batch row with `state == "blocked"`, `text` its `blocked` (the reason), `since`
    its `times["state_at"]`, **never its `updated`** (Q20); with none, `None`.
  - A CR both ready to merge and with an open `approval` wait gives two entries, one of each kind,
    with their own keys (Q17): no rule of which card wins.
  - Every entry: `key`, `kind`, `cr` (the CR id, or `None` for a backlog item), `item` (the backlog
    slug, or `None`), `title` (the row's or item's), `folder`, `pr` (`None` but for `approval` and
    `merge`), `text`, `note`, `since`, `session`, `merge_place`, `merge_total` (absent keys are
    `None`). `since` is the one time both the key and the entry's age use (Q20).
  - `key` names one occurrence of a fact: `question:<owner>:<wait id>:<since>`,
    `approval:<owner>:<wait id>:<since>`, `merge:<cr>:<since>`, `blocked:<cr>:<since>`, where `owner`
    is the CR id or `i:<slug>`, and `<since>` is empty when `since` is `None` (`merge:CR-12:`). A
    wait cleared then added again has a new id; a CR ready again (after rework, or a PR back to draft
    then ready with no new hand-back) has a new `state_at`; a CR blocked again has a new `state_at`:
    each is a new key, so a discarded entry's next occurrence shows again (Q6); a touch of the record
    that moves only `updated` keeps the key, so a discard holds while the fact lasts.
  - Order: `since` newest first, an entry with no `since` last, then by `key` (stable).
  - Nothing else makes an entry: no `asks_unread`, no pipeline or merge wait, no event, no journal
    line (Q2). The batch is the one in `4-batch/`, **running or paused** (Q18: the end of a batch's
    last CR pauses the batch when its PRs wait for the user's merge), as Home reads it.
- **`board/state.py:project_line`**: one more key, `"needs_you": needs_you(state)`. `_entry` and the
  other keys are unchanged. The `board` topic's hash (`board/api/topics.py`, over
  `data["projects"]`) already covers it, so a change of an entry pushes the topic.
- **`docs/server-api.md`**, the `board.get` row: add that each line of `projects` carries
  `needs_you`, the list of what needs the user (kinds and fields as above), built from the record
  and the planning folder, read-only. An added field stays protocol 1 (the page's "Versions").

### 2. The view, the navigation and the frame (Q1, Q9, Q11, Q13)

- **`clients/web/js/views/registry.js`**: import `* as inbox from './inbox.js'` and `inboxCount`
  from `../inbox/count.js`; add right after `home`:
  `{ id: 'inbox', icon: 'inbox', word: 'nav.inbox', module: inbox, overview: inbox, count: inboxCount, countAll: inboxCount, badge: true }`.
  `countOf(view, state)` returns `view.countAll(state)` on "All projects" when the entry has
  `countAll`, else what it returns today. Extend the head comment with `countAll` (the count on
  "All projects") and `badge` (the count also shows in the phone's bottom bar).
- **`clients/web/js/inbox/count.js`**: `inboxCount(state)`: the number of entries not hidden now
  (section 3) for the scope shown (the project's line, or the sum over every line on "All
  projects"); `null` when it is 0 or the `board` topic has not arrived, so the sidebar shows no
  number then.
- **`clients/web/js/ui/bottombar.js`**: a view with `badge` and a count draws
  `<span class="n">${n}</span>` after its word. **`clients/web/css/shell.css`** (a frame sheet):
  `.bnav .n` with tokens only (`--text-badge`, `--accent`, `--white`, `--radius-pill`, a `space`
  padding). If the bar no longer fits 360 px with the Inbox (and Help), `.bnav` gets
  `overflow-x: auto`, as CR-439's open question 4 says; whichever CR lands second keeps one rule.
- **`clients/web/js/ui/icons.js`**: one outline `inbox` (a tray), `currentColor`, like the others,
  e.g. `<path d="M3 13h5l1.5 3h5L16 13h5"/><path d="M5 5h14l2 8v6a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-6z"/>`.
- **`clients/web/js/ui/header.js`**: `title(state)` shows the surface's name only on "All projects"
  **Home**; every other view shows its own word (CR-439 makes the same edit: the second to land
  finds it done).
- **`clients/web/js/main.js`**: `drawFrame` sets `document.title` to `(${n}) chantier board` when
  `inboxCount(state)` is above zero, else `chantier board` (the `<title>` of `index.html`); after
  `subscribe(draw)`, `watchInbox()` (section 5) starts.
- **`clients/web/js/i18n/en.js`, `fr.js`**: `'nav.inbox': 'Inbox'` / `'nav.inbox': 'Boîte de réception'`
  beside the other `nav.*`; import `inbox` from `./en-inbox.js` / `./fr-inbox.js` and spread it.
- **`clients/web/index.html`**: `<link rel="stylesheet" href="css/views/inbox.css" />` after the
  other view sheets.
- No other page changes (Q13): Home's tiles and PR block, the cards' `waits:` line and the PRs page
  stay as they are, with no link to the Inbox. Home stays the page the board opens on; the router
  needs no change (`?v=inbox` is a known view, kept on "All projects" by its `overview`).

### 3. The device's marks (Q6, Q7)

- **`clients/web/js/model/inbox.js`**, pure: no DOM (`document`, `window`), no store
  (`core/store.js`), no `localStorage`, no words, no import but `../core/format.js` if needed (the
  design test checks it, Evidence):
  - `HOUR_MS = 3600000`, `LATER_HOUR = 8`, `KINDS = ['question', 'approval', 'merge', 'blocked']`.
  - `idOf(project, entry)` = `${project}|${entry.key}`.
  - `hideUntil(how, nowMs)`: `snooze` → `nowMs + HOUR_MS`; `later` → the next 08:00:00 in the
    device's local time strictly after `nowMs` (today's when it is before 08:00, else tomorrow's,
    built with `Date`'s `setHours(LATER_HOUR, 0, 0, 0)`); `discard` → `null`.
  - `isHidden(mark, nowMs)`: true for a `discard` mark, or a mark whose `until` is after `nowMs`.
  - `entriesOf(board, project)`: the shown scope's entries, each `{ ...entry, project, id }`: the
    line of `project`, or every line on `'*'` (each entry naming its project), newest first by
    `since`, else by `first[id]` (the device's first sight), else last.
  - `split(entries, marks, nowMs)` → `{ shown, hidden }`.
  - `prune(marks, liveIds, nowMs)`: the marks of ids still live and still hiding (an ended snooze or
    later mark goes; a discard mark goes when its entry is gone).
- **`clients/web/js/inbox/marks.js`**: the device's state, read and written only through
  `core/store.js`'s `pref` / `setPref` (the store stays the only writer of `localStorage`), as JSON
  under `chantier.inbox.marks` (`{ id: { how, until } }`), `chantier.inbox.first`
  (`{ id: ms }`, when the device first saw an entry), `chantier.inbox.shown` (`{ id: true }`, the
  ids the Inbox page has drawn, section 5) and `chantier.inbox.notify` (`'1'` when on):
  `loadMarks()`, `hide(id, how)`, `restore(id)`, `remember(liveIds)` (records first sights, then
  prunes marks, first sights and shown ids of gone ids; it runs only once the `board` topic has
  arrived, so a first empty state prunes nothing), `markShown(ids)`.
  - Only `hide` and `restore`, the user's own clicks, call `update({ inboxMarks })`, so every page
    redraws.
  - `remember` and `markShown` write storage only, **never `update()`**: they run inside a store
    listener (`watch.js`) or a view's `after()`, and an `update()` there would redraw the page,
    whose `after()` writes again, a loop. Each writes only when its set changes (`markShown` only
    when the set grows, `remember` only when a first sight is added or an id pruned).
- **`clients/web/js/core/store.js`**: `inboxMarks: {}, // Inbox: the device's hides, { id: { how, until } }`,
  `inboxKinds: ['question', 'approval', 'merge', 'blocked'], // Inbox: the kinds the filter shows (session only)`,
  `inboxTick: 0, // Inbox: a hide ended (device milliseconds), to redraw` and
  `inboxNotifyBlocked: false, // Inbox: this browser refused or failed a notification`. Not in the
  router's `reset`: the filter and the marks hold across projects.
- The server stores nothing; an entry hidden on the phone still shows on the desktop (Q7).

### 4. The page (Q1, Q5, Q8, Q10, Q11, Q17)

**`clients/web/js/views/inbox.js`**, `render(state)` / `mount(root)` / `after(root, state)` like the
other views; at most 300 lines, functions at most 50, complexity at most 10 (split into
`js/inbox/entry.js` for one entry's card if needed):

- `render`: `<div class="inbox">`, then
  - the lead: `<p class="inbox-lead">` with `inbox.lead` ("What needs you") and under it
    `inbox.sub` ("Questions, approvals, PRs to merge and blocked CRs that wait for you. Not the
    planning inbox: the requests to grill are in Triage.");
  - the notify control (section 5);
  - the kind filter: a `<div class="lfil" role="group">` with `inbox.filter` and one toggle per kind,
    the board's filter chip (DESIGN.md: filled when on, outlined grey when off): a
    `<button type="button" class="tag st <state>[ off]" aria-pressed data-ik="<kind>" data-key="ik-<kind>">`
    with the state's icon (`stateIcon`) and the kind's word; state per kind: `question` → `waits`,
    `approval` → `working`, `merge` → `ready`, `blocked` → `blocked`. A kind with no entry still has
    its toggle. Toggling writes `inboxKinds` (session only, like the Kanban's `priorityFilter`);
  - the list: the `shown` entries of the kinds on, one card each; with none, `empty(t('inbox.none'))`
    ("Nothing needs you");
  - the hidden: when there are hidden entries, `<details class="inbox-hidden"><summary>` with
    `inbox.hidden` ("Hidden ({n})"), then one compact card each (`variants: ['compact', 'dim']`) with
    the until words and a Restore button.
- **`clients/web/css/components/chip.css`**: one rule `.tag.st.off`, placed after the `.tag.st.<state>`
  rules, with the same declarations as `.tag.off` (`--edge: var(--line)`, `background: var(--panel)`,
  `color: var(--ink2)`) and a one-line comment. Reason: the state rules (`.tag.st.waits` and the
  others, three classes, later in the file) outrank `.tag.off` (two classes), so without it an off
  kind toggle stays filled with its state's tint. Tokens only; no new token.
- **An entry's card**: `card({ classes: 'inbox-entry', heading: 'div', top, title, body, meta, end,
  variants: [hidden && 'compact', hidden && 'dim'], attrs })`:
  - `top`: the kind chip (`tag('st <state>', html\`${stateIcon(state)}${word}\`)`, the kind's word
    through `tf(forge, 'inbox.kind.<kind>')`), on "All projects" the project's `mark(project)` and
    id, and the "new" mark (`tag('badge', t('inbox.new'))`) while it is new (section 5);
  - `title`: `<cr or slug> · <title>` (one line, cut, full text in `title`, by the card);
  - `body`: the question's whole words (`text`, escaped, never `raw`) for `question`; the reason for
    `blocked`; the approval's note for `approval` when it has one; nothing for `merge`;
  - `meta`: the age (`t('time.ago', { age: age(since, state.now) })`, nothing with no `since`); for
    `question` `inbox.session` ("Answer in: {title}") or `inbox.no_session` ("No session holds the
    seat"); for `merge` `inbox.merge_place` ("{n} of {total} in the merge order"); for a hidden one
    its until words (`inbox.until` "until {time}" with `hhmm`, `inbox.until_morning` "until
    tomorrow 08:00" or "until 08:00", `inbox.while` "while it lasts");
  - `end`: the actions, plain buttons, no menu, no date picker: **Open**, then **Snooze**,
    **Later**, **Discard** (`data-inbox="snooze|later|discard" data-inbox-id="<id>"`); a hidden
    entry has Open and **Restore** (`data-inbox="restore"`).
  - `attrs` is built by the `html` tag (`` html`data-key="inbox-${id}"` ``), never a string literal.
- A CR with both an `approval` and a `merge` entry shows two cards (Q17), each with its own actions.
- **Open** (Q5), one per entry, never a hide:
  - `approval`, `merge`: an `<a href target="_blank" rel="noopener">` to `safeUrl(pr)` with
    `tf(forge, 'pr.open')` / `mr.open` words (as `views/home-prs.js`); with no web address, on a
    project the CR's folder in the side panel (`opener(key)`), on "All projects" as below.
  - `question`, `blocked`, on a project: `opener(crKey)` (`c:<cr>`) or `opener(itemKey)` (`i:<slug>`),
    bound by `bindOpen(root)`: the side panel opens the CR's folder, as a click on any card does.
  - on "All projects", a folder Open is a button `data-project="<project>"`: the frame's existing
    handler moves to that project and the view stays the Inbox (it has `overview`), where the same
    entry's Open opens the panel.
  - No answer field, no merge or approve button, no link into a session (the board has none).
- `mount(root)`: `bindOpen(root)`; `delegate` click on `[data-inbox]` → `hide(id, how)` or
  `restore(id)`; on `[data-ik]` → toggle the kind in `inboxKinds`; on `[data-inbox-notify]`
  (section 5). Returns the cleanup.
- `after(root, state)`: `markShown(ids drawn)` (section 5); no `update()`.

**`clients/web/css/views/inbox.css`** (a page sheet: layout only, tokens only): `.inbox` a column
with a `space` gap and a reading `max-width`; `.inbox-lead`, `.inbox-hidden summary` margins and
sizes with `space` and `type` tokens; the actions row's gap. Nothing restyles the card or the chip.

### 5. Notifications (Q9)

- **The count**: the sidebar's number (section 2), the bottom bar's badge, and "(n)" at the head of
  the tab's title, on every page, for the scope shown; nothing at 0.
- **"New"**: an entry is new on this device until the Inbox page has shown it. `after()` passes the
  ids it drew to `markShown` (`chantier.inbox.shown`, pruned with the rest; written only when the set
  grows, never through `update()`, section 3); the view keeps, while it stays mounted, the set of ids
  that were new when it drew them, so their mark stays until the user leaves the page and is gone at
  the next visit.
- **`clients/web/js/inbox/watch.js`**, `watchInbox()`, started once by `main.js`: subscribes to the
  store; on each `board` change, takes every project's entries (all lines, whatever the page shows),
  calls `remember(liveIds)`, and, for an id it did not know at the previous change (none at the first
  change: what exists at load raises nothing) and not hidden, raises one browser notification when
  `chantier.inbox.notify` is `'1'` and `Notification.permission === 'granted'`:
  `new Notification(t('inbox.notify_title', { kind, project }), { body: '<cr> · <title>', tag: id })`,
  whose `click` listener (`addEventListener`, no `on...` attribute) focuses the window and moves to
  that project's Inbox. It also runs a 30 s timer that, when a hide has ended since the last look,
  writes `inboxTick` so the entry comes back by itself without a server event.
- **The guarded call.** The constructor can throw (Android Chrome throws `TypeError` on
  `new Notification` outside a service worker), and `core/store.js`'s `update()` calls its listeners
  with no `catch`, so a throw there would stop the other listeners' draw. So the whole notification
  step of `watch.js` runs in `try { ... } catch { ... }`: on a failure it writes `'0'` to
  `chantier.inbox.notify`, raises nothing more, and, out of the listener's turn (`setTimeout(..., 0)`,
  never a nested `update()` inside the listener), calls `update({ inboxNotifyBlocked: true })`. The
  page then shows the grey line `inbox.notify_denied` in place of the button, as for a denied
  permission. `Notification.requestPermission()` on the button's click is guarded the same way (a
  throw or a rejected promise reads as denied).
- **The button** "Notify me on this device" (`inbox.notify_on`), in the page under the lead, only
  when `'Notification' in window && window.isSecureContext` and `inboxNotifyBlocked` is false (a
  plain-HTTP address of the local network is not secure, so it shows nothing there; the board's
  default `127.0.0.1` is). A click asks `Notification.requestPermission()`; granted, it writes `'1'`
  and shows `inbox.notify_off_button` ("Stop notifications on this device"), which writes `'0'`.
  Permission denied, or a failure (above): `inboxNotifyBlocked` is set and one grey line
  `inbox.notify_denied` ("This browser blocks notifications for the board") shows; the button is off.
  Nothing is sent with no page open: no service worker, no push.
- No sound.

### 6. Words, DESIGN.md and the docs (Q1, Q12, Q17)

- **`clients/web/js/i18n/en-inbox.js`, `fr-inbox.js`** (merged into `en.js` / `fr.js`, head comment
  like `en-batch.js`): `inbox.lead`, `inbox.sub`, `inbox.filter`, `inbox.kind.question`
  (Question / Question), `inbox.kind.approval` (Approval asked / Approbation demandée, Q17),
  `inbox.kind.merge` (Ready to merge / Prête à fusionner), `inbox.kind.blocked` (Blocked / Bloquée),
  `inbox.none`, `inbox.new`, `inbox.open`, `inbox.snooze` (Snooze / Reporter 1 h), `inbox.later`
  (Later / Plus tard), `inbox.discard` (Discard / Écarter), `inbox.restore`, `inbox.hidden`,
  `inbox.until`, `inbox.until_morning`, `inbox.while`, `inbox.session`, `inbox.no_session`,
  `inbox.merge_place`, `inbox.notify_on`, `inbox.notify_off_button`, `inbox.notify_denied`,
  `inbox.notify_title`. "PR to review" is not an Inbox word: the board keeps it for the `to_review`
  CRs (Home, the PRs page). An Inbox word that says "PR" (`inbox.sub`) gets its MR variant in
  `en-mr.js` / `fr-mr.js`. Every key in both languages; chantier's own names (CR, PR, batch) stay as
  the board writes them.
- **`clients/web/DESIGN.md`**: a section after "Waits on a card" (and before or after CR-439's
  "The Help page", whichever is there), `## The Inbox page`: the `inbox` view, second after Home,
  on a project and on "All projects"; its entries are the `board` topic's `needs_you`, never built
  in the page; one card per entry (`inbox-entry`), the kind chip a state tag (`waits`, `working`,
  `ready`, `blocked`), the filter the board's filter chip, off by `.tag.st.off`; Open is a link or the
  side panel, never a write; the hides live in the browser (`chantier.inbox.*`, through
  `core/store.js`), no server write, and the "seen" and first-sight writes never redraw; the count
  shows in the sidebar, the bottom bar (`badge`) and the tab's title, nothing at 0; no sound, a
  browser notification only on the user's yes and only with a page open, its call guarded. The
  token table does not change. Where DESIGN.md describes the filter chip, add that a state chip
  toggle turns off with `.tag.st.off`.
- **`docs/web-board.md`**: a section `### Inbox` after "Home: a project": what makes an entry, the
  four actions, the hidden list, where the marks live (this browser only), the count, the tab title
  and the notification button (and why it does not show on a plain-HTTP network address), with the
  picture `web-board/inbox-pc.png`; `inbox-phone.png` joins the phone pictures named under "On a
  phone".
- **`scripts/docs_screenshots.py`**, `views()`: after the project Home,
  `goto(page, url, "inbox", "shop-api")` and `shot(page, "inbox", size)`. **`docs/demo/`**: the demo
  needs a question and an approval to show four kinds: add to `projects/shop-api/changes/4-batch/batch.json`
  one open `approval` wait on **CR-144** (it has a PR, `pull/16`, which is the wait's `link`:
  `wait add approval` refuses a CR with no PR and no `--ref`, so the demo holds only what the CLI
  could have written) and one open `answer` wait on **CR-145** (the `waits.make` shape, each `since`
  before the fixed clock 2026-06-18 10:30 UTC); CR-146 (blocked) and the ready CRs give the other two
  kinds. `just docs-screenshots` writes `docs/web-board/inbox-pc.png` and `inbox-phone.png`.

### 7. What does not change

AGENTS.md: no clause (the page reads the `board` topic it already reads; its only writes are the
browser's own storage; no test runs Node, Q19). No op, no topic, no protocol number change. No forge
read. No batch edit, no journal line, no message to an agent, no wait cleared, nothing marked read in
the record. No CR board pane change (`hooks/register.tsx`, `STATUS.json`), so no pane screenshot is
owed. `chantier live` is not touched (the new field is ignored by it).

## Out of scope (Q16)

Answering a question, approving, merging or unblocking from the board; a sound; e-mail or phone
push; a notification with no page open (no service worker); a hidden list shared between devices
(a server-kept list is a later change on the user's word); a link into a session; entries for
issues, pipelines, merge waits, CI turning red, or the Foreman's asks; any change to `chantier
live`; any change to Home, the cards' `waits:` line or the PRs page; a test that runs the web
client under Node, and the AGENTS.md sentence it would need (Q19: a recommendation for an inbox item
of its own).

## Batch-30 neighbours (Q14)

No `depends.json`. Shared files, found by text; the stack settles each:

- **CR-439 `board-help-page`**: `js/views/registry.js` (the Inbox entry goes right after `home`,
  Help right after it), `js/i18n/en.js` / `fr.js` (`nav.*`, one import and spread each),
  `js/ui/icons.js` (one icon each), `index.html` (one sheet each), `js/ui/header.js` (the same
  `title` edit), `js/main.js` (Help edits `configure` and `closeInnermost`; the Inbox `drawFrame`'s
  title and `watchInbox()`), `css/shell.css` (`.bnav` overflow, one rule), `DESIGN.md` (a section
  each, at the end). CR-439's test accepts Help right after `inbox` when that entry exists.
- **CR-429 `board-fingerprint-cache`**: changes how the server learns of changes and caches topic
  values (`board/api/topics.py`, `docs/server-api.md`), not what it publishes; `needs_you` is built
  inside `project_line`, so its cache carries it. Built on top of it (Q14): `docs/server-api.md`'s
  `board.get` row, edited by both.
- **CR-427 `board-running-batch-lane`**: `board/state.py` (it reads the batch rows already there;
  the Inbox adds one key in `project_line`), `docs/server-api.md`, `docs/web-board.md`.
- **CR-433, CR-434, CR-435** (the Batch page): `docs/web-board.md`, `docs/demo/` (CR-434),
  `js/core/store.js` (one field each), `css/shell.css`, `js/main.js` (`drawFrame`, CR-435),
  `scripts/docs_screenshots.py` (CR-435), `DESIGN.md`'s "One card, one column, one chip" rule (the
  Inbox leaves it alone). CR-433's check that `css/components/chip.css` holds no rule for its
  `.tag.pri-*` classes is untouched by the one `.tag.st.off` rule.
- **Coming specs** (`board-batch-view`, `board-triage-polish`, `board-history`, `board-griller`,
  `dashboard-pages`): a new view goes after the Inbox in `registry.js`, in its own CR's order;
  `docs/web-board.md`, `DESIGN.md`, `en.js` / `fr.js`, `icons.js`, `index.html` as above.

## Evidence (Q15, Q19)

**Checks in `just check`**, each reading the shipped files at the head under test:

- **New `tests/test_board_needs.py`** (in-process, on a prepared state like `test_board_waits.py`,
  with `forge_world`'s `World`, `crs_of`, `write_batch`, then `project_state` and `project_line`):
  - one batch with a CR holding an open `answer` wait, one an open `approval` wait, one ready to merge
    (`to_review`), one blocked with a reason, plus a backlog item's `waits.json` with an open
    `answer` wait and a seat: `needs_you` holds the five entries with their `kind`, `key`, `text`,
    `pr`, `since`, `session` and `merge_place`, newest first; a `pipeline` and a `merge` wait, a
    cleared wait, a merged CR's wait and `asks_unread` make none;
  - a CR both `to_review` and with an open `approval` wait gives two entries, kinds `approval` and
    `merge` (Q17);
  - the same batch paused (`status` paused) gives the same entries (Q18);
  - the `merge` and `blocked` keys and `since` come from `times.state_at` (else, for `merge`,
    `handed_back_at`); a change of the row's `updated` alone keeps both keys; a row with neither time
    gives `merge:<cr>:` and `since` `None` (Q20);
  - an entry leaves when its fact ends: the wait cleared, the CR merged, the CR no longer blocked;
    the same CR blocked again with a later `state_at` gives a new `key`;
  - parametrized where it keeps the file short.
- **New test in `tests/test_board_design.py`**, `test_the_inbox_is_the_second_view_and_reads_only`,
  on the shipped files:
  - in `js/views/registry.js` the second entry is `id: 'inbox'` with `overview`, `count` and
    `countAll`;
  - `js/views/inbox.js`, `js/inbox/*.js` and `js/model/inbox.js` import neither
    `core/transport.js`, `core/api.js` nor `api/`, and only `core/store.js` names `localStorage`;
  - `js/model/inbox.js` is pure (Q19): it names none of `document`, `window`, `localStorage`,
    `Notification`, and imports nothing but `../core/format.js` (no `core/store.js`, no `i18n/`);
  - `inbox.js` builds its cards with `card.js` and passes `attrs` only as an `html` template;
  - `css/components/chip.css` holds a `.tag.st.off` rule after its last `.tag.st.<state>` rule.
- No `tests/test_board_inbox_marks.py` and no test that starts Node (Q19).
- Existing checks: `test_the_web_frame_has_small_scripts_and_both_word_files_share_their_keys`
  (covers `en-inbox.js` / `fr-inbox.js`), `test_the_web_frame_is_self_contained_and_follows_the_style_rules`
  (no other origin, no `on...` attribute), `test_board_design.py`'s tokens, components and one card
  checks, `test_a_card_title_is_one_line_with_its_full_text_on_hover`; Biome (`just lint`).

**Before the push** (AGENTS.md): `just check` and `just eval-dry-run` in the worktree at the rebased
head (a change under the CLI's `src/`); the pipeline's `just scenario (ubuntu-latest)` green at
the PR's head before the PR.

**By hand, in the PR's Deliverables** (DESIGN.md: screenshots are the visual record), from
`chantier board` at the PR's head:

1. The Inbox on a project, desktop, English, with entries of the four kinds, one "new", the count
   in the sidebar and "(n)" in the tab.
2. The same, empty: "Nothing needs you".
3. "All projects" with the Inbox: entries of two projects, each naming its project, the summed count.
4. The phone (375 px): the list, the bottom bar's badge, the "Hidden (n)" line open.
5. French, one entry hidden by Later with its until words.

**The written check** (Q19: it is the hides' only proof, so each line states what was done and seen;
times are the device's local clock, which the check names with its time zone):

- Snooze hides an entry until now + 1 hour (the until words say so) and the entry comes back by
  itself after the hour, with the tab left open (the check notes the two times).
- Later before 08:00 hides until 08:00 the same day; after 08:00 until 08:00 the next day (the
  until words; the check states the local time of the click, one of the two cases at least, and
  names the other as not exercised if it was not).
- Discard hides while the fact lasts: the entry stays hidden across a push that touches the record
  without changing the fact (a heartbeat, a cost write), and a new occurrence (the wait cleared then
  added again) shows again.
- Restore brings a hidden entry back to the list; a hide on one browser does not hide on another.
- A kind toggled off in the filter shows outlined grey (`.tag.st.off`) and its entries go.
- Open on a PR opens the forge in a new tab; Open on a question opens the CR's folder in the panel;
  on "All projects" Open leads to the project's Inbox.
- Clearing a wait (`wait <cr> clear <id>` in a test batch) removes its entry within a push.
- With "Notify me on this device" on, a new wait raises one notification while the tab is in the
  background; on a plain-HTTP network address the button does not show.
- The guarded call: on Android Chrome, a click on the button (or a new entry with it on) shows the
  `inbox.notify_denied` line and no error; with no such phone at hand, the PR's Known gaps names
  it ("the guarded notification call not exercised on Android Chrome").
- The page does not redraw in a loop: the browser's console shows no repeated draw while the Inbox
  stays open (the "seen" write calls no `update()`).

## Open questions (built as A; the user asks none tonight)

1. **Where entries are built.** A (built): on the server, one read-only `needs_you` per project line
   of the `board` topic, so the project page and "All projects" read one list and the four kinds are
   tested in Python on a prepared state. B: in the page from `project.state`, with the server adding
   only each project's raw open waits to its line for "All projects" (two builders in two
   languages).
2. **How the hides are tested.** Decided (user-inbox-Q19): B, no JS run in the tests; the hides and
   their return are proved by the PR's written check, and the design test checks statically that
   `js/model/inbox.js` is pure. Left to the user, not built here: an inbox item of its own to allow
   one Node-run test of the web client's pure modules, with one sentence in AGENTS.md's test bullet,
   if the hides regress.
3. **"Ready to merge" in a newest-first list.** A (built): the list stays newest first (Q10); a
   `merge` entry shows its place, "n of m in the merge order" (Q2). B: the `merge` entries are
   grouped in merge order at the top of the list.
4. **The count at zero.** A (built): no number beside the entry and no "(0)" in the tab. B: "0"
   beside the entry.
5. **Which notifications.** A (built): a new entry of any project of the surface raises one, whatever
   the page shows, the user's one inbox. B: only the scope shown (the project, or all on "All
   projects").
6. **Open of a folder on "All projects".** A (built): it moves to that project's Inbox, where Open
   opens the panel. B: it moves to the project and opens the CR's folder at once, once the
   project's data arrives.
7. **A backlog question whose CR then enters the batch.** A (built): its key changes (`i:<slug>` to
   the CR id), so a discarded question shows again once; rare and harmless. B: key a wait by its
   folder's slug in both places.
