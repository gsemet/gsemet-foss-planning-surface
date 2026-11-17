# Feature session — plan (S5)

Inputs: `STATE.md` (protocol), `decisions.md` (U1–U17, D1–D28, binding), `CHANGES.md` (scope),
`analysis/*.md`. Repo `~/Projects/DevTools/markdown-okf-schema-studio`, branch `dev/gsemet`,
start `9df67aa` (0.3.1). Anchors in task files were checked against `9df67aa`; later tasks shift
line numbers, so every task names functions and gives lines as hints only.

6 phases, 45 tasks (T01–T45), 6 phase-end e2e checkpoints, 1 session-end `just preflight`,
14 archive landings (007–020). rendering-difference-on-windows stays open (D28, no task).
Two tasks (T26, T30) are proposals that need the user's approval at S6 (status `needs-approval`).

**D13 superseded by intent line 8** (`01-intent.md` of block-edition-palette: "Every
non-supported edition in the code should result in new feature added to the code"): no palette
button is hidden because its syntax does not render. Each unsupported syntax gets a rendering
task with a render test first (T06 strikethrough, T27 amsmath + figure width/align + `(label)=`
anchor icons, T33 inline colour), then the button. Emoji are inserted as Unicode (D11), which
already renders as text, so no rendering task is needed for them.

## 1. Execution model

Per task (strictly sequential): orchestrator (Opus) sets status `implementing`, launches a
Sonnet 5.5 implementer with **only** `tasks/Txx.md` plus the round number and, for rounds ≥ 2,
the review file. The implementer writes code and tests (new tests first, failing before the
change where possible), runs the task gate in the foreground, leaves nothing running, does not
commit, and writes `reports/Txx-rN.md`. Orchestrator re-runs the gate (`gating`), then a separate
Sonnet 5.5 reviewer gets the task file, the report and `git diff` and writes `reviews/Txx-rN.md`
with verdict `APPROVE` or `FIX-REQUIRED` (`reviewing`). Up to 3 rounds. On APPROVE the
orchestrator commits (one commit per task) and records the hash (`done`).

### Gate tiers (U4)

| Code | Command (repo root, foreground) | When |
| --- | --- | --- |
| B | `fnm exec -- npm run check-types && fnm exec -- npm test && fnm exec -- npm run test:visual` | every task (compile + types + unit + contracts + security + visual) |
| T | `env -u ELECTRON_RUN_AS_NODE fnm exec -- npm run test:integration -- --trusted-only` | tasks touching editing, messages, toolbar, webview runtime (includes realInput + checkboxToggle: **unlocked screen**) |
| S | `env -u ELECTRON_RUN_AS_NODE fnm exec -- npm run test:scroll` | tasks touching layout, anchoring, sticky band, toolbar geometry |
| R | `env -u ELECTRON_RUN_AS_NODE fnm exec -- npm run test:reload` | tasks touching persisted state or page reload |
| F | `env -u ELECTRON_RUN_AS_NODE fnm exec -- npm run test:integration` | tasks touching trust/readOnly or host lifecycle (scroll, untrusted, trusted, standalone, reload) |
| E | `env -u ELECTRON_RUN_AS_NODE fnm exec -- npm run test:e2e` | end of each phase |
| P | `just preflight` | once, end of session (cleans `out/`, reformats the justfile, `uv run` without `--no-sync`) |

Never run `just dev`, `just update`, `npm ci`, `npm install`, `uv sync`, `fnm install`.
Before any of T/S/R/F/E/P: `ps -ax | grep -E "run-tests|extensionDevelopmentPath" | grep -v grep`
must print nothing (no overlapping VS Code test runs; wait or kill leftovers of this session only).
Locked screen: realInput and checkboxToggle fail (keyboard injection) while the macOS session is
locked (`ioreg -n Root -d1 | grep -q CGSSessionScreenIsLocked` = locked). If T fails only there
while locked, record `gate: T pending-unlock` in the journal, continue the review on the other
evidence, and re-run T (or E) as soon as the screen is unlocked; a phase cannot close with a
pending-unlock T.

## 2. Phases

1. **Foundations and quick wins** (T01–T07): glossary, settings text, message registry, copy code,
   include end-line clamp, strikethrough, inline-image gaps.
2. **Toolbar and reading layout** (T08–T13): two-row toolbar with persisted view preferences and
   zoom, unified top gap, margin modes, back/next, TOC.
3. **Reading annotations** (T14–T19): comment/TODO chips, incoming-change marks, MyST autodetect.
4. **Edition palette** (T20–T35): shortcuts, palette bar, link panel, modes, grid/emoji, GFM (+
   proposals), MyST rendering gaps, MyST group, anchor edition, MyST proposals, image picker,
   figure editor, colour (sanitizer first), table-cell merge.
5. **Block operations** (T36–T41): move, paste image, multi-block selection.
6. **Local comments** (T42–T45): display, create/reply, resolve/delete/orphans, re-anchoring.

## 3. Task table

Gate column: B always, plus the listed suites. Status values: `todo`, `needs-approval`,
`implementing`, `gating`, `reviewing`, `changes-requested`, `done`, `blocked`, `dropped`.
Round = last round started.

| ID | Title | Backlog item | Ph | Size | Depends on | Gate | Commit type(scope) | Status | Round | Commit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | Shared glossary referenced from AGENTS.md | (U10, none) | 1 | XS | — | B | docs | done | 1 | `a79b714` |
| T02 | Clear setting descriptions, fixed wording, ordering | vscode-setting-rework | 1 | S | T01 | B | fix(vscode) | done | 2 | `0e20a45` |
| T03 | Preview message registry for new message types | copy-code-block (infra) | 1 | S | — | B T | refactor | done | 1 | `fd5233f` |
| T04 | Copy button on every code block | copy-code-block | 1 | S | T03 | B T | feat(render) | done | 2 | `a726bde` |
| T05 | Clamp included-block line ranges, mark included blocks | move-block-up-down (prereq) | 1 | S | — | B T | fix(editor) | done | 1 | `ef1dbce` |
| T06 | Render `~~strikethrough~~` | block-edition-palette (prereq) | 1 | S | — | B | feat(render) | done | 1 | `867c21f` |
| T07 | Inline-image editing gaps (linked image, raw `<img>`, ArrowUp into properties) | edit-inline-image | 1 | S | — | B T | fix(editor) | done | 1 | `b974c5e` |
| T08 | Two-row toolbar, persisted view preferences, Zoom −/+ | block-edition-palette | 2 | M | T03 | B T S R | feat(vscode) | done | 1 | `201b2d6` |
| T09 | Same ~40 px gap above the first element | bug-one-line-top-margin-missing | 2 | S | T08 | B S T | fix(render) | done | 1 | `3bf2624` |
| T10 | Margin button: Margin → Auto → Full width | clever-margin-break, block-edition-palette | 2 | M | T08 | B S T | feat(vscode) | done | 1 | `570bcee` |
| T11 | Back / Next per preview panel | block-edition-palette | 2 | M | T08 | B T S | feat(vscode) | done | 2 | `254b5e4` |
| T12 | Table of contents column (toggle, h1–h4, click to scroll) | toc-in-vscode-markdown-studio | 2 | M | T08 | B S T | feat(vscode) | done | 1 | `ba11c89` |
| T13 | TOC: collapsible nodes, current section highlight | toc-in-vscode-markdown-studio | 2 | S | T12 | B S | feat(vscode) | done | 2 | `9afb00f` |
| T14 | Comment and TODO chips in the preview | todo-comments | 3 | M | — | B T S | feat(render) | done | 2 | `817e056` |
| T15 | Expandable chips, `preview.showComments` setting | todo-comments | 3 | S | T14, T02 | B S T | feat(render) | done | 1 | `6eebd07` |
| T16 | Incoming-change marks (HEAD, green bar, setting) | show-incoming-diff | 3 | M | T03, T08, T02 | B T | feat(render) | done | 2 | `7481493` |
| T17 | Toolbar toggle for incoming-change marks | show-incoming-diff | 3 | S | T16 | B T R | feat(vscode) | done | 1 | `93f6a81` |
| T18 | MyST autodetect warnings in the preview | myst-autodetect | 3 | M | T06 | B | feat(render) | done | 3 | `5406410` |
| T19 | Autodetect warnings in Problems panel, conf.py watcher | myst-autodetect | 3 | S | T18 | B F | feat(vscode) | done | 2 | `4c5c869` |
| T10b | Center tables/figures, breakout centered on available area, README cream screenshot (U22) | clever-margin-break | 3b | S | T10, T12 | B S T | feat(vscode) | done | 2 | `a48535a` |
| T20 | Editing shortcuts Cmd/Ctrl+B/I, Ctrl+/ TODO toggle | block-edition-palette | 4 | M | — | B T | feat(editor) | done | 2 | `43fc386` |
| T21 | Palette bar, strict group (heading h1–h5, code + language, quote, rule, TODO…) | block-edition-palette | 4 | M | T20, T06 | B T | feat(editor) | done | 2 | `b572847` |
| T22 | Link mini-panel (text + URL, focus first empty), Cmd/Ctrl+K | block-edition-palette | 4 | M | T21 | B T | feat(editor) | done | 2 | `8bd2bc2` |
| T23 | Palette mode select strict/GFM/MyST, default setting | block-edition-palette | 4 | S | T21, T03, T02 | B T R | feat(editor) | done | 2 | `3f87eda` |
| T24 | Table 9×9 grid (hover highlight) and emoji picker | block-edition-palette | 4 | M | T21 | B T | feat(editor) | done | 1 | `df1424a` |
| T25 | GFM group: alert dropdown, checkbox, HTML table (convert + new) | block-edition-palette | 4 | M | T23 | B T | feat(editor) | done | 1 | `6dab226` |
| T26 | GFM proposals: details, footnote, mermaid, column alignment, kbd | block-edition-palette | 4 | S | T25 + approval | B T | feat(editor) | done | 1 | `78cf915` |
| T27 | Render amsmath, figure width/align, `(label)=` anchor icons | block-edition-palette | 4 | M | — | B T | feat(render) | done | 2 | `3ca7807` |
| T28 | MyST group: admonitions (all + custom), footnote, deflist, math, sub/sup, label | block-edition-palette | 4 | M | T23, T27 | B T | feat(editor) | done | 1 | `c23c8f2` |
| T29 | Anchor edition: click the anchor icon to rename the label | block-edition-palette | 4 | S | T27, T21 | B T | feat(editor) | done | 1 | `c82062e` |
| T30 | MyST proposals: `{ref}`/`{doc}` picker, `{cite}`, dropdown, `{table}`, `{kbd}` | block-edition-palette | 4 | M | T28 + approval | B T | feat(editor) | done | 1 | `f3941b3` |
| T31 | Image file picker (document folder) and Figure button | block-edition-palette | 4 | M | T23, T03 | B T | feat(editor) | done | 1 | `6c35140` |
| T32 | Figure editor (source, alt, caption, legend, width, align, name) | block-edition-palette | 4 | M | T31, T27 | B T | feat(editor) | done | 1 | `82481e1` |
| T33 | Keep restricted `<span style>` colours (sanitizer + runtime) | block-edition-palette | 4 | S | — | B T | feat(render) | done | 1 | `5b38a2d` |
| T34 | Colour picker (text + background) and colour-code swatch | block-edition-palette | 4 | S | T33, T21 | B T | feat(editor) | done | 2 | `8c97d64` |
| T35 | Palette inline group merged into the table-cell bar | block-edition-palette | 4 | S | T21 | B T | feat(editor) | done | 1 | `9d305ac` |
| T36 | Move a block with ↑/↓ on the insert bar | move-block-up-down | 5 | M | T05, T03 | B T S | feat(editor) | done | 1 | `5293923` |
| T37 | Alt+↑/↓ (Ctrl/Cmd+Alt in the text box) moves the block | move-block-up-down | 5 | S | T36 | B T | feat(editor) | done | 1 | `a57ddf1` |
| T38 | Paste an image into the block editor | paste-image-in-edit-mode | 5 | M | T03 | B F | feat(editor) | done | 1 | `ae5bac0` |
| T39 | Multi-block selection (Shift+click, Shift+↑/↓) | multibloc-selection | 5 | M | T05 | B T | feat(editor) | done | 2 | `c36c9e7` |
| T40 | Copy, cut, paste selected blocks as Markdown | multibloc-selection | 5 | M | T39, T03 | B T | feat(editor) | done | 1 | `b022ec4` |
| T41 | Alt+↑/↓ moves the selected blocks | multibloc-selection | 5 | S | T39, T37 | B T | feat(editor) | done | 2 | `5eae169` |
| T42 | Show comment threads from `<name>.comments.json` | local-comment-mode | 6 | M | T03 | B T S | feat(vscode) | done | 2 | `dade957` |
| T43 | Create a thread from a selection, reply, author | local-comment-mode | 6 | M | T42, T02 | B F | feat(vscode) | done | 2 | `89d6513` |
| T44 | Resolve, delete, list orphaned threads | local-comment-mode | 6 | S | T43 | B T | feat(vscode) | done | 2 | `fea8ce5` |
| T45 | Re-anchor threads after edits | local-comment-mode | 6 | M | T44 | B T | feat(vscode) | done | 2 | `f44d970` |

T01 is a soft prerequisite of every task that lists glossary terms (append to the file it creates).
`needs-approval`: the orchestrator asks the user at S6; approved → `todo`, refused → `dropped`
(the item lands without it, listed under open items as "dropped by the user").

### 3a. GFM group (T25) and proposals (T26, for user approval)

Intent items: alert/admonition (`>` + type dropdown at the caret: NOTE, TIP, IMPORTANT, WARNING,
CAUTION), checkbox (`- [ ] `), HTML table (convert the Markdown table under the caret to
`<table>` and insert a new HTML table). Proposals (all render in Studio today, all render on
GitHub): collapsible section `<details><summary>…</summary>…</details>`; footnote `[^n]` + its
definition; Mermaid diagram fence; table column alignment (left/centre/right on the separator
row of the table under the caret); `<kbd>` keys. GFM math `$…$` is already in the MyST group;
in GFM mode the math button is also shown (GitHub renders `$…$`).

### 3b. Curated MyST list (book: `agentic-coding-white-paper/book`, `sphinx/conf.py`)

The book enables `attrs_inline, colon_fence, deflist, dollarmath, fieldlist, html_admonition,
html_image, replacements, smartquotes, strikethrough, substitution, tasklist`,
`myst_heading_anchors = 3`, plus sphinx_design, sphinx_togglebutton, bibtex, mermaid.
Counts are occurrences in `book/chapters/*.md` (read-only scan, `.orig` files excluded).

| Feature | Syntax | Used in book | Renders in Studio today | Task |
| --- | --- | --- | --- | --- |
| Named admonitions (note, tip, warning, important, caution, danger, attention, error, hint, seealso) | `:::{note}` / ```` ```{note} ```` | yes (210) | yes | T28 |
| Custom admonition with title and class | `:::{admonition} Title` + `:class:` | yes (23) | yes | T28 |
| Dropdown admonition | `:class: dropdown` | yes (3) | yes | T30 (proposal) |
| Footnotes | `[^1]` + `[^1]: text` | no | yes | T28 |
| Definition lists | `Term` / `: definition` | no | yes | T28 |
| Inline math | `$…$` | yes (11) | yes | T28 |
| Display math | `$$…$$`, `{math}` | no | yes | T28 |
| amsmath environments | `\begin{align}` in `$$`/`{math}` | no | not proven | T27 (render), T28 (button) |
| Subscript / superscript | `` {sub}`x` `` / `` {sup}`x` `` | no | yes | T28 |
| Figure with caption, alt, name | `:::{figure} path` + `:alt:` `:name:` + caption | yes (109) | yes | T31 (button), T32 (editor) |
| Figure size and alignment | `:width:` `:align:` | yes (~115/110) | not proven | T27 (render), T32 (editor) |
| Image directive | `:::{image} path` | yes (11) | yes | T31 (Markdown image in all modes) |
| Label anchors | `(name)=` above a block | yes (5) | no marker | T27 (icon), T28 (insert), T29 (edit) |
| Cross-references | `` {ref}`name` ``, `` {doc}`path` `` | yes (1/1) | yes (`{ref}`) | T30 (proposal) |
| Citations | `` {cite}`key` `` | yes (412) | placeholder (bibliography is build-only) | T30 (proposal: insert key) |
| Table directive with caption | `:::{table} Caption` + `:widths:` | yes (18) | yes | T30 (proposal) |
| Keyboard keys | `` {kbd}`Ctrl+K` `` | yes (2) | verify in T30 | T30 (proposal) |
| Strikethrough | `~~x~~` | no (enabled) | no | T06 (render), T21 (button) |
| Task lists | `- [ ]` | no (enabled) | yes | T25 |
| Code with language | ```` ```python ```` / `{code-block}` | yes (55/5) | yes | T21 |
| Substitutions | `{{ name }}` | yes (6, index.md) | no (JS parser) | not a palette item; T18 warns when not enabled |
| Inline attributes | `[x]{.cls}` | yes (3) | no | not a palette item; T18 warns |
| Raw HTML image / table | `<img>`, `<table>` | yes (0/2) | yes | T07, T25 |
| Emoji | Unicode | yes (241) | yes (text) | T24 |
| Build-only directives | `{include}`, `{only}`, `{toctree}`, `{bibliography}`, `{animation}` | yes | include yes, others placeholders | not palette items |

## 4. Checkpoints

| After | Checkpoint | Then |
| --- | --- | --- |
| T07 | E (full e2e) | land 007–009 |
| T13 | E | land 010–012 |
| T19 | E | land 013–015 |
| T35 | E | land 016 |
| T41 | E | land 017–019 |
| T45 | E | land 020 |
| all | P (`just preflight`) once | append the preflight line to every report 007–020; S8 done |

A failing E: open a fix task `Txxa` (same protocol, `fix(scope)` commit) before landing; do not
start the next phase while E is red (pending-unlock excepted as in §1).

## 5. Archive landing

Landing = `mv .agents/changes/backlog/P2/<item> .agents/changes/archives/NNN-<item>` (keep
the intent files) and write `report.md` there. `.agents/changes/` is git-ignored: no commit.
Numbers follow landing order; never reuse or skip a number. A blocked task does not hold a
landing: the item lands with `Status: **partial**` and the task as an open item.

| NNN | Backlog item (folder) | Tasks | Lands after |
| --- | --- | --- | --- |
| 007 | P2/vscode-setting-rework | T02 (later settings: T15, T16, T23, T43 follow its style) | phase 1 |
| 008 | P2/copy-code-block | T03, T04 | phase 1 |
| 009 | P2/edit-inline-image | T07 | phase 1 |
| 010 | P2/bug-one-line-top-margin-missing | T09 | phase 2 |
| 011 | P2/clever-margin-break | T10 | phase 2 |
| 012 | P2/toc-in-vscode-markdown-studio | T12, T13 | phase 2 |
| 013 | P2/todo-comments | T14, T15 (Ctrl+/ is in 016, T20) | phase 3 |
| 014 | P2/show-incoming-diff | T16, T17 | phase 3 |
| 015 | P2/myst-autodetect | T18, T19 | phase 3 |
| 016 | P2/block-edition-palette | T06, T08, T10, T11, T20–T35 | phase 4 |
| 017 | P2/move-block-up-down | T05, T36, T37 | phase 5 |
| 018 | P2/paste-image-in-edit-mode | T38 | phase 5 |
| 019 | P2/multibloc-selection | T39, T40, T41 | phase 5 |
| 020 | P2/local-comment-mode | T42–T45 | phase 6 |

Not landed: P3/rendering-difference-on-windows (0-byte screenshot, D28; add a line to its
intent folder only if the user asks). T01 (glossary) has no backlog item: mention it in the
journal and in 016's report. 016's report also carries the intent traceability table (§11).

Report template (`archives/NNN-<item>/report.md`, same shape as 002/004):

```markdown
# Report — <item>

Status: **done** (feature session, <date>, branch `dev/gsemet`).   <!-- or **partial** -->

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| Txx | <user-visible change, one line> | `<hash>` |

## Proof of completion

- Txx: <n> new tests failed before the change and pass after; review <verdict> (<fix rounds>).
- Phase <n> e2e (<date>): <unit/contract/security counts>, visual <n> scenarios, integration
  suites <list> green.
- Session preflight (<date>): pass.            <!-- appended at session end -->

## Open items

- <blocked task, manual check left to the user, or "none">
```

## 6. Orchestrator protocol (resumable)

After every step: (1) update the task table row (status, round, commit), (2) set `STATE.md` S7
to `running` with "current: Txx <status> rN", (3) append one line to `journal.md`
(`- <date> Txx rN <event>: <one-line result>`). Write the files before launching the next agent.

Files: implementer report `reports/Txx-rN.md`; review `reviews/Txx-rN.md` (first line
`Verdict: APPROVE` or `Verdict: FIX-REQUIRED`, then findings with file:line); a blocked task's
diff `reports/Txx-blocked.patch`.

Resume from the first row whose status is not `done`/`blocked`:

| Status | Resume action |
| --- | --- |
| todo | Start round 1: set `implementing`, launch the implementer. |
| implementing | If `reports/Txx-rN.md` exists → `gating`. Else the implementer died: relaunch round N with "the working tree may hold your partial work; inspect `git status`/`git diff` first". |
| gating | Check no VS Code test is running (§1), re-run the task gate. Green → `reviewing`. Red → write the failure into `reviews/Txx-rN.md` as `FIX-REQUIRED` (gate failure) → `changes-requested`. |
| reviewing | If `reviews/Txx-rN.md` exists, act on its verdict; else relaunch the reviewer. |
| changes-requested | N < 3: start round N+1 (implementer gets the task file + `reviews/Txx-rN.md`). N = 3: `blocked`. |
| done | Verify `git log --oneline` contains the commit; if missing (crash between commit and table update), check `git status`: staged/uncommitted work for Txx → commit it now. |
| blocked | Skip. |
| needs-approval | Ask the user at S6 (or at the phase start if S6 passed); approved → `todo`, refused → `dropped`. Never start it unapproved. |
| dropped | Skip; list it as an open item in the landing report. |

Commit (on APPROVE): `git add` only files listed in the report (never `.agents/changes/`, `out/`,
`node_modules/`), `git commit -F <msg file>` with the task's draft subject (≤ 71 chars), a body
of user-facing lines ≤ 79 chars, and the trailer `Assisted-by: Claude:Sonnet-5.5`. No
`Co-Authored-By`, no `Signed-off-by`. Check `git status` is clean afterwards (apart from
`.agents/changes/`, which is ignored).

Blocked rule: after round 3 is not approved, save `git diff > reports/Txx-blocked.patch` (plus
copies of new untracked files under `reports/Txx-blocked/`), restore the tree to HEAD for the
task's files only (`git restore --staged --worktree <files>`, delete the task's new files; never
`git clean -x`), mark `blocked`, note it in the journal, and continue with the next task whose
"Depends on" contains no blocked task. Dependants of a blocked task become `blocked (dep Txx)`.
At the phase checkpoint, list blocked tasks to the user.

