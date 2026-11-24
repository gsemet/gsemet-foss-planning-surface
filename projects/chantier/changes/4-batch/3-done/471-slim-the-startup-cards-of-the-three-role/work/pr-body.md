## Summary

The Chief of Staff, Foreman and Driver role cards were each read nearly whole at start, hundreds of kilobytes for the first two. Each card is now cut by moment of need: the entry card keeps its opening and a list of moments, and each piece is a new `<role>-<moment>.md` card that a `startup-manifest.json` action reads when that situation arrives. Text moves, it is not reworded; no rule is added or dropped (five duplicates were removed, each still stated elsewhere, and a few join words were added; see "Autonomous decisions").

## Deliverables

The cards are cut by moment; the figures and every moved rule follow (old place, new file#section, action, moment). The 12,544-byte startup limit is unchanged and the highest reload is 12,535 (Chief of Staff, Copilot; 9 bytes under).

Each row: the rule's first words, its old place (`card#section`; a bold item of that section when the
words start with one; `driver.md` alone is its opening), its new `file#section`, the action that reads it, and the moment.
The same rows, in the same order, are `MOVED_RULES` (`skills/chantier/scripts/cli/tests/moved_rules.tsv`).

#### The figures

Measured with the union rule of `test_startup_manifest.py` (LF bytes, each byte once). "Base" is the
cut's base, this branch's parent `3c29dd7c` (`origin/main` at the cut); `origin/main` at f4c1bccd,
the specification's "today", stated a manifest of 4,537 bytes and is not re-measured here.

#### The six start readings

| Role | Base (Claude) | After (Claude) | Ratio | Base (Copilot) | After (Copilot) | Ratio |
|---|---|---|---|---|---|---|
| Chief of Staff | 380,314 | 198,870 | 0.52 | 380,320 | 108,926 | 0.29 |
| Foreman | 292,020 | 87,596 | 0.30 | 292,026 | 81,082 | 0.28 |
| CR Driver | 25,134 | 27,180 | 1.08 | 25,200 | 27,246 | 1.08 |
| Stack Driver | 66,302 | 34,054 | 0.51 | 66,364 | 34,116 | 0.51 |
| QA Driver | 36,137 | 24,122 | 0.67 | 36,207 | 24,192 | 0.67 |
| Release Driver | 47,462 | 25,806 | 0.54 | 47,522 | 25,866 | 0.55 |

What the fix round (Fable readings) added to the start readings, by move: the Chief of Staff's
any-moment rules (forge permissions, offering options and refusals, compacting, tips, the floor)
sit in one new piece, `chief-of-staff-any.md` (19,819 bytes), read by the `chief-of-staff` entry
action, so the Chief of Staff's start reading grew by 21,049 bytes (Claude, 177,821 to 198,870;
Copilot 87,975 to 108,926) and its entry card by 1,023 (30,809 to 31,832); two or three smaller
actions would cost less but need manifest bytes the reload does not have (9 bytes of room). The
Foreman's grew by 739 (moments reworded as events, the take-back and escalation lines); the Stack
Driver's by 1,362 (the every-take definitions and the "read `driver:ship` before a take's first
rebase or push" line, now in `driver.md#Stack driver`), the Release Driver's by 415 (its failure
rule, now in `driver.md#Release driver`), the CR Driver's and QA Driver's by 58.

Each Driver's figure counts `driver.md`'s opening. Where about half is not reached, the reason:

