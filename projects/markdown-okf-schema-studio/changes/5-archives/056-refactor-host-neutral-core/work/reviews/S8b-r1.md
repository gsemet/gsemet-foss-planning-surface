Verdict: FIX-REQUIRED

# S8b, round 1: internals and tests (REVIEWER)

I reviewed the round diff on `changes-requests/056-refactor-host-neutral-core` (HEAD `2516aa1` =
S8a): `git diff HEAD -M` plus the untracked files, ignoring `.venv` and `node_modules`. The review
was read-only, and only this file was written. To compare against HEAD, I built HEAD in a temporary
`git worktree` in the scratchpad and removed it afterwards. `git worktree list` shows only the main
checkout and the 056 worktree.

## Gates (re-run in the worktree, Node 24.22.0 via `fnm exec --`, foreground)

| Gate | Result |
| --- | --- |
| `npx tsc -p .` | exit 0 |
| `npm run test:unit` | 2 305 / 2 305 pass |
| `UV_NO_CONFIG=1 UV_OFFLINE=1 just check` | exit 0. Boundaries passed (252 modules, 0 violations). check-limits passed (600 files, 1 on the baseline). check-settings passed (18). pytest 31 passed (the `rm_rf` warnings are pytest temp-dir noise from before this round) |
| `npm run bundle` | exit 0, `preview.js` is 287.1 kB |

I did not re-run `just visual` or integration (not asked). The coder ran `just visual`: 320
scenarios, no PNG changed.

## What I verified independently (HEAD build vs worktree build)

- **Renderer: equivalent.**
  - `TREE_PASSES` and `HTML_PASSES` are the HEAD call sequence, in the same order and with the same
    conditions (extension check, includes only with `sourcePath`, checkboxes only with markers).
  - The `NODE_RULES` dispatch reproduces the old `if` chain, including fall-through:
    - Each rule's `kinds` cover every type its guard accepts. `isPlantUmlNode` is limited to
      `plantuml`, `mystDirective` and `code`, which the rule declares.
    - A type change by a non-finishing rule (the `html` to `rawHtmlTableBlock` rewrite, or a
      plug-in `render`) re-dispatches only to later rules of the new kind, as the old chain did.
    - The final `BLOCK_TYPES` line merge uses the current type.
  - I rendered all 115 tracked `.md` files plus 28 hand-written edge inputs, each with and without a
    render context. The edge inputs cover mermaid and plantuml, a missing or empty `{uml}`, empty
    `outputs`, cite and bibliography, unknown and empty directives, raw HTML tables, callout divs,
    dropdown and no-icon admonitions, figure width and alignment, `#tbl:` images, version
    directives, includes, grids, toctree and frontmatter. 286 / 286 results (HTML, diagnostics and
    dependencies) are byte-identical.
- **Sanitizer: nothing widened.**
  - `html-sanitizer.ts` is unchanged.
  - `directiveAttributeAllowed` only narrows what plug-ins may declare: `data-*` names, minus the
    three the sanitizer handles itself. A plug-in rule runs before the generic `on*` / `style` /
    URL checks, so the restriction is the right one. It also rejects `data` (the `<object>`
    resource attribute), because the check requires the dash.
  - The new registry test pins the restriction, and the existing descriptors pass it.
- **Frontmatter: equivalent on real data.**
  - I ran `analyzeFrontmatter` (strict on and off, `inspectLinks` on and off) on every tracked
    `.md` file, HEAD with its own fs and the worktree with `nodeSchemaFiles`. 460 / 460 results are
    identical, including the visual fixtures under `_schema`.
  - I ran 2 496 field, rename and remove patches on the 20 files with frontmatter. All are
    identical.
  - `nodeSchemaFiles` keeps the HEAD try/catch shape, `readText` still throws, and the
    `setSchemaFileReaderForTests` hook is kept.
- **Styles: byte-identical.** Every `previewStyles` export (3) is identical to HEAD.
  `previewStyles.ts` is 119 lines.
