# Retro, batch-30 (Foreman n°2)

Stack batch, 36 CRs merged, $292.64, no budget. Judged by the retro-critic: 4 kept, 10 dropped (9 already covered by open items).

## Kept (offered to the Chief of Staff as inbox items)

1. Pane screenshots go in as permalinks off the CR branch, so a restack never conflicts on a binary (restack conflicts on screenshots; `--attach` gave 403).
2. The scenario's serve/webui cases take a free port and init their own folders, so a local `just scenario` passes while the user's board runs (the `serve_and_webui` case failed on its first CI run: no `init`, `--seat` without `seat take`; locally it fails at the webui step because port 8765 is held, so the top CR's Windows run was waived twice).
3. A Verifier's throwaway board server stops with the Verifier and never outlives it to lock a CR folder (CR-460: `order merged` blocked until the user stopped PID 35708).
4. The scenario's welcome check reads the op count from `protocol.OPS`, and a Driver that touches the protocol runs the scenario unit (CR-449 and CR-458 broke in turn).

## Dropped, covered by open items

- Driver context limits and duplicate hand-backs: 1-inbox/driver-context-second-cut, 2-backlog/P1/role-cards-still-too-big-for-a-driver-s-.
- `take` wrong bases and reclaim, SHA rewrite by rebase-merge, `ship` `off:`: 2-backlog/P1/stack-batch-frictions-duplicate-commits-.
- Flaky tests: 2-backlog/P1/two-flaky-tests-of-batch-30 (add the `[only-one]` variant to its request).
- Stack re-sequencing: 2-backlog/P1/order-after-add-one-predecessor-without-, 2-backlog/P1/check-that-a-stack-s-branches-really-cha.
- Dropped as unmeasured or by design: round-limit exceptions (CR-449 six, CR-456 seven, each on the user's yes), STARTUP_LIMIT headroom, `forge-stack show` stale checks, one wrong-base rebase slip.

## After the retro (resumed batch: CR-461, CR-462)

- The release Driver ran out of context before `just release minor` (140k tokens in the notes and claims drafts); a second Driver finished. Release drafts of 94 rows belong in a worker, not the Driver.
- `just release minor` uses `-am`, which left `claims-v0.15.0.md` untracked; the Driver added it as a second commit, so origin/main's head was no longer "release: v0.15.0" and `just tag` stopped at check-tag. Candidate inbox item: the release recipe stages new files named by the release (or the release Driver commits them before `just release`), so the version commit stays the head.
