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

The answers say "machine". In this specification a machine is a **publisher**, named by **the
publisher's id**: what writes the published record. How that id is made is open question 2; the
text below keeps it abstract (`<publisher>` in messages).

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
- **Q7, a paused batch that starts again is a start.** Its first `take` or `order qa` writes the
  published record again as `running`, so another machine cannot take it over without the user's
  confirmation.
- **Q8, machine A's leftover local copy is replaced when needed.** A takes the batch back with
  `takeover` once it is paused again; A's `open` replaces the leftover copy of a batch closed
  elsewhere, after saying so. The user removes nothing by hand.
- **Q9, what the record publishes.** The published record holds the brief, the CRs' notes and the
  events (no worktree paths, no session ids), so a takeover finds everything.

## What changes

### 1. The published record: `5-archives/batches/batch-NN.json`

The published record is the file that already exists: `open` writes it as `running` today
(`core/batch_records.py`, `reserve_record`, `open_record`) and `close` completes it
(`history.close_record`). It stays one file per batch, so two machines never edit the same file.
It gains:

- `publisher`: the publisher's id of the last publish, written at every publish.
- `publish`: a counter, 1 at `open`, one more at each publish. Publishes are ordered by this
  counter, never by a clock: two machines' clocks are not compared.
- `published`: the UTC time of that publish, shown to the user only, never compared.
- `state`: `running` (written at a start) or `paused` (written at a pause), `closed` at `close`
  as today.
- `paused`: the pause's time, or `null`.
- At a pause, `cost_usd` and `cost_unpriced`: the cost to date (see 4), with `carried` (see 4).
- `resume`: what a takeover needs, as of the publish (Q9):
  - `batch`: `batch.json`'s content, the CRs' notes included, less what only means something on
    the machine that wrote it: the CRs' `worktree` paths, the transcript and session ids
    (`foreman`, `foreman_transcript`, `foreman_transcripts`, `foreman_claims`, `chief_transcript`,
    `chief_transcripts`) and `heartbeat`/`heartbeat_stopped`.
  - `events`: the lines of `events.jsonl`, as they are, less any worktree path or session id
    field an event carries.
  - `brief`: `brief.md`'s text.
- `taken_over`: a list, one entry per takeover: `{from, to, at, from_publish, confirmed}`
  (`from` and `to` publishers' ids; `from_publish` the counter taken over; `confirmed`: true when
  the batch was not paused and the user confirmed the other machine had stopped).

The local `batch.json` (`core/records.py`, `BatchRecord`) gains `published_as`: the counter of
this checkout's own last publish of the batch (0 when it never published it). It is what a
checkout compares with the record's `publish` (3 and 5).

