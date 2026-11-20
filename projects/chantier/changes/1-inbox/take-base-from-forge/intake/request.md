# take's base and the PR-in-draft label from the forge, not the order

Priority P2. From the Studio project's batch-06 retro (kept by its retro-critic), relayed by its Chief of Staff, 2026-11-20; chantier's batch-29 saw the same label.

For stacked CRs (Studio's CR-424, CR-427, CR-429), `take` printed the wrong worktree base, and the Foreman told each Driver to branch from origin/main. A stale "PR in draft ... after CR-425" label also went into an ask. Chantier's batch-29 showed the same "PR in draft" label on PRs that were out of draft on main (CR-407, 408, 409, 410, 413), because the recorded stack order put them after a CR with no PR.

Derive the base `take` prints and the waits-on / draft label from the forge state of the PRs (their base and draft state), not from the recorded order.
