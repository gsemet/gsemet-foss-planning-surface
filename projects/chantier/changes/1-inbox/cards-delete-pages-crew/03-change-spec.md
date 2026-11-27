# Delete the dead help pages of the Foreman, Driver and host side

## Goal

The owner wants the help pages that no longer earn their place gone (answer 3: delete all 65
pages now, in small CRs; this CR takes the 32 of the Foreman, Driver, worker and host side). A
deleted page's protective rule is never lost: before a page goes, this CR names where each of its
protective statements lives afterwards, and adds the missing home in its smallest form. A host
fact leaves the topic pages for a host row (`chantier host <capability>`); no sentence that names
a host or a forge tool moves into a card (answer 5: topic cards are agnostic of the host and the
forge, save exceptions; the one word kept is PR).

The work starts at the base the stack gives it, after `cards-inventory-last-reading`
(`depends.json`), which removes `docs/proofs/cards-inventory*` and `test_cards_inventory.py`,
trims `test_card_homes.py` and adds `docs/protective-rules.md`. Every file and line named below
is read again at that base before it is edited.

## What changes

All paths are under `skills/chantier/references/` unless they start with `docs/`, `hooks/` or
`skills/chantier/scripts/`.

### 1. The 32 pages deleted

From `topics/`:

- Host: `host-allow-extra.md`, `host-allow-not-add.md`, `host-allow-rules.md`,
  `host-allow-rules-copilot.md`, `host-auto-mode.md`, `host-auto-mode-steering.md`,
  `host-auto-mode-trials.md`, `host-claude-only.md`, `host-compact-copilot.md`,
  `host-configuration.md`, `host-configuration-copilot.md`, `host-for-you.md`,
  `host-for-you-sessions.md`, `host-foreman-worktree.md`, `host-reuse-foreman.md`,
  `host-sessions-copilot.md`, `host-sessions-more.md`, `host-surfaces.md`,
  `host-write-guard.md`, `host-write-guard-shell.md`.
- Stack: `merge-stack-gitlab.md`, `stack-run.md`.
- Release: `release-thread.md`.
- Direct mode: `direct-mode-p1.md`, `direct-mode-p3.md`, `direct-mode-epoch-p2.md`.
- Workers: `verifier-images.md`, `worker-shell.md`.
- A Driver on its CR: `checkpoints.md`, `cr-proof.md`, `matrix.md`, `pr-gitlab.md`.

### 2. `topics.json`

- Topics removed whole (every reading deleted): `worker-shell`, `verifier-images`,
  `checkpoints`, `cr-proof`, `matrix`, `pr-gitlab`, `merge-stack-gitlab`, `host-configuration`,
  `host-allow-rules`, `host-allow-extra`, `host-allow-not-add`, `host-auto-mode`,
  `host-auto-mode-steering`, `host-auto-mode-trials`, `host-write-guard`,
  `host-write-guard-shell`, `host-sessions-more`, `host-surfaces`, `host-foreman-worktree`,
  `host-reuse-foreman`, `host-for-you`, `host-for-you-sessions` (22).
- Topics kept, a reading removed: `pr-extras` (loses `topics/pr-gitlab.md`), `cr-ship` (loses
  `topics/cr-proof.md`), `release-evidence` (loses `topics/release-thread.md`), `ready-to-merge`
  (loses `topics/merge-stack-gitlab.md`), `stack-run` (loses `topics/stack-run.md`, keeps
  `stack-asks`, `stack-ends`, `stack-drop`), `direct` (loses `direct-mode-p1`, `-p3`,
  `direct-mode-epoch-p2`), `direct-mode` (loses `-p1`, `-p3`), `direct-mode-epoch` (loses `-p2`).
- Host maps whose Copilot reading was a deleted page become a one-host map `{"claude": …}`:
  `host-allow-broad`, `host-allow-add`, `host-allow-add-lines`, `host-refused`, `host-remote`,
  `host-subagent-signs`, `host-auto-fix`, `host-turn-end`, `host-driver-silence` (were
  `host-claude-only.md`), `host-compact` (was `host-compact-copilot.md`), `host-sessions` (was
  `host-sessions-copilot.md`). `host-heartbeat` keeps its two keys.