The publishes ("a start" and "a pause" of Q1, with Q7's restart counted as a start):

- `open` (as today, plus the new fields, `state: running`, `publish: 1`);
- `pause`, plain or held (see 2): `state: paused`;
- `takeover` (see 3): it is the batch's start on the new machine, `state` as the batch is after
  it (paused when taken over from a pause);
- the first `take` that sets a paused batch running again (`commands/driver.py`, the `reopen`
  event) and `order qa` on a paused batch (`commands/orders.py`, `_reopen`): the batch starts
  again, `state: running` (Q7). Another machine then cannot take it over at once while the first
  machine works on it again: it needs the user's confirmation, as for any running record.

Each publish writes the record's `publish` as the record's current one plus one, and sets the
local `published_as` to it.

`close` writes the record as today; it drops `resume` and keeps `publisher`, `publish`,
`taken_over` and the cost lines. A record written before this change has no `resume`: it cannot
be taken over (the refusal says so) and it blocks no `open` (5); nothing reads it differently
otherwise. batch-20's record, `running` with no `resume`, therefore stays as it is until the data
step of 6 closes it.

Every write of the record happens inside the same lock and the same all-or-nothing step as the
`batch.json` change it goes with: a pause, a start or a takeover that cannot write the record
changes nothing and says why. The CLI keeps no git write: the record reaches the surface (or the
project's repository, in-project) through the surface's autosync or the Chief of Staff's own
commit, as every planning-folder file today.

Docs and cards: `docs/planning-modes.md` ("What stays local, what is pushed": the record and its
`resume` are published, written at the start and the pause only, the live files stay local; the
`resume` holds the brief, the notes and the events, with no worktree path and no session id),
`docs/planning-folder.md` (the `5-archives/batches/` line and the pause paragraph),
`skills/chantier/references/concepts.md`: "Planning folder" ("written by `open` as `running`,
completed by `close`" becomes the list of publishes above), "Batch" (line 162: one batch at a
time across machines, a batch open elsewhere is taken over, not opened again) and "Batch
lifecycle" (line 244: each state's publish, the held pause of 2, and a takeover as a start).

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
bullet at line 1445, which today starts "Once every CR is merged or cancelled": it gains the held
pause on the user's word; the entry points table: "stop here, I will go on elsewhere" →
`pause --hold`). `evals/SCORECARD.md` C14 says the held pause.

### 3. `chantier takeover <batch>`: the batch reopens here

A new role-free command (`commands/takeover.py`, declared in `declare/takeover.py`, added to
`cli.py`'s `FULL_OUTPUT`), run by the Chief of Staff on the user's word, after pulling the
planning folder (the surface's autosync `sync`, or a plain pull).

`chantier takeover <batch> [--confirmed-stopped]`:

- **Reads** `5-archives/batches/batch-NN.json`.
- **Refuses** (exit 2, nothing written):
  - no record, a `closed` record, or one with no `resume`: `<batch> cannot be taken over: <cause>`;
  - a local batch of another id in `4-batch/`: `this machine holds <id>: it is not closed`;
  - a record `running` without `--confirmed-stopped`: `<batch> runs on <publisher> since <open or
    last start time> (published <time>): take it over only once the user confirms <publisher> has
    stopped: takeover <batch> --confirmed-stopped`;
  - the record's remote missing in this clone (as `open_settings` checks), or this host's
    playbook with problems (as `open` reads it);
  - a CR folder found nowhere in the planning folder (see below), named.
- **A local copy of the same batch** is replaced only when it is older than the record: the
  record's `publish` is higher than the local `batch.json`'s `published_as`. A local copy whose
  `published_as` equals the record's `publish` is refused: `this machine already holds <batch> as
  published`. This is how machine A takes back a batch B took over and paused again (Q8, and 5).
- **Writes**, under the lifecycle lock, all or nothing:
  - `4-batch/batch.json` from `resume.batch`, with: `host` this machine's host; the transcript
    and session fields empty, then `chief_transcript(s)` this session's own id (`own_transcript`,
    as `open` reads it; a direct batch refuses when it is unknown, as `open --direct` does);
    `foreman_epoch` kept, so the next claim is the next epoch; the playbook kept when the host is
    the same, else this host's (`read_playbook`); each CR not merged or cancelled gets this
    machine's worktree path (`repo.worktrees / f"{batch}-{cr}"`, as `add_cr` names it) and no
    agent; each CR keeps its `branch`, `pr`, `head`, `round`, `notes`, `after`, `cost_usd`;
    `published_as` the record's new `publish`.
  - `4-batch/events.jsonl` from `resume.events`, then one `takeover` event (`from`,
    `from_publish`, `confirmed`, the lost window when there is one, the agents cleared).
  - `4-batch/brief.md` from `resume.brief`, with one line added under "Autonomous decisions":
    `Taken over from <publisher> at <time>.`
  - `.batch-number`, as `open` keeps it.
  - The record (1): `taken_over` gains its entry; `publisher`, `publish` (one more) and
    `published` are this publish's.
  - The STATUS files, as after any change.
- **A paused record**: the batch is taken over at once and stays paused here; nothing is lost (a
  paused record has no agent, no open order and no stack agent, as 2 requires).
- **A running record, confirmed** (Q6): the snapshot is the last start's. The CLI reconciles each
  CR with where its folder is in the planning folder, found by its number: in `3-done`, `merged`
  (`merged_at` read from its `delivery.md` when it says it, else `null`), note `merged on
  <publisher>, read from the surface`; in `2-actives`, `blocked` with `blocked_reason`
  `context: taken over from <publisher>: rounds, notes, events and costs since <published> are
  lost on <publisher>`; in `1-pending`, `queued`; in `6-trash`, `cancelled`. Every CR not merged
  gets the note `lost on <publisher>: rounds, notes, events and costs since <published>`. The
  cost is named lost (4). The CLI reads no forge and runs no git command for this: the branches
  and PRs are the agents' to read (below).
  The agents the snapshot names are the other machine's and are gone with it: the CLI clears
  `stack_agent` and the `agent` of each open order (not `done`), each CR's agent too, and names
  each one cleared in the `takeover` event and in one printed line, `lost on <publisher>: <the
  stack agent | order O-k (<kind>) agent | CR agent>`. An open order stays open: its slot and its
  work are kept. An open QA order (`kind: qa`) stays open with its QA folder in the inbox (a
  planning-folder file, so what the QA driver wrote and published there is kept, the rest is lost
  on <publisher>); the steering session starts one new QA driver on that folder after the claim,
  or, on the user's word, ends the order with `order done`. A stack agent cleared is started again
  only when the stack has work, as today.
- **Prints**: `took over <batch> from <publisher> (<paused at | running since> <time>)`, then
  one line per CR (id, state, branch, PR or `no PR recorded`), the carried cost, and, when
  confirmed, the `lost on <publisher>` lines; last line: `next: claim the batch (direct: foreman
  set --epoch <n>), then take each CR back with its note`.

What the Chief of Staff does after `takeover` (`chief-of-staff.md`, a new "Taking over a batch"
section, and the entry points table: "take over batch-NN here", "reprends le batch ici"):

1. Preflight as at a batch's start (direct or Foreman, by the batch's steering, which never
   changes; under Remote Control a Foreman batch starts a new Foreman with no `cwd`, or reuses
   one: CR-414, merged 2026-11-20).
2. Claim the next epoch (direct: `foreman set`, `foreman transcript`, then `$CHANTIER rules`;
   Foreman: start a new Foreman with the next epoch and "Resume: taken over from <publisher>").
3. For each CR not merged: read its branch on the remote (`git -C <clone> fetch <remote>
   <branch>`, `git -C <clone> rev-parse <remote>/<branch>`) and its PR on the forge (`gh pr list
   --head <branch> --state all`, or `glab mr list --source-branch <branch>`), and take it back
   with `take <cr> --note "takeover: from <publisher>; branch <branch> at <sha>, PR <url or
   none>" --epoch <n>`. For a running record taken over, what the forge shows that the record
   lacks (a PR, a newer head) goes in that note; the Driver records it with `ship` as usual.
   Which CRs get a Driver at once is open question 1.
4. An open QA order or a cleared stack agent: as above.
5. Tell the user what was lost, when anything was, as the CLI printed it.

A worktree that is gone, its branch on the remote: three places today tell an agent to create a
worktree from a local branch or a base, and each gains the remote form, `git -C <main checkout>
fetch <remote> <branch>`, then `git -C <main checkout> worktree add -b <branch> <path>
<remote>/<branch>`, when the CR's branch is on the remote and has no local branch (a `takeover:`
note):

- `commands/facts.py:82-83`, the `worktree:` line of a CR's facts (`<base>` from `_base_of`, and
  `not created yet: a Driver creates it first`): for a CR with a `takeover:` note, the line names
  `<remote>/<branch>` as what the worktree is created from.
- `commands/crs.py:44-48`, `cr_worktree`'s refusal (`git worktree add -b <branch> <worktree>
  <base>`): it names the `<remote>/<branch>` form for such a CR.
- `skills/chantier/references/driver.md:711`, the stack driver's "one that is gone: `git -C <main
  checkout> worktree add <path> <branch>`": the branch may exist only on the remote after a
  takeover; the remote form above then applies.

`driver.md`, the worktree bullet (the CR Driver's): a CR whose branch is already on the remote and
has no local branch or worktree (a `takeover:` note) creates its worktree from `<remote>/<branch>`
as above. It keeps that branch and that PR: no new branch, no new PR. The pushed check of
`handback` (`driver_checks.handback_refusals`, `<remote>/<c.branch>`) is unchanged and now reads
the CR's own branch, so no second push is needed.

### 4. Costs carried and costs lost

- The batch record (`core/records.py`, `BatchRecord`) gains `carried`: a list of
  `{publisher, until, usd, unpriced, by_cr, lost}`, published in the record with the cost lines.
- **Each entry holds one publisher's own share, never a total.** At a takeover of a paused
  record, the new entry holds the pausing publisher's own priced share: the record's `cost_usd`
  minus the `usd` of every `carried` entry the record already lists (and likewise per CR for
  `by_cr`, and `unpriced` that publisher's own unpriced CRs), `until` the pause's time,
  `lost: false`. So A → B → A lists A's first share, B's share and, at A's next pause, A's later
  share, each once, and the total is their sum.
- At a confirmed takeover of a running record, the entry holds that publisher's share as of the
  last publish that priced one (none at the open: `usd` 0, a known zero) and `lost: true` with
  `until` the record's `published`.
- **A pause whose cost cannot be priced** (no transcript readable, a model with no price)
  publishes `cost_usd: null`, and `cost_unpriced` names what was not priced. A takeover of it
  writes that publisher's entry with `usd: null`. A `null` share is never added as 0: the spend
  and the budget add the known shares, and every line that shows a total with a `null` share in
  it says it is a floor (`at least $X`, then `<publisher>'s share unknown`).
- The spend and the budget (`spent_usd`, `check_budget`), the pause's cost lines
  (`cost_summary`), `status --refresh`, `cost`, and `close`'s final cost are this machine's
  priced rows plus every `carried` entry's known `usd`; a CR's cost adds its known `by_cr` shares.
- The cost lines say it: `Carried from <publisher>, priced there up to <until>: $X` (or `: unknown`
  for a `null` share), and, for a lost entry, `Lost on <publisher> after <until>: not counted,
  never estimated`. `batch-NN.md`'s Cost section keeps these lines. `docs/costs.md` says the same.
- `close`'s idle check and its pricing read this machine's transcripts only: the other machine's
  are not in the batch's record any more, so they neither refuse `close` nor get priced twice.

### 5. One batch across machines

- `open` refuses (`rails.check_no_open_batch`) while a published record that carries `resume`
  (written by this version) is `running` or `paused` and this machine holds no batch: `<batch> is
  open on <publisher> (<state> since <time>): take it over (takeover <batch>) or close it there`.
  This is the request's "no second batch". A record with no `resume` (older, such as batch-20's)
  blocks nothing.
