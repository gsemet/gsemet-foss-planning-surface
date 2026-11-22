# CR-444 investigation: the Inbox page

Paths: `CLI` = `skills/chantier/scripts/cli/` of the worktree; `PKG` = `CLI/src/chantier/`;
`WEB` = `PKG/clients/web/`. Base: CR-429's head 5afaae4d. Read only; nothing was run but `rules`.

## Project rules that touch the work

- AGENTS.md: `just check` before hand-back; `just eval-dry-run` for a change under `CLI/src/`; the
  pipeline's `just scenario` green before the PR (the CLI changes). A change under `WEB` reads
  `WEB/DESIGN.md` first and keeps it true. No Node in tests. CONTRIBUTING.md: a pane screenshot is
  owed only for `hooks/register.tsx` / `STATUS.json` changes (not this CR).
- The surface's AGENTS.md (40 lines) was listed by `rules`; not read here (nothing to do with a web page).

## DESIGN.md rules that bind this CR

1. Tokens only: every colour, radius, spacing, type size via `var()`; margin/padding/gap take
   `--space-*`/`--space-off-*`; font sizes `--text*`; radius `--radius*`. A view-sheet custom
   property holds only an angle, opacity or width. `.bnav .n` (shell.css): `--text-badge`,
   `--accent`, `--white`, `--radius-pill`, `--space-*` (all exist in tokens.css; `--radius-pill` is
   in the off-scale table). Token table needs no change (tested by `test_token_table`).
