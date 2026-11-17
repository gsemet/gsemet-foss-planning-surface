# CR 135 tasks

Integration branch `change-requests/135-audit-security-performance-pack` in `../markdown-okf-schema-studio-wt-135`. Order T1 → T26.

| Task | Status | Round | Commit | Integrated |
| --- | --- | --- | --- | --- |
| [T1](tasks/T1-myst-tightness.md) | ready | 1/3 | 6b792ce3 | e215ed3e (note: shared main-checkout node_modules/markdown-it-myst/dist/directives.js left patched; revert denied, for the user) |
| [T2](tasks/T2-plantuml-jar-profile.md) | ready | 3/3 | aaa07448 | 0c75030f |
| [T3](tasks/T3-sidecar-symlink.md) | ready | 2/3 | 771520be | 9dd67df5 |
| [T4](tasks/T4-sanitizer-hardening.md) | ready | 2/3 | b89cd2cd | 99a3de14 |
| [T5](tasks/T5-single-parse5-pass.md) | ready | 2/3 | d78e2d25 | ad3dbec3 |
| [T6](tasks/T6-visibility-shared-render.md) | ready | 2/3 | 65f696a1 | a1d59c9a |
| [T7](tasks/T7-drop-retain-context.md) | ready | 2/3 | 91622deb | 46412914 (no green ci-stress 3 (alert-dropdown/frontmatter-rename timeouts, also on unchanged code); reload suite green) |
| [T8](tasks/T8-restricted-settings-capabilities.md) | ready | 2/3 | 13a64d23 | 5593083c (note: previewEditing real-window suite not run) |
| [T9](tasks/T9-supply-chain-ci.md) | ready | 1/3 | e86401d0 | 95c81b6a (note: local just check: requirements-lint fails on stale .venv okfreq only (uvx 0.13.0 passes); --ignore-scripts only in release package job) |
| [T10](tasks/T10-vsix-contents.md) | ready | 2/3 | 43bf5a7f | 4a578e6f |
| [T11](tasks/T11-content-addressed-caches.md) | ready | 1/3 | 87c977c2 | 0712337f (bench ratio noise (0.43 to 0.48); highlight stage 50ms to 2ms) |
| [T12](tasks/T12-plantuml-jar-cache.md) | ready | 1/3 | b769e3ea | 03cd9d76 (note: just check fails only at requirements-lint update-coverage, 274 files baseline; SwRS validate 0 errors) |
| [T13](tasks/T13-event-fan-out.md) | ready | 2/3 | d1521a25 | 78be1fe9 |
| [T14](tasks/T14-stable-morph-keys.md) | ready | 1/3 | 07e8d0e4 | 40f4c45d (conflict in codeCopy.test.ts and SwRS LIFE-069 resolved keeping both intents) |
| [T15](tasks/T15-page-plantuml-queue.md) | ready | 2/3 | 168d5741 | 668f8e1e |
| [T16](tasks/T16-frontmatter-once.md) | ready | 1/3 | e6808ee7 | 54c76b5b (parse count 4 to 1, new test; unit green) |
| [T17](tasks/T17-bundle-trims.md) | ready | 1/3 | d8340349 | 19a5d720 (esbuild.mjs conflict kept T21 patch plugin + T18 worker; worker now shares lazy shiki/katex: extension.js 1.46 MB, renderWorker.js 3.59 to 1.02 MB) |
| [T18](tasks/T18-render-worker.md) | ready | 2/3 | 5af9b0f1 | 6b7b4a1c (SwRS LIFE-004 no collision; log/CHANGELOG conflicts kept both; bench: host stall 344-1627 ms to 6-14 ms) |
| [T19](tasks/T19-logger-port.md) | ready | 1/3 | 62ca444d | 0b4630be (CHANGELOG and frontmatter.ts import conflicts resolved keeping both) |
| [T20](tasks/T20-shared-syntax-primitives.md) | done | 1/3 | 0d13dee1 | f69d1c73 |
| [T21](tasks/T21-postinstall-patch.md) | ready | 2/3 | b92343c4 | faaf1254 (log.md conflict kept both; lock root specs match package.json, node_modules versions 1.7.4; removed stale out/ test js) |
| [T22](tasks/T22-lifecycle-typing-nits.md) | ready | 1/3 | 2f68de01 | 0c5cefc9 (SwRS TOOLBAR-079 conflict resolved keeping both scenarios) |
| [T23](tasks/T23-split-realinput-tests.md) | done | 2/3 | 6440f39d | 4a223496 (package.json conflict: new unit glob plus --import patch hook) |
| [T24](tasks/T24-boundaries-debt.md) | done | 1/3 | 286d7704 | b64fbafd |
| [T25](tasks/T25-unused-exports-sphinx.md) | ready | 1/3 | 940aec8b | 31e56e02 (allow-list reasons refreshed; still needed) |
| [T26](tasks/T26-split-large-modules.md) | ready | 1/3 | c9ae70d9 | 43c7eea8 (just check green; PR #144) |