- `session-shell` gains the seven worker roles of `worker-shell`: `coder`, `conflict-resolver`,
  `debugger`, `investigator`, `verifier`, `demo-explorer`, `inspector`; its trigger names a file
  write too.
- `pr-extras` gains the role `verifier` (it reads `topics/pr-images.md`, the images page for all
  roles).

### 3. `help` and a one-host map (`skills/chantier/scripts/cli/src/chantier/commands/help.py`)

`host-claude-only.md` was the Copilot reading of eleven kept topics; with it gone, `_forms` would
refuse those maps (`a host map reading needs exactly ('claude', 'copilot')`). The change:

- `_forms` accepts a host map whose keys are a non-empty subset of `HOSTS`, each value a string;
  any other key still raises `_bad`. Its message becomes `a host map reading names hosts among
  ('claude', 'copilot')`.
- `_print_topic`, on a host the map does not name, prints in place of the reading one line:
  `--- no reading on <host>: nothing of this topic is recorded there; tell the user nothing of it
  as a fact (`$CHANTIER host` lists what is recorded) ---`. This line keeps
  `host-claude-only.md`'s protective statement in the CLI, where naming a host is allowed. The
  exact wording is the Coder's within that meaning.

### 4. New host rows

Three capabilities, added to both `hosts/claude-code.json` and `hosts/copilot.json`, in the same
place in both (after `surface-session-writes`). Each means is at most 160 characters, 2 to 4 per
row, with no history words (the rules of `test_host_rows.py`):

- `allow-rules`, "How an allow rule matches", roles `chief-of-staff`. Claude Code: the host's
  documented matching (link to the permissions page the deleted page cited); the recommended
  rules and why are `references/hosts/claude-code.md`, "Allow rules", which P10 checks. Copilot:
  no allow rule recorded; recommend none.
- `auto-mode`, "A command in auto mode", roles `foreman`, `chief-of-staff`, `cr-driver`,
  `stack-driver`, `release-driver`. Claude Code: one command per call (a chain, a loop or a script
  matches no rule and is judged alone); a refusal is reported with its exact text, the
  classifier's label included, and a refused force push climbs `help refused-push`. Copilot: none
  recorded.
- `windows-powershell-args`, "A forge argument on Windows PowerShell 5.1", roles
  `chief-of-staff`, `cr-driver`, `stack-driver`, `release-driver`. Claude Code: a forge CLI
  argument with spaces or double quotes (a `--jq` expression) can arrive split (`accepts 1
  arg(s), received 3`): print `--json <fields>` alone and read it, or write it with no space and
  no double quote. Copilot: the same means, its row marked untested like every Copilot row
  (see question 2).

Two lines join the existing `start-foreman` row of `claude-code.json` (from
`host-reuse-foreman.md`): a stopped last Foreman may be reused at epoch 1, after the user is told
its old context costs and `/compact` (never `/clear`) is recommended first; never tell the user a
message wakes a closed session. If the row's 4-means limit is hit, the Coder folds them into the
existing means.

Each new capability gets a `## <capability>` heading in `docs/proofs/claude-code.md` and
`docs/proofs/copilot.md`, in the rows' order, before the `## Other: ` headings. Its body points to
the trial history already there (`### Allow rules`, `### Auto mode`, `### Windows PowerShell 5.1`
under `## Other: Configuration` in `claude-code.md`; for Copilot: never tried). `KNOWN` in
`skills/chantier/scripts/cli/tests/test_host_rows.py` goes from 50 to 53. No `## Other: `
section is removed.

### 5. Protective statements moved

