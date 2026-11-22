# Before and after: dropdown directive in the preview

Before: 1a5b98bbf84b76a3306bc362d10b506ce79d77e5 (origin/main, detached worktree, removed). After: 18a2ea9c8ad9b7d767037bdaf32352bda750d654.

Source: evidence/source.md (colon dropdown closed, backtick dropdown with `:open:`, untitled dropdown).
Reproduce: compile the tree, `node --import ./scripts/register-myst-patches.mjs evidence/render-dropdowns.cjs <root> <outdir>`, then `uv run --no-sync --group docs python evidence/shot-dropdowns.py <outdir> <prefix> <imgdir>` (renders with the real renderer, the preview theme CSS and the light and dark theme variables; the admonition CSS of the Sphinx theme is not loaded, so the details are drawn by the browser default).

| Pair | Shows |
| --- | --- |
| evidence/before-light.png, before-dark.png | three empty `<details></details>`: only the browser's "Details" label, no body |
| evidence/after-light.png, after-dark.png | titles "Closed colon dropdown" (closed), "Open backtick dropdown" (open, body shown), "Details" (untitled, closed); body of each in the DOM with data-line mapping |

Pictures show no user name or home path (no path on screen).
