# Report — 045-plantuml-js-engine

Status: **done** (2026-10-23, branch `feat/plantuml-js-engine`,
[PR #39](https://github.com/gsemet/markdown-okf-schema-studio/pull/39), rebase-merged 15:43Z by the
main session on user decision 11; main at 7149d6d).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 r1 | Built-in `@plantuml/core@1.2026.9` engine bundled into the webview (Smetana layout, no CSP change), `plantuml.useJar` setting, enabled in Restricted Mode, clear message for unsupported features | 9a3f293 (bea997f on main) |
| T1 r2 | `{uml}` / `{plantuml}` file form read by the host; local `!include*` via a page-to-extension message (8 levels, 64 files, 1 MiB per diagram, cycles refused, Restricted Mode = document folder, watched dependencies); URL/stdlib/`!import`/`!theme from` still refused | 87bd13c (7149d6d on main) |

## Proof of completion

- 2/3 rounds, reviewer APPROVE both (r2 minors only).
- Local after rebase: tsc clean, unit 1982/1982; visual scenarios count 310.
- CI: PR [run 39979301259](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/39979301259) pass (checks, static, visual, report).
- Screenshots (built-in engine, `{uml}` file, nested include, light and dark, unsupported message) on `pr-assets/39`.
- Dependency added with `--package-lock-only` + unpack into the shared node_modules (no prune).
- Autonomous decisions 1–10 listed in the PR body.

## Open items

- The on-demand real VS Code window job was not run on this PR (CSP and include round trip in a real webview unchecked).
- Follow-ups: built-in engine errors not reported as host diagnostics; include request ids restart at 1 per page load (`src/webview/scrollSync.ts:257`); missing-file watch ignores symlinks; include files served up to 5 MiB vs 1 MiB diagram cap.
