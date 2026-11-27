# Investigation CR-471: one path module for core and session

Base: origin/main 116f39d8 (v1.12.0). Read only; only greps and `gh pr list` were run.

## Map

`node:path` importers (all `import * as path from "node:path"`, no named imports):
- core (12): frontmatter/{fileLinks,okfFrontmatter,stemIndex}, mapping/{imageReference,mystTargets}, myst/confLocator,
  render/{documentGlob,mystRenderer,plantUmlIncludes,plantUmlRenderer,renderPipeline}, security/resource-policy.
- session (13): bibScan, hostEvents, previewManager, previewNavigator, sessionDocuments, sessionFactory, sharedWatchers,
  webview, features/{comments,hostRequests,htmlExport,links,scrollSync}.
- No other Node built-in in src/session. src/page imports no path.

Functions used (counts): dirname 44, resolve 40, basename 22, join 21, isAbsolute 20, relative 14, extname 9, sep 8,
parse 2 (`.root` in okfFrontmatter and resource-policy), explicit `path.win32` / `path.posix` (imageReference:26,
mystTargets:102: flavour chosen by whether the input is a Windows path). Other `path.*` hits are not node:path
(`file.path.split`, a local string in frontmatterValues).

.dependency-cruiser.cjs today:
- NODE_DEBT pure-path entries (PATH_SHIM): okfFrontmatter, imageReference, mystTargets, mystRenderer, plantUmlIncludes,
  renderPipeline. Mixed entries listing "path" beside other built-ins: fileLinks, stemIndex, confLocator, documentGlob,
  plantUmlRenderer, resource-policy.
- `core-no-node-builtins` exempts NODE_DEBT files; `core-node-debt-is-bounded` is generated per entry.
- Session already has `session-node-builtins-path-only` (allows only `path`); the request says session has no rule, so
  it is a tightening: replace by a no-built-in rule.
- `page-reaches-no-node-builtins` (reachable): the new module must stay unreachable from src/page (true today).
- No test in test/ exercises the cruiser config; only `just check-boundaries` (scripts/check-boundaries.mjs,
  transpiles src per file with esbuild, cruises out/boundaries).

## Smallest change

1. New `src/core/path/hostPath.ts`: `export * from "node:path";` (carries win32, posix, sep, parse and every function
   used; Node semantics unchanged, so Windows drive/UNC/backslash behaviour is identical by construction). No wrapper or
   re-implementation. Doc comment: a browser build swaps it.
2. In the 25 files replace the `node:path` import by a relative import of that module; call sites untouched.
3. `.dependency-cruiser.cjs`: add one NODE_DEBT entry `src/core/path/hostPath.ts` -> builtins ["path"], the only `path`
   entry; drop the 6 pure-path entries and the PATH_SHIM constant (or reword it for the single entry); remove "path"
   from the 6 mixed entries (fs / child_process stay). Replace the session rule with `session-no-node-builtins`
   (to: dependencyTypes core, no exception). Update the header comment and the NODE_DEBT doc.
4. CONTRIBUTING.md "Architecture" and any text saying session may import path (grep when implementing).

## esbuild alias feasibility

esbuild `alias` rewrites bare specifiers, not relative ones. Only hostPath.ts imports `node:path`, so a browser build
can set `alias: { "node:path": "<posix shim>" }` (precedent: scripts/page-bundle.mjs aliases `js-yaml` to
scripts/js-yaml-shim.mjs). Feasible. Constraint for that later shim: it must export `win32` and `posix` (used by
imageReference and mystTargets), `parse`, `sep`; path-browserify has `posix` but no real `win32`, so the shim needs a
win32 export. Out of scope; note it in the hostPath comment. Node bundles unchanged.

## Test placement

- Unit test `test/core/path/hostPath.test.ts`: exports identical to `node:path` (`win32`, `posix` same objects), plus
  win32 samples (`C:\a\b`, `\\server\share\x`, drive root via `parse().root`, `relative` across drives) giving the node
  results. Guards the Windows semantics.
- Boundary proof: `just check-boundaries` green; negative proof by temporarily adding a `node:path` import to a session
  file and to a core file, capture the rule names, revert.
- `just check` (Windows here; Linux in CI).

## Requirements impact

Pure refactor, no behaviour: no new SwRS. Markers stay with their files. Run `just check-markers` and
`just requirements-update`; a log entry in requirements/tiers/log.md only if project.guidelines.md "During a change"
calls it substantive (likely not). If check-unused-exports flags the `export *`, use scripts/unused-exports-allowlist.json.

## Overlap with open PRs

- #482 (CR-468, file-system port): touches .dependency-cruiser.cjs, core/frontmatter/{fileLinks,okfFrontmatter,stemIndex,
  linkFiles,fileLinkTypes}, session/features/{frontmatter,links}.ts, requirements log. It rewrites the fileLinks/stemIndex
  NODE_DEBT lines (drops fs).
- #481 (CR-467, WebCrypto): touches .dependency-cruiser.cjs (commentStore, csp entries), requirements log; no path imports.
- Avoidance: implement after #481 and #482 merge (the request says so), rebase onto main, then do the swaps and the
  cruiser edit on their final text. Change only per-entry lines and the session rule in the cruiser file; add the new
  entry at the top of NODE_DEBT (separate hunk). In the shared source files only the single import line changes
  (one-line hunks). Log: append, keep both. If #482 is still open, swap its files (fileLinks, stemIndex, okfFrontmatter,
  session links.ts) last, after rebasing.

## Risks

- Relative import depth errors (the compile catches them). No cycle: hostPath imports nothing local.
- A page-bundled core module importing hostPath would trip `page-reaches-no-node-builtins` (desired).
- Linux only runs in CI.

## Questions for the user

None. Location `src/core/path/hostPath.ts` is my choice (request: "for instance src/core/path/").

## Evidence plan

Kind: internal refactor, nothing to see in the UI; no screenshot.
- Logs in work/gates/*.log: `just check-boundaries` before and after; `grep -rn "node:path" src` before (25 importers in
  core and session) and after (only src/core/path/hostPath.ts in those layers).
- New unit test output (win32 / UNC / drive parity); existing path-heavy suites (imageReference, mystTargets,
  okfFrontmatter, plantUml includes, session links) green and unchanged.
- Negative proof: cruiser error text for a temporary `node:path` import in a session file and in a core file, reverted.
- `just check` on Windows green; `just preflight` static stage as the gate; Linux via the PR's CI.
- Cannot show: the browser-build swap (a later CR), a local Linux run.
