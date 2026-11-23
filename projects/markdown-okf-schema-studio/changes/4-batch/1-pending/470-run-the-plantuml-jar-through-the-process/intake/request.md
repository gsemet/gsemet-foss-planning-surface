# Run the PlantUML jar through the ProcessRunner port

issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/413

Part of issue #413 (browser-capable host).

- `src/core/render/plantUmlRenderer.ts` stops importing `child_process` and `fs`: the jar is spawned
  through the existing `ProcessRunner` port of `src/host-api/`, and any file access goes through the
  `FileSystem` port.
- The jar is a capability: when the host has no `ProcessRunner` (`capabilities.processes` false),
  the renderer falls back to the JS engine (`@plantuml/core`) as it does today when no jar is
  configured. Keep `core` free of the DOM-only `@plantuml/core` import (dependency-cruiser rule
  `core-no-dom-packages`): the fallback stays where it lives today.
- Behaviour unchanged in VS Code: same diagrams, same errors shown when the jar or Java is missing.
- Remove `child_process` and `fs` from the file's `NODE_DEBT` entry (keep `path` until the
  path-facade CR lands); `just check-boundaries` passes.
- Tests: a fake `ProcessRunner` in a unit test (jar run, jar missing, no processes capability).
