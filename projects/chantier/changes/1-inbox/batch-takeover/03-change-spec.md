---
type: cr-change-spec
description: Take over, on another machine, a batch opened and paused (or stopped) elsewhere, from a record published at the batch's start and pause.
---

# Change Specification: take over a batch opened on another machine

## Goal

In the user's words (2026-11-16, translated): "Reopen the batch here and take up its state as if
it had been started here." A batch opened on machine A and paused there (or stopped there without
a pause) is reopened on machine B as the same batch: its CRs, their PRs and branches, rounds,
notes, events and cost to date. No second batch is opened, no CR goes back to `3-ready`, and a CR
keeps its existing PR branch (no head pushed to two branches).

What happened instead (batch-21's retro): batch-20's `batch.json`, `events.jsonl` and `brief.md`
were local and unpublished; `pause` refused batch-20 because CR-296 was not merged, though nothing
ran; batch-20's record stays `running` in `5-archives/batches/`; CR-296 went back to `3-ready`
into a new batch-21, and its Driver pushed one head to batch-20's PR branch and to the batch-21
branch name the CLI expected for its pushed check.

## Decisions carried from `02-answers.md`

- **Q1, two records.** The batch's live record stays local and ignored by git, as today
  (`4-batch/batch.json`, `events.jsonl`, `brief.md`). A second record, published in the planning
  folder, is written only at the batch's start and at its pause. A takeover reads the published
  one.
- **Q2 as amended by Q5, when a takeover is allowed.** A paused batch is taken over at once. A
  batch not paused is refused, naming its open (start) time and its machine, and is taken over
  only when the user confirms the other machine has stopped. There is no "silent for a while"
  rule: the published record changes only at the start and the pause, so silence cannot be seen.
- **Q3, costs.** The cost priced to date on the machine that pauses is written in the published
  record at the pause; a takeover carries it over.
- **Q6, a machine stopped without a pause.** The takeover starts from the record published at the
  start, plus what the forge and the surface show (the PRs, the branches, the CRs' pushed
  documents). The rounds, notes, events and costs never published are named
  "lost on <machine>", never estimated.
- **Q4, scope: the whole retro point.** `pause` accepts a batch whose remaining CRs are stopped or
  blocked by the user; the CR keeps its existing PR branch; batch-20's stale record (`running` in
  `5-archives/batches/`) is closed as superseded.

## What changes

### 1. The published record: `5-archives/batches/batch-NN.json`

The published record is the file that already exists: `open` writes it as `running` today
(`core/batch_records.py`, `reserve_record`, `open_record`) and `close` completes it
(`history.close_record`). It stays one file per batch, so two machines never edit the same file.
It gains:

- `machine`: the name of the machine that last published it (`platform.node()`), written at every
  publish.
- `published`: the UTC time of that publish.
- `state`: `running` (written at a start) or `paused` (written at a pause), `closed` at `close`
  as today.
- `paused`: the pause's time, or `null`.
- At a pause, `cost_usd` and `cost_unpriced`: the cost to date (see 4), with `carried` (see 4).
- `resume`: what a takeover needs, as of the publish:
  - `batch`: `batch.json`'s content, less what only means something on the machine that wrote it:
    the CRs' `worktree` paths, the transcript and session ids (`foreman`, `foreman_transcript`,
    `foreman_transcripts`, `foreman_claims`, `chief_transcript`, `chief_transcripts`) and
    `heartbeat`/`heartbeat_stopped`.
  - `events`: the lines of `events.jsonl`, as they are.
  - `brief`: `brief.md`'s text.
- `taken_over`: a list, one entry per takeover: `{from, to, at, record_published, confirmed}`
  (`confirmed`: true when the batch was not paused and the user confirmed the other machine had
  stopped).

The publishes ("a start" and "a pause" of Q1):

- `open` (as today, plus the new fields, `state: running`);
- `pause`, plain or held (see 2): `state: paused`;
- `takeover` (see 3): it is the batch's start on the new machine, `state` as the batch is after
  it (paused when taken over from a pause);
- the first `take` that sets a paused batch running again (`commands/driver.py`, the `reopen`
  event) and `order qa` on a paused batch (`commands/orders.py`, `_reopen`): the batch starts
  again, `state: running`. This keeps a paused record from being taken over at once while the
  first machine works on it again (open question 1).

`close` writes the record as today; it drops `resume` and keeps `machine`, `taken_over` and the
cost lines. A record written before this change has no `resume`: it cannot be taken over (the
refusal says so); nothing reads it differently otherwise.

