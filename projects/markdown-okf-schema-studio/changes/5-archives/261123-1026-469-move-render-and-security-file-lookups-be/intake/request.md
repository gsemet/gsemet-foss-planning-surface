# Move render and security file lookups behind the async FileSystem port

issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/413

Part of issue #413 (browser-capable host), the PORT_FOLLOW_UP debt of `.dependency-cruiser.cjs`,
second half: the render and security side.

- `src/core/myst/confLocator.ts` (sync search of the governing `conf.py`),
  `src/core/render/documentGlob.ts` (sync toctree glob expansion) and
  `src/core/security/resource-policy.ts` (realpath checks of local resources; missing from the
  issue's list) stop using `fs` and go through the async `FileSystem` port of `src/host-api/`
  (extend the port if needed, with its Node and in-memory implementations).
- Callers become async; no synchronous file-system access remains on the render path for these
  three. The resource policy keeps its security guarantee (a path outside the allowed roots,
  symlinks included, is still refused).
- Behaviour unchanged for the user: same `conf.py` found, same toctree expansion, same resources
  allowed and refused; watch for render timing changes.
- Remove the `fs` built-in from the three files' `NODE_DEBT` entries (keep `path` until the
  path-facade CR lands); `just check-boundaries` passes.
- Tests: unit tests on `host-memory`'s `MemoryFileSystem`, including a symlink escape case for the
  resource policy where the in-memory port can express it.
