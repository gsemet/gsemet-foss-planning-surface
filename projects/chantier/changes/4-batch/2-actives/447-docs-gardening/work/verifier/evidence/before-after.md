# Before and after

Before: base 5691a05d (git history; no detached worktree made, the docs diff is in the PR). After: 4c9943619983b8d91c0a3a3d317961214a89e2ce.
Pairs: renders of the changed SVGs in svg-verifier/ (reproduce: `uv run --no-project --script work/check_svgs.py <worktree> <out> --render`); the PR's `docs/web-board/*.png` are the after pictures, each looked at (see verify.md). The before pictures are `git show 5691a05d:docs/web-board/<file>`; no pair image was kept beyond that.
