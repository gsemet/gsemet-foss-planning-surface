# Delete the dead help pages of the Foreman, Driver and host side

## Goal

The owner wants the help pages that no longer earn their place gone (answer 3: delete all 65
pages now, in small CRs; this CR takes the Foreman, Driver, worker and host side). A deleted
page's protective rule is never lost: before a page goes, this CR names where each of its
protective statements lives afterwards, and adds the missing home in its smallest form. A host
fact leaves the topic pages for a host row (`chantier host <capability>`); no sentence that names
a host or a forge tool moves into a card (answer 5: topic cards are agnostic of the host and the
forge, save exceptions; the one word kept is PR).

The request names 32 pages. This CR deletes 29 of them. Three Copilot readings stay, left for a
later step: `host-claude-only.md`, `host-compact-copilot.md` and `host-sessions-copilot.md`. Each
is the Copilot reading of a kept topic's host map. Removing one would need new CLI behaviour (a
host map that names one host, in `help`), and the request says to keep such a rule in its page
for a later step (section 3).

The work starts at the base the stack gives it, after `cards-inventory-last-reading`
(`depends.json`), which removes `docs/proofs/cards-inventory*` and `test_cards_inventory.py`,
trims `test_card_homes.py` and adds `docs/protective-rules.md`. Every file and line named below
is read again at that base before it is edited.

## What changes

All paths are under `skills/chantier/references/` unless they start with `docs/`, `hooks/` or
`skills/chantier/scripts/`.

### 1. The 29 pages deleted

From `topics/`:

- Host (17): `host-allow-extra.md`, `host-allow-not-add.md`, `host-allow-rules.md`,
  `host-allow-rules-copilot.md`, `host-auto-mode.md`, `host-auto-mode-steering.md`,
  `host-auto-mode-trials.md`, `host-configuration.md`, `host-configuration-copilot.md`,
  `host-for-you.md`, `host-for-you-sessions.md`, `host-foreman-worktree.md`,
  `host-reuse-foreman.md`, `host-sessions-more.md`, `host-surfaces.md`, `host-write-guard.md`,
  `host-write-guard-shell.md`.
- Stack: `merge-stack-gitlab.md`, `stack-run.md`.
- Release: `release-thread.md`.
- Direct mode: `direct-mode-p1.md`, `direct-mode-p3.md`, `direct-mode-epoch-p2.md`.
- Workers: `verifier-images.md`, `worker-shell.md`.
- A Driver on its CR: `checkpoints.md`, `cr-proof.md`, `matrix.md`, `pr-gitlab.md`.

### 2. `topics.json`

- Topics removed whole, because every reading is deleted (22): `worker-shell`,
  `verifier-images`, `checkpoints`, `cr-proof`, `matrix`, `pr-gitlab`, `merge-stack-gitlab`,
  `host-configuration`, `host-allow-rules`, `host-allow-extra`, `host-allow-not-add`,
  `host-auto-mode`, `host-auto-mode-steering`, `host-auto-mode-trials`, `host-write-guard`,
  `host-write-guard-shell`, `host-sessions-more`, `host-surfaces`, `host-foreman-worktree`,
  `host-reuse-foreman`, `host-for-you`, `host-for-you-sessions`.
- Topics kept, a reading removed: `pr-extras` (loses `topics/pr-gitlab.md`), `cr-ship` (loses
  `topics/cr-proof.md`), `release-evidence` (loses `topics/release-thread.md`), `ready-to-merge`
  (loses `topics/merge-stack-gitlab.md`), `stack-run` (loses `topics/stack-run.md`, keeps
  `stack-asks`, `stack-ends`, `stack-drop`), `direct` (loses `direct-mode-p1`, `-p3`,
  `direct-mode-epoch-p2`), `direct-mode` (loses `-p1`, `-p3`), `direct-mode-epoch` (loses `-p2`).
