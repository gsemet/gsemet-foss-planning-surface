Head: 2d7152e32a028f64683841bb27f7b93b23017a1a

All claims judged at 2d7152e32a028f64683841bb27f7b93b23017a1a (before: origin/main d9b3cd6b).

1. fs gone from the three files, NODE_DEBT keeps only path. Command: `grep -nE "\bfs\b|node:fs|readFileSync|existsSync|realpathSync|statSync|readdirSync" src/core/myst/confLocator.ts src/core/render/documentGlob.ts src/core/security/resource-policy.ts` -> no output; `.dependency-cruiser.cjs` lines 50-53, 63-64 show builtins: ["path"] only. PASS.
2. `just check-boundaries` -> "no dependency violations found (447 modules, 1241 dependencies cruised)" / "check-boundaries: passed (387 modules)". PASS.
3. `just compile` ok; `npm run test:security` -> tests 106, pass 104, fail 0, skipped 2; `npm run test:unit` -> tests 4982, pass 4965, fail 0, skipped 17. PASS.
4. Symlink escape on MemoryFileSystem: test/security/resource-policy.memory.test.ts (symlink-escape code for a file link and a linked folder, inside link served, unprimed refusal) and test/host-memory/memoryFileSystem.symlink.test.ts, both inside the passing suites of claim 3. PASS.
5. Behaviour parity: before/after render of the fixture, `diff -r` of render.html and meta.json: IDENTICAL (same conf.py extensions [colon_fence, deflist, dollarmath], same toctree expansion a.md b.md, same include, same outside-root refusal diagnostic). See verifier/evidence/before-after.md. PASS.
6. Render timing: median renderMs 7.59 before, 10.36 after (+~3 ms, small fixture, 15 runs). Observation for the Driver: the CR asked to watch timing; the PR description does not mention it. Not a failure.
7. PR description (#483, head 2d7152e, body equals pr-body.md): renders, Summary/Changes match the diff (async port use, prime of the realpath memo, core/files/fileSystem.ts, MemoryFileSystem symlinks, NODE_DEBT); no image; Known gaps absent and no UNVERIFIED claim exists; test counts stated (4955) are older than the 4965 now, a stale figure only. Review box unchecked, no Review claim. PASS.
8. Gate: no long gate pass exists at this head (ship note: "no long gate passed at 2d7152e"); no claim here needs only the long suite; CI at 2d7152e green per Driver note (checks, report, static, static-windows, viewer-graph, visual). Not run by me.

VERIFIED

---
Description pass at 2d7152e32a028f64683841bb27f7b93b23017a1a (posted body, gh pr view 483):

- Timing line (7.6 ms to 10.4 ms, 15 runs): matches claim 6. PASS.
- CI line: matches the Driver note at 2d7152e (checks, report, static, static-windows, viewer-graph, visual pass). PASS.
- Review line: matches r1/r2/r3 inspector approvals in the log (last approved at f773797, committed b52d710; head 2d7152e later fix commits). PASS.
- test:unit (4965): matches claim 3. PASS.
- test:security (103): FAIL. claim 3 output at this head is tests 106, pass 104, skipped 2; the body says 103.
- "preflight static stage" as a local gate at this head: FAIL. No proof at 2d7152e in verify.md; the log only has a preflight static note at 1944362.

NOT VERIFIED (description only)

---
Description pass 2 at 2d7152e32a028f64683841bb27f7b93b23017a1a (posted body re-read, gh pr view 483; gh pr checks 483):

- test:security "106 (104 pass, 2 skipped)": matches claim 3. PASS.
- test:unit 4965: matches claim 3. PASS.
- Local gates "just check pass" at 2d7152e: log note 09:01:48Z "before push at 2d7152e: just check: pass". PASS. The preflight static claim is gone.
- CI line (static, static-windows, viewer-graph, visual, report, checks green at 2d7152e): gh pr checks 483 shows pass for all of them. PASS.
- Review and Verified lines match the log (r1/r2/r3 approved; VERIFIED at 2d7152e). Timing line matches claim 6. PASS.

VERIFIED (description)
