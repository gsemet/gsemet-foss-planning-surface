# 043 — e2e-t2-final-campaign

From backlog `P2/e2e-campaign-rest` (copied here as `backlog-00-request.md`). Last P2 item.

## Problem

P9 T2 and F remain: real-window gaps (untrusted window, standalone, incoming changes, conf.py
warning, review threads, image paste, label rename, Back/Next, refreshPreview + keybinding,
doubleClickToSwitchToEditor) and the final full campaign (gallery, README image check, inventory).

## Decisions (user grill, 2026-10-23)

1. One CR, one PR: T2 then F, as plan.md section 6 "T2" and "F"
   (archives/021-feature-session-007-020/p9-e2e/plan.md), on current main (T1 = CR 040 landed).
2. Spikes (untrusted capture, standalone, incoming changes): a spike that is unstable is
   abandoned and listed in `followups.md` (and the PR), it never blocks the PR. No new flaky test.
3. Real-window tests run in CI only (job `integration`, xvfb). Agents never open a VS Code window
   on the user's machine. They still keep the local command working and isolated (unique
   user-data/extensions dirs, CDP ports, evidence folders, as T1 made it).
4. New real-window captures go in the required `integration` job only if stable: each new
   scenario must pass the stress mode (`just ci-stress`, CI rule 12; add it to the stress plan)
   before it lands as required. One that is not stable goes advisory (stress job) or to followups.
5. Speed (as CR 041): driver, coders and reviewers on Opus; coder gates tsc + unit + `just check`
   + `just visual`; reviewer checks the round diff; ready as soon as the required `checks` job is
   green and the PR is mergeable. Rounds: 3.
6. F runs from CI artifacts (the full campaign in CI), README images byte-compared with B0
   expectations; `images/` committed only when the difference is intended.

## Re-scope (user, 2026-10-23 afternoon) — overrides decisions 3 and 4

7. Option B: reduced T2. Keep only the gaps that need a real VS Code: incoming changes (014 has
   no screenshot), image paste (018 has no screenshot), Restricted Mode (untrusted window), review
   comment threads. Standalone, conf.py warning, label rename, Back/Next, refreshPreview keybinding
   and doubleClickToSwitchToEditor go to `followups.md` (main-session choice, user may correct).
8. CI: the required path keeps only the simulated tests (Playwright/Chromium: static, visual,
   report). The heavy real-VS Code tests (integration and stress) move to an optional job that
   does not run by default: manual trigger (`workflow_dispatch` input), not in `checks`.
9. Local: the real-VS Code tests must pass locally with a real VS Code. The user allows running
   them on their machine (one run at a time, `requests/WINDOW-TESTS.lock`). Done = local
   integration green + CI required checks green + the manual heavy job run once on the PR branch.
