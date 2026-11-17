# Report — 286-release-pr-body-shows-notes

Status: **done** (2026-11-11). PR #355 merged as `ec205a69`.

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | `release-process.guidelines.md`: "The version PR body" section (rendered notes and thread after `---` rules and headings, LFS image links, review loop on the delivered files); step 5 points to it | `ec205a69` |

## Proof of completion

- Snippet run as written on the 1.6.1 notes at `96a86e46`: both images 200 `image/png`, `Image:` line rendered, attribution last.
- `test/build/`: 169 passed. CI green at `76465b38` (static, static-windows, visual, checks, report).
- No visible change (process text).

## Open items

- First use: the next version PR (1.6.2 or 1.7.0).
