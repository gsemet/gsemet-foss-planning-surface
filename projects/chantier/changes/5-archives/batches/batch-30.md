# batch-30

Opened 2026-11-21T16:55:33Z, closed 2026-11-22T22:40:25Z, stack, steered by Foreman, no budget, final cost $298.48. [batch-30.json](batch-30.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-425](../261121-1801-425-factory-redefine/) | Running batch or next batch: the factory mode removed | merged | https://github.com/gsemet/chantier/pull/398 | 1 | $8.55 |
| [CR-429](../261122-0802-429-board-fingerprint-cache/) | The server watches the planning files; boards and watchers subscribe | merged | https://github.com/gsemet/chantier/pull/414 | 5 | $37.12 |
| [CR-430](../261121-1909-430-park-live-cr/) | The Foreman parks a CR stuck on an outside wait | merged | https://github.com/gsemet/chantier/pull/400 | 2 | $7.68 |
| [CR-431](../261121-2058-431-hold-live-cr/) | `order hold` of a live CR, in every batch mode | merged | https://github.com/gsemet/chantier/pull/399 | 3 | $8.64 |
| [CR-433](../261122-0718-433-board-batch-chip-stale/) | A batch CR's card shows its batch folder, not its old 3-ready chip | merged | https://github.com/gsemet/chantier/pull/406 | 1 | $5.22 |
| [CR-438](../261122-1225-438-stack-shape-guard/) | A stack batch keeps its shape after the Foreman's compactions | merged | https://github.com/gsemet/chantier/pull/412 | 4 | $7.98 |
| [CR-426](../261121-1748-426-board-exposure/) | The board stays on this machine unless asked, with a key you can rotate | merged | https://github.com/gsemet/chantier/pull/397 | 1 | $2.80 |
| [CR-427](../261121-2058-427-board-running-batch-lane/) | Board backlog: last column split into running batch and next batch | merged | https://github.com/gsemet/chantier/pull/401 | 3 | $4.82 |
| [CR-435](../261122-1106-435-board-batch-compact/) | Batch page: the mode and the legend move into the title row | merged | https://github.com/gsemet/chantier/pull/408 | 2 | $7.44 |
| [CR-436](../261122-0718-436-sync-blocked-by-others/) | Dev mode only for chantier itself; other projects in plugin mode | merged | https://github.com/gsemet/chantier/pull/405 | 1 | $5.19 |
| [CR-439](../261122-1225-439-board-help-page/) | Web board: a Help page of chantier's concepts and roles | merged | https://github.com/gsemet/chantier/pull/411 | 3 | $10.35 |
| [CR-432](../261121-2058-432-permissions-bypass/) | chantier's allow rules name real paths, not a wildcard | merged | https://github.com/gsemet/chantier/pull/402 | 2 | $3.67 |
| [CR-440](../261122-1106-440-board-triage-polish/) | Triage: fold each priority row, explain the writes-since-rescan count | merged | https://github.com/gsemet/chantier/pull/410 | 1 | $6.42 |
| [CR-449](../261122-1336-449-board-griller/) | A Griller started from the web board | merged | https://github.com/gsemet/chantier/pull/428 | 4 | $11.02 |
| [CR-428](../261121-2235-428-drop-to-next-batch/) | A CR taken out of a batch goes to the backlog, ready or the trash | merged | https://github.com/gsemet/chantier/pull/403 | 3 | $5.50 |
| [CR-441](../261122-1106-441-board-batch-view/) | Batch graph: one arrowhead per CR, lit arrows on top, a mode tooltip | merged | https://github.com/gsemet/chantier/pull/415 | 1 | $4.23 |
| [CR-455](../261122-1408-455-take-base-on-working-draft/) | A stack CR starts on another CR's branch only once that CR is ready | merged | https://github.com/gsemet/chantier/pull/421 | 4 | $6.33 |
| [CR-442](../261122-1106-442-stack-git-chain/) | An ordered stack is checked as a git chain | merged | https://github.com/gsemet/chantier/pull/417 | 2 | $6.64 |
| [CR-456](../261122-1513-456-rename-the-surface-server-command-to-ser/) | Rename the surface server's command to `serve`; add `webui` | merged | https://github.com/gsemet/chantier/pull/430 | 7 | $9.70 |
| [CR-443](../261122-1106-443-gate-hold-narrowing/) | gate runs only named commands; lease hold runs nothing | merged | https://github.com/gsemet/chantier/pull/416 | 3 | $10.02 |
| [CR-457](../261122-1625-457-two-board-keys-a-public-read-only-key-an/) | Two board keys: a public read-only key and a private key | merged | https://github.com/gsemet/chantier/pull/432 | 2 | $4.89 |
| [CR-434](../261121-2235-434-board-batch-kanban/) | Batch page: a Kanban of the batch's three folders | merged | https://github.com/gsemet/chantier/pull/407 | 1 | $3.17 |
| [CR-445](../261122-1106-445-board-history/) | Web board History page: what was done per day, week or month | merged | https://github.com/gsemet/chantier/pull/419 | 3 | $6.41 |
| [CR-458](../261122-1719-458-remote-cli-commands-through-the-surface/) | Remote CLI commands through the surface server: `login`, profiles, `cli.run` | merged | https://github.com/gsemet/chantier/pull/434 | 2 | $6.01 |
| [CR-446](../261122-1106-446-live-several-boards-and-keys/) | live: keys to scroll and filter, and up to 4 boards in one screen | merged | https://github.com/gsemet/chantier/pull/418 | 1 | $3.97 |
| [CR-459](../261122-1226-459-batch-graph-transitive-reduction-fold-me/) | Batch graph: transitive reduction, merged CRs folded, fewer crossings | merged | https://github.com/gsemet/chantier/pull/431 | 3 | $3.55 |
| [CR-437](../261122-0850-437-sync-lock-wait/) | A blocked uv sync names chantier's holders, waits, never kills | merged | https://github.com/gsemet/chantier/pull/409 | 1 | $5.74 |
| [CR-447](../261122-1758-447-docs-gardening/) | Garden the docs, the README and the SVGs after batch-30 | merged | https://github.com/gsemet/chantier/pull/435 | 2 | $5.38 |
| [CR-444](../261122-0901-444-board-user-inbox/) | Web board: an Inbox page of what needs the user | merged | https://github.com/gsemet/chantier/pull/426 | 1 | $6.09 |
| [CR-453](../261122-0819-453-agents-md-names-cli-forge-reads/) | AGENTS.md names the CLI's forge calls | merged | https://github.com/gsemet/chantier/pull/425 | 1 | $1.61 |
| [CR-448](../261122-0740-448-dashboard-pages/) | Web board Dashboard page: productivity and spending by closed batch | merged | https://github.com/gsemet/chantier/pull/420 | 3 | $8.05 |
| [CR-454](../261122-0920-454-surface-server-foreign-build/) | Tell a dev session when the surface server runs a foreign build | merged | https://github.com/gsemet/chantier/pull/427 | 3 | $3.29 |
| [CR-450](../261122-0735-450-push-refusal-ladder/) | A refused push climbs: Foreman, then Chief of Staff, then the user | merged | https://github.com/gsemet/chantier/pull/422 | 1 | $3.86 |
| [CR-451](../261122-0735-451-board-folder-lock-windows/) | A held CR folder: wait it out on Windows, then refuse with the cause | merged | https://github.com/gsemet/chantier/pull/423 | 2 | $2.35 |
| [CR-452](../261122-0723-452-store-reads-rest/) | the last readers onto the store, run-time proof | merged | https://github.com/gsemet/chantier/pull/424 | 3 | $6.19 |
| [CR-460](../261122-1717-460-board-key-survives-several-boards-and-a/) | Board key: several boards in one browser, a paste field, SameSite=Lax | merged | https://github.com/gsemet/chantier/pull/433 | 1 | $2.40 |
| [CR-461](../261122-2120-461-two-flaky-tests-of-batch-30/) | Make two flaky tests deterministic | merged | https://github.com/gsemet/chantier/pull/437 | 1 | $2.44 |
| [CR-462](../261122-2238-462-release-v0-15-0/) | Version PR for chantier v0.15.0 | merged | https://github.com/gsemet/chantier/pull/438 | 0 | $1.11 |

## Cost

- Total: $298.48, no budget
- Chief of Staff, steering the batch and Foreman $41.53 (14%), Drivers $93.46 (31%), workers $163.49 (55%)
- Most: CR-429 $37.12, other $11.13, CR-449 $11.02
- Chief of Staff, steering the batch and Foreman: 406 wakes, context 181,773 tokens on average, 266,967 at its peak
- Driver chantier:cr-driver with its workers: $233.52 (9752 calls)
- Driver chantier:stack-driver with its workers: $19.35 (928 calls)
- Driver chantier:release-driver with its workers: $1.11 (48 calls)
- Chief of Staff, steering the batch (outside the budget): $85.43 since the batch opened (1034 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $150.57 since the batch opened (3158 calls, 67 spec-writers, 38 spec critics)
- Chief of Staff, whole session: $1688.48 ($2.52 of it in the batch's spend), context 127,414 tokens; not counted: 17 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)

## Retro

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
