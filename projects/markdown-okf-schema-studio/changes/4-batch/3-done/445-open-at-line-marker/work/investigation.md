# Investigation CR-445 (read-only, worktree at 590b2c52)

## 1. Map (spec statements checked against the code)

Confirmed as the spec says: `StudioActivation.start` (`src/host-vscode/activation.ts`, 351 lines) does the
warm-up, `watchStemRoot`, `diagnostics.start()`, the `conf.py` watcher and all registrations in one
block; `resolvePreviewEditor` has no selection; no `ConfigurationTarget` in `src/`; `getConfiguration(`
read only in `vscodeHost.ts` (395 lines); `activationEvents` holds 4 entries; `SETTING_CATEGORIES` has 5
sections (order 1..5); `scrollCore.ts` 583 and `pageRuntime.ts` 743 (both in `src/page/features/`);
`KeyValueStore` exists (`src/host-api/keyValueStore.ts`); `Navigation` has only `showDocument` and
`openExternal`; `onLanguage` is refused by `test/security/lifeReq.requirements.test.ts` line 14;
`settingsRegistry.test.ts` lines 144-160 hold the `ConfigurationTarget` assertion.

New files (spec 4.x): `src/core/navigation/openingPolicy.ts`, `src/core/configuration/editorAssociationMigration.ts`,
`src/host-api/settingScopes.ts`, `src/host-vscode/openInStudio.ts`, `src/session/associationMigration.ts`,
`src/session/featureIntroductions.ts`, `src/page/features/lineMarker.ts`, a styles file, `test/visual/lineMarkerScenarios.ts`.
Touched: `activation.ts`, `vscodeHost.ts`, `hostToPage.ts` + router, `hostHandlers.ts`, `rendering.ts`,
`scrollSync.ts`, `links.ts`, `history.ts`, `navigation.ts`, `host-api/index.ts`, memory host,
`settingsRegistry.ts`, `package.json` (generated settings, commands, menus, activation), `testHooks.ts`,
`test/host/fakeVscode.ts`, `test/shared/testProfile.ts`, `test/shared/e2eGroups.ts`, `run-tests.ts`.

## 2. Spec statements that disagree with, or are not backed by, the code at 590b2c52

1. `isDocumentEligible` (`sessionDocuments.ts:27`) takes a `HostDocument` and tests only the `.md`
   extension of `document.path`; it does not test the scheme. The spec feeds it as a policy fact "eligible
   saved `file:` `.md`": the watcher must also test `scheme === "file"` (and that `host.documents.of(doc)`
   gives a path for `git:`/`untitled:`; unverified, check first).
2. The `KeyValueStore` doc comment says "for the workspace"; 4.5 needs the global state. Port is
   unchanged but the comment (and `WorkspaceChoices` wording) must be corrected.
3. `test/host/fakeVscode.ts` `tabGroups` is a `strict({...})` object (line 410) with no `onDidChangeTabs`,
   `close`, `all` with real tabs, and no `TabInputTextDiff`/`TabInputTextMerge` classes (only Webview,
   Custom, Text); `getConfiguration` has `inspect` returning `undefined` and no `update`. The spec only
   names `inspect`/`update`: the watcher host tests need the tab API faked too (larger than stated).
4. `stop()` calls `manager.diagnostics.stop()`, `disposeStemRootWatchers()` and `previewRenderer.dispose()`
   unconditionally; with 4.8 lazy start these must be guarded ("stops only what was started").
   Also `onWorkspaceFoldersChanged` (`manager.events.onFoldersChanged`) may add stem-root watchers
   before `ensureServicesStarted` ran: to read in `src/session/hostEvents.ts` when coding (not verified).
5. `startKeystrokeTracking()` and `manager.choices.refreshThreadAuthor` run at activation today; spec 4.8 does
   not say where they go (keep at activation: cheap, but then "starts only the watcher and the migration"
   in SwRS-LIFE-001 text is slightly untrue; say "registrations").
6. 6.3 / 6.1 say trials run "on Windows locally" with the existing harness: CONTRIBUTING.md "Windows"
   says the visual and real VS Code stages run on Linux and macOS only; `just integration` also needs
   bash for `_require-unlocked-screen`. See section 5.
