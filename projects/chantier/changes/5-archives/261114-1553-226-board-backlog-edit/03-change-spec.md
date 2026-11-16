# Change Specification: the board edits the backlog

## Goal

The user's words (2026-11-13): "pas d'edition du batch pour l'instant dans le board, juste de la
visu. edition = uniquement le backlog". The board's Triage view lets the user handle the backlog
as post-its, as in the prototype:

- drag a post-it between the inbox, P1 to P4 and `3-ready` (changing a priority *is* moving the
  folder);
- group post-its;
- put labels on them and filter by label;
- file a new idea with "New";
- edit a CR's Markdown;
- mark "the next batch is ready".

Each change is written at once through the CLI's role-free code, with a toast. A journal lists
what the board wrote since the user last said "rescan" to the Chief of Staff. The board never
messages the Chief of Staff and never touches a batch.

The rule of the split (`visualization-backend/02-answers.md`, "Split into CRs") is "the same thing
at the end": the prototype is the reference. This specification names the views and screenshots
this CR reproduces. The PR shows each one beside the prototype's, on PC and on the phone.

This is CR 4 of 5 of the split. It comes after `visualization-backend` (board-server: the server,
its read API, the token URL, live refresh) and `board-read-views` (the views' frame, the file
panel, Home, Kanban, the phone layout): `depends.json`.

## The references

The folder of `visualization-backend` moves with its CR. Find it by its slug: today it is
`.agents/changes/2-backlog/P2/visualization-backend/`, and later possibly under `5-archives/`.

- **The prototype:** `prototype/index.html`. Serve it as `prototype/README.md` says, then open
  `?v=triage` (Triage) and `?v=home` (Home). The Triage code is `index.html` lines 741-910: the
  constants `TCOLS` and `GRILL`, `gstate`, `labels`/`lfilter`/`labelOf`, `toast`, `move`,
  `groupOf`, `ungroup`, `moveGroup`, `postit`, `triage`, `selbar`, `dlist` and `bindTriage`. The
  New button is `newItem`, lines 1074 and 1103. The Triage CSS is lines 259-325, and its phone
  rules are under `@media (max-width:760px)` (line 353).
- **The screenshots** (`evidence/prototype/`) that this CR reproduces:

