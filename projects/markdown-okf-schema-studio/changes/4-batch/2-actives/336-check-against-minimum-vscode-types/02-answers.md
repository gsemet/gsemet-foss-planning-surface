# Answers

Short name: `min-vscode-types`

## 2026-11-17: triage

Owner, 2026-11-17, on the proposal to mark both remaining inbox CRs automatable and run them in a direct parallel batch: « Yes, run them ».

- Automatable: the Driver works from the request alone, no reviewed specification.

## 2026-11-17: answers to the blocked hand-back (ask A-2)

1. min-vscode-types-Q1: **Long gate red on Windows on a pre-existing test.** Asked: open the PR
   relying on Linux CI with a separate CR for the Windows test (recommended), or fix that test
   first. Owner: « 1. oui fix ». Read as: yes, open the PR, and file a CR that fixes the test
   (`test/page/tableBreakout.test.ts:398`, fails on origin/main 16105e0f on Windows). Recorded as
   a long-gate waiver for this CR with that CR as its follow-up.
2. min-vscode-types-Q2: **New devDependency** `@types/vscode-min` = `npm:@types/vscode@1.95.0`
   (exact-pinned alias, existing npm registry, one lock entry). Owner: « 2. oui mais je ne
   comprends pas pourquoi c est necessaire ». Approved; the PR body explains why the alias is
   needed (two versions of the same types package side by side).
3. **Archive in the PR** (the Driver's third question): decided by the Chief of Staff, no owner
   question: no archive in the PR. `.agents/changes/` is gitignored in the project since its CRs
   live in the planning surface; the project's rules rank above chantier's `archive:` line.