Each line: the deleted page, its protective statement, its home afterwards. A home marked
"exists" is already there at the base and is not edited.

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
| cr-proof | Verifier reply format, gaps to Known gaps first, evidence in Deliverables | exists: `verifier.md`, `cr-driver.md`, `pr-template.md` |
| cr-proof | A CR with a PR sent back turns its PR to draft first | new line in `topics/retake.md`, worded with no forge command |
| matrix | A matrix in the evidence plan when the CR depends on the host or a default; one checklist line per cell; the Inspector's prompt carries the whole matrix | replaces "`help matrix`" in `topics/cr-rounds.md` (see question 4) |
| matrix | The matrix probe before the first push (`phase <cr> verifier matrix probe`, the check of its reply, the `matrix probe <VERIFIED|NOT VERIFIED> at <sha7>` note, a failure is a round) | replaces "Then the matrix probe (`help matrix`)" in `topics/cr-ship.md`, compact; the Verifier's side exists in `topics/verifier-delta-matrix.md` |
| matrix | A CR on the board's write paths passes the scratch rule in each Coder's and Verifier's brief | new line in `topics/cr-rounds.md`; the rules themselves exist in `coder.md` and `verifier.md` "Never" |
| pr-gitlab | (no protective statement: three unproved lines) | none |
| merge-stack-gitlab | An MR stack merges one MR at a time from the bottom; an MR on a merge train or auto-merge is recorded only once the forge reads it merged | new line in `forges/gitlab.md` |
| merge-stack-gitlab | A middle MR merged: `order merged <k>` with `order note <k-1> --note "folded: <k> into <k-1>"` at once | replaces "(`help merge-stack-gitlab`)" in `topics/merge-recorded.md`, written out |
| stack-run | Pass the `brief:` output of `take stack` unchanged, then `agents set` | exists: `foreman.md`, "Starting Drivers"; `topics/stack-ends.md` |
| release-thread | No agent posts the announcement thread; it is a draft for the user | exists: `release-driver.md` Never ("post the announcement thread"); `topics/release-notes.md` places the thread in the version PR's body |
| direct-mode-p1 | `take --reclaim` of a live lease only on the user's word; escalation; titles | exists: `foreman.md` Never; `help lease`, `help escalation`, `help titles` |
| direct-mode-p3 | Nothing is sent to yourself; an ask is recorded with `asks` and told at once; a refused push is yours (`help refused-push-chief`); `close` is the user's word | the ask line is added to `chief-of-staff.md`'s Direct mode paragraph in its smallest form; the rest exists there and in "Asks first" |
| direct-mode-epoch-p2 | (no protective statement: a cost explanation) | none (see question 3) |
| host-configuration | The PowerShell 5.1 split argument | new row `windows-powershell-args` |
| host-configuration | Chantier writes no other setting of the user's | exists: `chief-of-staff.md`, "Asks first" |
| host-allow-rules, host-allow-rules-copilot | How a rule matches; none on Copilot | new row `allow-rules` |
| host-allow-extra | Release and fix rules only when the user grants them | exists: `hosts/claude-code.md` |
| host-allow-not-add | (P10 does not propose those rules) | none |
| host-auto-mode | One command per call; a refusal reported with its exact text | new row `auto-mode` |
| host-auto-mode-steering | The first-turn strong warning | exists: `topics/allow-rules-more-p1.md` |
| host-auto-mode-trials | (trial lists) | none; the history stays in `docs/proofs/claude-code.md` |
| host-claude-only | Tell the user nothing of a Claude-only subject as a fact on Copilot | the line `help` prints (section 3) |
| host-compact-copilot | Name no compacting command; the manual reload | exists: `compact` row of `copilot.json` |
| host-sessions-copilot | A refused start reported; "looks stopped"; lost Driver | exists: `start-foreman`, `list-sessions`, `subagent-stopped-outside` rows of `copilot.json` |
| host-configuration-copilot, host-sessions-more | The message limit | exists: `message-limit` rows |
| host-foreman-worktree | The Foreman's worktree check and its ask | exists: `foreman.md`, Start |
| host-reuse-foreman | Never say a message wakes a closed session; `/compact`, never `/clear` | `start-foreman` row (section 4) |
| host-for-you, host-for-you-sessions | A user step is said as where, do, paste, expect, and "I have not tested this path" | exists in part: `chief-of-staff.md` Never ("as fact what the host marks unproved"); see question 5 |
| host-surfaces | (option matrix, unproved) | none |
| host-write-guard, host-write-guard-shell | Write only where `writes:` allows | exists: the guard's own refusal text (`hooks/register.tsx`), `write-guard` rows, `coder.md` Never |

