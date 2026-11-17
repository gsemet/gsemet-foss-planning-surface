# S8b, round 2: internals and tests (coder report)

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-056`, branch
`changes-requests/056-refactor-host-neutral-core` (HEAD 2516aa1). Rounds 1 and 2 are uncommitted.
Nothing was committed, stashed or pushed, and `just preflight` was not run.

## F1: `isSameData` handles cyclic structures

### Fix

The fix is in `src/core/frontmatter/sameData.ts`.

- The comparison now carries a path memo: two `Map<object, number>`, one per side, holding the
  objects on the current path and their depth.
- When either side meets an object already on its path, the pair is equal only if both sides are
  at the same depth. This is how Node's cycle memos decide it. Entries are removed on exit
  (`try`/`finally`).
- The memo is passed through arrays, objects, symbol keys, `Set` and `Map`.
- The public `isSameData(a, b)` signature is unchanged. The module doc now mentions cycles.

### Tests

- **`test/core/frontmatter/sameData.test.ts`:** 8 cyclic sources were added to `YAML_SOURCES`.
  - `a: &x {b: *x}`, plus the near miss with an extra `c: 1`
  - a two-level cycle
  - `a: &x [1, *x]`, `a: &x [1, [1, *x]]` (an unrolled cycle) and `a: &x [2, *x]`
  - an alias shared between two keys
  - two nested anchors

  The existing all-pairs comparison against `util.isDeepStrictEqual` now covers them, on both the
  parsed values and their `structuredClone`s.
- **`test/core/frontmatter/okfFrontmatter.test.ts`:** new test "frontmatter patches stay minimal
  when the block holds a recursive alias". The source is
  `---\ntitle: a\nloop: &x\n  self: *x\nother: [1,2]\n---\nbody\n`. The test asserts:
  - the set patch is exactly `{start: 4, end: 12, text: "title: b"}`;
  - the full text after an insert (`new: v`), a remove (`title`) and a rename (`title` to `t2`).
    Each one is minimal and keeps `other: [1,2]` untouched.

### Failures before the fix

- **Patch test:** fails on the round-1 code. The set call returns the whole block, reformatted
  (`{start: 4, end: 45, text: "title: b\nloop: &x\n  self: *x\nother: [ 1, 2 ]"}`). The remove
  and rename calls throw `RangeError: Maximum call stack size exceeded`. I ran a probe on the
  round-1 build to confirm this.
- **sameData test:** fails with `RangeError: Maximum call stack size exceeded` when the memo
  check is disabled. To show this, I ran a copy of the compiled module with the check replaced by
  `if (false)`, in the scratchpad.

### Match with HEAD

I built HEAD in a temporary detached `git worktree` in the scratchpad and ran the four calls on
it. HEAD returns exactly what the new test asserts:

- `{4,12,"title: b"}`
- the insert, remove and rename texts above

The worktree build now gives the same four results.

### Extra check (not committed)

A scratchpad fuzz compared `isSameData` with `isDeepStrictEqual` on 640 000 pairs of random
cyclic graphs (objects and arrays, shared and self references, plus clones). There were 0
differences.

The temporary worktree and the scratchpad folder were removed afterwards. `git worktree list`
shows only the main checkout and wt-056.

## F2: "Add a message" recipe in CONTRIBUTING

`CONTRIBUTING.md`, section "Extension points", after "Add a setting". The recipe has five steps:

1. **Page to host:** the union member and the validator in `PAGE_TO_HOST_VALIDATORS`
   (`src/core/protocol/pageToHost.ts`). The envelope is checked first, and the table is typed by
   the union.
2. **Host to page:** the union member and the rule in `createHostMessageFilter`
   (`src/core/protocol/hostToPage.ts`), with its addressing (`render`, `document` or `own-id`) and
   an optional validator. The recipe also states the limit of the filter: it matches the message
   and checks the payload, but cannot tell whether the host had a reason to send it.
3. **Host side of page to host:** the gate in `PAGE_MESSAGE_GATES` (`src/session/pageMessages.ts`)
   and `router.on(type, …)` in the `register` method of the owning controller in
   `src/session/features/`. The page posts through its `PageHost`.
4. **Page side of host to page:** `hostMessages.on(type, …)` in the owning page feature or in
   `src/page/features/hostHandlers.ts`. The host sends it with `preview.postToPage(…)`.
5. **Tests and gates:**
   - the validator or filter tests in `test/core/protocol/` (`pageToHost.test.ts`,
     `hostToPage.test.ts`);
   - `test/session/previewManager.test.ts` checks that every type has exactly one handler. It pins
     the count (41), so the recipe says to raise it by one;
   - `tsc` refuses a missing gate, validator or filter rule (all three tables are typed by their
     union);
   - run `npx tsc -p .` and `npm run test:unit`.

The intro now says "Four registries".

## Non-blocking items addressed

- **I4, palette recipe step 3:** it now names the subject modules that hold the edit functions
  (`inlineEditActions.ts`, `blockEditActions.ts`, `linkEditActions.ts`, `tableEditActions.ts`,
  `colourEditActions.ts`).
- **Stale doc comment in `src/core/protocol/pageToHost.ts`:** step 3 pointed to
  `PAGE_MESSAGE_GATES` "in `src/extension.ts`". It now points to `src/session/pageMessages.ts`.
  This is a comment-only change.
- **Not changed:**
  - the `scenarioInvariants.test.ts` title still says "capture.py", because the rules keep test
    titles identical;
  - the redundant `sameEntries` re-walk on arrays is left as is (the reviewer asked for no change).

## Gates (worktree, Node 24.22.0 via `fnm exec --`, foreground, nothing left running)

| Gate | Result |
| --- | --- |
| `npx tsc -p .` | exit 0 |
| `npm run test:unit` | 2 306 tests, 2 306 pass, 0 fail (round 1 had 2 305; +1 is the recursive-alias patch test) |
| `UV_NO_CONFIG=1 UV_OFFLINE=1 just check` | exit 0. check-boundaries passed (252 modules), check-limits passed (600 files, 1 on the size baseline), check-settings passed (18 settings), pytest 31 passed. The `rm_rf` warnings are pytest temp-dir noise from before this round |
| `UV_NO_CONFIG=1 UV_OFFLINE=1 just visual` | exit 0, `{"status": "passed", "scenario_count": 320, "screenshot_count": 210}`. No baseline PNG changed (`git status` shows no `.png`) |
| `npm run bundle` | exit 0, `preview.js` is 287.1 kB |
| `npm run test:integration` | **Not run.** `ioreg -n Root -d1 -a \| grep -A1 CGSSessionScreenIsLocked` printed `<true/>` (screen locked), so the window lock was not taken. The driver must run it on an unlocked screen before the PR is marked ready |

## Open points

- Run the real VS Code integration tests under the window lock. This is still pending from
  round 1.
- The open points from round 1 are unchanged:
  - `realInput.test.ts` stays on the size baseline;
  - the optional directive plug-in follow-up;
  - `test/visual/__pycache__/` is git-ignored;
  - do not stage the `.venv` symlink.
- The PR text must list "CSS stays as TypeScript modules" under "Autonomous decisions" (review I1).

## Paths to stage for the whole step (76; excludes node_modules and .venv)

Round 1's 75 paths, plus `src/core/protocol/pageToHost.ts`. The files changed in round 2 are
`CONTRIBUTING.md`, `src/core/frontmatter/sameData.ts`, `src/core/protocol/pageToHost.ts`,
`test/core/frontmatter/okfFrontmatter.test.ts` and `test/core/frontmatter/sameData.test.ts`.

```text
.agents/skills/markdown-studio-exploratory-qa-claude/scripts/coverage-map.py
.dependency-cruiser.cjs
CONTRIBUTING.md
justfile
scripts/file-size-baseline.json
src/core/directives/directive.ts
src/core/directives/registry.ts
src/core/frontmatter/frontmatterParse.ts
src/core/frontmatter/frontmatterSerialize.ts
src/core/frontmatter/frontmatterValidate.ts
src/core/frontmatter/okfFrontmatter.ts
src/core/frontmatter/sameData.ts
src/core/frontmatter/schemaFiles.ts
src/core/preview/previewStyles.ts
src/core/preview/styles/commentStyles.ts
src/core/preview/styles/contentBlockStyles.ts
src/core/preview/styles/contentLayoutStyles.ts
src/core/preview/styles/editModeStyles.ts
src/core/preview/styles/editPaletteStyles.ts
src/core/preview/styles/frontmatterEditorStyles.ts
src/core/preview/styles/pageChromeStyles.ts
src/core/preview/styles/propertiesStyles.ts
src/core/protocol/hostToPage.ts
src/core/protocol/pageToHost.ts
src/core/render/mystBlockTransforms.ts
src/core/render/mystContextTags.ts
src/core/render/mystEngine.ts
src/core/render/mystGithubAlerts.ts
src/core/render/mystInlineTransforms.ts
src/core/render/mystNormalize.ts
src/core/render/mystRenderer.ts
src/core/render/mystTables.ts
src/core/render/mystTypes.ts
src/core/render/renderPipeline.ts
src/host-api/index.ts
src/host-vscode/vscodeHost.ts
src/node-services/schemaFiles.ts
src/page/modules/blockEditActions.ts
src/page/modules/colourEditActions.ts
src/page/modules/editActionHelpers.ts
src/page/modules/editActions.ts
src/page/modules/editPalette.ts
src/page/modules/editPalettePopovers.ts
src/page/modules/inlineEditActions.ts
src/page/modules/linkEditActions.ts
src/page/modules/tableEditActions.ts
src/session/features/frontmatter.ts
src/session/features/links.ts
src/session/features/rendering.ts
test/core/directives/registry.test.ts
test/core/frontmatter/okfFrontmatter.test.ts
test/core/frontmatter/sameData.test.ts
test/core/frontmatter/schemaRegistry.test.ts
test/core/protocol/hostToPage.test.ts
test/core/protocol/router.test.ts
test/core/render/mystFeatures.test.ts
test/core/render/mystFeaturesSupport.ts
test/core/render/mystPaletteRendering.test.ts
test/probe/previewProbe.ts
test/session/links.test.ts
test/shared/geometry-checks.js
test/site/e2eGroups.test.ts
test/site/scenarioInvariants.test.ts
test/visual/capture_comment_checks.py
test/visual/capture_edit_checks.py
test/visual/capture_final_checks.py
test/visual/capture_layout_checks.py
test/visual/capture_page_checks.py
test/visual/capture_support.py
test/visual/capture.py
test/visual/renderFixtures.ts
test/visual/scenarioAssertions.ts
test/visual/scenarioDefinitions1.ts
test/visual/scenarioDefinitions2.ts
test/visual/scenarioIds.ts
test/visual/scenarios.ts
```
