# A front matter is never a CR's title, and the board's panel hides it

## Goal

Some Change Specifications start with a YAML front matter (`---`, `type: ...`, `description: ...`,
`---`). The user saw `---` instead of the title in `open`'s CR list and in `brief.md` (batch-24:
CR-324, 325, 326, 329, 330, 331, 332), and in the board's panel. There the panel's title read
`---` and the body showed the front matter as plain text. What the user wants:

- a CR's title comes from the first Markdown heading after the front matter, wherever chantier
  reads that title;
- the board's panel does not show the front matter at all.

chantier only reads a front matter. It never writes one and never requires one.

## Where main stands (read at `5717626d`)

Commit `c9e645c1` ("fix(board): render the drawer, priority chips and CR titles correctly",
2026-11-17) landed after batch-24 and already fixed most of the title side:

- `chantier/core/files.py`: `FRONTMATTER` (one leading front matter, optional BOM, `\n` or `\r\n`)
  and `markdown_title(text)`. That function returns the first heading after a leading front
  matter, or else the first non-blank line without its `#`s, or else `""`.
- `chantier/lifecycle/stages.py` (`prepared_cr`, which `open` uses): `title = markdown_title(text)
  or directory.name`. The title `open` records, the `open` output lines
  (`commands/opening.py`, `f"{c.id} {c.title[:40]}: ..."`) and `brief.md` (`_brief_text`) all
  come from that recorded title.
- `chantier/lifecycle/backlog.py` (`idea_slug`) uses `markdown_title`.
- `chantier/status/views.py`: `_title(folder)` reads `TITLE_FILES` through `markdown_title`.
  `shown_title(recorded, folder)` replaces a recorded `---` (written by an older `open`) or an
  empty title with the folder's own title. Its callers are `views.py` (rows, backlog, summaries,
  done CRs), `board/crs.py` (the panel's and cards' `title`), `commands/driver.py`,
  `commands/facts.py` and `commands/close_archive.py`.
- `chantier/board/backlog.py` (`description`) skips a front matter before it takes the card's text.
- Tests: `tests/test_titles.py` and `tests/test_board_description.py`.

What is still open:

1. **The panel's body.** `board/web/js/panel/markdown.js`, `readFrontMatter`, draws the front
   matter as a muted key/value list (`<dl class="fm">`, styled in `board/web/css/panel.css`,
   `.panel .doc .fm`, `.fm dt`, `.fm dd`). The answers rule that it is hidden, and not shown as a
   table or a list either.
2. **One shared function, confirmed.** No reader of a CR's title may bypass `markdown_title`
   (directly, or through `_title` / `shown_title`). The investigation found none outside the list
   above. The Driver confirms this at its head and routes any new reader it finds through
   `markdown_title`.

## What changes

### Board panel (`skills/chantier/scripts/cli/src/chantier/board/web/`)

Read `board/web/DESIGN.md` first, as `AGENTS.md` asks, and keep it true. It names no front matter
style today, so no line of it should need to change. If it does name one at the head, remove that
line.

- `js/panel/markdown.js`: `renderMarkdown(text)` skips a leading front matter and draws nothing
  for it. The rendering starts at the line after the closing `---`.
  - A front matter is recognised by the same rule as `core/files.py`'s `FRONTMATTER`. It starts on
    the first line: `---`, optionally after a BOM, with optional trailing spaces or tabs. It ends
    at the next line that is `---`, with optional trailing spaces or tabs. An empty front matter
    (`---` right after `---`) is hidden too.
  - Without a closing `---`, nothing is a front matter, and the text renders as it does today.
  - `readFrontMatter` becomes a plain skip that returns the index of the first line after the
    front matter, or 0. `KEY_VALUE` and the `<dl class="fm">` markup go.
  - Update the comment above the function to say that the front matter is hidden.
  - Biome (`just check` runs `biome check` on `board/web`) must stay clean, with no unused import
    or constant left behind.
