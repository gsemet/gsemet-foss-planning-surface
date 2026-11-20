# Verify: CR-343 (garden block-editing and table-editing requirements)

Head: d99d2ef94b5ec2dd80f33ded348f031ecefa1aa5

PR #417 (draft, base main c698ac97d5b09c1d173ea02d2c0d58ead7be27b9). Move judged:
225e73b9..d99d2ef9. Logs and probes: `work/verifier/`.

Pass 2 (description only, same head d99d2ef, no commit moved: `git rev-parse HEAD` and `git
ls-remote origin refs/pull/417/head` both d99d2ef94b5ec2dd80f33ded348f031ecefa1aa5, `git status
--short` empty). The description was edited and posted again; claims 13 to 15 are judged again
on the posted description; claims 1 to 12 are carried from d99d2ef: the head and the tree did not
change, only the forge description did, which no proof of theirs exercises.

Verdict: VERIFIED.

## Claims

1. **Pushed head.** d99d2ef. `git rev-parse HEAD` -> d99d2ef94b5ec2dd80f33ded348f031ecefa1aa5;
   `git ls-remote origin refs/pull/417/head` -> same SHA; `git merge-base HEAD origin/main` ->
   c698ac97d5b09c1d173ea02d2c0d58ead7be27b9 (= origin/main). Worktree clean (`git status --short`
   empty). PASS.

2. **Long gate.** d99d2ef. `work/gates/20261118-125405.log` line 1: `gate CR-343 branch
   chantier/batch-06/cr-343-change-specification-garden-the-requirem head
   d99d2ef94b5ec2dd80f33ded348f031ecefa1aa5`; `$ just preflight`; ends `ci-static: passed`,
   `result: pass at d99d2ef94b5ec2dd80f33ded348f031ecefa1aa5`. PASS.

3. **CI.** d99d2ef. `gh pr checks 417`: checks, report, static, static-windows, visual pass (others
   skipping). `gh run view 44298860609 --json headSha,conclusion,jobs`: headSha d99d2ef9..., conclusion
   success; static-windows, integration, visual, stress, static, report, checks success. PASS.

4. **requirements-lint clean.** d99d2ef. `just requirements-lint` exit 0
   (`work/verifier/requirements-lint-d99d2ef.log`): `1138 requirements, 0 errors, 27 warnings`,
   `0 indexes would change`, `0 requirement OKF projections would change`, `0 files would change`,
   `main paths: 81 StRS checked, 542 SwRS citations, all valid`. PASS.

5. **okfreq trace clean, scope coverage.** d99d2ef. `uv run --no-sync --group requirements okfreq trace
   requirements --json` exit 0 (`trace-d99d2ef.json`): duplicates 0, non_leaf 0, missing_ids 0,
   warnings 0. `python -I work/verifier/check_scope.py <worktree> trace-d99d2ef.json`
   (`scope-d99d2ef.txt`): `markers on non-in-force or unknown IDs: []`; `in-force SwRS BLOCK/TABLE: 69
   exempt: []`; `no implementation marker: []`; `no test marker: []`. PASS.

6. **Diagrams and validation tests on every in-force StRS of the two scopes.** d99d2ef. Same probe:
   16 in-force StRS (BLOCK-001/003/006/008/011/014/016/025, TABLE-001/002/006/008/013/014/015/016),
   each `diagram_section=True mermaid_in_section=1 validation_test=True`. PASS.

7. **Duplicates superseded, nothing deleted.** d99d2ef. `git diff --name-only --diff-filter=D
   c698ac97 HEAD` -> empty. Each old ID has `req_lifecycle: superseded` and `superseded_by` as the
   spec's table: BLOCK-236..245 -> BLOCK-259; TABLE-070/073/074/076/080 -> TABLE-122;
   TABLE-003/004/005 -> TABLE-055; BLOCK-029 -> 033; BLOCK-002 -> 014; BLOCK-129 -> 109; TABLE-102 ->
   094; TABLE-118 -> BLOCK-255; BLOCK-258 -> BLOCK-260, 261; TABLE-035 -> TABLE-123..126; StRS
   TABLE-011 -> TABLE-013, 014; StRS TABLE-012 -> TABLE-015, 016. PASS.