- The host maps of the kept topics are unchanged. Each keeps its two keys
  (`host-allow-broad`, `host-allow-add`, `host-allow-add-lines`, `host-refused`, `host-remote`,
  `host-subagent-signs`, `host-auto-fix`, `host-turn-end`, `host-driver-silence`, `host-compact`,
  `host-sessions`, `host-heartbeat`).
- `session-shell` gains the seven worker roles of `worker-shell`: `coder`, `conflict-resolver`,
  `debugger`, `investigator`, `verifier`, `demo-explorer`, `inspector`. Its trigger becomes:
  `a shell call that chains, assigns, waits, backgrounds or changes folder; a file write; a text
  for the forge`.
- `pr-extras` gains the role `verifier`, because it reads `topics/pr-images.md`, the images page
  for all roles.

### 3. Three Copilot readings kept for a later step

`help` has no change. `skills/chantier/scripts/cli/src/chantier/commands/help.py` still needs each
host map to name `claude` and `copilot`, so three pages stay, unedited, with their map entries:

- `topics/host-claude-only.md`: the Copilot reading of nine kept topics (`host-allow-broad`,
  `host-allow-add`, `host-allow-add-lines`, `host-refused`, `host-remote`,
  `host-subagent-signs`, `host-auto-fix`, `host-turn-end`, `host-driver-silence`). Its rule stays
  where it is: on Copilot, tell the user nothing of a Claude-only subject as a fact.
- `topics/host-compact-copilot.md`: the Copilot reading of `host-compact`.
- `topics/host-sessions-copilot.md`: the Copilot reading of `host-sessions`.

All three are left for the later step that brings a host map naming one host into `help`. The
PR's description names them under that heading.

### 4. New host rows

Three capabilities are added to both `hosts/claude-code.json` and `hosts/copilot.json`, at the
same place in both (after `surface-session-writes`). Each means is at most 160 characters, each
row has 2 to 4 means, and no means uses a history word. These are the rules of
`test_host_rows.py`.

- `allow-rules`, "How an allow rule matches", roles `chief-of-staff`. Claude Code: the host's
  documented matching, with a link to the permissions page the deleted page cited. The
  recommended rules, and why, are in `references/hosts/claude-code.md`, "Allow rules", which P10
  checks. Copilot: no allow rule is recorded; recommend none.
- `auto-mode`, "A command in auto mode", roles `foreman`, `chief-of-staff`, `cr-driver`,
  `stack-driver`, `release-driver`. Claude Code: one command per call (a chain, a loop or a
  script matches no rule and is judged alone). A refusal is reported with its exact text, the
  classifier's label included, and a refused force push climbs `help refused-push`. Copilot: none
  recorded.
- `windows-powershell-args`, "A forge argument on Windows PowerShell 5.1", roles
  `chief-of-staff`, `cr-driver`, `stack-driver`, `release-driver`. Claude Code: a forge CLI
  argument with spaces or double quotes (a `--jq` expression) can arrive split (`accepts 1
  arg(s), received 3`). Print `--json <fields>` alone and read it, or write the argument with no
  space and no double quote. Copilot: the same means.

Marks. Every new row on both hosts is `untested`. On Claude Code, `docs/proofs/claude-code.md`
holds no trial for these three rows: "Allow rules" and "Auto mode" mark their lines
**documented** or **unproved**, a mark the rows do not carry (`test_host_rows.py` admits only
`proved` and `untested`), and "Windows PowerShell 5.1" records no proof. The steering session's
push "proved by use" in "Auto mode" proves the route of `help refused-push-chief`, not this row's
means. On Copilot every row is `untested` (`test_every_copilot_row_is_untested`).

Two lines join the existing `start-foreman` row of `claude-code.json`. They come from
`host-reuse-foreman.md`. First, a stopped last Foreman may be reused at epoch 1, after the user
is told that its old context has a cost and `/compact` (never `/clear`) is recommended first.
Second, never tell the user that a message wakes a closed session. The row goes from 2 means to
4. Its mark stays `untested`.