7. `experiments/0N-diff-view-*` (the model for "driving a real window with Playwright over CDP") are in the
   planning folder, hard-wired to `C:/Users/gaeta/Projets/studio-grill-diff-view` and `Code.exe`; nothing of
   them exists in the repo.
8. Spec 6.4 cites `toolbar-navigation/v37` in `scenarioDefinitions1.ts`; not verified (not needed).

## 3. Smallest change, risks

The smallest change is the spec itself; only trims: keep SettingScopes optional (already), merge
`studioTargetFor` and the policy in one test file, keep T11 signal "none" as default (rule 3 exception off)
unless T11 proves it cheaply; no separate `lineMarkerStyles.ts` if an existing styles file has room.

Risks: (a) `onLanguage:markdown` makes every existing integration/host test that assumed an inactive
extension change (stockCoexistence diff, LIFE-001 tests, tests that count activations); (b) File-size
ratchet 800 lines: `activation.ts` 351 and `vscodeHost.ts` 395 grow, keep logic in `openInStudio.ts` and the
core; (c) unused-exports check and import-boundary check on the new core/host-api files; (d) every
`Navigation` implementer and test fake must add `showDocumentInStudio` (search `showDocument:` in `test/`
and `src/host-memory`); (e) requirements: 11 new SwRS + 1 StRS, edits to LIFE-001/004/018/149/156, CORE-001
and markers move with `just requirements-update`; (f) the default of `searchResultsInStudio` depends on T2
(decision 22): coding it `true` then flipping costs a `generate-settings` re-run and doc edits, so the
flip must be one constant; (g) visual and real-window stages do not run on Windows (see 5).

Questions only the user can answer: none (the spec is decided).

## 4. Slicing into 3 rounds (the round limit; each gate-green alone: `just check`, requirements update/lint)

The spec's natural 6 slices (A settings, B migration+intros, C activation split, D page marker,
E watcher+policy, F navigation+Open as Text+docs) are merged pairwise.

**Round 1: configuration, migration, introductions, activation, "Open as Text".** (A+B+C+Open-as-Text)
- Files: `settingsRegistry.ts` (+`open` section, `just generate-settings` -> `package.json`),
  `host-api/settingScopes.ts` + index, `vscodeHost.ts` (`createVscodeSettingScopes`),
  `core/configuration/editorAssociationMigration.ts`, `session/associationMigration.ts`,
  `session/featureIntroductions.ts`, `activation.ts` (`ensureServicesStarted`, global state, migration
  call, commands `openAsText`, `showFeatureIntroductionsAgain`), `testHooks.ts`, `package.json`
  (`onLanguage:markdown`, two commands, `editor/title` menu, `commandPalette`), a small registry of
  "text editors Studio opened" in `openInStudio.ts` (the watcher itself comes in round 3),
  `docs/known-limitations.md` activation sentence.
- Tests: `editorAssociationMigration`, `associationMigration`, `featureIntroductions`, `settingScopes`
  (fakeVscode: `inspect`, `update`), changed `settingsRegistry` (ConfigurationTarget list) and
  `lifeReq.requirements` (activation events, new title), `package-contract` (commands), host test
  (no preview starts no service; first preview starts once).
- Requirements: StRS + SwRS for migration, introductions, Open as Text, settings (defaults), activation;
  edits to LIFE-001/004/149/156 and CORE-001; log entry. Settings do nothing yet except migrate:
  honest, settings descriptions must not claim more than they do until round 3 (or accept: one PR).
- Evidence: unit output; T5 and T6 (campaign) can run at the end of round 3; optionally the T6 launch
  here.

**Round 2: marker in the page, placement, Studio's own navigation.** (D+E-placement+F-navigation)
- Files: `core/protocol/hostToPage.ts` (+router), `page/features/lineMarker.ts`, `hostHandlers.ts`,
  hooks in `scrollCore.ts`/`pageRuntime.ts` (<= 800), core styles, `session/features/scrollSync.ts`
  (`postPendingRevealLine`), `rendering.ts`, `activation.ts` (`resolvePreviewEditor` consumes the pending
  line), `openInStudio.ts` (the "put Studio in place" function and `studioTargetFor` in
  `openingPolicy.ts`), `host-api/navigation.ts`, `vscodeHost.ts`, memory host/test fakes, `links.ts`,
  `history.ts`.