| Screenshot | What this CR reproduces from it |
| --- | --- |
| `v6-19-source-icon-triage.png` | Triage on PC: Inbox column, the "Backlog" column of P1 to P4 rows (an empty row is a thin strip), the `3-ready` column, the post-its tinted by grill state, the column headers with counts by state |
| `v6-24-triage-labels-phone.jpg` | Triage on the phone: the indicator, the journal button, the label filter row, one column per swipe, labels on the post-its, the bottom tab bar, "+ New" beside the project picker |
| `v6-23-home-written-by-board.png` | The Home tile "Written by the board" (count, "since your last 'rescan' to the CoS") |
| `v6-22-kanban-labels-pc.jpg` | The header's "+ New" button, and the Kanban Intake column's "+ New: a new idea" button (the Kanban itself is `board-read-views`') |
| `v6-16-all-projects-home-only-pc.jpg`, `v6-17-all-projects-home-only-phone.jpg` | On "All projects", "+ New" and Triage are hidden |

  Three states have no `v6` screenshot. For each, the reference is the prototype itself, taken at
  the same sizes during the PR's comparison:
  - **The selection bar**, with its "→ Inbox … → 3-ready", "Group", "Label…", "Open" and "✕"
    buttons. Its earlier look is in `v3-02-selection-and-drafts.jpg`. In that shot the drafts and
    "Inject" are gone, and the journal replaces them.
  - **A group frame**, with its handle, count and "undo".
  - **The journal panel**, and the `3-ready` column's foot in its three states: in preparation,
    declared ready, and changed since.
- **The rules:** `visualization-backend/02-answers.md`, in particular:
  - "Prototype 3" (post-its, grill states, moving, groups, "when is a batch ready?", automatable);
  - "Triage layout" and "Prototype 4" (the rows; a group lives where its post-its are);
  - "Scope answers" 1 and 2;
  - "Board to Chief of Staff: later";
  - "Editing is the backlog only";
  - "The "+ Intake" button becomes "New"";
  - "Labels and groups";
  - "The prototype as cleaned";
  - "Technology".
- **The measured targets** of `python-inline-deps/03-change-spec.md` ("Targets", "The package
  layout") apply to every Python file this CR adds or changes.

## Decisions carried from `02-answers.md`

| Decision | Where this spec carries it |
| --- | --- |
| The board writes: it edits files and moves folders; a priority change is a folder move (Scope answers 1) | "Writes", "Triage view" |
| Editing the Markdown in the board: yes (Scope answers 2) | "The Markdown editor" |
| Editing is the backlog only: inbox, `2-backlog/P1…P4`, `3-ready`; no `order` of any kind; "Inject into the running batch" removed; "the next batch is ready" stays a marker | "Writes" (the refusals), "The next-batch marker", "Out of scope" |
| "+ Intake" becomes "New": only a new idea in the inbox, through `file`; issue intake is automatic, elsewhere | "New" |
| Every backlog change written at once through the CLI's role-free commands, with a toast "Written: …"; nothing queued for the Chief of Staff | "Writes", "Toasts" |
| The journal: the Triage button "N writes since your last 'rescan'", its panel with "I said 'rescan' to the CoS", the Home tile "Written by the board"; the board never messages the Chief of Staff | "The journal" |
| The user says "I updated the priorities, rescan" to the Chief of Staff (Board to Chief of Staff: later) | "Cards and concepts" |
| Post-its tinted by grill state: raw, in grill, specified, automatable (in `3-ready` with no specification, a state of its own); counts by state in a column header; "N specified, M automatable" in `3-ready`; a move to `3-ready` says "(specified)" or "(automatable, no specification: your call)" | "Triage view" |
| Inbox on the left, P1 to P4 as rows in a central "Backlog" column (up is more urgent, an empty row a thin strip), `3-ready` on the right; on a phone the three swiped side by side | "Triage view" |
| Moving: drag to a column, or select with a click (several possible) and send from a bottom bar (the phone's way) | "Triage view", "Moving" |
| Groups: a drop on another post-it or "Group" on a selection makes a named group; a drop on a group joins it; a group moves whole by its handle and can be undone; it lives where its post-its are; an empty one disappears | "Groups" |
| Labels: on the post-its, a filter row at the top of Triage, "Label…" on a selection; labels and groups kept in the CRs' JSON, so on every device | "Labels", "What this CR needs from `cr-summaries`" |
| A batch is ready when the user says so: a marker with its time and the `3-ready` CRs; "Next batch ready: you said so at HH:MM, N CRs", "In preparation", "In preparation: 3-ready changed since your 'ready'"; a CR without a specification is only noted | "The next-batch marker" |
| The Ready column's text: the running batch's state, "the next batch opens after its close" | "The next-batch marker" |
| The overview hides the project views and the New button | "Triage view", "New" |
| The prototype is cleaned to the first version: no "To the CoS", no drafts, no "refresh summary" button | "Out of scope" |
| Hand-written HTML, CSS and JS, native ES modules with no compiler, one module per view; very clean, standard, modular code | "Code layout" |
| The final QA compares the whole result with the prototype, view by view, on PC and on the phone | "Evidence", "Final QA" |

## What changes

### 1. Writes: one backlog service in the CLI, called by the commands and by the server

The board is the CLI's own process. The answers say every write goes through the CLI's role-free
commands. So the server calls the **same functions** that `chantier file` and `chantier triage`
run, in process. It does not spawn a subprocess, and no second code path writes the planning
folder. Each function:

- takes a `Repo` (the server holds one per project; the commands build theirs with `Repo.find()`);
- takes `changes_lock`;
- refuses with the same `ChantierError` and message as the command;
- rewrites the dashboard as the command does;
- returns the command's output lines.

A new layer-2 module, `lifecycle/backlog.py` (in the layout of `python-inline-deps`; today's code
is `commands.file_cr`, `commands.triage` and `lifecycle.move_backlog_item`), holds:

| Function | Used by | What it does |
| --- | --- | --- |
| `file_idea(repo, text, slug=None)` | `commands/intake.py` `file_cr`; the server's "New" | today's body of `file_cr` once the text is read (title from the first non-empty line, slug, `_new_request`, dashboard) |
| `move_item(repo, item, to)` with `to` one of `inbox`, `P1`…`P4`, `3-ready` | `triage`; the server's moves | `move_backlog_item`, plus the way back to the inbox (below) |
| `edit_markdown(repo, item, relpath, text, base_sha256)` | the server only | see "The Markdown editor" |
| `declare_next_batch(repo)` and `next_batch(repo)` | the server only | see "The next-batch marker" |

`commands/intake.py`'s handlers keep their arguments, output, exit codes and help. They only parse
and call these functions.

**Back to the inbox: `chantier triage <item> --inbox`.** Today `triage` cannot move an item back to
`1-inbox` (`move_backlog_item` accepts `--priority P<n>` or `--ready`), and the prototype's Inbox is
a drop target. The fix is one option on the existing command, not a new command.

- `--priority`, `--ready` and `--inbox` are exclusive: exactly one is given. The usage message
  becomes "triage takes --priority P<n>, --ready or --inbox, one of them".
- An item already in `1-inbox` is refused with "<name> is already in 1-inbox" (precondition).
- A name already taken in `1-inbox` is refused with "1-inbox already holds <name>: nothing moved",
  as for the other targets.
- The output is "triaged 1-inbox/<name>".
- `--help` names the option.

**The server's write routes.** These go under the per-project API prefix that `visualization-backend`
defines (in-project mode has one project). They are guarded by the same token or random URL part
as the reads.

- Every write is a `POST` (or `PUT` for a file) with a JSON body (`Content-Type:
  application/json`, refused otherwise).
- The `Origin` header, when present, must be the server's own origin. This, with the token, keeps
  another site from writing through the user's browser.
- The CSP keeps `form-action 'none'`.

| Route (relative) | Body | Calls |
| --- | --- | --- |
| `POST backlog/new` | `{text, slug?}` | `file_idea` |
| `POST backlog/move` | `{items: [slug…] \| group: name, to}` | `move_item` per item, in order; for a single post-it leaving its group's column, its group is cleared (see "Groups") |
| `POST backlog/labels` | `{items, add}` | `cr-summaries`' label setter, per item |
| `POST backlog/group` | `{items, name}` | `cr-summaries`' group setter, per item (and moves to the first item's column first, as `groupOf`) |
| `POST backlog/ungroup` | `{name}` | clears the group of every member |
| `PUT backlog/file` | `{item, path, text, base_sha256}` | `edit_markdown` |
| `POST backlog/next-batch` | `{}` | `declare_next_batch` (the server reads `3-ready` itself and never trusts a list from the page) |
| `GET journal` | | the entries since the last rescan |
| `POST journal/rescan` | `{}` | records the user's "rescan" |

- An item is named by its slug. The server finds its folder among `1-inbox/`, `2-backlog/P1…P4/`
  and `3-ready/` only. A slug found nowhere there is refused with "<slug> is not in the backlog
  (inbox, P1…P4, 3-ready)". So a CR in `4-batch/`, `5-archives/` or `6-trash/` can never be
  written from the board.
- Several items: each is written in turn, and the answer lists each item's result. One refusal
  does not undo the writes before it, and stops none after it.
- The answer is `{"ok": true, "lines": [...], "journal": [entries added]}`, or `{"ok": false,
  "error": "<the CLI's message>"}`. The status is 400 for `EXIT_USAGE` and 409 for
  `EXIT_PRECONDITION` and `EXIT_CONFLICT` (exit codes in `state.py`, `core/errors.py` after the
  refactor). It is 403 for a bad token or origin, 415 for a body that is not JSON, and 500 for
  anything else.
- On "All projects" (the overview) no write route exists: an intake needs a project.

After a write the page reloads its data through the read API, so what it shows is always the
folder, never a local guess. A second device sees the change at its next live refresh
(`visualization-backend`). The writes are not optimistic: the post-it dims while its write runs.
On a refusal it stays where the folder is.

**Commit and push.** The board does not commit. With `surface-autosync` merged and the group
active, the surface's autosync commits and pushes the board's writes. Without an autosync,
today's rule stays: the Chief of Staff commits the planning folder by hand, at the rescan.

### 2. The journal

- A local file per planning folder, `board-journal.jsonl`, at the planning folder's root (in a
  surface, each project's `changes/`). It is ignored like `seat.json`: it is added to
  `state.IGNORED` (`core/files.py` after the refactor), so `ensure_gitignore` writes it. It is
  never pushed. The server is the only writer, and it appends one line per write, by atomic
  append under `changes_lock`.
- A line is `{"t": "<ISO time>", "kind": "new|move|label|group|ungroup|edit|next-batch",
  "items": [slugs], "text": "<the toast's words>"}`. "I said 'rescan'" appends `{"t": …, "kind":
  "rescan"}`. "Since the last rescan" means the lines after the last `rescan` line.
- On Triage (above the columns, as in `v6-24`): the button "✎ **N** write(s) since your last
  'rescan'", tinted when N > 0. A click opens the journal panel (prototype `dlist`):
  - its heading, "Written by the board in the folder";
  - each entry with its time (HH:MM) and text, or "nothing";
  - the buttons "I said 'rescan' to the CoS" (disabled when N = 0) and "Close";
  - the note "Each change is already written (the CLI's file and triage commands). The board does
    not talk to the Chief of Staff: tell it 'rescan' in the chat so it reads again."
  
  The prototype's "Reset all (prototype)" button does not exist in the real board.
- On Home (`v6-23`): the tile "Written by the board", with the count and "since your last 'rescan'
  to the CoS", or "nothing since your last 'rescan'" (the calm style) when N = 0. A click goes to
  Triage. `board-read-views` lays out Home. This CR adds that tile, or fills it if the frame left
  a place for it.
- A post-it named in an entry since the last rescan carries the "modified" mark (prototype
  `.pi.chg`).

### 3. The Triage view

A view module of the frame, first after Home in the menu and the phone's bottom bar, as in the
prototype. It is hidden on "All projects" (`v6-16`, `v6-17`).

- **Bar above the columns:**
  - the next-batch indicator;
  - the journal button;
  - the label filter row ("Labels" then one button per label; "show all" when a filter is on);
  - the legend of the four grill states.
- **Columns:**
  - Inbox on the left;
  - a central "Backlog" column, headed "↑ more urgent · drag a post-it up or down", holding the
    rows P1, P2, P3 and P4 (in a row, the post-its wrap; an empty row is a thin strip that says
    "empty: drop a post-it here");
  - `3-ready` on the right, keyed by the record's own value `3-ready`, never `ready`.

  Each header has its colour dot, the name, the count, and the counts by grill state with their
  icons.
- **A post-it** (prototype `postit`):
  - its grill-state icon;
  - the slug in monospace;
  - the late-summary clock and the origin badge, when `cr-summaries` gives them;
  - the title (three lines at most);
  - its labels;
  - a foot with the state's word, the file count and the "open" button. The button opens the CR's
    folder in the panel of `board-read-views`.

  Its shape is the prototype's: the radius `4px 4px 4px 14px`, the state tints, the tilt on hover
  that the user kept.
- **Grill states:**
  - specified: `03-change-spec.md` is present (green ✓);
  - automatable: in `3-ready` with no specification (violet ⚡);
  - in grill: `02-answers.md` is present, with no specification (amber half circle);
  - raw: anything else (grey dashed circle).
  
  The state comes from the read API (`visualization-backend`). If that API already exposes
  `specifying` (`status.spec_state`), it shows as "in grill" (open point 6).
- **`3-ready`'s foot:**
  - "N specified, M automatable ⚡: the Driver starts from the request" when the column is not
    empty;
  - the button "The next batch is ready";
  - one line on the running batch: "batch-N is <state>: the next batch opens after its close. The
    board does not touch the batch.", or "No batch running: the next batch can open."
- **Phone:** the three columns are swiped side by side (scroll snap, 86% each), with the rows
  stacked in the middle one (prototype CSS line 366). "+ New" sits beside the project picker
  (`v6-24`).

### 4. Moving

- **PC, drag and drop** (HTML5 drag events, prototype `bindTriage`):
  - a post-it dropped on a column or a row moves there (`backlog/move`);
  - dropped on another post-it, it makes a group or joins one (see "Groups");
  - a group dragged by its handle moves whole;
  - the drop target is highlighted.
- **Selection, on every device:**
  - a click or tap on a post-it (not on its "open" button) toggles its selection;
  - the bottom bar (prototype `selbar`) shows "N selected", "→ Inbox", "→ P1" … "→ P4", "→
    3-ready", then "Group" (two or more), "Label…", "Open" (one) and "✕";
  - Escape clears the selection.
  
  This is the phone's way, since touch browsers fire no HTML5 drag. Post-its are focusable, and
  Space or Enter toggles the selection, so the keyboard can do everything the mouse can.
- A drop or a send to the item's own column writes nothing. There is no rank inside a row.
- **The toast for a move** is the prototype's wording, in the page's language:
  - "Written: <slug>: priority P3 → P2";
  - "<slug> → inbox";
  - "<slug> → 3-ready (specified)";
  - "<slug> → 3-ready (automatable, no specification: your call)".

### 5. Groups

A group is a name in each member CR's JSON (`cr-summaries`' group field). A group is the set of
post-its of one project that carry the same name, and it is drawn in the column where they are.

- **Create:** a drop on a post-it that has no group, or "Group" on a selection. A dialog asks the
  name, with "group N" by default. Every member moves first to the target post-it's column (for a
  selection, the first one's), then gets the name. The toast: "group 'name': a, b (in P2)".
- **Join:** a drop on a grouped post-it or on a group's frame. The post-it moves to that column if
  needed, then gets the name.
- **Move whole:** by the handle `⠿ name · N`, to a column or a row: each member moves.
- **Undo:** the "undo" button clears the name from every member. The post-its stay where they are.
- **Leaving:** a single post-it moved alone to another column leaves its group (its name is
  cleared in the same write), as in the prototype's `move`. So a group's post-its are always in
  one column, and a group whose last post-it leaves disappears. Nothing is stored for a group
  itself.
- **Frame:** a dashed rounded frame (prototype `.grpf`), its members inside, before the loose
  post-its of the column. In a row, the members wrap.

### 6. Labels

Labels live in each CR's JSON (`cr-summaries`' labels field), so every device sees the same.