Each new capability gets a `## <capability>` heading in `docs/proofs/claude-code.md` and
`docs/proofs/copilot.md`, in the rows' order, before the `## Other: ` headings. Each heading has a
`Mark: untested` line and a `Card row: <name>` line, like the headings already there. The body
points to the trial history that already exists:

- In `claude-code.md`: `### Allow rules`, `### Auto mode` and `### Windows PowerShell 5.1`, under
  `## Other: Configuration`.
- In `copilot.md`: "No trial recorded on this host".

`KNOWN` in `skills/chantier/scripts/cli/tests/test_host_rows.py` goes from 50 to 53. No
`## Other: ` section is removed.

### 5. Protective statements moved

Each line gives the deleted page, its protective statement and its home afterwards. A home marked
"exists" is already there at the base and is not edited. A home marked "dropped" is an explicit
drop under card-cleanup-Q1, with its reason.

| Page | Statement | Home afterwards |
| --- | --- | --- |
| worker-shell | One command per call; no leading assignment; `$CHANTIER` in full, never in a shell variable; no `cd` into a CR folder; read before overwrite; UTF-8 no BOM | exists: `topics/session-shell-p1.md`, `-p2.md` (topic `session-shell`, now told to the workers) |
| worker-shell | A worker runs no `sleep` and no background shell | new line in `topics/session-shell-p1.md`: "A worker runs no `sleep` and no background task." |
| worker-shell | A file that already has a BOM keeps it: add none, strip none | added to `session-shell-p2.md`'s UTF-8 line |
| worker-shell | A raw log goes in a `*.log` file or `work/gates/`, never in a file published with the CR | new line in `session-shell-p2.md` (the Driver's copy in `topics/cr-prompt.md` exists) |
| worker-shell | A `$CHANTIER` that cannot run is a stop (floor 4): end the turn with its error as text | new line in `session-shell-p1.md`, same words (floor line 4 exists in every brief) |
| worker-shell | A skill or tool the role needs but lacks is not a stop: say so and work without it, never by another means | exists: `concepts.md` ("works without it, never without `$CHANTIER`") |
| worker-shell | Notes in `<work folder>/<role>/`; English; blocked: stop and say why | exists: each worker card's "You own" paragraph and reply template; the brief's language rule |
| verifier-images | The image and video rules of a Verifier | exists: `topics/pr-images.md`, same definitions (topic `pr-extras`, now told to `verifier`) |
| checkpoints | The commit message rule | exists: `topics/cr-ship.md` line "Commits:" |
| checkpoints | Once the branch is pushed, or when the checkpoint is not the head, it stays: never a rewrite for a message alone | replaces "Folding: `help checkpoints`" in `topics/cr-ship.md` |
| cr-proof | The `verifier` runs at the pushed head, given the plan, and the previous `verify.md` after the first | replaces "Next: `help cr-proof`" in `topics/cr-ship.md` (section 6) |
| cr-proof | `NOT VERIFIED` is a round | the same new `cr-ship.md` line |
| cr-proof | The Verifier's reply format; `verify.md`'s `Head:`; each claim with its SHA, command and output | exists: `verifier.md` (reply template, `verify.md` paragraph, `verdict` paragraph) |
| cr-proof | A gap left goes to Known gaps of `pr-body.md` first; evidence in Deliverables | exists: `cr-driver.md`, `pr-template.md` |
| cr-proof | A CR with a PR sent back turns its PR to draft first | new line in `topics/retake.md`, worded with no forge command |
| matrix | A matrix in the evidence plan when the CR depends on the host or a default; one checklist line per cell; the Inspector's prompt carries the whole matrix | replaces "`help matrix`" in `topics/cr-rounds.md` |
| matrix | The matrix probe before the first push (`phase <cr> verifier matrix probe`, the check of its reply, the `matrix probe <VERIFIED\|NOT VERIFIED> at <sha7>` note; `NOT VERIFIED` is a round) | replaces "Then the matrix probe (`help matrix`)" in `topics/cr-ship.md`, compact; the Verifier's side exists in `topics/verifier-delta-matrix.md` |
| matrix | Later verifiers get the last `matrix-r<n>.md` as the previous judgment, with the move | the same `cr-ship.md` line ends with it; the Verifier's side exists in `topics/verifier-delta-matrix.md` ("given the previous `verify.md` (or a `matrix-r<n>.md` …)") |
| matrix | A CR on the board's write paths passes the scratch rule in each Coder's and Verifier's brief | new line in `topics/cr-rounds.md`; the rules themselves exist in `coder.md` and `verifier.md` "Never" |
| pr-gitlab | (no protective statement: three unproved lines) | dropped: nothing protective; `forges/gitlab.md` names the tool |
| merge-stack-gitlab | An MR stack merges one MR at a time from the bottom, never "in one action from that MR"; an MR on a merge train or set to auto-merge is recorded only once the forge reads it merged | new line in `forges/gitlab.md`, marked **unproved** as on the page |
| merge-stack-gitlab | A middle MR merged (a fold): `order merged <k>` at once with `order note <k-1> --note "folded: <k> into <k-1>"`; tell the Foreman in the same message; tell the user that CR k's change now rides in CR k-1's PR | replaces "(`help merge-stack-gitlab`)" in `topics/merge-recorded.md`, written out with no forge name (section 6) |
| stack-run | Pass the `brief:` output of `take stack` unchanged, then `agents set` | exists: `foreman.md`, "Starting Drivers"; `topics/stack-ends.md` |
| release-thread | No agent posts the announcement thread; it is a draft for the user | exists: `release-driver.md` Never ("post the announcement thread"); `topics/release-notes.md` places the thread in the version PR's body |
| direct-mode-p1 | `take --reclaim` of a live lease only on the user's word; escalation; titles | exists: `foreman.md` Never; `help lease`, `help escalation`, `help titles` |
| direct-mode-p3 | Nothing is sent to yourself; an ask is recorded with `asks` and told at once; a refused push is yours (`help refused-push-chief`); `close` is the user's word | the ask line is added to `chief-of-staff.md`'s Direct mode paragraph in its smallest form; the rest exists there and in "Asks first" |
| direct-mode-epoch-p2 | Write a CR's `01-intent.md`, `02-answers.md`, `03-change-spec.md` and `work/specifying` with the Write or Edit tool, never a shell command: the CLI recognises grill work only by that write | new line in `topics/session-shell-p2.md`, next to the forge-text line (topic `session-shell`: `chief-of-staff`, `foreman`, `griller`, `spec-writer`, `spec-critic`) |
| direct-mode-epoch-p2 | The rest: how the cost lines price the steering session | dropped: an explanation, not a rule; `cost`'s own output says it |
| host-configuration | The PowerShell 5.1 split argument | new row `windows-powershell-args` |
| host-configuration | Chantier writes no other setting of the user's | exists: `chief-of-staff.md`, "Asks first" |
| host-allow-rules, host-allow-rules-copilot | How a rule matches; none on Copilot | new row `allow-rules` |
| host-allow-extra | Release and fix rules only when the user grants them | exists: `hosts/claude-code.md` |
| host-allow-extra | `Edit(<folder holding the repository and its worktrees>/**)`: it lets agents edit the CR worktrees next to the repository, at the risk of every file below that folder (the path is the user's); P10 does not check it | new sentence in `hosts/claude-code.md`, after the paragraph that closes "Capabilities and their commands" (a host reference, which may name the host's tools) |
| host-allow-extra | `mcp__ccd_pr__set_monitor`: no card uses it, to arm or disarm; its risk is a session that arms Auto-fix on a PR; P10 does not check it; unproved | the same new `hosts/claude-code.md` paragraph |
| host-allow-not-add | (P10 does not propose those rules) | dropped: P10's own list says it |
| host-auto-mode | One command per call; a refusal reported with its exact text | new row `auto-mode` |
| host-auto-mode-steering | The first-turn strong warning | exists: `topics/allow-rules-more-p1.md` |
| host-auto-mode-trials | (trial lists) | dropped from the cards; the history stays in `docs/proofs/claude-code.md` |
| host-configuration-copilot, host-sessions-more | The message limit | exists: `message-limit` rows |
| host-foreman-worktree | The Foreman's worktree check and its ask | exists: `foreman.md`, Start |
| host-reuse-foreman | Never say a message wakes a closed session; `/compact`, never `/clear` | `start-foreman` row (section 4) |
| host-for-you, host-for-you-sessions | A step that is the user's is given as one block: where, do, paste (complete, no placeholder), what you should see, cost first; a path the host does not mark proved is said untested | new line in `chief-of-staff.md`, with no host name (section 6); the Never line "as fact what the host marks unproved" exists |
| host-surfaces | (option matrix, unproved) | dropped: unproved options, nothing protective |
| host-write-guard, host-write-guard-shell | Write only where `writes:` allows | exists: the guard's own refusal text (`hooks/register.tsx`), `write-guard` rows, `coder.md` Never |
| host-claude-only, host-compact-copilot, host-sessions-copilot | (pages kept) | not deleted (section 3) |

`docs/protective-rules.md` (added by `cards-inventory-last-reading`): each line that names one of
the 29 deleted pages as a rule's home is updated, in this PR, to the home this table gives. A
line whose rule this table does not place is a stop for the Chief of Staff, not an edit.

The PR's description carries this table, in its Deliverables or in a section of its own, so a
reviewer sees each statement's home.

### 6. Pointers fixed and lines added

Every `help <name>` or link to a removed topic or deleted file is repointed or removed:

- Worker cards' "Rare cases": in `coder.md`, `conflict-resolver.md`, `debugger.md`,
  `demo-explorer.md`, `investigator.md` and `inspector.md`, `help worker-shell` becomes `help
  session-shell`. In `verifier.md` line 32, `verifier-images` becomes `pr-extras` (images) and
  `worker-shell` becomes `session-shell`. In `review-step.md` line 5, the text becomes "Shell
  rules: `$CHANTIER help session-shell`".
- Every parenthesis next to `session-shell` in a card's "Rare cases" reads the topic's new
  trigger: `(a shell call that chains, assigns, waits, backgrounds or changes folder; a file
  write; a text for the forge)`. This covers the three Driver cards (`cr-driver.md`,
  `release-driver.md`, `stack-driver.md`), the six worker cards above, `verifier.md`,
  `qa-driver.md` and `spec-writer.md`. The lead-ins that are not a parenthesis keep their words:
  `foreman.md`, `griller-skill.md`, `retro-critic.md`, `spec-critic.md`, and `review-step.md`
  (which has no parenthesis).
- `topics/session-shell-p1.md`'s first line names the workers too: "a Driver, a steering
  session, a worker, a Griller and a specification or retro agent".
- `topics/session-shell-p2.md` gains the grill-files line of section 5: "A CR's `01-intent.md`,
  `02-answers.md`, `03-change-spec.md` and `work/specifying` are written with the Write or Edit
  tool, never by a shell command: the CLI recognises grill work only by that write."
- Driver cards: `cr-driver.md` drops `checkpoints` and `matrix` from its rare cases;
  `release-driver.md` and `stack-driver.md` drop `checkpoints`.
- `topics/cr-ship.md`:
  - The `checkpoints` and `matrix` pointers are replaced as section 5 says. The matrix line ends
    with "later verifiers get the last `matrix-r<n>.md` as the previous judgment".
  - "GitLab: `help pr-gitlab`" is removed.
  - "Next: `help cr-proof`" becomes "Next: the `verifier` at the pushed head, given the plan, and
    the previous `verify.md` after the first; `NOT VERIFIED` is a round. Before the hand-back:
    `help closing`, `help handback-other`."
- `topics/cr-rounds.md` line 3: as section 5 says.
- `topics/merge-recorded.md` line 7 becomes, with no forge name: "A fold (`forge-stack show`
  prints `folded into <cr below>`) is recorded at once, a rule that keeps its precedence over the
  forge check: `order merged <k>` with `order note <k-1> --note "folded: <k> into <k-1>"`; tell
  the Foreman in the same message, and tell the user that CR k's change now rides in CR k-1's
  PR."
