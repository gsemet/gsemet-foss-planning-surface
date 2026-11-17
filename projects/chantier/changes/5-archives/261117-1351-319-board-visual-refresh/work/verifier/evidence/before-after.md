# Before / after pairs (CR-319)

Before: the base commit b9daeff, `git show b9daeff:docs/web-board/<view>-<size>.png` (committed pictures).
After: the head 9bb941f374df58ab4b5412125f14d61ee452debc, `work/verifier/shots.py` (Playwright, Chromium, board started by
`docs_screenshots.make_surface` / `start_board` over a scratch copy of docs/demo, `/api/board` intercepted by the
head's `fix_surface_path` so every path is made up: `/home/demo/...`). Same viewports as docs_screenshots (1400x860, config pc 1400x1500, phone 375x812).

| Pair | before | after |
| --- | --- | --- |
| Batch pc | before-batch-pc.png | after-batch-pc.png |
| Batch phone | before-batch-phone.png | after-batch-phone.png |
| Costs pc | before-costs-pc.png | after-costs-pc.png |
| Costs phone | before-costs-phone.png | after-costs-phone.png |
| Configuration pc | before-config-pc.png | after-config-pc.png |
| Configuration phone | before-config-phone.png | after-config-phone.png |

Every image was opened and looked at: no username, no home folder, only made-up paths (`/home/demo/shop-api`, relative `projects/shop-api/`).
Reproduce: `uv run --script <CR folder>/work/verifier/shots.py` from the CR's worktree (shots.py, shots2.py, shots3.py; facts in facts*.json).
Not captured: the side by side with the four `prototypes/01-mockups/final-*.html` (belongs to the description pass).
