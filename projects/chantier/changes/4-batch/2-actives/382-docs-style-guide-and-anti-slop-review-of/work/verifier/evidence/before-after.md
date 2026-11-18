# Before / after

- gates-before.png: docs/how-to/gates.md built at the base 22519166ff4d3c1ac13b156d1ce455c2de193cbb (detached worktree).
- gates-after.png: same page built at the head 787400ea5f95752e6383e7e54878cc23b3fffba7.
- Reproduce: `UV_PYTHON=3.13 uv run --locked --group docs sphinx-build -q -W -b html docs docs/_build/html`, then headless Chrome `--window-size=1200,2600 --screenshot=<png> file:///.../docs/_build/html/how-to/gates.html`.
- Look: both opened; show only page text (made-up commands), no username or home folder.
- Read the Docs preview: not captured (not a listed check; no RTD check on the PR).
