## Summary

The PlantUML renderer in `src/core` no longer imports `child_process` or `fs`: the jar runs through the `ProcessRunner` port and file access goes through core-local structural interfaces matched by the `FileSystem` port. When the host has no `processes` capability, the session falls back to the JS engine, as it does when no jar is configured. Part of #413.

## Changes

- `plantUmlRenderer.ts` spawns the jar via `processes.run` and stats via `files.stat`; new `plantUmlHost.ts` holds the structural ports (core cannot import `host-api`).
- `session/features/plantUml.ts` picks the builtin engine when `capabilities.processes` is false.
- `ProcessResult.signal` added; the node runner reports it and kills the process group on POSIX.
- `NODE_DEBT` entry of the renderer keeps only `path`.
- Tests on a fake `ProcessRunner` (jar run, jar missing, no processes capability); DIAG-089 gains a scenario.

## Impacts

No visible change.

## Changelog

No user-facing change.

## Known gaps

- The POSIX-only runner tests (process-group kill, signal) are skipped on Windows; Linux CI runs them.
- A stdin EPIPE now shows as "PlantUML exited with code N: <stderr>" instead of the raw "write EPIPE" (the runner ignores stdin errors).
- Windows has no process-group kill (unchanged).

## Autonomous decisions

- Core-local structural port interfaces, because `core` may not import `host-api`.
