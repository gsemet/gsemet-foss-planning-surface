# Move frontmatter file lookups behind the async FileSystem port

issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/413

Part of issue #413 (browser-capable host), the PORT_FOLLOW_UP debt of `.dependency-cruiser.cjs`,
first half: the frontmatter side.

- `src/core/frontmatter/fileLinks.ts` (sync existence checks of linked files) and
  `src/core/frontmatter/stemIndex.ts` (sync walk of the workspace for filename stems) stop using
  `fs` and go through the async `FileSystem` port of `src/host-api/` (extend the port if a needed
  operation is missing, with its Node and in-memory implementations).
- Callers become async; no synchronous file-system walk remains on the render path for these two.
  The stem index may be built ahead (cached, refreshed on watcher events) so rendering does not wait
  on a walk; say the choice in the PR.
- Behaviour unchanged for the user: linked-file checks and stem lookups give the same results; watch
  for render timing changes (a first render before the index is ready must not show wrong
  "missing file" states, or must re-render once ready).
- Remove the `fs` built-in from both files' `NODE_DEBT` entries (keep `path` until the path-facade
  CR lands); `just check-boundaries` passes.
- Tests: unit tests on `host-memory`'s `MemoryFileSystem` for both modules.
