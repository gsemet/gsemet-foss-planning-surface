# Task T1 (CR 201): Studio in the VS Code Agents window

Worktree (only place to edit): `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-201`,
branch `change-requests/201-agents-window-support`. Rules: [rules.md](rules.md). Read
`.agents/constitution.md` and `requirements/guidelines/requirements.guidelines.md` (in the worktree)
first. Background and evidence: [03-spike-report.md](03-spike-report.md) and
[04-implementation-plan.md](04-implementation-plan.md) in this PRD folder (absolute path:
`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/03-requests/201-agents-window-support/`).
Repository content stays in English; never link to `.agents/changes/` from the repository.

## Context

VS Code's Agents window (a companion window for agent sessions) disables any installed extension
with code that does not declare `capabilities.agentsWindow.supported` in its manifest. A spike on
VS Code 1.144 proved the declaration alone enables Studio there. Inside that window the active
agent session's working directory is mounted as the workspace folder with
`updateWorkspaceFolders`, and replaced or removed on every session switch. Two gaps follow:

- Gap 1: a preview opened while no folder holds its file is read-only, and stays read-only after
  the folder is added. `HostEvents.onFoldersChanged` (`src/session/hostEvents.ts`) only watches
  stems; `PreviewManager.refreshTrust` (`src/session/previewManager.ts`) already holds the
  promotion logic but runs only when trust is granted.
- Gap 2: when a folder is removed, `onFoldersChanged` calls `disposeSession(session, true)` for each
  session in that folder, which closes the Studio tab (SwRS-MDOKFSTUDIO-LIFE-143).

## Change

1. **Manifest** (`package.json`): add `"agentsWindow": { "supported": true }` under
   `capabilities`, beside `untrustedWorkspaces`. Make sure `scripts/generate-settings.mjs` keeps it
   (`just check-settings` and `just generate-settings` leave no diff). No `engines.vscode` bump.
   New `proposed` SwRS via `okfreq new` (LIFE scope, see the requirements guideline for the exact
   command): the manifest declares Agents window support so VS Code enables Studio there without a
   user setting. Test: assert the declaration, next to the existing `untrustedWorkspaces` manifest
   assertion (`test/security/trustReq.requirements.test.ts`) or in
   `test/host/lifeReq.requirements.test.ts`, with `@tests_req`; mark `@implements_req` where the
   project marks manifest-only requirements (follow how TRUST-001 does it).
2. **Mount promotes** (gap 1): extract the loop of `refreshTrust` into one `PreviewManager` method
   used by both `refreshTrust` and `onFoldersChanged` (when `added` is not empty). Same panel,
   reading state kept, active preview stays active, previews outside the added folder untouched.
   Update SwRS-MDOKFSTUDIO-TRUST-001 (or a new LIFE SwRS if clearer) with this behaviour.
3. **Unmount keeps the tab read-only** (gap 2, user decision): for a session whose workspace folder
   was removed, replace it on the same panel with a read-only session (resource root = document
   directory, no session roots) instead of disposing it. Render queue, watchers and Problems
   entries tied to the old session are still disposed, so no late result reaches the panel. A
   later added folder that holds the file promotes it again (step 2). Update
   SwRS-MDOKFSTUDIO-LIFE-143 (`proposed`): removing a folder no longer closes the panel. Update its
   tests, including `test/integration/workspaceDisposal.test.ts` if it asserts the panel closes;
   explain every changed assertion in the report (constitution, section 3).
4. **Docs**: `docs/user/open-studio.md`, add a short section on the Agents window: open a `.md`
   with Open With → Markdown OKF-Schema Studio; files of the active agent session are editable;
   other files open read-only; switching sessions keeps the tab, read-only until its folder is back;
   for a VS Code build that ignores the manifest declaration, the user setting
   `"extensions.supportAgentsWindow": { "GaetanSemet.markdown-okf-schema-studio": true }` or Agent
   Customizations → Extensions. `docs/known-limitations.md`: remote or cloud agent sessions
   (non-`file` folders) are not supported. `CHANGELOG.md` under the unreleased section (follow its
   existing style). Add "Agents window" to `.agents/glossary/common.md`. Check whether
   `README.md` or `docs/user/README.md` lists where Studio opens; add a line only if so.

## Tests first

Write the tests before the code and confirm each fails on the unchanged code (report the failure):

- manifest declares `capabilities.agentsWindow.supported === true`;
- a read-only preview (no workspace folder) becomes editable on the same panel when
  `onFoldersChanged([folder], [])` adds a folder that holds its file; the active preview stays
  active; a preview of a file outside that folder stays read-only;
- removing the folder of an editable preview keeps the same panel open, read-only, with its old
  session's resources disposed; adding the folder back makes it editable again.

Use the existing fake host and session test helpers in `test/session/` and `test/host/`.

## Gates (run in the worktree, foreground)

- `just compile`
- targeted unit tests for the touched files while iterating (`npm run test:unit` is acceptable)
- `just requirements-update`, then `just requirements-lint`
- `just check` (formatting, types, boundaries, file sizes, exports, markers, settings, unit,
  contracts, security, release tests, requirements lint): must pass

Do not run `just preflight`, e2e or integration suites (the driver runs them). Write your report to
`reports/T1-r<n>.md` in the PRD folder.
