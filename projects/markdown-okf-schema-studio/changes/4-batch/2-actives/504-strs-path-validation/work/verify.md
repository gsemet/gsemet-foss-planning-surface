# Verify CR-504 (CR-A)

Head: afbb55c527217ec66537dff308bbcfb5d05b25c8

All claims judged at `afbb55c5` unless marked `carried`. Base `4a47151e8d055b7f096b69b1fca2d9bf9636f863`. `<W>` is the CR worktree, `<CR>` the CR folder, `V` is `<CR>/work/verifier`.

## Verdict: NOT VERIFIED

Six claims fail (A to F below). The two failures of the verdict at `77a8d07` (wrong new-mode figures in the body; viewer, justfile, skill refresh and glossary absent) are fixed. No coder round is left, so A, D, E and F are code or marker gaps to hand back; B and C are body gaps.

## Gate

- `<CR>/work/gates/preflight-afbb55c.log`, first line: `CR-504 preflight at afbb55c527217ec66537dff308bbcfb5d05b25c8`.
- Last line: `preflight exit 0; requirements-lint exit 0; head afbb55c527217ec66537dff308bbcfb5d05b25c8; dirty 0`.
- Same log: `check-markers: 10 companion file(s), 458 in-force SwRS marked, 16 files on the marker baseline`; node tests `5249 / pass 5228 / fail 0 / skipped 21`; `206 passed` (pytest); `main paths: 96 StRS checked, 625 SwRS citations, all valid`; `use case diagrams: 94 StRS checked, all parse`.
- `$CHANTIER handoff CR-504`: `[ ] long gate passed (... none in chantier.yaml ...; none in the project's rules: handback CR-504 ready --no-gate "<rule>")`, `[ ] verdict VERIFIED`. The project gate is `just preflight` (static stage on Windows); no gate was run by this Verifier.

## Claims that hold

1. Head and PR. `git -C <W> status --porcelain --branch`: branch up to date with its remote, no change. `rev-parse HEAD` and `ls-remote origin <branch>`: `afbb55c5...`. `gh pr view 524`: `OPEN draft=True head=afbb55c5... title=build: declare StRS paths and SwRS scenarios on okf-schema 0.18`.
2. CI. `gh pr checks 524`: `static`, `static-windows`, `viewer-graph`, `visual`, `report`, `checks` pass; `integration`, `stress`, `release-check`, `toc-loop`, `gallery`, `pages`, `release`, `tag-release` skipping.
3. Review box. `$CHANTIER log CR-504`: `r5 approved at 77a8d074 (body-only re-inspection APPROVE), committed as afbb55c`.
4. Config and pin (diff against base). Coverage mode unchanged; `markers.accepts: '@accepts_req'`; `accepted_in_files` in `generated_fields`; `okf-schema>=0.18.1`; `uv.lock` 0.18.1 (base 0.17.0). `git diff <base> <head> -- src .github package.json package-lock.json` is empty.
5. Declarations and marker rules. `uv run --no-project --with pyyaml python -I V/scan.py <W> afbb55c5...`:
   - `requirements 1227; live StRS 95; live SwRS 460 (non-exempt 458, exempt 2: TRUST-070, TRUST-075); retired 672`
   - `declaration problems: 0`; `live StRS with scenarios: 95 / 95`; `live non-exempt SwRS with scenarios: 458 / 458`; `approved SwRS: []`; `retired SwRS without exemption+reason: 0`
   - `marker lines: tests 5543, accepts 62, implements 1517`; all eight violation counts 0
   - `SwRS scenarios 2622, unmarked 722` (per group as in the body); `StRS paths 156, unmarked 94`; `live StRS with no @accepts_req: 38`; `paths accepted 60, tests_req 2`
   - `LIFE-023` four paths, markers `[]`; TRUST-012 S1/S2 `tests_req` in test/security; TRUST-014 S1 `accepts_req` in test/security; `live SwRS with a test marker: 460` (also at each CR commit).