- "Label…" on a selection opens a dialog: one word, lower case, an existing label or a new one
  (the existing ones are offered). It adds that label to each selected CR that lacks it. The
  toast: "label 'docs' on a, b".
- A label's colour is fixed by its place in the sorted list of the project's labels, from the
  prototype's six (`LCOL`).
- **The filter:** a label button toggles it. Several labels show the post-its that carry any of
  them, and "show all" clears the filter. The filter is the page's state for the session; it is
  not written anywhere. Hidden post-its do not count in the headers.
- If `board-read-views` or `cr-summaries` has already built the label tags and the filter for the
  Kanban, Triage reuses those modules and does not copy them.

### 7. New

- Two buttons call it:
  - "+ New" in the page's header (`v6-22`; on the phone beside the picker, `v6-24`), hidden on
    "All projects";
  - "+ New: a new idea" at the head of the Kanban's Intake column (`v6-22`), which
    `board-read-views` draws and this CR wires.
- It opens a dialog: a native `<dialog>` with a text area "Your new idea", "File" and "Cancel".
  It never uses `window.prompt`.
- "File" sends `backlog/new` with the text as typed. `file` makes the title from the first line
  and the slug from the title, and nothing more is asked: no tracker and no issue URL.
- The toast: "Written: new idea in 1-inbox/<slug>".
- On "CR folder already exists", the dialog stays open, shows the CLI's message, and shows a slug
  field to file again with `slug`.

