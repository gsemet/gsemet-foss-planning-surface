# Before and after (CR-480, raw copy)

Before: base 80d482fddaeb659b251070b96ae66b0e2066c4bd (origin/main, detached worktree, with only the
branch's `test/visual` capture files copied in, since the base has no such check).
After: head c01042578e1fa0248761c1286fa33c336de63794.

Reproduce (from the worktree to test): `npm run visual:render`, then
`uv run --no-sync --group docs python work/verifier/dump_capture.py <out.json>` (wraps the
`capture_raw_copy.py` check of scenario `block-editing/v55-raw-copy-light-900` and records, for each copy it makes, the
browser's own selection text, `defaultPrevented`, text/plain and text/html). Home paths in the JSON are rewritten to `user`.

| File | What it shows |
| --- | --- |
| `before-cases.json` | 13 copies on the base page: `defaultPrevented` false for all, text/plain empty (nothing sets it); `browserSelectionText` is what the native copy gives: `Name\tValue\none\tfirst\ntwo\tsecond` (tab-separated cells, no `---`, no `**`) |
| `after-cases.json` | the same 13 copies at the head: cases 1-11 prevented with text/plain the raw source (case 2: `Intro with **bold** and a [link with **strong** words](...) here.\n\n---\n\n\| Name \| Value \| ...`), text/html rendered; case 0 (no source text sent) and case 12 (edge in an old-side card) not prevented, as specified |
| `after-selection-over-frontmatter.png` | the fixture with the last selected range highlighted (frontmatter table to the intro); no path or user name visible |

Not captured: the clipboard cannot be drawn on a screenshot; context-menu Copy, macOS, rich-editor paste, mouse drag and
text/html in the real VS Code window are not claimed.
