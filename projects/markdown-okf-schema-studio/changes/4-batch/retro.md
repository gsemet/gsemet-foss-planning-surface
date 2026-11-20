## 2026-11-20: CR-340..CR-351, CR-424..CR-434 (batch-06)

- [chantier] A second stack Driver was started on a CR whose record the first had already left, 25 minutes before the first one's hand-back arrived: a subagent Driver cannot SendMessage a Desktop `local_` Foreman session (its hand-back reaches the Foreman only as its final report), and `hosts/claude-code.md` lists "SendMessage to main" as proved: correct that row for a Desktop Foreman, and name in the stack-driver prompt's `Steering:` line what a subagent sends.
- [chantier] The worktree base `take` printed for a CR in a stack was wrong several times (CR-424, CR-427, CR-429: the Foreman told each Driver to create its worktree on origin/main), and the stale "PR in draft … after CR-425" label went into ask A-30: derive the printed base and the waits-on label from the forge state of the PRs, not from the recorded order.
- [project] "Filename too long" blocked a base checkout or worktree five times (CR-348, CR-350, CR-427, CR-431, CR-432), so fail-before claims went into PR bodies as UNVERIFIED: set `core.longpaths` (or a shorter worktree root) in the project's `AGENTS.md` and guidelines so a Verifier can check out the base.
- [project] The paste-url real-window flake went red twice (CR-350 dispatch 44647675614, CR-424 heavy run) and has no open item; `realinput-t45`, `previewManager.test.ts:162` and the checkbox-toggle timeout are already filed: file paste-url (and the drop-files case) and add both to the default stress scenarios.

(critic: kept 4, dropped 6)