- `forges/gitlab.md` gains one line, marked **unproved**: an MR stack merges one MR at a time
  from the bottom up to the commit named, never "in one action from that MR"; an MR on a merge
  train or set to auto-merge is recorded only once `glab` reads it merged.
- `topics/retake.md` gains the line "A CR whose PR was sent back: turn the PR to draft first."
- `chief-of-staff.md` gains two lines, in their smallest form and with no host name:
  - In the Direct mode paragraph: an ask is recorded with `$CHANTIER asks "<text>"` and told at
    once; nothing is sent to yourself.
  - The user's-step line of section 5 (`host-for-you`). Its exact place among the user-facing
    lines is the Coder's.
- `hosts/claude-code.md`:
  - Line 4: `help host-allow-rules` is removed from the list, and the row is named instead
    (`$CHANTIER host allow-rules`).
  - The new paragraph of section 5 holds the `Edit(…/**)` and `mcp__ccd_pr__set_monitor` notes.
- `topics/verifier-before-after.md`, `topics/verifier-description.md`,
  `topics/verifier-scratch.md`: `help verifier-images` becomes `help pr-extras`.
- `topics/host-allow-broad.md` line 19 and `topics/host-refused.md` line 19: the sentences that
  name `host-allow-extra` and `host-allow-not-add` are removed. `topics/host-sessions.md` line
  16: "(`help host-for-you`)" is removed.
