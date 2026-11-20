# Change Specification: typed waits, a CR records what it waits for

Part E of the seven-part split of `2-backlog/P3/planning-server` (planning-server-Q7, "7 CR
séparés"). It starts from that CR's `experiments/03-change-spec-all-parts.md`, "Part E. Typed
waits" (E.1 to E.8, here "the reference"), and its `02-answers.md` (Q1 to Q30). It builds on two
specified CRs, `1-inbox/typed-journal-events` (Part A) and `1-inbox/forge-connectors`: where their
specifications or `02-answers.md` differ from the reference, they rank over it, and this text
follows them (named in §2). The questions of this specification's first version are settled in
this CR's own `02-answers.md` (2026-11-20, by the Chief of Staff), carried below as decisions.

No `issue:` line: the CR has no tracker issue.

## 1. Goal, in the user's terms

A CR that cannot go on records **what it waits for**, as a typed fact: a person's answer, a review
request's approval, a green pipeline on a head, or a review request merged. The same four words on
GitHub and GitLab, on Claude Code and Copilot. A CR of the backlog can wait too (the user's answer
between two grills). The forge hub, which already reads the batch's PRs, tells the steering
session when the forge shows an approval, a pipeline or a merge wait met, so no one has to look;
the steering session clears the wait and takes the CR back as today. GitLab's approval read is
proved on a real merge request (Free and Premium) before chantier relies on it.

The word is **wait** everywhere, never "gate": the fast gate and the long gate keep that word
(`docs/gates.md` does not change).

## 2. Dependencies, order, and decisions carried

`depends.json`: `{"after": ["typed-journal-events", "forge-connectors", "plan-store-interface"]}`
(`02-answers.md`, answer 2). This CR writes a backlog CR's `waits.json` through `repo.store`
(Part B, `1-inbox/plan-store-interface`, whose §2 names this use). Part C
(`2-backlog/P3/planning-server`) is **not** a dependency: its refusal with no writer in external
mode (its C.8 text) applies through Part B's `check_publish` whenever it lands, with nothing to
change here. Before Part C lands, `check_publish` refuses nothing and the backlog write goes
through.

Part D (`1-inbox/driver-leases`) may land before or after this CR: **whichever lands second**
adds `--lease <n>` to `wait <cr> add` (by the Driver) and keeps it on `handback` with `--wait`,
by Part D's rules (required on a Driver's commands, refused when not live), and joins the two
AGENTS.md exception sentences (§8) into one.

