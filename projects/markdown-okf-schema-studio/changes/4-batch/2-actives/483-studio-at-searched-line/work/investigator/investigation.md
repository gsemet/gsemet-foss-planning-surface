# Investigation CR-483 searched-line (first take, read only, nothing run)

The worktree has no node_modules and no .vscode-test: `just dev` first. Nothing was built or tested here.

## 1. Files and entry points (verified by reading, base 024d33e9)

- `src/host-vscode/activation.ts` (507 lines):
  - `start()` registers the commands (`OPEN_AS_TEXT_COMMAND_ID` l.124) and `registerCustomEditorProvider` (l.129).
  - `resolvePreviewEditor(textDocument, webviewPanel)` l.413 does `manager.createSession(panel, document, folder, undefined, false)`, then `manager.startRender`. The line hand-off goes right after `createSession` (a `requestRevealLine` call on the new session).
  - `openAsText` l.251 is the model for the "no eligible editor" message. It is the only `tabGroups.close` today; the new command must not close anything.
  - `deserializePreviewPanel` l.443 (LIFE-038) makes older side previews fixed sessions: `inStudioTab` must stay false there.
- `src/host-api/navigation.ts`: `showDocument(documentId, selection?): PromiseLike<void>` is the port to widen (a line in, an outcome `"studio-created" | "studio-existing" | "other"` out).
- `src/host-vscode/vscodeHost.ts` l.282 `createVscodeNavigation(selections)`:
  - it finds an existing group by `TabInputText` only, then runs `vscode.open` in that group, else column One;
  - to add: find a `TabInputCustom` of `EDITOR_VIEW_TYPE` with the same uri in `tabGroups.all` (Q11, Q15), `openWith` in its column, deliver the line to the live session; otherwise record the pending line, run `vscode.open`, and decide the outcome by which tab appeared; drop the pending line on "other";
  - the file is 425 lines; the Studio-tab logic goes in a new module, as the spec says.
- `src/session/features/links.ts` l.273-309: computes `selection`, records history only when `followsActiveEditor` (comment l.291 to rewrite), calls `showDocument`. The same-document anchor path (l.244) is unchanged.
- `src/session/features/history.ts` `go()` l.81-133:
  - the other-file branch calls `showDocument` at l.124;
  - `historyOf` is a WeakMap per panel (l.24-43): add `shareHistory(source, created)`;
  - `recordNavigation` is l.72;
  - `go()` does `history.restore(before)` on error. With outcome `"other"`, Back and Next keep today's behaviour (the position moves); only links skip recording (Q13).
- `src/session/features/scrollSync.ts` l.260 `requestRevealLine`, `postPendingRevealLine`. `PENDING_LINE_WINDOW_MS` is in `src/core/navigation/pendingLine.ts` (a 2-line file). The pure pending-line class goes next to it, ported from the old `StudioLineRequests` (`git show 1ced0ced^:src/host-vscode/openInStudio.ts`: `recordPending`, `takePending`, `deliver`, `bindLiveSessions`).
- `src/session/previewSession.ts` l.70/93: `followsActiveEditor`. Add a read-only `inStudioTab`, set by `resolvePreviewEditor` and carried by `previewManager.ts` when it recreates a session.
- Side-preview marker path (Q3): `src/host-vscode/editorJumps.ts`, `src/session/hostEvents.ts` `onEditorJumped`, `studioSelections.ts` (`expect/take`).
- Tests and fakes:
  - `test/host/fakeVscode.ts` (830 lines) has a `showDocument` control at l.703. It needs tab groups with `TabInputCustom`, `openWith`, and a Studio-vs-text outcome.
  - Session tests build their own Navigation fakes (`test/session/links.test.ts`, `previewNavigator.test.ts`, `eventFanOut.test.ts`, `toolbarReq.requirements.test.ts` l.305-320, `test/host/lifeReq*`, `hostHarness.ts`). A port signature change touches all of them; a compatible optional outcome keeps most compile-only.
  - `src/host-memory` has no Navigation implementation, only these test fakes. "The memory host records the request" in 7.2 therefore means the fakes.
