# Delete the help topics that only print other topics' pages again

## Goal

The owner's words (2026-11-27): « ouvre un batch et lance ces 7 CR », with the cleanup plan's
answers, and behind them: « il faut mettre dans une carte un theme. et surtout avec un nombre de
carte important il faut orgnaiser le progressive disclosure efficacement ». This CR is step 1,
second item, of the card cleanup plan (plan section 6, item 2): fewer `help` names. Only names
that hold a text of their own stay. A name that only prints other topics' pages again is removed,
and every card, page, CLI string, doc and test that names it points at the page that fits. Nothing
points at a removed name afterwards, and a test keeps it so.

The plan and its verdicts are proposals. This specification checked their facts against main at
`4d12a5b` and recounted at the base this CR gets (below). The Driver counts again at its base.

## Before starting (the base)

- `depends.json` puts this CR after `cards-delete-pages-chief` and `cards-delete-pages-crew`, both
  after `cards-inventory-last-reading`. At the base, the 33 pages of the first and the 29 pages of
  the second are gone, with their 16 and 22 topic names, and `docs/protective-rules.md` exists. If
  one of these is not so, stop and tell the steering session: a CR below is not merged under this
  one.
- `cards-delete-pages-crew` keeps three host pages for a later step (`topics/host-claude-only.md`,
  `topics/host-compact-copilot.md`, `topics/host-sessions-copilot.md`) and keeps every host map
  with its two keys. This CR does not touch them.
- Every file and line named below is read again at the base before it is edited. The line numbers
  are those of `4d12a5b`.

## What "only prints other topics' pages again" means

A topic is removed when every reading it prints is printed by the other topics whose readings are
a strict subset of its own: it adds no text. This is checked on `topics.json` as it stands at the
base, not taken from the verdicts.

The verdicts (section C) mark 67 names "aggregate" at `4d12a5b`. That kind counts every topic with
more than one reading that is not a `-pN` set, so it also holds:

- the host maps (27 at `4d12a5b`, 12 at the base): one page per host, each its own text;
- two-page topics whose pages no other topic prints (`lease`, for instance);
- topics with a page of their own plus pages another topic also prints (24 at the base, among
  them `refused-push` and `stack`).

All of these hold a text of their own and stay as names.

Counted on `topics.json`: 240 topics at `4d12a5b`; 202 at the base (240 less the 16 and 22 names
the two CRs below remove). At the base, 10 topics add no text. Nine of them already do at
`4d12a5b`. The tenth is `stack-run`, whose own page `cards-delete-pages-crew` deletes; that CR keeps
the name only because this CR decides it.

## What changes

All paths are under `skills/chantier/references/` unless they start with `docs/` or
`skills/chantier/scripts/`.

### 1. `topics.json`: ten topics removed

Each line gives the topic, its roles, and the topics that print all its pages (each of them keeps
every role of the removed topic: checked at `4d12a5b`, checked again at the base).

| removed topic | roles | its pages are printed by |
|---|---|---|
| `trouble` | cr-driver, stack-driver, release-driver | `trouble-worker`, `trouble-remote`, `trouble-gate`, `trouble-git` |
| `release` | foreman, chief-of-staff | `release-take`, `release-tag` (which prints `release-stale` too) |
| `stack-run` | foreman, chief-of-staff | `stack-asks`, `stack-ends`, `stack-drop` |
| `grill` | chief-of-staff, griller | `grill-series`, `grill-options`, `grill-backlog`, `grill-restate`, `grill-specify`, `grill-critic`, `grill-critic-steps`, `where-cr-goes`, `writer` |
| `batch-start` | chief-of-staff | `trials`, `batch-plan`, `batch-plan-show`, `batch-plan-mode`, `batch-plan-cut`, `foreman-start` |
| `steering` | chief-of-staff | `steering-reports`, `order-verbs`, `order-drop`, `driver-question`, `chain-conflict`, `rounds-exception`, `watcher-events`, `watcher-lines`, `refused-push-chief`, `refused-push-chief-more`, `refused-rebase-chief`, `refused-answer`, `refused-push-judgement`, `refused-push-route`, `refused-rebase` |
| `ready-to-merge` | chief-of-staff | `merge-words`, `merge-gaps`, `merge-recorded`, `merge-series-stack`, `merge-stack-ready`, `stack-changes-chief` |
| `batch-end` | chief-of-staff | `batch-pause`, `retro-route`, `retro-route-chantier`, `batch-close`, `batch-close-stopped`, `recovery` |
| `direct` | chief-of-staff | `direct-mode` (which prints `direct-mode-switch` too), `direct-mode-epoch`, `direct-mode-accept` |
| `release-procedure` | chief-of-staff | `release-chief`, `release-chief-approve`, `release-chief-auto`, `release-chief-after` |