| Decision (source) | Where |
| --- | --- |
| Q7: seven separate CRs; A and B first, then C, then D to G | §2 |
| Q9: `wait` built and named in AGENTS.md as an exception to the measured-cost rule, citing the user's answer of 2026-11-20 ("tout") | §8 |
| Q22: a fourth type `merge`; a backlog CR may carry a wait (the user's answer between two grills) | §3.1, §3.2, §4 |
| Q23: GitLab approvals unproved; one read on a real GitLab MR on Free and on Premium before the GitLab half of `approval` ships | §5.3, §10.3 |
| Q24: forge monitoring through `forge-connectors`' interest registry and connectors; typed waits depend on it | §5 |
| Part A: a published type is one `PUBLISHED` entry of `hub/schemas.py` (model, wake rule, text, duplicate key, example payload) plus `just journal-schemas`; unknown types are counted and wake no one; a refused event is skipped | §6 |
| Part A §2 table: Part E publishes `wait-cleared@1`, written by the hub, wakes a watcher | §6 |
| forge-connectors §7: provider `waits` in `hub/waits.py`, kinds `{"pr"}`, one line in `PROVIDERS`; `by` `<batch> <cr> <wait id>`; `review` read by the connectors, null maps to `unknown`, never met; `board/forge_read.py` becomes `connectors` | §5 |
| forge-connectors §3.3: one `connectors.read` per project and cycle; a link no connector claims is left out with `UNCLAIMED`; a second repository makes the read refuse (`NOT_ONE_REPOSITORY`) | §5.2 |
| forge-connectors §7: "Part E's `wait add` decides whether to refuse such a `ref`" (another repository) | §4.2, §5.2 |
| forge-connectors §6.1 edit 1: Part E adds its interests to the budget sentence's "today" list | §8 |
| E.7, settled (`02-answers.md`, answer 1): the hub reads no forge for a backlog CR's waits; they are cleared by hand; AGENTS.md's budget does not change | §5.2, §12.2 |
| `02-answers.md`, answer 2: `plan-store-interface` joins `depends.json`; `planning-server` does not (its refusal applies through `check_publish` when it lands) | §2, §3.2 |
| `02-answers.md`, answer 3: `order drop` to the inbox or backlog writes the CR's open waits to the folder's `waits.json` | §3.2 |
| `02-answers.md`, answer 4: the free-text `blocked waits: <what>` reason stays; `--wait` adds typed waits beside any reason | §4.1 |
| `02-answers.md`: the writer's choices accepted (`link` beside `ref`; a link in another repository recorded, not read, cleared by hand; `open_waits` on the board; no pane change) | §3.1, §4.2, §5.2, §7 |
| Reference E.2: a wait changes no rule (`take`, `close`, `open`, the slots) | §4.5 |
| Reference E.2: no pane change, so no screenshot owed | §7.3 |
| driver-leases spec answer 2: the CR driver's common path stays capped at 45,000 bytes (`CR_DRIVER_COMMON_PATH_LIMIT`) | §9 |

## 3. What a wait is

### 3.1 The four types

Named by the fact, never by the forge or the host:

| Type | Waits for | `ref` | `link` |
| --- | --- | --- | --- |
| `answer` | a person's answer (the user, through the Chief of Staff) | the question, one line | null |
| `approval` | the review request's approval (a GitHub PR's review decision approved; a GitLab MR's approvals met, unproved: §5.3) | the PR or MR link | the same link |
| `pipeline` | a green pipeline on a head (every check of the head passed) | the head's full sha | the PR or MR link |
| `merge` | the review request merged (Q22) | the PR or MR link | the same link |

The reference gives `pipeline`'s ref as "the head's sha (and the PR or MR link)"; this
specification keeps the link in a field of its own, `link`, so the hub reads a link for every
forge type and `ref` stays one value.

A wait is one JSON object:

```json
{"id": "w2", "type": "pipeline", "ref": "3f1c9a0e...", "link": "https://github.com/o/r/pull/88",
 "since": "2026-11-20T10:02:03Z", "note": "CI re-run after the runner fix",
 "cleared_at": null, "cleared_by": null}
```

- `id`: `w1`, `w2`, ... per CR, the next after the highest id the CR ever had (a cleared wait
  keeps its id; ids carried from the backlog keep theirs).
- `since` and `cleared_at`: UTC ISO 8601 with `Z`, as the record's other times.
- `cleared_by`: `epoch <n>` (the steering session in a batch) or `hand` (a backlog CR).
- Open: `cleared_at` null. A cleared wait stays in the list (its history) until the CR leaves the
  stage it was cleared in (§3.2).

### 3.2 Where it lives

- **In a batch:** `CrEntry.waits` (a list, default empty) in `core/records.py`, saved in
  `batch.json` (local, never published). Waits are facts of the CR, not of the machine:
  `batch-takeover`'s `resume.batch` keeps them as it keeps the other `CrEntry` fields.
- **In the backlog** (`1-inbox/`, `2-backlog/P1..P4/`, `3-ready/`): `waits.json` in the CR's
  folder, `{"schema": 1, "waits": [...]}`. Published, browsable on the forge, it moves with the
  folder (a move of the folder is a move of the file). Written only through `repo.store`
  (`check_publish([<the CR folder>/waits.json])` before any change), so once Part C has landed,
  in external mode with no writer, the write is refused with Part C's C.8 text and nothing is
  written:
  `error: wait: the surface's writer is not running: nothing written; for the Chief of Staff:
  start the surface server ($CHANTIER board --seat <session id>)`.
- **Into a batch:** `commands/joining.py`'s `join_cr`, the one join path of both `open` and
  `order add`, reads the CR folder's `waits.json` once the folder is in `4-batch/1-pending/`, puts
  its **open** waits in the new `CrEntry.waits` (a cleared wait is dropped there) and consumes the
  file with `b.consume(cdir / "waits.json")`, as it consumes `formerly.json` today: deleted when the
  record saves, kept when the join is refused. A malformed `waits.json` refuses the join (exit 2,
  `<cr>: waits.json is not valid: <what>; fix it or remove it, then open again`) and writes
  nothing.
- **Out of a batch** (`order drop` to the inbox or the backlog, `lifecycle/moveout.leave_batch`,
  where `formerly.json` is written): the CR's open waits are written to the folder's `waits.json`
  in the same move (`02-answers.md`, answer 3), through `repo.store` like the move itself; a CR
  with no open wait gets no file.

## 4. Commands

### 4.1 `handback <cr> blocked --wait <type>[=<ref>] <reason>`

`declare/driver.py`'s `handback` gains `--wait`, repeatable (argparse `action="append"`).

- Each `--wait` adds one open wait to the CR, in the same locked write as the hand-back
  (`commands/driver.py`, `_handback_locked` → `handback_blocked`).
- `<type>` is one of the four; any other: exit 2, `--wait: <type> is not a wait type: answer,
  approval, pipeline or merge`.
- `=<ref>`: `answer` requires it (exit 2 without: `--wait answer needs the question:
  --wait answer="<question>"`). `approval` and `merge` with none take the CR's recorded PR link;
  `pipeline` with none takes the CR's recorded head and its PR link, and `pipeline=<sha>` takes
  that sha and the recorded PR link. Nothing recorded to default from: exit 2, `--wait <type>:
  <cr> has no recorded PR` (or `no recorded head`), and nothing is written.
- A link (given or defaulted) is checked as `wait add` checks it (§4.2).
- `--wait` on a `ready` hand-back: exit 2, `--wait is for a blocked hand-back`, nothing written.
- The reason stays free text with today's prefixes (`question:`, `approval:`, `merge:`, ...,
  `waits:`): `--wait` adds typed waits beside any reason and changes no prefix's meaning; the
  free-text `blocked waits: <what>` (a thing already on its way that no one decides: the stack
  driver, another CR, a push) stays as today (`02-answers.md`, answer 4).
