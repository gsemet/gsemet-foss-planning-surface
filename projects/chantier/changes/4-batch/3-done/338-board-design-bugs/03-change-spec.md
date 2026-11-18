# Change Specification: the board's drawer, Kanban priority chips and CR titles render correctly

## Goal

The UX QA of the board (`../board-design-realign/intake/ux-qa.md`, 2026-11-17) found four plain
bugs behind three of the user's complaints. The user split them out of `board-design-realign`
(design-Q1) to fix them first, in the running batch (batch-24):

1. **The CR drawer's file list.** Each file name shows in a grey box that overlaps its icon by
   6 px, and the sizes do not line up: the tree's `<span class="nm">` also matches the card band
   rule. The nested file's button class `ind` is also Triage's pill class (latent).
2. **The Kanban priority filter.** Each toggle draws the browser's 2 px outset button border and a
   grey square that means nothing.
3. **Front matter in the drawer.** A file that starts with `---` / `key: value` / `---` shows it as
   one paragraph ("--- type: cr-answers description: ... ---"). It must show as a muted key/value
   list.
4. **"---" titles.** A CR whose title file starts with a front matter is titled "---": 6 of the 8
   batch-24 CRs on Batch, PRs, Home's open PRs, Costs, the drawer's head and the CR board pane.

After this change the drawer's file list is a plain row per file (icon, name, size right-aligned)
with no box, the priority toggles have no border and no square, a front matter shows as a muted
key/value list above the document, and no title is ever "---". Every choice comes from
`02-answers.md` (design-Q1, the user's word, and bugs-S1 to bugs-S7, settled by the Chief of
Staff).

The code paths below are under `skills/chantier/scripts/cli/src/chantier/` (`<cli>`) and its
board page `<cli>/board/web/` (`<web>`), read at main `a65a8d3d`. The QA report's line numbers
are older than main's; this specification uses main's.

## What changes

### 1. The drawer's file list (bugs-S3)

- `<web>/js/panel/tree.js`, `button()`: the name's `<span class="nm">` becomes
  `<span class="fname">`; the nested file's button class `ind` becomes `nested` (the `on` class is
  unchanged).
- `<web>/css/panel.css`: `.panel .tree .ind` becomes `.panel .tree .nested`, and
  `.panel .tree .nm` becomes `.panel .tree .fname` (same declarations: ellipsis on one line). With
  the band rule no longer matching, the name has no margin, padding, fill or hairline, and the size
  (`.sz`, `margin-left: auto`) ends at the same x on every row.
- Not changed: the card band rule `.band, .meta, .nm` in `<web>/css/cards.css` keeps its `.nm`
  alias, still used by the Batch cards (`views/batch-graph.js`, `views/batch-pr-card.js`,
  `css/views/batch-graph.css`); Triage's `.ind` (`css/views/triage.css`) is unchanged.
- Check after the change: no other module of `<web>/js/panel/` writes `class="nm"` or `ind`, and no
  selector of `panel.css` still names `.tree .nm` or `.tree .ind`.

### 2. The Kanban priority filter (bugs-S4)

- `<web>/css/views/postit.css`, `.lbtn`: the toggle resets the browser's button look: `border: 0`
  and `font: inherit` (the existing `cursor: pointer` and small size stay; `.lbtn.on` is
  unchanged). The label filter (`js/labels/filter.js`), which uses the same `lab lbtn` button,
  loses its outset border too.
- The priority toggles (`js/labels/priority.js`, `priorityRow()`, buttons with `data-pf`) draw no
  `.lab::before` square: either a rule scoped to them (for example
  `.lbtn[data-pf]::before { content: none }`) or a class of their own instead of `lab`, at the
  Driver's choice, so long as the label toggles keep their label-coloured square and their look.
- Not changed: the on and off looks, the filter's behaviour (`bindPriority`, `priorityFilter`), the
  words.

