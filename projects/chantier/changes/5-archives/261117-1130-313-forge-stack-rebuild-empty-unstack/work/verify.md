# Verify CR-313

Head: 9572ed5663ace6cd9ce6cd9e25629d30f4f54754

All claims judged at 9572ed5663ace6cd9ce6cd9e25629d30f4f54754.

1. Six-row unit test passes. Command: `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests/test_cli_units.py -k "empty or reply or gh" -v` -> `6 passed, 6 deselected in 0.35s` (rows True/ran0..ran5, incl. `HTTP 404` row, `not JSON` rows).
2. `just test` at the head: `375 passed in 63.73s`.
3. `just scenario --unit stack --forge github` at the head: exit 0 (log: work/verifier/scenario-stack-github.log; unit file scenario/results/20261117-114632-30984/stack-github.md, 0 unchecked boxes). Output shows:
   - step 3: stderr `unstacked #150`, `HTTP 403`, last line `stack #150 is dissolved and no stack replaces it yet: run `forge-stack create``.
   - step 3b: `stack #105 is still open after 5 unstack tries ...` with no dissolved / unknown line.
   - step 3c: first rebuild exit 0 (`unstacked #201`, `stack #201 ... ready to merge`); second exit 4 with `unstacked #201`, `HTTP 403: stacks are not allowed`, last line dissolved; then `forge-stack create` exit 0 (stack #202).
   - step 3d: rebuild exit 4: `unstacked #202`, `not JSON: <html>`, last line `the forge accepted the create call but its reply cannot be read, so the stack's state is unknown: run `forge-stack show``, no dissolved line; `forge-stack show` exit 0, `stack #203 ready to merge`.
4. Card sentences: `git diff origin/main...HEAD -- skills/chantier/references` shows driver.md (dissolved line -> run `forge-stack create` itself; unknown-state line stays an anomaly, `show` read may be quoted) and chief-of-staff.md (run the command the last line names: create after dissolved, show after unknown-state, else rebuild) matching spec sections 3 and 4.
5. Code diff matches spec sections 1-2 (Unreadable, `gh(empty_ok)`, unstack `empty_ok=True`, `_make` raises Unreadable, `_rebuild` `gone`/`unstacked`/`making` markers and line choice), read in `git diff origin/main...HEAD`.
6. PR description (work/pr-body.md) matches the diff; Known gaps None, no UNVERIFIED claim. Test-plan boxes are the Driver's to tick.
7. CI green at the head (per prompt: 5 jobs); not rerun by me. Windows local `just scenario` full gate not run by me (unit stack/github only); `just test` passed on Windows.

VERIFIED

## Description pass at a857b3141a48b669be172463853151ba96e59f5f

Head: a857b3141a48b669be172463853151ba96e59f5f

Code claims 1-5 carried from 9572ed5: the move 9572ed5..a857b31 is a base change only (rebase onto CR-312's branch); `git diff HEAD~1 HEAD` shows the same 8 files (forge_stack.py, forge_stack_gh.py, fake_gh.py, run_scenario.py, scenario/README.md, driver.md, chief-of-staff.md, test_cli_units.py). Note: the stale `origin/...cr-312` ref (e610cb9) differs from the local CR-312 branch (5220b12), so the three-dot diff against it shows CR-312's files; HEAD~1 is the true base.

8. Posted PR description (`gh pr view 267 --json body`, headRefOid a857b31...) judged at a857b31: Summary, Deliverables (table of last lines, `gh(..., empty_ok)` and `Unreadable` signatures), Changes (files, six-row test, steps 3/3b/3c/3d, two card sentences) all match `git diff HEAD~1 HEAD`; nothing delivered is unmentioned. Fold is in place with blank lines after `</summary>` and before `</details>`, nothing after it; no internal reference outside Internal references; role names (stack driver, Chief of Staff) are product terms of changed cards; no Issues References (no issue line); Known gaps "None" with no UNVERIFIED claim; no STALE mark; proofs name SHAs, carried ones say why.
9. Review box "approved at 9572ed5": `chantier log CR-313` has "r1 approved at 3df17b9, committed as 9572ed5", which is the cited SHA.

VERIFIED
