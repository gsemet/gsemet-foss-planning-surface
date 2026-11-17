# Implementation plan

For the CR that picks this item. Read [the constitution](../../../../constitution.md) and
`requirements/guidelines/requirements.guidelines.md` first; this plan does not restate them.
Branch at pick time: `change-requests/NNN-agents-window-support` from fresh `origin/main` (NNN =
next free number, 201 on 2026-10-29). Grill questions with recommended answers:
[02-decisions.md](02-decisions.md).

## T1: declare Agents window support (manifest)

- `package.json`: add `"agentsWindow": { "supported": true }` under `capabilities`, beside
  `untrustedWorkspaces`. Check that `scripts/generate-settings.mjs` (it rewrites
  `capabilities.untrustedWorkspaces.restrictedConfigurations`) keeps the new key; run
  `just generate-settings` and confirm no diff.
- Requirement: `okfreq new` a `proposed` SwRS in the LIFE scope: "The extension SHALL declare
  support for the VS Code Agents window in its manifest, so that VS Code enables it there without
  a user setting." Mark `@implements_req` where the manifest is checked, as TRUST-001 does for
  `untrustedWorkspaces`.
- Test first: a manifest assertion beside the `untrustedWorkspaces` one in
  `test/security/trustReq.requirements.test.ts`, or in `test/host/lifeReq.requirements.test.ts`,
  with `@tests_req`. It fails on the current manifest.

## T2: a mounted folder promotes read-only previews (gap 1)

- `src/session/hostEvents.ts`, `onFoldersChanged`: after the watchers, when `added` is not empty,
  call the promotion that `refreshTrust` already performs. Extract the shared loop in
  `src/session/previewManager.ts` into one method (for example `promoteReadOnlySessions()`), used
  by both `refreshTrust` and `onFoldersChanged`, and keep `refreshTrust` as the trust entry point.
  The method keeps the reading state and the active preview, as today.
- Requirement: extend SwRS-MDOKFSTUDIO-TRUST-001 (or create a LIFE SwRS if the reviewer prefers):
  a read-only preview whose document falls in a newly added trusted workspace folder becomes
  editable, on the same panel, with its reading state.
- Tests first (`test/session/`, with the fake host): a preview opened with no folder is read-only;
  `onFoldersChanged([folder], [])` makes it editable; the same panel; the active preview stays
  active; a preview outside the added folder stays read-only.

## T3: an unmounted folder keeps the tab, read-only (gap 2)

Only after grill question 1 is answered (recommended: keep the tab).

- `onFoldersChanged`: for a session whose folder was removed, replace the session with a
  read-only one on the same panel (resource root = document directory, no session roots) instead
  of `disposeSession(session, true)`. The watchers, render stages and Problems entries tied to
  the folder are still disposed (LIFE-143 resource part).
- When a later `added` folder holds the file, T2 promotes it again: the round trip covers a
  session switch and the switch back.
- Requirement: update SwRS-MDOKFSTUDIO-LIFE-143 (`proposed`): a removed folder no longer closes
  the panel. Run `okfreq` impact and the test markers of LIFE-143. Update
  `test/integration/workspaceDisposal.test.ts` and state in the PR why the assertion changes
  (constitution, section 3).
- Tests: unit tests for remove → read-only and same panel, then add → editable again; resources
  of the old session disposed (no late render reaches the panel).

## T4: documentation

- `docs/user/open-studio.md`: a section "In the Agents window": Open With → Markdown OKF-Schema
  Studio; files of the active agent session are editable; other files open read-only; workaround
  for builds that ignore the declaration: `"extensions.supportAgentsWindow": {
  "GaetanSemet.markdown-okf-schema-studio": true }`, or Agent Customizations → Extensions.
- `docs/known-limitations.md`: remote or cloud agent sessions (non-`file` folders) are not
  supported; the Anchor button stays disabled without a text editor of the file.
- `CHANGELOG.md` under Unreleased. Writing skill: no change (no rendered syntax changes).
- Add "Agents window" to `.agents/glossary/common.md`.

## T5: proof and gates

- `just requirements-update`, then a dated entry in `requirements/tiers/log.md`.
- `just check`, then `just preflight` (completion gate).
- Manual evidence for the PR: replay the spike (`spike/spike.mjs`, variants v2 and v5, then v6)
  with the CR's VSIX. Expected: v2 still shows the bug without the declaration, v5 shows Studio,
  v6 phase 2 is editable, and phase 4 keeps the `second.md` tab read-only. Attach the v5
  screenshot to the PR Impacts section through the `-assets` branch.

## Risks

- Upstream churn: the Agents window gate is experimental (`enableAgentsWindowCapability`,
  `agentsWindowManagement`). Re-check the declaration on the current VS Code build at pick time
  with spike variant v5.
- File size: `previewManager.ts` is 560 lines (limit 800); the extraction in T2 must not grow it
  much.
- T3 changes behaviour in the main window too (removing a folder keeps the tab). This is intended,
  but the PR must call it out for an external reader.