6. New-mode validation (old failure A, fixed). `sh V/newmode.sh <W> <scratch> e5ee7ec1 06b301d1 d245fc02 77a8d074 afbb55c5` (okfreq 0.18.1 on a `git archive` copy with the mode switched): 0 errors on every commit; head `errors 0 warnings 64 : W004 x38, W2 x26`.
7. D5, approved StRS, requirement text. `V/reqdiff.py <W> <base> <head>`: one added requirement (SwRS-CORE-096); 97 retired SwRS exempted (92 superseded, 5 deprecated), none approved; the 15 approved StRS change only `approved_at` (`2026-11-25T15:37:43+01:00`), `verified.at`, `scenarios:` and heading ids; `approved_by` unchanged. Body text changes only in BLOCK-027, CORE-007 (generated link), TRUST-012, TRUST-014, CORE-069/080/082.
8. Baseline. `strsTestsInIntegration` is empty and `blocks` only shrinks (carried from 77a8d07: `git diff 77a8d074 afbb55c5 -- scripts/marker-baseline.json` is empty).
9. Each D10 rule has a test that fails on the old script (carried from 77a8d07: `git diff 77a8d074 afbb55c5 -- scripts/check-marker-companions.mjs test/build/checkMarkers.test.ts` is empty): compiled head test against the base script, `pass 6, fail 8`.
10. Unit tests. `fnm exec -- node scripts/node-test.mjs unit "out/test/site/**/*.test.js" "out/test/build/checkMarkers.test.js" "out/test/build/mutationReport.test.js"`: `tests 227, pass 226, fail 0, skipped 1`.
11. Viewer tests fail on the old code. Head viewer tests against base viewer sources in a scratch folder (`node --test` on model, home, pages, write, mainPaths): `tests 40, pass 21, fail 19`; every new test is among the failures. Mutation report: the base regex cannot match `#S<n>`, so the new `mutationReport` test fails on base (code read).
12. Justfile, docs, skills (old failure B, fixed). `git diff <base> <head>`: both report targets write `requirements-trace.json`; CONTRIBUTING, project guidelines (D14) and the five glossary terms are there; the vendored skills and `requirements.guidelines.md` equal a fresh okfreq 0.18.1 output plus the "Studio benches" note; `log.md` has the `2026-11-25` entry.
13. Changes beyond markers. `V/codediff.py` and `V/splitcheck.py <W> <base> <head>`: other code changes only in docs, skills, justfile, pyproject, lock, check script, baseline, scripts/mutation/report-pure.mjs, test/build, split test files and viewer files; the split files lose no assertion.
14. Owner steps 1 to 4, on the site built at base and at head (`V/buildsite.cjs`, `V/shots.cjs`; images viewed, no username or home folder): head home cards `2/156` paths tested, `60/156` accepted, `0/95` covered, `1900/2622` scenarios; the old `23 of 95` card is gone; area columns filled for 16 areas, totals `2/156` and `60/156`; LIFE-023 shows S1 to S4 each "None" (named gap); behaviour pages list tests per scenario, 722 "missing" marks over 460 pages. Pairs: `<CR>/work/verifier/evidence/before-after.md`.
15. Owner steps 5 and 6 and the other rules. `uv run --no-project python -I V/ownersteps.py <W> <scratch copy>`: untouched copy passes; one broken marker at a time gives `accepts-placement`, `fragment-required`, `fragment-undeclared`, `accepts-on-swrs`, `strs-tests-in-integration`.
16. Classification table positions. `V/table.py <W> <CR>/work/pr-body.md <base> <head>`: `rows 185` (removed 122, real VS Code 58, product outside VS Code 3, simulated 2), `bad rows 0`; base 185 StRS marker lines in 62 files, head 64 in 38; the one head marker without a row is a new one (`mystBlocksWindow.ts:151`, MYST-016#S2).
17. Impacts figures, computed from the base report and the head report and trace (`V/figures.py`, `V/figures2.py`): base 95 live, 23 covered, 24 with all linked SwRS covered; head 0 covered, 24, one direct-marker case; only the viewer reads these reports.
18. Named gaps are true: 722/2622, 94/156, 38 (claim 5); "StRS covered" 0 of 95 (claim 14); LIFE-023 (claim 5, 14); TRUST-012 paths start from the running Studio and TRUST-014 from a maintainer's install (files read); CORE-069 S5 says counts do not depend on the mode (file read).
19. PR body form. `V/prcheck.py V/pr524.json <CR>/work/pr-body.md <W> <base> <head>`: posted and local differ only on the CI line (posted `- [ ] CI green: pending`, local ticked); no internal reference outside "Internal references", no username or home path, no image; "No visual change in the extension" carries its reason; the Changes list matches the diff groups.

## Failures

A. StRS marker sort against spec section 3, D9 and owner answers Q7 and Q28 (walk in real VS Code -> accepts; walk on the simulated bench -> `tests_req #S<n>`).
- `experiments/02-audit-sample.md` classes 13 of 31 sampled lines "path". At the head, 8 of those 13 are removed: rows 11 TABLE-001 (`flushBeforeNavigate.ts`), 16 LIFE-014 (`serializer.test.ts`), 17 LIFE-001 (`stockCoexistence.test.ts`), 21 BLOCK-011, 23 CODE-004, 26 PALETTE-018, 29 MYST-009, 30 DIAG-001 (the last five in `test/visual`, all 5 sampled simulated walks).
- `git grep -n -E "@(tests_req|accepts_req) StRS-MDOKFSTUDIO-(TABLE-001|LIFE-014|LIFE-001|BLOCK-011|CODE-004|PALETTE-018|MYST-009|DIAG-001)" afbb55c5 -- test` returns six `accepts_req` lines in other files or paths (PALETTE-018#S1, LIFE-001#S1, TABLE-001#S1, MYST-009#S2, BLOCK-011#S1, LIFE-014#S1), none in the audited places, none at all for CODE-004 or DIAG-001, no simulated `tests_req` for any of the eight.
- CODE-004 S1 is walked by `check_code_copy` (`test/visual/capture_comment_checks.py:627-679`, flag in `scenarioDefinitions1.ts:451-465`); the built CODE-004 page shows "None". Only 2 simulated-path markers exist in the whole table.
- Wider than the sample: `git grep -c -E "@(tests_req|accepts_req) StRS-" <rev> -- test/visual` counts 74 lines at the base and none at the head (exit 1). The only `@tests_req StRS` lines left anywhere are TRUST-012#S1 and #S2 in test/security (the table's 2 "simulated path" rows). LIFE-001#S2, BLOCK-011#S2, MYST-009#S1, CODE-004#S1 and DIAG-001#S2, all classed walked by the audit, have no marker at all.
- The body's "122 removed (a snapshot, a partial path or a duplicate of a SwRS marker)" and "a walked path keeps a StRS marker" are therefore false, and no Known gap names it. The audited files are essentially unchanged since the audit.

B. Classification table (spec section 3: "file, line, StRS, class, outcome", class from the rubric walks a path / partial path / single-state snapshot / SwRS duplicate / other). The Class column of all 122 removed rows reads only `removed` (claim 16 output), which is the outcome, not a class. Not a Known gap.

C. Spec section 3: "Scenarios that no marker covers after the sweep stay declared and are listed in the PR body." The body gives counts per group only (line 281; line 285 "The per-scenario list is not inlined"; line 52 under Autonomous decisions). CR-505 `03-change-spec.md:99` takes "the list in CR-504's PR body" as its input, so that input does not exist. Not a Known gap.

D. Spec section 3: a test that checks no declared scenario is read again, and either the SwRS gains the scenario or the marker moves to the SwRS the test does check. The body (line 55): "136 dropped because the test checks no declared scenario". Neither required outcome; not a Known gap. `V/lastmarker.py <W> <base> <head>`: `base (file, SwRS) pairs 1910 gone at head 68`.

E. Spec section 3: "The scenario is read from the test, not guessed from the test's name." `uv run --no-project --with pyyaml python -I V/sample.py <W> afbb55c5... 504 16` over `5541` SwRS fragment lines; 3 of 16 name a scenario the test does not check:
- `test/core/render/mathRenderer.test.ts:52` MYST-024#S8 "Sphinx-style math delimiters are typeset" on "math cannot inject trusted HTML commands or external links" (only `\href` and `\htmlStyle`).
- `test/core/render/alertSourceLines.test.ts:150` GFM-009#S10 "Alerts inside a colon container" on the fenced-code test (the same marker at :164 sits on a list-item test).
- `test/session/lineEndingSave.test.ts:40` BLOCK-234#S3 "A CRLF table keeps its line endings" on a test that saves a last paragraph.
None of the three files is in `<CR>/evidence/r2-2*-sweep-weak.md` (Grep: no match), so they belong to the matches scored good and never read. The viewer's `1900/2622` and the body's `722` unmarked therefore overstate what is tested. The body names "Fragments scored good ... were not re-read" under "Others", which is not among the gaps accepted for the follow-up change, and a Grep of the CR-505 spec for a re-reading task finds none.

F. Body: "A new SwRS (SwRS-MDOKFSTUDIO-CORE-096) states the behaviour of the marker check, each rule tested by its own test"; spec section 4 (the marker-check SwRS is updated for the rules). The check has the rule `implements-fragment` (`scripts/check-marker-companions.mjs:168`, listed in the body's rule table). CORE-096's normative text and its scenarios S1 to S6 never mention `@implements_req`; its test (`test/build/checkMarkers.test.ts:272-281`) is marked `CORE-096#S3` "A fragment is missing or unexpected", which describes only `fragment-required` and `fragment-unexpected`.

## Observations (not counted as failures)

- "Tested by" block of a scenario card has no horizontal padding (`test/site/requirementsViewer/viewer.css:242`; `after-swrs.png`).
- The posted body still reads `CI green: pending` (CI is green, claim 2). Its "Evidence: none" and the Known gap "the site was not looked at in a browser" are overtaken by the verifier evidence: the site change is visible, so the pairs belong in Impacts.
- "that review removed the last marker of TRUST-005, TRUST-090, REVIEW-219, LIFE-169 or LIFE-170 from some `test/integration` files" is incomplete: `lastmarker.py` shows 26 (file, SwRS) pairs, 24 SwRS, gone from `test/integration`; 11 SwRS have no `test/integration` marker left and none is named (BLOCK-053, BLOCK-216, CORE-022, CORE-043, DIAG-001, FMEDIT-024, FMSCHEMA-001, FMSCHEMA-084, PALETTE-031, PALETTE-217, THEME-001). The five named still have some.
- Two sections in the fold come before "Changes" (classification table, uncovered counts).
- No review request on the PR (`reviewRequests 0, reviews 0`); the owner is probably the author. "Human decisions" omits answer Q30. The 5 deprecated exemption reasons and the `log.md` entry (no own heading for the sort) differ slightly from the spec's form.
- Write refusal met by this Verifier, nothing written, the file was then put in `<CR>/work/scratch`: `refused: .../scratchpad/cmds.py is outside the folders this agent may write in (<W>; <CR>); write there`.