- `css/panel.css`: remove the three `.panel .doc .fm` rules, since nothing draws `.fm` any more.
- Unchanged: the panel's `<h2>` title (`js/panel/head.js`, `title(target.title)`). It already
  comes from the server's `shown_title`. The board's Markdown editor (the drawer's raw-text edit)
  keeps showing and saving the front matter as it is: the user edits the file's own text.

### Title readers (Python, `skills/chantier/scripts/cli/src/chantier/`)

- No behaviour change is expected. `markdown_title` stays the one function that turns a document's
  text into a title.
- At the head, the Driver searches `src/chantier/` for any other code that derives a CR's title
  from a file's first line or first heading, for example `lstrip("#")`, `startswith("#")`, or the
  first line of `splitlines()` applied to a CR file. Each one it finds goes through
  `markdown_title` (or `_title` / `shown_title` when it holds a recorded title).
- Out of this search: the agent files' own front matter (`plugin_files.py`) is not a CR's title,
  and `board/backlog.py`'s `description` is a body, not a title.

### Cards and docs

None. No card describes the panel's front matter or how a title is read.

## Decisions carried from `02-answers.md`

- A CR file that starts with a YAML front matter takes its title from the first Markdown heading
  after it. Every reader of a CR's title does so: `open`'s CR list, `brief.md`, the board's panel
  and any other reader the investigation finds, through one shared function (`markdown_title`).
- The board's panel does not render the front matter. It is hidden, not shown as a table (and so
  not as the key/value list main draws today).
- chantier writes no front matter and requires none.
- No spec critic: this is a display fix with no role behaviour behind it.

## Out of scope

- Writing, requiring, validating or using a front matter's keys (`type`, `description`) anywhere.
- Rewriting titles already recorded as `---` in past batches' records. `shown_title` already shows
  the folder's title in their place.
- The front matter of the plugin's agent files (`agents/`, `com.github.copilot/agents/`) and
  `plugin_files.py`'s own `FRONTMATTER`.
- The board's Markdown editor, which keeps the raw text.
- The CR board pane (`hooks/register.tsx`): it shows `STATUS.json`'s titles, which already go
  through `shown_title`. This CR changes no `STATUS.json` field, so the pane screenshot rule does
  not apply.

## Evidence

- **Tests (`just test`, in-process, fast):**
  - Keep `tests/test_titles.py` and `tests/test_board_description.py` green, unchanged.
  - If the Driver routes a newly found title reader through `markdown_title`, add a
    `pytest.param` to the parametrized case of `test_titles.py` that covers that reader with a
    front-matter file. Add no new test file.
- **The panel's rendering, on the shipped file:** the check reads
  `board/web/js/panel/markdown.js` from the repository at the head under test, not a copy. Before
  the push, the Driver runs it with the justfile's pinned Node (`uvx --from nodejs-wheel==24.19.0
  node --input-type=module -e "..."`, importing `renderMarkdown` from the shipped path by file
  URL) on these inputs, and reports each output in the PR's Deliverables:
  - `---\ntype: cr-spec\ndescription: x\n---\n\n# Title\n\nText.\n`: the output holds the heading
    and the paragraph, and contains neither `type`, `cr-spec`, `description`, `<dl` nor `---`;
  - the same input with a BOM and with `\r\n` line endings: the same result;
  - `---\n---\n# T\n`: only the heading;
  - `---\ntype: x\n\n# Heading\n` (no closing fence): rendered as today, front lines included;
  - a text with no front matter: unchanged from main's output.

  If `markdown.js`'s imports (`core/dom.js`, `core/format.js` and `model/words.js` behind it) do
  not load under Node, the Driver says so in the PR. It then proves the same cases in the running
  board instead, as below, and names the gap in Known gaps. It does not add a Node test harness to
  the repository.
- **The board, by hand:** with `chantier board` serving the head, open a CR whose
  `03-change-spec.md` starts with a front matter (for example one of batch-24's, in `5-done`, or a
  backlog CR given one in a scratch copy of the planning surface). The panel's title is the first
  heading, and its body starts with that heading, with no `---`, no key/value list and no
  `type:` line. Put one screenshot in the PR's Deliverables, captioned with the head's short SHA.
- **`open` and `brief.md`:** already covered by
  `test_a_title_behind_a_frontmatter_is_found_recorded_and_shown`, which checks the recorded
  title. The `open` output line and `brief.md` both print that recorded title.
- **Gates:** `just check` (pytest, ruff, biome) at the rebased head, and `just eval-dry-run`,
  because the change is under the CLI's `src/`. The pipeline's `just scenario (ubuntu-latest)`
  job must be green at the PR's head.

No host or default matrix: nothing here depends on the host or on a configured value.

## Open questions

None.
