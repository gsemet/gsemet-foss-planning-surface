# Verify CR-444

Head: e293b928a6b1d5ae25063225ed82396e78c98de9

Verdict: NOT VERIFIED (only the PR description claim fails; the code claims hold)

## Claims

1. Long gate passed at the head (e293b928). Proof: gate log first line
   `gate CR-444 branch chantier/batch-07/cr-444-show-blank-line-runs-as-a-reachable-blan head e293b928a6b1d5ae25063225ed82396e78c98de9`,
   last line `result: pass at e293b928a6b1d5ae25063225ed82396e78c98de9` (work/gates/20261121-043324.log).
2. Unit, page and session suites pass at e293b928. Command: `npm run compile` then
   `node scripts/node-test.mjs unit "out/test/{core/mapping,core/render,core/export,core/protocol,session,page}/**/*.test.js"`
   -> `tests 3172, pass 3168, fail 0, skipped 4` (skips are Windows symlink tests).
3. The new spec checks exist and pass (blankRuns, blockRange isCommonMarkBlank/checkBlankRun/planBlankRunRemoval/Paste, insertion,
   render marker, export, validators, session blankRunHost, page runtimeBlankLines). Command:
   `node scripts/node-test.mjs unit "out/test/{core/mapping/blankRuns,core/mapping/blockRange,core/mapping/insertion,core/render/blankRunsList,core/export/htmlExport,core/protocol/pageToHost,session/blankRunHost,page/runtimeBlankLines}.test.js"`
   -> `tests 160, pass 160, fail 0`; 58 of the test names mention blank (work/verifier/targeted-tests.log).
4. Spec wiring read at the head (grep): export removes both attributes (`exportContent.ts:40`), host appends
   `<div hidden data-okf-blank-runs=...>` (`renderPipeline.ts:256`), `op: "delete-blank-lines"` in `hostToPage.ts:124` and
   `sourceEdits.ts:519`, host-only `blankRunRegion` in `blockEdits.ts:52`, held-edit refusal on a differing run (`blockEdits.ts:523`),
   page reads the host element from the content children, skipping page-made blocks (`blankLines.ts:48-53`).
5. Requirements: `just requirements-lint` -> `use case diagrams: 93 StRS checked, all parse` (exit 0).
6. CI at the head (`gh pr checks 453`): static, static-windows, visual, report, checks pass; integration, stress skipping
   (heavy run 44862880704 in progress, not proved here).
7. Review box: driver notes `r3 inspector approved at ccf9ff75` and `r3 approved at ccf9ff75, committed as e293b928` exist in
   `chantier log` (the Foreman note says rounds 1-2 approved at 67ecf991 and ccf9ff75).
8. Images (opened, e293b928 code, captured by the coder): edit mode shows a dashed "Blank lines (3)" block between two
   paragraphs; selected shows the selection outline and the Delete block button (x) at the left; reading mode shows no block.
   No username or home path on screen in any of the three. They are not yet attached to the PR.

## Failed

- PR description as posted (`gh pr view 453 --json body`):
  - Impacts says "Screenshots are added below once verified" and no image is attached;
  - no Known gaps section, though real gaps exist: kept-editor path in `contentPatch.ts` across a patch not run in real VS Code,
    integration/stress not run at the head (heavy run in progress), full visual suite not run locally;
  - Test plan boxes "Local gates", "Review", "CI green" are unchecked although the gate passed and the review is approved.
  The Summary, Deliverables and Changes match the diff (57 files vs the CR-439 base).

## Not proved

- Real VS Code scenario (spec Integration 1-5, LF and CR LF): not run at this head; heavy CI run pending.
- Kept editor across a content patch in real VS Code (page-level test passes in runtimeBlankLines).
- Minor: the label reads "Blank lines (3)", the spec example reads "N blank lines"; not a claim failure.

NOT VERIFIED