### 8. The Markdown editor

There is no prototype of the editor (open point 2). It lives in the file panel of
`board-read-views`, and only for a backlog item's file.

- A Markdown file (`.md`) of an item in the inbox, P1 to P4 or `3-ready` shows an "Edit" button
  above its rendered text. `STATUS.md` does not, and no other file does.
- "Edit" puts in place of the rendered text:
  - a monospace text area holding the file's exact text;
  - "Save" and "Cancel" (and Ctrl+S or Cmd+S to save);
  - on the phone, the panel full screen.
  
  Leaving with unsaved changes asks for confirmation.
- "Save" sends `PUT backlog/file` with the SHA-256 of the text as it was loaded. The read API
  returns that hash with a file's content; this CR adds it if the API lacks it. `edit_markdown`:
  - finds the item in the backlog, and checks `relpath` relative, with no `..`, ending in `.md`,
    not `STATUS.md`, an existing file inside the item's folder (`board._inside` confines today);
  - refuses with "<item>/<path> changed since you opened it: reload it" (conflict) when the file's
    hash differs from `base_sha256`;
  - writes the text in UTF-8 with no byte-order mark, by atomic rename (`write_file`), keeping
    the file's line endings (CRLF stays CRLF);
  - refuses a text over 1 MB, today's cap of the board's file view.
  
  No file is created, renamed or deleted from the board.
