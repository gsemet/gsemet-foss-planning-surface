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

<!-- TO COMPLETE before the first post: paste from work/coder/deliverables.md, line 61 to its end (the other 58 rows and the HOMES lists). Check the quoted CLI span of FM-B047 for internal wording. -->

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
