# Verify CR-470

Head: 3f6d3efb6123372cce02bd738914f706f47bab2a

Move 2a19650..3f6d3efb (restack onto CR-471, conflict resolved). Judged again at 3f6d3efb: every claim whose proof runs the renderer, boundaries or tests (the move touched them).

- Core imports no child_process/fs/node:path in the PlantUML renderer, judged at 3f6d3efb: `grep -n "^import" src/core/render/plantUmlRenderer.ts src/core/render/plantUmlHost.ts` shows `../path/hostPath`, parse5 and local imports only. The NODE_DEBT entry is dropped (conflicts.md; description now says so? see description claim). `just check` boundaries: "no dependency violations found (449 modules, 1242 dependencies cruised)".
- Jar runs through the port, judged at 3f6d3efb: `grep -n "processes.run|outputExceeded|files.stat" src/core/render/plantUmlRenderer.ts` shows files.stat (88, 228, 247), processes.run (302), outputExceeded (311).
- Gate, judged at 3f6d3efb: `just check` exit 0 (log: work/verifier/check-3f6d3efb.log): unit 5000 tests, 4979 pass, 0 fail, 21 skipped; contracts 106 tests, 104 pass; format, compile, boundaries, limits, exports, settings, requirements-lint, check:diagrams passed. This covers the fallback test (diagReq.plantuml, processes:false), the node processRunner tests and the port-based renderer tests.
- Capability fallback, bounded output, early kill, signal, process-group kill: carried from 2a19650: src/session/features/plantUml.ts, src/host-api/processRunner.ts and src/node-services/processRunner.ts are in the CR's diff unchanged by the restack, and their tests pass in the check above.
- Known gaps (POSIX-only tests skipped on Windows, EPIPE message, no Windows group kill, no before-run) match the code.
- PR description at 3f6d3efb: sections render, mermaid diagram, no images; Summary/Changes match the 27-file diff vs base 792ae892 (renderer, plantUmlHost, session feature, runner port and node runner, tests, SwRS DIAG-084/089/097, log). The Changes line "NODE_DEBT entry of the renderer keeps only path" is stale after the restack: the entry is removed (the diff touches .dependency-cruiser.cjs with 3 deletions; the renderer has no node:path import). Minor inaccuracy; the description's claim contradicts the diff.
- Review box: inspector approval at 3f6d3efb is in `$CHANTIER log CR-470` per the brief. Verified/CI boxes unticked as agreed.

PR description re-checked at 3f6d3efb after the Driver fix: `gh pr view 487 --json body` Changes now says the renderer imports ../path/hostPath and no node:path, so its NODE_DEBT entry is removed; this matches the diff. The description is otherwise unchanged and consistent.

VERIFIED
