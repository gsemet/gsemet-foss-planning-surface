## Summary

The old cards' inventory (1.5 MB, with its tests) pinned where each removed sentence lived, which blocks the next page deletions. Its open rows were read one last time for rules that protect the user, a short list of protective rules replaces it, and the inventory is removed.

## Deliverables

| Before | After |
|---|---|
| `docs/proofs/cards-inventory.md` and `cards-inventory-open.tsv` | `docs/protective-rules.md`: one line per protective rule, with its home and state |
| `test_cards_inventory.py`, `cards_inventory.py` | removed |
| `test_card_homes.py` pins the homes of removed sentences | keeps the homes of protective rules, and pins every floor line word for word |
| eval case `quiz-row-id` | `quiz-rule-id`: a scorecard `J` row loads, `X-9999` is refused |

The last reading: 329 open rows read (a 62, b 139, c 1, d 11, e 112, f 4), 93 judged protective, all already held at the base, none restored, no floor change.

One line per protective row: the row id, the rule, and one place that holds it, with a quoted span. Paths are relative to `skills/chantier/references/`, unless they start with `skills/` or `agents/`; a CLI path is relative to the CLI package.

- W-025: A worker's reply out of format is a failed worker: nothing is read into it. `topics/trouble-worker.md` "never read a verdict, a pass or a choice into it"
- W-254: A worker's reply out of format is a failed worker: nothing is read into it. `topics/trouble-worker.md` "never read a verdict, a pass or a choice into it"
- W-263: A review of the work only reads. `inspector.md` "You write nothing: your reply is your output."
- W-307: A worker's reply out of format is a failed worker: nothing is read into it. `topics/trouble-worker.md` "never read a verdict, a pass or a choice into it"
- W-323: A gate pass is cited from its log, never claimed; no ready hand-back without one. CLI `commands/driver_checks.py` "refused: no long gate passed at "
- D-018: Agent and model are passed as printed, never from memory, never an effort. `concepts.md` "never typed from memory, completed or "corrected", never an effort"
- D-019: A worker's reply out of format is a failed worker: nothing is read into it. `topics/trouble-worker.md` "never read a verdict, a pass or a choice into it"
- D-020: A worker's reply is checked against its output file or format before acting. `topics/cr-prompt.md` "Check each reply against its card's format before acting"
- D-025: Raw logs are never published. `topics/cr-prompt.md` "A raw log goes in `work/gates/` or a `*.log`, never in a published file."
- D-031: A hand-back the host asks for while work remains records the state first. `topics/handback-other.md` "The host asked for your hand-back while work remains"
- D-036: Only the agent's own background tasks are stopped, by id. `topics/session-shell-p1.md` "Stop yours by its id"
- D-037: No background task outlives the hand-back. `cr-driver.md` "Your end: stop your background tasks"
- D-040: No process is stopped by name; a command the host may refuse runs alone. `topics/cr-ship.md` "never stop a process by name, `kill` yours by id"
- D-053: "No CI" is never claimed on one look. `topics/ci-no-check.md` ""No CI" needs two looks a minute apart."
- D-056: With an early push or CI beside the long gate, the PR is a draft until both are green at that head. `topics/conflicts-early-push.md` "The PR leaves draft (`gh pr ready`, `glab mr update --ready`, then `ship`) only once the gate has passed"
- D-058: Real commit messages: no wip, no internal reference. `topics/cr-ship.md` "Never `wip`, "pending", "checkpoint""
- D-064: A blocked hand-back says what is wrong and what next, state recorded first. `topics/handback-other.md` "A decision only the user can take is `blocked question: <text>`."
- D-065: A refused wait or hand-back is not worked around. `topics/handback-other.md` "A `--wait` the CLI refuses is not worked around"
- D-068: Commit by name; never stash, `add -A`, `reset --hard` or discard work. `cr-driver.md` "`git reset --hard` or anything that discards the worktree's work"
- D-070: A later PR body edit is verified again; ready only on the default branch. `topics/closing.md` "any later edit runs the pass again before the PR turns ready"
- P-002: A lost claim stops the agent; only the steering session reclaims. `topics/lease.md` "Stop at once, record nothing more, tell the steering session."
- P-003: A checkpoint commit has a real message. `topics/cr-ship.md` "so each commit, a checkpoint included, has a message in the project's commit style"
- P-006: A second take never opens a second PR and never resets hard. `topics/retake.md` "never a second PR"
- P-007: In a stack, the branch below is rebased only on a note or a refusal, never reset hard. `topics/retake-notes.md` "never `reset --hard`"
- P-008: No probe of the board's write paths on the live planning folder. `coder.md` "point a test or probe of the board's write paths at the live planning folder"
- P-010: A creating remote command is not re-run before checking it did not take effect. `topics/trouble-remote.md` "check whether the first attempt took effect"
- P-013: A resolved conflict voids every earlier pass and verdict. `topics/conflicts.md` "takes `--conflict`: it voids every earlier pass, verdict and carry"
- P-014: No skipped proof, no worked-around refusal, nothing touched on a merged change. `topics/handback-other.md` "Never skip a proof pass to save budget"
- FM-062: A start prompt is passed as printed. `foreman.md` "pass, unchanged, the output of the `brief:` command"
- FM-064: A start prompt is passed as printed. `foreman.md` "pass, unchanged, the output of the `brief:` command"
- FM-B047: A change taken back is shipped, gated and verified again before ready. CLI `commands/driver_checks.py` "A ready CR is shipped at the worktree's head, clean, pushed, gated and verified."
- FM-404: A running gate is left alone when an ended agent wakes. `topics/lost-driver.md` "With a gate running, leave it."
- FM-486: The early conflict check changes no PR and switches no mode on its own. `topics/chain-conflict.md` "each PR stays ready to merge on its own"
- FM-552: A push is not tried when its route rule is missing or may be denied. `topics/refused-push-route.md` "Missing: push nothing"
- FM-586: A rebase is not tried when its rule is missing or denied. `topics/refused-rebase.md` "rebase nothing"

