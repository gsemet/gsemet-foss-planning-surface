# Put core and session path arithmetic behind one path module

issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/413

Part of issue #413 (browser-capable host), the PATH_SHIM debt of `.dependency-cruiser.cjs`.

- Today the `core` files listed under PATH_SHIM in `NODE_DEBT` (`okfFrontmatter.ts`,
  `imageReference.ts`, `mystTargets.ts`, `mystRenderer.ts`, `plantUmlIncludes.ts`,
  `renderPipeline.ts`, and the `path` left in the files of the other #413 CRs) and 13 files of
  `src/session/` import `node:path` directly.
- Add one host-neutral path module in `core` (for instance `src/core/path/`) that every `core` and
  `session` file imports instead of `node:path`. In the Node build it is `node:path` (Windows paths
  must keep working exactly as today); a later browser build swaps it for a posix shim by an esbuild
  alias. This module is the only `NODE_DEBT` entry left for `path`.
- dependency-cruiser: `core` and `session` import no Node built-in except through that module; add a
  rule for `session` too (today it has no Node built-in rule). Empty the other `path` entries of
  `NODE_DEBT`.
- No behaviour change, on Windows above all (drive letters, backslashes, UNC paths): `just check`
  passes on Windows and Linux.
- This CR runs after the other #413 CRs of the batch where possible, so it starts on their work and
  touches each import once.
