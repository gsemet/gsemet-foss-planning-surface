# Conflicts: CR-470 rebased on CR-471 (792ae892), new head 3f6d3efb

- `.dependency-cruiser.cjs`: dropped the `plantUmlRenderer.ts` NODE_DEBT entry (no `child_process`, `fs` or `node:path` left; the path comes from `../path/hostPath`). Base removal of the other path entries kept.
- `src/core/render/plantUmlRenderer.ts` imports: kept `../path/hostPath` (CR-471), dropped `node:child_process` / `node:fs` (CR-470). Both sides added an options field `files` (base `PolicyFiles`, CR `PlantUmlFiles`): merged into one `files: PolicyFiles & PlantUmlFiles`; the jar and Java-home lookups use it too.
- Follow-on: removed `plantUmlFiles` (renderPipeline `RenderOptions`, sessionFactory, baselineDiff); the pipeline passes `options.files` (duplicate `files` key removed). `plantUmlProcesses` stays.
- Tests (diagReq.jar, plantUmlCache, plantUmlEngine, plantUmlJarIncludes, plantUmlRenderer): took the port-based fakes (`hostOf`, `fakeRunner`) over the spawn fakes; `hostOf` carries `files`, so the base's `files: createNodeFileSystem()` lines were dropped where doubled, and added where a call had none. Spawn-level detach/kill tests are gone (covered by test/node-services/processRunner.test.ts).
- test/session/baselineDiff and diagReq.plantuml.requirements: union of both host stubs (`capabilities.processes` plus `files: createNodeFileSystem()`).
- test/visual/renderFixtures.ts, mystFeatures, plantUmlFile, diagReq.pipeline: removed duplicate `files` / `plantUmlFiles`.
- No BOM added; rebase continued, commit message kept.

Fast gate: `just check` (log: work/conflict-resolver/check.log): exit 0 (passes; only okfreq W2 broken-cross-link warnings, pre-existing). `tsc --noEmit -p .` clean.