- `topics/stack-deliver.md` line 4 keeps `help stack-run`, because the topic stays.
- CLI source: in `skills/chantier/scripts/cli/src/chantier/commands/permissions.py` line 28, the
  comment "(`help host-allow-not-add`)" is removed. The test
  `test_every_topic_a_line_names_exists` scans comments too. This is the only change under `src/`.
- `docs/incidents.md`, "Where it lives":
  - Line 34 (`host-configuration`) becomes `chantier host windows-powershell-args`.
  - Lines 42 and 97 (`host-auto-mode`) become `chantier host auto-mode`.
  - Line 72 (`worker-shell`) becomes `chantier help session-shell`, linked to
    `topics/session-shell-p1.md`.
- Any other pointer that the evidence's grep finds at the base is fixed the same way.

### 7. Tests (`skills/chantier/scripts/cli/tests/`)

Each test reads the shipped file at the head under test, never a copy.

- `test_cli_stop.py`: the `worker-shell.md` needle moves to `topics/session-shell-p1.md`, with
  the same words.
- `test_launch_modes.py` line 134: the loop checks `session-shell-p1.md` only.
- `test_triage_moves.py`, `test_every_role_is_told_to_keep_its_shell_out_of_cr_folders`: `told`
  is `session-shell`'s roles alone, and `untold` stays `{"board-griller"}`. The "into a CR folder"
  check reads `session-shell-p2.md` only.