### 3. Front matter in the drawer (bugs-S5)

- `<web>/js/panel/markdown.js`, `renderMarkdown(text)`: before the block loop, a leading front
  matter is read: after an optional BOM, the first line is `---` (trailing spaces allowed) and a
  later line is `---`; the lines between are the front matter, and the document resumes after the
  closing line. With no closing line there is no front matter and the text renders as today.
- It is drawn first, as a definition list: `<dl class="fm">`, one `<dt>` (the key) and `<dd>` (the
  value) per `key: value` line (the key is the text before the first `:`, the value the trimmed
  rest, run through `inline()` so it is escaped like the rest of the document). A line that is not
  `key: value` (an indented continuation, a `- item`, a bare word) joins the previous value with a
  space; a blank line is skipped. An empty front matter draws nothing.
- `<web>/css/panel.css`: `.panel .doc .fm` is a two-column grid (keys auto, values the rest), the
  small text size (`--text-small`), keys in `--ink3`, values in `--ink2`, no border, no fill, no
  chip, a gap below it before the document (`--space-3` or similar token). Values wrap
  (`overflow-wrap: anywhere`). Tokens only; no new colour.
- The editor ("Modifier") is not touched: it shows and saves the whole file, front matter
  included. The file's text sent to the editor is the raw text, never the rendered one.
- `markdown.js` stays under 300 lines and each function under Biome's limits (complexity at most
  10, at most 50 lines): the front matter reader is its own function.
- Not here: `type:` as a chip and `description:` as a lead paragraph (the report's target, in
  `board-design-realign`).

### 4. Titles (bugs-S1, bugs-S2)

**One rule, one helper.** A function `markdown_title(text) -> str` (name at the Driver's choice)
returns a document's title: the text with `\r\n` turned into `\n`, its leading front matter removed
by `FRONTMATTER` (the regex now in `<cli>/board/backlog.py:31`), then the first line that starts
with one to six `#` and a space, without its `#`s and spaces; with no such line, the first
non-blank line, `lstrip("# ").strip()`'d as today; with nothing, `""`. It lives, with `FRONTMATTER`,
in a module that `status/views.py`, `lifecycle/stages.py` and `board/backlog.py` all import with no
cycle (`board/backlog.py` already imports `status/views.py`): for example `<cli>/core/files.py`,
beside `read_text`. `board/backlog.py` then imports `FRONTMATTER` from there instead of defining
it. `plugin_files.py`'s own `FRONTMATTER` (agent files) is not touched.

**New titles.**

- `<cli>/status/views.py`, `_title(folder)`: for each of `TITLE_FILES`, `markdown_title` of the
  file; the first non-empty wins; the folder's name otherwise.
- `<cli>/lifecycle/stages.py`, `prepared_cr()`: `title = markdown_title(text) or directory.name`.
  So `open` and `add` record a real title, the branch name (`slugify(title)` in
  `commands/opening.py`) included.

**Titles already recorded.** The record is not rewritten. A helper, for example
`shown_title(recorded, folder)`, returns `recorded` unless it is empty or a front matter's opening
fence (`recorded.strip() == "---"`), and then `_title(folder)` (when the folder is known and
exists; `recorded` otherwise). It is used wherever a recorded title is served:

- `<cli>/status/views.py`: `cr_view` (`"title"`, which `STATUS.json` and the drawer's head show),
  `_row`, `_past` (`s.get("title")` read from an archived `STATUS.json`), `_done_rows`.
- `<cli>/board/crs.py`, `_row`: `subject(shown_title(c.title, folder))`.
- `<cli>/history.py`, `cr_entry` (the closed batch's record written at `close`, read by Costs'
  history): the title shown, the CR's folder resolved from its `path` as the caller allows (pass
  the repository or the resolved title in; the Driver picks the least intrusive way).
- Any other place found by a search for `c.title`, `"title"` and `get("title")` under `<cli>/`
  that serves a CR's recorded title to the board, a STATUS file or a record; the Driver lists them
  in the PR. Prompt lines and CLI messages (`commands/facts.py`, `commands/driver.py`,
  `commands/opening.py`'s output) get the helper too where the folder is at hand; where it is not,
  they stay as they are, and the PR says so.

`board/prs.py` and the board's pages (Batch, PRs, Home, Costs, the drawer's head) read the titles
from these views, so they need no change of their own.

### Words, cards, docs

No new user-facing string, no card change, no docs change. `just docs-screenshots` is not owed by
this CR (by hand, before a release).

## Out of scope

- Everything else in the QA report: the side bar, unboxing columns, lanes, blocks and rows, the one
  chip, filter chip and segmented control, the type scale and radii, the drawer's head and facts
  row, the file list as a grid with folder captions, the phone tree and file picker, the clipped
  gate line on the Batch PR cards, the Costs KPI tiles and receipt, Configuration's repeated
  values, the language mix and its rule: all in `board-design-realign`.
- Scoping or removing the card band rule's `.nm` alias; the on/off look of the filter toggles.
- Rewriting a recorded title in `batch.json`, `STATUS.json` or an archive.

## Evidence

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; `just test`
stays within its budget):

