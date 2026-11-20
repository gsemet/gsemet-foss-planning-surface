# Verify CR-430

Head: 2bea4c6a035e124bc7a0c5889af41db485e88d92

Verdict: VERIFIED

Move judged: restack 585983a..2bea4c6 onto CR-428 9f17229 (clean). Delta proof, in the CR worktree:
`git rev-parse f28463c5^{tree} 9f17229^{tree} 585983ae^{tree} 2bea4c6^{tree}`:
`eeca428d...`, `eeca428d...`, `e8579db6...`, `e8579db6...` (old and new base have the same tree, old and
new head have the same tree); `git diff --name-only f28463c5 9f17229 | wc -l`: `0`;
`git diff 9f17229 2bea4c6 | git patch-id --stable` and `git diff f28463c5 585983ae | git patch-id --stable`:
both `5bec069b5f4defc36cd81ce3324f6d0e3eb3222d`. The move touched no file any proof runs; claims 1-3 were
still run again at 2bea4c6, claims 4-5 are carried. Runs: a detached worktree of 9f17229 (sparse:
`.agents/` and `docs/` left out for path length; node_modules linked read only from the CR worktree) at
`work/scratch/b`, before at 9f17229, then detached at 2bea4c6 (after); removed at the end. The CR
worktree was not modified.

0. Pushed head, at 2bea4c6. `git rev-parse HEAD` in the CR worktree: `2bea4c6a035e124bc7a0c5889af41db485e88d92`;
   `git ls-remote origin`: `refs/heads/chantier/batch-06/cr-430-...` at `2bea4c6a035e...`, CR-428's branch at
   `9f17229b0332...`; `gh pr view 437 --json headRefOid,baseRefName`: `2bea4c6a035e...`, base
   `chantier/batch-06/cr-428-run-the-tablebreakout-width-tests-on-lin`. `git status --short`: empty.
1. The new test passes, at 2bea4c6. `node node_modules/typescript/bin/tsc -p .`: exit 0;
   `node scripts/node-test.mjs unit out/test/core/render/mystFeatures.test.js`: exit 0,
   `✔ references to captionless figures and tables stay readable`,
   `✔ a numref to a captionless figure or table shows its number`, `tests 46`, `pass 46`, `fail 0`.
   Before, at 9f17229, same commands: exit 0, only `✔ references to captionless figures and tables stay
   readable`, `tests 45`, `pass 45`, `fail 0`. Logs: verifier/evidence/before-9f17229.log, after-2bea4c6.log.
2. The test can fail, at 2bea4c6 (scratch worktree only). Line 167's expected texts changed with sed to
   `"{numref}fig-empty"` / `"{numref}tbl-empty"`, tsc, same command: exit 1,
   `✖ a numref to a captionless figure or table shows its number`, `tests 46`, `pass 45`, `fail 1`,
   `actual: [ 'fig-empty', 'Figure 1', 'tbl-empty', 'Table 1' ]` (verifier/mutation-2bea4c6.log). Reverted
   with `git checkout --`; `git hash-object` of the file `1ba583030abe...` equals
   `git rev-parse HEAD:test/core/render/mystFeatures.test.ts` `1ba583030abe...`.
3. Requirement text, at 2bea4c6. `git diff --stat 9f17229 2bea4c6`: requirements/tiers/log.md +9,
   SwRS-MDOKFSTUDIO-MYST-019.md 1 line, test/core/render/mystFeatures.test.ts +41; no src/ file.
   `git diff --word-diff ... MYST-019.md`: only the Method line of the verification notes changes (drops
   "which checks `{ref}` only; the `{numref}` case is untested", names both tests); the Criteria line is
   context, unchanged. The test diff adds two `// @tests_req SwRS-MDOKFSTUDIO-MYST-019` lines (the existing
   `{ref}` test and the new one).
4. Requirements checks (okfreq validate/lint/update-coverage, check_main_paths, use-case diagrams,
   generate-report row `SwRS-MDOKFSTUDIO-MYST-019 ... ✅ covered`): judged at 585983a, all pass, exit 0.
   carried from 585983a: 2bea4c6 has the same tree as 585983a (`e8579db6...`, claim "Move judged").
5. MYST-017 heading placeholder test unchanged: carried from 585983a: same tree; the diff at 2bea4c6
   (claim 3) still touches only mystFeatures.test.ts in test/, mystPaletteRendering.test.ts not in it.
6. Long gate: `just preflight` passed at 585983a (work/gates/20261120-124259.log, first line `gate CR-430
   branch chantier/batch-06/cr-430-bug-swrs-myst-019-s-numref-scenario-cont head
   585983ae0f5125538b67d3d02af3246aa1cc31eb`); `$CHANTIER log CR-430`: `driver carry
   head=2bea4c6a035e124bc7a0c5889af41db485e88d92 base=9f17229b... gate_from=585983ae...`. Carried from
   585983a: same tree, same patch-id.
7. Review: `$CHANTIER log CR-430`: `move 6d76d24..585983a (restack) inspector approved at
   585983ae0f5125538b67d3d02af3246aa1cc31eb`, then the `carry` event to 2bea4c6 (clean rebase, same tree).
8. PR description (`gh pr view 437 --json body`), at 2bea4c6, SHA lines excluded per the brief: Summary,
   Deliverables table (Figure 1 / Table 1 as line 167 asserts), Changes (the three files, the marker on the
   existing test, notes only in MYST-019, the log entry) and Impacts match the diff; nothing missing or
   unmentioned; renders (sections, table); no image; Known gaps "None" with no UNVERIFIED claim and no
   uncaptured pair; CR-430 and PR #419 only under Internal references. The Test plan SHA lines (6d76d24)
   are left to the stack driver, per the brief.
9. CI: `gh pr checks 437` at 2bea4c6: static, static-windows, visual pending; others skipping. Not proof.
10. Evidence: verifier/evidence/before-after.md (text pair, claim 1). No visible change, no screenshot.

## Earlier passes

585983a: NOT VERIFIED only because the forge had rewritten the remote branch (all claims held). 6d76d24:
VERIFIED. This pass supersedes both at 2bea4c6.
