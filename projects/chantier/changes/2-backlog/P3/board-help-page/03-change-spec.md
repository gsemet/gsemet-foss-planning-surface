# Web board: a Help page of chantier's concepts and roles

Short name: `help`. A new view of the web client; no server, CLI, card or agent change.

## Goal

The user (2026-11-15): "Add a page under Home called 'Help' that explains the concepts, the roles,
etc., with nice cards to click for more detail. Take roughly the concepts presented in the README."
Both board languages. The batch's goal (ui-night, 2026-11-21): a working UI, shown.

The board gets a **Help** view in the sidebar: two groups of the board's own cards, **Concepts** and
**Roles**, each a name and one sentence; a click (or Enter) opens a short detail on the same page,
kept in the address, closed by Escape, its close control or Back, ending where it applies with one
"Read more" link to chantier's documentation on GitHub. All its text ships in the English and
French language files; the page calls no server operation and shows no project data.

Every path below is under `skills/chantier/scripts/cli/src/chantier/clients/web/` unless it starts
with `skills/`, `docs/` or `tests/` (`tests/` is `skills/chantier/scripts/cli/tests/`). Read
`DESIGN.md` first and keep it true (AGENTS.md).

## Decisions carried from 02-answers.md

| Answer | Carried as |
| --- | --- |
| ui-night | the CR joins batch-30; a working UI is the goal |
| ui-night act | not this CR's matter (the Inbox's); Help writes nothing, so AGENTS.md's rule holds |
| help-Q1 | registry order: `home`, `inbox` (when `board-user-inbox` has landed), `help`, then `triage`... (section 1) |
| help-Q2 | one module for a project and for "All projects", no `count` (section 1) |
| help-Q3 | 12 concept cards and 11 role cards, fixed below against the README (section 3) |
| help-Q4 | a card is a name and one sentence; one detail open at a time, on the same page, closed by Escape or its close control; detail at most about 150 words (sections 2, 4) |
| help-Q5 | cards and detail built by `js/ui/card.js`, a plain grid under two headings, tokens and the existing icon set only, no picture, no diagram (section 4) |
| help-Q6 | text in `js/i18n/en-help.js` and `fr-help.js`; no op, no topic, no data read (sections 1, 3) |
| help-Q7 | every key in both files; the language button redraws at once (it already redraws the page); chantier's names stay in English in French (section 3) |
| help-Q8 | a `doc` URL per topic that has a page, on `https://github.com/gsemet/chantier`, new tab; French says the page is in English (section 3) |
| help-Q9 | `&h=<topic>` in the address; Back closes the detail (section 2) |
| help-Q10 | out of scope list (below) |
| help-Q11 | text written against chantier as batch-30 leaves it; `docs-gardening` owns `docs/web-board.md` and the batch-end correction (below) |
| help-Q12 | no `depends.json`; shared files listed (below) |
| help-Q13 | the evidence (below) |

## What changes

### 1. The view, the sidebar and the frame

- **`js/views/registry.js`**: import `* as help from './help.js'` and add one entry right after
  `home` (after `inbox` if `board-user-inbox`'s entry is already there):
  `{ id: 'help', icon: 'help', word: 'nav.help', module: help, overview: help, offline: true }`.
  No `count`: the sidebar shows no number beside it. `overview: help` keeps it in the sidebar and
  the phone's bottom bar on "All projects" (`ui/sidebar.js:shown`, `ui/bottombar.js` need no
  change). Extend the file's head comment with `offline`: the view needs no project data.
- **`js/ui/host.js`**: `ready(state)` is true for a view whose registry entry has `offline`
  (import `entry` from the registry), whatever `state.data` holds; other views are unchanged. So
  Help draws with a project whose data has not arrived and while the board is unreachable.
- **`js/ui/header.js`**: `title(state)` shows the surface's name only on "All projects" **Home**;
  every other view, Help included, shows its own word (today it is the surface name for any view
  on "All projects", which only Home reaches). `crumbs` and `stats` are unchanged.
- **`js/ui/icons.js`**: one new outline `help` (a circle with a question mark), in
  `currentColor`, like the others, e.g.
  `<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14"/><path d="M12 17h.01"/>`.
- **`js/i18n/en.js`, `fr.js`**: `'nav.help': 'Help'` / `'nav.help': 'Aide'` beside the other
  `nav.*` words; import `help` from `./en-help.js` / `./fr-help.js` and spread `...help` with the
  others.