- Tests: protocol, `runtimeLineMarker`, session pending-line, session navigation, `studioTargetFor`;
  `test/visual/lineMarkerScenarios.ts` (light/dark; real captures only on Linux CI or by the page
  runtime harness locally).
- Requirements: SwRS marker placement/lifetime/edit mode, navigation SwRS.
- Evidence: visual captures, before/after (the "before" is the unchanged page: no marker).

**Round 3: policy, watcher, trials, docs.** (E-watcher+G)
- Files: `openingPolicy.ts` (truth table), `openInStudio.ts` watcher (`onDidChangeTabs`...), wiring in
  `start`, `test/integration/openAtLine.test.ts`, `openAtLineCampaign.ts`, `run-tests.ts`,
  `testProfile.ts`, `e2eGroups.ts`, `stockCoexistence.test.ts` (+ no Studio tab), docs
  (`open-studio.md`, `settings.md`, `known-limitations.md`), glossary, `CHANGELOG.md`, SwRS for the
  never-replaced list and for jump/plain opening, decision 21/22/26/28 outcomes (known issues, default
  flip).
- Tests: `openingPolicy.test.ts`, integration trials.
- This is the heaviest round: run T2 first (it fixes the default and the signal), then the rest.

If a round would not fit, the first thing to cut is the `openAtLineCampaign.ts` automation of T11 (do
T11 by hand and record), not any SwRS.

## 5. Evidence plan

Kind: user-visible behaviour in VS Code and in the page (marker), plus settings and a manifest.

- Page marker: screenshots from `test/visual` scenarios (light, dark, high contrast); the "before" is the
  same scenario without `previewRevealLine`. These stages run on Linux/macOS CI; locally on Windows the
  page runtime tests (`test/page`) run, screenshots only through CI's report artefact.
- Real VS Code trials (T1 to T13): the repo's own harness (`run-tests.ts` + `trusted-suite.ts` over CDP,
  `@vscode/test-electron`) is documented as Linux/macOS only. It has Windows code paths (`runIsolation.ts`
  short temp root, `run-e2e.mjs` `npm.cmd`), but nothing says it passes on Windows: the coder should try
  `npm run test:integration -- ` (not `just integration`, which needs bash) once in round 1 and report. The
  proven Windows route is the exploration style (VS Code `Code.exe` from outside, Playwright `connectOverCDP`,
  isolated user-data/extensions dirs) used by `experiments/01..04`: it needs the extension built (`just
  compile`) and loaded with `--extensionDevelopmentPath`.
  - Feasible locally on Windows through that route: T1 (flash duration), T2, T3, T4, T5, T7, T8, T9, T10,
    T12, T13 (all drive one window, settings via `settings.json` or `getConfiguration().update`).
  - T6 and T11 (campaign: settings files written before launch, reload, read back from disk): feasible on
    Windows by the same outside route (they launch their own windows); the in-repo `openAtLineCampaign.ts`
    should reuse `reload-suite.ts`, and is verified on CI Linux.
  - T11's "extension inactive at launch" needs `onLanguage:markdown` to have been the only activation:
    check by the absence of the Studio output channel or `extensions.getExtension(...).isActive` through
    the extension host: no API from CDP, use the DOM output channel list.
  - Not shown locally: Linux behaviour (heavy CI `gh workflow run ci.yml --ref <branch> -f heavy=true`),
    macOS, Web, Remote, Agents window, merge editor and multi-file "Open All Changes" (unit only, as the
    spec says). Keyboard timing T1/T5 numbers are Windows-specific; record the OS.
- Settings/manifest: `just generate-settings` diff of `package.json`, `just check` output.
- Migration: the before/after contents of the user and workspace `settings.json` (T6 log files, kept as
  `*.log`, with a screenshot of the notice).
- Docs and requirements: `just requirements-lint` output.
- Gate: `just check`, `just requirements-update`, `just requirements-lint`; `just preflight` on Windows is the
  static stage only (AGENTS.md); the visual and integration stages go to CI on the branch.