- `status` with no local batch, and `resolve_batch`'s "no running batch" refusal, name such a
  record the same way (one line), so a session's start sees it.
- On machine A, once B has taken the batch over: every command that writes the batch refuses when
  the record's `publish` is higher than A's `published_as` and its `publisher` is not A's:
  `<batch> was taken over by <publisher> at <time>: this machine's copy is stale, nothing was
  written`; A's `status` says the same in its first line, and adds what clears it (Q8): `takeover
  <batch>` once the record is paused, or `open` once it is closed.
- A's leftover copy is replaced, never removed by hand (Q8):
  - **The batch paused again elsewhere**: A runs `takeover <batch>`; its local copy is older than
    the record (`publish` higher than its `published_as`), so it is replaced (3).
  - **The batch closed elsewhere**: A's `open` (`rails.check_no_open_batch`, and `open`'s own
    step) reads the local `4-batch/batch.json`'s id; when that batch's published record is
    `closed` and names another publisher, `open` prints `<batch> was closed on <publisher> at
    <time>: this machine's leftover copy is replaced`, removes the local batch files
    (`batch.json`, `events.jsonl`, `brief.md`, the batch's STATUS files and locks: the
    git-ignored files of `4-batch/`), and opens the new batch in the same lifecycle lock, all or
    nothing. It removes no worktree and no branch: those are the agents' (the Chief of Staff names
    A's leftover worktrees to the user, as at any close). A local batch whose record is not
    `closed` is refused as today.

