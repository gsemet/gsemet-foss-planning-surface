Head: 1bb39317c3dbf9d344ad508813cb83ad5c229d24

Verdict: VERIFIED. Every claim holds at 1bb3931. The long gate passed at this head on both forges, CI is green on
all five jobs, and the PR description matches the head, including its Review box.

Move 1448479 -> 1bb3931: a rebase from b394a35 onto main 9ac3adb.
- `git range-diff b394a35..1448479 9ac3adb..1bb3931` gives `1: 5fc412a = 1: f8ddcf0` and `2: 1448479 = 2: 1bb3931`.
  Both patches are identical.
- `git rev-parse 'b394a35^{tree}' '9ac3adb^{tree}'` gives the same tree for both, 895e89e3c8aeaa65e81dc6cd6e5819013edcb23b,
  so the base content did not change.
- `git rev-parse 'HEAD^{tree}' '1448479^{tree}'` gives the same tree for both, 209bdf03993eef0549967af8661bd78fe77ec192.
- So the move touched no file, behaviour or dependency that any proof exercises. Each claim below that was judged
  at an earlier head is carried with that reason. `git diff --name-only 9ac3adb HEAD` still lists 19 files.

Probes (from the 894806a pass): a scratch repository at
C:/Users/gaeta/AppData/Local/Temp/claude/f81ba1603abd10b3/bd1945f6-9982-485f-b29f-477277e80753/scratchpad/v89, with
the harness scripts v89setup.ps1, v89e2.ps1, v89e4.ps1 and v89e5.ps1 in the same folder.

1. The patch: carried from 1448479, because the tree is identical (above). At 894806a, `git diff --stat 86056e5 894806a`
   showed only `scenario/run_scenario.py | 2 +-`, so the CLI and the cards were byte-identical to 86056e5.
   `git show 1bb3931` is the one-line S4 change: the expected text goes from `'"board" and "ci"'` to
   `'"ci" and "long_gate"'`.
2. E2: carried from 894806a, because the tree is identical. With `parallel: 2`, `.long-gate.run` named CR-101 and
   `.long-gate.2.run` named CR-102, and the two gates ran at once. CR-103 logged
   `waiting for the long gate of CR-101 ... and CR-102 ...`, then took slot 2 and passed.
3. E3: carried from 894806a, because the tree is identical. The status showed `activity CR-101 gate running`,
   `activity CR-102 gate running` and `activity CR-103 gate queued behind CR-101, CR-102`.
4. E4: carried from 894806a, because the tree is identical.
   - `gate CR-102 --stop` stopped only slot 2, and CR-101 passed.
   - `order merged CR-102 --epoch 0` printed `stopped the long gate of CR-102 (pg31960)`.
   - `cancel CR-103 --epoch 0` printed `cancelled CR-103; stopped 1: pg4596`.
   - Stopping a CR that held no slot exited 2 with `no long gate of CR-102 running (running: CR-101): not stopped`.
5. E5: carried from 894806a, because the tree is identical.
   - `--first` without `--epoch` exited 2. With a command it exited 1.
   - With `--epoch 0` it printed `moved the long gate of CR-103 to the head of the queue (ahead of: CR-102)`.
   - With a stale epoch it exited 3.
   - The gates passed in the order CR-101, CR-103, CR-102, and no `first-*` marker was left.
6. E6: carried from 894806a, because the tree is identical.
   - `parallel: 0`, `parallel: two`, `slots: 2` and an empty `long_gate:` were each refused, by `gate` with exit 2
     and by preflight with `P12 FAIL`.
   - `parallel: 1` was valid and gave `P12 ok`.
7. E1, E2.4 and E7, at 1bb3931: the long gate `work/gates/20261114-145657.log`, line 1
   `gate CR-242 ... head 1bb39317c3dbf9d344ad508813cb83ad5c229d24`.
   - Line 24: `github: 813/813 checks passed in 1011.4 s` (transcript `scenario/results/github-20261114-151412.md`).
   - Line 27: `gitlab: 791/791 checks passed in 1017.3 s` (transcript `scenario/results/gitlab-20261114-153110.md`).
   - Line 28: `result: pass at 1bb39317c3dbf9d344ad508813cb83ad5c229d24`. `chantier log CR-242` records
     `gate result=pass head=1bb3931... command=just scenario run=20261114-145657-31236`.
   - That covers steps 18, 18b, 12c and 19b, the surface step and the S4 fix, on both forges.
8. E8: carried from 894806a, because the tree is identical. The diff of the cards and docs shows only the lines that
   C, E and F name. No file under `agents/` or `com.github.copilot/agents/` is in the CR's diff.
9. E9, at 1bb3931:
   - Local `just check` passed in the same gate log. Line 6 is `All checks passed!` (ruff), line 10 is
     `Success: no issues found in 124 source files` (mypy, with `strict = true`), and line 18 is `69 passed in 19.00s`.
     `chantier log CR-242` records `gate result=pass head=1bb3931... command=just check`.
   - CI: `gh pr checks 188` (run 43602114925) shows `just check` passing on macos, ubuntu and windows,
     `just eval-dry-run` passing, and `just scenario (ubuntu-latest)` passing in 13m59s.
10. The PR description (`gh pr view 188`, headRefOid 1bb39317c3dbf9d344ad508813cb83ad5c229d24, base main, draft,
    MERGEABLE): PASS.
    - It renders. The sections, the yaml block, the table and the `<details>` fold all have blank lines around them,
      and there are no images.
    - Changes names all 19 files of `git diff --name-only 9ac3adb HEAD` and claims no file outside that diff.
    - Test plan, "passed again in the long gate at 1bb3931 (github 813/813, gitlab 791/791)": backed by claim 7.
    - "Local gates (at 1bb3931: just check, pytest and ruff pass)" and "mypy --strict clean for linux, darwin,
      win32": backed by claim 9 (the local Windows run, plus the `just check` jobs on ubuntu, macos and windows).
    - Evidence "carried from 86056e5": holds, because the CLI and the cards are byte-identical from 86056e5 to
      1bb3931 (claim 1), and the long gate at 1bb3931 re-ran step 19b (claim 7).
    - Review box ("inspector approved at 86056e5 and at 1448479 (S4 fix and restack); carried to 1bb3931 (restack
      onto main, same tree as 1448479, range-diff patches identical)"). `chantier log CR-242` has
      `inspector approved at 86056e5 (restack)` at 12:38:02Z and `inspector approved at 1448479 (restack onto
      b394a35 and the S4 fix; range-diff patches identical)` at 13:40:27Z. The carry's reason holds by the move
      above (same tree, identical range-diff), and the Driver's note at 13:57:00Z records that move. PASS.
    - "CI green at 1bb3931 (all five jobs pass)": backed by claim 9.
    - "Verified at 1bb3931 (pending)" is left unticked, which was true when it was written.
    - Known gaps is accurate. The gitlab gap is gone, which is correct because gitlab passed at this head (claim 7).
      The slot-2 surface check creates its files by hand (`scenario/run_scenario.py:6280-6286`). Making
      `just scenario` isolable per worktree is out of scope. No claim is UNVERIFIED, no evidence pair is missing,
      and no failed claim was accepted.
    - No STALE mark is left.
