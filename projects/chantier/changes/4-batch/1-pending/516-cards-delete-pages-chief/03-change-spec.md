# Delete the Chief of Staff side's dead help pages, rules moved first

## Goal

The owner's words (2026-11-27): « ouvre un batch et lance ces 7 CR », and card-cleanup-Q1:
« A. Tout, règles replacées (recommandé) ». This CR deletes the 33 help pages of the Chief of
Staff side that the Fable review marked for deletion, all of them, now (git keeps them). Before a
page goes, every rule in it that protects the user is put in a place that stays: a role card, a
page that is kept, the floor, or a CLI refusal that already exists. Every pointer to a deleted page
or topic name is fixed, so that no card, page, CLI string, test, doc or eval link names something
`help` no longer knows.

It is step 1, first half, of the card cleanup plan (plan section 6, item 1). The plan and the
verdicts are proposals: this specification checked their claims against main at `4d12a5b`, and the
Driver checks them again at its base (see "Before starting").

## Before starting (the base)

- `depends.json` puts this CR after `cards-inventory-last-reading`. At the base, these are gone:
  `docs/proofs/cards-inventory.md`, `docs/proofs/cards-inventory-open.tsv`,
  `skills/chantier/scripts/cli/tests/test_cards_inventory.py` and `cards_inventory.py`. If they are
  still there, stop and tell the steering session: that CR is not merged under this one.
- That CR may have added sentences to pages, possibly to one of the 33 pages below, and may have
  changed `test_card_homes.py` and the figures of `test_brief_bytes.py`. Read each of the 33 pages
  at the base, not this specification's copy. A sentence it added to a page this CR deletes is
  judged like the others below (protective: it moves; else it goes) and named in the PR.
- That CR adds `docs/protective-rules.md`, one line per protective rule with its home (plan
  section 5 and verdicts section D). If it is not at the base, stop and tell the steering session.
  The PR's table (below) cites its lines by their own words.
- `cards-delete-pages-crew` is the sibling CR in the same stack, also after
  `cards-inventory-last-reading`; it adds lines to `chief-of-staff.md` (among them the
  `host-for-you` line: where, do, paste, expect, and "I have not tested this path") and possibly to
  `foreman.md`. That line is that CR's, not this one's. Whichever of the two lands second sees both
  CRs' additions in the byte check of part 4 ("Byte ceilings").

## What changes

### 1. The 33 pages deleted

All in `skills/chantier/references/topics/`:

- session, seat, board, watcher: `board-lines`, `board-p2`, `compacting-p1`, `compacting-p2`,
  `cost`, `first-turn-p2`, `options`, `pr-template-own`, `session-start-surface-p2`,
  `sync-offer-p1`, `sync-offer-p2`, `watcher-board-p2`, `watcher-events-p2`, `watcher-lines-p1`
- starting a batch: `allow-rules-more-p2`, `config-p2`, `foreman-start-more`,
  `forge-permissions-gitlab`
- ending a batch: `batch-close-p2`, `batch-close-stopped-p2`, `demo-p2`, `retro-lines`
- grill and tickets: `grill-example`, `grill-specify-p2`, `griller-cost`, `ticket-summary-post-p1`
- merge and asks: `asks`, `ready-asks`
- steering: `orders-queue`, `qa-order`, `wakes-p1`
- refused push: `refused-forge-chain`, `refused-push-chief-more-p2`

### 2. `references/topics.json`

- Sixteen topic names lose their only reading and are removed: `asks`, `board-lines`,
  `compacting`, `cost`, `foreman-start-more`, `forge-permissions-gitlab`, `grill-example`,
  `griller-cost`, `options`, `orders-queue`, `pr-template-own`, `qa-order`, `ready-asks`,
  `refused-forge-chain`, `retro-lines`, `sync-offer`.
- Twenty-one topics keep their other readings and only lose the deleted page's: `allow-rules-more`,
  `batch-close`, `batch-close-stopped`, `batch-end`, `batch-start`, `board`, `config`, `demo`,
  `first-turn`, `grill`, `grill-specify`, `orders`, `refused-push-chief-more`, `retro`,
  `session-start-surface`, `steering`, `ticket-summary-post`, `wakes`, `watcher-board`,
  `watcher-events`, `watcher-lines`. Their triggers, roles and `review_by` stay as they are.