- `test_help_topics.py`: the line 115 assertion `"# Commits and checkpoints"` is removed. It is
  vacuous once the page is gone. No other change: the host maps keep two keys.
- `test_card_homes.py`: the names `matrix`, `stack-run` (as a page), `checkpoints` and
  `worker-shell` left in `HOMES` at the base point to the new homes of section 5. Where the rule
  now lives in a file the test already checks, they are removed.
- `test_host_rows.py`: `KNOWN` becomes 53 (section 4).
- `test_plugin_files.py` passes unchanged. No host tool or forge tool name moves into a card that
  does not start with `host-`. The new `forges/gitlab.md` line may name `glab` (a forge note) and
  the new `hosts/claude-code.md` paragraph may name the host's tools.

## Decisions from 02-answers.md

1. "ouvre un batch et lance ces 7 CR" (2026-11-27) is read as "grilled enough". The owner's
   confirmation is still recorded as owed (question 1).
2. The batch is a stack. This CR sits in it after `cards-inventory-last-reading`, and only the
   top CR of the stack owes the local Windows scenario run.
3. card-cleanup-Q1 A: all 65 pages go now, and each CR says, before it deletes, where every
   protective rule goes (section 5). Three of this CR's 32 stay for a later step, because their
   removal needs new CLI behaviour, as the request provides (section 3).