2. No side accent border (no `border-left/right/inline*`, one-side inset shadow, pseudo bar).
3. Components styled in their own sheet only (`css/components/{card,column,chip}.css`); a page
   sheet (`css/views/inbox.css`) only lays out: grid/flex/gap/order/`*-self`/width/min/max
   width/height/overflow/margin on a component. It must not restyle a card or chip
   (`test_components`). The `.tag.st.off` rule goes in `chip.css` (DESIGN: a toggle chip is "filled
   when on, outlined grey when off, the same size in both states"; update that sentence).
4. Every card is built by `js/ui/card.js` (`test_one_card`): the Inbox entry uses `card({...})`
   only, no hand-written `class="card"`.
5. One-line titles: title cut with ellipsis, full text in `title` (card.js `heading()` does it;
   `test_a_card_title_is_one_line...`).
6. Words: every string through `t()`/`tf()`/`tn()`, in both languages (the code-targets test
   `test_the_web_frame_has_small_scripts_and_both_word_files_share_their_keys` diffs en* vs fr* key
   sets across `en*.js` / `fr*.js` including `*-inbox.js` and `*-mr.js`, and caps every
   `js/**/*.js` at 300 lines).
7. One transport: only `core/transport.js` (+ api.js) talk to the server; the Inbox imports none.
8. Protected features untouched; "Waits on a card" section untouched; add `## The Inbox page`
   after it and the filter-chip sentence. Test checks tokens table vs tokens.css, sheets, components,
   `check_raw` literals (see `tests/test_board_design.py`).
9. Frame test also bans (see `test_the_web_frame_is_self_contained...`, not re-read): other origins,
   `on...` attributes, so `new Notification(...)` must use `addEventListener('click')`.

## Files the spec edits, and what is there now

### Server (Python)
- `PKG/board/state.py`: `project_line(project_id, state)` (line ~191) builds the line from
  `state["batch"]`, `state["backlog"]`, `state["events"]`; add `"needs_you": needs_you(state)`.
  `_entry(c)` -> `{cr, title, pr}`. `_seat(repo)` -> `{title, env}` or None, held under
  `state["seat"]`. `state["batch"]["merge_order"]` (list of CR ids, `crs.merge_order`),
  `state["batch"]["crs"]` rows. Note `_batch` is built for `repo.batch_folders()[0]` whatever the
  batch's status, so running and paused both feed `needs_you` (Q18) with no extra work.
- `PKG/board/crs.py::_row` (the row): fields needed: `cr`, `title`, `folder`, `state` (= `c.status`),
  `pr` (= `c.shown_pr()`), `blocked` (reason, only when status blocked), `open_waits`
  (`typed_waits.open_of(c.waits)` if `counted(status)`, i.e. empty for merged/cancelled),
  `handed_back_at`, `times["state_at"]`, `to_review`, `updated`. All present; no change to `_row`.
  `times.cr_times` (`PKG/board/times.py`): `state_at` = max of take/round/handback/pr-draft/cancel and
  order merged/drop events; None with no events. A heartbeat or cost write is not in `STATE_KINDS`,
  so `state_at` is stable under them (Q20). Beware: a `ready` CR whose PR turns draft then ready
  gets a `pr-draft` event, so `state_at` moves: new `merge` key, as specified.
- `PKG/board/backlog.py::backlog_items` (line ~120): items carry `item` (slug), `title`, `folder`,
  `open_waits` (from `open_waits(store, folder)` reading `waits.json`; [] on invalid). `needs_you`
  walks `state["backlog"]` (dict of the stages `inbox, P1..P4, 3-ready`, STAGES).
- Waits shape (`PKG/core/waits.py::make`): `{id, type, ref, link, since, note, cleared_at,
  cleared_by}`; `TYPES = answer, approval, pipeline, merge`; `since` is `clock.now()` (UTC ISO `...Z`).
  `open_of` = `cleared_at is None`. `wait add approval` refuses a CR with no PR and no `--ref`
  (spec's demo statement; not re-verified in the CLI code).
- `PKG/board/reads.py::board_data` calls `project_line(p.id, state_of(ctx, p, ask=False)[0])` per
  project: `needs_you` rides there. `PKG/board/api/topics.py::_board` hashes `data["projects"]`,
  so a changed entry pushes the topic. The page's own filter in `core/refresh.js::onBoard`
  compares `JSON.stringify([projects, writer])`, so `needs_you` redraws too.
- Fingerprint (`PKG/board/fingerprint.py`, `counts_for`): DEEP covers `4-batch`, `3-ready`,
  `2-backlog`, `1-inbox` whole, so a `waits.json` or `batch.json` change moves the rev; nothing to add.
- New `PKG/board/needs.py` (`needs_you`, `KINDS`), pure; mypy applies (`just lint` runs mypy): type
  the dict plumbing as the sibling modules do (`dict[str, Any]`).
- `docs/server-api.md` line 77: `board.get` row lists `projects` among the keys; add the
  `needs_you` sentence there. The "welcome op count" mentioned in the brief is not touched: the spec
  adds no op or topic (the `welcome` row, line 53, lists `ops`/`topics` only as arrays; no number to
  change; the `Versions` text of "an added field stays protocol 1" is to be cited, not edited).

### Web client (all under `WEB/`)
- `js/views/registry.js`: `VIEWS` array (home first). `countOf(view, state)` =
  `project(state) ? view.count?.(state) ?? null : null`, where `project = state.project !== ALL &&
  Boolean(state.data)`. Change: on ALL return `view.countAll?.(state)` when present, else null as now.
  The head comment documents `overview`; add `countAll` and `badge`.
- `js/ui/sidebar.js`: `item()` draws `<span class="n">${n}</span>` after the word from `countOf`;
  `shown(view, state)` = ALL needs `overview`. No change needed there beyond `countOf`.
- `js/ui/bottombar.js`: `bottomBar(state)` maps `VIEWS.filter(shown)` to a button with `.ic` icon
  and word; add the `badge` count with `countOf`. `css/shell.css`: `.bnav` (line ~95, hidden by
  default, `display:flex` under `@media (max-width: 760px)` with `justify-content: space-around`),
  `.bnav button` column flex; 7 views + Inbox = 8 buttons on 360 px: add `overflow-x: auto`
  (the spec's CR-439 rule; whichever CR lands second keeps one rule). Existing `.bnav .ic .svgi`
  rule lives in `css/components.css:25`.
- `js/ui/icons.js`: icon table keyed `home`, `triage`, ... with path strings (e.g. line 5, 16);
  add `inbox`.
- `js/ui/header.js`: `title(state)` today `state.project === ALL ? surfaceName(state) : t(entry(view).word)`;
  spec: on ALL show the surface name only for `home`, else the view's word. Also `crumbs` uses
  `surfaceName` as the first crumb (unchanged). `stats(state)` on ALL shows `overall(state)`: on
  the Inbox that stats line stays (spec silent; flag in questions).
- `js/main.js`: `drawFrame(state)` paints the frame; add `document.title`; `subscribe(draw)` then
  `draw(snapshot())` then `boot()` at the bottom: add `watchInbox()` after `subscribe(draw)`.
  `[data-project]` click handler: `toAll = el.dataset.project === ALL && !overviewIds().includes(view)`;
  `go({project})` otherwise keeps the current `view`, so on ALL a folder-Open button with
  `data-project="<p>"` moves to that project and stays on `inbox` (Q6/OQ6 A).
- `js/core/store.js`: `data` object + `update(patch)` (`Object.assign` + call every listener, **no
  try/catch**), `pref(key)` = `localStorage.getItem('chantier.'+key)`, `setPref(key, value)`.
  Both are the only `localStorage` users (a test claims this, to be extended). Note the keys
  `chantier.inbox.marks` etc. are `pref('inbox.marks')`: the `chantier.` prefix is added by `pref`,
  so `marks.js` calls `pref('inbox.marks')`, not the full name. Add the four fields
  (`inboxMarks`, `inboxKinds`, `inboxTick`, `inboxNotifyBlocked`). `pref` can throw when storage
  is disabled (privacy mode): `marks.js` should read inside try/catch (not in spec).
- `js/core/router.js`: `ALL = '*'`, `configure(views, overview)` from the registry ids; `?v=inbox`
  needs no change. `reset` list: not touched.
- `js/ui/host.js::show(root, state)`: mounts a view once per `project|view` key, then `render`
  every draw, `after(root, state)` every draw. `ready(state)` for ALL = `state.board`. `paint()`
  (`js/core/paint.js`) skips an unchanged markup. The view module shape is
  `{render, mount?, after?}`; the same module is `module` and `overview` for the Inbox.
- `js/i18n/en.js` / `fr.js`: merge imports `batch, board, costs, mr, prs, write` and spread them at
  the end (lines 241-246); `nav.*` keys at lines 14-20. Add `inbox` import/spread and `nav.inbox`.
  `en-mr.js`/`fr-mr.js` hold `mr.<key>` variants (`mr.open`, `mr.home.open_prs`...) read by
  `tf(forge, key)` on GitLab; `inbox.sub` mentions PR so it needs `mr.inbox.sub` in both.
  `tf` replaces `{name}` from `params`.
- `index.html`: view sheets listed in the `<head>` (last: `css/views/home-project.css`); add
  `css/views/inbox.css`.
- `css/components/chip.css`: `.tag.off` at line 78 (before the state rules); `.tag.st.<state>` rules
  lines 168-197 (`.tag.st.queued, .tag.queued` last at ~196). Add `.tag.st.off` after the last
  state rule. `button.tag` (line 69) gives a toggle its 1px border via `--edge`.
- `js/views/home-prs.js` (`prsBlock`): reference for a PR row: `isMergeRequest(url) ? t('mr.open') :
  t('pr.open')`, `<a href target=_blank rel=noopener>` and `opener(crKey(c), 'pr-')` for the folder.

### Helpers (signature, file)
- `card(parts = {})` `WEB/js/ui/card.js`: `{as, href, classes, attrs, variants[], heading('div'|'h2'|'h3'),
  priority, picked, top, title, labels, desc, body, meta, end, foot, stamps}`; `attrs` is Markup
  (use `html` tag); `end` is wrapped in `.card-end`; returns Markup. Variants allowed (card.css):
  `compact`, `dim` among the list (to verify `card-compact` and `card-dim` exist in card.css).
- `tag(kind, text, {badge=false})` `js/ui/parts.js`: `<span class="tag ${kind}[ badge]">`.
  `tag('badge', ...)` as the spec writes gives class `tag badge` (kind `badge`) AND no `badge`
  option; check which one `.tag.badge` (chip.css line 18) wants: use `tag('', t('inbox.new'), {badge:true})`
  or `tag('badge', ...)`: both give `tag badge` (the second `tag badge`, the first `tag  badge`).
- `stateIcon(s)` `js/ui/parts.js`: `s` a name or CR; returns `<span class="si <name>">`; names with
  glyphs come from `stateGlyph` (`icons.js`): confirm `waits`, `working`, `ready`, `blocked` are
  all there (they are the `.si.*` states in chip.css).
- `priorityChip(bucket, {button, on, attrs})` shows how a toggle chip is built: `<button type=button
  class="tag pri-X[ off]" aria-pressed="on" ${attrs}>`; the Inbox filter follows with `st <state>`.
- `empty(text)`, `mark(id)` (project square), `dot`, `live` in `js/ui/parts.js`.
- `opener(key, scope='')` and `bindOpen(root)` `js/ui/open.js`: `data-open="<key>" data-key="<scope>open-<key>"
  tabindex=0 role=button`; `bindOpen` delegates click and Enter/Space on `[data-open]` and calls
  `targetFor(snapshot(), key)` (`js/model/targets.js`): it resolves against `state.data`, so it
  works on a project only; `crKey(c)` = `c:<cr>`, `itemKey(item)` = `i:<slug>`. On ALL the
  spec uses a `data-project` button instead.
- `delegate(root, type, selector, handler)` `js/core/dom.js`: returns the remover; the handler gets
  `(event, element)`. `html` tag, `raw`, `textOf`, `esc`, `setHtml`, `$`, `$$`.
- `age(iso, nowIso)`, `hhmm(iso)` (local `HH:MM`, '' if invalid), `safeUrl(url)`, `isMergeRequest`,
  `prNumber` `js/core/format.js`. The i18n's `time.ago` key: not seen in en.js lines 1-30; grep
  before relying on it (`t('time.ago', {age})`), add to `en-inbox.js` as `inbox.ago` if missing.
- `t(key, params)`, `tf(forge, key, params)`, `tn` `js/model/words.js`; `t` uses the shown
  project's forge (`snapshot().data?.forge`), so on ALL use `tf(line.forge, ...)` per entry.
- `pref/setPref/update/subscribe/snapshot` `js/core/store.js`.

### Tests, docs, tooling
- `CLI/tests/test_board_waits.py`: shows the prepared-state pattern (`World` fixture `world`,
  `crs_of(name, state, count)`, `write_batch(project, status, crs)`, `world.repo(name)`,
  `cr_rows(repo, read_batch(repo, 'batch-01'), events)`, `backlog_items(FolderStore(tmp), tmp, rows)`).
  `CLI/tests/forge_world.py`: `crs_of` rows have `pr` `LINK.format(name, n)`, `pr_draft False`,
  `status` given (so `ready`; `to_review` needs `ready_word == READY_TO_MERGE`, which in
  `stack_words.py` depends on the mode and PR draft/base: a stack/series test may need
  `settings.mode` in `write_batch`; check `crs_of` produces `to_review` True on the "ready" CRs, as
  `test_board_prs*.py` suggests). `project_state(project_id, repo, surface, live)` is callable directly
  (used in `tests/test_leases.py` line 380 and `test_store_runtime.py` line 171) and
  `project_line(id, state)`; `needs_you` is pure, so the test can also feed a hand-built dict.
  Events can be written with `EventRecord(...)` and the batch's `events.jsonl` for `state_at`.
- `CLI/tests/test_board_design.py`: helpers `_web(*parts)`, `rules(css)`, parametrized checks; new
  test goes there (spec).
- `docs/web-board.md`: sections `### Home: a project` (line 24, picture `project-pc.png`), `## On a
  phone` (line 139) with the phone table (line 145); add `### Inbox` and `inbox-phone.png`.
- `scripts/docs_screenshots.py::views(page, url, size)` (line 227): `goto(page, url, view, project)`
  and `shot(page, name, size)`; insert after the project home. It uses `?p=<project>&v=<view>&lang=en`.
- `docs/demo/projects/shop-api/changes/4-batch/batch.json`: batch-03 running; CRs: CR-141 merged,
  CR-142/143/149 ready with PRs, CR-144 working with `pull/16`, CR-145 working no PR, CR-146 blocked
  (`blocked_reason` "question: should refunds ..."), CR-147/148 queued. Add `waits` (list) to
  CR-144 (an `approval` wait, link `.../pull/16`) and CR-145 (an `answer` wait): the fixture's rows
  show no `waits` key today. `docs/demo/AGENTS.md` and `README.md` exist (read before editing the demo).
  Two projects needed for screenshot 3 (All projects): `mobile-app` and `docs-portal` exist; their
  batches may need no waits (All projects shows shop-api's entries and any other project's).

## The smallest change (what the spec already names, in build order)

1. `board/needs.py` + `project_line` key + `docs/server-api.md` row + `tests/test_board_needs.py`.
2. `model/inbox.js` (pure), `inbox/marks.js`, `inbox/count.js`, `inbox/watch.js`, `views/inbox.js`
   (+ `inbox/entry.js` if over 300 lines or 50-line functions), `css/views/inbox.css`,
   `.tag.st.off`, i18n pair, store fields, registry/sidebar/bottombar/header/main/icons/index.html.
3. DESIGN.md, `docs/web-board.md`, screenshot script, demo, `test_board_design.py` test.
Nothing smaller meets the spec: the server field is the one place the two scopes can share.

## Risks and checks (values other code measures from)

- `countOf` and the bottom bar: the sidebar's `.n` span exists for every count; the phone bar had no
  count span, so `.bnav button` flex-column layout must still fit 8 buttons at 360 px.
- `lines()` in `core/refresh.js` stringifies `projects`; `needs_you` contains `since`/`text`:
  harmless. `needs_you` added to every project line grows `board` payload (CR text on every push).
  `project_line` is also read by `chantier live` (`clients/tui/`), which ignores unknown keys (the
  spec says so; confirm no strict model in `board/api/protocol.json` / pydantic models forbids extra keys:
  search `protocol.json` for `projects` schema before coding, and `scripts/protocol_schema.py`).
- Search for `to_review` / `blocked` lines elsewhere to see if a published schema lists the line's
  keys exactly (`board/api/` models, `docs/server-api.md`): if a model with `extra=forbid` exists,
  `needs_you` must be added there.
- `header.title` change is also CR-439's; the second to land finds it done (merge conflict risk only).
- A merged CR's open waits are already empty (counted). A backlog item whose CR joined the batch is
  keyed twice over a short time (OQ7).
- `merge_order` `crs.merge_order` for `parallel` mode sorts by `handed_back_at or ""`: `merge_place`
  is a place in that list, valid for every mode.
- `Notification` constructor guard, `pref()` under disabled storage, `document.title` on every draw:
  `drawFrame` runs on every store change; set the title only when it differs.
- 300-line file cap on every `js/**/*.js`, Biome (`just lint` runs `biome check` on `WEB`): quotes,
  import order (sorted), no unused vars, line width are enforced: run the formatter style of siblings.

## Questions only the user can answer

None blocking: the spec's Q1-Q20 are answered. Two small points the spec leaves, decided as A and
flagged for the Driver: (1) on "All projects" the Inbox page keeps `stats(state)` (the surface's four
figures) under its title: left as is; (2) `time.ago` word: add `inbox.ago` if `time.ago` does not
exist.

## Evidence plan

Kind: a UI feature (web client page) plus one read-only server field.

- Before/after by command: `just test` (new `tests/test_board_needs.py`, new design test), `just lint`
  (ruff, mypy, Biome), `just check`, `just eval-dry-run`, and the pipeline's `just scenario`.
  Output: the pytest summary lines, saved in `work/gates/` as `*.log` (not published).
- A command's output showing `needs_you` on a real state: run `chantier board` from the worktree
  against `docs/demo` (or the planning surface) and `curl`/`board.get` once; capture the JSON of one
  project line into `evidence/needs-you.json` (small, trimmed to `needs_you`). Before: key absent;
  after: the four kinds.
- Screenshots (the visual record, DESIGN.md): from `chantier board` serving `docs/demo` at the
  head, via Playwright (`scripts/docs_screenshots.py` already drives it: `just docs-screenshots`
  after the `views()` edit writes `docs/web-board/inbox-pc.png` and `inbox-phone.png`). The five
  by-hand pictures of the spec (project with four kinds and "new"/count/tab title; empty; All
  projects; phone with badge and open "Hidden (n)"; French with a Later hide) are taken by a small
  Playwright script in the scratchpad or `work/` (a Playwright run is the project's own tool, `uv
  run --script scripts/docs_screenshots.py` carries it); the tab title is read with
  `page.title()` and printed, since a screenshot does not show it. Hides (Snooze/Later/Discard)
  are driven with Playwright clicks, then `page.evaluate` of `localStorage` for the marks, the
  clock set with `page.clock` for the 1 h return and the 08:00 cases (this proves the "written
  check" lines that no test covers; mark each line as run or not exercised).
- Cannot be shown: the browser notification (headless Chromium can be given the permission with
  `context.grant_permissions(['notifications'])`; the OS toast itself is not visible), the guarded
  call on Android Chrome (to name in Known gaps), the plain-HTTP network address case (a second
  non-loopback origin would be needed: say not exercised unless a LAN address is reachable), and
  no pane screenshot is owed (no `hooks/` change).
- Open gap: Playwright availability on this machine is unchecked; if absent, the five screenshots and
  the written check need the user's browser, to say in Known gaps.
