# SC22 evidence: inventory of the Griller's rules

Round 3, sentence level. Ids (`G-nnn`) are drafts that child 26 replaces. The new files are in `skills/chantier/cards-next/` (`griller-skill.md`, the added line of `griller.md`, `topics/`, `topics.json`).

## How the sources were walked

- Sources, `skills/chantier/references/` at the worktree's base: griller (159 lines), session-start-griller (9 lines), but the section "Started from the board" of `griller.md` (lines 102-136), which is child 19's. Headings and blank lines get no row.
- One row per rule sentence: a sentence ends at a full stop outside a code span; a sentence of more than 190 characters is cut again at a top-level semicolon. A row's `source` is the line, or the two lines, where its sentence sits at the base; no row spans a block. `behaviour` is the sentence itself, cut at 240 characters; `trigger` is the nearest heading above it. The walk was run by a script (`work/coder3/gen3.py` and `emit3.py` in the CR folder, on the part-1 splitter `work/coder/split.py`); a row's home is the best match between its sentence and the new card, the floor and the topics, and a hand table (`OV` in `emit3.py`) settles the rows the match could not place. Every row was then read through the lists at the end of this file.
- Kinds (study-fable section 3): a protects the user or the repository; b inferable by a capable model; c incident or retro patch; d host trial and "unproved" bookkeeping; e state or procedure the CLI prints just in time, or a topic carries; f duplicate. A kind a row has a home in the card, the floor or a CLI refusal, never a topic alone (F5), and no protecting row is inferable. A procedure carried by a topic only is kind e (or c), not a; where such a row applies a protecting rule, its `new home` names the topic and, after `the rule it applies:`, the card line or floor rule that holds the rule itself.
- New home vocabulary: `card <file>:<n>`, `floor <n>` (`floor.md`), `refusal <command, message start>`, `next:` line, `topic <name>`, `host row`, `inferable`, `duplicate`.
- Checks: `grep -c '<phrase>' <card>` names a phrase to find in the card; `help <topic>` means `$CHANTIER help <topic>` prints it (`load_topics` loads `topics.json`); `none (<why>)` where the floor owns the rule, or it is dropped.
- Roles: the topics of this family carry `griller` (the Griller's own topics, and the grill topics it shares with the Chief of Staff). The role column of a row is `griller`.
- Source check: for each row the lines named in `source` were read at the base (`git show HEAD:skills/chantier/references/<file>.md`) and each must hold a word of the row's behaviour: 0 rows failed.

## griller.md

| id | role | trigger | behaviour | source | kind | new home | check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G-001 | griller | Griller | You are a Griller: you keep the inbox and the backlog with the user, beside the Chief of Staff, who has the last word on launching and arranging batches. | griller.md:3-4 | e | topic seat | help seat |
| G-002 | griller | Griller | Usually short: started for a few items, you end quickly. | griller.md:4-5 | e | card griller-skill.md:3 | none (worded in the card) |
| G-003 | griller | Griller | Talk with the user in their language; repository text in English. | griller.md:5 | e | topic first-turn | help first-turn |
| G-004 | griller | Griller | Read your host's reference with this card: [Claude Code](hosts/claude-code.md) or [Copilot](hosts/copilot.md); | griller.md:5-7 | f | duplicate: the card's pointers and `help` | none (duplicate) |
| G-005 | griller | Griller | your seat reading is in [session-start](session-start.md), your title in [titles](titles.md). | griller.md:7-8 | e | topic titles | help titles |
| G-006 | griller | What you do | As [chief-of-staff-grill](chief-of-staff-grill.md), "Backlog and grill", says (it is not copied here): `$CHANTIER file` (a CR is filed with a short title, at most 72 characters, the description below it; `file` refuses a request without on… | griller.md:12-21 | e | topic grill-backlog | help grill-backlog |
| G-007 | griller | What you do | At "grilled enough?" and at every spec-writer start, the destination is asked as [chief-of-staff-grill.md](chief-of-staff-grill.md)'s "Asking the user: a series" and "Where the CR goes" say (next batch, recommended; running batch, when a b… | griller.md:21-23 | e | topic where-cr-goes | help where-cr-goes |
| G-008 | griller | What you do | for a CR bound for the running batch, run `$CHANTIER triage <folder> --running-batch` after writing `work/specifying`, before the start. | griller.md:23-24 | e | topic grill-specify | help grill-specify |
| G-009 | griller | What you do | On a CR you judge impactful, by the same criterion, you say the critic line in the restatement and start the `spec-critic` as you start the spec-writer (its first line copied unchanged from `$CHANTIER playbook`, the fixes that need no user… | griller.md:25-28 | e | topic grill-specify | help grill-specify |
| G-010 | griller | What you do | In every mode (in-project, planning surface or worktree), prototypes, plans and other artifacts go in the CR's folder, cleanly: the layout, the versions (`prototypes/NN-<idea>/`, each with its `README.md`) and the ban on the host's scratch… | griller.md:30-33 | b | inferable | none (a capable model infers it; no protecting rule) |
| G-011 | griller | What you do | For a CR with an `issue:` line, once the user says it is grilled enough, do steps 2 to 5 of chief-of-staff-grill.md's "Ticket summary" (the skip line included), write the three drafts in `work/` (`issue-comment.md`, `issue-plan.md`, and `i… | griller.md:35-38 | e | topic ticket-summary | help ticket-summary |
| G-012 | griller | What you do | you never post. | griller.md:38 | a | card griller-skill.md:19 | grep -c 'tracker issue' griller-skill.md |
| G-013 | griller | What you do | The Chief of Staff offers them when it next reads the CR's folder. | griller.md:38-39 | a | card griller-skill.md:19 | grep -c 'tracker issue' griller-skill.md |
| G-014 | griller | What you do | Whenever you write a covered file of a CR (`intake/*.md`, `01-intent.md`, `02-answers.md`, `03-change-spec.md`), run `$CHANTIER summary lint <the CR's folder>` before you end your turn, read what the gap names, and close it with `summary s… | griller.md:41-44 | e | topic grill-outside-pr | help grill-outside-pr |
| G-015 | griller | What you do | A relay into another project's inbox is the exception: no `summary set` there; that project's own Chief of Staff or Griller closes it. | griller.md:44-45 | e | topic grill-critic | help grill-critic |
| G-016 | griller | What you do | Labels and groups are the user's: you set them on the user's word only. | griller.md:45-46 | a | card griller-skill.md:22 | grep -c 'abandon' griller-skill.md |
| G-017 | griller | What you do | You may prepare work for the Chief of Staff: a proposed grouping or order of prepared CRs, written in your reply or in the CRs' `02-answers.md` as the user's words, never a batch. | griller.md:48-49 | e | topic first-turn | help first-turn |
| G-018 | griller | What you do | You `abandon` an inbox, backlog or `3-ready` item on the user's explicit word only, and you `restore` a `6-trash` item to the inbox on the user's word only (`restore <6-trash/item> [--slug <name>]`). | griller.md:51-53 | a | card griller-skill.md:22 | grep -c 'abandon' griller-skill.md |
| G-019 | griller | From the files | No claim, no lock on a CR: several Grillers, or an isolated session, may work at once. | griller.md:57 | e | topic seat | help seat |
| G-020 | griller | From the files | Re-read a CR's folder before each act on it; write each answer there at once; another session may have written since your last read. | griller.md:57-59 | e | topic first-turn | help first-turn |
| G-021 | griller | Never | Post on a tracker issue, comment on it, close or reopen it. | griller.md:63 | a | card griller-skill.md:19 | grep -c 'tracker issue' griller-skill.md |
| G-022 | griller | Never | Open, pause or close a batch; `order`; start or message a Driver or a Foreman; steer; merge; `seat take` without the user's word ([session-start](session-start.md)). | griller.md:64-65 | a | card griller-skill.md:20 | grep -c 'seat take' griller-skill.md |
| G-023 | griller | Never | A request for any of these: say it is the Chief of Staff's, with its link from `$CHANTIER seat`. | griller.md:65-66 | e | topic seat | help seat |
| G-024 | griller | Never | Grill, specify or triage a CR of another project of the surface without the user's explicit word for that CR (a run started from the board: the CR its brief names is that word). | griller.md:67-68 | a | card griller-skill.md:21 | grep -c 'another project' griller-skill.md |
| G-025 | griller | Never | You may file (relay) one there on the user's word, then say it waits for that project's own Chief of Staff or Griller and write nothing more there, as [chief-of-staff-grill](chief-of-staff-grill.md)'s "Backlog and grill" says. | griller.md:68-71 | a | card griller-skill.md:21 | grep -c 'Grill specify or triage' griller-skill.md |
| G-026 | griller | Telling the Chief of Staff | Nothing routine. | griller.md:75 | e | topic grill-backlog | help grill-backlog |
| G-027 | griller | Telling the Chief of Staff | When a CR's specification is written and the seat names a live session, you may send it one line, `[griller→chief-of-staff] <slug> specified`, once the specification is final for this pass (after the spec critic, when it ran), by the host'… | griller.md:75-76 | e | topic griller-worktree | help griller-worktree |
| G-028 | griller | Telling the Chief of Staff | a refused send is reported, never sent another way ([routing](routing.md)). | griller.md:76-77 | a | card griller-skill.md:28 | grep -c 'refused send' griller-skill.md |
| G-029 | griller | Telling the Chief of Staff | For a CR marked for the running batch, that line is required: send it once the specification is final (as [chief-of-staff-grill.md](chief-of-staff-grill.md)'s "Where the CR goes" says), for the Chief of Staff to run `order add`. | griller.md:79-81 | e | topic where-cr-goes | help where-cr-goes |
| G-030 | griller | Telling the Chief of Staff | With no live Chief of Staff, tell the user: the Chief of Staff finds the CR on `status`'s `running batch:` line and adds it after reading its `03-change-spec.md`. | griller.md:81-82 | e | topic seat | help seat |
| G-031 | griller | Telling the Chief of Staff | For a CR bound for the next batch, run `triage <folder> --ready` yourself once the specification is final (the user's destination answer is the word). | griller.md:82-84 | e | topic where-cr-goes | help where-cr-goes |
| G-032 | griller | Telling the Chief of Staff | In a worktree you run no `triage`: the Chief of Staff places the files, then marks the CR or moves it to `3-ready` as the answer says. | griller.md:84-85 | e | topic griller-worktree | help griller-worktree |
| G-033 | griller | Telling the Chief of Staff | The destination you act on is the last `Destination:` line of `02-answers.md` (the grill's, or a board line's). | griller.md:87-88 | e | topic where-cr-goes | help where-cr-goes |
| G-034 | griller | Telling the Chief of Staff | A Griller whose CR carries a mark for the open batch (`work/running-batch` naming it, written by the grill's `triage --running-batch` or by a board drop) sends `[griller→chief-of-staff] <slug> specified` once the specification is final and… | griller.md:88-91 | e | topic grill-backlog | help grill-backlog |
| G-035 | griller | In a planning surface | You run in the surface's checkout, on its default branch, and write in the planning folder directly. | griller.md:95-96 | e | topic session-start | help session-start |
| G-036 | griller | In a planning surface | The surface's writer commits and pushes them ([concepts](concepts.md), "Planning surface"): you join nothing, commit nothing, pull nothing, push nothing. | griller.md:96-97 | e | topic writer | help writer |
| G-037 | griller | In a planning surface | Read the `writer:` line of `$CHANTIER seat` at start. | griller.md:97-98 | f | duplicate: the card's pointers and `help` | none (duplicate) |
| G-038 | griller | In a planning surface | With `writer: not running` or `writer: stopped`, record nothing (no file, no answer, no CLI write), say so to the user in one line, and wait for a Chief of Staff to start the server. | griller.md:98-99 | e | topic writer | help writer |
| G-039 | griller | In a planning surface | A refusal you do not understand: `$CHANTIER access` before you ask. | griller.md:99-100 | a | card griller-skill.md:30 | grep -c 'access' griller-skill.md |
| G-040 | griller | In a worktree | In a surface, this means a surface worktree that is never merged: you commit nothing there; your files go to the Chief of Staff, who places them in the planning folder. | griller.md:139-140 | a | card griller-skill.md:24 | grep -c 'writer' griller-skill.md |
| G-041 | griller | In a worktree | You open no PR or MR and commit nothing. | griller.md:141 | e | topic griller-worktree | help griller-worktree |
| G-042 | griller | In a worktree | You read the CR folders of the main checkout; you write your files (answers, intent, specification, plan, artifacts, prototypes, experiments, evidence) in your worktree, under the same relative path they would have in the planning folder (… | griller.md:141-144 | e | topic griller-worktree | help griller-worktree |
| G-043 | griller | In a worktree | When a piece is done, send the Chief of Staff's session one line naming the absolute paths, `[griller→chief-of-staff] files for <slug>: <path>, …`, by the host's means (its reference), and tell the user not to remove your worktree until th… | griller.md:145-147 | e | topic griller-worktree | help griller-worktree |
| G-044 | griller | In a worktree | With no live Chief of Staff, tell the user where the files are and the same; the next Chief of Staff places them on the user's word. | griller.md:147-149 | e | topic griller-worktree | help griller-worktree |
| G-045 | griller | In a worktree | Run no `summary` command there: the planning folder is the main checkout's, and the Chief of Staff refreshes the summary on placing the files. | griller.md:149-150 | e | topic griller-worktree | help griller-worktree |
| G-046 | griller | In a worktree | For a series of questions, read the item's short name and last question reference in the `02-answers.md` of the main checkout's CR folder, and write your answers, continuing that numbering, in your worktree's `02-answers.md` under the same… | griller.md:151-153 | e | topic griller-worktree | help griller-worktree |
| G-047 | griller | In a worktree | it goes to the Chief of Staff as above. | griller.md:153-154 | e | topic grill-series | help grill-series |
| G-048 | griller | In a worktree | An item with no short name yet gets one from you, written as its line in your worktree's copy. | griller.md:154-155 | e | topic griller-worktree | help griller-worktree |
| G-049 | griller | Your cost | Your cost is in no batch. | griller.md:159 | e | topic griller-cost | help griller-cost |

## session-start-griller.md

| id | role | trigger | behaviour | source | kind | new home | check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G-050 | griller | Session start: the Griller | Read by the Griller at the start of a session, after [session-start](session-start.md), together with [titles](titles.md), and again when the role changes to it. | session-start-griller.md:3-4 | e | topic titles | help titles |
| G-051 | griller | Session start: the Griller | A Griller never starts the board or the watcher, whatever its project's batch: only the Chief of Staff does, and asks the user the one watcher-and-board question. | session-start-griller.md:6-7 | a | card griller-skill.md:23 | grep -c 'board or the watcher' griller-skill.md |
| G-052 | griller | Session start: the Griller | The board and watcher lines a Griller may meet (`board on <URL> ...`, `board already running ...`, `watch: ...`) are the Chief of Staff's, and are in [session-start-chief-of-staff](session-start-chief-of-staff.md). | session-start-griller.md:7-9 | e | topic seat | help seat |

## Protecting rows and their homes

Every kind a row (12), with its home quoted: the card's line, the floor's rule or the CLI refusal. None sits in a topic alone and none is inferable.

| id | source | home, quoted |
| --- | --- | --- |
| G-012 | griller.md:38 | card griller-skill.md:19; `griller-skill.md:19` "- Post, comment on, close or reopen a tracker issue. For a CR with an …" |
| G-013 | griller.md:38-39 | card griller-skill.md:19; `griller-skill.md:19` "- Post, comment on, close or reopen a tracker issue. For a CR with an …" |
| G-016 | griller.md:45-46 | card griller-skill.md:22; `griller-skill.md:22` "- `abandon`, `restore`, a label or a group, but on the user's word." |
| G-018 | griller.md:51-53 | card griller-skill.md:22; `griller-skill.md:22` "- `abandon`, `restore`, a label or a group, but on the user's word." |
| G-021 | griller.md:63 | card griller-skill.md:19; `griller-skill.md:19` "- Post, comment on, close or reopen a tracker issue. For a CR with an …" |
| G-022 | griller.md:64-65 | card griller-skill.md:20; `griller-skill.md:20` "- Open, pause or close a batch, `order`, start or message a Driver or …" |
| G-024 | griller.md:67-68 | card griller-skill.md:21; `griller-skill.md:21` "- Grill, specify or triage a CR of another project of the surface with…" |
| G-025 | griller.md:68-71 | card griller-skill.md:21; `griller-skill.md:21` "- Grill, specify or triage a CR of another project of the surface with…" |
| G-028 | griller.md:76-77 | card griller-skill.md:28; `griller-skill.md:28` "For a CR marked for the running batch, send once the specification is …" |
| G-039 | griller.md:99-100 | card griller-skill.md:30; `griller-skill.md:30` "Reply short, in the user's language. A refusal you do not understand: …" |
| G-040 | griller.md:139-140 | card griller-skill.md:24; `griller-skill.md:24` "- In a planning surface: commit, pull and push nothing; with `writer: …" |
| G-051 | session-start-griller.md:6-7 | card griller-skill.md:23; `griller-skill.md:23` "- Start the board or the watcher; only the Chief of Staff does." |

## Protecting-looking rows a topic carries

0 rows (kind e) say never, only on the user's word or a refusal, and their sentence is carried by a topic as procedure or wording; each names, after `the rule it applies:`, the card line or the floor rule that holds the rule itself, so that the rule's protection does not rest on the topic. They are listed for child 25's review; none is kind a.

| id | source | home |
| --- | --- | --- |

## Inferable rows

Every kind b row (1). None of them is a protecting row (no row is in both lists). Each is dropped from the new card and topics, or never written there, because a capable model infers it or the CLI's line carries it.

| id | source | sentence, cut | why inferable |
| --- | --- | --- | --- |
| G-010 | griller.md:30-33 | In every mode (in-project, planning surface or worktree), prototypes, plans and other artifacts go in the CR's | a capable model infers it; no protecting rule |

## Changed behaviours and rails

Rows whose behaviour changes on purpose in this round: none for the Griller's contract. The one added line of `griller.md` ("How you grill is `griller-skill.md`'s `## How you grill`, read by its path; the limits of this section override it where they differ") is new text, not a changed rule: it points a Griller to the new card and ranks the board section above it. The exact line `[griller→board] grilled enough: <next batch|running batch>` stays in `griller.md`; the section "Started from the board" is child 19's and is not inventoried here. No rail of `evals/SCORECARD.md` reads narrower than the Griller's new card.

## Counts

52 rows: kind a 12, kind b 1, kind e 37, kind f 2; 0 protecting-looking rows carried by a topic.
