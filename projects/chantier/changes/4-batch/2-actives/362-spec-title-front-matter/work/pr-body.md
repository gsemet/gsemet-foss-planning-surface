## Summary

A Change Specification can start with a YAML front matter (`---`, `type: ...`, `---`). The board's panel drew that front matter as a key/value list above the document. This change hides it: the panel's Markdown view skips a leading front matter and starts at the first line after the closing `---`. The title side was already fixed on main: every reader of a CR's title goes through one function, `markdown_title`, which takes the first heading after a front matter.

## Deliverables

- The panel no longer draws a front matter: no `---`, no `type:` line, no key/value list. The raw-text editor still shows and saves the file as it is.
- Rule for a front matter (same as the Python side): `---` on the first line (optional BOM, trailing blanks allowed), closed by the next `---` line. With no closing line, nothing is a front matter and the text renders as before.

```js
// board/web/js/panel/markdown.js
function readFrontMatter(lines) {
  if (!/^﻿?---[^\S\n]*$/.test(lines[0] ?? '')) return 0;
  const end = lines.findIndex((line, i) => i > 0 && /^---[^\S\n]*$/.test(line));
  return end < 0 ? 0 : end + 1;
}
```

Panel output for a document that starts with a `type: cr-spec` front matter (rendered by `renderMarkdown`, Node 24.19.0):

| Input | Before, at `5717626` | After, at `f1792cd` |
| --- | --- | --- |
| front matter, heading, paragraph (plain, BOM or CRLF) | `<dl class="fm">` key/value list, then the heading and paragraph | heading and paragraph only |
| empty front matter | heading only | heading only |
| unclosed `---` | text as is | text as is |
| no front matter | heading and paragraph | heading and paragraph |

Shipped-file checks (Node 24.19.0, `renderMarkdown` imported from the file): plain, BOM and `\r\n` front matter render only the heading and the paragraph; an empty front matter renders only the heading; an unclosed one and a text without any render as on main.

## Blast radius

Grade: **1**. A display change in one JS function and three removed CSS rules; `git revert` restores the previous panel.

## Autonomous decisions

- The closing-line match uses `[^\S\n]*` instead of `[ \t]*`, because the linter refuses `\t` in a regular expression; it also accepts other blank characters.

## Known gaps

- No screenshot of the panel from the running board yet.

<details>
<summary>Details</summary>

## Changes

- `board/web/js/panel/markdown.js`: `readFrontMatter` is a plain skip returning the first line after the front matter, or 0; the key/value parsing and `<dl class="fm">` markup are removed.
- `board/web/css/panel.css`: the three `.panel .doc .fm` rules are removed.
- A search of the CLI's sources found no other reader deriving a CR's title outside `markdown_title`.

## Impacts

The panel's body starts at the document's first heading. No other visual change.

## Test plan

- [x] No behaviour change in Python; existing title tests unchanged (19 title and description tests pass at `f1792cd`)
- [x] Local gates at `f1792cd`: `just check` (601 passed), `just eval-dry-run` (17 of 17)
- [x] Evidence: before at `5717626`, after at `f1792cd` (renderMarkdown output table in Deliverables; no panel screenshot, see Known gaps)
- [x] Review: approved at `f1792cd`
- [x] Verified at `f1792cd`
- [x] CI green at `f1792cd`: `gh pr checks 326`, all 5 jobs pass

## Internal references

- CR-362 spec-title-front-matter
- Evidence files (not uploadable): `work/verifier/evidence/node-before.log`, `node-after.log`, `before-after.md`

</details>