- **Tests:**
  - `mystFeatures.test.ts` + `mystPaletteRendering.test.ts` + `mystFeaturesSupport.ts`: compared as
    a sorted line multiset against HEAD's `mystFeatures.test.ts`, they differ only in imports,
    blank lines, two doc comments and `export` prefixes.
  - The `SCENARIOS` dump (320 entries, functions serialized) is identical to HEAD.
  - The protocol tests move to direct imports with identical assertions, which closes S8a I2. The
    "declared in its body" comment is dropped with them.
  - The other changed tests only add `schemaFiles` / `nodeSchemaFiles` in their setup.
- **capture.py split:** I compared the top-level statements by AST. All 121 HEAD definitions and
  assignments appear exactly once across `capture*.py`, each with an identical `ast.dump`. Nothing
  is missing or extra, and there are no `global` statements, so no module-level rebinding is lost
  through `from … import`. The module docstrings follow the file's existing style.
  `__pycache__/` is git-ignored.
- **Ratchet:** the baseline only loses entries, and only `realInput.test.ts` remains. No `src/`
  file is above 800 lines (the largest new one is `frontmatterSerialize.ts`, 746). The boundary
  exceptions only shrink (`RENDERER_SPLIT` is gone, and `fs`, `util` and `perf_hooks` are dropped
  from core).

## Findings

### F1: medium (blocking): `isSameData` overflows the stack on a recursive YAML alias, where `isDeepStrictEqual` did not

`src/core/frontmatter/sameData.ts:56` (`isSameData`), called from `verified()` at
`src/core/frontmatter/frontmatterSerialize.ts:306`.

`yaml` turns a recursive alias into a cyclic object (`loop: &x\n  self: *x`, so
`doc.loop.self === doc.loop`). Node's `isDeepStrictEqual` detects cycles with its memos.
`isSameData` recurses forever and throws `RangeError: Maximum call stack size exceeded`. I
reproduced this with HEAD and the worktree built side by side, on
`---\ntitle: a\nloop: &x\n  self: *x\nother: [1,2]\n---\nbody\n`:

| Call | HEAD | Worktree |
| --- | --- | --- |
| `createFrontmatterFieldPatch(src, "title", "b")` | minimal `{4,12,"title: b"}` | whole block, reformatted (`other: [ 1, 2 ]`) |
| `createFrontmatterFieldPatch(src, "new", "v")` | minimal insert | whole block, reformatted |
| `createFrontmatterFieldRemovePatch(src, "title")` | minimal | **throws RangeError** |
| `createFrontmatterFieldRenamePatch(src, "title", "t2")` | minimal | **throws RangeError** |

The input is unusual, but it is a visible behaviour change in the properties editor, and an
uncaught throw in a pure move step. The new pin test does not cover cycles.

Fix:
- Give `isSameData` cycle detection the way Node does it: an internal `memo` (two
  `Map<object, number>` of the objects on the current path, or a pair stack). When either side is
  already on the path, return whether both were entered at the same position. Pop on exit.
- Add cyclic sources to `YAML_SOURCES` in `test/core/frontmatter/sameData.test.ts`, so the
  all-pairs comparison against `isDeepStrictEqual` covers them, for example
  `"a: &x\n  b: *x\n"`, `"a: &x [1, *x]\n"` and a near miss such as `"a: &x\n  b: *x\n  c: 1\n"`.
  `structuredClone` keeps the cycles.
- Add one patch test in `okfFrontmatter.test.ts`: remove, rename and set a field of a frontmatter
  with a recursive alias, and assert the minimal patch. This test fails before the fix (it throws).

### F2: low (blocking, cheap, last step): the CONTRIBUTING recipe "how to add a message" is missing

`CONTRIBUTING.md`, section "Extension points" (around line 108). `task.md` → Docs asks for "how to
add a message, a palette action, a directive, a setting". The palette action, directive and setting
recipes are there. A message recipe is not: the only mention is the `liveSetting` sentence at line
149.

