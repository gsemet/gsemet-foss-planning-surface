# Heavy CI red on main: preview-smoke reads the page before it is shown

The real-VS-Code jobs `integration` and `stress` are red on `main` since d762a732, at their first
step `preview-smoke`. This CR proves the cause, fixes what is wrong (product or test, as the cause
says), and gets both heavy jobs green again, at the bottom of batch-09's stack, before 1.12.1.

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

Proof plan, cheapest first; stop when one of H1 / H2 is proven:

1. Local real window, when the machine can run it (`just integration`, see
   `.agents/guidelines/local-worktree.guidelines.md`): on a scratch branch off `main`, in
   `runPreviewSmoke`, wait up to 10 s for the status page to leave (`waitFor` of
   `test/integration/previewEditingHelpers.ts`) before the assertions. Green step: H1. Timeout:
   H2; read the Studio output channel and the extension host log for the rejected show.
2. Otherwise the same scratch branch, pushed, with
   `gh workflow run ci.yml --ref <branch> -f heavy=true`.
3. Only if 1 and 2 do not conclude: bisect with heavy runs on branches at 20b12216, 35258332,
   7b8339e9 and b4a8cb12 (d9b3cd6b is known green).

The scratch branch is evidence only; it is not the fix. The PR names the proven cause and the run
or log that proves it.

## The fix, by proven cause

**If H2:** fix the product so the show lands in a real window, in the file the proof points to
(`src/session/features/rendering.ts`, `src/session/webview.ts`,
`src/core/security/resource-policy.ts` or the VS Code file port). `preview-smoke` stays as it is,
apart from what the H1 branch below also needs.

**If H1,** two ways; see "Open questions" for which one. The spec's default is A.

- **A. Product: the open command resolves again once the page is shown.** `requestDocument` in
  `src/session/previewManager.ts` waits, after `session.queue.request(document)`, for the session's
  pending show (the `updates` chain of `RenderingController` in
  `src/session/features/rendering.ts`, exposed by a small method). The order of 1.12.0 is restored
  for every caller (`openPreview`, the custom editor and the serializer in
  `src/host-vscode/activation.ts`), and `preview-smoke` is not touched. The wait must not hang on
  a disposed session, a hidden panel or a deferred result (an open inline editor): those resolve
  as today.
- **B. Test: `preview-smoke` waits for the rendered page.** A `waitFor` on the document identity,
  `phase === "ready"` and the page no longer being the status page, before the unchanged
  assertions. The PR says why the product is right (the page shows the same content; only the
  moment the command's promise resolves moved, and no requirement states that moment).

Whatever the branch, every assertion of `runPreviewSmoke` keeps its intent.

## A cheaper test, outside the heavy jobs

- With A (or H2 where it applies): a test in `test/host/` (the real activation on the fake
  `vscode`, as `test/host/coreReq.requirements.test.ts` does) that awaits the open command and,
  with no extra `turn()`, finds the rendered document in the page HTML (an admonition of the
  source), not the status page. It fails on `main` today and runs in `just check`.
- With B: no product behaviour to pin. The guard is a static test (in `test/build/` or beside the
  integration helpers) that fails when a file of `test/integration/` reads `.html` of
  `getActivePreviewForTests()` straight after `executeCommand(COMMAND_ID)` with no wait between.
  If this proves brittle, the Driver says so in the PR and drops it; it is "where possible".

## Requirements (SwRS)

- A or H2: a behaviour of `src/` changes, so an SwRS changes in the same PR. First look for the
  leaf that already holds it (SwRS-MDOKFSTUDIO-LIFE-003, "Open Preview to Side opens or reveals a
  side preview", is the likely one); add the sentence or scenario "the command completes when the
  page shows the document", else create one with `okfreq new`. Markers `@implements_req` at the
  wait and `@tests_req` at the new test, `just requirements-update`, a dated entry in
  `requirements/tiers/log.md`.
- B: no SwRS text changes. The existing markers of `trusted-suite.ts` stay where they are
  (`@tests_req SwRS-MDOKFSTUDIO-TRUST-012` on `run`). `just requirements-update` is still run and
  must change nothing.

## Other heavy failures hidden behind this one

Every step after `preview-smoke` has not run in a real window since d9b3cd6b, across seven
commits. Known suspects of the same race, to check first:

- `test/integration/sourceMapping.test.ts`: reads `preview.html` straight after the command.
- Every wait that tests `phase === "ready"` and then reads `html` (for example
  `waitForCurrentPreview` in `test/integration/previewEditingHelpers.ts`, `dirtySnapshots`,
  `projectFeatures`, `lifecycle`): `phase` comes from the render queue and can now be `ready` one
  step before the page HTML is assigned. Those that also test the HTML in the predicate are safe.

With A most of these disappear with the fix; with B each one gets its own wait. Each hidden
failure found by the heavy runs is named in the PR with its cause and fix. One that needs a
behaviour decision is reported to the Chief of Staff, not decided by the Driver. Failures from
b4a8cb12 (PlantUML through `ProcessRunner`) and 7b8339e9 (paths through one module) are in scope
on the same terms.

## Delivery

- Place: the bottom of batch-09's stack, on `main`, beside CR-477, so CR-475, CR-476, CR-477 and
  the release CR-478 are each heavy-run on top of it. It ships in 1.12.1.
- `CHANGELOG.md`: a line only if the product changed (A or H2).
- No CI job is added or changed; `.github/workflows/ci.yml` and the `ci-*` targets stay as they
  are.

## Out of scope

- Undoing the async render port of 20b12216 or 35258332.
- Making heavy runs mandatory on stack heads before a merge (a process matter).
- Any behaviour change beyond the proven cause and the hidden failures it uncovers.

## Evidence (acceptance)

1. The proof of the cause: the run or the local log, linked in the PR.
2. The new cheap test fails on `main` (2e2efa6c) and passes on the fix (A, H2; the static guard
   for B).
3. `just preflight` green on the branch.
4. A heavy run of the fixed head, `gh workflow run ci.yml --ref <branch> -f heavy=true`, with
   `integration` and `stress` both green: `preview-smoke` done and every later step done. The run
   number is in the PR. This is the acceptance; a green `preview-smoke` with a later red step is
   not.
5. The PR lists each hidden failure, or says that none was found.

## Open questions

1. When H1 is proven, A or B? In 1.12.0 the open command's promise resolved after the page was
   shown; no requirement states it and a reader sees no difference. A restores it in the product
   (small, gives a real cheap test, covers the other racing tests at once, needs an SwRS sentence
   and maybe a CHANGELOG line). B keeps the product and makes each test wait. The spec's default
   is A.
