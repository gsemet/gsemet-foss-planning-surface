# Round 2 work list (written by scratch/merge/worklist.py)

332 rows with no resolvable compliant home: 57 kind a (home must be `floor`, `card` outside topics/ or `refusal`; no re-kinding), 139 `inferable` with no quiz case, 136 other open rows. Close a row by an entry in a `scratch/merge/overrides-*.tsv` table (or a quiz case), then rerun merge.py and this.
A restored line goes to a topic first for a non-a row; in a full card, replace words.
The card bytes below are against the card budgets; `test_brief_bytes.py` caps each role's brief as well, and may have less room.

## Inferable rows with no quiz case (inf-<n> cases)

W-010, W-025, W-047, W-085, W-117, W-144, W-157, W-200, W-206, W-220, W-243, W-254, W-263, W-271, W-292, W-307, W-362, D-009, FM-050, FM-115, FM-129, FM-B039, FM-B047, FM-168, FM-263, FM-264, FM-291, FM-292, FM-312, FM-313, FM-315, FM-316, FM-334, FM-335, FM-349, FM-393, FM-436, FM-486, FM-492, C-008, C-010, C-046, C-190, C-345, C-375, C-1027, C-1048, C-1059, C-1079, C-1082, C-1084, C-1087, C-1090, C-1095, C-1097, C-1101, C-1105, C-1106, C-1164, C-1196, C-1203, C-1254, C-1295, C-1412, C-1413, C-1479, C-1607, C-1610, C-1613, C-1614, C-1616, C-1617, G-010, H-001, H-002, H-003, H-004, H-005, H-006, H-007, H-008, H-009, H-010, H-071, H-075, H-076, H-077, H-081, H-090, H-201, H-207, H-243, H-314, H-320, H-387, H-401, H-433, H-440, H-441, H-446, H-527, H-528, H-850, H-853, H-854, H-858, H-881, H-889, H-929, H-930, H-931, H-932, H-938, H-1006, H-1010, H-1014, H-1070, H-1071, H-1073, H-1080, H-1175, H-1252, H-1260, H-1285, H-1293, H-1429, H-1453, H-1454, H-1455, H-1456, H-1461, H-1547, H-1549, H-1552, H-1553, H-1554, H-1556, H-1590, H-1650

## chief-of-staff.md: 51 open, 35 without a case

