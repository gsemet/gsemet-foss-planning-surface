Head: 37f0cb0e4fd1766cdf13ce385d39fb7d256d4130

All claims judged at 37f0cb0 (the pushed head). Long gate waived by the user; not run. CI green at the head (per the Driver's brief).

1. ship refuses a merge commit above its base (exit 2, records nothing, rebase line), accepts a linear branch, refuses an unreadable base, fallback base, stack lower-CR case, --conflict: judged at 37f0cb0.
   Command: uv run --no-sync pytest tests/test_carry_ship.py -k merge_commit -q (in skills/chantier/scripts/cli)
   Output: `7 passed, 15 deselected in 15.17s`. The 7 cases (main merged in, the CR below merged in, a merge only below, fallback base, unreadable base, after a rebase, --conflict) assert exit 2, the message words ("holds a merge commit" / "cannot check", "rebase", "--force-with-lease", "fetch and ship again"), no new ship event, no carry event, no pr/head in the record; the linear and below-only cases exit 0 with one new ship event. Code read: merge_check.refuse_merge_commit runs `git rev-list --merges <lower>..<head>` (check=True), called in delivery.ship before read_state.
2. Cards say rebase only: concepts.md rule 8 and exit-2 list, driver.md (rebase means, carries bullet, folded paragraph, stack driver), conflict-resolver.md: judged at 37f0cb0 by `git show HEAD` diff read (rebase-only, no --rebase-merges, no "Update branch" button, forge rebase action unproved with trial named).
3. Four agent descriptions on both hosts: judged at 37f0cb0.
   Command: grep -h "^description" agents/{cr-driver,release-driver,stack-driver,conflict-resolver}.md com.github.copilot/agents/chantier-*.agent.md
   Output: all eight lines carry "updating its branch by rebase only" / "restacks by rebase only" / "(never a merge)", identical per pair.
4. Scenario check and README line exist: judged at 37f0cb0 (scenario/run_scenario.py adds the CR-101 merge-commit refusal and the reset-then-ship check; scenario/README.md ship item names it). Not run (full scenario excluded by brief).
5. PR description draft (work/pr-body.md) vs diff: Summary, Deliverables table, Changes, Autonomous decisions (merge_check.py module, note in driver carries section) match the diff; Known gaps lists the unproved forge rebase and ship-only check. Test plan boxes (Review, Verified, CI sha7) are still template placeholders in the draft, to be filled by the Driver at posting; no images.

VERIFIED

Description pass at 37f0cb0 (posted body, gh pr view 442 --json body): structure, fold, Test plan SHAs, Review note (f4c1bcc, committed as 37f0cb0, in `log`), CI (all five checks SUCCESS) and Changes/Deliverables vs diff are right. One failure: Known gaps omits that the local long gate failed twice on Windows and was waived (it appears only in the Test plan); that is a knowingly shipped unproven item. Minor: the sample message shows `<base>` where the code prints `origin/main`-style `{name}`.

NOT VERIFIED

## Description pass (second start), judged at 37f0cb0e4fd1766cdf13ce385d39fb7d256d4130

Command: gh pr view 442 --json body; gh pr diff 442 --name-only. Body renders (fold with blank lines), sections in order, Known gaps now names the waived local long gate, the unproved forge rebase and the ship-only check; sample message matches merge_check.py; Review box f4c1bcc / committed 37f0cb0 matches the driver note; no images; no internal references outside Internal references; Summary/Deliverables/Changes match the 17 files of the diff. Description: VERIFIED.

VERIFIED