- The aggregate names stay (another CR, `cards-delete-aggregate-topics`, removes them). No `-pN`
  set is joined and no remaining page is renamed (`cards-one-page-per-theme`).

The counts are those of `4d12a5b` (240 topics before, 224 after); the Driver recounts at its base.

### 3. The protective rules and where each lives afterwards

Each line names the page, the rule, and its home after this CR. "Moved" means this CR writes the
sentence into that file, in its smallest form, in English, without rewording the kept file's other
text (one exception: part 4, "Byte ceilings"). "Held" means the home already says it at `4d12a5b`;
the Driver checks it still does.

| deleted page | protective rule | home afterwards |
|---|---|---|
| `asks` | `asks --read all` never clears the list: an ask stays unread until the user has heard it or it was acted on | moved: one sentence in `chief-of-staff.md`, beside "Progress and Completion reports" (part 4) |
| `asks` | a refused send between sessions is reported, never sent another way | held: floor 9 |
| `refused-forge-chain`, `refused-push-chief-more-p2` | a refused push, rebase or forge command: once, unchanged, never `--force`, never another form, never a change to the permission settings | moved: joins the "Rail:" sentence of `chief-of-staff.md` ("…`--force-with-lease`, never `--force`") |
| `refused-forge-chain` | a refused `gh pr ready` / `gh pr edit --base` only on a PR the record holds for a CR of this batch; a second refusal reported with its exact text | held: `chief-of-staff.md` "Settles alone" item 3; floor 9 |
| `refused-push-chief-more-p2` | on the yes run it once, unchanged; refused again: exact text and command to the user, no second try | held: `chief-of-staff.md` "Settles alone" ("A host refusing your run: … run it once on the yes"); `refused-push-chief-more-p1` |
| `board-lines`, `board-p2` | the board is never stopped by the agent but by `serve --restart` on a yes; another session's board is the user's to stop; never restarted on another port; a refused restart's stop command is printed, never run | held: `chief-of-staff.md` Never ("Restart the board on another port…; a board another session serves is the user's to stop"), Asks first 2, floor 10, `board-restart` ("A refusal: one line with the printed stop command, never run by you") |
| `board-lines` | a board's announced link is no readiness proof (only a successful probe is); the board never blocks a session, a preflight, a batch or a report; each `board` line passed on once, as printed | moved: one bullet at the end of `topics/board-p1.md` |
| `board-lines` | LAN reach is untested | held: `chief-of-staff.md` Never ("…as fact what the host marks unproved") |
| `sync-offer-p1`, `sync-offer-p2`, `session-start-surface-p2` | a sync never stops or kills a process but this session's own board and watcher, on the user's yes, by the host's stop of their background task, never by PID; a `webui` server is named with its stop command for the user to run by hand; any other holder is waited on | moved: the last paragraph of `sync-checkout.md` (part 4); also held: `chief-of-staff.md` Asks first 2, floor 10 |
| `sync-offer-p1`, `sync-offer-p2` | the offer's conditions and limits: no offer while another holder is listed or a gate runs (listed, or shown by `$CHANTIER status`); no third line; on the yes the board and the watcher start again whatever the result, the yes covering the restart; no answer leaves the offer standing; the cost said first in two parts (off for every project unless another session's watcher takes the hub; off a planning surface there is no writer) | moved: the same paragraph of `sync-checkout.md` (part 4) |
| `watcher-board-p2` | "rescan" decides nothing: still ask before opening a batch | held: floor 7 |
| `watcher-events-p2` | a config, tracker, pull or other-session line: tell the user, act on nothing; a `batch.slots` change is offered as `order slots`, nothing sent before the user's word | moved: one bullet at the end of `topics/watcher-events-p1.md` |
| `ticket-summary-post-p1` | publish only on the yes, by the Chief of Staff only, every text from its file, never typed in a shell; a refused or failed post: exact text, stop, nothing retried another way; an artifact that fails: no comment; read back what is visible to whom; the post recorded under the yes | moved: steps 7 to 9, condensed, at the top of `topics/ticket-summary-post-p2.md` (part 4) |
| `demo-p2` | a demo fixture is prepared outside the repository's tracked files and removed at the end | moved: one sentence in `topics/demo-p1.md`'s "The study" bullet |
| `demo-p2` | a problem found in the demo is the user's decision (`order note <cr>`, a round of fixes, or the inbox) | moved: one sentence at the end of `topics/demo-p1.md` |
| `demo-p2` | the Chief of Staff's subagent never commits, pushes or writes in a CR worktree | held: `topics/demo-p1.md` ("It never starts an implementation: …") |
| `allow-rules-more-p2` | a settings file P10 reports `unreadable: ...` is not written; a refused settings edit: exact text, no other file, tool or retry | moved: one bullet at the end of `topics/allow-rules-more-p1.md`; also held: floor 9, `topics/allow-rules` ("Nothing else is written in any settings file") |
| `config-p2` | an invalid configuration layer is shown to the user, never fixed by the agent | held: `chief-of-staff.md` Asks first 1 ("project file writes"), `topics/config-p1.md` ("you edit a file … only on the user's word") |
| `config-p2` | a role started generic runs with the caller's tools, not restricted | held: `playbook`'s own output (`(the caller's, not restricted)`, `playbook/lines.py`) |
| `orders-queue` | a cancelled dependency never frees its CR | held: `take`'s refusal (`rails.py`, `waits_for`: "a cancelled one stays unmet"), `topics/chain.md` |
| `orders-queue` | a queued CR that `status` shows `waits for …` is not started | held: `take`'s refusal (`<cr> waits for …: it starts once each is …`) |
| `orders-queue` | start every CR `take` would accept, up to the free slots, none held in reserve | moved: `foreman.md`, "You own", the "Starting Drivers" item (part 4) |
| `wakes-p1` | the Foreman starts its own watcher with the command its `watch: not running` line prints, as is; never copies a `watch:` line into a Driver's prompt; arms no heartbeat while the batch is paused with no CR | moved: `foreman.md`, "You own", the "Starting Drivers" and "Heartbeat and watcher" items (part 4) |
| `retro-lines` | never rewrite an earlier retro section | moved: joins the "Append to `4-batch/retro.md` a section…" sentence of `topics/retro.md` |
| `retro-lines` | which problems go in the retro; a refused command's line format; one untagged line when there is none | moved: three short sentences in `topics/retro.md` (part 4) |
| `batch-close-p2` | `close --yes` only on the yes; a refusal reported, not retried in a loop | held: `chief-of-staff.md` Asks first 4, floor 9 |
| `batch-close-p2` | on a CR still held at the end, offer to wait or send it out, and act on the answer only; a held agent that still runs: wait for its hand-back, never a timer | moved: one bullet at the end of `topics/batch-close-p1.md` (part 4) |
| `batch-close-stopped-p2` | a trashed CR returns to the inbox only on the user's word | held: `chief-of-staff.md` Never ("`abandon`, `restore` … but on the user's word") |
| `pr-template-own` | the user's own PR template is a CR delivered by a Driver's PR, never written in the main checkout by the Chief of Staff | held: `pr-template.md` "A customised version"; the card's Rare-cases list links that section (part 4) |
| `foreman-start-more` | a Foreman in a worktree: no way around suggested | held: floor 9, `foreman.md` Start (the `blocked` ask, then stop) |
| `foreman-start-more` | a workaround the user allows for one batch is passed to the Foreman in their words and never made a rule | moved: one sentence in `topics/foreman-start-p2.md`, step 4 (part 4) |
| `griller-cost`, `grill-specify-p2` | the Griller's and the specification agents' cost is in no batch | held: `griller.md` and `griller-skill.md` ("Your cost is in no batch"), `status-layout.md` "Cost" |
| `grill-specify-p2` | a CR marked for the running batch gets no `triage`; `specified` is sent once, a refused send reported | held: `griller-skill.md` "Ending" |