Fix: add a short **Add a message** recipe that names:
- the union member and its validator in `src/core/protocol/pageToHost.ts` or `hostToPage.ts`,
  with the limits of the host filter for host-to-page messages;
- the `router.on(type, …)` registration: a session feature controller for page-to-host, or
  `src/page/features/hostHandlers.ts` for host-to-page;
- the test files that pin the validators (`test/core/protocol/`).

### I1: info: CSS stays as TypeScript modules. I accept this as an autonomous decision

The spec says ".css files". The coder kept per-feature template-literal modules. I evaluated the
alternatives:
- The 8 style modules interpolate 9 TypeScript values: `DEFAULT_PREVIEW_CONTENT_WIDTH` (3 times),
  the registry's `directiveStyle("figure" | "admonition" | "tables")`, `gridColumnCss()` and
  `CALLOUT_ICONS.triangle` (twice). Plain `.css` files cannot hold these without adding a
  placeholder or templating layer. That layer would undo the S7 rule that a directive owns its
  style in its descriptor.
- The tsc `out/` tree is what the unit, visual and integration suites import, and
  `src/session/webview.ts` imports it too. With `.css` sources, the build needs either:
  - a committed generated TS module plus a `--check` gate. There is a precedent
    (`generate-settings`), but it would duplicate about 4 000 lines in the repository;
  - or a generation step before tsc, wired into `compile`, `watch`, `test`, `test:integration`, CI
    and the VS Code tasks.
- What ships is already a real stylesheet (`out/bundle/preview.css`), and it is byte-identical.

Both options add build machinery and risk for no runtime gain. I do not require the change. The PR
text must list this under "Autonomous decisions" as a deliberate deviation from the spec wording,
so the user can decide. CONTRIBUTING already explains it (line ~101).

### I2: info: the synchronous `SchemaFiles` port is acceptable

The port is synchronous because `analyzeFrontmatter` runs synchronously inside the render. Going
async would change timing, which a pure move step must not do. It is narrow (4 read-only methods),
documented with TSDoc, implemented in `node-services` and injected through `HostServices`, with no
new boundary exception. One detail: the interface lives in `core/frontmatter/schemaFiles.ts` and
`host-api` re-exports it. The other ports are declared in `host-api`. This is fine because `core`
may not import `host-api`, and the core function needs the type. A later async `FileSystem`-backed
version belongs with the existing `PORT_FOLLOW_UP` items.

### I3: info: open points accepted

- `realInput.test.ts` stays on the baseline. Its scenarios share module-level mutable state, and
  only a real-window run could prove a split. This is justified, and the spec's "big files under
  the ratchet" names `src/` files only.
- Version admonitions, `{include}`, `{uml}` and the table-style branch stay in the renderer as
  named passes. The pass order is output-relevant, and S7 made the plug-ins optional per directive.
  Keep this as a follow-up.
- Integration was not run (screen locked). The driver must run it under the lock before marking
  the PR ready (this is the last step).

### I4: info: small items

- `test/site/scenarioInvariants.test.ts:71`: the title still says "registered in capture.py" while
  `STEP_NAMES` now lives in `capture_support.py`. Keeping test titles is consistent with the
  "identical tests" rule. Optional.
- The CONTRIBUTING palette recipe step 3 is still accurate (the `handlers` table is in
  `createEditActions`). Optionally add that the edit functions live in the subject modules
  (`inlineEditActions.ts`, `blockEditActions.ts`, ...).
- `isSameData` arrays: `sameEntries` re-walks the index keys after the element loop. This is
  correct but redundant. No change needed.

## Required for round 2

1. F1: cycle-safe `isSameData`, plus cyclic cases in `sameData.test.ts` and one patch test that
   fails before the fix.
2. F2: the "Add a message" recipe in CONTRIBUTING.
3. Re-run tsc, unit, `just check`. `just visual` is not needed for these two changes, but cheap.
