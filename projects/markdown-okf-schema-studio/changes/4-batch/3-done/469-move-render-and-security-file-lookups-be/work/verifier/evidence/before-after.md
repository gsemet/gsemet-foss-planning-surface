# Before / after (no screenshots: internal refactor)

Before: origin/main d9b3cd6bef9659f401b24337159691b7306fe907 (detached worktree, compiled). After: 2d7152e32a028f64683841bb27f7b93b23017a1a.

Pair 1: rendered HTML + diagnostics + dependencies of one fixture (conf.py with colon_fence/deflist/dollarmath, toctree glob, include, local image, image outside root, include outside root, junction to outside folder). `diff -r` of both outputs: identical.
Pair 2: renderMs, 15 runs: before median 7.59 ms (min 6.30), after median 10.36 ms (min 7.78). About +3 ms on a small fixture.

Reproduce: `node mkfix.cjs <ws>`; `node --import ./scripts/register-myst-patches.mjs parity.cjs <out dir> <ws> <outdir> [head]`. Paths in the raw meta.json hold the local home folder; only render.html (path-normalised, no username) is kept.
