# Before and after

- Before (base faa4719): the board has no PRs page; no capture is possible (the view does not
  exist). `just test`: 262 passed in 49.75s.
- After (head 0141856a18873984c4687b72eaab1b39fb38cc4f): `evidence/prs-page.png` in the CR folder,
  the PRs view from a real board with `scenario/fake_gh.py` as `gh` (PR 12 merged, 15 conflicting,
  16 draft, 17 `mergeable: UNKNOWN`). `just test`: 300 passed in 50.14s.
- Reproduce: from the worktree, a scratch copy of `docs/demo/` made git by
  `scripts/docs_screenshots.py` (`make_surface`, `start_board`), `FAKE_GH_STATE` pointing at a
  state file with `{"prs": {...}}`, a `gh.cmd` first on PATH running `scenario/fake_gh.py`, then
  Playwright opens `?p=shop-api&v=prs`.
- Not captured: a page on a real forge.
