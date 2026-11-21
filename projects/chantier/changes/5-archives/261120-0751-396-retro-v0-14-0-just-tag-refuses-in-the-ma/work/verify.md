Head: 10b371ff69fa5a182dec14c650828ffe4782fc85

Second pass, move 83119497..10b371ff (fix commit + rebase onto CR-395). Raw log of the six-case run: work/verifier-ff-run.log.

Claims judged at 10b371ff (real subprocess: shipped scripts/version.py copied into a throwaway clone of a bare origin under scratch, run with `python -I scripts/version.py ff-main`; scratch removed after; never run in main checkout or worktree):
- behind by a uv.lock commit: rc=0, stdout `main checkout: fast-forwarded to c321d36; uv.lock changed: sync pending`, HEAD == origin/main. PASS (the earlier failed claim, main() dispatch, is fixed).
- already at origin/main: rc=0, `main checkout: already at add6b57`, HEAD unchanged. PASS
- on another branch: rc=1, `just tag: the checkout is on feat, not main: run just tag from the main checkout, on main`, HEAD unchanged. PASS
- detached HEAD: rc=1, `just tag: detached HEAD, not main: ...`, HEAD unchanged. PASS
- tracked file modified: rc=1, `just tag: the main checkout has tracked changes (f.txt): commit or set them aside yourself, then run just tag again`, content still `changed`, HEAD unchanged. PASS
- diverged: rc=1, `just tag: main cannot fast-forward to origin/main (hint: Diverging branches can't be fast-forwarded, you need to either:): nothing was changed; ...`, HEAD unchanged. PASS (reason is git's first stderr line, as specified)
- untracked file while behind: rc=0, fast-forwarded, u.txt still present. PASS
- docstring usage block has `uv run --script scripts/version.py ff-main` (version.py line 11); `ff-main` subparser with the specified help. PASS
- justfile `tag`: first command `ff-main`, before `check-tag` (justfile lines 79-83). PASS
- `pytest skills/chantier/scripts/cli/tests/test_release_tag.py -q`: 8 passed. PASS
- Cards/CONTRIBUTING: `git diff --stat 42bed00f HEAD` = 7 files (CONTRIBUTING, justfile, version.py, chief-of-staff, driver, foreman, test_release_tag); concepts.md rule 8 and agents/ untouched. driver.md holds `waits: the steering session runs`, foreman.md holds `tag done: steering session`. PASS
- Rebase: range-diff 83119497...10b371ff shows caa2051c = 83119497 (patch unchanged), only the CR-395 base commit and the fix commit are new. CARRIED from 83119497 for the rest: the cards and CONTRIBUTING patch is unchanged.
- CI at 10b371f: Driver's note says all five jobs pass (log line `CI: gh pr checks 363`); not re-run by me.

PR description (gh pr view 363): Summary, Deliverables and Changes match the 7-file diff; Known gaps names the untested `just tag`. Note: the Test plan still cites `8311949` for local gates and Review; the Driver refreshes them at 10b371f (Verified/CI boxes also its to fill, per the brief). The log shows `r3 approved at 83119497, committed as ab7ef5d6` and the rebase at 10b371ff with just check pass (911), no review note at 10b371ff; the Driver must carry the Review box with its reason. No long gate passed at 10b371f (recorded by ship as off); the Driver owes `just scenario`.

VERIFIED

## Description pass

Head: 10b371ff69fa5a182dec14c650828ffe4782fc85

Judged at 10b371ff: `gh pr view 363 --body` against `git diff 42bed00f..HEAD` (7 files) and the pr-template audit.
- Sections in order, fold with blank lines, nothing after `</details>`; Internal references last and the only place naming CR-396. PASS
- Deliverables before/after table matches the justfile diff (fetch replaced by ff-main); refusal list, output lines and `; uv.lock changed: sync pending` match `ff_main` in scripts/version.py. PASS
- Changes lists all 7 files (CONTRIBUTING, justfile, version.py, three cards, test_release_tag.py); `--no-overwrite-ignore` is in the code. PASS
- "Release driver", "steering session": product terms of the card change, not doer of the work. PASS
- Test plan SHAs refreshed to `10b371f`; Review "carried from 8311949" matches log notes (`r3 inspector approved at 83119497`, rebase patch unchanged); `gh pr checks 363`: 5 jobs pass; 911 matches the log note. PASS
- Known gaps: names the untested `just tag` hand-off; no UNVERIFIED mark, no accepted failure. PASS

VERIFIED
