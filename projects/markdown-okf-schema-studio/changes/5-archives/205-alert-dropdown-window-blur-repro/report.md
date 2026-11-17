# Report: CR 205

PR [#232](https://github.com/gsemet/markdown-okf-schema-studio/pull/232), merged commit 48916687. Landed 2026-10-31 in stack #230 → #234 (gh stack 235, rebase merge by the user, main 5ebd3b2f). Top heavy run 41151371662 on tree abe65ccbb2525d9e48e5aacc2778aff79e7f270a: attempt 1 red only on the known alert-dropdown flake (stress round 7/20), `--failed` green. Final Opus Inspector on the whole stack: APPROVE (nits in P3 stack-230-234-followups).

- Reproduced once in 200 rounds (run 41145454738), root cause not found (signature: textarea blur, related=none, page keeps focus, the webview frame loses focus inside the window).
- Lands the `stress_repeat` / `stress_scenarios` knob of the manual CI run, to loop chosen stress scenarios. Backlog item P2 alert-dropdown-window-blur stays open.

## Backlog item (archived 2026-10-31)

The backlog item `alert-dropdown-window-blur` is kept in [backlog-item/](backlog-item/). Reproduced once in 200 rounds, cause not found; on watch (owner, 2026-10-31). Earlier CRs on the same flake (180, 186, 194) are not archived again.