`docs/protective-rules.md` (added by `cards-inventory-last-reading`): each line that names one of
the 32 deleted pages as a rule's home is updated, in this PR, to the home this table gives. A
line whose rule this table drops (none expected) is a stop for the Chief of Staff, not an edit.

The PR's description carries this table (its Deliverables or a section of its own), so a reviewer
sees each statement's home.

### 6. Pointers fixed

Every `help <name>` or link to a removed topic or deleted file, repointed or removed:

- Worker cards' "Rare cases": `coder.md`, `conflict-resolver.md`, `debugger.md`,
  `demo-explorer.md`, `investigator.md`, `inspector.md`: `help worker-shell` becomes `help
  session-shell`. `verifier.md` line 32: `verifier-images` becomes `pr-extras` (images),
  `worker-shell` becomes `session-shell`. `review-step.md` line 5: "Shell rules: `$CHANTIER help
  session-shell`".
- `topics/session-shell-p1.md` first line names the workers too ("a Driver, a steering session,
  a worker, a Griller and a specification or retro agent").
- Driver cards: `cr-driver.md` drops `checkpoints` and `matrix` from its rare cases;
  `release-driver.md` and `stack-driver.md` drop `checkpoints`.
- `topics/cr-ship.md`: the four pointers of section 5 (`checkpoints`, `matrix`, `pr-gitlab`,
  `cr-proof`); "GitLab: `help pr-gitlab`" is removed; "Next: `help cr-proof`" becomes the steps
  `cr-proof` gave that exist elsewhere ("Next: the `verifier` at the pushed head; before the
  hand-back `help closing`, `help handback-other`").
- `topics/cr-rounds.md` line 3, `topics/merge-recorded.md` line 7: section 5.
- `topics/verifier-before-after.md`, `topics/verifier-description.md`,
  `topics/verifier-scratch.md`: `help verifier-images` becomes `help pr-extras`.
- `topics/host-allow-broad.md` line 19 and `topics/host-refused.md` line 19: the sentences naming
  `host-allow-extra` and `host-allow-not-add` are removed. `topics/host-sessions.md` line 16:
  "(`help host-for-you`)" is removed.
- `hosts/claude-code.md` line 4: `help host-allow-rules` removed from the list (the row
  `allow-rules` named instead: `$CHANTIER host allow-rules`).
- `topics/stack-deliver.md` line 4 keeps `help stack-run` (the topic stays).
- CLI source: `skills/chantier/scripts/cli/src/chantier/commands/permissions.py` line 28, the
  comment "(`help host-allow-not-add`)" is removed (the test `test_every_topic_a_line_names_exists`
  scans comments too).
- `docs/incidents.md` "Where it lives": line 34 (`host-configuration`) becomes `chantier host
  windows-powershell-args`; lines 42 and 97 (`host-auto-mode`) become `chantier host auto-mode`;
  line 72 (`worker-shell`) becomes `chantier help session-shell`, linked to
  `topics/session-shell-p1.md`.
- Any other pointer found at the base by the grep of the evidence is fixed the same way.

### 7. Tests (`skills/chantier/scripts/cli/tests/`)

Each test reads the shipped file at the head under test, never a copy.

- `test_cli_stop.py`: the `worker-shell.md` needle moves to `topics/session-shell-p1.md`, same
  words.
- `test_launch_modes.py` line 134: the loop checks `session-shell-p1.md` only.
- `test_triage_moves.py` `test_every_role_is_told_to_keep_its_shell_out_of_cr_folders`: `told`
  is `session-shell`'s roles alone; untold stays `{"board-griller"}`; the "into a CR folder" check
  reads `session-shell-p2.md` only.
- `test_help_topics.py`:
  - `test_every_topic_resolves_on_both_hosts`: a one-host map on a host it does not name is
    skipped for that host; every map names `claude`.
  - a prepared test beside `test_prepared_host_map_reading_is_resolved_per_host`: a map
    `{"claude": "a.md"}` loads, prints `a.md` on `claude`, and on `copilot` prints the "no reading
    on copilot" line and no file; a map with an unknown key still raises.
  - line 115's `"# Commits and checkpoints"` assertion is removed (vacuous once the page is gone).
- `test_card_homes.py`: the names `matrix`, `stack-run` (as a page), `checkpoints`,
  `worker-shell` left in `HOMES` at the base point to the new homes of section 5, or are removed
  where the rule now lives in a file the test already checks.
- `test_host_rows.py`: `KNOWN` 53 (section 4).
- `test_plugin_files.py` passes unchanged: no host tool or forge tool name moves into a card that
  does not start with `host-`; the new `forges/gitlab.md` line may name `glab` (a forge note).

## Decisions from 02-answers.md

1. "ouvre un batch et lance ces 7 CR" (2026-11-27) is read as "grilled enough"; the owner's
   confirmation is still recorded as owed (question 1).
2. The batch is a stack: this CR sits in it after `cards-inventory-last-reading`, and only the
   top CR of the stack owes the local Windows scenario run.
3. card-cleanup-Q1 A: all 65 pages go now; this CR deletes its 32 and says, before it deletes,
   where each protective rule goes (section 5).
4. card-cleanup-Q5 A: steps 1 to 3 with a new version, in small CRs; the other project reads the
   cards live, so this CR lands within that version's stack and adds no step of its own.
5. Topic cards are agnostic of the host and the forge, save exceptions; one word, PR: host facts
   go to host rows (section 4), forge facts to `forges/gitlab.md`, and every new card line is
   written with no host or forge tool name.

## Out of scope

- The Chief of Staff side pages (`cards-delete-pages-chief`), the aggregate topic names
  (`cards-delete-aggregate-topics`), joining the `-pN` pages (`cards-one-page-per-theme`).
- `host-heartbeat-copilot.md` and every page not in section 1.
- The cost code's Write-tool coupling named in `direct-mode-epoch-p2.md`.
- Removing a host map's Copilot reading other than the three deleted Copilot pages.
- Rewording the kept pages beyond the lines sections 5 and 6 name.
- The `## Other: ` trial sections of `docs/proofs/*.md`.