- Real window: `test/integration/openAtLine.test.ts` (161 lines, `withAssociation`, step `open-at-line` at `trusted-suite.ts` l.268). It reads the page through CDP (`connectWorkbench`, `findCurrentFrame`); the marker selector is `.sphinx-preview-line-marker`. `test/site/e2eGroups.test.ts:55` asserts the INTEGRATION_TESTS count (39), so a second test file changes it.
- Also touched: `package.json` and `test/security/package-contract.test.ts`; `docs/user/open-studio.md`; `docs/known-limitations.md`; requirements LIFE-181, TOOLBAR-059, StRS LIFE-023, new SwRS via `okfreq new`; the glossary; CHANGELOG.

## 2. Smallest change

5.2, `inStudioTab`, the port outcome and 5.3 do not depend on the probe, so the Driver can build them while the probe runs. Order:

1. The probe (throwaway or first version of the real-window test).
2. The pure pending-line class, the 5.2 command, `inStudioTab`, the port outcome, links, history, Back and Next (5.3).
3. 5.1 only for entries the probe marks **signal**.

## 3. Risks

1. **Probe (my reading, unproven).**
   - VS Code turns `file.md:42`, a search result and Go to Symbol into editor options (`selection`). `resolveCustomTextEditor(document, panel, token)` receives neither options nor a fragment, and CR-477 already measured the selection dropped for `vscode.open`.
   - Plausible signals: (1) a `#L42` fragment on `TabInputCustom.uri`, only for the link entry and only if VS Code keeps it; (2) a transient text editor selection event or `activeTextEditor`, unlikely for a custom editor; (3) no public API for the search or Quick Open line (4.2 items 4 and 5).
   - Likely verdict: at most the link `#L42` entry has a signal, so 5.1 is mostly or entirely not built. This is a guess; the probe decides.
2. **Local Windows proof.**
   - `ci-integration` needs a real VS Code (`downloadAndUnzipVSCode`, network), a CDP port and an active window. The screen-lock guard is macOS-only, and `just preflight` on Windows skips integration (justfile l.469), so nothing shows it runs on this machine. To try first: `fnm exec -- npm run test:integration` after `just dev`.
   - Spec 4.3 needs observation on Linux AND local Windows. Linux only through `gh workflow run ci.yml --ref <branch> -f heavy=true`, which needs a pushed branch (Driver or Foreman).
   - Unit tests and the fake cannot prove the probe: the fake would invent the behaviour under test.
   - Driving Search, Quick Open, Problems and Go to Symbol by commands in a window is fragile (Quick Open needs the keyboard, Search needs a search service). The fallback is the CDP keyboard of the `realInput` harness.
3. **Outcome detection is racy.** After `vscode.open`, the tab appears asynchronously and `resolveCustomTextEditor` may run after the command promise. Use the pending line being taken by `resolvePreviewEditor` (a callback) plus a tab-group check with a bounded wait. A text tab means `"other"` and the line is dropped (never applied to text).
4. **TOOLBAR-059 amendment** partly changes an existing assertion; constitution section 3 asks to say why (the non-Studio fixed-preview assertions stay).
5. **VS Code Go Back / Go Forward (Q9)** may not follow an `openWith` reveal of an existing tab. Measure; stop and report if only proposed API could fix it.
6. **Sizes.** `fakeVscode.ts` is 830 of 1500 allowed; `openAtLine.test.ts` is 161, so split only if it nears the limit; new host code stays out of `activation.ts`.
7. **Windows paths.** Existing code compares `fsPath`; keep that for the new `TabInputCustom` search (drive-letter case).

## 4. Questions only the owner can answer

None from this first take. If the probe shows no signal at all, the spec itself drops 5.1.

## 5. Evidence plan

Kind: host behaviour change, visible in VS Code (which tab opens, the line marker).

- **Before and after:** the `[open-at-line]` console lines of the real-window test (studio, text, marks per row, as today) with the probe table in the header comment; Playwright screenshots of the Studio frame showing `.sphinx-preview-line-marker` for the command and each link, Back and Next row (via the `harness.ts` helpers).
- **Technique:** extend `test/integration/openAtLine.test.ts` (step `open-at-line`). Run locally on Windows only if `npm run test:integration` works here (to try first), else the Linux CI dispatch with the run link in the PR. The probe table and the VS Code version go in the PR body.
- **Unit and host:** `just check`; vitest on the pure pending-line class, session tests for links and history, `fakeVscode` host tests (each failing on 80d482fd); the manifest test; `just requirements-lint` and `just requirements-update`.
- **Cannot be shown locally:** the Linux half of the probe verdict (4.3); a real Alt+Left (use `workbench.action.navigateBack`); the owner's 7.4 scenario needs a VSIX (`just package`).