8. **Four approved StRS corrections, one commit each.** d99d2ef. `git show --stat`: 26a9bea0
   touches only StRS-BLOCK-025 (Known issue line removed, `depends_on` BLOCK-041, diagram,
   approved_at 2026-11-18T10:55:00+01:00); 04064e6b only StRS-BLOCK-003 (2 cross-scope rationale
   bullets removed, diagram, approved_at); 8415bbb7 only StRS-TABLE-001 (6 "belongs to"/pointer
   bullets removed, diagram, approved_at); 1ba6a4f6 the TABLE-012 split (TABLE-012 superseded,
   TABLE-015/016 new, children reparented, RI-T45). Shared rules in b00bb39c (depends_on of BLOCK-041,
   058, 109). Owner agreement in advance: `02-answers.md` garden-Q1 A. PASS.

9. **CSS produced byte-identical.** base c698ac97 vs d99d2ef. `css_entry.ts` bundled with esbuild
   against each tree, run with node: both outputs 56557 bytes, sha256
   b205abdabcfa27d6ee7dcfbb865d0c2a4d44ec81c73d925fac6f3550e3a43793, `cmp` -> IDENTICAL
   (`work/verifier/evidence/`). PASS.

10. **src changes are markers only.** d99d2ef. `git diff -U0 c698ac97 HEAD -- src
    ':!src/core/preview/styles' | grep -E '^[-+]' | grep -vE '^(\+\+\+|---) ' | grep -vE
    '^[-+]\s*(//|\*|/\*)'` -> no output (only comment lines changed); style files covered by claim 9.
    PASS.

11. **Markers per behaviour, at most 3 IDs per comment.** d99d2ef. `node
    scripts/check-marker-companions.mjs` -> `check-markers: 5 companion file(s), 434 in-force SwRS
    marked, 46 files on the marker baseline`, exit 0. Count of IDs per marker line over all changed
    src/test files (awk, >3) -> no output. Hub stacks: IDs in the 12 lines above the declaration,
    base -> head: closeBlockEdit 5 -> 2, openMappedEditor 4 -> 0, renderTableCellEditor 3 -> 1;
    `git diff` of blockEditor.ts shows the 5-ID stack on openBlockEditor moved onto its branches
    (BLOCK-041 on the open guard, 014, 102, 033, TABLE-001). Baseline only shrinks
    (`scripts/marker-baseline.json`: every changed value lower or removed). PASS.

12. **r5/r6 RI-T16 changes, r7 docs.** d99d2ef. `git show 06c93715 b7cd8dfb d99d2ef9`: the click
    check measures `p[data-sphinx-source-line]:not([data-sphinx-preview-editing="true"])`; the
    reopen step asserts `data-sphinx-preview-edit-mode` equals "off" with `@tests_req
    SwRS-MDOKFSTUDIO-LIFE-172`; StRS-BLOCK-001 diagram now `[*] --> Reading: new preview, any edit mode
    last chosen`, `[*] --> Editing: reload of the same document, edit mode on` (consistent with
    LIFE-170 "starts from the saved panel state" and LIFE-172 "opens in preview mode", both derived
    from StRS-BLOCK-001); StRS prose unchanged; owner question added to `requirements/tiers/log.md`.
    Ran in a real window: heavy run 44298860609 integration log
    (`work/verifier/heavy-integration-44298860609.log`): `PASS real-input screenshot:
    block-editing/r14-edit-mode-no-reflow`, `STEP done: real-input (376297 ms)`, `ci-integration:
    passed`; RI-T45 (`scenarioTableInsertFromSlash`, run.ts:249) runs in that same step. PASS.