## Evidence

- The diff is deletions, pointer fixes, the moved lines of section 5, the three host rows and
  their proof headings, the `help.py` change and the tests; nothing else.
- `$CHANTIER help` lists no removed topic; `$CHANTIER help <each of the 22 removed>` refuses with
  `no topic <name>`; `$CHANTIER help host-allow-broad --host copilot` prints the "no reading on copilot" line; `$CHANTIER help session-shell` names the
  workers; `$CHANTIER host allow-rules`, `auto-mode`, `windows-powershell-args` print their rows
  on both hosts.
- A repository grep for each of the 32 page names (`help <name>`, `topics/<name>.md`) finds
  none, outside `docs/proofs/` trial history and the git folder's old briefs.
- `docs/protective-rules.md` names none of the 32 pages as a home.
- `just check` passes; `just eval-dry-run` passes (a change under the CLI's `src/`).
- The long gate `just scenario (ubuntu-latest)` is green at the PR's head (a CLI and cards
  change).
- The PR description carries the table of section 5.

## Questions for the Chief of Staff

1. Answer 1 reads "ouvre un batch et lance ces 7 CR" as "grilled enough": does the owner confirm?
2. A one-host map in `help.py` (a CLI change) replaces `host-claude-only.md`. Is that the way, or
   should the eleven maps drop to a plain Claude reading, with the Copilot silence left to
   `chantier host`?
3. `direct-mode-epoch-p2.md`'s Write-tool cost coupling is dropped with the page. File it as an
   inbox item for the cost code, or leave it?
4. The matrix lines go to the `cr-rounds` and `cr-ship` topic pages, not to `cr-driver.md` as the
   review verdict proposed, to keep the Driver's start brief small. Agreed? And does the matrix
   probe stay at all (the verdict calls it over-built; `verifier-delta-matrix.md` and
   `closing.md` still name it)?
5. `host-for-you`'s "where, do, paste, expect, and say it is not tested" recipe: the verdict gives
   it one line in `chief-of-staff.md`; that card is `cards-delete-pages-chief`'s side. Add the
   line here, leave it to that CR, or drop it as inferable?
6. `windows-powershell-args` is an operating system fact: is a row on both hosts right, the
   Copilot one marked untested?