Every write of the record happens inside the same lock and the same all-or-nothing step as the
`batch.json` change it goes with: a pause, a start or a takeover that cannot write the record
changes nothing and says why. The CLI keeps no git write: the record reaches the surface (or the
project's repository, in-project) through the surface's autosync or the Chief of Staff's own
commit, as every planning-folder file today.

Docs: `docs/planning-modes.md` ("What stays local, what is pushed": the record and its `resume`
are published, written at the start and the pause only, the live files stay local),
`docs/planning-folder.md` (the `5-archives/batches/` line and the pause paragraph),
`skills/chantier/references/concepts.md` ("Planning folder": "written by `open` as `running`,
completed by `close`" becomes the list of publishes above).

### 2. `pause --hold`: the batch stops with CRs not merged

`chantier pause --epoch <n> --hold "<the user's words>"` (`commands/closing.py`, `pause`;
`declare/closing.py`), run by the steering session on the user's word only (the Chief of Staff in
direct mode; in Foreman mode the Chief of Staff sends the Foreman the user's words and the
Foreman runs it).

- Accepted, with `--hold`: remaining CRs that no Driver holds: `queued`, `ready`, `blocked`, and
  `working` with no agent recorded (a Driver that stopped, cleared by the steering session with
  `agents set <cr> - --epoch <n>` after a `note`). Such a `working` CR becomes `blocked` with
  `blocked_reason` `context: held at the pause: <the user's words>`, its phase cleared.
- Still refused, with or without `--hold`: a `working` CR with an agent recorded, an open order,
  a stack agent; the refusal names each, as today.
- Without `--hold`, today's refusal stands, and when the only causes are CRs a hold would accept,
  it ends with: `on the user's word: pause --epoch <n> --hold "<their words>"`.
- The `pause` event records `hold` (the words) and the held CRs; the batch's `STATUS.md` names
  them; the record is published as `paused` (1), cost to date included.
- `close` is unchanged: it refuses while a CR is not merged or cancelled. A held batch is taken
  over, or set running again (`order add`, `take <cr> --note`), not closed.

Cards: `foreman.md` (the pause: `--hold` on the Chief of Staff's message carrying the user's
words, never on its own judgment), `chief-of-staff.md` ("Steering a batch yourself", "The pause"
bullet; the entry points table: "stop here, I will go on elsewhere" → `pause --hold`).
`evals/SCORECARD.md` C14 says the held pause.

### 3. `chantier takeover <batch>`: the batch reopens here

A new role-free command (`commands/takeover.py`, declared in `declare/takeover.py`, added to
`cli.py`'s `FULL_OUTPUT`), run by the Chief of Staff on the user's word, after pulling the
planning folder (the surface's autosync `sync`, or a plain pull).

`chantier takeover <batch> [--confirmed-stopped]`:

- **Reads** `5-archives/batches/batch-NN.json`.
- **Refuses** (exit 2, nothing written):
  - no record, a `closed` record, or one with no `resume`: `<batch> cannot be taken over: <cause>`;
  - a local batch of another id in `4-batch/`: `this machine holds <id>: it is not closed`;
  - a record `running` without `--confirmed-stopped`: `<batch> runs on <machine> since <open or
    last start time> (published <time>): take it over only once the user confirms <machine> has
    stopped: takeover <batch> --confirmed-stopped`;
  - the record's remote missing in this clone (as `open_settings` checks), or this host's
    playbook with problems (as `open` reads it);
  - a CR folder found nowhere in the planning folder (see below), named.
- **A local copy of the same batch** is replaced only when it is older than the record
  (`resume.published` later than this machine's own last publish of it); a local copy as new as
  the record is refused: `this machine already holds <batch> as published`.
- **Writes**, under the lifecycle lock, all or nothing:
  - `4-batch/batch.json` from `resume.batch`, with: `host` this machine's host; the transcript
    and session fields empty, then `chief_transcript(s)` this session's own id (`own_transcript`,
    as `open` reads it; a direct batch refuses when it is unknown, as `open --direct` does);
    `foreman_epoch` kept, so the next claim is the next epoch; the playbook kept when the host is
    the same, else this host's (`read_playbook`); each CR not merged or cancelled gets this
    machine's worktree path (`repo.worktrees / f"{batch}-{cr}"`, as `add_cr` names it) and no
    agent; each CR keeps its `branch`, `pr`, `head`, `round`, `notes`, `after`, `cost_usd`.
  - `4-batch/events.jsonl` from `resume.events`, then one `takeover` event (`from`, `record_published`,
    `confirmed`, the lost window when there is one).
  - `4-batch/brief.md` from `resume.brief`, with one line added under "Autonomous decisions":
    `Taken over from <machine> at <time>.`
  - `.batch-number`, as `open` keeps it.
  - The record (1): `taken_over` gains its entry; `machine` and `published` are this machine's.
  - The STATUS files, as after any change.
- **A paused record**: the batch is taken over at once and stays paused here; nothing is lost.
- **A running record, confirmed** (Q6): the snapshot is the last start's. The CLI reconciles each
  CR with where its folder is in the planning folder, found by its number: in `3-done`, `merged`
  (`merged_at` read from its `delivery.md` when it says it, else `null`), note `merged on
  <machine>, read from the surface`; in `2-actives`, `blocked` with `blocked_reason`
  `context: taken over from <machine>: rounds, notes, events and costs since <published> are lost
  on <machine>`; in `1-pending`, `queued`; in `6-trash`, `cancelled`. Every CR not merged gets
  the note `lost on <machine>: rounds, notes, events and costs since <published>`. The cost is
  named lost (4). The CLI reads no forge and runs no git command for this: the branches and PRs
  are the agents' to read (below).
- **Prints**: `took over <batch> from <machine> (<paused at | running since> <time>)`, then
  one line per CR (id, state, branch, PR or `no PR recorded`), the carried cost, and, when
  confirmed, the `lost on <machine>` line; last line: `next: claim the batch (direct: foreman set
  --epoch <n>), then take each CR back with its note`.

What the Chief of Staff does after `takeover` (`chief-of-staff.md`, a new "Taking over a batch"
section, and the entry points table: "take over batch-NN here", "reprends le batch ici"):

1. Preflight as at a batch's start (direct or Foreman, by the batch's steering, which never
   changes; under Remote Control a Foreman batch needs a Foreman to reuse, as today).
2. Claim the next epoch (direct: `foreman set`, `foreman transcript`, then `$CHANTIER rules`;
   Foreman: start a new Foreman with the next epoch and "Resume: taken over from <machine>").
3. For each CR not merged: read its branch on the remote (`git -C <clone> fetch <remote>
   <branch>`, `git -C <clone> rev-parse <remote>/<branch>`) and its PR on the forge (`gh pr list
   --head <branch> --state all`, or `glab mr list --source-branch <branch>`), and take it back
   with `take <cr> --note "takeover: from <machine>; branch <branch> at <sha>, PR <url or none>"
   --epoch <n>`. For a running record taken over, what the forge shows that the record lacks (a
   PR, a newer head) goes in that note; the Driver records it with `ship` as usual.
4. Tell the user what was lost, when anything was, as the CLI printed it.

`driver.md`, the worktree bullet: a CR whose branch is already on the remote and has no local
branch or worktree (a `takeover:` note) creates its worktree from it: `git -C <main checkout>
fetch <remote> <branch>`, then `git -C <main checkout> worktree add -b <branch> <path>
<remote>/<branch>`. It keeps that branch and that PR: no new branch, no new PR. The pushed check
of `handback` (`driver_checks.handback_refusals`, `<remote>/<c.branch>`) is unchanged and now
reads the CR's own branch, so no second push is needed.

### 4. Costs carried and costs lost

- The batch record (`core/records.py`, `BatchRecord`) gains `carried`: a list of
  `{machine, until, usd, unpriced, by_cr, lost}`. At a takeover of a paused record, one entry
  holds the record's cost to date (its `cost_usd`, `cost_unpriced`, and each CR's `cost_usd`),
  `until` the pause's time, `lost: false`. At a confirmed takeover of a running record, the entry
  holds the cost of the last publish that priced one (none at the open: `usd` 0) and `lost: true`
  with `until` the record's `published`.
- The spend and the budget (`spent_usd`, `check_budget`), the pause's cost lines
  (`cost_summary`), `status --refresh`, `cost`, and `close`'s final cost are this machine's
  priced rows plus every `carried` entry's `usd`; a CR's cost adds its `by_cr` share.
- The cost lines say it: `Carried from <machine>, priced there up to <until>: $X` and, for a lost
  entry, `Lost on <machine> after <until>: not counted, never estimated`. `batch-NN.md`'s Cost
  section keeps both lines. `docs/costs.md` says the same.
- `close`'s idle check and its pricing read this machine's transcripts only: the other machine's
  are not in the batch's record any more, so they neither refuse `close` nor get priced twice.

### 5. One batch across machines

- `open` refuses (`rails.check_no_open_batch`) while a published record is `running` or `paused`
  and this machine holds no batch: `<batch> is open on <machine> (<state> since <time>): take it
  over (takeover <batch>) or close it there`. This is the request's "no second batch".
- `status` with no local batch, and `resolve_batch`'s "no running batch" refusal, name such a
  record the same way (one line), so a session's start sees it.
- On machine A, once B has taken the batch over: every command that writes the batch refuses when
  the record's `published` is later than A's own last publish and names another machine:
  `<batch> was taken over by <machine> at <time>: this machine's copy is stale, nothing was
  written`; A's `status` says the same in its first line (open question 2 for what A does next).

### 6. batch-20's stale record, closed as superseded

- The CLI reads a record's optional `superseded_by`: `history.last_closed_text` prints
  `<batch> superseded by <other>` for it, and nothing counts it as a running batch.
- After this CR merges, the Chief of Staff writes, with its Write tool, in the surface's
  `projects/chantier/changes/5-archives/batches/batch-20.json`: `state` `closed`, `closed` the
  time of the edit, `superseded_by` `batch-21`, `report` `null`, the other fields as they are; it
  is published like any planning-folder file. The CR's PR body names this step under Deliverables
  so the Chief of Staff runs it at the merge.

## Out of scope

- A batch run on two machines at once, and any live mirror of the batch's state: the record moves
  only at a start, a pause and a takeover.
- Any estimate of a lost cost or of lost rounds.
- Moving a running Driver from one machine to another: a Driver is never moved; a takeover starts
  fresh Drivers from the published state.
- The CR board pane (`hooks/register.tsx`) and the `STATUS.json` fields it shows: unchanged, so no
  pane screenshot is due. `hooks/` and `types/` are untouched (no `just mod`).
- The `agents/` and `com.github.copilot/agents/` files: unchanged (the contract is in the cards).
- Batches already closed: unchanged.

## Evidence

- `just check` on Linux, macOS and Windows; the PR's `just scenario (ubuntu-latest)` green at its
  head; the Windows long gate locally as AGENTS.md says.
- Tests (`skills/chantier/scripts/cli/tests/`, a parametrized `test_takeover.py`, in-process,
  fast): each refusal of 3 (no record, closed, no `resume`, another local batch, running without
  `--confirmed-stopped`, a local copy as new as the record); `pause` with and without `--hold`
  for each CR state of 2 (accepted: queued, ready, blocked, working with no agent; refused: working
  with an agent, an open order, a stack agent), and the hint line; `open` refused by a published
  open record of another batch; the published record's fields after `open`, a held `pause`, a
  `takeover` and a reopening `take` (no worktree path, no transcript id in `resume.batch`); the
  carried and lost cost lines; `last_closed_text` with `superseded_by`. `just test` stays inside
  its budget.
- Scenario (`scenario/run_scenario.py`): a case `batch_takeover` in the `surface-board` unit
  (README Coverage bullet `(unit: surface-board)`), on a `SurfaceWorld` with a second checkout of
  the surface and of the project's clone standing for machine B:
  1. On A: open a batch with two CRs; one ships a PR (scripted Driver), is handed back `ready`;
     the other stays `queued`. `pause` is refused, with the `--hold` hint; `pause --hold` passes;
     the record is `paused` with the cost to date and a `resume`; the surface's git lists the
     record and none of `4-batch`'s local files (`surface_publishes` updated).
  2. Publish A's surface, pull it in B. In B: `takeover` passes at once; `batch.json`'s CRs keep
     branch, PR, head, round and notes; worktree paths are B's; `events.jsonl` holds A's lines
     plus `takeover`; `status` shows the batch paused.
  3. In B: the ready CR's scripted Driver creates its worktree from `origin/<branch>` and hands
     back `ready` again at the same branch: the pushed check passes with no second branch on the
     remote (`git ls-remote` lists one branch for the CR).
  4. In B: `pause` again; the cost lines show `Carried from <machine>` and the total is A's plus
     B's.
  5. Back in A: a writing command refuses with `taken over by`; `open` in a third clean checkout
     refuses naming the open batch.
  6. A running record (no pause): `takeover` without `--confirmed-stopped` refuses naming the
     open time and the machine; with it, the CRs follow their folders (`2-actives` → `blocked`
     `context:`, `3-done` → `merged`), and the `lost on <machine>` note and cost line are there.
- The data step of 6 is seen in the surface after the merge: batch-20.json reads `closed`,
  `superseded_by: batch-21`, and `status`'s line says it.

## Open questions

1. **The first `take` after a pause republishes the record as `running`.** Q1 says the published
   record is written "only at the start and at the pause". This specification counts a paused
   batch set running again (its first `take`, or `order qa`) as a start, so another machine does
   not take over at once a batch the first machine is working on again. Keep that, or publish only
   at `open` and `pause`?
2. **Machine A's stale copy after a takeover.** Its writing commands refuse (5). What then clears
   A's local `4-batch/` files: A takes the batch back with `takeover` when it is paused again
   (the specification already allows a newer record to replace an older copy), and, once B has
   closed it, A's `open` replaces a stale copy of a closed batch after saying so? Or the user
   removes them by hand?
3. **What the record publishes.** The `resume` snapshot publishes the brief, the CRs' notes and
   the events as written (local paths and agent ids among them; worktree paths and session ids
   are left out). A surface may be public: is that acceptable, or should notes and events be
   left out of the snapshot (then a takeover keeps only the CRs' state, the brief and the costs)?