No page file is deleted and no page text moves: each removed topic's pages stay, printed by the
topics in the table. A topic found at the base that also adds no text, and is not in this table,
is removed the same way and named in the PR. A topic of this table that holds a text of its own at
the base stays, and the PR says why.

The word `ready-to-merge` stays everywhere it names the ask (`asks "ready-to-merge …"`, the
`ready-to-merge` line): only the topic name goes.

### 2. `refused-push` and `stack` become real pages

Both stay as names (the CLI prints them: `push.py`'s `(`help refused-push`)`, `stack_shape.py`'s
`read `$CHANTIER help stack` now and after each compaction`). Each keeps only the pages that are its
own; the pages it borrowed stay printed by their own topics, which its own pages already name.

- `refused-push`: its readings become `topics/refused-push.md` and `topics/refused-push-steering.md`.
  It no longer prints `refused-push-answer.md` (named by `refused-push.md`: "The answer: `help
  refused-push-answer`"), nor `refused-push-judgement.md`, `refused-push-gate.md`,
  `refused-push-route.md` and `refused-push-run.md` (named by `refused-push-steering.md`: "Next:
  `help refused-push-judgement`, `help refused-push-route`", which print the gate and run pages).
  Its roles and trigger stay.
- `stack`: its reading becomes `topics/stack.md`. It no longer prints `stack-outside.md` (named by
  `stack.md`: "The other asks: `help stack-outside`"). Its roles and trigger stay.

Joining `refused-push.md` and `refused-push-steering.md` into one file is not this CR's
(`cards-one-page-per-theme`).

### 3. The other topics with a text of their own

The other 22 topics at the base that print a page of their own plus pages another topic prints
(`ci`, `conflicts`, `handback-other`, `pr-extras`, `retake`, `cr-workers`, `stack-restack`,
`stack-make`, `sync`, `merge-under-grant`, `long-gate`, `lost-driver`, `park`, `release-tag`,
`retro`, `retro-critic`, `wakes`, `stack-grows`, `refused-rebase`, `refused-push-judgement`,
`refused-push-route`, `direct-mode`) hold a text and stay unchanged. Whether they too drop their
borrowed readings is question 2.

### 4. The pointers fixed

Each pointer to a removed name names the page that fits; none is settled by copying a text.

- `cr-driver.md` line 23: "(`help trouble`)", after "a gate … while its result can still count",
  becomes "(`help trouble-gate`)".
- `cr-driver.md` line 33, `release-driver.md` line 31, `stack-driver.md` line 33, the "Rare cases:"
  list: the one entry `` `trouble` (a worker fails, an escalation, a remote command fails, a gate to
  stop, a git command in the wrong place) `` is replaced by the four topics that print its pages,
  each with its share of the old words: `` `trouble-worker` (a worker fails, an escalation);
  `trouble-remote` (a remote command fails); `trouble-gate` (a gate to stop); `trouble-git` (a git
  command in the wrong place) ``. This pointer truly needs four pages, so it names them.
- `foreman.md` line 3: "(`help direct`)" becomes "(`help direct-mode`)".
- `topics/ci.md` line 6: "an infrastructure failure or a flake: `help trouble`" becomes `help
  trouble-remote`.
- `topics/ci-beside-gate.md` line 6: "An infrastructure failure, or a job also red on the default
  branch: `help trouble`" becomes `help trouble-remote`.
- `topics/cr-prompt.md` line 6: "Failures: `help trouble`." becomes "Failures: `help
  trouble-worker`." (a worker's reply that fails its format).
- `topics/release-ship.md` line 9: "On the infrastructure: one re-run (`help trouble`)" becomes
  `help trouble-remote`.
- `topics/stack-deliver.md` line 4: "the condition of `help stack-run`" becomes "the condition of
  `help stack-asks`" (the local-gate clause sent "only with `passed`" is in `stack-asks.md`).

At `4d12a5b`, these are all the pointers to the ten names in the tracked files outside
`docs/proofs/` (a scan of every `help <name>` and of the "Rare cases:" lists). The CLI's source
names none of the ten (`test_every_topic_a_line_names_exists` reads it); `hosts/*.json`, `hooks/`,
`docs/`, `evals/`, `scenario/` and `README.md` name none. Any other pointer the Driver finds at its
base (one the two CRs below added included) is fixed the same way and named in the PR.
`docs/proofs/` (trial history) and `evals/results/` (recorded runs) are history and are not edited.

### 5. Byte ceilings

`test_brief_bytes.py` measures each role's whole brief. At `4d12a5b`: `cr-driver` 11,090 of
11,100, `release-driver` 10,407 of 10,500, `stack-driver` 10,217 of 10,300, `foreman` 22,554 of
22,600. The two CRs below change these cards before this CR's base. The four-entry list adds
about 59 bytes to each Driver card, `trouble-gate` 5 more to `cr-driver.md`, and `direct-mode` 5
to `foreman.md`.

The ceilings are not raised (the Chief of Staff's call of 2026-11-27, written in
`cards-delete-pages-chief`'s specification, applies here too). When an addition does not fit, the
Driver tightens the wording of the line that receives it (the "Rare cases:" list's other
parentheses; `foreman.md`'s first paragraph), with no pointer and no rule dropped. It quotes in the
PR the `brief-bytes` lines of the four roles, before (at the base) and after (at the head). If
tightening the receiving line is not enough, it stops and asks the steering session, and does not
raise a figure.

### 6. `docs/protective-rules.md`

This CR deletes no page, so no line loses its home file. In the same PR:

- a line that names one of the ten removed names as a home (`help trouble`, or "topic
  `steering`", for instance) gets the topic of section 1's table that prints the page holding the
  rule, or the page itself;
- a line whose quoted span contains a sentence this CR edits (section 4) gets the span as it
  reads at the head.

No other line changes, and no line is removed. After this CR, no line of that file names a removed
topic.

### 7. Tests (`skills/chantier/scripts/cli/tests/`)

All of them read the shipped files at the head under test.

- `test_help_topics.py`, new `test_every_topic_holds_a_text_of_its_own`: for each topic of
  `load_topics()`, the readings of the other topics whose readings are a strict subset of its own
  do not cover all its readings (a host map reading counted as one reading). A failure names the
  topic and the topics that cover it. It fails at `4d12a5b` (nine topics), and at this CR's head it
  passes and keeps a name with no text from coming back.
- `test_help_topics.py`, the pointer test that `cards-delete-pages-chief` adds (every `help <name>`
  in the shipped references and the skills' `SKILL.md` names a topic, and each name of the Chief of
  Staff card's "Rare cases:" list): extended to the backticked names of every card's "Rare cases:"
  list that follow `` `$CHANTIER help <topic>`: `` (the Driver cards, `qa-driver.md`,
  `verifier.md`). A failure names the file, line and name. If that test is not at the base, this CR
  adds it as `cards-delete-pages-chief`'s specification describes it, with this extension.
- `test_card_homes.py`: a removed name still in `HOMES` at the base (at `4d12a5b`, `stack-run` in
  `test_role_cards_split`) is replaced by the topics of section 1's table that print the pages
  holding its rules (for `stack-run`: `stack-asks`, `stack-ends`, `stack-drop`, each added once).
- `test_brief_bytes.py`: its figures do not change; it passes at the head (section 5).
- `test_help_lists_them_all` and `test_for_lists_only_that_roles_topics` read `load_topics()` and
  pass unchanged.

## Decisions from 02-answers.md

1. « ouvre un batch et lance ces 7 CR » (2026-11-27) is read as "grilled enough" for this CR; the
   owner's confirmation is still owed (question 1).
2. The batch is a stack. This CR sits above `cards-delete-pages-chief` and
   `cards-delete-pages-crew`, and below `cards-one-page-per-theme`. Only the CR on top of the stack
   owes the local Windows `scenario` run.
3. card-cleanup-Q5 A: steps 1 to 3 ship with a new version, in small CRs; steps 4 to 7 wait. This
   CR is plan step 1's second item and adds no step of its own. The moment the batch lands, given
   the other project that reads the cards live, is the steering session's and the user's call at
   merge time.
4. The owner's « un theme » per card and progressive disclosure organised for many pages: a reader
   is led to one topic per case (the four `trouble-*` topics, `direct-mode`, `stack-asks`) instead
   of a name that prints several themes at once (`steering` printed 25 pages at `4d12a5b`).

## Out of scope

- Deleting a page, or moving or rewording a page's text, beyond the pointer lines of section 4 and
  the tightening section 5 allows.
- The 22 topics of section 3 (question 2), joining `-pN` sets or a topic's pages into one file
  (`cards-one-page-per-theme`), and the three kept Copilot host pages and the host maps.
- Any change under `skills/chantier/scripts/cli/src/` (none is needed), `help.py` included; the
  `next:` lines that name a guide (plan step 4).
- `docs/proofs/` and `evals/results/`.
- The version bump (`release-card-cleanup`).

## Evidence

- The diff holds only: the ten `topics.json` entries removed, the readings of `refused-push` and
  `stack`, the pointer lines of section 4 (and any tightening of section 5), the lines of
  `docs/protective-rules.md` of section 6, and the tests. No file under `topics/` is deleted.
- `chantier help`'s first line before (at the base, `topics: 202; …`) and after (`topics: 192;
  …`), quoted in the PR, the Driver's own count if the base differs. `chantier help <name>` answers
  `no topic <name>` for each of the ten.
- `chantier help refused-push` prints only `references/topics/refused-push.md` and
  `references/topics/refused-push-steering.md`; `chantier help stack` prints only
  `references/topics/stack.md`; each `--- references/… ---` line quoted.
- `chantier help --for cr-driver` lists the four `trouble-*` topics and no `trouble`; `help --for
  chief-of-staff` lists none of the ten.
- The new `test_every_topic_holds_a_text_of_its_own` and the extended pointer test pass;
  `test_every_topic_a_line_names_exists` passes. A repository grep for `help <name>` and for each
  removed name in backticks, over the tracked files outside `docs/proofs/` and `evals/results/`,
  finds only the ask word `ready-to-merge`, quoted in the PR.
- No line of `docs/protective-rules.md` names a removed topic; each line this CR changed names a
  home that exists at the head and holds the rule (the PR quotes it).
- The `brief-bytes` lines of `cr-driver`, `release-driver`, `stack-driver` and `foreman` before and
  after, each at or under its unchanged figure.
- `just check` passes. The cards change, so the pipeline's `just scenario (ubuntu-latest)` job is
  green at the PR's head; the local Windows `scenario` run is owed only by the CR on top of the
  stack (AGENTS.md). No change under the CLI's `src/` or `evals/kit/`, so `just eval-dry-run` is
  not owed.

## Questions for the Chief of Staff

1. Answer 1 reads « ouvre un batch et lance ces 7 CR » as "grilled enough": does the owner confirm?
2. The request names only `refused-push` and `stack` as names that "become real pages". The 22
   topics of section 3 also print pages that another topic prints. This specification leaves them
   unchanged, since each holds a text and the request names only those two. Should this CR also
   drop their borrowed readings, as for `refused-push` and `stack`? Each own page then needs to name
   the topic it no longer prints, and some do not today (`ci.md`, for instance), which adds a line.
   The other choice is to leave this to `cards-one-page-per-theme`.
