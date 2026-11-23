# Heavy CI red on main: preview-smoke reads the page before it is shown

The real-VS-Code jobs `integration` and `stress` are red on `main` since d762a732, at their first
step `preview-smoke`. This CR proves the cause, fixes the product, and gets both heavy jobs green
again, at the bottom of batch-09's stack, before 1.12.1.

Rules: the code repository's `AGENTS.md`, `.agents/constitution.md`,
`.agents/guidelines/ci.guidelines.md` and `requirements/guidelines/project.guidelines.md`
("During a change") apply; this spec restates none of them.

## Goal

As in 1.12.0 (d9b3cd6b): in a real window, the preview of
`test/integration/fixtures/preview.md` shows its admonitions and everything `preview-smoke`
asserts, and `integration` and `stress` are green on the fixed head. No assertion is weakened to
get there.

## What is known (read from the logs and the code, not run)

- The step is `runPreviewSmoke` in `test/integration/trusted-suite.ts`. It opens `preview.md`,
  adds an unsaved marker, runs `await vscode.commands.executeCommand(COMMAND_ID)`, then reads
  `getActivePreviewForTests().html` at once, with no wait, and asserts `/admonition/iu`, `/math/iu`,
  the local image, the CSP, the nonce, one KaTeX stylesheet, the toolbar and the dirty marker.
- In both red runs (45156102152 at d762a732, 45187475612 at 2e2efa6c) the HTML printed by the
  failed assertion is not a rendered document without admonitions. It is the status page:
  `<body data-sphinx-preview-status-page>… Preview pending … Rendering the active buffer.` The step
  fails 1.3 to 1.5 s after it starts, in both jobs.
- 20b12216 made the show of a finished render asynchronous. In
  `src/session/features/rendering.ts`, `updatePreview` now returns a promise (it awaits
  `previewLocalResourceRoots` and `buildPreviewWebviewHtml`, which read files through the async
  port), and `handleQueueState` calls it with `fireAndForget`. In d9b3cd6b it was synchronous, so
  the page HTML was assigned before `manager.requestDocument` (`src/session/previewManager.ts`)
  and so the open command resolved. Now the command resolves while the page still holds the
  pending status page.
- The same commit lengthened the wait of the simulated hosts (`turn()` in
  `test/host/hostHarness.ts` and `test/host/lifeReqHarness.ts` gained a disk round trip), which is
  why the pull-request jobs stayed green.

## Hypothesis the Driver proves first

**H1 (most likely): a timing change, not lost admonitions.** Since 20b12216 the open command
resolves before the rendered page is assigned; `preview-smoke` reads the pending page. The page
gets the rendered document, admonitions included, a moment later.

**H2 (to rule out): the show never lands in a real window.** `showPreview` rejects or hangs on the
real host (`createVscodeFileSystem()` behind `manager.host.files`: `realpath`, `stat`, `readFile`
in `ResourcePolicy.open` and `prime`); `fireAndForget` logs it and the page stays pending. This
would be a product regression users see.

Proof plan; stop when one of H1 / H2 is proven:

1. Default: a scratch branch off `main` where `runPreviewSmoke` waits up to 10 s for the status
   page to leave (`waitFor` of `test/integration/previewEditingHelpers.ts`) before its assertions,
   pushed, then `gh workflow run ci.yml --ref <branch> -f heavy=true`. Green step: H1. Timeout:
   H2; read the extension host log of the run for the rejected show.
2. A local real window instead (the same scratch change, `npm run test:integration`) only when the
   Driver's host already runs it and no other active CR is using an app window: the repository is
   on Windows and the other active CRs may hold the window
   (`.agents/guidelines/local-worktree.guidelines.md`).
3. Only if 1 and 2 do not conclude: bisect with heavy runs on branches at 20b12216, 35258332,
   7b8339e9 and b4a8cb12 (d9b3cd6b is known green).

The scratch branch is evidence only; it is not the fix. The PR names the proven cause and the run
or log that proves it.

## The fix

**H1 proven (heavy-red-Q5: A, the product fix).** `requestDocument` in
`src/session/previewManager.ts` waits, after `session.queue.request(document)`, for the session's
pending show (the `updates` chain of `RenderingController` in
`src/session/features/rendering.ts`, exposed by a small method). The wait stays inside those two
files. It must not hang on a disposed session, a hidden panel or a deferred result (an open inline
editor): those resolve as today.

What it changes, by caller:

- `openPreview` on the first open (`activation.ts:440`) and on the same document again
  (`activation.ts:419`);
- `refreshActive`, the Refresh Preview command (`previewManager.ts:696`);
- `deserializePreviewPanel` (`activation.ts:547`).

What it does not change: the custom editor (`startRender`, `activation.ts:472`, not awaited), and
Open Preview on another document (`switchAfterFlush`, `activation.ts:417`, not awaited in 1.12.0
either).

