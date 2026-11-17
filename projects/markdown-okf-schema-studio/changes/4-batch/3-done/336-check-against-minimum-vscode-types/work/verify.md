# Verify CR-336

Head: 5f828f02e29e2a6c9fd841a8242de4c75f9447da

Gate: waived (O-1). `npm` is not on PATH in this session, so the scripts' own command was run through node
(`node node_modules/typescript/bin/tsc ...`, the exact body of `check:min-vscode` and `check-types`).

Verdict: VERIFIED

## Claims (all judged at 5f828f02)

1. `check:min-vscode` passes on current src/.
   `node node_modules/typescript/bin/tsc --noEmit -p tsconfig.vscode-min.json` -> `min exit 0`.
   `tsc --noEmit -p tsconfig.json` -> `types exit 0`.

2. The check bites. Probe appended to src/extension.ts: `type Probe = typeof vscode.lm.registerMcpServerDefinitionProvider;`
   - min: `src/extension.ts(54,31): error TS2339: Property 'registerMcpServerDefinitionProvider' does not exist on type 'typeof lm'.` `min exit 1`
   - main type-check: `types exit 0`
   Probe reverted with `git checkout src/extension.ts`; `git status --short` empty.
   (A first probe using `vscode` as a value hit TS1361 in both configs because of `import type`; discarded, not counted.)

3. `just check` runs it: `justfile:162: check: format compile check-min-vscode ...`; recipe at justfile:134 runs `{{ npm }} run check:min-vscode`;
   `ci-static` (justfile:275-278) runs `just check`. CI at this head: `gh pr checks 406` -> static pass, static-windows pass, visual pass.

4. Lock: `package-lock.json:2530` `node_modules/@types/vscode` version 1.140.0; `:2537` `node_modules/@types/vscode-min` name @types/vscode version 1.95.0.
   Installed: `node_modules/@types/vscode-min/package.json` 1.95.0, `node_modules/@types/vscode/package.json` 1.140.0.

5. `just update` rejects the alias: `just --dry-run update` prints `ncu --upgrade --reject @types/node,@types/vscode,@types/vscode-min ...`.

6. PR 406 description (as posted, headRefOid 5f828f02): explains why the alias is needed (two versions side by side, npm cannot install two
   versions under one name); CR numbers only under Internal references; Summary, Deliverables and Changes match
   `git diff --stat origin/main...HEAD` (CONTRIBUTING.md, justfile, package-lock.json, package.json, tsconfig.vscode-min.json); Known gaps
   (Windows tableBreakout, identical on base) matches work/diagnosis.md. Test-plan boxes keep `<sha7>` placeholders, unchecked, for the Driver to fill.

Not checked here: the Review box (unchecked in the posted body), `just format`.

Evidence: none required, no visible change (before-after.md not applicable).

VERIFIED

## Description-only pass (PR 406 body as posted, head 5f828f02e29e2a6c9fd841a8242de4c75f9447da)

Command: `gh pr view 406 --json body,headRefOid` -> headRefOid 5f828f02e29e2a6c9fd841a8242de4c75f9447da. Code unchanged; claims 1-5 carried from the pass above (same SHA).
- Test plan boxes checked, all naming `5f828f0`: CI green at 5f828f0 holds (`gh pr checks 406`: static, static-windows, visual, checks, report pass; rest skipping). Review: `chantier log` note "r2 approved at 6afd12d6, committed as 5f828f02" matches. Verified at 5f828f0: earlier VERIFIED verdict at this head. Local gates `just check-min-vscode` passes (claim 2/3 above; the driver's preflight run reported all but tableBreakout passing); `just format` relies on that gate run, not re-run here.
- Internal references: CR-336 and CR-339 appear only under Internal references; no role names elsewhere.
- Known gaps (tableBreakout fails on Windows, identical on base, Linux CI is the check, follow-up CR) matches work/diagnosis.md.
- Renders: sections, code block and the details fold are well formed; no images.

VERIFIED
5f828f02e29e2a6c9fd841a8242de4c75f9447da
