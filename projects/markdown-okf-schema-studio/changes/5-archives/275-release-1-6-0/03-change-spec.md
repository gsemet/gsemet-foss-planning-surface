# 275 Release 1.6.0

## Owner's request

Release 1.6.0 (a minor), agreed with the owner on 2026-11-10.

## Scope

The stack is on main (HEAD ecb368e9 after #341):

| CR | PR | Change |
| --- | --- | --- |
| 268 | #337 | Tab/arrow leaves a table cell showing stale content |
| 269 | #338 | A wide table no longer narrows while a cell is edited |
| 270 | #339 | Inline Markdown hardening in cells (snake_case, `2 * 3 * 4`, `//host`) |
| 272 | #340 | Inline SVG pictures: `svg` fence or raw `<svg>` block (issue #336) |
| 273 | #341 | Front matter values `= this.field` (issue #334) |

Highlights: inline SVG pictures and `= this.field`. CR 274 stays queued until the release is published.

## Decisions

- Hold every other merge. Never comment on GitHub issues, never touch auto-merge.
- Version PR opened as a draft, marked ready when its checks are green.
- Nothing irreversible (tag, publish, merge of the version PR) before the owner approves notes and thread.
- Hero image: a dedicated showcase scenario is welcome; an existing capture is acceptable.
