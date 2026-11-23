## Summary

The conf.py lookup, the toctree glob expansion and the local-resource security checks read the disk with Node's `fs` directly. That blocks running the renderer in a browser-capable host. They now go through the async `FileSystem` port. Part of #413.

## Deliverables

```mermaid
flowchart LR
  confLocator --> FS[FileSystem port]
  documentGlob --> FS
  resourcePolicy --> FS
  FS --> Node[Node FileSystem]
  FS --> Mem[MemoryFileSystem, now with symlinks]
```

## Changes

- `confLocator`, `documentGlob` and `resource-policy` use the async port; callers (include, diagram-file and glob stages, webview build, conf events, render worker) became async.
- The resource policy primes its realpath memo asynchronously before the synchronous HTML sanitizer runs; the refusal of paths outside the allowed roots, symlinks included, is unchanged.
- The port interface lives in `src/core/files/fileSystem.ts` (host-api re-exports it) so core need not import host-api.
- `MemoryFileSystem` gained symlinks, with a symlink-escape test.
- `fs` removed from the three `NODE_DEBT` entries.

## Impacts

No visual change; same conf.py, toctree expansion and allowed/refused resources.

## Blast radius

Grade: 2. Shared render path became async; a revert restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS markers updated, `just requirements-update`
- [x] Changelog: No user-facing change
- [x] Local gates: compile, test:unit (4955), test:security (103), check-boundaries, check, preflight static stage
- [ ] Review
- [ ] CI green