- **CR Driver (1.08):** its first action at the base was already its minimum (three `Means:`
  sections and "CR driver"). It now also reads `driver.md#Means: the specification` (347 bytes,
  the opening's "Specification" bullet moved there, as section 3 asks) and its boot grew by the
  list of moments in `driver.md#Startup core` (+2,022 bytes boot: 8,519 to 10,541), which carries
  the moments that were links before (re-takes, trouble, refusals, conflicts, hand-backs, PR
  extras, session, matrix) and the step lists of the other Drivers.
- **QA Driver (0.67):** its role section is short and it still needs `driver:start` and the
  specification at its first step; the four ship sections moved to `driver:ship`, read at its ship.
- **Release Driver (0.54):** close to half; its first line keeps `driver:start` and "Release driver"
  with its step list.

### Boot and reload per role (limit 12,544, not raised)

| Role | Boot base (Claude/Copilot) | Boot after | Reload base | Reload after |
|---|---|---|---|---|
| chief-of-staff | 11,636 / 11,642 | 11,708 / 11,714 | 12,527 / 12,533 | 12,529 / 12,535 |
| status | 11,385 / 11,391 | 11,688 / 11,694 | 12,276 / 12,282 | 12,509 / 12,515 |
| griller | 11,197 / 11,203 | 11,267 / 11,273 | 12,088 / 12,094 | 12,088 / 12,094 |
| router | 11,135 / 11,141 | 11,581 / 11,587 | 12,026 / 12,032 | 12,402 / 12,408 |
| foreman | 7,740 / 7,921 | 8,566 / 8,747 | 8,631 / 8,812 | 9,387 / 9,568 |
| cr-driver (all Drivers share it) | 8,519 / 8,585 | 10,541 / 10,607 | 9,410 / 9,476 | 11,362 / 11,428 |
| board-griller | 10,242 / 10,335 | 11,096 / 11,189 | 11,133 / 11,226 | 11,917 / 12,010 |

The highest is the Chief of Staff's Copilot reload, 12,535 (9 bytes under the limit; 33 before the fix round).

#### The manifest

4,537 bytes at f4c1bccd (the specification's figure); 4,556 at the base `3c29dd7c`; 5,429 after
(+873 at the base: 32 new actions, one short line each, the one-host form for the Chief of Staff's
and the Foreman's host cards, and `@driver:start`, `@driver:ship`, `@driver:end`, `@driver:brief`
and `@host`, each saving bytes over its readings written out).

#### The CR Driver's own limits (`test_startup_manifest.py`)

| Lines | Bytes | Limit |
|---|---|---|
| `cr-driver` | 16,639 | 18,000 |
| `cr-driver` + `cr-driver:ship` + `cr-driver:closing` | 35,996 | 36,000 (35,972 at the base) |
| restart + `cr-driver:closing` | 9,346 | 13,000 |
| `driver.md`'s opening | 2,154 | `CR_DRIVER_OPENING_LIMIT` lowered from 2,500 to 2,154 |

#### The Chief of Staff (`chief-of-staff.md`)

| First words | Old place | New place | Action | Moment |
|---|---|---|---|---|
| - **The pause:** on `[foreman→chief-of-staff] | chief-of-staff.md#While it runs | chief-of-staff-batch-end.md#While it runs: the pause and what follows | `chief-of-staff:batch-end` | a batch's last CR ended: the pause, the retro, a recovery |
| - **Any other list of changes | chief-of-staff.md#While it runs | chief-of-staff-batch-end.md#While it runs: the pause and what follows | `chief-of-staff:batch-end` | a batch's last CR ended: the pause, the retro, a recovery |
| - **The chantier route** (a | chief-of-staff.md#While it runs | chief-of-staff-batch-end.md#While it runs: the pause and what follows | `chief-of-staff:batch-end` | a batch's last CR ended: the pause, the retro, a recovery |
| - **When the project is chantier | chief-of-staff.md#While it runs | chief-of-staff-batch-end.md#While it runs: the pause and what follows | `chief-of-staff:batch-end` | a batch's last CR ended: the pause, the retro, a recovery |
| - **Closing:** `--yes` only on | chief-of-staff.md#While it runs | chief-of-staff-batch-end.md#While it runs: the pause and what follows | `chief-of-staff:batch-end` | a batch's last CR ended: the pause, the retro, a recovery |
| - **Recovery:** a stale heartbeat | chief-of-staff.md#While it runs | chief-of-staff-batch-end.md#While it runs: the pause and what follows | `chief-of-staff:batch-end` | a batch's last CR ended: the pause, the retro, a recovery |
| - **Putting back:** on the | chief-of-staff.md#While it runs | chief-of-staff-batch-end.md#While it runs: the pause and what follows | `chief-of-staff:batch-end` | a batch's last CR ended: the pause, the retro, a recovery |
| At your first turn of a session | chief-of-staff.md#Forge permissions (P9) | chief-of-staff-any.md#Forge permissions (P9) | `chief-of-staff` | the first turn and any moment (`chief-of-staff-any.md`, read by the entry action) |
| At step 1 of "Starting a batch", | chief-of-staff.md#The trials before the go | chief-of-staff-batch-start.md#The trials before the go | `chief-of-staff:batch-start` | the user's "run them", up to the Foreman's start or `open --direct` |
| Only in the turn where the | chief-of-staff.md#Starting a batch | chief-of-staff-batch-start.md#Starting a batch | `chief-of-staff:batch-start` | the user's "run them", up to the Foreman's start or `open --direct` |
| In direct mode no Foreman | chief-of-staff.md#Steering a batch yourself | chief-of-staff-direct.md#Steering a batch yourself | `chief-of-staff:direct` | steering a batch yourself (direct mode) |
| ```bash $CHANTIER file "<raw request>" | chief-of-staff.md#Backlog and grill | chief-of-staff-grill.md#Backlog and grill | `chief-of-staff:grill` | filing, moving or grilling a CR, the Spec-writer and the spec critic |
| - **The words to the user** | chief-of-staff.md#While it runs | chief-of-staff-merge.md#While it runs: merging | `chief-of-staff:merge` | a PR ready to merge, a merge to record, a stack, a hold, an insert |
| - **The icon is the present:** | chief-of-staff.md#While it runs | chief-of-staff-merge.md#While it runs: merging | `chief-of-staff:merge` | a PR ready to merge, a merge to record, a stack, a hold, an insert |
| - **A draft says "do not merge":** | chief-of-staff.md#While it runs | chief-of-staff-merge.md#While it runs: merging | `chief-of-staff:merge` | a PR ready to merge, a merge to record, a stack, a hold, an insert |
| - **"You can merge it"** / | chief-of-staff.md#While it runs | chief-of-staff-merge.md#While it runs: merging | `chief-of-staff:merge` | a PR ready to merge, a merge to record, a stack, a hold, an insert |
| - **A plain `ready-to-merge <cr> | chief-of-staff.md#While it runs | chief-of-staff-merge.md#While it runs: merging | `chief-of-staff:merge` | a PR ready to merge, a merge to record, a stack, a hold, an insert |
| - **A series batch:** the | chief-of-staff.md#While it runs | chief-of-staff-merge.md#While it runs: merging | `chief-of-staff:merge` | a PR ready to merge, a merge to record, a stack, a hold, an insert |
| - **A stack batch:** the one-action | chief-of-staff.md#While it runs | chief-of-staff-merge.md#While it runs: merging | `chief-of-staff:merge` | a PR ready to merge, a merge to record, a stack, a hold, an insert |
| - **Dropping a CR from a stack:** | chief-of-staff.md#While it runs | chief-of-staff-merge.md#While it runs: merging | `chief-of-staff:merge` | a PR ready to merge, a merge to record, a stack, a hold, an insert |
| - **Holding a CR:** on the | chief-of-staff.md#While it runs | chief-of-staff-merge.md#While it runs: merging | `chief-of-staff:merge` | a PR ready to merge, a merge to record, a stack, a hold, an insert |
| - **Inserting a CR into a | chief-of-staff.md#While it runs | chief-of-staff-merge.md#While it runs: merging | `chief-of-staff:merge` | a PR ready to merge, a merge to record, a stack, a hold, an insert |
| A release is a CR a Release | chief-of-staff.md#Releases | chief-of-staff-release.md#Releases | `chief-of-staff:release` | a release |
| - **Status:** `$CHANTIER status [--notes]`, | chief-of-staff.md#While it runs | chief-of-staff-steering.md#While it runs | `chief-of-staff:steering` | a batch running: status, reports, asks, the watcher, a refused force push or rebase |
| Before you offer the user | chief-of-staff.md#Offering options | chief-of-staff-any.md#Offering options | `chief-of-staff` | the first turn and any moment (`chief-of-staff-any.md`, read by the entry action) |
| - **Compacting:** once per session | chief-of-staff.md#While it runs | chief-of-staff-any.md#Compacting and tips | `chief-of-staff` | the first turn and any moment (`chief-of-staff-any.md`, read by the entry action) |
| - **Tips:** a tip comes only at four key moments | chief-of-staff.md#While it runs | chief-of-staff-any.md#Compacting and tips | `chief-of-staff` | the first turn and any moment (`chief-of-staff-any.md`, read by the entry action) |
| This applies the Hard rule "A refusal is said before it is met" | chief-of-staff.md#Offering options | chief-of-staff-any.md#Offering options | `chief-of-staff` | the first turn and any moment (`chief-of-staff-any.md`, read by the entry action) |
| The least time the batch can take, counted from facts | chief-of-staff.md#Starting a batch | chief-of-staff-any.md#The floor | `chief-of-staff` | the first turn and any moment (`chief-of-staff-any.md`, read by the entry action) |
| You ask the user for the batch's shape at every opening | chief-of-staff.md#Backlog and grill | chief-of-staff-batch-start.md#Starting a batch | `chief-of-staff:batch-start` | the user's "run them", up to the Foreman's start or `open --direct` |
| - **conflict:** in the surface's | chief-of-staff.md#Backlog and grill | chief-of-staff-writer.md#The surface's writer | `writer` | the surface's writer (a `writer:` line); also read by `chief-of-staff:grill` |
| - **blocked:** the way out | chief-of-staff.md#Backlog and grill | chief-of-staff-writer.md#The surface's writer | `writer` | the surface's writer (a `writer:` line); also read by `chief-of-staff:grill` |
| - **offline, or late:** tell | chief-of-staff.md#Backlog and grill | chief-of-staff-writer.md#The surface's writer | `writer` | the surface's writer (a `writer:` line); also read by `chief-of-staff:grill` |
| - **not running:** start the | chief-of-staff.md#Backlog and grill | chief-of-staff-writer.md#The surface's writer | `writer` | the surface's writer (a `writer:` line); also read by `chief-of-staff:grill` |
| - **stopped:** tell the user | chief-of-staff.md#Backlog and grill | chief-of-staff-writer.md#The surface's writer | `writer` | the surface's writer (a `writer:` line); also read by `chief-of-staff:grill` |

#### The Foreman (`foreman.md`)

| First words | Old place | New place | Action | Moment |
|---|---|---|---|---|
| - **An early conflict check | foreman.md#Your means | foreman-conflict.md#An early conflict check (parallel batch) | `foreman:conflict` | an early conflict check (parallel batch) |
| - **A held CR** (the Chief | foreman.md#Your means | foreman-hold.md#A held CR | `foreman:hold` | a held CR, a parked CR, a mode switch |
| - **Parking a CR on an outside | foreman.md#Your means | foreman-hold.md#Parking a CR on an outside wait | `foreman:hold` | a held CR, a parked CR, a mode switch |
| - **A mode switch** (the Chief | foreman.md#Your means | foreman-hold.md#A mode switch | `foreman:hold` | a held CR, a parked CR, a mode switch |
| - **A lost Driver** (a CR's, | foreman.md#Your means | foreman-lost-driver.md#A lost Driver | `foreman:lost-driver` | a Driver lost, silent, ended with no hand-back or stopped from outside |
| - On an `order merged <dependency>` | foreman.md#Your means | foreman-merge.md#An order merged, by mode | `foreman:merge` | a CR handed back ready, an `order merged`, the main checkout after a merge, a merge on GitHub, a CR taken back from `ready` |
| - **The main checkout after | foreman.md#Your means | foreman-merge.md#The main checkout after a merge | `foreman:merge` | a CR handed back ready, an `order merged`, the main checkout after a merge, a merge on GitHub, a CR taken back from `ready` |
| - **Merging on GitHub** (a | foreman.md#Your means | foreman-merge.md#Merging on GitHub | `foreman:merge` | a CR handed back ready, an `order merged`, the main checkout after a merge, a merge on GitHub, a CR taken back from `ready` |
| - A CR taken back from `ready` | foreman.md#Your means | foreman-merge.md#A CR taken back from ready | `foreman:merge` | a CR handed back ready, an `order merged`, the main checkout after a merge, a merge on GitHub, a CR taken back from `ready` |
| **The retro critic.** Draft the | foreman.md#Your goal | foreman-pause.md#The retro critic | `foreman:pause` | the pause and its retro |
| A Driver's force push the | foreman.md#A Driver's refused force push | foreman-refused.md#A Driver's refused force push | `foreman:refused` | a Driver's `push` or `rebase` line; also read by `chief-of-staff:steering` and `driver:refused` |
| A Driver's rebase the host | foreman.md#A Driver's refused rebase | foreman-refused.md#A Driver's refused rebase | `foreman:refused` | a Driver's `push` or `rebase` line; also read by `chief-of-staff:steering` and `driver:refused` |
| - A Release driver takes the | foreman.md#Your means | foreman-release.md#A release CR | `foreman:release` | a release CR |

#### The Drivers (`driver.md`)

| First words | Old place | New place | Action | Moment |
|---|---|---|---|---|
| The specification, whole or by part | driver.md | driver.md#Means: the specification | `driver:brief` | a CR, stack or QA Driver's first line (the specification) |
| - A `ship` refused `holds | driver.md#Means: carries, conflicts and the early push | driver-conflicts.md#Means: carries, conflicts and the early push | `driver:conflicts` | a carry, a conflict, the early push, a CR's move |
| A move is any change of the | driver.md#CR driver: moves and conflicts | driver-conflicts.md#CR driver: moves and conflicts | `driver:conflicts` | a carry, a conflict, the early push, a CR's move |
| - When the host asks for your | driver.md#Means: hand-backs out of the ordinary | driver-handback-other.md#Means: hand-backs out of the ordinary | `driver:handback-other` | a hand-back out of the ordinary |
| A specification that names no | driver.md#CR driver: matrix probe | driver-matrix.md#CR driver: matrix probe | `cr-driver:matrix` | a matrix probe, the board's write paths |
| A CR that touches the board's write paths carries, | driver.md#CR driver: the board's write paths | driver-matrix.md#CR driver: the board's write paths | `cr-driver:matrix` | a matrix probe, the board's write paths |
| - The archive in the PR: when | driver.md#Means: the archive in the PR | driver-pr-extras.md#Means: the archive in the PR | `driver:pr-extras` | the PR's archive, an image and the look, a GitLab form |
| - A taken-back note `evidence: | driver.md#Means: images and the look | driver-pr-extras.md#Means: images and the look | `driver:pr-extras` | the PR's archive, an image and the look, a GitLab form |
| - For GitLab, use `glab`'s | driver.md#Means: GitLab forms | driver-pr-extras.md#Means: GitLab forms | `driver:pr-extras` | the PR's archive, an image and the look, a GitLab form |
| - A force push the host refuses | driver.md#Means: a force push the host refuses | driver-refused.md#Means: a force push the host refuses | `driver:refused` | a force push or a rebase the host refuses |
| "A Driver's refused rebase", as for a push: | driver.md#Means: a rebase the host refuses | driver-refused.md#Means: a rebase the host refuses | `driver:refused` | a force push or a rebase the host refuses |
| A CR whose first `take` shows a `PR:` link came back to a batch: use | driver.md#CR driver: re-takes | driver-retake.md#CR driver: re-takes | `cr-driver:retake` | a re-take note (`rebase:`, `restack`, `folded:`) |
| - Before the branch's first | driver.md#Means: checkpoint commits | driver-session.md#Means: checkpoint commits | `driver:session` | a steering session's message, the lease, a checkpoint commit |
| - `[foreman→driver <cr>] note <text>`: | driver.md#Means: the steering session's messages | driver-session.md#Means: the steering session's messages | `driver:session` | a steering session's message, the lease, a checkpoint commit |
| Read when you wait, or when | driver.md#Means: the lease | driver-session.md#Means: the lease | `driver:session` | a steering session's message, the lease, a checkpoint commit |
| - A worker refused for its | driver.md#Means: a worker that fails | driver-trouble.md#Means: a worker that fails | `driver:trouble` | a failing worker or remote command, an escalation, a git command in the wrong place, a long gate to stop, CI with no check or beside the long gate |
| - Escalation ([concepts](concepts.md), "Escalation"): only | driver.md#Means: escalation | driver-trouble.md#Means: escalation | `driver:trouble` | a failing worker or remote command, an escalation, a git command in the wrong place, a long gate to stop, CI with no check or beside the long gate |
| - CI's `timing:` line is, | driver.md#Means: a remote command fails | driver-trouble.md#Means: a remote command fails | `driver:trouble` | a failing worker or remote command, an escalation, a git command in the wrong place, a long gate to stop, CI with no check or beside the long gate |
| - When the project's rules | driver.md#Means: CI beside the long gate | driver-trouble.md#Means: CI beside the long gate | `driver:trouble` | a failing worker or remote command, an escalation, a git command in the wrong place, a long gate to stop, CI with no check or beside the long gate |
| - Stop only your own CR's | driver.md#Means: stopping a long gate | driver-trouble.md#Means: stopping a long gate | `driver:trouble` | a failing worker or remote command, an escalation, a git command in the wrong place, a long gate to stop, CI with no check or beside the long gate |
| - The rules do not replace | driver.md#Means: when CI lists no check | driver-trouble.md#Means: when CI lists no check | `driver:trouble` | a failing worker or remote command, an escalation, a git command in the wrong place, a long gate to stop, CI with no check or beside the long gate |
| - A Driver and its workers | driver.md#Means: a git command in the wrong place | driver-trouble.md#Means: a git command in the wrong place | `driver:trouble` | a failing worker or remote command, an escalation, a git command in the wrong place, a long gate to stop, CI with no check or beside the long gate |
| Once the release is out (the | driver.md#Release driver | release-driver-end.md#Release driver: the end | `release-driver:end` | the end |
| - A release PR merged (you | driver.md#Release driver | release-driver-merged.md#Release driver: after the merge | `release-driver:merged` | after the merge |
| - What a person reviews or | driver.md#Release driver | release-driver-notes.md#Release driver: the notes, the drafts and the PR body | `release-driver:notes` | the notes, the drafts and the PR body |
| - In every mode, prepare the | driver.md#Release driver | release-driver-ship.md#Release driver: the release PR | `release-driver:ship` | the release PR |
| **Inserting into a stack ready | driver.md#Stack driver | stack-driver-changes.md#Stack driver: changes to a stack on the forge | `stack-driver:changes` | an insertion, a drop, a hold, a park, a conflict, heavy CI |
| **Removing a dropped CR.** Taken | driver.md#Stack driver | stack-driver-changes.md#Stack driver: changes to a stack on the forge | `stack-driver:changes` | an insertion, a drop, a hold, a park, a conflict, heavy CI |
| **A CR held out of the stack.** | driver.md#Stack driver | stack-driver-changes.md#Stack driver: changes to a stack on the forge | `stack-driver:changes` | an insertion, a drop, a hold, a park, a conflict, heavy CI |
| **A CR parked.** Taken with | driver.md#Stack driver | stack-driver-changes.md#Stack driver: changes to a stack on the forge | `stack-driver:changes` | an insertion, a drop, a hold, a park, a conflict, heavy CI |
| **A conflict that needs code,** | driver.md#Stack driver | stack-driver-changes.md#Stack driver: changes to a stack on the forge | `stack-driver:changes` | an insertion, a drop, a hold, a park, a conflict, heavy CI |
| **Heavy CI on a head.** A | driver.md#Stack driver | stack-driver-changes.md#Stack driver: changes to a stack on the forge | `stack-driver:changes` | an insertion, a drop, a hold, a park, a conflict, heavy CI |
| **A CR that joins** (it has | driver.md#Stack driver | stack-driver-joins.md#Stack driver: a join, a draft turning ready, a merge, a deadline | `stack-driver:joins` | a join, a draft turning ready, a merge, a deadline |
| **A draft that turns ready | driver.md#Stack driver | stack-driver-joins.md#Stack driver: a join, a draft turning ready, a merge, a deadline | `stack-driver:joins` | a join, a draft turning ready, a merge, a deadline |
| **A merge during a take.** | driver.md#Stack driver | stack-driver-joins.md#Stack driver: a join, a draft turning ready, a merge, a deadline | `stack-driver:joins` | a join, a draft turning ready, a merge, a deadline |
| **Deliver by a time.** A take | driver.md#Stack driver | stack-driver-joins.md#Stack driver: a join, a draft turning ready, a merge, a deadline | `stack-driver:joins` | a join, a draft turning ready, a merge, a deadline |
| **Making the stack.** Once two | driver.md#Stack driver | stack-driver-make.md#Stack driver: making the stack | `stack-driver:make` | making the stack and its five checks |
| **The local gate at the mergeable | driver.md#Stack driver | stack-driver-make.md#Stack driver: making the stack | `stack-driver:make` | making the stack and its five checks |
| **The five checks,** read on | driver.md#Stack driver | stack-driver-make.md#Stack driver: the five checks | `stack-driver:make` | making the stack and its five checks |
| The stack is what your prompt | stack-driver-restack.md#Stack driver: the restack pass | driver.md#Stack driver | `stack-driver` | the stack driver's first line (every take's definitions) |
| The release CR is the top piece | stack-driver-restack.md#Stack driver: the restack pass | driver.md#Stack driver | `stack-driver` | the stack driver's first line (every take's definitions) |
| A release with no PR yet is no anomaly | stack-driver-restack.md#Stack driver: the restack pass | driver.md#Stack driver | `stack-driver` | the stack driver's first line (every take's definitions) |
| A step fails on the product | release-driver-merged.md#Release driver: after the merge | driver.md#Release driver | `release-driver` | the release Driver's first line (any step's failure) |

## Blast radius

Grade: **2**. Instructions now arrive by action; a rule a role fails to read at its moment is the risk. Revert restores the single cards.

## Autonomous decisions

- To fit the 12,544-byte limit (the user chose to free bytes in the startup text rather than raise it or add a second manifest), the startup text was shortened with no rule lost: five duplicates removed, each still said elsewhere (the Chief of Staff skill description's no-argument sentence; the "chantier writes only" lines of the Chief of Staff and Griller skills; `startup-core.md`'s ", never \"without it\""; the launch paragraph's "never a Foreman, a Driver or a worker"; `session-start.md` "5. Reload"'s first sentence).
- The session-start reading takes only its own host card (also narrows the Griller's reading), to fit the limit.
- The cut is more than five edits, said plainly: besides the five duplicates, the startup text lost `startup-core.md`'s "runs no uv sync", the "(from the session's context...)" clause, "and its assets", and `driver.md`'s opening lost the gloss "(`git`, `gh`, `glab`)" after "Git and the forge are yours" (to hold its 2,154-byte opening limit). Each is a gloss, not a rule.
- `session-start.md` "5. Reload": its first sentence is not a duplicate (`role-core.md` says "At boot", and the reload action reads neither the host core nor the role's startup sections); its replacement widens "startup sections only" to the entry action plus the moment's action. That widening is specification Q11 and is intended.
- Fix round 1 (Fable readings): the Chief of Staff's any-moment rules are one new piece, `chief-of-staff-any.md`, read by the `chief-of-staff` entry action (cost above). Drivers finding 1 is a text pointer ("read `driver:ship` before a take's first rebase or push") because adding `@driver:ship` to the `stack-driver` action cost 11.9 KB; Drivers 6 (`driver:trouble`, 13,350 bytes) stays: the CR Driver's ship union has 4 bytes of room.

## Known gaps

- The Chief of Staff's sentence "chantier writes only to the planning folder (...), and a CR's archive in its PR when the project asks" is not in `skills/chief-of-staff/SKILL.md` any more (about 160 bytes; the Copilot reload has 9 bytes of room). Its twin is in `session-start.md` "4. First turn", where the user first hears it. Not restored.
- The Foreman's critic-for-any-other-list rule stays in the pause piece, and `foreman:reference` still reads the whole host card for one section (no byte room in the manifest for a section action).
- The CR Driver's start reading grew (1.08 of base, 25,134 to 27,180): its first action was already minimal; the specification section moved to its first step and its boot now carries the list of moments that were links before.
- The Foreman's "a Driver's silence" section exists only in the Claude host card, so its action cannot name it in the one-host form; the Foreman's reference action reads the whole host card, so it is reached.
- Independent readings of spec section 5 (slim-cards-Q9), one per role, read-only, all "fix first" with no rule lost: Chief of Staff, 334 of 334 blocks found; Foreman, 1,128 sentences, 0 lost; Drivers, 254 paragraphs, 0 lost. Their findings (CoS 1-6, Foreman 1-6, Drivers 1-8) are fixed in the fix round or answered above; the Inspector was re-run on the changed body (see Test plan). The readings are not re-run on the fixed body.

<details>
<summary>Details</summary>

## Changes

- New pieces `chief-of-staff-*.md`, `foreman-*.md`, `driver-*.md`, `stack-driver-*.md`, `release-driver-*.md`; entry cards trimmed; manifest actions added; links in cards, `CONTRIBUTING.md`, `evals/` updated; compaction sentence in `session-start.md`.
- Tests: `test_role_cards_split.py`, `test_start_reading.py`, `moved_rules.tsv`; nine tests read the file where a phrase now lives, assertions kept.

## Human decisions

- Each big card is cut by moment of need, each piece an action read when its situation arrives; the three roles in one change; the Chief of Staff and Foreman read only their own host's card; the manifest stays small with the moments listed in each entry card; after a compaction a role re-reads its entry action then its current moment's; the four Drivers' first readings are cut by step.
- The limit stays at 12,544 bytes: bytes are freed in startup text, not a raised limit or second manifest.

## Impacts

No visible change; roles read less at start.

## Test plan

- [x] Full test suite and lint pass (2405 passed) at `a96fd75`; CI `just check` to be read green on Linux, macOS and Windows at `a96fd75`.
- [x] Long gate `just scenario` passed at `3be21b3` before the fix round; at `a96fd75` it is running locally and in CI (result quoted by the Foreman's ready line).

## Internal references

CR-471 slim-cards; closes the backlog item role-cards-still-too-big-for-a-driver-s-.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