4. card-cleanup-Q5 A: steps 1 to 3 ship with a new version, in small CRs. The other project
   reads the cards live, so this CR lands within that version's stack and adds no step of its
   own.
5. Topic cards are agnostic of the host and the forge, save exceptions; the one word kept is PR.
   Host facts go to host rows or `hosts/claude-code.md` (sections 4 and 5), and forge facts go to
   `forges/gitlab.md`. Every new topic-card line is written with no host or forge tool name.

## Out of scope

- The Chief of Staff side pages (`cards-delete-pages-chief`), the aggregate topic names
  (`cards-delete-aggregate-topics`) and joining the `-pN` pages (`cards-one-page-per-theme`). The
  `host-for-you` line in `chief-of-staff.md` is this CR's; `cards-delete-pages-chief` is told so.
- Any change to `help.py`, and a host map that names one host. `host-claude-only.md`,
  `host-compact-copilot.md` and `host-sessions-copilot.md` stay for that later step.
- `host-heartbeat-copilot.md` and every page not in section 1.
- The cost code's Write-tool coupling named in `direct-mode-epoch-p2.md`. The rule it implies
  moves to `session-shell-p2.md`, and the code is unchanged.
- Rewording the kept pages beyond the lines that sections 5 and 6 name.
- The `## Other: ` trial sections of `docs/proofs/*.md`.

## Evidence

- The diff holds only: deletions, pointer fixes, the moved and added lines of sections 5 and 6,
  the three host rows and the two `start-foreman` lines with their proof headings, the
  `permissions.py` comment, and the tests.
- `$CHANTIER help` lists no removed topic, and `$CHANTIER help <name>` refuses with `no topic
  <name>` for each of the 22 removed names.
- `$CHANTIER help host-allow-broad --host copilot` still prints `host-claude-only.md`.
- `$CHANTIER help session-shell` names the workers and the new trigger.
- `$CHANTIER help --for coder` lists `session-shell` with that trigger.
- `$CHANTIER host allow-rules`, `auto-mode` and `windows-powershell-args` print their rows,
  `(untested)` and with the untested sentence, on both hosts.
- A repository grep for each of the 29 page names (`help <name>`, `topics/<name>.md`) finds
  none, outside the `docs/proofs/` trial history and the git folder's old briefs.
- `docs/protective-rules.md` names none of the 29 pages as a home.
- A grep of the new topic-card lines (`session-shell-p1.md`, `session-shell-p2.md`,
  `cr-ship.md`, `cr-rounds.md`, `merge-recorded.md`, `retake.md`, `chief-of-staff.md`) finds no
  `gh`, `glab`, `GitLab`, `GitHub`, `Claude` or `Copilot` in them.
- `just check` passes. `just eval-dry-run` passes, because `permissions.py` under the CLI's
  `src/` changes.
- The long gate `just scenario (ubuntu-latest)` is green at the PR's head (a CLI and cards
  change).
- The PR's description carries the table of section 5 and names the three kept Copilot pages as
  left for the later step.

## Questions for the Chief of Staff

1. Answer 1 reads "ouvre un batch et lance ces 7 CR" as "grilled enough": does the owner confirm?
