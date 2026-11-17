# T1 — Parallel CI jobs driven by `ci-*` justfile targets

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-024 (branch
`ci/parallel-jobs`, from origin/main b74afe2). Work ONLY there; `node_modules`
and `.venv` are symlinks to the main checkout: never delete or stage them.
Read `00-request.md`, `rules.md` and `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/guidelines/ci.guidelines.md` (the rules
this change must satisfy).

## Change

1. `justfile` (keep its style; `just format` must leave it unchanged):
   - `dev-ci`: non-interactive CI setup from lock files: apt plantuml + graphviz (`sudo -n`, only
     when not already present or only on Linux, so it does not break on macOS), `npm ci`,
     `uv sync --group docs --group release`, `playwright install --with-deps chromium`.
     Use the `npm` variable (CI sets STUDIO_NPM). No fnm in CI (setup-node provides node).
   - `ci-static`: format check (`just format` then `git diff --exit-code -- justfile`), check,
     sphinx-check.
   - `ci-visual`, `ci-integration`: the two e2e stages, each standalone, each writing its reports
     under `out/reports/`. They must share a campaign identity so `ci-report` can merge them: read
     `scripts/run-e2e.mjs` and `test/integration/review-index.ts`; let each stage reuse a campaign
     given through the existing env vars (`STUDIO_E2E_RUN_ID`, `STUDIO_E2E_STARTED_AT`,
     `STUDIO_E2E_COMMAND`) or create one when absent (local run). Keep `npm run test:e2e` (and its
     unit tests in test/build or test/site, grep `runCampaignStages`) working unchanged.
   - `ci-report`: merge the stage outputs (review:finish → e2e manifest/junit) and fail if a stage
     manifest is missing or failed.
   - `ci-gallery`: gallery + site from existing e2e outputs (no e2e re-run).
   - `preflight`: same coverage as today, by calling `clean`, then `ci-static`, `ci-visual`,
     `ci-integration`, `ci-report`, `ci-gallery` in sequence, continuing after a failure and
     reporting the failed count like today.
2. `.github/workflows/ci.yml`:
   - jobs `static`, `visual`, `integration` (under `xvfb-run --auto-servernum`), each: checkout
     (lfs) + `git lfs pull`/`fsck` if still needed, setup-node (`.nvmrc`, npm cache), setup-uv,
     setup-just, `just dev-ci`, `just ci-<name>`, upload `out/reports/` as a per-job artifact
     (`if: always()`).
   - The campaign identity is set once for the workflow (env from `github.run_id` /
     `github.run_attempt`, a fixed started-at from the run) so both e2e jobs share it.
   - job `report` (needs visual + integration, `if: always()`): download both artifacts into
     `out/reports/`, `just ci-report`, upload the merged reports.
   - job `gallery` (only when `workflow_dispatch` input `gallery: true`; needs report): download,
     `just ci-gallery`, upload.
   - job `checks` (needs static, visual, integration, report; `if: always()`): fails unless all
     needed jobs succeeded. `tag-release` keeps `needs: checks`.
   - Keep `on:`, permissions, tag-release/release/pages untouched otherwise. Do not touch
     pages.yml/release.yml.
3. README/CONTRIBUTING/AGENTS.md: list the new targets where targets are documented (AGENTS.md
   "Main targets").

## Gates (foreground)

`npx tsc -p .`, `just --fmt --check --unstable` or `just format` + `git diff --exit-code -- justfile`,
`just ci-static`, `just ci-visual`, then `just ci-report` with only the visual output present must
fail clearly (integration missing), and with a faked passing integration manifest it must pass (do
this in a temp copy of out/reports, then restore). `just --dry-run ci-integration` and
`just --dry-run dev-ci` to show the commands. Do NOT run `just dev-ci` (it installs), `ci-integration`,
`just preflight` or anything opening VS Code windows. If `actionlint` exists locally, run it.
CI proves the rest.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/024-ci-parallel-jobs/reports/T1-r<round>.md`.
