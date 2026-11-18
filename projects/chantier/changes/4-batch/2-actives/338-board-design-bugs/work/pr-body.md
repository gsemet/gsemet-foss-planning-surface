## Summary

The board had four plain rendering bugs. In a change request's drawer, each file name sat in a grey box that overlapped its icon and the sizes did not line up. The Kanban's priority filter toggles drew the browser's outset button border and a meaningless grey square. A file starting with a front matter (`---` / `key: value` / `---`) showed it as one run-on paragraph. And a change request whose title file starts with a front matter was titled "---" on the Batch, PRs, Home and Costs pages, in the drawer's head and in the CR board pane.

## Deliverables

Before (base `5b86c93`) and after (head `7b8b87c`), 1440x900, on the same made-up demo data. The drawer, with a file that has a front matter open: boxed names and run-on front matter before; plain rows with aligned sizes and a key/value list after.

| Before | After |
| --- | --- |
| ![Drawer before](../evidence/before-drawer.png) | ![Drawer after](../evidence/after-drawer.png) |

The Kanban's priority and label rows: outset borders and grey squares before; neither after.

| Before | After |
| --- | --- |
| ![Kanban before](../evidence/before-kanban.png) | ![Kanban after](../evidence/after-kanban.png) |

- Drawer file list: plain row per file (icon, name, size right-aligned), no box; the tree's name class is `fname` and the nested file's class is `nested`, so the card band rule and Triage's pill class no longer match.
- Priority filter: no border (`border: 0`, `font: inherit` on `.lbtn`) and no square on the priority toggles (`.lbtn[data-pf]::before { content: none }`); the label toggles keep their coloured square.
- Front matter: drawn first as a muted key/value list.

```text
markdown_title(text)   core/files.py   front matter removed, first '#' heading, else first non-blank line
shown_title(recorded, folder)          a recorded "---" is replaced by the folder's title
```

## Blast radius

Grade: **1**. Local to the board's CSS and JS and to how a title is read; the record is not rewritten. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The shown title is applied to the closed batch's history at the point where the close step builds its CR entries (`commands/close_archive.py`), so `history.py` stays untouched: it is the least intrusive way to hand it the folder's title.
- The front matter reader treats a line as `key: value` only when it starts with a word character, so a `- item` line joins the previous value.
- A request filed in the inbox takes its slug from the same title rule, so a request with a heading below a paragraph is slugged from that heading, as a CR's title is.

## Known gaps

- No screenshot of the "---" titles: the demo data records real titles, so the title fix is proven by its tests only.
- No screenshot of the pane from a real session.
- `opening.py`'s CR lists (`open` and `add` output) still print a CR's recorded title as recorded, so a title recorded as "---" before this change still shows there; `seat.py` and `summary.py` hold no CR title.

<details>
<summary>Details</summary>

## Changes

- `board/web/js/panel/tree.js`, `css/panel.css`: class renames; front matter list styles.
- `board/web/js/panel/markdown.js`: `readFrontMatter`, drawn as `<dl class="fm">`.
- `board/web/css/views/postit.css`: priority toggle look.
- `core/files.py`: `FRONTMATTER` (moved from `board/backlog.py`) and `markdown_title`.
- `status/views.py`, `lifecycle/stages.py`, `lifecycle/backlog.py` (a filed request's slug), `board/crs.py`, `commands/close_archive.py`, `commands/facts.py`, `commands/driver.py` (prompt lines): new title rule and `shown_title`.
- `tests/test_titles.py`: parametrized tests for the rule, `_title`, `shown_title` and `open`.

## Human decisions

- The quick fixes (drawer file list, priority chips, front matter display, "---" titles) are split out of the wider board realignment and delivered first, on their own.

## Impacts

The drawer, the Kanban priority row and every CR title read correctly; no new string.

## Test plan

- [x] New or changed tests (they fail on the previous code): `tests/test_titles.py`
- [x] Local gates carried from `7b8b87c`: `just check` (484 passed), `just eval-dry-run` (17 of 17)
- [x] Evidence: before at `5b86c93`, after at `7b8b87c`
- [x] Review: approved carried from `7b8b87c`
- [x] Verified carried from `7b8b87c`
- [x] CI green at `7b8b87c`: all five jobs pass, `just scenario (ubuntu-latest)` included

## Internal references

- CR-338, batch-24; specification in the CR's folder (`03-change-spec.md`, `02-answers.md`).

</details>