Room: 5999/6000 LF bytes, 1 left.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| H-1360 | a | A user may allow one for a batch: that word stays in that batch, is sent with the user's own words, and never becomes a rule. | hosts/claude-code.md:787-789 | form not allowed for kind a; seed home: card chief-of-staff.md:31 (the Foreman's worktree override is dropped per sc21-Q1, default, to confirm by the owner) |
| H-1421 | a | Chantier explains the steps and never does them. | hosts/claude-code.md:897-898 | form not allowed for kind a; seed home: card chief-of-staff.md:13; floor 7; topic host-remote |
| H-706 | a | It is not a **For you** item: nothing waits on the user, but a sync pending more than 3 minutes: then one **For you** item, `sync pending: held by <holders>`, with the offer to stop your own board and watcher when they are the only holders ... | status-layout.md:106 | form not allowed for kind a; seed home: card chief-of-staff.md:14 |
| H-833 | a | **The forge's tools:** when the project's forge is GitHub and `gh` is missing or not logged in, or the `gh stack` extension (github/gh-stack) is not installed, recommend it and say why (the stack driver then makes the stack on GitHub with ... | init.md:101-106 | form not allowed for kind a; seed home: card chief-of-staff.md:13; topic init-tools |
| H-899 | a | When that holds at the 3-minute message, the offer is in that message; | sync-checkout.md:15 | form not allowed for kind a; seed home: card chief-of-staff.md:14 |
| H-905 | a | anything else is not own (another session's board included, and a server `webui` started, whose command line holds no `--seat`: step 6 never offers to stop it). | sync-checkout.md:15 | form not allowed for kind a; seed home: card chief-of-staff.md:14; topic sync-offer |
| H-907 | a | On the user's yes: stop the watcher and the board, list the holders again, sync only if none, then start the board and the watcher again whatever the result (`session-start-chief-of-staff.md`'s board start, and the watcher's printed ... | sync-checkout.md:15 | form not allowed for kind a; seed home: card chief-of-staff.md:14 |
| C-286 | d | otherwise yes on desktop, Remote Control and terminal \| unproved until a real switch runs (trial: the first real switch, its events showing the `steering` event `direct` and each `resume: switch to direct mode` take) \| \| "Run this command… | chief-of-staff-any.md:129-132 | open; seed home: host row (unproved bookkeeping dropped from the topic) |
| C-472 | d | Where the host refuses to start a session, or the session you are in is not fit, the way is a step of the user's: give the "For you" block of the reference, after saying what the choice costs, and say "I have not tested this path" for a bl… | chief-of-staff-batch-start.md:220-223 | open; seed home: host row (unproved bookkeeping dropped from the topic) |
| C-003 | e | You start no Driver or background agent (see Subagents; the board, a background command of the CLI, is not an agent: [session-start-chief-of-staff](session-start-chief-of-staff.md)) and never message a Driver: every order goes through the… | chief-of-staff.md:5-8 | open; seed home: card chief-of-staff.md:22 |
| C-011 | e | \| The user asks… \| Do \| Read \| \| --- \| --- \| --- \| \| "init", a guided tour, "I am new here" \| `$CHANTIER init`, then the tour \| [init](init.md) \| \| anything, at the start of a session \| read `AGENTS.md`: how the project ships, the branch,… | chief-of-staff.md:21-25 | open; seed home: topic first-turn |
| C-014 | e | [Steering a batch yourself](chief-of-staff-direct.md#steering-a-batch-yourself) (`chief-of-staff:direct`) \| \| a batch, "run the P1s", a series, a stack \| preflight → show the plan → go → `$CHANTIER open` → start the Foreman, or steer it yo… | chief-of-staff.md:25-26 | open; seed home: topic batch-plan |
| C-017 | e | `close --yes` only on the user's yes \| `chief-of-staff:batch-end` \| \| add, drop, reorder, change a CR; | chief-of-staff.md:30-31 | open; seed home: topic retro; the rule it applies: card chief-of-staff.md:16; floor 10 |
| C-021 | e | with `writer: not running`, write nothing \| `chief-of-staff:grill` ("With a planning surface") \| \| a watcher's notification or end \| read its output, act on each line as in [The watcher](session-start-chief-of-staff.md#the-watcher) (with `… | chief-of-staff.md:32-33 | open; seed home: topic watcher-events |
| C-023 | e | after the user's no in this session, ignore the line \| `chief-of-staff:steering` \| \| "what did it cost?" \| `$CHANTIER cost` \| `chief-of-staff:steering` \| \| "my own PR template" \| `$CHANTIER file` a CR for the guideline and the template; | chief-of-staff.md:34-36 | open; seed home: topic watcher; no rule: an entry-point table row |
| C-024 | e | a CR Driver delivers them by PR, see [pr-template](pr-template.md) \| The project (this card) \| \| "use my agent for <role>", "which models?", "which agents and models?", a role's skills or tools \| `hosts.<host>.roles.<role>.agent` (or `mode… | chief-of-staff.md:36-37 | open; seed home: topic pr-template-own |
| C-027 | e | it counts from the next batch \| The project (this card) \| \| "add a <kind> review" \| the `chantier` section of `AGENTS.md`, on the user's word \| The project (this card) \| \| "I restarted the app", "resume" \| liveness check; | chief-of-staff.md:39-41 | open; seed home: topic config; the rule it applies: card chief-of-staff.md:13 |
| C-034 | e | a page that lost its cookie (a home-screen app, a private tab) asks for the link on the page: the user pastes the link there \| [session-start-chief-of-staff](session-start-chief-of-staff.md) \| \| "a new board key", "the board's link leaked"… | chief-of-staff.md:46-47 | open; seed home: topic board-restart; no rule: a fact about the CLI, the host or the forge |
| C-052 | e | never offer a workaround the rules forbid ("No fallback" holds). | chief-of-staff.md:65-66 | open; seed home: topic main-checkout; the rule it applies: floor 3 |
| C-098 | e | Say also that a Driver's force push was refused once with these rules set (batch-23); | chief-of-staff.md:129-130 | open; seed home: host row; no rule: wording of a message or report |
| C-1014 | e | ```bash $CHANTIER file "<raw request>" [--title "<short title>"] [--slug <slug>] # or @<file> for a raw request file $CHANTIER triage <inbox-or-backlog-folder> --priority P1\|P2\|P3\|P4 # a backlog item changes priority $CHANTIER triage <inbo… | chief-of-staff-grill.md:5-10 | open; seed home: topic grill-backlog; the rule it applies: card chief-of-staff.md:26 |
| C-1039 | e | This is an exception to the summary rule of the paragraph above ("A CR's summary ... applies to your own writes too") for the `intake/request.md` that `file` wrote: the other project's own Chief of Staff or Griller writes the intent and cl… | chief-of-staff-grill.md:59-62 | open; seed home: topic grill-surface |
| C-1047 | e | One call is about one CR or backlog item; questions about another item go in a separate call. | chief-of-staff-grill.md:77-78 | open; seed home: topic grill-series |
| C-1053 | e | With the line there, use it unchanged: the name is kept for the item's life, whoever asks next. | chief-of-staff-grill.md:85-86 | open; seed home: topic grill-series |
| C-1065 | e | No call goes out without it, and never with the references left out of it. | chief-of-staff-grill.md:102-103 | open; seed home: topic grill-series; no rule: wording of a message or report |
| C-1143 | e | The destination acted on is the last `Destination:` line of the CR's `02-answers.md`, whether the grill wrote it or a board line did (see "A watcher's notification or end"): `Destination: next batch ...`, `triage <folder> --ready`; | chief-of-staff-grill.md:209-211 | open; seed home: topic where-cr-goes |
| C-1157 | e | A CR's artifacts during a grill follow [concepts](concepts.md), "A CR's folder holds its work": prototypes and experiments go in the CR's folder; | chief-of-staff-grill.md:235-236 | open; seed home: topic grill-backlog |
| C-1238 | e | Every finding takes one of the two ways. | chief-of-staff-grill.md:359 | open; seed home: topic grill-critic-steps |
| C-1244 | e | "1 écarté"); then the questions, in the format of "Asking the user: a series" (text first, `<short name>-Q<n>` references continuing the item's numbering, at most 5 per call), together with the specification's own open questions. | chief-of-staff-grill.md:366-369 | open; seed home: topic grill-series |
| C-1309 | e | "Released in" (`chief-of-staff:release`) is the closing comment of the request's "Land" row, unchanged. | chief-of-staff-grill.md:471-472 | open; seed home: topic release-chief-after |
| C-1442 | e | P10's warning (one per capability, the base only at a first turn) comes as the Chief of Staff's question ([chief-of-staff](chief-of-staff.md), "The project"). | session-start.md:53-54 | open; seed home: topic allow-rules |
| C-1443 | e | P9 now holds the forge's rights and branch rules too ([chief-of-staff-any](chief-of-staff-any.md), "Forge permissions"). | session-start.md:54-55 | open; seed home: topic forge-permissions |
| C-154 | e | Each moment below is an action of `startup-manifest.json`: read its piece when the moment comes, and what the line adds. | chief-of-staff.md:234-235 | open; seed home: card chief-of-staff.md:41 |
| C-1542 | e | `board already running at <URL>`: the same line (and the same second line, when it follows, then the `board: listens on the local network (...)` line when the board listens beyond this machine, which you pass on, and an added `board runs a… | session-start-chief-of-staff.md:52-53 | open; seed home: topic board-lines |
| C-156 | e | Filing, moving or grilling a CR, the Spec-writer and the spec critic, "archive <link>", a PR follow-up on a ticket: `chief-of-staff:grill`. | chief-of-staff.md:237 | open; seed home: card chief-of-staff.md:41; no rule: a pointer |
| C-161 | e | Steering a batch yourself (direct mode): `chief-of-staff:direct`, with steering, and merge or batch-end as they come; it adds the Foreman's card, whose own moments you read as they come. | chief-of-staff.md:242 | open; seed home: card chief-of-staff.md:35; no rule: a pointer |
| C-165 | e | A moment that needs several (direct mode: steering, merge, batch-end, the Foreman's) reads each. | chief-of-staff.md:246 | open; seed home: card chief-of-staff.md:35; no rule: a pointer |
| C-255 | e | First use: the first-turn introduction ([session-start](session-start.md)) or the end of the `init` tour. | chief-of-staff-any.md:83-84 | open; seed home: topic first-turn |
| C-315 | e | The Tips rule above and the "For you" block (`status-layout.md`) go together. | chief-of-staff-any.md:154 | open; seed home: topic compacting |
| C-495 | e | It holds the shape, the cost table, the Tips line, "MR" or "PR", and how a CR is named. | chief-of-staff-steering.md:15 | open; seed home: card chief-of-staff.md:39 |
| C-625 | e | The watcher (the command the CLI prints, in the background; the user's yes once per session, [session-start-chief-of-staff](session-start-chief-of-staff.md), "The watcher"; the host's means, its reference, "Run the watcher"). | chief-of-staff-steering.md:244-245 | open; seed home: topic seat; the rule it applies: card chief-of-staff.md:3 |
| C-643 | e | The watcher's other lines (its `started the board (PID <n>)` clause, the board's lines it passes on, the lines of a board that does not come up or of a seat it cannot start one for): as [session-start-chief-of-staff](session-start-chief-of… | chief-of-staff-steering.md:283-285 | open; seed home: topic watcher-lines |
| C-659 | e | A `config changed on the board: specifying.parallel ...` line is told as it stands and changes nothing in the batch; the next spec-writer start reads the new limit. | chief-of-staff-steering.md:305-307 | open; seed home: topic watcher-events |
| C-669 | e | The other `board wrote (...)` lines, or a `config changed on the board` line of a role's key (`hosts.<host>.roles...`): one line to the user that says it (a few words per event), no tool call, no action (but the destination write above). | chief-of-staff-steering.md:324-327 | open; seed home: topic watcher-board; topic watcher-events |
| C-697 | e | A draft says "do not merge": every PR in draft you name to the user carries, in the user's language, "do not merge" / "ne pas merger" and what blocks it: "🟤 #174 CR-222: ne pas merger, base = branche de CR-237". | chief-of-staff-merge.md:26-28 | open; seed home: topic merge-words; the rule it applies: floor 1 |
| C-748 | e | In direct mode the steering session checks its own asks the same way (the CLI already refuses such an ask; the check catches one recorded before it or forced without a fitting order). | chief-of-staff-merge.md:110-111 | open; seed home: topic merge-series-stack; no rule: procedure |
| C-902 | e | Read [foreman](foreman.md) (and, for a stack batch, [foreman-stack](foreman-stack.md)) and your host's reference ([Claude Code](hosts/claude-code.md) or [Copilot](hosts/copilot.md)) and do what they say of the Foreman, until the batch comp… | chief-of-staff-direct.md:7-10 | open; seed home: topic direct-mode |
| H-1612 | e | Reload", with `$CHANTIER` as this file defines it, nothing else of this file but its Startup core; it sets no mode. | skills/chief-of-staff/SKILL.md:29 | open; seed home: card skills/chief-of-staff-SKILL.md:35 |
| H-750 | e | The examples and the full rule are in [chief-of-staff-any](chief-of-staff-any.md), "Compacting and tips". | status-layout.md:208-209 | open; seed home: topic compacting |
| C-1292 | f | read them back with `gh issue artifact list <link> --json number,name,url`; | chief-of-staff-grill.md:437-438 | open; seed home: duplicate: the card's pointers and `help` |
| C-1513 | f | Read only (`seat`, `status`): no order, `take`, heartbeat, Driver, message or `uv sync`. | session-start.md:180-181 | open; seed home: duplicate: the card's pointers and `help` |
| C-008 | b | The Foreman, the Drivers and the workers get their own instructions in their prompts; you never read theirs, except the Foreman's when you steer a batch yourself in direct mode. | chief-of-staff.md:15-16 | no quiz case |
| C-010 | b | Who talks to whom: [routing](routing.md). | chief-of-staff.md:17 | no quiz case |
| C-046 | b | Within what you have, judge freely. | chief-of-staff.md:55 | no quiz case |
| C-190 | b | You have no timer: it happens on that message. | chief-of-staff.md:281-282 | no quiz case |
| C-345 | b | critical path: CR-221 → CR-237 → CR-222 → CR-225 → CR-226 → CR-228." | chief-of-staff-any.md:201-202 | no quiz case |
| C-375 | b | P9 also covers the forge's rights ([Forge permissions](chief-of-staff-any.md#forge-permissions-p9)): they only warn. | chief-of-staff-batch-start.md:59-60 | no quiz case |
| C-1027 | b | A named archive folder is checked; the default walk leaves `5-archives` out. | chief-of-staff-grill.md:40-41 | no quiz case |
| C-1048 | b | A series may touch any facet of its item (scope, words, icons). | chief-of-staff-grill.md:78-79 | no quiz case |
| C-1059 | b | The reference names the question only: the context, and anything else that names the CR (status, PR, `depends.json`), names it by number and slug as [concepts](concepts.md) says ("CR-250 grill-question-format"). | chief-of-staff-grill.md:91-94 | no quiz case |
| C-1079 | b | A worked example, one item (`ready-wording`, CR-231 ready-line-wording), two questions. | chief-of-staff-grill.md:128 | no quiz case |
| C-1082 | b | Context: CR-231 ready-line-wording. | chief-of-staff-grill.md:133 | no quiz case |
| C-1084 | b | A. | chief-of-staff-grill.md:134 | no quiz case |
| C-1087 | b | B. | chief-of-staff-grill.md:135 | no quiz case |
| C-1090 | b | C. | chief-of-staff-grill.md:136 | no quiz case |
| C-1095 | b | Context: CR-231 ready-line-wording. | chief-of-staff-grill.md:140 | no quiz case |
| C-1097 | b | A. | chief-of-staff-grill.md:141 | no quiz case |
| C-1101 | b | B. | chief-of-staff-grill.md:142 | no quiz case |
| C-1105 | b | Recommendation: A, a gap left out is a surprise at the merge. | chief-of-staff-grill.md:143 | no quiz case |
| C-1106 | b | ``` | chief-of-staff-grill.md:144 | no quiz case |
| C-1164 | b | a claude.ai artifact or an inline visualization that matters to the CR has its source saved in `prototypes/NN-<idea>/` (its link, if any, in that version's `README.md`); | chief-of-staff-grill.md:242-244 | no quiz case |
| C-1196 | b | "critique : oui, elle touche le contrat des Drivers"). | chief-of-staff-grill.md:297 | no quiz case |
| C-1203 | b | `Spec critic: yes, it touches the Drivers' contract.`), so a later session knows whether it is due. | chief-of-staff-grill.md:303-304 | no quiz case |
| C-1254 | b | A reference built on this shape: [ticket-summary-example](ticket-summary-example.md). | chief-of-staff-grill.md:380-381 | no quiz case |
| C-1295 | b | GitHub's comment `--attach` takes only images and video, so there is no attachment tier on GitHub. | chief-of-staff-grill.md:441-442 | no quiz case |
| C-1412 | b | This card is deferred action guidance. | session-start.md:3 | no quiz case |
| C-1413 | b | Startup reads only the common, host, role and wrapper entries in `startup-manifest.json`. | session-start.md:3-4 | no quiz case |
| C-1479 | b | It lets small requests outside the tracker be accepted and prioritised; the tracker keeps the strategic vision, external requests and long-term planning. | session-start.md:129-130 | no quiz case |
| C-1607 | b | The editor gets a dark theme, chosen in Settings > Appearance. | ticket-summary-example.md:11 | no quiz case |
| C-1610 | b | Left out: a theme per document, and custom colours. | ticket-summary-example.md:15 | no quiz case |
| C-1613 | b | What changes for you: a "Theme" choice (Light, Dark, System) in Settings > Appearance. | ticket-summary-example.md:23 | no quiz case |
| C-1614 | b | Limits: one theme for the whole app; printing stays light. | ticket-summary-example.md:24 | no quiz case |
| C-1616 | b | Docs: the Settings page gains a "Theme" paragraph. | ticket-summary-example.md:26 | no quiz case |
| C-1617 | b | ```html <!-- Mock-up: imitates the planned result; not the product. --> <!doctype html> <html><head><meta charset="utf-8"><title>Dark theme, mock-up</title> <style>body{background:#1e1f22;color:#e6e6e6;font-family:system-ui}</style></head>… | ticket-summary-example.md:30-37 | no quiz case |
| H-889 | b | Six steps: | sync-checkout.md:3 | no quiz case |
| H-1556 | b | The full rules stay where they are. | reload-rules.md:3 | no quiz case |

## coder.md: 0 open, 2 without a case

Room: 1603/1500 LF bytes, 103 over.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| W-010 | b | Within what you have, judge freely | coder.md:21 | no quiz case |
| W-025 | b | A reply out of that format is a failed worker, which the Driver starts again rather than reads; a reply in format that is only longer than its cap is read and noted, not restarted | coder.md:43-45 | no quiz case |

## concepts.md: 14 open, 0 without a case

Room: 26181 LF bytes, budget: see test_brief_bytes.py and the card tests.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| H-115 | b | It has no name, only a number: `batch-<n>` (`<n>` on two digits, counting all batches), its own files in `4-batch/` (its CRs in the three state folders there), and `--batch` takes the number, `4` or `batch-04`. | concepts.md:211-214 | open; seed home: card concepts.md:55 |
| H-042 | e | The default carries a closing verb (`Closes #<n>`, `Closes <KEY>-<n>`), so the issue closes at the merge as the tracker's integration reads it; a project rule may say otherwise. | concepts.md:77-78 | open; seed home: card concepts.md:14 |
| H-050 | e | A sub-folder is created only when its first file is written: neither the CLI nor an agent creates `prototypes/`, `experiments/` or `evidence/` ahead of use. | concepts.md:104-105 | open; seed home: card concepts.md:41 |
| H-111 | e | **A CR's name:** when an agent names a CR to a person or in a report (messages, report tables, asks; in a CR's PR only the description's Internal references section, never the title or the body's text, unless the project's rules say ... | concepts.md:206-209 | open; seed home: card concepts.md:43 |
| H-304 | e | ```chantier <role> for <cr> "<title>" of batch <batch>, in the project <root>. / Read <skill>/references/startup-core.md, the host core, role core, and the short startup section / named by <skill>/references/startup-manifest.json; defer ... | concepts.md:518-533 | open; seed home: card concepts.md:87 |
| H-313 | e | a prompt without the line is not guarded; a role that needs other folders, or fewer, gets its own line from the card that starts it. | concepts.md:552-554 | open; seed home: card concepts.md:99 |
| H-315 | e | An agent starts right the first time: the parent copies the first line of the role, unchanged, from what it sees at that moment. | concepts.md:556-557 | open; seed home: card concepts.md:107 |
| H-318 | e | A refused agent answers every later message with that same answer and does nothing else, whatever the message holds (on Claude Code a message resumes an agent that ended its turn, with its context, not one the host stopped (a `killed` ... | concepts.md:560-563 | open; seed home: card concepts.md:107 |
| H-330 | e | A subagent of the Chief of Staff (the Demo explorer, or an exploration, a prototype or a study) is started the same way: its first line is the one of the table above. | concepts.md:579-580 | open; seed home: card concepts.md:119 |
| H-331 | e | When the work is for a CR, its brief names that CR's folder and the place in it (a `prototypes/NN-<idea>/` or `experiments/`), and its result (the study, the report) is written there as a file, not only returned in the conversation. | concepts.md:580-583 | open; seed home: card concepts.md:119 |
| H-356 | e | \| `release-driver` \| `take <cr>`, a CR of kind `release` \| `driver.md` \| none \| none \| own branch \| | concepts.md:640 | open; seed home: card concepts.md:129 |
| H-357 | e | \| `stack-driver` \| `take stack` \| `driver.md` \| none \| yes \| batch branches \| | concepts.md:641 | open; seed home: card concepts.md:129 |
| H-379 | e | \| The rounds used up: a `blocked rounds:` hand-back, whatever the round's failure (a red CI job, a gate broken after a rebase, a Verifier `NOT VERIFIED`, an Inspector `FIX-REQUIRED`) \| the CR Driver hands back `blocked rounds:` as always; ... | concepts.md:683 | open; seed home: card concepts.md:140 |
| H-390 | e | If such a CR fails again (a new `blocked` hand-back that counts for either of the first two rows, or its escalated `debugger` or `conflict-resolver` failing the same way), the Foreman (the Chief of Staff in direct mode) does not `take` it ... | concepts.md:700-704 | open; seed home: card concepts.md:146 |

## conflict-resolver.md: 2 open, 1 without a case

Room: 1494/1500 LF bytes, 6 left.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| W-052 | a | Never claim a check you did not run | conflict-resolver.md:25 | form not allowed for kind a; seed home: card conflict-resolver.md (Never) |
| W-062 | a | You never commit, push or merge | conflict-resolver.md:26 | form not allowed for kind a; seed home: card conflict-resolver.md (Never: push ... merge; the rebase stays a rebase) |
| W-047 | b | Within what you have, judge freely | conflict-resolver.md:20-21 | no quiz case |

## cr-driver.md: 30 open, 0 without a case

Room: 3749/4000 LF bytes, 251 left.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| D-011 | a | Read the specification whole or by part to brief workers, write `pr-body.md`, judge the proof; the detail of "What changes" is the Coder's and Inspector's; copy its list of file edits as a checklist into each Coder's prompt | driver.md:31-36 | form not allowed for kind a; seed home: topic (new) cr-rounds |
| D-013 | a | After `handoff` and `log`, read `pr-body.md`, `work/verify.md` and the evidence files by name and caption, not opened; read pr-template only before the first body edit; do not open the spec, `investigation.md`, the `r<n>.md` notes or the diff; start at the first closing step with no `closing:` note | driver.md:46-55 | form not allowed for kind a; seed home: topic restart |
| D-016 | a | `handoff` (counts nothing) and `log`; a round only for what the notes ask | driver.md:63-65 | form not allowed for kind a; seed home: topic (new) cr-workers |
| D-017 | a | `round <cr> --note ... --lease <n>` before each Coder; refused past the limit (exit 5) `blocked rounds:`; budget spent `blocked budget:`; refused exit 2 with nothing new: read `handoff`, start the round's coder or `note` why | driver.md:66-72 | form not allowed for kind a; seed home: topic (new) cr-workers (the commands) and cr-rounds (the limits) |
| D-019 | a | A reply out of format is a failed worker; the Inspector and extra review steps reply the JSON object alone, parseable | driver.md:79-82 | form not allowed for kind a; seed home: topic (new) cr-rounds; topic trouble-worker |
| D-020 | a | Coder, Investigator, Debugger: their output file exists (`r<n>.md`, `investigation.md`, ...); Verifier and Conflict resolver replies: ship and proof, conflicts | driver.md:83-87 | form not allowed for kind a; seed home: topic (new) cr-rounds; cr-proof; conflicts |
| D-025 | a | A raw log goes in `work/gates/` or a `*.log` file, never in a file published with the CR | driver.md:108-111 | form not allowed for kind a; seed home: topic (new) cr-prompt (the `writes:` line and the raw log) and PART 1's worker-shell |
| D-026 | a | `context: <n> tokens` read after each; at 130,000 record state with `note`, then `handback <cr> blocked context:` | driver.md:117-121 | form not allowed for kind a; seed home: topic closing (the numbers) and card cr-driver.md (115,000 line) |
| D-028 | a | Never end your turn to wait for a child: its reply is the result of the call | driver.md:126-128 | form not allowed for kind a; seed home: card cr-driver.md (background-shell wait line) and topic lease |
| D-035 | a | Start in the worktree or the project root, never in the CR folder; read and write the CR folder's files by absolute paths; change no shell's folder into a CR folder; name targets (`-C`, `--repo`, `-R`) | driver.md:141-148 | form not allowed for kind a; seed home: topic trouble-git, restart, facts (the folders) |
| D-038 | a | First step `git -C <main checkout> fetch <remote> <default branch>`, then `worktree add -b <branch> <path> <base>` | driver.md:157-162 | form not allowed for kind a; seed home: topic (new) cr-workers |
| D-039 | a | Never `git branch -a` or `git branch --list` with no pattern, nor `git status` outside your worktree | driver.md:163-165 | form not allowed for kind a; seed home: topic (new) cr-workers |
| D-040 | a | Rebase first, so the long gate passes on the head you push: fetch, `rebase <base>`; a conflict is a `conflict-resolver`; never stop a process by name, `kill` yours by id; a command the host may refuse runs alone | driver.md:168-176 | form not allowed for kind a; seed home: topic (new) cr-ship |
| D-041 | a | Run the project's fast gate and any pre-push check at the rebased committed head, yourself, one command per call, never through `gate`; one note per command `before first push at <sha7>: <command>: pass`; a failure is a round | driver.md:177-185 | form not allowed for kind a; seed home: topic (new) cr-ship |
| D-045 | a | A short gate you run yourself in the worktree, never through `gate` | driver.md:219-223 | form not allowed for kind a; seed home: topic (new) cr-ship (D-041) |
| D-047 | a | Only your own CR's, only when its result can no longer count; `cancel` is the steering session's | driver.md:226-227 | form not allowed for kind a; seed home: topic trouble-gate |
| D-050 | a | Read the result yourself; judge it by the project's rules: a skipped job is never green; a job red on the default branch is not the CR's (note it); infrastructure failure, flake or CI over 3 hours: "a remote command fails"; the rest is a round | driver.md:238-242 | form not allowed for kind a; seed home: topic ci; trouble-remote |
| D-051 | a | The only source is the forge's list of checks for the PR at the pushed head; files, rules, an earlier note and a guess are not a source | driver.md:242-246 | form not allowed for kind a; seed home: topic ci |
| D-052 | a | Confirm the PR's head on the forge is the pushed head (`gh pr view --json headRefOid`) | driver.md:246-249 | form not allowed for kind a; seed home: topic ci |
| D-053 | a | Two looks a minute apart; a list that contradicts the rules is noted | driver.md:249 | form not allowed for kind a; seed home: topic ci-no-check (part of ci) |
| D-054 | a | The note names the command and the head (seven characters): `CI: gh pr checks 12 at abc1234: test pass`; the PR body's CI box says the same | driver.md:250-253 | form not allowed for kind a; seed home: topic ci |
| D-055 | a | Never taken whole: `gh run view <run> --log-failed > <work folder>/ci-<run>.log`, then Grep or Read by parts, or give it to a `debugger` | driver.md:254-257 | form not allowed for kind a; seed home: topic ci |
| D-056 | a | CI beside the long gate, an early push | driver.md:218 | form not allowed for kind a; seed home: topic ci-beside-gate (part of ci) |
| D-058 | a | Each commit, a checkpoint included, has a message in the project's commit style saying what it holds; never `wip`, "pending", "checkpoint", a round or review state, a CR number, a batch or a role | driver.md:261-267 | form not allowed for kind a; seed home: topic (new) cr-ship; topic checkpoints |
| D-066 | a | Coder, Inspector (a `FIX-REQUIRED` is a round), extra review steps, Verifier (a gap is a round or a Known gap), the Debugger first when the cause is not plain | driver.md:320-375 | form not allowed for kind a; seed home: topic (new) cr-rounds |
| D-068 | a | Commit by name, check `diff --stat` empty and the tree clean, `note "r<n> approved at <head>, committed as <sha>"`; push, PR as a draft, `ship <cr> <link>`, CI, Verifier | driver.md:376-400 | form not allowed for kind a; seed home: topic (new) cr-ship; card lines 8-9 |
| D-070 | a | Steps 1 to 4: evidence boxes updated; a short `verifier` pass on the posted description; PR turned ready; `handback ready <pr link>` with the Known gaps; `closing:` notes | driver.md:413-441 | form not allowed for kind a; seed home: topic closing |
| D-044 | e | `gate <cr> <name> [...]` runs only the long gates `chantier.yaml` names, in the worktree, in order; never stopped while running; a rebase with a conflict resolved takes `ship --conflict` and the early push | driver.md:215-221 | open; seed home: topic conflicts-early-push; `$CHANTIER gate --help` |
| X-003 | e | A brief that asks a debugger or a verifier to read an artifact names its evidence folder | driver.md:112-113 | open; seed home:  |
| D-048 | f | Never taken whole: its result from `handoff` or the log's last lines | driver.md:227-228 | open; seed home: floor 7 |

## debugger.md: 0 open, 1 without a case

Room: 1281/1500 LF bytes, 219 left.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| W-085 | b | Within what you have, judge freely | debugger.md:20-21 | no quiz case |

## demo-explorer.md: 0 open, 2 without a case

Room: 1612/1500 LF bytes, 112 over.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| W-144 | b | Within what you have, judge freely | demo-explorer.md:18-19 | no quiz case |
| W-157 | b | The demo is in the batch's language | demo-explorer.md:10 | no quiz case |

## foreman.md: 19 open, 21 without a case

Room: 3997/4000 LF bytes, 3 left.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| FM-B037 | a | The batch keeps the slots it opened with, whatever the board's Configuration page now says: only an `order slots` the Chief of Staff sends changes them. | foreman.md:129 | form not allowed for kind a; seed home: refusal check_slot (rails.py:57, the batch's own slots); floor 9 |
| H-1737 | a | After a start with a model, read that `model`; when it differs from the printed identifier, stop the agent's work and report both. | hosts/copilot.json:164 | form not allowed for kind a; seed home: floor 3; host row model-ran-on |
| FM-489 | d | Marks: the check is plain git, the same on both hosts and forges; its run by a Copilot Foreman is unproved. | foreman-conflict.md:42-43 | open; seed home: host row (Copilot reference: `hosts/copilot.md`) |
| FM-B012 | d | the Copilot host's path is unproved. | foreman.md:86-87 | open; seed home: dropped (unproved bookkeeping, kind d; no host row holds it) |
| FM-B017 | d | The Copilot host's path is unproved (as for the stack's top above). | foreman.md:94 | open; seed home: dropped (unproved bookkeeping, kind d; no host row holds it) |
| FM-004 | e | A prompt that reaches a session which ran an earlier batch starts a new batch from the state alone, never from what you remember of the last one: its limits, orders and heartbeat are not yours to carry, and you arm a new heartbeat. | foreman.md:7-10 | open; seed home: card foreman.md:10; topic wakes |
| FM-005 | e | As your first act, set the session title your prompt gives on yourself (your host's reference says how; where it offers no way, the title stays). | foreman.md:10-11 | open; seed home: card foreman.md:6 |
| FM-008 | e | Do it at the start of every batch you steer, and again after a compaction: reread only those startup sections and your `batch` action, and the `rules:` pointer of `status`'s `batch:` line, not whole cards (in a stack batch, also [foreman-s… | foreman.md:14-16 | open; seed home: card foreman.md:10 |
| FM-010 | e | Then decide: which CR a Driver takes next, what a Driver must hear, what the Chief of Staff must know. | foreman.md:16-17 | open; seed home: card foreman.md:3 |
| FM-012 | e | In direct mode the Chief of Staff reads this card and steers the batch itself, with the differences of [chief-of-staff](chief-of-staff-direct.md#steering-a-batch-yourself). | foreman.md:17-18 | open; seed home: card foreman.md:3 |
| FM-017 | e | After `final` you end your work and stay idle: no Driver, no worker, no tool call of yours runs, so that a later `close` finds nothing running; the cost at the pause is the cost to date. | foreman.md:28-30 | open; seed home: card foreman.md:31 |
| FM-051 | e | `$CHANTIER take <cr> [--note "<why>"] --epoch <n>`: the CR is a Driver's; it prints the facts for the prompt ([concepts](concepts.md), "Starting an agent"). | foreman.md:214-215 | open; seed home: card foreman.md:13 |
| FM-064 | e | see [concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md), "A Driver's prompt". | foreman.md:226 | open; seed home: card foreman.md:13 ("copy whole the prompt"); card concepts.md:105 |
| FM-101 | e | In the text of an ask, name a CR by its number and slug together (`concepts.md`, "A CR's name"). | foreman.md:288-290 | open; seed home: card foreman.md:38 |
| FM-404 | e | A background task it left running woke it. | foreman-lost-driver.md:18-19 | open; seed home: topic lost-driver |
| FM-473 | e | The command, one per pair, from the main checkout (with a planning surface, `git -C <clone>`, the clone `take` names), with each CR's branch as `handoff <cr>` prints it: `git merge-tree --write-tree --name-only --no-messages <new cr's bran… | foreman-conflict.md:17-19 | open; seed home: topic conflict-check |
| FM-476 | e | Any other exit (a missing ref, a git older than 2.38 that does not know `--write-tree`): no ask about a conflict; | foreman-conflict.md:21-22 | open; seed home: topic conflict-check |
| FM-548 | e | Legitimate: the route rule first (Claude Code; on Copilot, where P10 does not run, skip this step and go to step 4). | foreman-refused.md:70-71 | open; seed home: topic refused-push-route |
| FM-552 | e | or | foreman-refused.md:80 | open; seed home: topic refused-push-route |
| FM-050 | b | `handoff <cr>` and `log <cr>` for a CR's story. | foreman.md:212-213 | no quiz case |
| FM-115 | b | It does not stop with the heartbeat or with a pause, even the heartbeat's stop after 30 minutes with no Driver: it leaves a merge of a PR handed back ready, after a pause, recorded. | foreman.md:316-318 | no quiz case |
| FM-129 | b | An order's line or a `ping` starts a turn; if it leaves a Driver running, arm the heartbeat again. | foreman.md:340-341 | no quiz case |
| FM-B039 | b | A refusal you do not understand: `$CHANTIER access <cr> --epoch <n>` before you ask; it explains and changes nothing. | foreman.md:131-132 | no quiz case |
| FM-B047 | b | The `take` reopens the CR to `working` and counts no round; its Driver runs `ship` at the new head, then passes the long gate and a `VERIFIED` verdict there before `handback ready`. | foreman.md:146-148 | no quiz case |
| FM-168 | b | The CLI reads such a CR `ready to merge`, with no remark on the record. | foreman-stack.md:12-13 | no quiz case |
| FM-263 | b | Nothing of the stack left open: neither. | foreman-stack.md:195 | no quiz case |
| FM-264 | b | Say in your next line to the Chief of Staff which one you chose and why, in one clause. | foreman-stack.md:197 | no quiz case |
| FM-291 | b | Several merges handled in one turn get one attempt after the last of them. | foreman-merge.md:52 | no quiz case |
| FM-292 | b | The order of the other steps after a merge (rebase notes, `take`) is unchanged. | foreman-merge.md:52-53 | no quiz case |
| FM-312 | b | No ask, no message: the Chief of Staff reads the note for its next report. | foreman-merge.md:79-80 | no quiz case |
| FM-313 | b | The CR's state is unchanged. | foreman-merge.md:80-81 | no quiz case |
| FM-315 | b | After: no reload of the plugin, no new reading of the cards (the CLI is read live; the cards load at the next session or with `/reload-plugins`). | foreman-merge.md:85-86 | no quiz case |
| FM-316 | b | The next merge recorded tries again from step 1. | foreman-merge.md:86-87 | no quiz case |
| FM-334 | b | the resume steps below do not apply. | foreman-merge.md:122-123 | no quiz case |
| FM-335 | b | The `take` comes next: it holds the slot, or makes the CR wait for one like a queued CR when none is free. | foreman-merge.md:124-125 | no quiz case |
| FM-349 | b | Direct mode does this part itself. | foreman-hold.md:13 | no quiz case |
| FM-393 | b | Then `order done`. | foreman-hold.md:87 | no quiz case |
| FM-436 | b | each of those keeps its own path. | foreman-lost-driver.md:81 | no quiz case |
| FM-486 | b | Each PR stays as its hand-back left it: a `ready-to-merge` PR stays mergeable on its own. | foreman-conflict.md:35-36 | no quiz case |
| FM-492 | b | there is no confirmation to ask. | foreman-release.md:7 | no quiz case |

## griller-skill.md: 3 open, 1 without a case

Room: 3621/4000 LF bytes, 379 left.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| G-009 | e | On a CR you judge impactful, by the same criterion, you say the critic line in the restatement and start the `spec-critic` as you start the spec-writer (its first line copied unchanged from `$CHANTIER playbook`, the fixes that need no user… | griller.md:25-28 | open; seed home: topic grill-restate; topic grill-critic-steps |
| G-017 | e | You may prepare work for the Chief of Staff: a proposed grouping or order of prepared CRs, written in your reply or in the CRs' `02-answers.md` as the user's words, never a batch. | griller.md:48-49 | open; seed home: topic first-turn; the rule it applies: card griller-skill.md:5 |
| G-050 | e | Read by the Griller at the start of a session, after [session-start](session-start.md), together with [titles](titles.md), and again when the role changes to it. | session-start-griller.md:3-4 | open; seed home: topic titles |
| G-010 | b | In every mode (in-project, planning surface or worktree), prototypes, plans and other artifacts go in the CR's folder, cleanly: the layout, the versions (`prototypes/NN-<idea>/`, each with its `README.md`) and the ban on the host's scratch… | griller.md:30-33 | no quiz case |

## griller.md: 1 open, 1 without a case

Room: 1925 LF bytes, budget: see test_brief_bytes.py and the card tests.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| W-367 | a | You write no issue drafts: the Chief of Staff drafts them when it starts the spec-writer | griller.md:122-124 | form not allowed for kind a; seed home: card griller.md (write issue drafts: the Chief of Staff drafts them) |
| W-362 | e | "In a planning surface" holds but its `seat` reading: skip it (the server has checked the writer before the run) | griller.md:111-113 | no quiz case |

## inspector.md: 0 open, 4 without a case

Room: 2000/2000 LF bytes, 0 left.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| W-243 | b | Within what you have, judge freely | inspector.md:19-20 | no quiz case |
| W-254 | b | A reply out of that format is a failed worker, which the Driver starts again rather than reads; a reply in format that is only longer than its cap is read and noted, not restarted | inspector.md:34-36 | no quiz case |
| W-263 | b | Read only; you may run the fast gate to check a claim | inspector.md:41-42 | no quiz case |
| W-271 | b | `blocking` is not limited in number: each item there is worth a round, and keeps the 300-character limit | inspector.md:62-63 | no quiz case |

## investigator.md: 0 open, 1 without a case

Room: 1486/1500 LF bytes, 14 left.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| W-117 | b | Within what you have, judge freely | investigator.md:20-21 | no quiz case |

## pr-template.md: 6 open, 0 without a case

Room: 12032 LF bytes, budget: see test_brief_bytes.py and the card tests.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| H-459 | e | They do not know the backlog, and `.agents/changes/` is not in git (but see the archive below). | pr-template.md:22-23 | open; seed home: card pr-template.md:12 |
| H-470 | e | A file path the diff changes (for instance `skills/chantier/references/driver.md`) may be named in Changes whatever its name. | pr-template.md:42-43 | open; seed home: card pr-template.md:15 |
| H-473 | e | The form of each line, the project's rules first (form, keyword, title or body, for instance `Closes JIRAJPT-1245`); where they say nothing, chantier's default: | pr-template.md:46-47 | open; seed home: card pr-template.md:16 |
| H-491 | e | a before/after tree or table (files moved or split, sizes, settings); | pr-template.md:78 | open; seed home: card pr-template.md:20 |
| H-503 | e | A proof carried over a move says so (`at <head7> (carried from <sha7>)`: it names the head it now stands at and the SHA it came from; only the SHA after `carried from` may lie outside the head's history, and `ship` names any other); | pr-template.md:93-96 | open; seed home: card pr-template.md:22 |
| H-507 | e | it is never left as a plain fact. | pr-template.md:99-100 | open; seed home: card pr-template.md:22 |

## qa-driver.md: 1 open, 0 without a case

Room: 1567/2000 LF bytes, 433 left.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| D-082 | a | Never writes on the PR, commits, pushes or comments | driver.md:574-591 | form not allowed for kind a; seed home: card qa-driver.md (Never) |

## release-driver.md: 2 open, 0 without a case

Room: 3809/3000 LF bytes, 809 over.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| D-084 | a | Open it as the base says: ready on the default branch, a draft on another base | driver.md:604-605 | form not allowed for kind a; seed home: topic release-ship |
| D-090 | a | The specification's; none there: pick the best from what the release ships | driver.md:633-635 | form not allowed for kind a; seed home: topic release-notes |

## release-template.md: 3 open, 0 without a case

Room: 7002 LF bytes, budget: see test_brief_bytes.py and the card tests.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| H-581 | e | \| A closing "why it matters" line \| "... This means you stay in the flow." \| (line removed) \| | release-template.md:64 | open; seed home: card release-template.md:44 |
| H-582 | e | \| Mechanism instead of consequence \| "The parser now debounces change events on the block node." \| "Typing fast in a long block no longer freezes the editor." \| | release-template.md:65 | open; seed home: card release-template.md:45 |
| H-584 | e | \| A sentence about a missing image \| "No screenshot: this change has nothing to show." \| (sentence removed; the change has no picture) \| | release-template.md:67 | open; seed home: card release-template.md:46 |

## retro-critic.md: 0 open, 1 without a case

Room: 1565/1500 LF bytes, 65 over.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| W-220 | b | Started in the background or not, as the parent needs your answer before it writes | retro-critic.md:7-8 | no quiz case |

## review-step.md: 3 open, 0 without a case

Room: 1497 LF bytes, budget: see test_brief_bytes.py and the card tests.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| H-848 | e | You run in the foreground for a Driver, do one short task and return. | review-step.md:3-4 | open; seed home: card review-step.md:3 |
| H-878 | e | One JSON object and nothing around it (no prose, no code fence), with exactly the keys `verdict`, `head`, `blocking`, `minor`, `confidence`, and no other key. | review-step.md:51-52 | open; seed home: card review-step.md:9 |
| H-885 | e | An item states a defect; what was checked and found right does not go in the reply. | review-step.md:60-61 | open; seed home: card review-step.md:17 |

## spec-critic.md: 0 open, 2 without a case

Room: 1572/1500 LF bytes, 72 over.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| W-200 | b | An inbox item often has no specification | spec-critic.md:16 | no quiz case |
| W-206 | b | The host references' marks: proved, documented, unproved | spec-critic.md:32-33 | no quiz case |

## stack-driver.md: 6 open, 0 without a case

Room: 3783/4000 LF bytes, 217 left.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| D-077 | a | `forge-stack create` or `gh stack`, rebuild after a change, five checks, no other means without the user's word | driver.md:536-552 | form not allowed for kind a; seed home: topic stack-make; card stack-driver.md |
| D-078 | a | `$CHANTIER stack` before a take's first rebase: its `head` values are the old heads | driver.md:553-561 | form not allowed for kind a; seed home: topic stack-restack |
| D-080 | a | A take's note `resume:` or a stack partly restacked: re-read, never redo | driver.md:569-573 | form not allowed for kind a; seed home: topic stack-restack; topic restart |
| X-004 | c | The release CR is the top piece, listed last; a release with no PR yet is no anomaly: it joins like any CR when it has its PR | driver.md:462-464 | open; seed home:  |
| X-005 | c | The release PR stays a draft on top until its CR is handed back ready and the checks hold, then turns ready with the others; a fix CR is not in the stack | driver.md:464-465 | open; seed home:  |
| X-006 | e | A stack batch is opened in stack mode or switched by order mode; after a switch the stack's order starts from the record's order | driver.md:467-469 | open; seed home:  |

## ticket-summary-example.md: 3 open, 0 without a case

Room: 1308 LF bytes, budget: see test_brief_bytes.py and the card tests.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| C-1602 | e | Modelled on a real ticket summary of 2026-11-10; its text is not kept here. | ticket-summary-example.md:3 | open; seed home: card ticket-summary-example.md:1; no rule: the sample's provenance, dropped |
| C-1603 | e | The shape and the size are the point: [chief-of-staff-grill](chief-of-staff-grill.md), "Ticket summary", says how it is made and posted. | ticket-summary-example.md:3-4 | open; seed home: card ticket-summary-example.md:3 |
| C-1606 | e | What will be done: | ticket-summary-example.md:10 | open; seed home: card ticket-summary-example.md:9 |

## verifier.md: 2 open, 2 without a case

Room: 3112/3000 LF bytes, 112 over.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| W-319 | a | The reply is the template at the end and nothing else (no greeting, no summary, no list of what was checked and found right): the whole of the output to the Driver | verifier.md:64-66 | form not allowed for kind a; seed home: card verifier.md (Reply in at most ten lines, after `verdict` has run; the block) |
| W-323 | e | You cite the pass in `verify.md` by the gate log's first line (the CR and the full SHA it ran at) and `handoff`'s checklist, at the full SHA verified; the CLI is what refuses a hand-back without a gate pass | verifier.md:74-76 | open; seed home: card verifier.md (Cite the gate pass by its log's first line and `handoff`); refusal: `handback` without a gate pass |
| W-292 | b | Within what you have, judge freely | verifier.md:21-22 | no quiz case |
| W-307 | b | A reply out of that format is a failed worker, which the Driver starts again rather than reads; a reply in format that is only longer than its cap is read and noted, not restarted | verifier.md:65-68 | no quiz case |

## shared (no single card): 47 open, 65 without a case

Room: choose a topic or the owning card.

| id | kind | behaviour | old source | why |
|---|---|---|---|---|
| D-010 | a | A rule you did not read still binds you; read its section before you act | driver.md:28-29 | form not allowed for kind a; seed home: card line "Rare cases: `$CHANTIER help <topic>`" and each `next:` line |
| D-012 | a | Run `handoff <cr>` and `log <cr>` first, read the sections of the steps to do, never of those done | driver.md:38-44 | form not allowed for kind a; seed home: topic restart |
| D-027 | a | Only when the last `context:` line read 130,000 or more, or for the closing hand-off (115,000 at `VERIFIED`, 130,000 during the closing); any other reason names that reason | driver.md:122-126 | form not allowed for kind a; seed home: topic closing |
| D-030 | a | A turn that ends with nothing running in the background ends your run: the host asks for your hand-back at once | driver.md:132-133 | form not allowed for kind a; seed home: host row `end-turn-background` and `driver-hand-back` |
| D-036 | a | Keep the id of each background task; stop each by that id with the host's stop of a background task as soon as its result is read | driver.md:148-151 | form not allowed for kind a; seed home: card Your end line (`host stop-own-background-task`); host row `stop-own-background-task` |
| D-037 | a | Stop every task still running, except the shell that runs `$CHANTIER gate`; a task left running wakes you after the hand-back | driver.md:151-154 | form not allowed for kind a; seed home: card Your end line; topic handback-gate-draft |
| D-064 | a | `question:`, `approval:`, `merge:`, `fix:`, `infra:`, `budget:`, `rounds:`, `context:`; the reason says what is wrong and what next | driver.md:308-314 | form not allowed for kind a; seed home: topic (new) cr-handback; topic handback-other |
| P-003 | a | A checkpoint commit has a real message; folded before the PR | driver-session.md:36-42 | form not allowed for kind a; seed home: topic checkpoints |
| P-005 | a | Re-takes: reread the notes, rebase on the base, a conflict is a `conflict-resolver`, a new push through `chantier push` | driver-retake.md:1-75 | form not allowed for kind a; seed home: topic retake |
| P-007 | a | Re-take inside a stack | driver-retake.md:93-109 | form not allowed for kind a; seed home: topic retake-stack (part of retake) |
| P-011 | a | A gate log is never taken whole; a failure is a round | driver-trouble.md:101-140 | form not allowed for kind a; seed home: topic trouble-gate |
| H-449 | c | Its text is never typed, built or escaped in a shell command, in any shell, and the file is never written by the shell (a redirection, a here-string, `Out-File`, `Set-Content`): PowerShell reads a backtick as an escape (`` `f `` is a form ... | concepts.md:801-805 | open; seed home: topic session-shell |
| H-1015 | d | **Mark of the section.** The rule (the live Driver, no live Driver and both-steerings points, and the event-is-not-an-order point) is **unproved** until the next real campaign shows it. | hosts/claude-code.md:132-133 | open; seed home: topic host-auto-fix |
| H-1181 | d | Include this content in your final response instead." The rule is as users report it in <https://github.com/anthropics/claude-code/issues/44657> and <https://github.com/anthropics/claude-code/issues/101519>: **unproved** by Anthropic. | hosts/claude-code.md:467-470 | open; seed home: topic host-refused |
| H-1233 | d | Seen 177 times in the user's week, mostly from subagents. | hosts/claude-code.md:558-559 | open; seed home: topic host-auto-mode-trials; no rule: a measurement, not carried |
| H-1254 | d | Whether 300000 holds, given the measured 165 to 170k compaction above (which concerns this very value), is unproved: the same trial settles the recommendation and records the cap. | hosts/claude-code.md:595-597 | open; seed home: topic host-compact |
| H-1437 | d | Unproved until a user has followed it once, like every block above. | hosts/claude-code.md:927-928 | open; seed home: topic host-allow-add |
| H-1526 | d | Until then the manual reload ("chantier reload", `session-start.md`, "Reload") is the only one, and the Chief of Staff names no compacting command (the "Compacting" section holds). | hosts/copilot.md:108-110 | open; seed home: topic host-compact |
| H-1002 | e | **A PR that is not a batch's** (the user's own PR in the same session) is out of chantier's rule: it is between the user and the app. | hosts/claude-code.md:110-111 | open; seed home: topic host-auto-fix |
| H-1011 | e | **During a normal batch chantier stays silent** about Auto-fix: it does not ask the user to turn it off, has no preflight check for it and gives no "For you" line for it (chantier cannot see whether Auto-fix is on, and a line at every go ... | hosts/claude-code.md:127-129 | open; seed home: topic host-auto-fix |
| H-1025 | e | The notice has no rank in that order, just as an Auto-fix event has none. | hosts/claude-code.md:152-153 | open; seed home: topic host-turn-end |
| H-1033 | e | Every other notice falls under the rule above. | hosts/claude-code.md:164 | open; seed home: topic host-turn-end |
| H-1105 | e | \| `Bash(git -C * rebase chantier/*)` and `PowerShell(…)` \| the same onto the bare `chantier/` branch of the CR under it in a series or a stack (the command refused in markdown-okf-schema-studio batch-09, 2026-11-23) \| a local rebase of the ... | hosts/claude-code.md:271 | open; seed home: card hosts/claude-code.md:24 |
| H-1120 | e | \| `Bash(gh pr create*)` and `PowerShell(…)` \| a Driver opens its PR (refused once as "Git Destructive") \| any PR on any repository `gh` can reach \| documented (rule form) \| | hosts/claude-code.md:286 | open; seed home: card hosts/claude-code.md:39 |
| H-1123 | e | \| `Bash(gh pr checks*)` and `PowerShell(…)` \| a Driver reads its CI \| read-only \| documented (rule form) \| | hosts/claude-code.md:289 | open; seed home: card hosts/claude-code.md:42 |
| H-1124 | e | \| `Bash(gh pr view*)` and `PowerShell(…)` \| a Driver or the steering session reads a PR \| read-only \| documented (rule form) \| | hosts/claude-code.md:290 | open; seed home: card hosts/claude-code.md:43 |
| H-1129 | e | \| `Bash(glab mr update*)` and `PowerShell(…)` \| a Driver's description or the stack's retarget on GitLab \| any MR edit on any project `glab` can reach \| documented (rule form) \| | hosts/claude-code.md:295 | open; seed home: card hosts/claude-code.md:48 |
| H-1130 | e | \| `Bash(glab mr view*)` and `PowerShell(…)` \| a Driver reads its MR \| read-only \| documented (rule form) \| | hosts/claude-code.md:296 | open; seed home: card hosts/claude-code.md:49 |
| H-1131 | e | \| `Bash(glab mr close*)` and `PowerShell(…)` \| the same close, on GitLab \| closing any MR `glab` can reach \| documented (rule form) \| | hosts/claude-code.md:297 | open; seed home: card hosts/claude-code.md:50 |
| H-1134 | e | \| `SendMessage` \| the Foreman and the Drivers message each other (refused twice) \| any message between this session's agents and sessions \| **unproved**: `SendMessage` as a rule is not documented (absent from tools-reference, checked ... | hosts/claude-code.md:300 | open; seed home: card hosts/claude-code.md:53 |
| H-1187 | e | Seen otherwise for a subagent. | hosts/claude-code.md:483 | open; seed home: topic host-auto-mode |
| H-1215 | e | What a trial before the go can and cannot prove (the Chief of Staff's trials, "Capabilities and their commands"): | hosts/claude-code.md:533-534 | open; seed home: topic host-auto-mode-trials |
| H-1265 | e | The mod is Claude Code's only (`CONTRIBUTING.md`): the automatic reload exists only where the plugin's mod loads. | hosts/claude-code.md:621-622 | open; seed home: topic host-compact |
| H-1295 | e | \| Desktop, driven by Remote Control \| the host's Remote Control notice \| yes, with no `cwd` and no `preset`, in its own folder; a start with `cwd` or `preset` is refused (proved 2026-11-20) \| yes, on a main checkout: it starts a new ... | hosts/claude-code.md:681 | open; seed home: topic host-sessions |
| H-1340 | e | \| Switch to Foreman mode \| yes \| yes: a new Foreman with no `cwd`, or a reused one ("Reusing the last Foreman") \| no \| preflight P1 fails in a terminal; proved 2026-11-20 for the first two (the rule above) \| | hosts/claude-code.md:766 | open; seed home: topic host-surfaces |
| H-1341 | e | \| Switch to direct mode \| yes \| yes, except the stop of a Foreman not answering (needs the machine) \| yes \| needs only the Chief of Staff's own session; unproved until a real switch runs (trial: the first real switch, its events showing ... | hosts/claude-code.md:767 | open; seed home: topic host-surfaces |
| H-1344 | e | \| `/permissions`, `/config` \| no: the app's own settings \| no \| yes \| terminal dialogs; unproved \| | hosts/claude-code.md:770 | open; seed home: topic host-surfaces |
| H-1346 | e | \| `/chantier-board` \| yes \| the pane does not show in a Remote Control view (`docs/boards.md`) \| yes \| documented in `docs/boards.md` \| | hosts/claude-code.md:772 | open; seed home: topic host-surfaces |
| H-1391 | e | Nothing for the user: the Chief of Staff starts it with no `cwd`, as at the desk (proved 2026-11-20). | hosts/claude-code.md:844-845 | open; seed home: topic host-for-you |
| H-1430 | e | Cost: none beyond the summary; the same conversation continues. | hosts/claude-code.md:915 | open; seed home: topic host-for-you |
| H-145 | e | The stack-driver runs during the batch keep the stack current (made at two PRs ready, a CR that joins on top, a newly ready CR moved below the drafts, a restack after a merge at once, as today); | concepts.md:268-271 | open; seed home: topic stack-grows |
| H-1542 | e | One named exception: in the dev mode, a `uv sync` that chantier's own processes block (holding the checkout's `.venv`; Windows os error 32) is not a launch failure: the session goes on unsynced with `sync pending`, as its skill's ... | startup-core.md:11-14 | open; seed home: card skills/chantier-SKILL.md:23 |
| H-166 | e | **A CR dropped from the stack** is removed: the PRs above go to draft first, its commits come out of the branches above (by the stack driver, or by the Driver of a working CR), its PR is closed when it goes to the trash (otherwise it goes ... | concepts.md:298-302 | open; seed home: topic stack-drop |
| H-223 | e | There is no version confirmation: the version is the specification's, else the Driver's choice, with its reason. | concepts.md:379-380 | open; seed home: topic release-ship |
| D-006 | f | Grep the heading then Read by offset and limit; never `cat`, `sed`, `awk` or `Get-Content` a section; never read twice | driver.md:17-18 | open; seed home: floor 7 (read by parts, never a whole large file) and `help` printing one topic |
| D-032 | f | Never take a large output whole: a diff by `git diff --stat`/`--name-only`; over about 200 lines a file under `work/` first, then read in parts | driver.md:136-139 | open; seed home: floor 7 |
| H-1521 | f | The command hygiene of `concepts.md` rule 9 applies on both hosts. | hosts/copilot.md:99 | open; seed home: topic worker-shell |
| D-009 | b | Another Driver's section, another role's card and the users' docs are not opening reads | driver.md:27 | no quiz case |
| H-001 | b | The steering sessions and the Drivers read this file: the words the team shares, the boundaries, and how an agent is started. | concepts.md:3-4 | no quiz case |
| H-002 | b | Each worker reads its own card, which restates the rules it uses. | concepts.md:4 | no quiz case |
| H-003 | b | At startup, identify the role, batch, project and parent session. | concepts.md:8 | no quiz case |
| H-004 | b | **Pull request (PR):** a merge request on GitLab. | concepts.md:12 | no quiz case |
| H-005 | b | **Connector:** the module that reads one forge, read-only (GitHub and GitLab ship). | concepts.md:13 | no quiz case |
| H-006 | b | **Interest:** a PR or MR, or a tracker issue a CR's `issue:` line names, that someone waits for; | concepts.md:14-15 | no quiz case |
| H-007 | b | `chantier interests` lists them; the forge hub reads only the PRs and MRs, while a client is subscribed (a running batch's open approval, pipeline and merge waits are interests too), an outside poller (the user's own program) the issues, ... | concepts.md:15-17 | no quiz case |
| H-008 | b | **`access`:** `$CHANTIER access [write\|claim\|push] [<cr>]` explains, read-only, what the rules say now for this session: whether it may write the planning folder (the writer), claim a CR (`take`'s checks, with `--epoch`) or push a CR's ... | concepts.md:18-20 | no quiz case |
| H-009 | b | It changes nothing, renews no lease and is no permission. | concepts.md:20-21 | no quiz case |
| H-010 | b | A refusal stays the refusing command's. | concepts.md:21 | no quiz case |
| H-071 | b | Its `.gitignore`, written by the CLI, keeps the batch's own files (`batch.json`, `events.jsonl`, `brief.md`, STATUS, locks, `.batch-number`, `seat.json`) and the detailed logs (`work/gates/`, `*.log`) and the Verifier's scratch folder ... | concepts.md:134-138 | no quiz case |
| H-075 | b | The next batch number is read from these records. | concepts.md:142 | no quiz case |
| H-076 | b | `$CHANTIER validate` checks the whole planning folder (stages, CR folders, outside archives' names, `summary.json`'s format, missing or late summaries, broken links between its Markdown files, and, as a gap, a surface `chantier.yaml`'s ... | concepts.md:142-145 | no quiz case |
| H-077 | b | a surface's own validation calls it; it blocks no other command. | concepts.md:145-146 | no quiz case |
| H-081 | b | The project's `AGENTS.md` may point to its surface with one line, `- planning: <url>, projects/<name>`, which the Chief of Staff reads and the CLI does not. | concepts.md:153-155 | no quiz case |
| H-090 | b | Full account: [planning modes](../../../docs/planning-modes.md). | concepts.md:168-169 | no quiz case |
| H-201 | b | A `ready` or `blocked` CR holds none. | concepts.md:352 | no quiz case |
| H-207 | b | `gate`, `verdict`, `ship`, `note` and `handback` are never refused for it. | concepts.md:358 | no quiz case |
| H-243 | b | Each is written before it is sent: a lost message loses nothing. | concepts.md:406 | no quiz case |
| H-314 | b | `<skill>` is the absolute folder of this file's parent. | concepts.md:556 | no quiz case |
| H-320 | b | Each agent's `description` ends with "Prompt starts with:" and its first line. | concepts.md:564-565 | no quiz case |
| H-387 | b | `cost` already shows the model of each transcript. | concepts.md:696 | no quiz case |
| H-401 | b | Within what you have, judge freely: what a red check means, what a note does to a round, which CR goes next, is yours to decide and say. | concepts.md:722-723 | no quiz case |
| H-433 | b | Every role holds this rule: [startup core](startup-core.md). | concepts.md:770-771 | no quiz case |
| H-440 | b | and a task left running wakes its owner each time it reports. | concepts.md:784 | no quiz case |
| H-441 | b | [driver](driver.md) and [foreman](foreman.md) say when each role stops its tasks. | concepts.md:784-785 | no quiz case |
| H-446 | b | The host's side of this is in your host's reference, section "Configuration" (the workers do not need it: their cards hold what they use). | concepts.md:793-795 | no quiz case |
| H-527 | b | The studio's Test plan item on requirements (SwRS, `just requirements-update`) is specific to that project and is left out; | pr-template.md:213-214 | no quiz case |
| H-528 | b | an Evidence item replaces it, as chantier's Verifier produces the before/after. | pr-template.md:214-215 | no quiz case |
| H-850 | b | Read only this card. | review-step.md:7 | no quiz case |
| H-853 | b | Ground rules: | review-step.md:13 | no quiz case |
| H-854 | b | Work only in the CR's worktree (`cd` there first). | review-step.md:15 | no quiz case |
| H-858 | b | Within what you have, judge freely. | review-step.md:19-20 | no quiz case |
| H-881 | b | The verdict covers that commit plus the uncommitted diff you reviewed. | review-step.md:55 | no quiz case |
| H-929 | b | What is proper to this host: the tools, the heartbeat, the sessions, and what only the user can do. | hosts/claude-code.md:3-4 | no quiz case |
| H-930 | b | The cards say what a role judges and point here. | hosts/claude-code.md:4 | no quiz case |
| H-931 | b | Read it with your card when you run on Claude Code. | hosts/claude-code.md:4-5 | no quiz case |
| H-932 | b | The host provides the role's named startup prompt and its declared tools. | hosts/claude-code.md:9 | no quiz case |
| H-938 | b | \| Generic \| Claude Code \| Mark \| | hosts/claude-code.md:20 | no quiz case |
| H-1006 | b | **The cost.** Even ignored, each event starts a turn of the steering session, which the user pays for. | hosts/claude-code.md:117-118 | no quiz case |
| H-1010 | b | Turning it off also loses Auto-fix for the user's own PRs. | hosts/claude-code.md:126 | no quiz case |
| H-1014 | b | A tip may come later, from a measure of the ignored turns' cost in a real batch. | hosts/claude-code.md:130-131 | no quiz case |
| H-1070 | b | The Foreman reads this file with its card. | hosts/claude-code.md:209 | no quiz case |
| H-1071 | b | A Driver reads the sections its card's "Opening reads" names ("Tools", "Auto mode", "Compacting", "The write guard"), when the step comes: "Auto mode" tells it what a refusal means and that it is reported, never worked around. | hosts/claude-code.md:209-211 | no quiz case |
| H-1073 | b | \| Tool \| Needed for \| Checked by \| Missing \| | hosts/claude-code.md:217 | no quiz case |
| H-1080 | b | The last three rows are not checked: a default the Driver of this change chose to keep, and may change on its judgment. | hosts/claude-code.md:226-227 | no quiz case |
| H-1175 | b | Each with why: | hosts/claude-code.md:457 | no quiz case |
| H-1252 | b | Why: long sessions with pauses past the cache's life. | hosts/claude-code.md:593-594 | no quiz case |
| H-1260 | b | It does not rely on the summary or on the model noticing. | hosts/claude-code.md:612-613 | no quiz case |
| H-1285 | b | A guard at fault costs nothing. | hosts/claude-code.md:660 | no quiz case |
| H-1293 | b | \| Class \| How it is known \| Can start a session \| Fit for a Foreman \| | hosts/claude-code.md:678 | no quiz case |
| H-1429 | b | What is not possible on the host (a fork that cannot be told apart) is written here as found, with no workaround. | hosts/claude-code.md:910-911 | no quiz case |
| H-1453 | b | What is proper to this host: the tools, the heartbeat, the sessions. | hosts/copilot.md:3 | no quiz case |
| H-1454 | b | The cards say what a role judges and point here. | hosts/copilot.md:3-4 | no quiz case |
| H-1455 | b | Read it with your card when you run on Copilot. | hosts/copilot.md:4 | no quiz case |
| H-1456 | b | The host provides the role's named startup prompt and its declared tools. | hosts/copilot.md:8 | no quiz case |
| H-1461 | b | \| Generic \| Copilot \| | hosts/copilot.md:19 | no quiz case |
| H-1547 | b | Report role, project, checked state, blocked actions and causes, pending permissions, authorized effects, evidence limits (failed, unavailable, not performed, available, documented, exercised, server-announced, not tested, skipped). | startup-core.md:22-24 | no quiz case |
| H-1549 | b | Before an action, read every reading the manifest lists for it; an unreadable one blocks that action only. | startup-core.md:27-28 | no quiz case |
| H-1552 | b | At boot read only the cores, your wrapper and the manifest's startup sections for your role; read the rest of a card only before an action whose readings name it. | role-core.md:3-4 | no quiz case |
| H-1553 | b | The host provides the documented Claude tools and hooks described by the deferred host reference. | host-core-claude-code.md:3-4 | no quiz case |
| H-1554 | b | The host provides the documented Copilot tools and agent sessions described by the deferred host reference. | host-core-copilot.md:3-4 | no quiz case |
| H-1590 | b | The startup reading is named by `startup-manifest.json`. | skills/chantier/SKILL.md:29 | no quiz case |
| H-1650 | b | Your startup reading is named by `startup-manifest.json`. | skills/status/SKILL.md:23-24 | no quiz case |

## Other round-2 work (see `## Hand-over checklist` of the inventory)

- P3: open kind-a rows (`open:` homes in `## Rows`) are round 2's work list
- P4: no `inf-<n>` case is written yet; the `inferable` rows with no case are round 2's
- P5: which host row is the program's untested host path is not confirmed
- P6: counted per rule only, not checked place by place against the base
- sc03: 7 of the 24 spans start a string literal; 7 sit inside a message and 10 cross literals, not checked as the message start
- sc06: the grouped cases are round 2
- sc08: not listed one by one; their rows carry a home or are open
- sc09-Q2: the "The CLI knows no role" sentence still differs from sc09's recorded wording; one-line edit in round 2
- sc13: not each read against `msg` and `inbox`; D-047 is open
- sc15: FM-473, FM-476 and FM-489 are open
- sc20-U: not written; round 2
- sc21-B1e: `judge` carries no image-replaced note (no "image" in commands/judge.py); foreman.md's Asks line says "(image notes too)"
- sc21-B6: no row is `removed: answer 8`; FM-B053 is kind a (it holds that line) and stays homed on foreman.md
- sc21-Q1: H-1360 is kind a, dropped by sc21-Q1 "default, to confirm by the owner"; open until the owner decides
- sc21-C: none written; round 2
- sc22-B: the answer 8 items 3 and 4 rows are not marked `removed:`
- sc22-J: J22 lacks the steering refused-rebase route and J11 holds only the force-push ladder; round 2
- sc22-C: a8-ask-settings-json, tracker-approval, griller-tracker-never and direct-brief-foreman are missing; round 2
- sc23-2: not re-read as a named pass in round 1
- sc24-2: not done as a named pass in round 1
- sc24-3: X-004 is open; the sync-offer, session-shell pointer and restart-offer sentences are not re-read
- evals/SCORECARD.md J11 and J22; the CONTRIBUTING.md line; stale card text.
- Auto-homed non-a rows: recheck a sample, some may not hold their rule (r1.md).
