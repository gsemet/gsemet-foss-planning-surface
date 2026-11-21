# Before and after (CR-441)

Before: base 8d99cd1e393fac6a7e978f442c1af80b1e5831e9 (detached worktree, `npm run compile`, okfreq report).
After: head 5abb7af1a61d1cd6eee1115148adbe8ac7f470de.

Pairs: `before/<ID>-<desktop|narrow>.png` and `after/<ID>-<desktop|narrow>.png` for BLOCK-003,
FMSCHEMA-014, BLOCK-014, MYST-006, REVIEW-012, MYST-009 (map box only, made-up paths: none shown),
with `metrics.txt` (map size, overlap count) in each folder. desktop = 1280 px, narrow = 800 px.

Reproduce: `npm run compile`; `uv run --no-sync --group requirements okfreq generate-report requirements
--output-json out/reports/requirements/requirements-report.json --output-summary-md
out/reports/requirements/requirements-report.md`; `node work/shoot.cjs <tag>` (copied under `out/graphlab/`
so its root resolves to the worktree). `probe.cjs` measures page overflow and joined states.