- **`index.html`**: one `<link rel="stylesheet" href="css/views/help.css" />` after the other view
  sheets.

### 2. The address (help-Q9)

`js/core/router.js` (with the store, the only writer of the URL):

- The head comment names `&h=<topic>` (the Help view's open topic).
- `rules` gains `topics: []`; `configure(views, overview, topics = [])` stores it.
- `resolve()` returns `topic`: `asked.get('h')` when the view is `help` and the id is in
  `rules.topics`, else `null` (an unknown or stale id opens the page with no detail). Keep
  `resolve` within Biome's complexity limit (a small helper like `only` is fine).
- `href()` writes `h` only when `place.view === 'help'` and `place.topic` is set.
- A new `topicOf(place, now, view)`, beside `tabOf`: `null` on any other view; `place.topic` when
  it is given (`null` closes; an id not in `rules.topics` is `null`); else `now.helpTopic` (a
  change of project keeps the open topic, Help being the same everywhere).
- `go()` passes `topic: topicOf(...)`; `apply()` sets `helpTopic: topic ?? null`. Every move
  pushes a history entry as today, so opening a topic is one entry and Back closes it; `listen()`'s
  `popstate` already re-resolves the address.
- `js/core/store.js`: `helpTopic: null, // Help: the open topic's id (the address's h=), or null`.
- `js/main.js`: `configure(ids(), overviewIds(), topicIds())` with `topicIds` from
  `js/views/help-topics.js`; `closeInnermost()` gains, after the panel's branch,
  `else if (helpTopic) go({ topic: null })` (Escape closes the detail; the existing guard
  `!$('dialog[open]')` stays).

### 3. The content (help-Q3, Q6, Q7, Q8, Q11)

- **`js/views/help-topics.js`** (data only, no words): `TOPICS`, in display order, each
  `{ id, group, doc }`: `group` is `'concepts'` or `'roles'`, `doc` a full URL or `null`; and
  `export const topicIds = () => TOPICS.map((t) => t.id)`. Ids are lower case with underscores
  (`[a-z_]+`): the language-file check's key pattern (`'([\w.]+)':`) does not match a hyphen.
- **`js/i18n/en-help.js`, `fr-help.js`** (merged into `en.js` / `fr.js`, head comment like
  `en-batch.js`): the page's words, `help.intro` (one line under the title: what the page is, "click
  a card for more"), `help.concepts`, `help.roles` (the two headings), `help.close`,
  `help.read_more` (en "Read more", fr "En savoir plus (page en anglais)"), and per topic
  `help.<id>.name`, `help.<id>.line` (one sentence, fits the card's two-line description) and
  `help.<id>.body`. A body is plain text: paragraphs separated by `\n\n`, a list as lines starting
  with `- `; no Markdown, no HTML. English body at most 150 words, French at most 175 (French runs
  longer). Each file stays under 300 lines.
- **French** (help-Q7): plain French around chantier's own names as the board writes them: Chief
  of Staff, Foreman, Driver, Griller, batch, slot, CR, PR, Coder, Inspector, Verifier, stack driver,
  Release driver, spec-writer, spec critic. `nav.help` is "Aide".
- **Source** (help-Q3, Q11): the README as batch-30 leaves it; where the README only names a role
  or concept, the documentation page the README links for it (see open question 2). Nothing from
  the cards, the code or the CLI's help; no command reference.

The 23 topics, in order. "Facts" are what the detail must say (from the README section named);
"Read more" is the topic's `doc` (repository `https://github.com/gsemet/chantier`, `R` =
`https://github.com/gsemet/chantier`, `D` = `https://github.com/gsemet/chantier/blob/main/docs/`).

**Concepts**

| id | name (en) | Facts (README section) | Read more |
| --- | --- | --- | --- |
| `change_request` | Change request | one level over the tracker's issues; small requests accepted and prioritised without entering the tracker; a folder, from one line to prototypes; agents read it for its intent; fungible: split, merged, dropped (intro, "Change Requests Lifecycle") | `R#change-requests-lifecycle` |
| `grill` | Grill and specification | the Chief of Staff (or a Griller) asks the questions a change needs; each answer is recorded; at "grilled enough" you choose the next batch (`3-ready`, default) or the running batch, and the spec-writer writes the Change Specification, checked by the spec critic on an impactful CR (intro, "Planning modes" first paragraph, "Running batch or next batch", "Use") | `D` + `use-cases.md#turn-ideas-into-ready-work` |
| `planning_folder` | Planning folder | where chantier writes everything, Markdown and JSON; the stages: inbox, backlog P1 to P4, `3-ready` (the next batch), `4-batch` (pending, active, done), then archives (intro, "Planning modes", "Use" "init") | `D` + `planning-folder.md` |
| `batch` | Batch and slots | n CRs, m PRs, p batches, 1 release; not continuous delivery; slots: CRs run side by side, a CR added while the batch runs waits for a free slot; running, paused, closed; close on your yes (intro, "Running batch or next batch", "Batch modes" last paragraph) | `D` + `use-cases.md#the-life-of-a-batch` |
| `cr_lifecycle` | A CR's life | planning, study, implementation, QA, deployment, archive; the implementation loop with Drivers and strict reviews; the QA loop; the release (sections "Change Requests Lifecycle", "Detailed lifecycle") | `R#detailed-lifecycle` |
| `planning_modes` | Planning modes | in-project (`.agents/changes/`, the default) or an external planning surface (its own repository, one folder per project, the server commits and pushes the plan) ("Planning modes") | `D` + `planning-modes.md` |
| `steering` | Direct or Foreman | who steers the batch: the Chief of Staff itself (direct) or a nested Foreman session; the mode follows where you are, `foreman` or `direct` forces one; in direct mode grill in a Griller session while the batch runs ("Direct or Foreman", "How Chantier works") | `D` + `use-cases.md#choose-your-configuration` |
| `batch_modes` | Batch modes | parallel (default), series, stack: how the PRs relate and who merges what, when; you merge, never chantier; `depends.json` waits in every mode; a running batch can switch mode ("Batch modes") | `R#batch-modes` |
| `project_rules` | Your project's rules | your changes must land without chantier; `AGENTS.md` and an optional `chantier.yaml` are the only configuration (agent and model per role) (intro "Respect the project's rules") | `D` + `agents-and-models.md` |
| `gates` | Gates | the fast gate and the long gate you declare in `AGENTS.md`; init checks the long gate and writes the lines on your yes ("Install", "Use", "More") | `D` + `gates.md` |
| `costs` | Costs and limits | a batch has a budget; steering and Drivers are most of it; the Chief of Staff's session is priced apart, never in the budget; ask "what did it cost?" or `chantier cost`; the slots and the specifying limit are set on the Configuration page ("What a batch costs") | `D` + `costs.md` |
| `boards` | Boards | this web board (live, triage from the phone, one client of the server's API), the read-only pane in Claude Code, `chantier live` in a terminal ("The CR board", "More") | `D` + `boards.md` |

**Roles**

| id | name (en) | Facts | Read more |
| --- | --- | --- | --- |
| `chief_of_staff` | Chief of Staff | the one person you talk to, in your session; keeps the backlog, grills, opens batches on your go, steers in direct mode; holds the seat ("One person to talk to", "Use") | `D` + `use-cases.md` |
| `griller` | Griller | an optional session that refines the inbox and the backlog beside the Chief of Staff, never opens a batch ("Use", "How Chantier works") | `D` + `use-cases.md#a-chief-of-staff-and-grillers-in-remote` |
| `foreman` | Foreman | a nested session that steers a batch in Foreman mode, so the Chief of Staff stays free to grill ("Direct or Foreman") | `D` + `use-cases-foreman.md` |
| `driver` | Driver | runs one CR in its worktree, delegates to workers and reviews, up to a PR handed back ready ("Detailed lifecycle", "Planning modes" worktrees) | `D` + `agents-and-models.md` |
| `spec_writer` | Spec-writer and spec critic | writes the Change Specification in the background once a CR is grilled enough; the critic checks it on an impactful CR ("Use") | `D` + `use-cases.md#turn-ideas-into-ready-work` |
| `coder` | Coder | writes the code of a round; runs the fast gate; can be your own agent ("Use", gates page) | `D` + `agents-and-models.md` |
| `inspector` | Inspector | reviews each round; your extra review steps run after it ("Use") | `D` + `agents-and-models.md` |
| `verifier` | Verifier | verifies a CR's head before it is handed back (the long gate's `VERIFIED`) ("What a batch costs", gates page) | `D` + `gates.md` |
| `conflict_resolver` | Conflict resolver | a worker that settles a rebase's conflicts ("What a batch costs") | `null` |
| `stack_driver` | Stack driver | in stack mode, makes the native stack on the forge and restacks it ("Batch modes") | `R#batch-modes` |
| `release_driver` | Release driver | runs a release CR by your project's own procedure; you approve each irreversible action, or say "auto" ("Releases") | `R#releases` |

A body that a batch-30 CR makes false at the batch's end is `docs-gardening`'s to correct (help-Q11).

### 4. The page (help-Q4, Q5)

**`js/views/help.js`**, `render(state)` / `mount(root)` / `after(root, state)` like the other views:

- `render`: `<div class="help">`, the intro line, then per group a heading (`<h2>`,
  `help.concepts` / `help.roles`), a `<div class="help-grid">` of cards, and, when the open topic
  is in that group, its detail right after that group's grid.
- **A topic's card**: `card({ classes: 'help-card', heading: 'h3', title: t('help.<id>.name'),
  desc: t('help.<id>.line'), variants: [open && 'sel'], attrs })` with `attrs` =
  `data-help="<id>" data-key="help-<id>" tabindex="0" role="button" aria-expanded="<open>"
  aria-controls="help-detail"`. No priority chip, no band.
- **The detail**: one more `card({ as: 'section', classes: 'help-detail', heading: 'h3', title:
  name, body, meta, end, attrs: 'id="help-detail" tabindex="-1"' })`; `body` is the paragraphs
  (`<p>`) and lists (`<ul><li>`) of `help.<id>.body`, built with `html` (escaped text, never
  `raw`); `meta` the "Read more" link when `doc` is set (`<a href target="_blank" rel="noopener">`,
  `help.read_more` and the `ext` icon); `end` a `<button type="button" data-help-close
  data-key="help-close">` with `help.close`. One detail at a time.
- `mount(root)`: `delegate` click on `[data-help]` → `go({ topic: id })`, or `go({ topic: null })`
  when that card is the open one (a second click closes); keydown Enter or Space on `[data-help]`
  does the same (`preventDefault` on Space); click on `[data-help-close]` → `go({ topic: null })`.
  Returns the cleanup like `costs.js`.
- `after(root, state)`: when the open topic changed since the last call, move the focus to the
  detail (`#help-detail`, `preventScroll: false`, so the phone scrolls to it) on open, back to the
  card `[data-key="help-<id>"]` of the topic just closed on close.