- `markdown_title` (one parametrized test, for example in `test_board_description.py`): a heading
  after a front matter; the same with a BOM and with CRLF; a front matter then a heading-less line
  (that line); a heading below a paragraph (the heading); only a front matter (`""`); no front
  matter (as today); an unclosed `---` then a heading (no front matter: the heading).
- `_title` and `prepared_cr`: a CR folder whose `03-change-spec.md` starts with a front matter gives
  the heading's text, and `open` records it as the CR's title.
- `shown_title`: a recorded `---` with the folder present gives the folder's title; a recorded real
  title is kept; a recorded `---` with no folder stays `---`.

**The board's page** has no JS unit tests: `just lint` (Biome on `<web>`) and
`tests/test_code_targets.py` check the touched JS and CSS; the screenshots below prove the render.

**Screenshots** (bugs-S7): before (main at the CR's base) and after (the PR's head), on the same
data, side by side in the PR's Deliverables, at the QA's desktop size (1440x900), with no username
or home folder in view:

1. The drawer, with a file that has a front matter open (a CR's `02-answers.md` or
   `03-change-spec.md`) and the file list in view, own files and a sub-folder's: before, the boxed
   names and "--- type: ... ---"; after, plain rows with aligned sizes and the key/value list.
2. The Kanban's priority row ("Priorités"): before, the outset borders and grey squares; after,
   neither. The label filter's row too, if it is shown on the same page.
3. The Batch page on batch-24, whose CRs showed "---": after, their real titles (bugs-S2, with no
   record edit). Optionally PRs or Costs as well.

**The CR board pane** (bugs-S6, AGENTS.md): the PR's Deliverables carry one screenshot of the pane
from a real Claude Code session running the PR's head (`claude --plugin-dir <worktree>`, as
CONTRIBUTING.md says), captioned with the head's SHA (seven characters), showing a batch-24 CR's
real title where main shows "---". Until it is there, Known gaps names it ("no screenshot of the
pane from a real session"), so the ready line quotes it.

**Gates** (AGENTS.md):

- Before the first push, the Driver runs `just check` in the worktree at the rebased head it pushes,
  and `just eval-dry-run` there (the change is under the CLI's `src/`).
- The long gate: the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head (a CLI
  change). No scenario step is added: the title rule and the shown title are covered by the tests
  above; the scenario must stay green.
- Windows coverage: if this CR is on top of batch-24's stack, it also passes `just scenario`
  locally (`chantier gate`) at its head before the user merges; when a CR joins on top, that local
  run moves to it.
- `just mod` is not owed: nothing under `hooks/` or `types/` changes.

## Open questions

None.