## 7. Cross-cutting conventions (repeated in each task's rules)

- **Message registry (T03)**: `src/preview/previewMessages.ts` maps each new webview→host type to
  a validator; `isPreviewSyncMessage` (extension.ts:406) accepts registered types and ignores
  the generic edit fields for them. Unknown types are silently dropped.
- **Host→webview side channels**: posted with the current stage ids (the page drops others,
  `sameContext`, scrollSync.ts:309) and re-posted on every `previewReady` (extension.ts:2424),
  because a content patch replaces the content. The page re-applies decorations at the end of
  `initializeContent` (scrollSync.ts:3278), which runs on load and after each patch.
- **Shell stays stable**: `contentPatch.ts` compares everything outside
  `#sphinx-myst-preview-content`; toolbar markup must be identical across renders, and runtime UI
  (TOC, copy button, popovers) is created by the page script, not by the host HTML. View
  preferences live on `<html>` attributes set by the runtime (not in `runtimeContextKey`).
- **Inline style is blocked by CSP** (`style-src` nonce only): runtime styling uses CSSOM
  (`element.style.setProperty`), never `style="…"` markup.
- **Webview code**: `scrollSync.ts` is a template literal (doubled backslashes, `${}`); new logic
  goes into self-contained factory modules injected with `.toString()` (pattern: `textEditing.ts`,
  scrollSync.ts:56–58).
