# Before and after (CR-318, head 2ca565e1, base 30fd3f52)

Pairs (before = detached worktree of 30fd3f52, after = head 2ca565e1), 1800 px full-page captures:
- v06 expanded light 900, v10 expanded dark 900, v18 expanded cream 900 (the 5 rows of 3 before, 4 rows of 4 after).
- v07, v11, v19 collapsed (light, dark, cream) at 900.
Files: before/ and after/, same names.

Reproduce, in each worktree after `just dev`:
  npm run visual:render
  uv run --no-sync --group docs python test/visual/capture.py --scenario toolbar-navigation/v06-toolbar-expanded-light-900 (and v07, v10, v11, v18, v19)
PNGs land in out/reports/e2e/screenshots/visual/toolbar-navigation/.
Not captured as images: 360 px, white and cream 360 scenarios (checks ran, no screenshot).
