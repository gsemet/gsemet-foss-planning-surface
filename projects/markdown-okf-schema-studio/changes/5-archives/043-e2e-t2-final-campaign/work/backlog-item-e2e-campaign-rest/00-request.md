# E2E campaign rest — P9 T1, B5, T2, F (P2, decided 2026-10-22)

P9 (e2e campaign audit) landed B1–B4 in PR #11. Remaining, parked for the PR:

- **T1** real-window capture registry + shared evidence writer, dedupe (~117 -> ~102), clips,
  gallery integration, README real-window sources. Stopped mid-way: WIP in git `stash@{0}`
  ("P9-T1 WIP (parked for PR, U37)") and as a patch + tar in
  `archives/021-feature-session-007-020/p9-e2e/parked/` (moved there at session end).
- **B5** visual gaps for extension states (~21) + high-contrast exploratory.
- **T2** real-window gaps: untrusted workspace, standalone, incoming changes (014 has no
  screenshot), conf.py warning, comment threads, paste image (018 has no screenshot).
- **F** final full campaign, gallery, README check, inventory regenerated.

Plan, inventory and state: `archives/021-feature-session-007-020/p9-e2e/` (plan.md, STATE.md).
Before P10 requirements (the campaign is their baseline).
Watch: CI flake seen once on PR #11 — visual `sticky-3 light [read:properties] 1 control sits
under the toolbar` (passed on the runs before).

## Split (user, 2026-10-22)

4 CRs in order: B5 → `requests/029-e2e-b5-extension-states`, then T1, T2, F (still here).
- High contrast removed from B5.
- T1/T2/F: real-window tests must be runnable locally at least at the end of the development, and
  several runs may happen in parallel (unique user-data/extensions dirs, CDP ports, evidence folders).
- T1 restarts from the plan on current main; the parked patch/stash is only a reference.
