# Verify CR-312

Head: 81039ceb2d3794c8c25982df6c42fec8525076c2

Move judged: e610cb9..81039ce, a rebase onto main 607561b.

1. Patch unchanged, at 81039ce: `git range-diff e610cb9~1 e610cb9 81039ce` ->
   `1:  e610cb9 = 3:  81039ce feat(evals): start Claude campaigns without a Foreman away from the desk`
   (the other two lines are main's new commits fa795cf, 607561b).
2. `just eval-dry-run` at 81039ce (run now): `ok eval-root: setup refuses a workspace outside the eval root, a missing and a malformed file (exit 2, nothing created); inside, it passes with the allow rules and no trust entry`; last line `dry run: 17 of 17 cases as expected`.
   After: `ls evals/kit/eval-root.local.json` -> No such file; `git status --short` empty.
3. carried from e610cb9: setup refusals by hand (no file, malformed file: exit 2, nothing created); outside-root and root-itself covered by item 2's case. Reason: patch unchanged (item 1), base change touches only cards docs (fa795cf, 607561b).
4. carried from 60da054: spec sections 1-5 against the diff, no CLI/scenario/agent change, nothing writes ~/.claude.json, no visual change (patch unchanged, item 1).
5. PR #266 description, `gh pr view 266` at head `81039ceb2d3794c8c25982df6c42fec8525076c2` (`--json headRefOid`): renders; Summary/Deliverables/Changes match the 11-file `git diff --stat origin/main` (.gitignore, README, 6 runbooks, dry_run.py, setup.py, hosts/claude-code.md); SHA marks name 81039ce or carried SHAs with reasons; Known gaps names the unproved trial; no images. Review box (approved at 3df17b9, committed as 8b6ee60) matches `chantier log CR-312`: "r2 approved at 3df17b969d41f7584c805f9f9ad1240e96bf51e4, committed as 8b6ee60". CI: `gh pr checks 266` -> 5 checks pass (macos, ubuntu, windows check; eval-dry-run; scenario ubuntu).

VERIFIED
