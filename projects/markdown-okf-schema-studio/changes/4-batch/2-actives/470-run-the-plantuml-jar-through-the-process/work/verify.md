# Verify CR-470

Head: 2a19650a5f28207aa3b33e6d2b83e194e3748896

All claims judged at 2a19650a.

- Core no longer imports child_process/fs in the PlantUML renderer: `grep -n "^import" src/core/render/plantUmlRenderer.ts src/core/render/plantUmlHost.ts` shows only node:path, parse5 and local imports. NODE_DEBT entry keeps `builtins: ["path"]` (`git diff origin/main...HEAD -- .dependency-cruiser.cjs`). `just check` runs check:boundaries: "no dependency violations found (447 modules)".
- Jar runs through the port: renderer calls `processes.run(... maxStdoutBytes: MAX_PLANTUML_OUTPUT_LENGTH)` and `files.stat`, handles `result.outputExceeded` (lines 87, 301-310).
- Capability fallback: `engineFor` returns "builtin" when `!capabilities.processes` (diff of src/session/features/plantUml.ts); renderer without `processes`/`files` takes the refusal branch (line 350); test at test/session/diagReq.plantuml.requirements.test.ts:133 with `processes: false`; DIAG-089 gains the scenario.
- Bounded output, early kill, signal, process-group kill: diff of src/host-api/processRunner.ts and src/node-services/processRunner.ts; tests in test/node-services/processRunner.test.ts (maxStdoutBytes, bytes vs chars, maxStderrChars, signal, group kill with posixOnly skip on win32, EPIPE).
- Gate: `just check` at the head, exit 0 (log: work/verifier/check.log): unit 4984 tests, 4963 pass, 0 fail, 21 skipped; contracts 102 tests, 0 fail; format, compile, boundaries, limits, exports, markers, settings, requirements-lint, check:diagrams all passed.
- Known gaps (POSIX-only tests skipped on Windows, EPIPE message change, no Windows group kill) match the code and tests above.
- PR body: sections render, Summary/Changes match the 27-file diff, no images. Test-plan boxes are unchecked (Driver's to tick); "tests fail on the previous code" was not run by me (not proven by a before run; the replaced tests construct a fake ProcessRunner that the old code does not accept).

VERIFIED
