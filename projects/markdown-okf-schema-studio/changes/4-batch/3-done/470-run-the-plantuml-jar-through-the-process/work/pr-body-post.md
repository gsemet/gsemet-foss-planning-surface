
The PlantUML renderer in `src/core` imported `child_process` and `fs`, which a browser-capable host cannot provide. It now runs the jar through the `ProcessRunner` port and reads files through the `FileSystem` port; when the host has no `processes` capability, the session falls back to the JS engine, as it does when no jar is configured. Part of #413.

## Deliverables

```mermaid
flowchart LR
  R[core: plantUmlRenderer] -->|PlantUmlProcesses| P[host-api: ProcessRunner]
  R -->|PlantUmlFiles| F[host-api: FileSystem]
  P --> N[node-services: processRunner]
  S[session: engineFor] -->|capabilities.processes false| B[builtin JS engine]
  S -->|processes true| R
```

## Changes

- `plantUmlRenderer.ts` spawns the jar via `processes.run` and stats via `files.stat`; new `plantUmlHost.ts` holds the structural ports (core cannot import `host-api`).
- `session/features/plantUml.ts` picks the builtin engine when `capabilities.processes` is false.
- `ProcessOptions` gets a bounded-output option (early kill, as the renderer had); `ProcessResult.signal` added; the node runner reports it and kills the process group on POSIX.
- `NODE_DEBT` entry of the renderer keeps only `path`.
- Tests on a fake `ProcessRunner` (jar run, jar missing, no processes capability) and on the node runner; DIAG-089 gains a scenario.

## Impacts

No visible change: the same jar, arguments, caps and messages run through the port.

## Blast radius

Grade: 2. The shared `ProcessRunner` port and node runner change (detached child, `signal`, output cap), and every jar diagram goes through them. A plain revert restores the previous behaviour.

## Test plan

- [x] New or changed tests: the fake-runner and node-runner tests need the new port (the previous code does not accept the fake), verified at 3f6d3ef; a before-run on the old code was not made
- [x] Requirements: SwRS updated (DIAG-089), markers kept, `just requirements-update`
- [x] Changelog: No user-facing change
- [x] Local gates at 3f6d3ef: `just check` exit 0 (run by the conflict-resolver on the restacked tree; earlier run at 2a19650: unit 4963 pass, 0 fail, 21 skipped)
- [x] Review: approved at 3f6d3ef (restack onto CR-471, conflict resolved; rest carried from 2a19650)
- [ ] Verified at 3f6d3ef
- [ ] CI green at 3f6d3ef

## Known gaps

- The POSIX-only runner tests (process-group kill, signal) are skipped on Windows; Linux CI runs them.
- A stdin EPIPE now shows as "PlantUML exited with code N: <stderr>" instead of the raw "write EPIPE" (the runner ignores stdin errors).
- Windows has no process-group kill (unchanged).
- The new tests were not run against the previous code (they need the new port, which it does not accept), and there is no before/after evidence: the change has no visible output.

## Autonomous decisions

Taken without the owner:

- Core-local structural port interfaces, because `core` may not import `host-api`.
- The stdin EPIPE diagnostic change above, and the runner ignoring stdin errors.