13. **PR description: renders, no images.** d99d2ef (pass 2). `gh pr view 417 --json body -q .body` saved to
    `work/verifier/pr-body-forge-2.md`; `diff` against `work/pr-body.md` -> `90d89 < ` (only a
    trailing blank line). Sections (Summary, Approved requirements changed, Deliverables, Blast
    radius, Autonomous decisions, Known gaps, then Changes, Impacts, Test plan, Internal
    references inside one `<details>` fold, closed), the table and the lists are well formed; no
    image attached. PASS.

14. **PR description: Known gaps and Test plan.** d99d2ef (pass 2). The steering decision (StRS-BLOCK-001 vs LIFE-170/172)
    has its bullet; the local non-run of the real-window steps, TABLE-124, PALETTE-031, BLOCK-261 and
    BLOCK-109 have theirs. No `**UNVERIFIED:**` claim, no STALE mark, no failed-and-accepted claim.
    Reworded gap "long gate ran on Windows ... real VS Code jobs ran only in CI's heavy run on
    Linux, green at d99d2ef": gate log `work/gates/20261118-125405.log` line 1 names CR-343 at
    d99d2ef94b5e...; `preflight: visual, integration, report and gallery stages skipped on Windows;
    CI runs them`; `result: pass at d99d2ef...`; `gh run view 44298860609 --json headSha,conclusion`
    -> `d99d2ef94b5ec2dd80f33ded348f031ecefa1aa5 success`, jobs integration, stress, visual,
    static, static-windows, report, checks success; `.github/workflows/ci.yml` runs-on
    ubuntu-latest except one windows-latest (static-windows). Test plan boxes:
    - Local gates at d99d2ef: `just preflight` pass (gate log above); `just requirements-lint`
      pass and its line `main paths: 81 StRS checked, 542 SwRS citations, all valid` (claim 4);
      `just check` run by this Verifier at d99d2ef, clean tree: exit 0
      (`work/verifier/check-d99d2ef-desc.log`, ends `0 files would change`, `main paths: 81 StRS
      checked, 542 SwRS citations, all valid`).
    - Review box "approved; the last review's changes are committed as b7cd8df and d99d2ef":
      `$CHANTIER log CR-343` -> `r7 approved at 06c9371588d4..., committed as b7cd8dfb (RI-T16
      reopen test + LIFE-172) and d99d2ef9 (...)`: the SHAs cited match the round's
      `committed as`. Earlier rounds r1 to r6 each have an approved inspector note.
    - CI green at d99d2ef: `gh pr checks 417` -> checks, report, static, static-windows, visual
      pass (others skipping); heavy run 44298860609 as above.
    - New tests and real-window steps pass in heavy CI at d99d2ef: claim 12.
    PASS.

15. **PR description matches the diff.** d99d2ef (pass 2). PASS.
    `git diff --name-only c698ac97 HEAD | grep -vE '^(requirements|src|test)/'` ->
    `docs/VISION.md`, `scripts/marker-baseline.json`; `git diff --name-status c698ac97 HEAD --
    test src | grep -v '^M'` -> `A test/integration/realInput/tableInsertSlash.ts`, `A
    test/page/runtimeTableCellBlur.test.ts`. The posted Changes now names each: `docs/VISION.md`
    (Tables row, TABLE-015 and TABLE-016 replace TABLE-012), the marker-gate baseline, the new
    `runtimeTableCellBlur.test.ts` and the new `realInput/tableInsertSlash.ts` (3x2 table from the
    slash menu); `requirements/` and `src/` (markers only, claims 9 and 10) as before. Summary,
    Approved requirements changed and Deliverables match claims 7 and 8 (carried from d99d2ef,
    unchanged tree). Pass 1 failure (VISION.md and tableInsertSlash.ts missing) is fixed.

## Evidence

`work/verifier/evidence/before-after.md` (CSS pair, before c698ac97, after d99d2ef).
