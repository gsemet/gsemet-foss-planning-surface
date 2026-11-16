# Commit map: v0.8.0..HEAD, every feat: and fix: to its place in the notes

N = 95 non-merge commits; feat:/fix: listed below.

| Commit | Subject | Place in the notes |
| --- | --- | --- |
| b802015 | feat: fast-forward a clean main checkout after each merge the steering session records | Smaller changes: A clean main checkout follows each merge |
| b1e5879 | fix(evals): let the audit pass a Verifier's detached worktree and a direct batch's report refresh | All fixes: Evals |
| a2bd6ab | feat(board): add a Refresh button to every view and show when the pane last checked and its period | Highlight "Refresh the board, and open it from your phone" |
| d762044 | feat: pick the Chief of Staff's batch mode from the surface, rework the README and document the CR board | Highlight "Start a batch in the mode your screen can run" |
| e799950 | fix(cost): count a direct batch's steering turns as steering, not grill, unless they write a CR's files or start a spec-writer | All fixes: Costs |
| 5d7305d | fix(cli): a stop of the long gate is a separate marker, never lost and never a failure | All fixes: The long gate |
| b6e3d31 | feat(cli): gate --stop stops a Driver's own long gate; cancel needs --epoch | Smaller changes: A Driver stops its own long gate |
| 55164d9 | fix(evals): count a release go answered merge as an action that waited for the user | All fixes: Evals |
| eb31c07 | feat(release): a release CR asked in a batch is a normal CR of that batch, on top of its stack | Highlight "The release arrives with the batch it ships" |
| 27c1539 | fix(ci): warm the uv cache before the eval dry run so its offline lock finds the registry listings | All fixes: Evals |
| 6732ecd | fix(evals): apply the dry-run patch from an LF copy so a Windows checkout does not break git apply | All fixes: Evals |
| a535fbb | feat(evals): an end-to-end dry run of the campaign path as evidence for eval-kit changes | Smaller changes: Evals you can replay |
| 3dc912f | feat(cli): price claude-fable-5-2 in the built-in table | Smaller changes: Honest costs (fable price) |
| 54cf7b7 | fix(cards): PowerShell 5.1 quoting of gh --jq, and the exact list of commands that take --epoch | All fixes: Cards |
| d6271d4 | fix(evals): audit counts the release PRs, reset ignores refs/pull, sandbox merge command, allow rules, uv.lock in release CRs, docs | All fixes: Evals |
| d72df44 | feat(evals): reproducible eval campaigns on the sandbox (runbooks, docs, audit fix) | Smaller changes: Evals you can replay |
| c514ea8 | feat(evals): add the frozen shelf CRs and their hidden judge tests | Smaller changes: Evals you can replay |
| 59c8a58 | feat(evals): build the shelf eval sandbox project, its deterministic base commit and its reset | Smaller changes: Evals you can replay |
| be32d09 | fix(cards): scope the no-edit rule to CR and stack Drivers, keep body-only fixes, move the BOM rule to concepts | All fixes: Cards |
| 4a97ee4 | fix(cards): a Driver stages the round's files by name, never git add -A | All fixes: Cards |
| ab42a93 | fix(cards): re-read rule files after a compaction, review fixes go to a coder, final body verified, heartbeat stop cancels the wake | All fixes: Cards |
| c37c19e | fix(cards): files a role writes, the PR body included, are UTF-8 without a byte-order mark | All fixes: Byte-order marks |
| abea291 | fix(cards): a Foreman reads the rules each batch; every worker prompt carries the required lines | All fixes: Cards |
| 6b05434 | fix: the scenario and the Foreman card clear the recorded agent before a take | All fixes: The scenario |
| 70b064a | feat: a ready CR sent back to its Driver can be handed back again | Smaller changes: Batch modes (hand back again) |
| 25ca568 | fix: the CLI reads a planning folder's files through a leading byte-order mark | All fixes: Byte-order marks |
| fb775a2 | fix(evals): the audit reads shell writes, CLI calls and throwaway repos more strictly | All fixes: Evals |
| 28b8f66 | fix(evals): the audit reads CLI calls, git verbs and shell writes as the shell runs them | All fixes: Evals |
| 4d50cf5 | fix(evals): the audit reads a PR body past its BOM and skips throwaway repos in J3 | All fixes: Evals |
| 012e88e | fix(evals): the audit checks only the agents of the batch it audits | All fixes: Evals |
| 9137864 | fix: the heartbeat says something true in direct mode: wake gap, recorded stop, one epoch rule | All fixes: The heartbeat |
| 74256ab | feat: the steering session sees a dead Driver by per-CR activity lines and restarts it from the recorded state | Smaller changes: Dead Drivers |
| cd1a89a | feat: the gate proof binds to one full commit, the budget refuses a round, and restore brings a trashed CR back to the inbox | Smaller changes: Proof you can trust / Honest costs (budget refuses a round); restore not named |
| 51503c6 | fix: the scenario's remote_board step writes a priced transcript before status --refresh | All fixes: The scenario |
| 4b90993 | feat: chantier board, a read-only web view of the planning folder for the user in remote | Highlight "Refresh the board, and open it from your phone" |
| d69eb88 | feat: calls of a model with no price are counted and named, the cost is a floor, prices come from chantier.yaml, and the cost report has one fixed skeleton | Smaller changes: Honest costs |
| 06c9ce6 | feat: the eval campaigns are redesigned: real-foreman, real-direct, claude-planted and copilot, one scorecard and an audit on every campaign | Smaller changes: Evals you can replay |
| 7010fa6 | feat: close keeps the batch's retro in the archive of its last merged CR | Smaller changes: Retros |
| fe9852d | feat: the worker write guard reads a writes: line, starts the agent in its first folder, and passes what it cannot judge with a board note; just mod runs the mod's checks | Smaller changes: A write guard for workers |
| 04ed67b | feat: report back on tracker issues (issue line, closing line, grill comment, Released in) | Smaller changes: Tracker issues |
| 3e4a129 | feat: Sonnet by default for the Foreman and the Drivers, escalation on named trouble, a 300K auto-compact window | Smaller changes: Sonnet by default |
| 24cc7eb | fix: take the broken worker write guard off main | All fixes: The write guard |
| 1e99343 | fix: the write guard covers worker roles only, never a Driver | All fixes: The write guard |
| 204d478 | feat: handback ready needs a passed long gate and a VERIFIED verdict, workers cannot write outside their worktree, and the batch-09 retro's CLI fixes | Smaller changes: Proof you can trust |
| fde3da8 | fix: a missing gate pass goes back to the Driver, and the new card lines are wrapped | All fixes: Cards |
| 1b1c2e0 | feat: the Chief of Staff judges a refused force push and runs it without asking the user | Smaller changes: A force push that was refused |
| 5249695 | fix: the shape shown covers series, and the default shape is parallel | All fixes: The batch shape |
| 2f25949 | feat: a retro at each pause, the Chief of Staff's cost split in grill and steering, and the batch's steering and shape shown | Smaller changes: Retros (cost split not named) |
| b3b2da4 | fix: the playbook scenario follows the batch modes | All fixes: The scenario |
| f6557ef | feat: an optional chantier.yaml playbook, parsed and resolved by the CLI | Smaller changes: chantier.yaml |
| 997b9db | feat: each proof names the SHA it judged, unproven claims are marked, an unobserved cost is unknown, never 0 | Smaller changes: Proof you can trust |
| 7ad33cb | feat: the Chief of Staff offers release auto and gives one contextual tip at four key moments | Smaller changes: Retros (release auto and tip) |
| 08b2f82 | fix: just tag refuses unless origin/main is the release commit, the full gh release command, no go for the user's merge, the UUID scan after an underscore | All fixes: The release tag |
| 7d58b96 | feat: a batch has three modes, parallel (default), series and stack | Smaller changes: Batch modes |
| 1540c75 | fix: the reload reads status-layout.md, renamed by CR-162 | All fixes: Cards |
| cf27483 | feat: the Chief of Staff keeps its rules through compaction, a reload by hand and by the mod, and options that fit where the user is | Smaller changes: Several sessions on one repository (rules through compaction) |
| de9ea80 | fix: the QA file is 04-result.md, and the guard's rule is recorded with its proof | All fixes: Cards |
| 5cedbbf | fix: the status card and the QA notes get names the host's write guard accepts, and the guard is recorded | All fixes: Cards |
| f21d493 | feat: several CRs can join a paused batch, the first take sets it running again | Smaller changes: Batch modes (join a paused batch) |
| fb8990b | feat: an external planning surface, a git repository of its own that holds the planning of several projects | Smaller changes: A planning folder of its own |
| fb737a8 | fix: the status command reads each CR's icon from the batch STATUS.md | All fixes: Status |
| 9f94f52 | feat: a /chantier:status command and a short report card, so a status keeps the approved shape | Smaller changes: A changes tree, version 2 (/chantier:status) |
| 57c195e | fix: the batch folder is 4-batch, one batch runs at a time | All fixes: Status |
| f85c4c6 | feat: the changes tree, version 2: 3-ready, 4-batches with three states, 5-archives, 6-trash | Smaller changes: A changes tree, version 2 |
| 1ceb402 | feat: the Verifier checks the PR description as posted, clean and consistent with the diff | Smaller changes: A Verifier reads the PR description |
| c2e6bb3 | fix: remove a stray byte order mark from commands.py | All fixes: Byte-order marks |
| 462e7e4 | feat: several sessions on one repository: one Chief of Staff, Grillers beside it, and a skill for each role | Smaller changes: Several sessions on one repository |
| 410e1a2 | feat: chantier recommends and checks the Claude Code configuration (allow rules, compaction, prerequisites) | Smaller changes: A configuration check |
| 419e7da | feat: the default PR description folds its details and shows the user's grill decisions | Smaller changes: A Verifier reads the PR description (default description) |
| a67c9e4 | feat(cli): forge-stack create and show make and check the native stack on GitHub | Smaller changes: One forge stack, merged in one go |
| ac3546c | feat(cards): a stack is one forge stack merged in one go, and every agent states the first line its prompt must start with | Smaller changes: One forge stack, merged in one go |

Total 71 feat:/fix: commits. Other commits (docs:, test:, wip:) are in For contributors or not named.