- **View preferences (T08)**: `src/state/previewViewPreferences.ts` holds zoom, widthMode, toc,
  incomingChanges in one workspaceState key; message `previewViewPreferenceChanged`.
- **Settings style (T02)**: every setting has `markdownDescription` (what it does, the effect of
  each value) and an `order`: preview reading 10–29, preview sync 30–39, editing 40–49, comments
  50–59, frontmatter 60–79, PlantUML 80–89. New keys: `preview.showComments` (T15),
  `preview.showIncomingChanges` (T16), `editing.defaultPaletteMode` (T23), `comments.authorName`
  (T43). Each also updates `test/security/package-contract.test.ts` and README "Settings".
- **CHANGELOG.md**: one user-facing bullet per feat/fix task at the top of `## Unreleased`
  (create the heading above `## 0.3.1` once).
- **No "Sphinx" in user-facing literals** of extension.ts, preview/webview.ts, render/*.ts.

## 8. Risk register

| # | Risk | Where | Mitigation |
| --- | --- | --- | --- |
| R1 | Template-literal escaping breaks the runtime silently (`\n` vs `\\n`, `${`) | scrollSync.ts | New code in factory modules; any edit inside scrollSync gets a webview unit test that executes the generated script (harness `createRuntimeHarness`, scrollSync.test.ts:331). |
| R2 | New message type not in the allowlist → dropped silently | extension.ts:406–540 | T03 registry + a unit test per new type; reviewer greps for every `postMessage({ type:` added. |
| R3 | Shell key changes per render → every keystroke reloads the page | contentPatch.ts:60–112, :164 | Static toolbar markup; runtime-created UI; preferences on `<html>` via runtime; `test/webview/contentPatch.test.ts` case per task that touches webview.ts. |
| R4 | Decorations lost after a content patch | applyContentPatch scrollSync.ts:254 | Re-apply in `initializeContent`; host re-posts on `previewReady`; tests patch then assert. |
| R5 | Edit lock / single active edit: atomic host edits racing an open editor | extension.ts:1603 pattern, editLock.ts | Refuse while `preview.activeBlockEdit` (message to user), disable UI while `activeBlockEdit`. |
| R6 | Blur commit trap: any focus loss saves and closes the block editor | scrollSync.ts:2769 | `mousedown` preventDefault on every palette control; relatedTarget-inside-palette exception; native dialog sets `suspendBlurCommit`. |
| R7 | Keyboard suites need an unlocked screen | realInput, checkboxToggle | §1 pending-unlock rule; E at phase end. |
| R8 | Visual geometry checks assume one toolbar row of 4 buttons, 56 px editor margin | capture.py:1471–1495, :1688 | T08/T09 update those checks explicitly; never weaken a check without saying why in the report. |
| R9 | Included blocks carry foreign end lines → wrong ranges for move/cut | mystRenderer.ts:645, :752 | T05 first; block operations refuse `data-sphinx-preview-included`. |
| R10 | Shortcut swallowed by the workbench (Cmd+K chord, Cmd+B) | webview key forwarding | preventDefault + stopPropagation; manual check (§9); fallback Cmd/Ctrl+Shift+K (D14). |
| R11 | Untrusted/readOnly paths: new host edits must refuse | extension.ts:2367 | Every new edit handler checks `preview.readOnly`; F gate for T19, T38, T43. |
| R12 | CRLF documents: textarea normalises to LF | move/cut/paste/insert | Pure helpers keep document EOLs; CRLF unit tests in every pure module. |
| R13 | `vscode.git` API absent or different | T16 | Optional adapter with a local minimal interface; feature off without it. |
| R14 | scrollSync.ts growth and harness cost (296 KB test file) | all webview tasks | New test files per module; extend the harness only where needed. |

## 9. Manual checks for the user at the end

1. Cmd/Ctrl+K, Cmd/Ctrl+B, Cmd/Ctrl+I and Ctrl+/ inside a block text box in real VS Code: the
   palette action runs, the workbench does nothing (no chord prompt, no sidebar toggle).
2. Alt+↑/↓ on macOS inside and outside the text box (Option+arrow word navigation still works in
   the text box; Ctrl/Cmd+Alt+↑/↓ moves there).
3. Margin Auto/Full on Windows with classic scrollbars: no horizontal page scroll; wide table
   edges not hidden under the scrollbar.
4. Copy-code and Cmd/Ctrl+C/X/V on blocks: the system clipboard holds the raw text.
5. Paste a screenshot from the OS clipboard into a block editor (image file written, alt
   selected).
6. Image picker: the native dialog opens in the document folder; the block editor stays open.
7. Incoming-change marks in a real repo after editing, staging and committing.
8. Zoom 70 %/200 % with the TOC open on a narrow and a wide pane; TOC hides on narrow panes.
9. rendering-difference-on-windows: provide a new screenshot (D28).
10. Keyboard suites if any phase closed while the screen was locked.

## 10. Decisions still open (planner defaults, applied unless the user objects)

- O1. Incoming-change setting vs toggle: `preview.showIncomingChanges=false` turns the feature
  off and hides the toolbar button; otherwise the per-workspace toggle (default on) decides.
- O2. Palette placement (U2): first child of the block-editor frame, above the text box, so it
  is created and removed with the editor and survives every path the editor survives.
- O3. Margin "Margin" state = the `maxContentWidth` setting; with the setting at 0 all three
  states look the same (button still cycles).
- O4. Zoom has no reset button; the tooltip shows the current percentage; 100 % is a normal step.
- O5. Back/Next records document jumps only in a preview that follows the active editor; a
  locked preview records in-page anchor jumps only.
- O6. TOC lists every rendered h1–h4 (including headings from `{include}`), excluding headings
  inside the properties table, admonitions and the sticky band; clicking scrolls to the element.
- O7. Chip expansion state is per panel (webview state), keyed by source line; not persisted
  across VS Code restarts.
- O8. Comments in a read-only (untrusted or outside-workspace) preview: threads shown, creation
  and changes disabled.
- O9. Multi-block selection: no Delete/Backspace action in v1 (U13 lists copy, cut, paste, move).
- O10. Diff marks and comment highlights are not shown inside an open block editor (the raw text
  box replaces the rendered block).
- O11. Figure "legend" (intent line 82) = the paragraphs after the caption inside the
  `{figure}` body (MyST/Sphinx legend); the figure editor edits source, alt, caption, legend,
  width, align and name. Other ideas offered: `:class:`, `:figwidth:` (not implemented unless
  approved).
- O12. Anchor rename (T29) changes only the `(label)=` line, not `{ref}` uses elsewhere; the
  status line says how many `{ref}` uses in the document still point to the old name.
- O13. Link panel (T22): Enter in the URL field inserts, Escape returns to the text box without
  inserting; an empty URL inserts `[text]()` with the caret inside the parentheses.

## 11. Intent traceability (P1 block-edition-palette `01-intent.md`, line → task)

| Line | Intent item | Task(s) |
| --- | --- | --- |
| 3 | Floating palette in edit mode ("below the existing one") | T21 (placement superseded by line 29 and U2: above the edited block) |
| 5–6 | Extensible, simple, harmony with the floating panel | T20 (action registry), T21 (shared look) |
| 8 | Every non-supported edition → new feature | §0 note (D13 superseded): T06, T27, T33 |
| 12 | Back | T11 |
| 13 | Next | T11 |
| 14 | Zoom in/out | T08 |
| 15 | Margin on/off | T10 (3 states, U5) |
| 17 | Split on 2 lines | T08 |
| 19–25 | Mode select strict / GFM / MyST | T23 |
| 29 | Placement on top of the edited block | T21 |
| 31–32 | Table cell: merge or shift | T35 (merge, U2) |
| 36 | Title dropdown h1–h5 | T21 |
| 37 | Italic | T20 (Cmd/Ctrl+I), T21 |
| 38 | Bold | T20 (Cmd/Ctrl+B), T21 |
| 39 | Strikethrough | T06 (render), T21 |
| 40 | Code fence + language dropdown | T21 |
| 41–42 | Link, Ctrl+K, selection = text, caret at URL | T22 |
| 43 | Blockquote | T21 |
| 44 | Horizontal rule | T21 |
| 45–46 | Table 9×9 grid, hover highlight, one click | T24 |
| 47 | Image file picker, default document folder | T31 |
| 48 | Emoji picker | T24 |
| 49 | HTML colour picker, self-activated on a colour code | T33 (render), T34 |
| 50–51 | TODO indicator (icon + hover text), Ctrl+/ | T20 (shortcut), T21 (button), T14–T15 (rendered chip) |
| 57–58 | GFM admonition `>` + type dropdown at the caret | T25 |
| 59 | Checkbox | T25 |
| 60 | HTML table: convert Markdown table, add new table | T25 |
| 62 | Propose others (GFM) | §3a, T26 (needs approval) |
| 67–68 | Inspect book/, curated MyST list | §3b, T30 (proposals, needs approval) |
| 72 | Admonitions all types + custom | T28 |
| 73 | Footnotes | T28 |
| 74 | Definition lists | T28 |
| 75 | Math (LaTeX) | T27 (amsmath render), T28 |
| 76 | Subscript / superscript | T28 |
| 77 | Figures, image with caption | T31, T32 |
| 78 | Anchors: icon where placed, click to edit | T27 (icon), T28 (insert), T29 (edit) |
| 82 | Figure custom editor (size, caption, legend, …), edit button or bar button | T32 |
| 83 | Colour picker, text + background | T34 |
| 84 | Emoji picker at the caret | T24 |
| 85 | URL panel: 2 fields, text prefilled, focus first empty | T22 |