- C-003: The steering session never does the implementing agents' work and starts no implementer. `chief-of-staff.md` "let a subagent implement."
- C-023: The watcher and the board start only on the user's yes. `chief-of-staff.md` "started on the session's yes"
- C-024: Configuration files are edited only on the user's word. `topics/config-p1.md` "only on the user's word"
- C-027: Project rules are written only on the user's word. `chief-of-staff.md` "So are `git init`, an install, project file writes"
- C-034: A new board key or network exposure only on the user's word. `topics/remote-login.md` "on the user's word, `board.host: network`"
- C-472: A path never tested is said to be untested. `chief-of-staff.md` "or as fact what the host marks unproved"
- C-625: The watcher and the board start only on the user's yes. `topics/watcher.md` "A no starts neither"
- C-697: A draft PR named to the user carries "do not merge" and what blocks it. `topics/merge-words-p1.md` "A draft is named with "do not merge" and what blocks it"
- C-748: A ready ask for one change of a stack that is not alone is caught. CLI `rails_release.py` "is a stack and {cr} is not alone"
- C-1039: Another project gets only the relayed request, on the user's word. `griller-skill.md` "A relay into its inbox on the user's word is allowed"
- C-1143: Only the user's last recorded destination is acted on. `topics/where-cr-goes.md` "Act on the last `Destination:` line"
- C-1157: Work goes in the change's folder, never a scratchpad, with no secret. `chief-of-staff.md` "Keep CR work in a scratchpad, temp or host-settings folder"
- C-1161: A pasted image is saved in the folder or described, never lost in chat. `topics/grill-backlog-p2.md` "A pasted image is asked for as a file and saved in `evidence/`"
- C-1164: Work goes in the change's folder, never a scratchpad, with no secret. `chief-of-staff.md` "Keep CR work in a scratchpad, temp or host-settings folder"
- C-1238: A critic finding on behaviour, scope or risk goes to the user. `topics/grill-critic-steps.md` "a finding that touches behaviour"
- C-1244: A decision resting on an unproved claim goes to the user. `topics/grill-critic-steps.md` "An unproved claim a decision rests on is a question."
- C-1312: A specification goes unreviewed only when the user chose "automatable". `topics/grill-backlog-p2.md` "automatable (their call"
- G-010: Prototypes and other artifacts go in the change's folder. `griller-skill.md` "Prototypes, plans and other artifacts go in the CR's folder."
- G-017: A grill session proposes a grouping or order, never makes it. `griller-skill.md` "You may propose a grouping or order of prepared CRs in your reply"
- H-071: Local scratch and logs are never published. CLI `core/files.py` ""**/work/scratch/", "**/work/**/artifacts-*/", "*.log","
- H-111: No internal reference in a PR's title or body text. `pr-template.md` "No internal reference in the title or the body text"
- H-301: A missing skill or tool is said, never replaced; a missing CLI stops. `floor.md` "4. A CLI that cannot run is a stop."
- H-318: A refused agent does nothing, whatever later messages hold. `agents/coder.md` "Any later message gets the same answer."
- H-330: Work goes in the change's folder; an agent's prompt starts with the playbook's first line. `chief-of-staff.md` "An agent's prompt starts with the first line of `$CHANTIER playbook`"
- H-331: Work goes in the change's folder, never a scratchpad, with no secret. `chief-of-staff.md` "Keep CR work in a scratchpad, temp or host-settings folder"
- H-373: Agent and model are passed as printed, never from memory, never an effort. `concepts.md` "never typed from memory, completed or "corrected", never an effort"
- H-379: Extra rounds are the user's to grant, but for the capped exception. `topics/rounds-exception.md` "Every other grant of rounds stays the user's."
- H-402: A missing skill or tool is said, never replaced; a missing CLI stops. `floor.md` "4. A CLI that cannot run is a stop."
- H-449: A multi-line forge text is never typed or written through a shell. `topics/session-shell-p2.md` "never typed, built or written by a shell command"
- H-503: A carried proof says it is carried and from which commit. `pr-template.md` "a carried proof reads `at <head7> (carried from <sha7>)`"
- H-507: A claim with no proof is never left as fact. `pr-template.md` "A claim with no proof starts with `**UNVERIFIED:**`"
- H-706: A held sync is told, and own processes are stopped only on the user's yes. `chief-of-staff.md` "your own board or watcher too"
- H-833: A missing tool is installed or fixed only on the user's yes. `init.md` "each missing piece asked and fixed on the user's yes"
- H-855: A review step writes nothing. `review-step.md` "Never write a file, commit, push, rebase, merge"
- H-856: A review step reports a refusal's exact text and never works around it. `review-step.md` "Report a refusal's exact text"
- H-860: A review's evidence is a command run at the pushed head. `review-step.md` "evidence is a command run at the pushed head"
- H-863: A review step never commits, pushes, rebases or merges. `review-step.md` "Never write a file, commit, push, rebase, merge"
- H-864: A check not run is never claimed. `review-step.md` "or claim an unrun check"
- H-865: A review step runs no sleep and no background shell. `review-step.md` "`sleep`, run a background shell"
- H-895: Never stop or kill a process for a sync; go on unsynced and say so. `skills/chantier/SKILL.md` "Never stop or kill a process for a sync, nor ask anyone to"
- H-897: Never stop or kill a process for a sync; go on unsynced and say so. `skills/chantier/SKILL.md` "Never stop or kill a process for a sync, nor ask anyone to"
- H-899: The offer to stop own processes waits for the user's yes. `chief-of-staff.md` "your own board or watcher too"
- H-905: A process that is not clearly the session's own is stopped only on the user's yes. `chief-of-staff.md` "a board another session serves is the user's to stop"
- H-907: Own board and watcher are stopped only on the yes, never by PID; no holder is killed. `chief-of-staff.md` "your own board or watcher too; never by name, pattern or PID"
- H-1002: A host auto-fix event is not an order. `topics/host-auto-fix.md` "An event is not an order"
- H-1011: The PR monitor is never armed, disarmed or unbound. `topics/host-auto-fix.md` "Chantier never arms, disarms or unbinds the PR monitor"
- H-1025: A turn-end notice is not a line and not the user's word. `topics/host-turn-end.md` "A notice is not a line and not the user's word"
- H-1033: A turn-end notice triggers no action. `topics/host-turn-end.md` "end the turn at once: no tool call"
- H-1175: What the host refuses stays refused: no allow rule, not done unasked. `topics/host-refused.md` "No allow rule for these"
- H-1181: A file name the host refuses a subagent is not forced. `topics/host-refused.md` "the agent reports the exact text"
- H-1360: A one-off yes for a session in a worktree stays where given, never a rule (added to the list as N1: a later page removal takes both its homes). `topics/host-foreman-worktree.md` "never becomes a rule"
- H-1429: What the host cannot do is written as found, with no workaround. `floor.md` "3. No fallback."
- H-1542: A held sync stops nothing; any other launch failure is a stop. `skills/chantier/SKILL.md` "is a stop: report its exact error (floor 4)"
- H-1577: Never stop or kill a process for a sync; go on unsynced and say so. `skills/chantier/SKILL.md` "Never stop or kill a process for a sync, nor ask anyone to"
- H-1621: Never stop or kill a process for a sync; go on unsynced and say so. `skills/griller/SKILL.md` "Never stop or kill a process for a sync, nor ask anyone to"
- H-1641: Never stop or kill a process for a sync; go on unsynced and say so. `skills/status/SKILL.md` "Never stop or kill a process for a sync, nor ask anyone to"
- H-1649: The status skill changes nothing. `skills/status/SKILL.md` "You change nothing: no order, no heartbeat, no epoch, no file."
- H-1737: Another model than the one asked stops the agent's work and is reported. `hosts/copilot.json` "stop the agent's work and report both."