- The toast: "Written: <slug>/<path> edited". The panel shows the new rendering.
- An edit changes the CR's Markdown, so its summary becomes late (`cr-summaries`' checksum) and
  the clock appears. That is expected. The board writes no summary.

### 9. The next-batch marker

- "The next batch is ready" (in `3-ready`'s foot) calls `declare_next_batch`. It writes
  `next-batch.json` at the planning folder's root: `{"declared_at": "<ISO time>", "crs":
  ["<slug>", …]}`, the slugs then in `3-ready`, sorted. It is plain JSON and committed with the
  planning folder (by the autosync, or by the Chief of Staff), so the Chief of Staff on any
  machine reads it.
- The button is disabled when `3-ready` is empty or the marker already matches it.
- The indicator, computed by the page from the marker and the current `3-ready`:
  - **declared:** "● Next batch ready: you said so at HH:MM, N CRs" (green), when the marker's
    list equals `3-ready`'s;
  - **changed:** "● In preparation: 3-ready changed since your 'ready'" (amber), when it differs
    and at least one of its CRs is still in `3-ready`;
  - **in preparation:** "● In preparation: N CRs in 3-ready" (amber), with no marker, or once none
    of its CRs is in `3-ready` any more (a batch took them). Nothing deletes the file then; it is
    simply stale.
- A CR with no specification is only noted ("automatable"), never refused. Nothing computed
  decides readiness: the marker is the user's word.
- The toast: "Written: next batch ready to go with: a, b".

### 10. Toasts

One module (`ui/toast.js`), shared with the other views:

- dark, centred above the bottom bar, as `.toast` in the prototype;
- a success says "Written: …" and goes after 2.6 s;
- a refusal shows the CLI's message on a red tint and stays until it is closed or another toast
  replaces it;
- `role="status"` for success and `role="alert"` for a refusal.

### 11. Code layout

This CR follows the user's rule ("hyper propre, beaux standards, modularité"), the layering of
`python-inline-deps`, and the module conventions that `board-read-views` set for the frame. The
static folder is the one `visualization-backend` chose: below, `static/` stands for it.

**JavaScript:** native ES modules, no build. Each module has one responsibility, stated in a head
comment, and exports named functions only. Rendering and wiring are separate: a render function
returns DOM or markup from data, and a `bind` function attaches handlers. Every piece of text from
the record goes through the frame's escaping. No inline script or handler is used (the CSP is
`script-src 'self'`).

| Module | Holds |
| --- | --- |
| `static/views/triage.js` | the view: fetches, lays out the bar and columns, calls the modules below |
| `static/triage/model.js` | pure functions: columns, grill state, groups derived from the items, counts, the indicator's state; no DOM |
| `static/triage/postit.js` | one post-it's markup |
| `static/triage/drag.js` | HTML5 drag and drop: post-it, group handle, column, group frame |
| `static/triage/selection.js` | the selection and the bottom bar |
| `static/triage/groups.js` | create, join, move, undo; through `api/backlog.js` |
| `static/triage/ready.js` | the indicator and `3-ready`'s foot |
| `static/labels/filter.js`, `static/labels/tags.js` | the filter row, the tags and their colours (shared with the Kanban) |
| `static/journal/journal.js` | the button, the panel, the Home tile's data |
| `static/edit/new-idea.js` | the New dialog |
| `static/edit/markdown-editor.js` | the editor in the file panel |
| `static/api/backlog.js` | one function per write route; returns the result or throws a `BoardWriteError` carrying the CLI's message |
| `static/ui/toast.js`, `static/ui/dialog.js` | the toast; a `<dialog>` helper (text, choices, focus kept and returned) |

**CSS:** `static/css/triage.css`, `journal.css`, `editor.css`, `dialog.css`, on the frame's tokens
(colours, radii, the 12px floor, focus ring). The state tints, the grill colours and the
`.chg`, `.sel` and `.drag` marks are the prototype's values. The Impeccable rules of
`02-answers.md` ("Visual rules", "Impeccable pass") hold: AA contrast, no text under 12px (badges
11px), an edge or a shadow but not both, drawn SVG icons and not glyphs. The exceptions are the
grill icons ✓ and ⚡ and the handle ⠿, kept as the prototype shows them.

**JS and CSS checks:** this CR meets the JS and CSS targets and their linter that the earlier board
CRs add to `just check` (`python-inline-deps`, "Out of scope"). If none exists when the Driver
starts, see open point 9.

**Python:** the targets of `python-inline-deps` apply to every new or changed file:

| Module | Holds |
| --- | --- |
| `lifecycle/backlog.py` | the backlog functions of section 1 |
| `board/journal.py` | read, append, rescan |
| `board/write_api.py` | the write routes, the origin and content-type checks, the error-to-status mapping, the journal line |

### 12. Cards and concepts

- `skills/chantier/references/chief-of-staff.md`, in the table of the user's words (after the row
  "board on my phone"), one row:
  - the user's words: "rescan", "I updated the priorities";
  - what the Chief of Staff does: read the backlog again (`$CHANTIER status`, the dashboard,
    `next-batch.json`). With no autosync, it commits the planning folder's changes by hand. It
    tells the user what moved, and whether the next batch is declared ready.
  
  No other card changes, and no agent file changes.
- `skills/chantier/references/concepts.md`:
  - in "Lifecycle": an item goes back from `2-backlog/` or `3-ready/` to `1-inbox/` with `triage
    --inbox`;
  - in "`3-ready`": the user may mark the next batch ready from the board (`next-batch.json`, the
    user's word with its time and list); the mark decides nothing.
- `docs/boards.md`, the remote board's section: what the board writes (the backlog only), the
  journal and "rescan", in a few lines. The full page is `board-docs-screenshots`'.

### What this CR needs from `cr-summaries`

Labels and groups are fields of each CR's condensed JSON, and that JSON is `cr-summaries`'. This CR
calls `cr-summaries`' functions that set a CR's labels and group, under the same lock, and reads
both fields, the origin and the late flag through the read API. It does not define their storage.
`depends.json` lists only `visualization-backend` and `board-read-views` (see open point 1). If the
Driver starts before `cr-summaries`' CLI part is merged, it stops and says so (no fallback, no
labels kept elsewhere).

## Out of scope

- Any batch edit: `order` of any kind (add, slots, budget, rounds), "Inject into batch-N", or a
  move of a CR in `4-batch/`.
- The queue to the Chief of Staff, asks, the chat, "To the CoS", drafts, and the "refresh summary"
  button: the second step.
- Fetching a GitHub, GitLab or Jira issue (automatic, elsewhere), and any field in New beyond the
  text.
- Abandon and restore from the board (open point 3), rank inside a priority row, removing a label
  or renaming a group (open point 4), and creating, renaming or deleting files in a CR folder.
- Writing summaries, origins or checksums (`cr-summaries`).
- The read views, the panel, Home's layout, Kanban, Batch, Costs and the picker
  (`board-read-views`); the server, token and live refresh (`visualization-backend`); the autosync
  pill (`surface-autosync`); the docs' screenshots (`board-docs-screenshots`).
- `hooks/`, `types/` and `STATUS.json`: the pane draws nothing new, so `AGENTS.md`'s pane
  screenshot rule is not triggered and no `just mod` is needed.
- A version bump.

## Evidence

The Verifier keeps each item in `work/verifier/evidence/`, and the PR body quotes them.

- **E1. `just check`** passes on Windows here, then in CI on Linux, macOS and Windows, with the
  Python targets and the JS and CSS checks clean. Structure tests stay few: at most one test is
  added, and only if the JS checks do not already cover it. That test would check that every
  module under `static/` is reachable from the entry module and that none uses an inline handler.
- **E2. `just scenario`** passes on both forges (the CLI changes). New steps:
  - **The `triage --inbox` command:**
    - an item moves P2 → inbox;
    - `--inbox` on an inbox item is refused;
    - two target options are refused, with the usage message.
  - **In the board section** (today "16c. The remote board", reworked by
    `visualization-backend`), on a board started on the scenario's world:
    - `POST backlog/move` inbox → P2 → `3-ready` → inbox, each followed by the folder on disk
      and the journal's lines;
    - `backlog/new` makes `1-inbox/<slug>/intake/request.md` byte-equal to the text, and a second
      one with the same title gets 409 and the CLI's "already exists" message;
    - `PUT backlog/file` with the right hash writes the file, keeping CRLF;
    - the same request again with the old hash gets 409, and the file is unchanged;
    - `STATUS.md`, a path with `..`, a non-`.md` file, a slug of a `4-batch` CR and a `5-archives`
      folder are each refused, with nothing written;
    - `backlog/next-batch` writes `next-batch.json` with the sorted `3-ready` slugs;
    - `journal/rescan` empties `GET journal`;
    - a write with no token, a foreign `Origin`, or a `text/plain` body is refused, with nothing
      written;
    - `git check-ignore` holds `board-journal.jsonl`;
    - with `cr-summaries` merged: `backlog/labels` and `backlog/group`, then a single move out of
      the group clears that item's group.
- **E3. Side by side with the prototype**, PC (1400x860) and phone (375x812). The PR's
  Deliverables show each real view beside the prototype's at the same size, captioned with the
  head's seven-character SHA:
  - Triage (`v6-19` PC, `v6-24` phone);
  - the Home tile (`v6-23`);
  - the "+ New" buttons (`v6-22`);
  - "All projects" with no Triage and no New (`v6-16`, `v6-17`);
  - and, against the prototype taken live: the selection bar on the phone, a group, the journal
    panel, and `3-ready`'s foot in its three states.
  
  The real board runs on a copy of this repository's planning folder (never the folder itself),
  with the prototype on its own snapshot. The data differ, so the comparison is of layout, style
  and words, and each difference is named and explained in the PR. The editor and the New dialog
  are shown alone (no prototype).
- **E4. Drag and drop** on PC in Chromium and in Firefox: a post-it to a row, a post-it on a
  post-it (a group), a group by its handle. Playwright's `drag_to` is used where it fires the
  events. Otherwise the Driver records a short screen capture by hand, or the PR's Known gaps
  names "drag and drop not verified by automation" (02-answers already noted that automation
  could not fire it).
- **E5. Two devices:** a move made on the phone shows on the PC at its next refresh. The journal
  is the same on both. "I said 'rescan'" on one empties it on the other.
- **E6. No console error** on PC or phone across every action of E3.
- **E7. Commit:** with `surface-autosync` merged and an active group on a scratch surface, a board
  write is committed and pushed by the group. Without an autosync, `git status` shows the change
  uncommitted and nothing else.

## Final QA

`02-answers.md`, "Split into CRs": after the five CRs, the Chief of Staff orders one final QA that
compares the whole board with the prototype, view by view, on PC (1400x860) and phone (375x812).
This CR's share of it:

- Triage in every state of E3;
- the journal button, panel and Home tile;
- New from the header and from the Kanban;
- the editor;
- the next-batch indicator.

Each is taken from the merged `main` beside the prototype's `?v=triage` and `?v=home`. The QA
lists every difference, and each one is fixed or accepted by the user.

## Open points (defaults taken; the Chief of Staff takes them to the user)

1. **`cr-summaries` before this CR.** Labels and groups are written through `cr-summaries`'
   commands, and `depends.json` does not list it. Default: the Chief of Staff adds
   `"cr-summaries"` to this CR's `depends.json` (this specification changes no other file). The
   alternative is to ship this CR without labels and groups, which breaks "the same thing at the
   end".
2. **The Markdown editor has no prototype.** Default: an "Edit" button in the file panel, a plain
   text area, Save and Cancel, a hash check against a concurrent change, `.md` only, never
   `STATUS.md`, no file created or deleted.
3. **Abandon from the board.** The answers list "abandon" among the role-free commands, but the
   cleaned prototype has no button for it, and the prototype is "exactly what is delivered".
   Default: no abandon or restore in this CR.
4. **Removing a label, renaming a group.** They are not in the prototype. Default: not in this CR.
   A label is removed by an agent through `cr-summaries`' command.
5. **The way back to the inbox.** Default: a `--inbox` option on `triage`, since the prototype's
   Inbox is a drop target and the bottom bar has "→ Inbox". The alternative is to drop the Inbox as
   a target.
6. **`specifying`.** The prototype has four grill states. Default: an item whose specification is
   being written (`work/specifying`) shows as "in grill".
7. **The journal's place.** Default: a local, ignored `board-journal.jsonl` per planning folder,
   written by the server only, where "rescan" is a line and not a deletion. The alternative is the
   server's memory, which a restart would empty.
8. **The marker's place and life.** Default: `next-batch.json` at the planning folder's root,
   committed, never deleted by the board, and read stale once its CRs left `3-ready`. `open` does
   not change. The Chief of Staff reads it at "rescan" (the one card row of section 12).
9. **JS and CSS checks.** Default: those that `visualization-backend` or `board-read-views`
   ship. If neither ships one, this CR adds none, and the PR's Known gaps says so. The other
   option is that this CR adds the linter itself.
10. **The page's language.** The prototype is in French and the repository's text in English.
    Default: the language `board-read-views` ships, with this specification's English words as
    the translation of the prototype's ("Écrit : …" is "Written: …", and "J'ai dit « rescan » au
    CoS" is "I said 'rescan' to the CoS").
11. **The card row for "rescan".** Default: one row in `chief-of-staff.md` (section 12), so that
    the user's "rescan" and the marker mean something to the Chief of Staff. The alternative is no
    card change: the Chief of Staff then reads the folder as it judges best.

## Decisions after the specification (they replace the open points they name)

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- **The page's language: both.** English by default and French, from one word file per language, built so that more translations can be added later. The prototype's French labels are the French file. Where an open point above says English only or French only, this answer replaces it.
- **JS and CSS lint: ESLint (and Stylelint, Prettier) through uvx**, on a Node.js taken from PyPI and pinned in the `justfile`, run by `just check`; Biome instead if it covers the targets more simply. `uv`, `just` and `git` stay the only tools installed by hand. The first CR that ships JavaScript (visualization-backend) adds it.
- The other open points stay at the specification's defaults.
