# Verify CR-227

Head: e4c67aae0c6874902578b99d7f7595b9b16ba174

Re-judged after the rebase 6c65f4e..e4c67aa (onto CR-226's 439b383). Only what the move touched.

| Claim | SHA | Command | Output |
| --- | --- | --- | --- |
| E1 `just check` passes | e4c67aa | `just check` (worktree) | ruff 0.17.5 format 159 files ok, check ok; mypy 1.20.0 strict "no issues found in 138 source files" (win32 only; linux/darwin are CI's); uv lock --check ok (20 packages); biome 2.6.7 90 files ok; pytest 72 passed; release-notes ok |
| E2 reduced scenario step | e4c67aa | scratch driver drv.py: SurfaceWorld.build, init, prepare, open --default-branch main, surface_autosync(w); HOME/USERPROFILE/CLAUDE_CONFIG_DIR at scratch | RESULT pass 18, fail 0 (twice): same checks as at 6c65f4e still hold: P13/status lines for blocked and approval, dead participant file kept, board join, /api/board object, stop/start/approve refusals and `approve` then `start . --enable-only`, non-JSON POST refused |
| Other claims (spec lines, detection, panel behaviour) | 6c65f4e | - | carried from 6c65f4e: the rebase conflicts were in board write routes; E2 and check re-run green on the new head |
| E3 real tool | - | - | carried from 6c65f4e: not run, git-lfs not found; not proved |
| E4 / QA screenshots vs prototype | - | - | carried from 6c65f4e: needs a browser; not proved |

Long gate waived by the user; just scenario not run. User's surface repo untouched.
