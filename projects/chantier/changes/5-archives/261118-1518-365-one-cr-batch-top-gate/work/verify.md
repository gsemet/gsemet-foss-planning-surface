# Verify CR-365

Head: c586ff068c6afb7e331c834b78bb39942d48e5a3

All claims judged at c586ff06 (`git rev-parse HEAD` in the worktree; PR 329 headRefOid equals it).
Commands: `git diff origin/main` (read in full), `git diff origin/main --name-only`, `git grep -n "local gate <cr> at" HEAD -- skills`.

1. No change outside the three cards: `--name-only` printed exactly chief-of-staff.md, driver.md, foreman.md (skills/chantier/references/). No CLI, hook, agent, doc change. OK.
2. Same top definition: driver.md long-gate bullet and foreman.md boundaries bullet carry the same words ("last open CR other than a release CR (every other non-release CR merged or cancelled; a fix CR counts; a one-CR batch's CR from the start), or, when the last open non-release CRs are all handed back ready and no other CR is working or queued, the last of them in `status`'s order"). OK.
3. Clause form identical to CR-359's: `local gate <cr> at <sha7>: passed|failed|not run` in foreman.md:455 (asks list), foreman.md:130/132, chief-of-staff.md:1028, matching CR-359's existing uses (driver.md:939/966/978, chief-of-staff.md:1088). OK.
4. Both Foreman moments: foreman.md bullets "at each ready hand-back" and "when it becomes the top later" (merge, drop, cancel leaving one non-release CR open or only ready ones). OK.
5. Gate note inside the rebase take, parallel and series: both sub-bullets of the `order merged` bullet add `take <cr> --note "rebase: <merged cr> merged; long gate: ...locally"`, "no separate gate take"; the boundaries bullet says "never a second one". OK.
6. Driver reads plain `status` before the `ship` preceding the ready hand-back: driver.md long-gate bullet. OK.
7. Waiver exception: driver.md hand-back waiver sentence and foreman.md waiver check, both read words from `status` order list then `STATUS.json` (`gate.waiver`). OK.
8. Chief of Staff: clause paragraph (1028), all-ready offer exception, several merges with top last, gates forecast counting top once. All in diff. OK.
9. Copilot unproved sentence: foreman.md "The Copilot host's path is unproved (as for the stack's top above)". OK.
10. Asks list tails on `ready-to-merge` and `pr-in-draft` (foreman.md:455); "Deliver by a time" sentence added. OK.
11. Every `take` form is `take <cr> --note "..."` (no --epoch) in the added Foreman text. OK.
12. PR description (work/pr-body.md; forge body checked with `gh pr view 329`): Summary, Deliverables, Changes match the diff (three cards, listed items present); Known gaps hold both spec gaps; no image; no role-name issue seen. The forge body's Test plan boxes (Local gates, Review, Verified, CI) are still unfilled placeholders `<sha7>`: the Driver fills them at hand-back (note: `log` holds "r1 inspector approved at 4a49d5c7" and "approved at 4a49d5c7, committed as c586ff06", which supports Review). Not a failure now.
13. CI green all 5 jobs and local `just check`: stated in the brief, not rerun by me; not claimed as my proof.
14. Windows local gate owed by the Driver per AGENTS.md as batch top: not in my scope; not claimed.

VERIFIED


## Description pass at c586ff068c6afb7e331c834b78bb39942d48e5a3

Head: c586ff068c6afb7e331c834b78bb39942d48e5a3

- Posted body (`gh pr view 329 --json body,headRefOid`, headRefOid c586ff06): renders (sections, fold with blank lines, no images); matches `git diff --stat origin/main...HEAD` (3 cards: driver.md, foreman.md, chief-of-staff.md, no code), same as Changes and Blast radius.
- Test plan SHAs all c586ff0 = head. CI: `gh pr checks 329` all 5 jobs pass (incl. just scenario ubuntu). Review box: `log CR-365` note "r1 approved at 4a49d5c7, committed as c586ff06" proves it. Verified box: the VERIFIED verdict at c586ff06 in the log.
- Known gaps lists the unproved Copilot path and behaviour; no UNVERIFIED/STALE marks. Role names are product terms of the cards changed; Internal references holds the CR names.

VERIFIED
