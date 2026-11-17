# Task T2 — PlantUML JAR: security profile and limits

Audit finding(s): S-03, CR 3 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t2`, branch `change-requests/135-t2-plantuml-jar-profile` (local only, from origin/main).

## Scope

Run the JAR with `PLANTUML_SECURITY_PROFILE` (the strictest profile that keeps local `!include` inside the allowed root working), `-DPLANTUML_LIMIT_SIZE`, and an explicit `java` resolution. `src/core/render/plantUmlRenderer.ts`. Proof: spawn-stub test on env and args.

## Definition of done

- The change above; a test that fails on the unchanged code; benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync.
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.