- `driver_checks.handback_args`' usage text names `--wait`.
- The printed hand-back line gains, when waits were added, `; waits: <type>[, <type>...]`.

### 4.2 `wait <cr> add <type> [--ref <ref>] --note "<text>"`

A new command in `declare/driver.py` (implemented in a new `commands/waits.py`). `--note` is
required (the reason, one line).

- **In a batch** (`<cr>` a CR id of the batch in `4-batch/`):
  - by the Driver (no `--epoch`; `--lease <n>` once Part D has landed, §2) or by the steering
    session (`--epoch <n>`, checked as every epoch command checks it). It records a wait without
    ending the Driver and without changing the CR's status.
  - `approval`, `pipeline`, `merge` with no `--ref`: the defaults of §4.1; none recorded: exit 2.
  - `answer` with no `--ref`: exit 2, `wait add answer needs --ref "<the question>"`.
- **On a backlog CR** (`<cr>` the CR's folder, as `summary` takes it; refused under `4-batch/`
  with exit 2 `<folder> is in the batch: name its CR id`): any session (the Chief of Staff, a
  Griller), with no `--epoch` and no `--lease` (either given: exit 2). `--ref` is required for
  every type (a backlog CR has no recorded PR): exit 2 without. For `pipeline`, `--ref` is the
  sha and `--link <link>` is required too (`--link` exists for `pipeline` only, in a batch it
  overrides the recorded PR). Written through `repo.store` (§3.2).
- **The link check** (every `approval`, `pipeline` and `merge` wait, in a batch or the backlog):
  - a link no connector claims (`connectors.connector_for(link)` is None): exit 2 with
    `connectors.UNCLAIMED`'s text, nothing written (AGENTS.md: no fallback);
  - in a batch, a link of another repository than the batch's recorded PRs (another `Place`):
    **recorded**, and the line printed says `w<n> <type>: <link> is not in the batch's repository:
    the hub does not read it; clear it by hand`. The hub's `waits` provider leaves it out of its
    interests (§5.2), so it never makes the project's read refuse with `NOT_ONE_REPOSITORY` and the
    one-query budget holds. A batch with no recorded PR yet: the first link's repository is
    compared again at every hub cycle (§5.2), never refused at `add`.
  - a `pipeline` sha is checked as a full hex sha (40 or 64 characters); `wait add` also accepts
    a 7-or-more prefix in a batch when it is a prefix of the recorded head, and stores the full
    one; anything else: exit 2.
- Prints `<cr> w<n> <type> added` (and the repository line above when it applies).

### 4.3 `wait <cr> clear <id>`

- In a batch: `--epoch <n>` required (the steering session only); without it, exit 2 `wait clear
  in a batch is the steering session's: wait <cr> clear <id> --epoch <n>`. Sets `cleared_at`
  (now) and `cleared_by` (`epoch <n>`).