`preview-smoke` is not edited: every assertion of `runPreviewSmoke` stays as it is. Under this fix
the CR touches neither `src/host-vscode/activation.ts` nor `test/integration/trusted-suite.ts`,
apart from the CR-477 case below.

**H2 proven instead.** A product regression: fix the product so the show lands in a real window,
in the file the proof points to (`src/session/features/rendering.ts`, `src/session/webview.ts`,
`src/core/security/resource-policy.ts` or the VS Code file port). The rest of this spec applies
the same way.

## A cheaper test, outside the heavy jobs

A test in `test/host/` on the real activation and the fake `vscode`. `openPreview` of
`test/host/hostHarness.ts` runs under `MockTimers` and does not await the command (a plain await
deadlocks on the 120 ms debounce). So: start the command, capture the page HTML in a `.then` on
its promise, and drive the clock and `turn()` until the promise settles. The captured HTML must be
the rendered document (an admonition of the source), not the status page. A small harness entry
for this is allowed. The test fails on `main` today and runs in `just check`.

## Races the fix does not cover

The fix covers only renders that go through `requestDocument`. Edit renders
(`refreshPreviewDocument`, `rendering.ts:517` and `530`, `previewManager.ts:631`), deferred results
and document switches still publish `phase === "ready"` before the page HTML is set, and about 70
waits of `test/integration/` check `phase`.

The Driver greps `test/integration/` for waits that check `phase === "ready"` and then read
`html` outside the predicate, after an edit or a switch, and moves the HTML condition into the
predicate. These are test fixes (the product is right: the page gets the same content), each one
listed in the PR. One green heavy run does not prove their absence: these races are intermittent,
so the grep is done whatever the run says.

## Other heavy failures hidden behind this one

Every step after `preview-smoke` has not run in a real window since d9b3cd6b, across seven
commits; b4a8cb12 (PlantUML through `ProcessRunner`) and 7b8339e9 (paths through one module) are
in scope on the same terms. Each hidden failure the heavy runs find is named in the PR with its
cause and fix. One that needs a behaviour decision is reported to the Chief of Staff, not decided
by the Driver.

Overlap with CR-477 (`4-batch/2-actives/477-raw-text-opens-studio`): a hidden failure in the
open-at-line step or in the opening watcher is named in the PR and left to CR-477, unless it
blocks the later steps; then the smallest test-side wait is applied here.

## Requirements (SwRS)

The behaviour of `src/` changes, so SwRS-MDOKFSTUDIO-LIFE-003 ("Open Preview to Side opens or
reveals a side preview") changes in the same PR: the command completes once the page shows the
document, in its scenarios "First preview" and "The shown document again" only (not "Another
document"). If Refresh Preview or the restored panel has its own leaf, the Driver adds the
sentence there too, else LIFE-003 and the log entry carry it. Markers: `@implements_req` at the
wait, `@tests_req` at the new test. Then `just requirements-update` and a dated entry in
`requirements/tiers/log.md`. The test-side waits change no SwRS.

## Delivery

- Place: the bottom of batch-09's stack, on `main`, beside CR-477. CR-475, CR-476 and CR-477 are
  rebased onto this CR, and the release CR-478 on top, so each is heavy-run on it. Conflicts in
  `requirements/tiers/log.md` and `CHANGELOG.md` keep both entries. It ships in 1.12.1.
- `CHANGELOG.md`: the fix is a `fix` commit in `src/`, so the PR adds one line under
  `## Unreleased`, for example "Open Preview to Side and Refresh Preview complete once the page
  shows the document again, as in 1.12.0 (CR-<n> heavy-red, PR #<n>)".
- No CI job is added or changed; `.github/workflows/ci.yml` and the `ci-*` targets stay as they
  are.

## Out of scope

- Undoing the async render port of 20b12216 or 35258332.
- Awaiting the show in the custom editor or on a document switch.
- Making heavy runs mandatory on stack heads before a merge (a process matter).
- Any behaviour change beyond the proven cause and the hidden failures it uncovers.

## Evidence (acceptance)

1. The proof of the cause: the heavy run of the scratch branch (or the local log), linked in the
   PR.
2. The new `test/host/` test fails on `main` (2e2efa6c) and passes on the fix.
3. The list of the test-side waits moved into their predicate, from the grep, in the PR.
4. `just preflight` green on the branch.
5. A heavy run of the fixed head, `gh workflow run ci.yml --ref <branch> -f heavy=true`, with
   `integration` and `stress` both green: `preview-smoke` done and every later step done. The run
   number is in the PR. This is the acceptance; a green `preview-smoke` with a later red step is
   not.
6. The PR lists each hidden failure, those left to CR-477 included, or says that none was found.

## Open questions

None.