### 6. batch-20's stale record, closed as superseded

- The CLI and the board read a record's optional `superseded_by`; nothing counts such a record as
  a running batch.
- `last_closed()` (`core/batch_records.py:109-119`) returns the closed record with the highest
  number, so it never shows batch-20 (batch-21 and later are closed or higher): it is unchanged,
  and no `status` line names batch-20.
- Where `superseded_by` shows: the web board's history. Its model,
  `board/web/js/model/history.js:5` `closedBatches`, feeds the home's history
  (`views/home-history.js`), the home feed's last closed batch (`views/home-feed.js`) and the
  Costs history (`views/costs-history.js`). batch-20's record, once closed, must not appear there
  as an empty closed batch (CRs `0/0`, a cost of `$0`, or the home feed's "last closed"): a
  superseded record is drawn as one line, `<batch> superseded by <other>` (a key in
  `i18n/en-board.js` and `i18n/fr-board.js`), with no CR count and no cost, and the home feed's
  last closed batch skips it. The board server's `_history` (`board/state.py:102`) serves the
  record as it is.
- After this CR merges, the Chief of Staff writes, with its Write tool, in the surface's
  `projects/chantier/changes/5-archives/batches/batch-20.json`: `state` `closed`, `closed` the
  time of the edit, `superseded_by` `batch-21`, `report` `null`, the other fields as they are; it
  is published like any planning-folder file. The CR's PR body names this step under Deliverables
  so the Chief of Staff runs it at the merge.

## Out of scope

- A batch run on two machines at once, and any live mirror of the batch's state: the record moves
  only at a start (Q7's restart included), a pause and a takeover.
- Any estimate of a lost cost or of lost rounds.
- Moving a running Driver from one machine to another: a Driver is never moved; a takeover starts
  fresh Drivers from the published state.
- Removing a machine's leftover worktrees or branches: the CLI replaces only the batch's local
  files (5).
- The CR board pane (`hooks/register.tsx`) and the `STATUS.json` fields it shows: unchanged, so no
  pane screenshot is due. `hooks/` and `types/` are untouched (no `just mod`). The web board's
  history views (6) are not the pane.
- The `agents/` and `com.github.copilot/agents/` files: unchanged (the contract is in the cards).
- Batches already closed: unchanged.

## Evidence

- `just check` on Linux, macOS and Windows; the PR's `just scenario (ubuntu-latest)` green at its
  head; the Windows long gate locally as AGENTS.md says.
- Tests (`skills/chantier/scripts/cli/tests/`, a parametrized `test_takeover.py`, in-process,
  fast): each refusal of 3 (no record, closed, no `resume`, another local batch, running without
  `--confirmed-stopped`, a local copy whose `published_as` equals the record's `publish`);
  `pause` with and without `--hold` for each CR state of 2 (accepted: queued, ready, blocked,
  working with no agent; refused: working with an agent, an open order, a stack agent), and the
  hint line; `open` refused by a published open record of another batch that carries `resume`,
  and not refused by a `running` record with no `resume`; `open` replacing a leftover local copy
  whose record is `closed` by another publisher (the line printed, the old files gone, the new
  batch open) and refusing one whose record is not `closed`; the published record's fields after
  `open`, a held `pause`, a `takeover` and a reopening `take` or `order qa` (`state: running`
  again; `publish` one more at each, `published_as` equal to it; no worktree path, no transcript
  or session id in `resume.batch` and `resume.events`; the notes and the brief present); a
  confirmed takeover of a running record with a stack agent, an open order and an open QA order
  (the agents cleared, each named `lost on <publisher>`, the orders still open); the carried
  entries over A → B → A (three entries, each publisher's own share once, the total their sum);
  an unpriced pause (`cost_usd: null`, the carried line `unknown`, the spend a floor, never
  `$0` added); the lost cost line; the facts' `worktree:` line and `cr_worktree`'s refusal
  naming `<remote>/<branch>` for a CR with a `takeover:` note. `just test` stays inside its
  budget.
- Board (`tests/test_board.py`): the state the board serves holds batch-20's record `closed` with
  `superseded_by`, served as it is. `closedBatches` and the three history views are pure over that
  state; the Driver proves their drawing of a superseded record (one `superseded by` line, no CR
  count, no cost, not the home feed's last closed batch) with the scenario case's board check
  below.
- Scenario (`scenario/run_scenario.py`): a case `batch_takeover` in its own unit, `takeover`
  (a README Coverage bullet `(unit: takeover)`), with its own budget set by the rule of
  `scenario/README.md` (the loaded `--jobs 4` time plus about 25 percent, a row added to the
  table at line 54), on a `SurfaceWorld` with a second checkout of the surface and of the
  project's clone standing for machine B. **Two publishers on one host:** the publisher's id
  belongs to a checkout (open question 2's leaning), so the two checkouts are two publishers as
  they are; the case asserts their ids differ before step 1. Should the answer make the id the
  host's own, the scenario cannot make two publishers on one host and this case is revisited with
  the answer.
  1. On A: open a batch with two CRs; one ships a PR (scripted Driver), is handed back `ready`;
     the other stays `queued`. `pause` is refused, with the `--hold` hint; `pause --hold` passes;
     the record is `paused` with the cost to date, `publish` and a `resume`; the surface's git
     lists the record and none of `4-batch`'s local files (`surface_publishes` updated).
  2. Publish A's surface, pull it in B. In B: `takeover` passes at once; `batch.json`'s CRs keep
     branch, PR, head, round and notes; worktree paths are B's; `events.jsonl` holds A's lines
     plus `takeover`; `status` shows the batch paused.
  3. In B: the ready CR's scripted Driver creates its worktree from `origin/<branch>` and hands
     back `ready` again at the same branch: the pushed check passes with no second branch on the
     remote (`git ls-remote` lists one branch for the CR). The record now reads `running` (Q7).
  4. In B: `pause` again; the cost lines show `Carried from <A's id>` and the total is A's share
     plus B's.
  5. Back in A, after a pull: a writing command refuses with `taken over by`, and `status` names
     `takeover`; `takeover` then replaces A's copy (the record is paused), and the record's
     `carried` lists A's and B's shares, each once; `open` in a third clean checkout refuses
     naming the open batch.
  6. A running record (no pause): `takeover` without `--confirmed-stopped` refuses naming the
     open time and the publisher; with it, the CRs follow their folders (`2-actives` → `blocked`
     `context:`, `3-done` → `merged`), and the `lost on <publisher>` note and cost line are there.
  7. The batch closed on one checkout (its CRs merged or cancelled); in the other, after a pull,
     `open` prints the `leftover copy is replaced` line and opens the next batch.
  8. The board, served from one checkout with a record carrying `superseded_by`: its history
     shows that batch as `superseded by <other>`, with no CR count and no cost.
- The data step of 6 is seen in the surface after the merge: batch-20.json reads `closed`,
  `superseded_by: batch-21`, and the web board's history shows `batch-20 superseded by batch-21`,
  not an empty closed batch.

## Open questions for the user

1. **The CRs after a takeover.** Does each CR stay as it is (state, branch, PR), with a Driver
   started only when the CR has work (a `queued` CR when a slot frees, a `ready` one when a
   restack or a review asks for it), or does the Chief of Staff take back every CR not merged at
   once? The spec's leaning: each stays as it is, a Driver only when there is work.
2. **How a machine is named** (the publisher's id). A short id per checkout of the planning
   folder, never the hostname, with an optional label the user gives; or the host's name? The
   spec's leaning: a short per-checkout id with an optional label (this is also what lets the
   scenario run two publishers on one host).
3. **A sync conflict on the record** (two machines publish the same `batch-NN.json` before either
   pulls, for instance two takeovers). The spec's leaning: the Chief of Staff repairs it by hand
   in the surface, the later takeover (the higher `publish`, then the one the user names) wins,
   and the other publisher is named to the user.