The other pages hold no protective rule: `compacting-p1`, `compacting-p2` (tips and compaction
advice), `cost` (a pointer to `status-layout.md`), `first-turn-p2` (the introduction continued),
`options` (where the user can act from; "no look-alike" is floor 3), `watcher-lines-p1` (the lines
say their command; a seat take is the card's Never), `forge-permissions-gitlab` (all unproved),
`grill-example` (a worked example), `ready-asks` (the CLI prints `superseded by A-<k> (marked
read)`), `qa-order` (`foreman.md` "Starting Drivers" covers `order qa`'s `brief:`). The rest of
`wakes-p1` (stop the watcher by its id on a switch to direct mode: `foreman.md` "Stop stray
background tasks by id"), of `orders-queue` (the born-paused batch's `ready` reply: `foreman.md`
Start; an added CR sets a paused batch running: the CLI's `take`), of `retro-lines` (a release's
retro named, not copied; the routes: `retro-route`) and of `foreman-start-more` (the reuse of a
stopped Foreman session; arming the heartbeat on `ready`) is held there or goes. Losing their
non-protective text (tips, compaction advice, the reuse of a stopped Foreman session, the GitLab P9
probes, the posting commands per forge) is the owner's choice in card-cleanup-Q1.

The PR carries this table, updated to what the Driver found at its base: for each protective
statement of a deleted page, where it lives afterwards. A page found to hold something still needed
that this table does not list: move it to its home and say so in the PR.

### 3b. `docs/protective-rules.md`

Each line of `docs/protective-rules.md` (added by `cards-inventory-last-reading`) whose home is one
of the 33 deleted pages is updated, in this CR's PR, with the rule's new home from the table above
(the card, kept page, floor item or CLI refusal). No other line of that file changes, and no line is
removed: a rule whose page goes keeps its line, with its new home. A line the table does not cover
gets its home found and moved the same way, and is added to the PR's table. After this CR, no line
of that file names a deleted page.

### 4. The moved text and the pointer fixes, file by file

Where a sentence is given below, it is the meaning to keep; the Driver may tighten the wording, not
widen or drop a rule.

`skills/chantier/references/chief-of-staff.md`
- Line 5: drop `help refused-forge-chain` from the parenthesis.
- The "Rail:" sentence: "never `--force`" becomes "never `--force`, another form or a change to the
  permission settings".
- After "Progress and Completion reports keep …": "Mark an ask read (`asks --read A-<k>`) once the
  user has heard it or you acted on it; `--read all` never clears the list."
- Rare cases: remove `options`, `compacting`, `asks`, `cost`; replace `pr-template-own` with a link
  to [pr-template](pr-template.md), "A customised version" (the user's own PR template).
- The `host-for-you` line is `cards-delete-pages-crew`'s; this CR does not add it.

`skills/chantier/references/foreman.md`, "You own" (`orders-queue` and `wakes-p1`), one short
addition per rule, folded into the existing items:
- "Starting Drivers: … then `agents set`; fill free slots." gains: never a `watch:` line in a
  Driver's prompt; and "fill free slots" becomes: start every CR `take` would accept, up to the free
  slots.
- "Heartbeat and watcher, `next --epoch <n>` per wake." gains: the watcher started with the command
  your `watch: not running` line prints, as is; no heartbeat while the batch is paused with no CR.

Byte ceilings. `test_brief_bytes.py` measures each role's whole brief (card, floor, facts, host
rows). At `4d12a5b` the measures are `chief-of-staff` 24,351 of 24,400 (49 bytes free) and
`foreman` 22,554 of 22,600 (46 bytes free); `cards-inventory-last-reading` may change both before
this CR's base. The additions above do not fit that room as plain additions (about 150 bytes net on
`chief-of-staff.md`, about 100 on `foreman.md`). The ceilings are not raised: the Driver first fits each
addition by tightening the wording of the line that receives it (the "Rail:" sentence, the
"Progress and Completion reports" line, the Rare-cases list; the "Starting Drivers" and "Heartbeat
and watcher" items), no rule of those lines dropped, and quotes the before and after measures in the
PR. The check at this CR's head counts both this CR's and `cards-delete-pages-crew`'s additions when
that CR is below this one; when this CR is below, the crew CR's Driver counts them. If tightening
the receiving lines is not enough, the Driver tightens other lines of the same two cards, no rule
dropped. Only if that fails too, it moves the Foreman's four added rules (part 3, `orders-queue` and
`wakes-p1`) out of `foreman.md` into a kept page the Foreman reads, and the PR's table names that
page as their home. The ceilings are never raised (the Chief of Staff's call, 2026-11-27).

`skills/chantier/references/griller-skill.md`: drop "(`help griller-cost`)" after "Your cost is in
no batch".

`skills/chantier/references/status-layout.md`, "Tips": drop the last sentence "The full rule:
`help compacting`." The tip rule above it stays as it is.

`skills/chantier/references/sync-checkout.md`: the last paragraph's "Pending 3 minutes after the
first try: `help sync-offer`." becomes the rule, in one short paragraph (or two), holding at least,
with the quoted phrases kept word for word (the tests pin them):
- pending 3 minutes after the first try (a turn, not a timer), tell the user once, naming the
  holders (in a batch, the report's **For you** item; else one chat line); a server `webui` started
  is named with its stop command (`taskkill /PID <n> /T /F` on Windows, `kill <n>` elsewhere), for
  the user to run by hand;
- "stop none but your own board and watcher, on the user's yes": when every holder listed is this
  session's "own board or watcher" (own board: its command line holds "`--seat <this session's id>`"
  and this session's `serve --seat` did not print "`board already running`"; own watcher: this
  session's `watch` of this project while it holds the seat; "Anything else is not own."), offer
  once to "stop them on the user's yes", the cost said first: the board, the writer and the hub are
  off for every project meanwhile, "unless another session's watcher takes the hub"; off a planning
  surface there is no writer (name the board and the hub only);
- no offer while another holder is listed or a gate runs (listed, or shown by `$CHANTIER status`);
  "no third line": a holder or gate appearing after the offer is not told;
- on the yes stop them by the host's stop of their background task, never by PID, sync only if no
  holder is left, then start the board and the watcher again whatever the result: "the yes covers
  the restart"; a holder still listed is waited on, never stopped;
- no answer: the offer stands; after a no, do not ask again.
The sentence on an ordinary sync failure stays.

`skills/chantier/references/topics/board-p1.md`:
- The bullet "A watcher's board stops by itself …" loses its second sentence ("To stop it sooner,
  on the user's word only, run the stop command with the PID … (`taskkill /PID <pid> /T /F` on
  Windows, else `kill <pid>`)."), which contradicts the card's "never by name, pattern or PID"
  (Asks first 2, floor 10). The first sentence stays; stopping the board sooner is `serve --restart`
  on the user's yes (`board-restart`) or the user's own act.
- Add one bullet: pass each `board` line on once, as printed; an announced link is no readiness
  proof (only a successful probe such as `GET /api/board` is); the board never blocks a session, a
  preflight, a batch or a report.

`skills/chantier/references/topics/watcher-events-p1.md`: add one bullet: any other line (a config
change, `tracker saw`, `surface pull brought`, `another session wrote`): one line to the user, act
on nothing (the CR is not claimed, moved or grilled); a `batch.slots` change is offered as
`order slots --note <new>` for the running batch, sent only on the user's word.

`skills/chantier/references/topics/ticket-summary-post-p2.md`: steps 7 to 9 at the top, condensed,
naming no forge tool: 7. publish on the yes only, by the Chief of Staff only, every text from its
file, never typed in a shell; the tracker's issue artifacts, else attachments, else a collapsed
section of the comment; a refused or failed post: the exact text to the user and stop, the texts
kept in `work/`, nothing retried another way; an artifact that fails: the comment is not posted.
8. Read back the comment and the artifacts; say what is visible and to whom. 9. Record under the yes
in `02-answers.md`: `Posted on <ticket link>, <date>: comment <url>; plan <ref>; demo <ref or
none>`. The page's "steps 7 to 9" and `ticket-summary-p2.md`'s "`help ticket-summary-post` for 7 to
9" then still point at these steps.

`skills/chantier/references/topics/demo-p1.md`: "The study" bullet adds "Prepare any fixture
outside the repository's tracked files and remove it at the end."; a last line adds "A problem the
demo finds is the user's decision: `order note <cr>`, a round of fixes, or the inbox."

`skills/chantier/references/topics/batch-close-p1.md`: add one bullet: a CR still held at the end:
offer to wait or to send it out (`order drop <cr> --note trash|ready|P1..P4`), and act on the answer
only; a held agent that still runs: wait for its hand-back, never a timer.

`skills/chantier/references/topics/foreman-start-p2.md`: step 4 drops "More: `help
foreman-start-more`." and adds "A workaround the user allows for one batch (a Foreman in a
worktree, for instance) is passed to the Foreman in their words, never made a rule."

`skills/chantier/references/topics/allow-rules-more-p1.md`: add one bullet: a refused edit of the
settings: the exact text (floor 9), no other file, tool or retry; a settings file P10 reports
`unreadable: ...`: do not write it; the user fixes it first.

`skills/chantier/references/topics/retro.md`: the append sentence gains "never rewrite an earlier
one"; the last line "The problems to list and the rules of the section: `help retro-lines`." is
replaced by three short sentences:
- A problem is an ask, a block, a refusal, a restarted Driver, a red gate or CI, a round past the
  first, cache expiries or a cost far over the others, an infrastructure failure, or a command the
  host refused (read `status --notes`, `events.jsonl`, the CRs' `work/` notes and `cost --explain`).
- A refused command is one line per distinct command: ``- [chantier] refused `<command>`
  (<capability>): <the row or rule to fix>``.
- A batch with no problem gets one untagged line saying so.

`skills/chantier/references/topics/direct-mode-accept-p2.md`: "(`help retro-lines`, `help
retro-critic`)" becomes "(`help retro`, `help retro-critic`)".

`skills/chantier/references/topics/ask-lines.md`: "ready asks are (`help ready-asks`)" becomes
"ready asks are (the CLI prints `superseded by A-<k>`)".

`skills/chantier/references/topics/orders.md`: the last line keeps only "The Chief of Staff's:
`help order-verbs`." (or its equivalent wording), without `help orders-queue`.

`skills/chantier/references/topics/forge-permissions-p2.md`: "GitLab: `help
forge-permissions-gitlab`." becomes "GitLab: no probe is written; say the forge permissions were not
checked." The pointer to `forge-permissions-say` stays.

`skills/chantier/references/topics/grill-series.md`: drop "; `help grill-example`".

`skills/chantier/references/topics/main-checkout-p1.md`: "(an eval or a worktree session: `help
options`)" becomes "(an eval running, or a session on a worktree)".

`evals/ticket-summary/RUNBOOK.md`: the `ticket-summary-post` link points at
`topics/ticket-summary-post-p2.md`; "the first trial of the topic's unproved GitHub lines (`gh issue
artifact`, a comment from a file)" becomes "the first trial of posting an issue artifact and a
comment from a file" (the topic no longer names those commands).

Any other pointer the Driver finds at its base (a card, a page, a host row in
`references/hosts/*.json`, a CLI string under `skills/chantier/scripts/cli/src/`, `hooks/`, `docs/`,
`evals/`, `README.md`) to one of the 33 files or the 16 names is fixed the same way: the pointer
goes, or names the kept page that now holds the rule. At `4d12a5b` the CLI's source names none of
them (`test_every_topic_a_line_names_exists` reads it). The Copilot host row "Name no compacting
command or setting to the user." stays: it is a host fact, not a pointer.

### 5. Tests

All read the shipped files at the head under test.

- `skills/chantier/scripts/cli/tests/test_card_homes.py` (as left by `cards-inventory-last-reading`):
  remove `compacting` and `options` from `test_role_cards_split`'s topics, `board-lines` and
  `sync-offer` from `test_session_start_split`'s and `test_launch_modes`'s; their rules' homes
  (`card chief-of-staff.md`, `card sync-checkout.md`, `topic board`, `topic board-restart`) are
  listed or added there.
- `test_command_names.py`, `test_the_blocked_sync_steps_name_the_serve_holder_and_its_stop`: the
  `taskkill /PID <n> /T /F` and `kill <n>` assertion reads `sync-checkout.md`.
- `test_launch_modes.py`:
  - `test_the_four_skills_hold_the_checked_sync_that_waits_and_never_kills` reads
    `topics/sync-offer-p1.md` and `-p2.md` as `offer`: `offer` becomes `_flat(refs /
    "sync-checkout.md")`, and every phrase of `SYNC_OFFER_PHRASES` ("stop them on the user's yes",
    "own board or watcher", "Anything else is not own.", "unless another session's watcher takes the
    hub", "no third line", "the yes covers the restart") is kept in the rewritten paragraph of
    `sync-checkout.md` (part 4), so the tuple does not change.
  - `test_the_cards_and_hosts_state_the_exception_the_row_and_the_for_you_item`: its "own board"
    assertion (`` `--seat <this session's id>` `` and `` `board already running` ``) reads
    `sync-checkout.md` instead of `topics/sync-offer-p1.md`; its "stop none but your own board and
    watcher, on the user's yes" assertion reads `sync-checkout.md` instead of
    `topics/session-start-surface-p2.md`.
  - the dev-mode test drops its `session-start-surface-p2.md` assertion (the other four files still
    state the rule).
- `test_event_audience.py`: `test_the_watcher_topic_states_the_end_rule_in_one_line` and its
  `EVENTS_TOPIC` constant go: they pin a sentence of a deleted page; the watcher's timing is said by
  its own output and by `AGENTS.md`.
- `test_brief_bytes.py`: its figures do not change; it passes at the head (part 4, "Byte
  ceilings").
- New, in `test_help_topics.py`: every `help <name>` pointer in the shipped references
  (`skills/chantier/references/**/*.md`, the skills' `SKILL.md`), including each name of the
  Chief of Staff card's "Rare cases:" list, names a topic of `topics.json`; a failure names the file,
  line and name. It passes at `4d12a5b` (checked) and at this CR's head, and stops a later deletion
  from leaving a dead pointer. Kept fast and in-process, as the other tests of that file.

## Out of scope

- The pages of the Foreman, Driver and host side (`cards-delete-pages-crew`), its `host-for-you`
  line in `chief-of-staff.md`, the aggregate topic names (`cards-delete-aggregate-topics`), joining
  `-pN` sets (`cards-one-page-per-theme`).
- Rewording any kept card or page beyond the sentences named above (and the tightening part 4's
  "Byte ceilings" allows); new CLI behaviour (a rule that would need it stays a card line, for a
  later step); a change to the floor; raising a `test_brief_bytes.py` figure.
- The other contradictions the verdicts list in kept pages (only `board-p1`'s stop by PID is fixed
  here, on the Chief of Staff's call).
- The version bump (`release-card-cleanup`) and the moment the batch lands relative to the other
  project's open batch, which reads the cards live (card-cleanup-Q5): the steering session's and the
  user's call at merge time.

## Evidence

- The diff is the 33 deletions, the `topics.json` entries, the pointer fixes, the moved sentences,
  the `board-p1` sentence removed, the updated lines of `docs/protective-rules.md` and the tests:
  nothing else.
- `chantier help` lists none of the 16 removed names and no topic reads a deleted file;
  `chantier help sync-offer` (and each of the 16) answers `no topic …`. The PR quotes `help`'s first
  line before and after (topic count).
- The new pointer test passes; `grep` for each of the 33 file names and 16 names over the repository
  (outside git history) finds none, quoted in the PR.
- `grep -n "PID" skills/chantier/references/topics/board-p1.md` finds no stop command.
- The PR's table of protective rules (part 3), checked at the base, each home quoted.
- No line of `docs/protective-rules.md` names one of the 33 deleted pages; each line this CR
  changed names a home that exists at the PR's head and holds the rule (the PR quotes it).
  If `test_card_homes.py` or another test at the base reads that file, it passes.
- `test_brief_bytes.py`'s printed `brief-bytes role=chief-of-staff` and `role=foreman` lines before
  (at the base) and after (at the head), quoted in the PR, each at or under its unchanged figure.
- `just check` passes. The cards change, so the pipeline's `just scenario (ubuntu-latest)` job is
  green at the PR's head; in this stack batch the local Windows `scenario` run is owed only by the
  CR on top of the stack (AGENTS.md).

## Questions for the Chief of Staff

None: the byte-ceiling question was answered (part 4, "Byte ceilings").