- Within the limits: file at most 300 lines, functions at most 50 lines, complexity at most 10.

**`css/views/help.css`** (a page sheet: layout only, tokens only, DESIGN.md "Tokens" and
"Components"): `.help-grid` a grid `repeat(auto-fill, minmax(220px, 1fr))` with a `space` token gap
(as Home's tiles), one column on the narrow layout by itself; the headings' and intro's margins and
sizes with `space` and `type` tokens; `.help-detail` `margin-top` and a `max-width` for reading.
Nothing restyles the card.

**`css/components/card.css`**: the clickable card's hover also for a Help card:
`.card[data-open]:hover, .card[data-help]:hover { border-color: var(--card-hover); }`. No new
token, colour or variant.

### 5. DESIGN.md

Add a section after "Waits on a card", `## The Help page`, saying: the `help` view, after Home (and
the Inbox), the same on every project and on "All projects", no count; it needs no project data
(the registry's `offline`) and calls no op or topic; every word is an i18n key of `en-help.js` /
`fr-help.js`, the topics' list (ids, group, link) in `js/views/help-topics.js`; topic cards and the
detail are the one card (`help-card`, `help-detail`, the `sel` variant for the open one), in
`css/views/help.css`'s grid; the open topic is the address's `h=`, closed by Escape, its close
button or Back; no picture or diagram. The token table does not change.

## Out of scope (help-Q10)

No search or filter, no guided tour, no tooltips or "?" links on other pages, no command
reference, no live data (agents and models stay on the Configuration page), no Help in
`chantier live`. No server op, no protocol change, no AGENTS.md change, no CR board pane change (so
no pane screenshot is owed). `docs/web-board.md` and its picture are `docs-gardening`'s (help-Q11).

## Batch-30 neighbours (help-Q12)

No `depends.json`. Shared files, found by text; the stack settles each:

- `board-user-inbox` (Inbox page): `js/views/registry.js` (its entry goes before `help`),
  `js/i18n/en.js` / `fr.js` (`nav.*`), `js/ui/icons.js`, `index.html`, `DESIGN.md` (a section of
  its own), possibly `js/core/router.js`, `js/core/store.js`, `js/ui/header.js`.
- CR-434 (`board-batch-kanban`): `js/core/router.js` (`TABS`, `tabOf`, `settle`) and
  `js/core/store.js`; Help adds `topicOf` beside `tabOf` and one store field.
- CR-435 (`board-batch-compact`): `js/main.js` (`drawFrame`); Help edits `configure(...)` and
  `closeInnermost`.
- CR-427, CR-433, CR-434, CR-435 all edit DESIGN.md's "One card, one column, one chip" rule; Help
  adds a new section at the end and leaves that rule alone.
- CR-429 (server watching files): none (Help reads nothing from the server).
- `docs-gardening`, last: adds Help to `docs/web-board.md` and corrects a false Help text.

## Evidence (help-Q13)

**Checks in `just check`** (each reads the shipped files at the head under test):

- `tests/test_code_targets.py::test_the_web_frame_has_small_scripts_and_both_word_files_share_their_keys`,
  unchanged: it now covers `en-help.js` / `fr-help.js` (both files share every key; each script
  at most 300 lines).
- One new test in `tests/test_board_design.py`, `test_the_help_page_is_a_view_with_both_languages_and_real_links`,
  reading from the repository:
  - `js/views/registry.js`: an entry `id: 'help'` with `overview` and no `count`, placed right
    after `home` or right after `inbox` when that entry exists;
  - each id of `js/views/help-topics.js` matches `[a-z_]+`, the 12 `concepts` and 11 `roles` ids
    of section 3 in order, and `en-help.js` holds its `.name`, `.line` and `.body` keys;
  - each body's word count (string read with a regex that takes `'...'` or `"..."` with escapes):
    English at most 150, French at most 175;
  - each `doc` starts with `https://github.com/gsemet/chantier`, and the file it names exists in
    the repository (`README.md` for `R#...`, `docs/<file>` for `D...`), and its `#anchor`, when it
    has one, is a heading of that file (GitHub's slug: lower case, spaces to `-`, punctuation
    dropped);
  - `js/views/help.js` and `js/views/help-topics.js` import neither `core/transport.js`,
    `core/api.js` nor `api/`.
- `tests/test_board_design.py`'s existing checks: tokens, no literal, components not restyled by
  `help.css`, one card (`help.js` builds its cards with `card.js`).
- Biome (`just lint`): file, function and complexity limits.

**Before the push** (AGENTS.md): `just check` and `just eval-dry-run` in the worktree at the
rebased head (a change under the CLI's `src/`); the pipeline's `just scenario (ubuntu-latest)`
green at the PR's head before the PR.

**By hand, in the PR's Deliverables** (DESIGN.md: screenshots are the visual record), from
`chantier board` at the PR's head:

1. The Help page on a project, English, desktop: Help in the sidebar after Home (and Inbox), no
   count.
2. The same in French, with one detail open (address `&h=<id>`), its "En savoir plus (page en
   anglais)" link.
3. "All projects" with Help selected: Help in the sidebar, title "Help".
4. The narrow layout (360 px wide): one column of cards, a detail open, the bottom bar.

And a short written check in the PR: every card opens and closes by mouse, by Enter, by Escape, by
the close button and by Back; a reload with `&h=` opens the same detail; the language button
switches the open page at once; a "Read more" link opens GitHub in a new tab; with the board
stopped after the page loaded, Help still shows its text.

## Open questions (built as A; the user asks none tonight)

1. **Where the detail opens.** A (built): a full-width detail card right after the open card's
   group grid, the open card marked `sel`; no new window, no server read. B: in the side panel
   (`#panel`), which today is the CR folder's panel (head, tree, file reads, editor) and would need
   a non-folder branch in `panel/panel.js`. C: the clicked card widens in place across its row,
   leaving a gap at the row's end.
2. **How strictly "only what the README says".** A (built): the README, and for a topic the README
   only names (the workers mostly), the documentation page the README links for it. B: the README
   alone; the worker cards then say little, or fold into one "Workers" card.
3. **Help before the board's first answer.** A (built): as every view, the page shows "Loading…"
   until the first `board.get` answers (the address is resolved only then); afterwards Help shows
   whatever the board's state. B: resolve `?v=help` before the first answer and draw Help at once.
4. **The phone's bottom bar.** A (built): Help is in the bottom bar like every view; if the bar no
   longer fits 360 px with the Inbox and Help, `.bnav` in `css/shell.css` gets `overflow-x: auto`
   (a frame sheet, no component), shown in screenshot 4. B: Help stays out of the bottom bar on the
   phone.
