# Report — audit-security-performance-pack

Status: **done** (2026-10-28, branch `change-requests/135-audit-security-performance-pack`, PR #144, merge commit d978725a).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | perf(render): split source lines once per parse in markdown-it-myst tightness patch | d53fa42a |
| T2 | fix(security): run the PlantUML JAR with a restricted security profile and size limit | d0e24539 |
| T3 | fix(comments): refuse symlink sidecar and write it atomically | 655467e4 |
| T4 | fix(security): harden the HTML sanitizer | f72e0783 |
| T5 | perf(preview): single parse5 pass per page build | 7c738cca |
| T6 | perf(session): render hidden previews on show and share one render per document | 763c5bc3 |
| T7 | perf(vscode): stop retaining hidden preview webviews | fea7212f |
| T8 | fix(security): restrict frontmatter path settings and gate page-callable capabilities | 7886cda0 |
| T9 | ci: audit production deps, pin actions to SHAs, scope job permissions | 0e79e872 |
| T10 | build(vsix): leave source maps, docs, .claude and pyproject.toml out of the package | 8b5a4acc |
| T11 | perf: bounded content-addressed caches for highlight, KaTeX, toctree and schema listing | a6c28602 |
| T12 | perf(plantuml): cache SVG by source hash and cap concurrent JVMs at 2 | a6cc858b |
| T13 | perf(page): stable morph keys, single-flight layout, throttled code-copy placement | 1bae10f4 |
| T14 | perf(page): drop superseded PlantUML runs in the page queue | 12df2923 |
| T15 | perf(frontmatter): parse front matter once per unchanged text | 19308d76 |
| T16 | perf: cut event fan-out with shared watchers, canonical dependency sets and a stem index | d92ad5f6 |
| T17 | refactor: Logger port and fireAndForget replace console calls and unobserved promises | 7f3e85ad |
| T18 | refactor: share fence, front-matter and escape primitives in src/core/syntax | 7e2cd102 |
| T19 | fix: dispose comments watcher, unobserve rescan links, bound dismissed banners, type paste events | 6abe5726 |
| T20 | perf(render): render MyST in a worker thread with cancellation and adaptive debounce | 773a8569 |
| T21 | build: apply the MyST source patches in memory instead of patching node_modules | 376340fc |
| T22 | test: split realInput suite into test/integration/realInput/ | b963b829 |
| T23 | perf(bundle): lazy-load highlighting and KaTeX, one YAML library, split Mermaid build | 99bb7e27 |
| T24 | chore: add unused-exports check to just check and remove dead exports | b4e6b6ae |
| T25 | refactor: retire session to node-services boundary debt behind host ports | 006b6407 |
| T26 | refactor: split the 700+ line modules into focused files | a22f96f9 |
| T27 | fix(build): apply the MyST source patches to the render worker bundle | 89aa967b |
| T28 | test: apply the MyST source patches in the bundle test and ignore JAVA_HOME in the missing-java test | 62ccd471 |
| T29 | fix(test): measure render times on the host harness clock, not the wall clock | d978725a |

## Proof of completion

- Merged by the user through gh stack #161 (`gh stack merge`, 2026-10-28 08:01). Normal CI (static, visual, checks) green on the PR; heavy CI: 40640634459 (integration and stress green).
- 26 tasks, each one commit, integrated in order on the integration branch; CI fixes added 3 commits (worker bundle MyST patch, hermetic bundle and missing-java tests, harness render clock).
- Benches: extension.js 4.28 MB -> 1.46 MB; renderWorker.js 3.59 MB -> 1.02 MB; host-thread stall during a render 344-1627 ms -> 6-14 ms; front-matter parses per build 4 -> 1; foreign document change with 50 sessions 1.5 ms -> 0.18 ms; PlantUML second render of the same source spawns 0 JVMs; churn subscriptions 153/303/453 -> 0.
- Requirements traceability: `reports/TRACEABILITY.md` (86 IDs touched, 0 gaps); `just check` green with the CI okfreq (okf-schema 0.13.0), 2893 unit tests.
- Task reports and reviews in `reports/` and `reviews/`; task table in `TASKS.md`; PR body in `reports/PR-BODY.md`.

## Open items

- Local real-window suites were not all run (screen locked overnight); heavy CI is the proof.
- `scenarioAlertDropdown` fails often in the full real-window sequence, with or without the change (T18 report): candidate backlog item.
- The main checkout's `node_modules/markdown-it-myst/dist/directives.js` was left patched by T1 (revert denied); `npm ci` in the main checkout restores it.
- Audit report folder archived here (`backlog-audit-performance-security-maintainability/`); closed by CRs 132, 133, 135 and 137.