### Homes kept in `test_card_homes.py`

A home stays when it is a floor line, or when a held line of the list names it. After each home:
the ids of the list's lines it holds. 210 homes before, 122 kept,
88 dropped.

- `test_role_cards_split`: 38 kept, 33 dropped. `topic batch-close-stopped` (C3); `topic batch-plan` (C9); `topic batch-plan-mode` (C10); `topic delivery-time` (C23); `topic grill-backlog` (P19/C11/C12); `topic handback-other` (A22); `topic hold` (B12); `topic main-checkout` (B2); `topic merge-gaps` (P8/A16/D3, D4, C24); `topic merge-series-stack` (P6/D7); `topic merge-under-grant` (B10); `topic merge-words` (P1/D1, D2); `topic pr-extras` (A18); `topic recovery` (D19); `topic refused-push` (A14); `topic refused-rebase` (B9); `topic release-merged` (P5/A5/D5/D6, A6); `topic release-ship` (A3, A4); `topic retake` (P14/A1/A2); `topic retro-critic` (B22); `topic retro-route-chantier` (P12/D10, D9); `topic stack-changes` (A13/B13); `topic trials` (D22); `topic trouble-gate` (A24); `topic trouble-git` (P3/A12, P4/A11); `topic trouble-remote` (A7, A8); `topic trouble-worker` (A9); `card chief-of-staff.md` (P2, A15/D13, C21, P5/A5/D5/D6, P7/C16/D21, C9, D14, P10, B19, C22, D17, C2, P12/D10, D12, C7, P17/D15, C3, C19, C20, D16, D19, D23, P18, C23); `card foreman.md` (B1, P2, A14, A15/D13, B2, A13/B13, B16, B10, A8, P13/B5/C5, A21, P16/B3/B4, B15); `card release-driver.md` (A3, P5/A5/D5/D6, A4, A6, A25); `card stack-driver.md` (P3/A12); `card verifier.md` (A19); `floor 1` (P1/D1); `floor 10` (P10, B19, C22); `floor 5` (P3/A12); `floor 6` (P5/A5/D5/D6); `floor 7` (P7/C16/D21, C15); `floor 9` (P9, D11, D22)
- `test_startup_manifest`: 9 kept, 4 dropped. `topic grill-surface` (C17, P7/C16/D21); `topic seat` (D16); `topic session-start` (D24); `card chief-of-staff.md` (P2, A15/D13, C21, P5/A5/D5/D6, P7/C16/D21, C9, D14, P10, B19, C22, D17, C2, P12/D10, D12, C7, P17/D15, C3, C19, C20, D16, D19, D23, P18, C23); `card concepts.md#Starting an agent` (A10); `card foreman.md` (B1, P2, A14, A15/D13, B2, A13/B13, B16, B10, A8, P13/B5/C5, A21, P16/B3/B4, B15); `card griller-skill.md#Never` (P18, C18); `skill chief-of-staff` (B19); `skill griller` (B19)
- `test_session_start_split`: 10 kept, 4 dropped. `topic board-lines` (C22); `topic board-restart` (C22); `topic seat` (D16); `topic sync-offer` (B19); `topic watcher` (D17); `card chief-of-staff.md` (P2, A15/D13, C21, P5/A5/D5/D6, P7/C16/D21, C9, D14, P10, B19, C22, D17, C2, P12/D10, D12, C7, P17/D15, C3, C19, C20, D16, D19, D23, P18, C23); `card griller-skill.md#Never` (P18, C18); `card sync-checkout.md` (B19); `skill chief-of-staff` (B19); `skill griller` (B19)
- `test_stack_chain_cards`: 6 kept, 4 dropped. `topic cr-handback` (A21); `topic refused-push` (A14); `topic release-ship` (A3, A4); `topic retake` (P14/A1/A2); `card cr-driver.md` (P3/A12, P4/A11, A24); `card stack-driver.md` (P3/A12)
- `test_stack_shape`: 5 kept, 4 dropped. `topic batch-plan-mode` (C10); `topic merge-series-stack` (P6/D7); `topic stack-outside` (B11); `card foreman.md` (B1, P2, A14, A15/D13, B2, A13/B13, B16, B10, A8, P13/B5/C5, A21, P16/B3/B4, B15); `floor 7` (P7/C16/D21, C15)
- `test_reload_rules`: 6 kept, 3 dropped. `topic batch-plan-mode` (C10); `topic merge-gaps` (P8/A16/D3, D4, C24); `topic merge-series-stack` (P6/D7); `topic merge-words` (P1/D1, D2); `card foreman.md` (B1, P2, A14, A15/D13, B2, A13/B13, B16, B10, A8, P13/B5/C5, A21, P16/B3/B4, B15); `floor 1` (P1/D1)
- `test_came_back`: 16 kept, 19 dropped. `topic hold` (B12); `topic order-drop` (D8); `topic project-rules` (D23); `topic refused-push` (A14); `topic refused-push-chief` (A15/D13); `topic refused-push-chief-more` (P9); `topic retake` (P14/A1/A2); `topic stack-changes` (A13/B13); `topic watcher-board` (D20); `card chief-of-staff.md` (P2, A15/D13, C21, P5/A5/D5/D6, P7/C16/D21, C9, D14, P10, B19, C22, D17, C2, P12/D10, D12, C7, P17/D15, C3, C19, C20, D16, D19, D23, P18, C23); `card cr-driver.md` (P3/A12, P4/A11, A24); `card foreman.md` (B1, P2, A14, A15/D13, B2, A13/B13, B16, B10, A8, P13/B5/C5, A21, P16/B3/B4, B15); `card routing.md` (P16/B3/B4); `floor 10` (P10, B19, C22); `floor 7` (P7/C16/D21, C15); `floor 9` (P9, D11, D22)
- `test_release_tag`: 2 kept, 0 dropped. `topic release-merged` (P5/A5/D5/D6, A6); `topic release-tag` (B16)
- `test_rebase_rules`: 2 kept, 0 dropped. `topic refused-push` (A14); `topic refused-rebase` (B9)
- `test_cli_stop`: 5 kept, 4 dropped. `card concepts.md#Starting an agent` (A10); `floor 3` (A10); `floor 4` (a floor line, every one stays); `floor 9` (P9, D11, D22); `skill chantier` (B19)
- `test_watcher_step`: 1 kept, 3 dropped. `topic watcher` (D17)
- `test_event_audience`: 2 kept, 1 dropped. `topic seat` (D16); `card chief-of-staff.md` (P2, A15/D13, C21, P5/A5/D5/D6, P7/C16/D21, C9, D14, P10, B19, C22, D17, C2, P12/D10, D12, C7, P17/D15, C3, C19, C20, D16, D19, D23, P18, C23)
- `test_board_restart`: 4 kept, 2 dropped. `topic batch-close-stopped` (C3); `topic board-restart` (C22); `card chief-of-staff.md` (P2, A15/D13, C21, P5/A5/D5/D6, P7/C16/D21, C9, D14, P10, B19, C22, D17, C2, P12/D10, D12, C7, P17/D15, C3, C19, C20, D16, D19, D23, P18, C23); `floor 10` (P10, B19, C22)
- `test_command_names`: 2 kept, 0 dropped. `card sync-checkout.md` (B19); `skill chief-of-staff` (B19)
- `test_release_template_card`: 2 kept, 1 dropped. `topic pr-extras` (A18); `topic release-evidence` (A25)
- `test_launch_modes`: 12 kept, 4 dropped. `topic batch-close-stopped` (C3); `topic board-lines` (C22); `topic board-restart` (C22); `topic sync-offer` (B19); `card chief-of-staff.md` (P2, A15/D13, C21, P5/A5/D5/D6, P7/C16/D21, C9, D14, P10, B19, C22, D17, C2, P12/D10, D12, C7, P17/D15, C3, C19, C20, D16, D19, D23, P18, C23); `card concepts.md#Starting an agent` (A10); `card sync-checkout.md` (B19); `floor 10` (P10, B19, C22); `floor 4` (a floor line, every one stays); `skill chantier` (B19); `skill chief-of-staff` (B19); `host name-env-holders` (B19)