- On a backlog CR: no `--epoch` (given: exit 2); `cleared_by` `hand`; written through
  `repo.store` (refused with no writer, §3.2).
- An id the CR does not have, or already cleared: exit 2, `<cr> has no open wait <id>`.
- Prints `<cr> <id> cleared`.

### 4.4 `wait [<cr>]`

Read-only (no epoch, no lease):

- `<cr> waits for: w1 answer since HH:MM: "<ref>"; w2 pipeline on <sha7> since HH:MM` (`approval`
  and `merge`: `w3 approval on <link> since HH:MM`), only open waits; an `approval` wait on a
  GitLab link while §5.3's proof is not recorded ends with ` (GitLab approval: cleared by hand
  until proved)`; a wait of another repository (§4.2) ends with ` (not in the batch's repository:
  cleared by hand)`. `HH:MM` in UTC, as the record. `<sha7>` is the sha cut to `SHA_SHOWN` (7).
- `<cr> waits for nothing` when it has none open.
- With no `<cr>`: one line per CR of the batch with an open wait (in the batch's CR order), then
  one per backlog CR with an open wait (folder path, in the stage order inbox, P1..P4, 3-ready);
  `nothing waits` when none.

### 4.5 `status`, `handoff`, and what a wait does not change

- `status` (`commands/batch_status.py`, `_cr_row`): a CR row with open waits gains
  ` | waits: <type>[, <type>...]` (the rows' existing separator; the queued CRs' `| waits for
  <deps>` is another thing and stays).
- `status` prints each `wait-cleared@1` line of the batch whose wait is still open, as it prints
  the `merged` lines (§6.2).
- `handoff` (`commands/facts.py`, `cr_facts`) prints, for a CR with open waits, the `wait <cr>`
  line of §4.4.
- A wait changes no rule: `take` (with or without `--note`), `close`, `open`, the slots, the
  dependencies and `order` read the CR's status as today. `take` clears no wait; a CR taken back
  with an open wait keeps showing it until it is cleared. A CR the record holds merged or
  cancelled keeps its waits in the record and the hub no longer reads them (§5.2).

## 5. The hub's part

### 5.1 The provider

New module `skills/chantier/scripts/cli/src/chantier/hub/waits.py`, provider `waits`, kinds
`{"pr"}`, added as one line to `PROVIDERS` in `hub/interests.py` (forge-connectors §4.1), after
`batch`.

- `collect(repo)`: when the batch in `4-batch/` is running (the `batch` provider's
  `running_batch` reading, an unreadable or absent record gives no interest): one `pr` interest
  per open `approval`, `pipeline` or `merge` wait of a CR the record does not hold merged or
  cancelled, whose `link` is claimed by a connector and is in the batch's repository (§5.2).
  `facts`: `{state, checks}`, plus `review` for `approval`. `by`: `<batch> <cr> <wait id>`. An
  `approval` wait on a GitLab link while §5.3's proof is not recorded gives no interest.
- `judge(repo, interests, facts)`: for each interest whose link was read, met when:
  - `merge`: `facts.state == "merged"`;
  - `pipeline`: `facts.head` equals the wait's `ref` and `facts.checks == "green"`;
  - `approval`: `facts.review == "approved"` (`unknown`, `required`, `changes-requested` and
    `unproved` are never met).

  Each met wait gives one `wait-cleared@1` event (§6). The journal's duplicate key (batch, CR,
  wait id) keeps it to one line however many cycles see it.
- It records nothing in the batch, writes no `hub` entry field (forge-connectors §3.3), runs no
  git, messages no agent.

### 5.2 The budget and the repository

The waits' links join the project's **one** `connectors.read` per cycle (forge-connectors §3.3,
step 3): no new query, no new cycle. A wait's link usually is a PR the `batch` provider already
reads; `pipeline` needs no extra field; `approval` adds `review` to the query only when an
`approval` interest exists.

`collect` leaves out a link whose `Place` differs from the batch's recorded PRs' `Place` (the
first recorded PR's, as `connectors.read` requires one). It is shown "not in the batch's
repository: cleared by hand" (§4.4) and never makes the project's read refuse with
`NOT_ONE_REPOSITORY`. With no recorded PR in the batch, a wait's link has nothing to compare to:
the provider uses the first wait link's `Place`, and leaves out the waits of any other.

Backlog CRs' waits are **not** read by the hub (E.7, `02-answers.md`, answer 1): they are cleared
by hand, and AGENTS.md's query budget does not change.

### 5.3 GitLab approval, unproved until read on a real MR (Q23)

Until both proofs below are recorded in this CR's evidence, `connectors/gitlab.py` keeps
answering `review: unproved` (forge-connectors §3.2), `collect` gives no interest for a GitLab
`approval` wait, and `wait` shows it `(GitLab approval: cleared by hand until proved)`. GitLab
`pipeline` and `merge` waits are read as on GitHub (their facts are those the hub already reads).

The proof (before the GitLab half of `approval` ships): one real `glab api graphql` read of a
merge request's approvals (`approved` of the MR, and `approvalsRequired`/`approvalsLeft` when the
plan has them) on a **Free** project and on a **Premium** project, each recorded in the CR's
evidence with the command, the project's plan, the MR's approval rule, and the answer's relevant
fields. When both answer as expected, the Driver:

- adds the field to `gitlab_query` only when `review` is asked (with none asked, the query text
  stays byte for byte today's), mapping `approved: true` → `approved`, `false` → `required`,
  absent or null → `unknown`;
- removes the `unproved` gate in `collect` and the `(GitLab approval: ...)` suffix;
- extends `scenario/fake_glab.py` and `tests/forge_world.py`'s GitLab answer with the field.

An answer other than expected on either plan: the GitLab half does not ship; the PR's Known gaps
names it ("GitLab approval read not proved on <plan>: <what it answered>") and the unproved
behaviour above stays. No fake forge stands for this proof. The proof needs a real GitLab
account on both plans: if the Driver has none, it hands back `blocked question:` naming what it
needs (it does not ship the GitLab half on a guess).

## 6. The journal type `wait-cleared@1`

### 6.1 Its `PUBLISHED` entry (`hub/schemas.py`)

| Field | Value |
| --- | --- |
| model | `batch` (string, `^batch-[0-9]+$`; the reference allows null for a backlog CR, which no writer emits since the hub reads no backlog wait (`02-answers.md`, answer 1): the model keeps `batch` nullable as the reference gives it), `cr` (`^CR-[0-9]+$`), `wait` (`^w[0-9]+$`), `wait_type` (`approval`, `pipeline` or `merge`), `ref` (string), `seen_at` (UTC time) |
| writer | the hub (`hub/waits.py`, through `journal.append(repo, events, "hub")`) |
| wakes a watcher | yes |
| text (`event_text`) | `forge saw <wait_type> met: <cr> <wait> (<ref, a sha cut to 7>); for the steering session: wait <cr> clear <wait> --epoch <n>, then take it back` (`<n>` printed as is: the steering session fills its own epoch) |
| duplicate key | (`batch`, `cr`, `wait`) |
| example payload | `{"batch": "batch-29", "cr": "CR-3", "wait": "w2", "wait_type": "pipeline", "ref": "3f1c9a0e5b7d2c4a6e8f0b1d3c5a7e9f1b3d5c7a", "seen_at": "2026-11-20T10:02:03Z"}` |

Then `just journal-schemas` writes its entry in the shipped `hub/schemas.json`; Part A's
`test_event_types.py` covers it with no change to the test.

### 6.2 Where it shows

- The watcher (`hub/lines.py`, `watch_lines`) wakes the Chief of Staff's session with its text, as
  for `merged@1`.
- `status`: `journal.lines` prints the batch's `wait-cleared@1` lines whose wait is still open in
  the record (cleared: no longer printed), beside the `merged` lines.

## 7. The board

### 7.1 Data

- `board/crs.py`, `_row`: a new field `open_waits`, the CR's open waits (`[{id, type, ref,
  link}]`), from `batch.json`. The existing `waits` field (a queued CR's dependencies, read by
  `web/js/model/semantics.js` as `c.waits`) keeps its name and meaning.
- `board/backlog.py`, `backlog_items`: the same `open_waits` field, from the folder's
  `waits.json` (absent: empty; malformed: empty, `validate` reports it).

### 7.2 Views

- Kanban (`web/js/views/kanban-cards.js`, `crCard`): a blocked CR with open waits shows
  `waits: <type>[, <type>...]` in the step span in place of "waits for the user"; with none, it
  keeps "waits for the user".
- The backlog card (`web/js/ui/item-card.js`): a CR with open waits shows `waits: <types>`.
- The words in `web/js/i18n/en.js` and `fr.js`, both.
- The Driver reads `board/web/DESIGN.md` first and keeps it true (AGENTS.md); when it puts
  `open_waits` on another view's card, that view's section of `docs/web-board.md` says it too.

### 7.3 The pane

`STATUS.json`'s fields that the CR board pane shows do not change (`status/words.phase_text`
stays "waits for the user" for a blocked CR): no pane change, so no screenshot owed (AGENTS.md).

## 8. AGENTS.md (chantier's own)

1. "The CLI's scope": after "a new CLI tool comes from measured token-costly behaviour, never
   from speculation", name `wait` as an exception: built on the user's answer of 2026-11-20
   ("tout", planning-server-Q9), a CR's typed waits (answer, approval, pipeline, merge). When
   Part D has landed with its `lease` sentence, `wait` joins that sentence (one list of the named
   exceptions, each citing the same answer).
2. The hub's sentence: "it appends to that project's `forge-journal.jsonl` (...) one line per
   merge the record does not hold and per CI turning red on a PR ready to merge" adds "and per
   wait of a running batch's CR that the forge shows met (`wait-cleared@1`)", "and nothing else"
   kept.
3. The budget sentence, as forge-connectors' §6.1 edit 1 leaves it: its "today" list adds "and
   the PRs or MRs that the open approval, pipeline and merge waits of the running batch's CRs
   name, in the same query". The query count does not change.
4. The write list needs no change: a backlog CR's `waits.json` is a file of the planning folder
   ("chantier writes only in the planning folder"), and `batch.json` already is.

## 9. Cards

Each change on both hosts' agent files only where the agent files carry it (the role's contract
is the card; `agents/` and `com.github.copilot/agents/` are unchanged unless the Driver finds a
sentence there these cards make false, then both together, bodies identical).

- `skills/chantier/references/driver.md`:
  - "Means: hand-backs out of the ordinary" (off the common path, read when it applies): when the
    block is a wait of one of the four types, block with `--wait <type>[=<ref>]` (the defaults of
    §4.1), and `wait <cr> add` for a wait that does not end the Driver; a `--wait` refused: hand
    back without it, naming the refusal in the reason.
  - "Means: your end" (common path): one pointer, at most ~120 bytes, beside the list of reasons:
    "a wait of a known type: `--wait`, see Means: hand-backs out of the ordinary". The 45,000-byte
    cap (`CR_DRIVER_COMMON_PATH_LIMIT` in `test_startup_manifest.py`) does not rise (driver-leases
    spec answer 2): the bytes are paid by tightening that section's existing text, dropping no
    rule. If Part D landed first and the room is gone, the pointer is dropped and the whole text
    stays off the common path.
- `skills/chantier/references/foreman.md` and `skills/chantier/references/chief-of-staff.md`:
  clear a wait (`wait <cr> clear <id> --epoch <n>`) on the user's answer or on a `wait-cleared@1`
  line, then take the CR back as today (`take <cr> --note "..."`). `status`'s `| waits:` and the
  `wait` command are how they see what a blocked CR waits for.
- `skills/chantier/references/chief-of-staff.md` and `skills/chantier/references/griller.md`: a
  backlog CR left waiting for the user's answer between two grills gets `wait <folder> add answer
  --ref "<the question>" --note "<why>"`, cleared (`wait <folder> clear <id>`) when the answer is
  recorded in `02-answers.md`.
- `skills/chantier/references/concepts.md`, "Words": the word **wait** (the four types, where a
  wait lives, that it changes no rule, never "gate").

## 10. Docs, diagrams and other text made false

### 10.1 Changed

- `docs/web-board.md`, "Kanban": "a blocked one 'waits for the user'" becomes: a blocked one shows
  its open waits (`waits: answer`, `waits: pipeline`, ...), "waits for the user" staying for a
  block with no typed wait; a backlog card with an open wait shows it too. Another view's section
  changes only if the Driver puts `open_waits` on that view's card.
- `docs/planning-folder.md`:
  - the CR folder paragraph ("A CR's folder may also hold `prototypes/NN-<idea>/` and
    `experiments/` ...") adds a backlog CR's `waits.json`: published, moves with the folder,
    carried into the batch's record at `open` or `order add` (open waits only) and removed there;
  - the `validate` paragraph adds the shape of a backlog CR's `waits.json`;
  - "The event journal": the `wait-cleared@1` row of Part A's types table (writer the hub, wakes a
    watcher).
- `skills/chantier/scripts/cli/scenario/README.md`: the new case's coverage bullet (§11.2).
- `docs/hosts.md`: if forge-connectors has put the `review` fact in its connector rows, the GitLab
  cell changes when §5.3's proof ships (and only then).

### 10.2 Searched and unaffected

- SVGs: none is made false. `docs/cr-lifecycle.svg` and `docs/cr-lifecycle-texts.md` ("⛔ blocked:
  question, approval, budget…" stays true: a block carries typed waits or none), its `<desc>`
  unchanged; `docs/batch-pace.svg` (its "CRs wait" are queued CRs) and its texts;
  `docs/cr-folder-lifecycle.svg`, `docs/cr-lifecycle-simple.svg`, `docs/batch-lifecycle.svg`
  ("waits for the next batch", "waits for its next ready CR": other waits) and their `-texts.md`;
  no SVG names the hub or the journal.
- `docs/boards.md`: the pane's "waits for the user" on a blocked CR stays (§7.3).
- `docs/gates.md`: keeps "gate" for the fast and long gates.
- `docs/use-cases-foreman.md`, `docs/use-cases-direct.md`, `README.md`: a blocked CR "parked as
  blocked with its question", "comes back as a question": still how the user hears it.
- `docs/web-board.md` Home's "Waiting for you" tile (the blocked CRs) and the Batch view's
  "waits" badge (queued dependencies): unchanged.

## 11. Evidence

### 11.1 Tests (`skills/chantier/scripts/cli/tests/`, in-process, parametrized)

- `tests/test_waits.py` (new), parametrized over the four types where it applies:
  - `handback blocked --wait` records each type (defaults from the recorded PR and head; `=<ref>`
    given); `--wait` on `ready` exits 2 and writes nothing; `--wait answer` with no question and a
    defaulted type with nothing recorded exit 2 and write nothing; an unknown type exits 2;
  - `wait add` in a batch with and without `--ref`, by the Driver and with `--epoch`; a link no
    connector claims exits 2 with `UNCLAIMED` and writes nothing; a link of another repository is
    recorded with its line;
  - `wait clear` with `--epoch` clears; without `--epoch` in a batch exits 2; an unknown or
    cleared id exits 2;
  - `wait <cr>` prints both forms; `wait` with no CR lists the batch's then the backlog's;
  - on a backlog CR: `wait add answer` writes `waits.json`, `wait clear` clears it, `--ref`
    missing exits 2; `open` (and `order add`) carries the open wait into `batch.json`, drops the
    cleared one and removes the file; a malformed `waits.json` refuses the join and leaves it;
  - a refusing `repo.store.check_publish` (Part B's seam, made to refuse in the test) refuses the
    backlog `wait add` and `wait clear` and nothing is written; once Part C has landed at the
    Driver's base, the same case runs in external mode with no writer and checks the C.8 text;
  - `order drop` to the inbox and to the backlog writes the open waits to `waits.json`, and a CR
    with none gets no file;
  - `status` shows `| waits: <types>` and a still-open `wait-cleared@1` line, not a cleared one;
    `handoff` prints the wait line; `take` of a CR with an open wait behaves as today (a wait
    changes no rule).
- `tests/test_validate.py`: a valid `waits.json` and a malformed one in a backlog CR (one
  parametrized case each); a `waits.json` under `4-batch/` reported as today's unknown file.
- `tests/test_forge_hub.py`, with the fake forge world (`tests/forge_world.py`), parametrized: on
  GitHub an approval, a green pipeline on the wait's head and a merge each give one
  `wait-cleared@1` line, never twice over two cycles; a red pipeline, a green pipeline on another
  head, and `review` `unknown` give none; on GitLab a green pipeline and a merge each give one
  line, an approval gives none and no `review` is asked (unproved); a wait link of another
  repository is not read and the project's read does not refuse; the waits add no query (one
  `connectors.read` per project and cycle, counted).
- Part A's `test_event_types.py` covers `wait-cleared@1` from `PUBLISHED` (no change to the test).
- `tests/test_board*.py`: `open_waits` on a batch row and a backlog item; the existing `waits`
  field unchanged.
- `tests/test_startup_manifest.py`: unchanged; it reads `driver.md` from the repository at the
  head under test and keeps the 45,000-byte cap, so it proves §9's common-path bytes.
- Budget: `just test` stays within AGENTS.md's limit (at most 30 s above 18.5 s); this CR's tests
  add about 2 s on the user's Windows machine, measured and stated in the PR.

### 11.2 Scenario (`skills/chantier/scripts/cli/scenario/run_scenario.py`)

- A case `typed_waits` in a GitHub unit other than `gates` (the long gate's unit). The reference
  lets the Driver pick the closest; recommended: `surface-board` (500 s), beside `forge_hub`, whose
  `SurfaceWorld` and short hub times (`CHANTIER_HUB_TEST_TIMES`) it reuses. A Driver blocks with
  `--wait pipeline`, the fake forge (`scenario/fake_gh.py`, `api graphql`) turns the head green,
  the journal holds one `wait-cleared@1`, the scripted Foreman clears the wait and takes the CR
  back.
- The same case in unit `gitlab` (95 s, measured 92.0 s): `scenario/fake_glab.py` gains the
  `api graphql` answer the hub reads (it has none today).
- Budgets: the README's rule (loaded `--jobs 4` time plus about 25%). Each case adds at most about
  20 s to its unit; the `gitlab` unit has 3 s of room, so its budget will likely rise: the Driver
  measures and updates the literal in `UNITS` and the README's table by that rule, never above
  what it measured plus 25%. The README's coverage bullet names `typed_waits`
  (`test_scenario_coverage.py` checks it names an existing case).
- The long gate (`just scenario (ubuntu-latest)`) passes at the PR's head (a CLI and cards
  change), `just check` and `just eval-dry-run` in the worktree before the first push (AGENTS.md).

### 11.3 Host and forge matrix

| Host | Forge | Case | Expected |
| --- | --- | --- | --- |
| Claude Code | any | `handback --wait`, `wait add`, `wait clear`, `wait` | same commands and lines (the CLI knows no host) |
| Copilot | any | the same | the same |
| any | GitHub | `approval` wait, review approved | one `wait-cleared@1` (after forge-connectors' `reviewDecision` proof) |
| any | GitHub | `approval` wait, review null | `unknown`, never met, no line |
| any | GitHub | `pipeline` wait, its head green | one line |
| any | GitHub | `merge` wait, merged | one line |
| any | GitLab | `approval` wait, proof not recorded | not read; `(GitLab approval: cleared by hand until proved)` |
| any | GitLab | `approval` wait, proof recorded on Free and Premium | read; one line on `approved: true` |
| any | GitLab | `pipeline` and `merge` waits | as on GitHub |
| any | another repository's link | any forge type | recorded, not read, "cleared by hand" |
| any | no connector claims the link | `wait add` | exit 2, `UNCLAIMED` |

### 11.4 Real reads

- The GitLab approval proof of §5.3 (Free and Premium), in the CR's evidence before the GitLab
  half ships.
- No other real read: GitHub's `reviewDecision` proof is forge-connectors' (its §3.2).

## 12. Rollout and out of scope

### 12.1 Rollout

- One PR, after `typed-journal-events`, `forge-connectors` and `plan-store-interface` are merged
  (`depends.json`); Part C may land before or after. `batch.json` gains a field with a default (an older record reads as no waits);
  `waits.json` is new (an older chantier reading a backlog CR ignores it, and `validate` of an
  older chantier reports it as an unknown file: the Driver checks and names it in the PR).
- An older watcher reading `wait-cleared@1` counts it and wakes no one (Part A's unknown types).
- The GitLab half of `approval` ships in the same PR only when its proof is recorded; else it
  stays a Known gap, and a later PR turns it on.

### 12.2 Out of scope

- The hub reading backlog CRs' waits (`02-answers.md`, answer 1).
- A wait clearing itself: the hub only signals (`wait-cleared@1`); the steering session clears.
- A wait changing a rule (`take`, `close`, `open`, slots, dependencies).
- Waits for an issue, a comment, a person on the forge, or anything other than the four types;
  issues are `outside-poller`'s.
- Leases (`--lease`, Part D) beyond the alignment of §2; access (Part F); outside contributions
  (Part G).
- The CR board pane and `STATUS.json` (§7.3).
- A "summary listings" command: the reference names one for the backlog, but `summary` only has
  `lint`, `set`, `label` and `group`; `wait` with no CR (§4.4) and the board's backlog cards
  (§7) are where a backlog CR's open waits show.

## 13. Open questions for the user

None: the first version's four are settled in this CR's `02-answers.md` (§2).