Keys removed, none of their homes being named by the list: `test_triage_moves` (`topic session-shell` dropped); `test_board_running_lane` (`topic where-cr-goes` dropped).

## Blast radius

Grade: **1**. Documentation, tests and the eval kit only; no card, command or hook changes. A plain `git revert` restores the previous files.

## Autonomous decisions

- A home in `test_card_homes.py` is kept for a topic when a listed line names that page (or one of its numbered parts), for a card when a line quotes it, for a skill or host row when a line names it; every floor home stays.
- A rule held today only by pages planned for deletion is listed as held there, so the change that deletes them has to place it.

## Known gaps

- Some `to add` lines name no step of the cleanup plan, because no step brings them; each says so.
- One listed rule (a one-off permission for a session in a worktree stays in that batch) is held only by two topic pages planned for deletion; the change that deletes the first of them has to move it and update the line.
- No test guards `docs/protective-rules.md`, by choice, so it can drift.

<details>
<summary>Details</summary>

## Changes

- New `docs/protective-rules.md`.
- Removed the two inventory files and their two test modules.
- `test_card_homes.py`: homes trimmed, floor lines 2 and 8 pinned, a word-for-word floor test.
- `evals/kit/quiz.py`, `evals/kit/dry_run.py`, `evals/README.md`: a quiz case no longer names inventory row ids.

## Human decisions

- The inventory and its tests are dropped after one last reading of its open rows; a list of protective rules replaces it.
- A protective rule that belongs in the floor is put to the owner before the floor changes, and the change waits for the answer. None arose.
- A protective rule nothing holds, that one card line could hold, is restored here; one that needs code stays `to add`. None needed restoring.
- Allow rules are written by the user from a command made for their system; a refused push or rebase gets the exact command prepared. Both are listed as `to add`.

## Impacts

No visual change. Eval cases may name floor rules, scorecard `J` rows and `R-nnn` ids only.

## Test plan

- [ ] New or changed tests
- [ ] Local gates at `<sha7>`: `just check`, `just eval-dry-run`
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-515 cards-inventory-last-reading. Work files in the CR folder: `work/investigator/`, `work/coder/`.

</details>
