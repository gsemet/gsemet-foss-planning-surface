# Fable review, appendix: the verdict for every file

Companion of `fable-review-plan.md` (2026-11-27, chantier main at 4d12a5b). A proposal: nothing here
is deleted or changed without the owner's word.

How it was made. The 296 topic pages were all read whole, by four helper readers (one per slice),
each applying the plan's tests (section 2 of the plan). The destinations marked `exists?` were not
checked in the CLI's source; `new:` means the command or line does not exist today. The root cards
were read whole for `floor`, `chief-of-staff`, `foreman`, `cr-driver` and `review-step`; the other
root files were read in part or judged from their headings and size (marked "sampled").

Verdicts: `DELETE-inferable` (the model does it alone, or the CLI's output says it), `DELETE-dup`
(said elsewhere), `DELETE-stale` (history, trial notes, removed output), `CLI` (mechanical: a
command, a refusal or a `next:` line carries it), `KEEP-card` (a line of the role's card),
`KEEP-guide` (a rare case that needs judgement: one page per theme).

## A. Root files, host files, forge files

| file | bytes | verdict | destination | reason |
|---|---:|---|---|---|
| floor.md | 554 | KEEP | floor.md, at most 14 lines | The ten rules nothing overrides. Add the few protective lines of plan section 5. |
| chief-of-staff.md | 6,040 | KEEP, rewrite | at most 5 KB | Holds the right things, but packed too tight to read; its list of 29 "rare cases" goes (the CLI names the guide at the moment). |
| foreman.md | 4,465 | KEEP, rewrite | at most 4 KB | Same. "Never 3" is one 900-character sentence: becomes refusals of the steering push and rebase. |
| cr-driver.md | 5,099 | KEEP, rewrite | at most 4 KB | Same. Its list of 19 topics goes: `next <cr>` names the guide. |
| stack-driver.md | 4,854 | KEEP, rewrite (sampled) | at most 4 KB | Same family as cr-driver. |
| release-driver.md | 4,716 | KEEP, rewrite (sampled) | at most 4 KB | Protects irreversible actions: the densest protective card. |
| qa-driver.md | 1,776 | KEEP (sampled) | as is | Short. |
| coder, conflict-resolver, debugger, investigator, spec-writer, spec-critic, retro-critic, demo-explorer (8 files) | 12,483 | KEEP (sampled) | as is | 1.3 to 1.7 KB each: already what a card should be. |
| inspector.md, verifier.md | 5,166 | KEEP (sampled) | as is, plus the lines of the `KEEP-card` worker pages | The two checkers; their pages below fold in. |
| review-step.md | 1,515 | KEEP | as is | The contract of a project's own review step. |
| griller.md (the board's Griller) | 1,946 | KEEP (sampled) | as is | |
| griller-skill.md (the Griller session) | 3,652 | KEEP (sampled) | as is | |
| concepts.md | 26,543 | split | `help words` (3 KB) + delete | "Words" is a real glossary (keep, shortened). "Starting an agent" and "A Driver's prompt" describe what `brief` now does (stale, per CR-510's gaps). The rest repeats `--help`. |
| routing.md | 4,826 | CLI, then delete | the CLI prints and checks each line | A table of line formats the CLI already prints (`order`, `asks`, `handback`); the rest is the refused-push route. |
| status-layout.md | 11,576 | CLI | `status --report` prints the report, filled | A fixed layout "read whole before every report": the clearest case of a format that code should print. Keep 1 KB: what the Chief of Staff adds. |
| pr-template.md | 12,170 | split | `pr body` writes the factual parts, `pr check` runs the audit; 4 KB of writing rules stay | Batch-31's retro: PR bodies came back NOT VERIFIED on facts the record holds. |
| release-template.md | 7,083 | KEEP, trim (sampled) | at most 5 KB | Writing judgement (release notes for people). |
| init.md | 6,213 | KEEP, trim (sampled) | at most 4 KB, absorbs `init-checks`, `init-tools` | A guided tour for a person: instruction by nature. |
| sync-checkout.md | 1,862 | CLI, then delete | the launcher's `--sync` | AGENTS.md says the launcher already runs the checked sync; chantier's own dev rule, shipped to every project. |
| ticket-summary-example.md | 1,352 | merge | guide `tickets` | An example is worth keeping, inside its theme. |
| topics.json | 67,004 | shrink | about 4 KB | 240 entries become about 24; no `review_by`, no aggregate entries. |
| hosts/claude-code.json | 25,940 | KEEP, never whole at boot | 50 rows, plus about 10 from the `host-*` pages | What a model cannot know (this host's tool names). 37 of 50 rows are marked untested. |
| hosts/copilot.json | 23,059 | KEEP on disk | same rows | All 50 rows are marked untested. Never loaded on Claude Code. |
| hosts/claude-code.md | 23,477 | CLI | `preflight` prints the rules to add (`allow_samples.py` already holds them) | The allow-rule table exists twice, in this file and in the code. Move the table to `docs/`. |
| forges/github.md, gitlab.md | 1,209 | KEEP | as is | |
| skills/chantier/roles.yaml | 13,503 | KEEP, extend | gains `guides:` and `commands:` per role | The role index becomes the one index of what a role may load. |
| the four SKILL.md | 14,063 | not read | | Not reviewed. |
| agents/ and com.github.copilot/agents/ wrappers | not measured | not read | | About 1 KB each; the program's study found them not to be the problem. |

## B. The 296 topic pages, by family

| page | bytes | verdict | destination | reason |
|---|---:|---|---|---|
| **Host notes (Claude Code, Copilot)** | | | | |
| host-allow-add | 1380 | CLI | same command; it prints the fallback text when the edit is refused | Instructions around the one-liner; unproved |
| host-allow-add-lines | 1558 | CLI | new: `preflight --add-rules` merges the P10 rules itself, on the user's yes | Two shell one-liners that edit JSON: exactly what code should do |
| host-allow-broad | 1530 | CLI | P10 output already names broad/stale rules and replacements | Describes P10's print; keep 1 rule: never remove a user's rule (card) |
| host-allow-extra | 812 | DELETE-stale | docs/proofs | Design rationale and an unused unproved MCP rule; nothing to act on |
| host-allow-not-add | 637 | DELETE-stale | docs/proofs | Host doc trivia; P10 simply does not propose these rules |
| host-allow-rules | 1547 | DELETE-inferable | docs link in a `host` row | Host's documented matching rules; P10 does the matching |
| host-allow-rules-copilot | 348 | DELETE-stale | `host` row "allow rules: none recorded" | Says nothing is known |
| host-auto-fix | 1595 | KEEP-guide | `host auto-fix` row, cut to 4 lines | Real quirk and protection: an Auto-fix event is no order, never merge the base in |
| host-auto-mode | 1459 | DELETE-stale | one `host` row: one command per call; report a refusal verbatim | Classifier lore, mostly unproved; `chantier push` replaced the problem |
| host-auto-mode-steering | 1542 | DELETE-stale | the first-turn alert, if kept, printed by `preflight` when the rule is missing | Mostly unproved speculation; `push not tried` contradicts floor 9 |
| host-auto-mode-trials | 1580 | DELETE-stale | docs/proofs | Trial epistemology and unproved lists; no action for an agent |
| host-claude-only | 198 | DELETE-dup | `host` prints "not recorded on this host" itself | Boilerplate filler |
| host-compact | 1275 | KEEP-guide | `host compact` row, 3 lines | Recommended settings are a host fact; reload line dups `reload` |
| host-compact-copilot | 408 | DELETE-dup | `host compact` row | Says only "unknown; reload by hand" |
| host-configuration | 1545 | DELETE-dup | preflight P5/P9/P10 output | Describes preflight; keep the PowerShell 5.1 `--jq` quirk as one host row |
| host-configuration-copilot | 1253 | DELETE-stale | `host` rows | "All unproved"; the known-issue list is history |
| host-driver-silence | 1330 | KEEP-guide | `lost-driver` guide (3 lines) | Key quirk: a Claude Driver is silent until its end; silence never starts a second one |
| host-for-you | 1325 | DELETE-inferable | one CoS card line: where/do/paste/expect, say "not tested" | Formatting recipe for user instructions |
| host-for-you-sessions | 975 | DELETE-inferable | — | A model can explain "start a new session, paste this"; all unproved |
| host-foreman-worktree | 666 | DELETE-dup | foreman.md Start (worktree check) and its ask | Already the Foreman's start stop; the CoS explains alone |
| host-heartbeat | 1375 | CLI | `host heartbeat` row; `status --stop-heartbeat` prints "cancel the wake" | Arming recipe = a host row; keep the /loop no-interval quirk there |
| host-heartbeat-copilot | 1309 | CLI | `host heartbeat` row + `playbook` timing | Arming recipe; row data, not a page; unproved |
| host-refused | 1274 | KEEP-guide | `host refused` row: the report-file-name quirk only | One real quirk (a subagent's `report*.md` write is refused); rest is design |
| host-remote | 1466 | KEEP-guide | `host start-session` row, 3 lines | Real quirk: a Remote Control start takes no cwd/preset; rest unproved |
| host-reuse-foreman | 943 | DELETE-inferable | 2 lines in the `host start-session` row | A cost trade-off a model weighs alone; closed-session wake unproved |
| host-sessions | 1482 | CLI | `preflight` P1/P6/P7 classify the session; print the class and its fit | A table of what preflight computes |
| host-sessions-copilot | 623 | DELETE-stale | `host` row | "Nothing else recorded" |
| host-sessions-more | 1196 | DELETE-stale | the message limit (10) as one host row | All unproved; only the inter-session message limit is usable |
| host-subagent-signs | 1347 | KEEP-guide | `lost-driver` guide / host row `subagent-signs` | Exact host notices and their meaning cannot be inferred |
| host-surfaces | 1584 | DELETE-inferable | — | Option matrix mostly unproved; a model adapts to where the user is |
| host-turn-end | 1600 | KEEP-guide | `host turn-end` row, 3 lines, in the CoS brief | Real costly quirk: a turn-end notice must trigger no tool call |
| host-write-guard | 1224 | DELETE-dup | the hook's refusal text; dev docs | Hook implementation description |
| host-write-guard-shell | 1391 | DELETE-dup | the hook's own refusal text; dev docs | Documents hook internals; the refusal says where to write |
| **Refused push or rebase** | | | | |
| refused-answer | 1010 | CLI | `next --epoch` for `blocked waits: push/rebase` prints the restart take with the answer | Fixed way back; "never ping" follows from the blocked state |
| refused-forge-chain | 807 | DELETE-dup | chief-of-staff.md "Settles alone" 3-4 | Card already holds the rule and rail; page repeats it. |
| refused-push | 1559 | CLI | `chantier push` exit 4 text names the two notes and the hand-back; new: `handback blocked --refused-push` fills the shas | Two fixed four-step recipes; the card already says never retry, never raw push. |
| refused-push-answer | 1086 | CLI | the `take` note's own text plus `next <cr>` | A lookup table from note prefix to next step. |
| refused-push-chief-more-p1 | 1166 | KEEP-guide | refused | User-facing part of a not-legitimate push; shrink to 4 lines; answer formats to CLI. |
| refused-push-chief-more-p2 | 513 | DELETE-dup | CoS card rail ("run it once on the yes") | Repeats the card: once, unchanged, never another form. |
| refused-push-chief-p1 | 1502 | CLI | new: steering form of `push` (check, note, push, answer line) | Fixed sequence; judgement part is small. Never a non-chantier or default branch: card rail, best a refusal. |
| refused-push-chief-p2 | 597 | CLI | same command prints the answer line | Answer formats and routing are mechanical; failed lease is card rail. |
| refused-push-gate | 1198 | CLI | new: `chantier push <cr> --as-steering --epoch <n>` (checks, pushes, answers) | Skips and refusals are record lookups the command can make. |
| refused-push-judgement | 1041 | CLI | new: same command (ancestor, `git cherry`, gate pass at sha: all computable) | The "judgement" is three git checks and one events lookup. |
| refused-push-route | 1209 | CLI | new: same command; `preflight` P10 read by code | A command form and an allow-rule lookup. |
| refused-push-run | 1179 | CLI | new: same command prints the line to send and records the note | Fixed notes and message strings per outcome. |
| refused-push-steering | 1506 | CLI | new: same command refuses a non-`chantier/*` or default branch (the `push` rails already do) | Hard checks on branch name and handoff: the rails `push.py` already holds. |
| refused-rebase | 1145 | CLI | same subcommand: branch/base check as its refusal | A "hard refusal" check written in prose is a rail |
| refused-rebase-chief | 1262 | CLI | new: steering `rebase <cr>` (tie, clean, fetch, rebase, note, answer) | Fixed sequence with fixed answers; card item 2 holds the rule. |
| refused-rebase-run | 856 | CLI | new: steering `rebase <cr> --epoch` runs fetch+rebase with rails and notes the result | One guarded command and fixed notes: a subcommand like `push` |
| **Stack batches** | | | | |
| merge-github | 672 | CLI | new: `release merge <cr>` does the stack lookup and the merge-async poll | Raw API recipe, unproved by an agent; needs an AGENTS.md exception |
| merge-series-stack-p1 | 1324 | CLI | `order mode` printed line (exists); `judge` names the next PR | Describes what a series or mode switch does; CLI prints it. "Never merge for the user" is floor 1. |
| merge-series-stack-p2 | 1372 | CLI | new: `asks`/`judge` refuse a mismatched alone ask (asks already refuses per-CR in a stack) | Hand check of an ask against the shape line is a rail; last sentence dup of floor. |
| merge-stack-gitlab | 1285 | DELETE-stale | forges/gitlab.md one line; `forge-stack show` wording | Marked unproved throughout; merge-train check could be a forge read in `order merged`. |
| merge-stack-ready-p1 | 1469 | CLI | `forge-stack show` + `judge` word the stack ask whole | Says how to phrase what the CLI already computes (five checks, `partial stack mergeable below`). |
| merge-stack-ready-p2 | 1497 | CLI | `judge` adds heavy-CI and waiver clauses; rebuild refusal already names the next command | 1 line KEEP-guide (heavy CI at top only, user's choice); rest is wording. |
| retake-stack | 1826 | CLI | `ship` refusals (exist, quoted) and `take`'s `base` line | Restates two refusals and how to read `take`; refusals should carry the next command. |
| stack | 1425 | KEEP-guide | `stack` guide (6 lines) | The model of a stack batch; needed once, not inferable |
| stack-asks | 1092 | CLI | `judge stack --record` words `stack-ready-to-merge` from `forge-stack show` and the record | A long ask format assembled by hand from the record: error-prone |
| stack-changes | 2362 | KEEP-guide | `stack-driver`; new: `stack plan` prints the `rebase --onto` commands | Insert and drop sequences are computable; what to do with a dropped PR is a protection. |
| stack-changes-chief-p1 | 1265 | CLI | `order drop`/`order add` printed line says the consequences; new: insert drafts the PRs above | What-to-tell text belongs in the order's output; draft-first step is a rail. |
| stack-changes-chief-p2 | 1067 | CLI | `order hold` output; release refusal while held or parked | Consequences text; keep 1 line: ask when "held" or "out" is unclear. |
| stack-checks | 1468 | CLI | `forge-stack show` checks; `next:` prints `take stack --note "<failed check>"` | Describes command output; the insert sequence is `next` advice |
| stack-deliver | 1008 | KEEP-guide | `stack` guide (4 lines) | Real judgement: which CRs to start to meet a time |
| stack-drop | 1374 | CLI | `order drop` in a stack prints the fan-out lines | Fan-out recipe; the heavy-CI relay is a fixed line |
| stack-ends | 760 | CLI | `next --epoch` maps each stack-driver end to its take | Three fixed mappings |
| stack-gate | 1182 | CLI | `next stack`; new: `handback stack` builds the hand-back line | Line format and lease flags are mechanical; "a failed gate leaves it a draft" is one line. |
| stack-grows | 1422 | CLI | `status`/`next` already print `take stack now`; `take` computes bases | Describes the CLI; keep "never correct a base by a note" in the guide |
| stack-hold | 2240 | KEEP-guide | `stack-driver` | Hold, park, conflict needing code: abort, push nothing, anomaly. Sequences to `stack plan`. |
| stack-joins | 1476 | KEEP-guide | `stack-driver` | "Never leave a rebuild half done before a deadline" is judgement; the rest to `next stack`. |
| stack-make | 1749 | CLI | `forge-stack show` prints the five checks (exists); `next stack` | The five checks are already code; the page lists them again. |
| stack-merge | 1465 | KEEP-guide | `stack` guide (4 lines) | "A choice you make per merge": restack or rebase notes |
| stack-outside | 994 | KEEP-guide | `stack` guide (2 lines); `asks --outside-stack` already needs an order | Protection: never `--outside-stack` on your own judgement |
| stack-record | 1239 | CLI | `ship` refusals (exist); new: `ship` records the `restack:` note itself | Refusal answers and note strings. |
| stack-restack | 1839 | CLI | new: `stack check` runs the `merge-base --is-ancestor` chain; `stack` output | Chain check and ordering are computable; "who moves a branch" is 1 line KEEP-card. |
| stack-run | 1283 | DELETE-dup | foreman.md Starting Drivers; `take stack` output | The start rule is in the card; the rest describes the concept (see stack) |
| stack-takes | 943 | CLI | `take stack` prints the note line for each `not on its place` row; `next` says when the final-order take is due | Fan-out and a due condition |
| **Release** | | | | |
| release-chief-after-p1 | 1331 | KEEP-guide | release | `publication done` only from the user's own words: protective; shrink to 3 lines; rest relay mechanics. |
| release-chief-after-p2 | 964 | CLI | new: `release issues <cr>` lists shipped `issue:` lines; `status` draft link | List-building is mechanical; keep 1 line: one yes for the list, auto never covers comments. |
| release-chief-approve-p1 | 1167 | KEEP-guide | release | Ask the post-merge word with the merge go, per step; `judge` could word it. 3 lines keep. |
| release-chief-approve-p2 | 525 | CLI | new: an order form for "wait" that is not a take | Text documents a CLI quirk (`order note` on a ready CR is a take); fix the quirk. |
| release-chief-auto-p1 | 1278 | CLI | `order grant` refusal (no budget; exists?) + `next:` | Numbered procedure; "auto only from the user's own word" is card ask-first 3. |
| release-chief-auto-p2 | 589 | KEEP-guide | release | What auto covers and never covers: protective scope; 3 lines. |
| release-chief-p1 | 1477 | KEEP-guide | release | Judgement: where the procedure is, gaps are questions, why a release joins a stack; halve it. |
| release-chief-p2 | 1276 | CLI | `order add --release`, `order confirm` refusals; grant line | Mostly restates CLI rails; report.md/conversation.md copy step is doubtful, drop or automate. |
| release-end | 984 | CLI | `next <cr>` after `release published` (checklist) | An ordered checklist the CLI can print; the retro line format is `retro draft`'s. |
| release-evidence | 1474 | KEEP-guide | `release-driver` (merge into release-template.md) | Editorial judgement on pictures; belongs with the release template, cut by half. |
| release-merged | 2854 | KEEP-guide | `release-driver` | Held steps, the main-checkout step, publication by someone else: irreversible actions, real protection. |
| release-notes | 2063 | KEEP-guide | `release-driver` (merge with release-evidence) | "Files are the source, body a copy", no agent posts; half is forge mechanics to cut. |
| release-ship | 2315 | KEEP-guide | `release-driver` | New attempt never by `reset --hard`, half-done irreversible work: stop. `ship` refusals to CLI. |
| release-stale | 979 | KEEP-guide | `release` guide (4 lines) | Judgement: a content change makes a release stale; a defect goes to its CR |
| release-tag | 956 | CLI | `next:` on the `blocked waits: steering runs <step>` hand-back prints the command; notes automatic | Fixed step; the card keeps "run only what the Driver handed back, never force" |
| release-take | 1498 | CLI | `take <release>` builds the note from `handoff`'s `approvals unused:` itself | A note assembled from the record is code |
| release-thread | 405 | DELETE-inferable | release-template.md if wanted | Marketing style advice a model writes alone; "no agent posts" is in release-notes. |
| **Direct mode** | | | | |
| direct-mode-accept-p1 | 1430 | KEEP-guide | direct | What is refused while steering directly (no grill, no demo) is a policy; half is CLI refusals already |
| direct-mode-accept-p2 | 685 | CLI | `next --epoch` at the pause (exists) lists fast-forward, retro, report, close | Pause sequence is the Foreman brief's plus `next` |
| direct-mode-back | 903 | KEEP-guide | direct | Stop own Drivers before the Foreman claims (no two Drivers on one CR); better a `foreman set` rail (new) |
| direct-mode-epoch-p1 | 967 | CLI | usage refusals (exit 2) already say when `--epoch` is required or refused | A list of which commands take a flag: `--help` and refusal material |
| direct-mode-epoch-p2 | 923 | DELETE-dup | `cost --explain` | Explains cost rows; the Write/Edit-tool coupling should be fixed in the cost code |
| direct-mode-p1 | 1208 | DELETE-dup | foreman brief, `help lease`, chief card | "Do as the Foreman card says" plus lease, escalation and title repeats |
| direct-mode-p2 | 1472 | CLI | `foreman set` output `next:` (rules, start Drivers from `brief:`); `take` prints `brief:` (exists) | Start sequence the commands already print; "a Driver's work is never yours" is in the card |
| direct-mode-p3 | 538 | DELETE-dup | chief card, Direct mode and settles-alone | Nothing sent to yourself: inferable; refused push in the card |
| direct-mode-switch-p1 | 1237 | CLI | new: one takeover command does the transcript pre-check and the Foreman-alive test | 9-step procedure with record compares; keep "user's word only" |
| direct-mode-switch-p2 | 1314 | KEEP-guide | direct | Never assume a stopped session ended its children; stop a Foreman only on the yes (~500 B) |
| direct-mode-switch-p3 | 717 | CLI | same takeover command; `foreman set` output | Claim steps and what the output must show |
| direct-mode-switch-p4 | 1423 | CLI | same takeover command prints the restart list; `take --note resume:` | Mechanical restart loop per ended Driver; "never the word epoch" kept by the CLI printing "Foreman n°" |
| **Lost Drivers, leases, recovery** | | | | |
| handover | 937 | CLI | new: `order mode direct` (or `foreman handover`) prints the stop sequence; seat check a refusal | Fixed sequence; the seat check is mechanical |
| lease | 1436 | CLI | `--lease` refusals, `lease <unit>` output (source names `help lease` 6 times) | Every case is a CLI line; the refusal can say the next command itself. |
| lease-steering | 1383 | CLI | `next --epoch` already names a stale lease; `access` explains | Says when to run `agents set -`; keep "reclaim a live lease only on the user's word" (in foreman.md). |
| lost-context | 1271 | CLI | `next --epoch`: "blocked context: restart" with the exact take; counts the second | Fixed restart path and a counter |
| lost-driver | 1373 | KEEP-guide | `lost-driver` guide | Alive/ended/suspect is judgement; merge with silent, outside and host signs |
| lost-outside | 1502 | KEEP-guide | `lost-driver` guide (4 lines) | Protective: clear the id on a stop; restart without asking; rest is counting |
| lost-restart | 1499 | CLI | new: `restart <unit> --cause …` = clear id + handoff + take resume; counters in the record | Four-command sequence repeated in 8 pages; counting is code |
| lost-silent | 1068 | KEEP-guide | `lost-driver` guide | Proof of death and "never record a hand-back yourself" |
| recovery | 1468 | KEEP-guide | lost-driver | Prove the Foreman alive before reporting; resume recipe should be `next` output; `cancel` line dup of card. |
| restart | 1183 | CLI | `take` prints the resume point; `next <cr>` (first closing step with no note) | Where to resume is computed from the log; "do not reread the spec" is one card line. |
| seat-handover | 1376 | KEEP-guide | session | Seat moves only on the user's word; never stop a Driver; shrink to 5 lines, lines to `seat take` output. |
| take-back | 1505 | KEEP-card | foreman.md (already there); the id shuffle goes to `take`/`restart` | Core rule already in the card; the rest is mechanical |
| **Grill, backlog, tickets** | | | | |
| grill-backlog-p1 | 1310 | KEEP-guide | grill | Record every answer at once (owner's rule) is KEEP; command forms are `--help`; sweep = `summary lint` `next:` |
| grill-backlog-p2 | 740 | KEEP-guide | grill | Where artifacts go in a CR folder (4 lines); triage outcomes are the user's call |
| grill-critic | 1398 | KEEP-guide | grill | When a critic is worth its cost: judgement; merge with -steps into ~900 B |
| grill-critic-steps | 1460 | KEEP-guide | grill | Fix-versus-question sort of critic findings is judgement; steps 2 and 6 are `brief spec-critic` |
| grill-example | 1152 | DELETE-inferable | - | A worked multiple-choice question; the model needs none |
| grill-options | 1245 | KEEP-guide | grill | Options format and the "grilled enough?" choices: a user-facing convention the owner set; ~500 B |
| grill-outside-pr | 1416 | CLI | new: `file --archive-pr <link>` (reads the forge, writes the archive folder and summary) | Folder name format, file template, gh fields: a command, rarely used |
| grill-restate | 1179 | KEEP-card | griller.md and chief-of-staff.md | "Grilled enough?" only after a full restatement; never decide alone; the 10 MB case to DELETE |
| grill-series | 1492 | KEEP-guide | grill | Core grill convention (one item per call, references, text first); owner-tuned; trim to ~800 B |
| grill-specify-p1 | 1438 | CLI | new: `brief spec-writer <folder>` writes `work/specifying`, enforces `specifying.parallel`, prints the prompt | Marker file, limit and restart are mechanics; KEEP 1 line: review the spec against the answers |
| grill-specify-p2 | 700 | DELETE-dup | `cost`, `triage --help`, griller card | Cost row facts and the Griller's one message line |
| grill-surface | 1072 | KEEP-card | chief-of-staff.md (has the never) and griller.md | Another project's CR needs the user's word: protection already in the card; rest dup |
| griller-cost | 231 | DELETE-dup | `cost` output | 231 bytes saying a cost row exists |
| griller-worktree | 1195 | KEEP-guide | grill (Griller-only section) | Real constraint (worktree never merged, files handed over); rare; ~500 B; better a refusal of `triage`/`summary` there |
| ticket-summary-p1 | 1479 | KEEP-guide | grill (ticket section) | What an outside reader gets, what never leaks (CR ids, cost): judgement and privacy; halve. |
| ticket-summary-p2 | 1189 | KEEP-guide | grill (ticket section) | Privacy check and "no yes, nothing posted" protective; style advice inferable. |
| ticket-summary-post-p1 | 1493 | DELETE-stale | - | Every route marked unproved; a model knows `gh issue comment --body-file`. Keep "from a file, never retried". |
| ticket-summary-post-p2 | 676 | KEEP-card | chief-of-staff.md (already there) | Issue closing only by the PR's line is in the card; follow-up line is one guide sentence. |
| where-cr-goes | 1462 | CLI | new: spec-final check in `triage`; `order add` refusal `next:` | Deterministic routing once the user answers; keep 1 line: the destination is the user's answer. |
| **Starting a batch** | | | | |
| allow-rules | 1356 | CLI | new: `preflight --add-allow-rules` (merges exactly P10's rules on the user's yes); P10 prints the question text | Mechanical JSON merge; "only on the yes, nothing else in settings" is already in the card |
| allow-rules-more-p1 | 1496 | CLI | preflight P10 output: print the broad/stale warning and the "what stops without it" sentence per capability (new: wording) | Fixed sentences per capability; 1 line KEEP-card: never remove or edit the user's rule |
| allow-rules-more-p2 | 387 | DELETE-dup | floor 9 + host row allow-add | Refused edit = report exact text; already floor 9 and a host row |
| batch-plan | 1502 | CLI | `preflight` (runs P1..P14); `next:` after preflight names plan then open | Checklist the command already runs; its 2 protective lines are in the card |
| batch-plan-cut-p1 | 1273 | KEEP-guide | batch-start | Judgement: the cut to fit a time; depends only for a real need; depends.json format belongs to `open`'s refusal |
| batch-plan-cut-p2 | 1031 | KEEP-guide | batch-start | Same-lines wait is judgement, 3 lines; rest inferable |
| batch-plan-mode-p1 | 1502 | KEEP-guide | batch-start | Recommending parallel/series/stack is judgement; gh-stack detail to `forge-stack`/P9 output; GitLab "unproved" |
| batch-plan-mode-p2 | 1427 | CLI | `preflight` prints the steering mode this surface can run and why (exists? partly, P1/P2); new: `open --mode` mandatory | Mode detection is mechanical; "never parallel by default" = remove the default |
| batch-plan-mode-p3 | 1103 | CLI | `preflight --mode foreman` refusal; the plan line comes from preflight | Wording of one plan line; forced-mode refusal is a preflight rail |
| batch-plan-show-p1 | 1095 | CLI | new: `plan` (or `open --dry-run`) prints CRs, waits, slots, budget, team, steering | A fixed list of facts all read from playbook and the record; the model adds the reasons |
| batch-plan-show-p2 | 731 | CLI | `order waive --help`; the new plan output handles the empty batch | Command forms; 1 line KEEP: a waiver quotes the user's words, never a brief note |
| config-p1 | 1401 | CLI | `playbook --help`, `playbook` output and validation errors (exist) | Config key reference; the CLI validates and resolves; 1 line KEEP-card: edit chantier.yaml only on the user's word |
| config-p2 | 1143 | DELETE-dup | `playbook` output, P12 refusal | Role list and start ways are printed by playbook; "never fix the file yourself" to the card |
| config-p3 | 1108 | CLI | `preflight`/`playbook` `Needs:` lines print the missing-skill warning (Needs: exists) | Comparing named skills with the session is a check; wording fixed |
| delivery-time-p1 | 1455 | CLI | new: `status` and the plan print `floor:` (lock term, chain term, critical path) from events.jsonl | A formula over the record computed by hand today: the clearest CLI move of this slice |
| delivery-time-p2 | 884 | CLI | same `floor:` line (CI time from the hub, or "unknown") | Formula and example; the one protective line (no time promised but from the floor) is in the card |
| foreman-start-more | 1134 | DELETE-stale | host rows (reuse-foreman, foreman-worktree) | Duplicates host pages; edge cases, partly unproved |
| foreman-start-p1 | 933 | CLI | `open --help` and `open` output `next:` (record approved waits, complete brief.md) | A usage line copied into a card; open already refuses and prints |
| foreman-start-p2 | 1206 | CLI | new: `brief foreman` prints the whole Foreman start prompt (title, CLI line, Team, Needs) | A prompt skeleton assembled by hand from playbook output: what `brief` exists for |
| forge-permissions-gitlab | 861 | DELETE-stale | - | "All unproved"; if wanted, it is code in P9, not text |
| forge-permissions-p1 | 1415 | CLI | new: `preflight` P9 runs the gh probes itself (read-only forge reads; needs an AGENTS.md line) | Three fixed API probes and their reading: pure mechanics |
| forge-permissions-p2 | 1299 | CLI | same P9 probes (stacks API, default-branch rules, merge methods) | Same; the warnings are fixed sentences |
| forge-permissions-say | 839 | CLI | the P9/P10 output is the block to pass on | Wording of what the probes found |
| init-checks | 1498 | KEEP-guide | init.md (fold in) | Tour content: propose fast and long gate lines; read only on `init`; drop the topic |
| init-tools | 1492 | KEEP-guide | init.md (fold in) | Install offers on the user's yes; allow-rules part is dup |
| project-rules-p1 | 1189 | CLI | `preflight`/`rules` output and `next:` | Start sequence is mechanical; "absent gate never means success" and source-of-fact rule dup of cards. |
| project-rules-p2 | 1096 | CLI | new: `playbook` line proposes the exact `chantier.yaml` lines (it already prints `none named`) | Proposing lines is mechanical; "write on the user's yes" is card ask-first 1. |
| trials-p1 | 1069 | CLI | new: `preflight --trials` prints the exact trial commands for this batch | List derivable from the batch options; the agent runs them, the CLI prints them. |
| trials-p2 | 710 | CLI | new: `open --trial` records the "Permission trials" section | Record format; keep 1 line: a refusal never blocks the go and is said at once. |
| **Ending a batch** | | | | |
| batch-close-p1 | 1315 | CLI | `close` (check form prints the bilan); new: `close --yes` removes the listed worktrees/branches itself | Procedure; "only on the yes" is in the card |
| batch-close-p2 | 1248 | DELETE-dup | `close` refusals name each cause | Restates the refusal list; "report, do not loop" is floor 9 |
| batch-close-stopped-p1 | 1434 | KEEP-guide | batch-end | `--stopped` only on the user's yes per named agent: real protection; rest is `close` refusal text |
| batch-close-stopped-p2 | 498 | DELETE-stale | - | Copilot lease residue (unproved host); trash-restore duplicates `restore` |
| batch-pause | 1402 | CLI | `next` (chief view) after `final`: read retro, Completion report, offer close (exists? partly) | Sequence already in the card's End paragraph; heartbeat sentence is a host row |
| cleanup | 685 | CLI | end-of-batch cleanup exists; `next --epoch` prints the remove commands for a `kept:` CR | Two git commands; "never remove a trashed/backlog worktree" already foreman Never 6 |
| demo-p1 | 1242 | KEEP-guide | merge (demo offer) + `brief demo-explorer` | Own subagent never implements (card has it); stale hand-built `Read <skill>` prompt form |
| demo-p2 | 540 | DELETE-inferable | - | How to walk a user through a demo; the model does it |
| retro | 1234 | KEEP-guide | `retro` guide (5 lines) | project vs chantier tagging and judging points; the sequence is `next` |
| retro-critic | 1352 | KEEP-guide | `retro` guide (4 lines) | The brief gives evidence, never your argument; a failed critic: `retro not checked` |
| retro-critic-write | 612 | CLI | `retro draft --write` / new `retro apply` writes the kept and dropped files | File formatting; "follow the verdicts as given" one card line |
| retro-lines | 1067 | DELETE-dup | `retro draft` lists problems from events; last bullet dups orders-queue | The draft is generated; the tag rule is in retro.md |
| retro-route-chantier-p1 | 1465 | KEEP-guide | retro | Public-issue privacy check (step 4) is protective; steps 1-3, 5 mechanical: new `retro issue draft`. |
| retro-route-chantier-p2 | 442 | CLI | new: `retro issue post` (or 1 line: post only on the yes) | Two mechanical steps. |
| retro-route-p1 | 1076 | CLI | `retro` output header; `file` | Wording of critic counts; keep 1 line: a chantier point is never filed in another project. |
| retro-route-p2 | 1050 | KEEP-guide | retro | Own-initiative change lists go through the retro-critic first: judgement rule; self-repo detection is CLI. |
| **Merge and asks** | | | | |
| ask-lines | 1022 | CLI | `asks <kind>` validates the kind and prints the line; `judge`/`next`/`conflicts` already word theirs | Fixed line formats; one rule (an image incident rides the CR's ask) to foreman card |
| asks | 661 | DELETE-dup | `asks` output + chief card | Mark an ask read when relayed: `asks` can print that as its `next:` line |
| local-gate | 1248 | CLI | `judge` computes owed/passed and refuses the ask; `next` prints the `take … --note "long gate: …"` | Record lookup and fixed notes; the protection is `judge` refusing |
| long-gate | 1266 | KEEP-guide | `gates` guide (5 lines) | Judging whether an exemption holds against the project's rules is judgement |
| long-gate-waiver | 1331 | CLI | `judge`/`handback` check the waiver order from the record; `order waive --help` | Pure record check; a waiver's scope is data |
| merge | 1507 | CLI | `order merged` prints, per CR, the exact `take`/note line (it already prints `restack owed`) | Per-mode fan-out computed from the record |
| merge-gaps-p1 | 1465 | CLI | `judge` wording (exists) carries the gaps and the local-gate clause; the chief relays it unchanged | The rule is "quote the ask as worded"; KEEP-card 1 line: never drop a gap when relaying |
| merge-gaps-p2 | 1393 | KEEP-guide | merge | Screenshot/leak asks are judgement; 3 lines keep, local-gate clause quoting is CLI (`judge`). |
| merge-recorded | 1353 | CLI | watcher line `next: order merged <cr>` (exists in hub line); new: `order merged` accepts a taken-out CR by PR | Recording sequences are mechanical; "parallel: first ready wins" is inferable. |
| merge-under-grant | 1186 | CLI | `release go` already gates; `release merge` runs it; card keeps Never 1 | Conditions are a refusal; the API steps are code |
| merge-words-p1 | 1075 | CLI | `status` `label` and `handed back:` words (exist) | Vocabulary and icons are copied from CLI output; 1 card line: "ready to merge" only when mergeable now. |
| merge-words-p2 | 862 | KEEP-card | chief-of-staff.md | "You can merge" only after the ready-to-merge line reaches you: protects the user (CR-510 incident). 2 lines. |
| ready-asks | 367 | DELETE-dup | `asks`/`judge` print `superseded by` | Explains CLI output |
| **Session, seat, board, watcher** | | | | |
| board-lines | 1508 | DELETE-dup | the board's own start lines | "Pass each line on as printed": the lines explain themselves; never stop it yourself is floor 10 |
| board-p1 | 1414 | KEEP-guide | board | What the board is, who may start it, stop only on the user's word; trim to ~600 B |
| board-p2 | 531 | DELETE-dup | chief card (never another port; another session's board is the user's) | Both rules already in the card's Never list |
| board-restart | 1455 | CLI | the `board runs another build` line carries the offer and the `serve --restart` command (line exists; cost sentence new) | One yes per restart is in the card; new-key is `serve --help` |
| compacting-p1 | 1220 | DELETE-inferable | - | Tips and compaction advice: UX garnish the model does alone; exists only as card text |
| compacting-p2 | 720 | DELETE-inferable | - | Example tips; decoration |
| cost | 295 | DELETE-dup | status-layout.md "Cost"; chief card | Pure pointer page |
| first-turn-p1 | 1347 | KEEP-guide | session (or a user doc read on "what is chantier?") | Newcomer intro; shrink to ~600 B |
| first-turn-p2 | 1020 | DELETE-dup | first-turn-p1, README, AGENTS.md | Same intro continued; example phrases |
| options | 1136 | DELETE-inferable | - | Offer only what the user can do from where they are: common sense. "No look-alike" is floor 3. |
| pr-template-own | 312 | DELETE-inferable | - | "File a CR for it" follows from the card's never-write-project-files rule. |
| refusals-to-say-more | 1484 | CLI | the refusals of `order confirm`, `order add`, `round` say what/why/ways | Rows restate refusal texts; rounds exception dup of rounds-exception; price line inferable. |
| refusals-to-say-p1 | 1343 | CLI | refusal texts of `order qa`/`order add`; row C to a `host` row | The principle (say a refusal before trying) is one line already in the CoS card. |
| refusals-to-say-p2 | 503 | CLI | `close` refusal text (exists) | Restates the close refusal and its ways. |
| reload | 818 | CLI | new: `seat`/`status` after reload prints role and the read-only line; hook reload message | The read-only rule after reload is one skill sentence; the rest is sequence. |
| remote-login | 1037 | CLI | `webui --help`, `login --help` | Command reference; network exposure on the user's word keeps 1 line (board guide). |
| seat-p1 | 1385 | CLI | `seat` output + `next:` (role, the one question) | Decision table on the seat state is deterministic; the CLI can print role and question. |
| seat-p2 | 1161 | CLI | `seat` output; refusal on a stale seat | Deterministic table; role change on the user's word is already in the card. |
| session-start | 1168 | CLI | `preflight --direct` P6/P7 failure text + `next:` | The three-part message is what the refusal should print; left-behind check is CLI-able. |
| session-start-surface-p1 | 1261 | CLI | new: launcher resolves `--project` from the `planning:` pointer | Pure path resolution; refuse with the "add its checkout" text. |
| session-start-surface-p2 | 459 | DELETE-dup | AGENTS.md dev-mode rule; launcher `--sync` | Chantier's own dev mode, shipped to every project's context. |
| sync-offer-p1 | 1240 | DELETE-inferable | CoS card Asks-first 2; launcher `--sync` names the holders | Over-specified etiquette around `sync pending` |
| sync-offer-p2 | 953 | DELETE-inferable | same; "never by PID" is floor 10 | Same |
| titles | 1503 | CLI | new: `seat take` prints the title to set | Title is a pure format computed from hostname, role and batch. |
| watcher | 1503 | KEEP-guide | board | The one yes for watcher and board, and what a no means: consent on processes and network; 5 lines. |
| watcher-board-p1 | 1246 | CLI | server writes `Destination:` itself; watcher line carries `next: order add` | Mechanical transcription and a deterministic "spec final?" check. |
| watcher-board-p2 | 507 | DELETE-inferable | - | "Rescan: read the backlog again"; "still ask before opening a batch" is floor 7. |
| watcher-events-p1 | 1065 | CLI | watcher line `next:`; new: `order merged` confirms on the forge itself | Forge confirmation before recording is a check the command can do (`ship` already reads the forge). |
| watcher-events-p2 | 1185 | DELETE-dup | the watcher's output; AGENTS.md | Describes watcher timing internals; the lines explain themselves; keep "tell, act on nothing". |
| watcher-lines-p1 | 736 | DELETE-dup | the watcher's own lines | Each line already says what to do ("the printed command or reason"); no judgement. |
| watcher-lines-p2 | 887 | CLI | `watch: not running` line already carries the command | Restart rules: make each end line say "start again" or "do not". |
| watcher-pull | 863 | CLI | `status` `pull path` line and the output's `next` line (exist per page) | Run the printed command each turn; one line at most. |
| writer | 1284 | KEEP-guide | board | Writer states: `writer:` line should carry its own way out; keep conflict rule (never force push, never pull/push by hand), 4 lines. |
| writer-off | 407 | CLI | `take` refuses while the writer is off (exists?); `next` prints the ask | Two fixed asks; the refusal is the protection |
| **Workers** | | | | |
| inspector-audit | 1130 | KEEP-card | inspector.md (3 short lines) | What an Inspector checks is its judgement; small, role-specific, always needed on a CR round. |
| session-shell-p1 | 896 | KEEP-card | floor/driver card: "no sleep or polling loop; stop your tasks by id" (2 lines) | Two rules, rest is definitions; split by the byte budget. |
| session-shell-p2 | 964 | KEEP-card | one shared `shell` block in `brief` (5 lines) | "No cd into a CR folder" and "forge text is a file" matter; hook could refuse the cd. |
| spec-writer-extras | 1141 | KEEP-card | spec-writer.md (3 lines) | Specification judgement (CI job environment, matrix, prepared text); small. |
| verifier-before-after | 1183 | KEEP-card | verifier.md (4 lines) | The Verifier's core method; too central to be a rare topic. |
| verifier-delta-matrix | 1504 | KEEP-guide | verifier.md `## After a move` (matrix probe: delete) | What "touched" means is judgement; the probe ceremony goes with matrix.md. |
| verifier-description | 1340 | CLI | new: `chantier pr check <cr>` (render, SHA on proofs, STALE, gaps vs UNVERIFIED, role names) | Most items are greps of the posted body; "consistent with the diff" stays one card line. |
| verifier-images | 1340 | DELETE-dup | pr-images.md, same definitions word for word | One images page for all roles. |
| verifier-review-box | 464 | CLI | new: `pr check` compares the Review box SHA with the log's notes | A lookup in `log <cr>`. |
| verifier-scratch | 1396 | KEEP-card | verifier.md (3 lines) + new: refuse `$CHANTIER` aimed at the live project from a scratch folder | "Never run the live `$CHANTIER` on a scratch project" protects the real record. |
| worker-shell | 1467 | DELETE-inferable | 3 lines to the shared shell block of `brief` | Read-before-write, UTF-8, one command per call: a model does it; keep BOM and "blocked: stop". |
| **A Driver on its CR** | | | | |
| checkpoints | 971 | DELETE-dup | cr-ship.md says the same commit-message rule | Keep one line in the driver card: "every commit lands on main: a real message"; folding is inferable. |
| ci | 1598 | CLI | new: `chantier ci <cr>`; 2 lines KEEP-card (already in cr-driver.md) | Head check, source rule and note format are mechanical; card already holds the two rules. |
| ci-beside-gate | 2061 | CLI | `next <cr>` on the `ci: beside the long gate` line; new: `ship` prints the CI-only systems gap | Fixed sequence and outcomes table; the Known-gaps bullet is derivable from the checks list. |
| ci-no-check | 1069 | CLI | new: `chantier ci <cr>` (reads the forge at the pushed head, waits, two looks, writes the note) | Pure mechanics: a timed second look and a note format. |
| closing | 1901 | CLI | `next <cr>` steps `closing 1..4`; new: `handback` refuses a body edit after the description pass | A four-step checklist with fixed note strings; the thresholds are already in the card. |
| conflicts | 2249 | KEEP-guide | `conflicts` | Carry vs moved-patch judgement is real; half is `ship` refusals restated (delete those lines). |
| conflicts-early-push | 960 | CLI | `next <cr>` after a rebase with a PR; exists?: `gate --stop` refusal | Fixed order: draft, push, ship, gate beside CI, ready. |
| conflicts-local-gate | 1196 | CLI | `take`/`handoff` already print `long gate: this CR runs <command> locally`; `handback` refuses without it (exists?) | Who owes the local run is computed from shape and rules: the record's job. |
| cr-handback | 1514 | CLI | `handback` refusals (exist, quoted); new: `handback` builds `gaps:` from the posted body | Restates refusals; the `gaps:` copy is mechanical and was batch-31's NOT VERIFIED source. |
| cr-prompt | 1393 | CLI | `phase` set by `brief <role>`/`round`/`gate`/`ship`; new: `chantier reply check <role> <file>` | Phase bookkeeping and reply-format checks are mechanical; one line on `writes:` is in the card. |
| cr-proof | 1051 | DELETE-dup | verifier.md, cr-driver.md ("a gap goes to Known gaps first"), pr-template.md | Restates the Verifier's reply format and the card; last line is duplicated in the page itself. |
| cr-review-step | 858 | CLI | `brief <review-step> <cr>` writes this prompt (brief already reads the project's review steps) | A prompt skeleton typed by hand; `brief` should print it like any role. |
| cr-rounds | 2069 | KEEP-guide | `rounds` (new, one page for cr-workers, cr-rounds, cr-ship) | The round's shape and "body-only FIX-REQUIRED is no round" are judgement; note strings go to CLI. |
| cr-ship | 2422 | CLI | `next <cr>` (commit, probe, rebase, checks, gate, push, PR, ship, CI, verifier); new: `ship --open` creates the draft PR | A fixed pipeline in order; 3 lines dup of card (add by name, base, fast gate yourself). |
| cr-workers | 1528 | CLI | `round` refusals (exist), `workers:` line of `take` (exists); new: `take` creates the worktree | Worktree creation and worker start are printed commands; nothing to judge. |
| handback-gate-draft | 1348 | CLI | `take`/`handoff` `gate:` line (exists); `handback` refusal for an owed local run (exists?) | Reads printed lines back; the release-draft sentence is inferable. |
| handback-other | 2040 | CLI | `handback --help` (reason forms, `--wait` types); 2 lines KEEP-card | A list of argument forms; keep "never skip a proof pass to save budget" in the card. |
| handback-refused | 1010 | CLI | each `handback` refusal carries its own next step (M9) | Three refusals each with one fixed answer; "merged: touch nothing" belongs in the refusal text. |
| matrix | 1354 | DELETE-inferable | 2 lines to cr-driver.md evidence plan | "Name a matrix in the evidence plan" is one sentence; the probe ceremony is over-built. |
| pr-extras | 1905 | CLI | new: `chantier archive <cr>` writes the cleaned archive at the printed path; `ship` already prints `archive missing` | File list, size thresholds and zip rule are mechanical. |
| pr-gitlab | 501 | DELETE-stale | docs/proofs (unproved list) | Three "unproved" lines and "read `glab --help`". |
| pr-images | 1891 | KEEP-guide | `pr` (one short page: images) + hook | Floor 8's definition and the leak procedure protect the user; cut to about 600 bytes. |
| qa-results | 953 | KEEP-card | qa-driver.md (3 lines) | Result file shape and "report only what you reproduced"; the worktree command to `order qa` output. |
| retake | 2338 | CLI | `next <cr>` on a `rebase:` note; `ship`'s `off:` lines (exist) | A rebase recipe by note kind; one line KEEP-card: "never a second PR". |
| retake-notes | 1878 | CLI | each note (`unhold:`, `rebase: … dropped`, `rebase: mode`, `folded:`) answered by `next <cr>` | Per-note recipes; `folded:` is GitLab-only and unproved (delete). |
| steering-messages | 1305 | KEEP-card | driver cards (4 lines: note, ping, stop, taken back) | The card already holds half; `msg --help` carries the command. |
| trouble-gate | 1506 | KEEP-guide | `trouble` | "Never stop a gate because it is slow, never another CR's" is judgement; queue facts to `gate --help`. |
| trouble-git | 911 | KEEP-card | cr-driver.md Never list (1 line) + write guard | "Write nothing in `.git`; never clean the main checkout by force": hook can refuse. |
| trouble-remote | 1588 | KEEP-guide | `trouble` | Retry once, check the first attempt took effect, 4xx is no infra: short and real. |
| trouble-worker | 2188 | KEEP-guide | `trouble` | "Never read a verdict into an out-of-format reply; never resume by message" is real judgement. |
| **Steering a running batch** | | | | |
| chain | 1322 | KEEP-guide | `merge` guide (or 3 lines in foreman.md) | Real judgement: chain only when the same lines would conflict, never a started CR |
| chain-conflict | 1162 | CLI | the Foreman's `chain`/`conflict` lines end with the command to run; `conflicts` already words the ask | Record-at-once sequences; the stack-switch question is worded by `conflicts` |
| conflict-check | 1482 | CLI | `next:` after a ready hand-back in a parallel batch names `conflicts <cr>`; the command prints its ask | Describes what the command does; "switches no mode" is in its --help |
| driver-question | 1340 | CLI | each ask line ends with its command (`next:`): `order note`, `wait clear` | Lookup table from ask kind to command; the ask can carry it |
| drop | 736 | CLI | the drop order's line already names the action; make it print the exact forge command | Pure mechanics; "no --delete-branch, no comment" goes in the printed command |
| escalation | 1031 | CLI | `next --epoch` counts blocks and prints `take … --note "escalate: …"` or the `question` ask | Counting rule (twice, once per CR); a refusal can enforce once-per-CR |
| hold | 1505 | CLI | `order hold/unhold` `next:` lines per CR state; `take` refuses a held CR (exists?) | State-by-state recipe; "never take a held CR" should be a refusal |
| main-checkout-p1 | 726 | CLI | new: `sync main`, or automatic in `order merged` (AGENTS.md already allows this fast-forward) | Preamble to a 5-step script |
| main-checkout-p2 | 1351 | CLI | same command; its refusals carry the why; it writes the note | Five checks + ff-only merge + note: textbook CLI work |
| mode-switch-p1 | 1256 | CLI | `order mode` output / `next --epoch` lists the per-CR notes | Describes what the record did, plus fan-out |
| mode-switch-p2 | 1168 | CLI | same; `forge-stack unstack` named by the `next:` line | Fan-out recipe per target mode |
| order-drop | 1150 | CLI | `order drop` refusal without `--note`, `--note inbox` refused (exist per page) | 1 card line: ask the destination, never choose. Rest is refusal text. |
| order-verbs-p1 | 1119 | CLI | `order --help` | Pure command reference; duplicates argparse help. |
| order-verbs-p2 | 938 | CLI | `order --help` | Pure command reference. |
| orders | 1312 | CLI | each order's line in `status`/`next` says what the hands do | Per-order recipe; the `access` pointer is in --help |
| orders-queue | 1005 | DELETE-dup | foreman.md ("fill free slots"), `take` refusals, `status` `waits for` | Restates CLI behaviour; born-paused batch: `next` says "send ready, wait" |
| park | 947 | KEEP-guide | foreman.md, 2 lines | Judgement: park an outside wait at once, never trouble in the work |
| park-back | 812 | CLI | `next --epoch` / `park` output prints the take and the dependents' notes | Fan-out recipe |
| qa-order | 549 | DELETE-dup | `order qa` prints `brief:`; foreman.md "Starting Drivers" | Same start rule as any Driver |
| rounds-exception | 910 | KEEP-guide | gates | A grant the CoS makes alone, capped; the cap should be a rail of `order rounds`. |
| status-notes | 1134 | CLI | `status --notes` computes the floor line (delivery.py exists) | Fixed formats and arithmetic. |
| status-notes-more | 1357 | CLI | `status --notes` prints these lines (`partial stack mergeable` exists) | Fixed formats computed from the record; pure template. |
| steering-reports-p1 | 1462 | CLI | `status --refresh` prints the Notes lines; host row for the turn-end notice | 2 card lines: never read the Foreman's transcript; never "epoch" to the user. Turn-end dup of host-turn-end. |
| steering-reports-p2 | 684 | CLI | new: `status --refresh` runs `git status --porcelain` and `forge-stack show` itself (read-only) | Two pre-report checks a command can run. |
| wakes-forge | 1017 | CLI | the watcher line already names the command; `order merged` checks the forge first (new read) | Line-to-action map; the forge check should be a refusal |
| wakes-p1 | 1008 | DELETE-dup | foreman.md heartbeat line; the `watch:` line prints its command | Contradicts wakes-p2 and the card on the watcher's life |
| wakes-p2 | 918 | KEEP-card | foreman.md (2 lines: end the heartbeat, not the session; short turns) | The idle stop saves real money; the sequence is `next` |

## C. The 240 topic names

A topic is a name `help` accepts. 126 are one page; 47 are one subject cut in `-pN` parts; 67 are aggregates that print other topics' pages again (their bytes are counted twice or more in "bytes printed").

| topic | pages | bytes printed | kind | pages' verdicts |
|---|---:|---:|---|---|
| worker-shell | 1 | 1467 | page | DELETE-inferable 1 |
| session-shell | 2 | 1860 | parts | KEEP-card 2 |
| verifier-scratch | 1 | 1396 | page | KEEP-card 1 |
| verifier-description | 1 | 1340 | page | CLI 1 |
| verifier-review-box | 1 | 464 | page | CLI 1 |
| verifier-delta-matrix | 1 | 1504 | page | KEEP-guide 1 |
| verifier-before-after | 1 | 1183 | page | KEEP-card 1 |
| verifier-images | 1 | 1340 | page | DELETE-dup 1 |
| inspector-audit | 1 | 1130 | page | KEEP-card 1 |
| spec-writer-extras | 1 | 1141 | page | KEEP-card 1 |
| lease | 2 | 2819 | aggregate | CLI 2 |
| refused-push | 7 | 8778 | aggregate | CLI 7 |
| refused-push-answer | 1 | 1086 | page | CLI 1 |
| restart | 1 | 1183 | page | CLI 1 |
| checkpoints | 1 | 971 | page | DELETE-dup 1 |
| steering-messages | 1 | 1305 | page | KEEP-card 1 |
| trouble | 4 | 6193 | aggregate | KEEP-guide 3, KEEP-card 1 |
| trouble-worker | 1 | 2188 | page | KEEP-guide 1 |
| trouble-remote | 1 | 1588 | page | KEEP-guide 1 |
| trouble-gate | 1 | 1506 | page | KEEP-guide 1 |
| trouble-git | 1 | 911 | page | KEEP-card 1 |
| ci | 3 | 4728 | aggregate | CLI 3 |
| ci-no-check | 1 | 1069 | page | CLI 1 |
| ci-beside-gate | 1 | 2061 | page | CLI 1 |
| conflicts | 3 | 4405 | aggregate | KEEP-guide 1, CLI 2 |
| conflicts-early-push | 1 | 960 | page | CLI 1 |
| conflicts-local-gate | 1 | 1196 | page | CLI 1 |
| handback-other | 3 | 4398 | aggregate | CLI 3 |
| handback-refused | 1 | 1010 | page | CLI 1 |
| handback-gate-draft | 1 | 1348 | page | CLI 1 |
| closing | 1 | 1901 | page | CLI 1 |
| pr-extras | 3 | 4297 | aggregate | CLI 1, KEEP-guide 1, DELETE-stale 1 |
| pr-images | 1 | 1891 | page | KEEP-guide 1 |
| pr-gitlab | 1 | 501 | page | DELETE-stale 1 |
| retake | 3 | 6042 | aggregate | CLI 3 |
| retake-stack | 1 | 1826 | page | CLI 1 |
| retake-notes | 1 | 1878 | page | CLI 1 |
| matrix | 1 | 1354 | page | DELETE-inferable 1 |
| cr-workers | 2 | 2921 | aggregate | CLI 2 |
| cr-rounds | 1 | 2069 | page | KEEP-guide 1 |
| cr-review-step | 1 | 858 | page | CLI 1 |
| cr-ship | 2 | 3473 | aggregate | CLI 1, DELETE-dup 1 |
| cr-handback | 1 | 1514 | page | CLI 1 |
| stack-restack | 2 | 3078 | aggregate | CLI 2 |
| stack-make | 2 | 2931 | aggregate | CLI 2 |
| stack-joins | 1 | 1476 | page | KEEP-guide 1 |
| stack-changes | 1 | 2362 | page | KEEP-guide 1 |
| stack-hold | 1 | 2240 | page | KEEP-guide 1 |
| release-notes | 1 | 2063 | page | KEEP-guide 1 |
| release-ship | 1 | 2315 | page | KEEP-guide 1 |
| release-merged | 1 | 2854 | page | KEEP-guide 1 |
| release-end | 1 | 984 | page | CLI 1 |
| qa-results | 1 | 953 | page | KEEP-card 1 |
| cr-proof | 1 | 1051 | page | DELETE-dup 1 |
| cr-prompt | 1 | 1393 | page | CLI 1 |
| stack-record | 1 | 1239 | page | CLI 1 |
| stack-gate | 1 | 1182 | page | CLI 1 |
| merge | 1 | 1507 | page | CLI 1 |
| take-back | 1 | 1505 | page | KEEP-card 1 |
| main-checkout | 2 | 2077 | parts | CLI 2 |
| sync | 3 | 2077 | aggregate | CLI 2 |
| merge-under-grant | 2 | 1858 | aggregate | CLI 2 |
| long-gate | 2 | 2597 | aggregate | KEEP-guide 1, CLI 1 |
| local-gate | 1 | 1248 | page | CLI 1 |
| orders | 2 | 2317 | aggregate | CLI 1, DELETE-dup 1 |
| drop | 1 | 736 | page | CLI 1 |
| cleanup | 1 | 685 | page | CLI 1 |
| chain | 1 | 1322 | page | KEEP-guide 1 |
| qa-order | 1 | 549 | page | DELETE-dup 1 |
| escalation | 1 | 1031 | page | CLI 1 |
| lost-driver | 5 | 6713 | aggregate | KEEP-guide 3, CLI 2 |
| lost-restart | 1 | 1499 | page | CLI 1 |
| lost-context | 1 | 1271 | page | CLI 1 |
| lost-outside | 1 | 1502 | page | KEEP-guide 1 |
| hold | 1 | 1505 | page | CLI 1 |
| park | 2 | 1759 | aggregate | KEEP-guide 1, CLI 1 |
| mode-switch | 2 | 2424 | parts | CLI 2 |
| conflict-check | 1 | 1482 | page | CLI 1 |
| release | 3 | 3433 | aggregate | CLI 2, KEEP-guide 1 |
| release-take | 1 | 1498 | page | CLI 1 |
| release-tag | 2 | 1935 | aggregate | CLI 1, KEEP-guide 1 |
| retro | 4 | 4265 | aggregate | KEEP-guide 2, DELETE-dup 1, CLI 1 |
| retro-critic | 2 | 1964 | aggregate | KEEP-guide 1, CLI 1 |
| wakes | 3 | 2943 | aggregate | DELETE-dup 1, KEEP-card 1, CLI 1 |
| handover | 1 | 937 | page | CLI 1 |
| writer-off | 1 | 407 | page | CLI 1 |
| stack | 2 | 2419 | aggregate | KEEP-guide 2 |
| stack-grows | 3 | 3373 | aggregate | CLI 2, KEEP-guide 1 |
| stack-deliver | 1 | 1008 | page | KEEP-guide 1 |
| stack-run | 4 | 4509 | aggregate | DELETE-dup 1, CLI 3 |
| stack-drop | 1 | 1374 | page | CLI 1 |
| stack-checks | 1 | 1468 | page | CLI 1 |
| stack-merge | 1 | 1465 | page | KEEP-guide 1 |
| refused-answer | 1 | 1010 | page | CLI 1 |
| refused-rebase | 2 | 2001 | aggregate | CLI 2 |
| refused-push-judgement | 2 | 2239 | aggregate | CLI 2 |
| refused-push-route | 2 | 2388 | aggregate | CLI 2 |
| stack-asks | 1 | 1092 | page | CLI 1 |
| stack-ends | 1 | 760 | page | CLI 1 |
| wakes-forge | 1 | 1017 | page | CLI 1 |
| refused-push-run | 1 | 1179 | page | CLI 1 |
| refused-push-gate | 1 | 1198 | page | CLI 1 |
| retro-lines | 1 | 1067 | page | DELETE-dup 1 |
| retro-critic-write | 1 | 612 | page | CLI 1 |
| stack-takes | 1 | 943 | page | CLI 1 |
| lost-silent | 1 | 1068 | page | KEEP-guide 1 |
| stack-outside | 1 | 994 | page | KEEP-guide 1 |
| refused-rebase-run | 1 | 856 | page | CLI 1 |
| release-stale | 1 | 979 | page | KEEP-guide 1 |
| long-gate-waiver | 1 | 1331 | page | CLI 1 |
| orders-queue | 1 | 1005 | page | DELETE-dup 1 |
| merge-github | 1 | 672 | page | CLI 1 |
| park-back | 1 | 812 | page | CLI 1 |
| grill | 11 | 13708 | aggregate | KEEP-guide 7, KEEP-card 1, CLI 2, DELETE-dup 1 |
| grill-series | 1 | 1492 | page | KEEP-guide 1 |
| grill-example | 1 | 1152 | page | DELETE-inferable 1 |
| grill-options | 1 | 1245 | page | KEEP-guide 1 |
| grill-backlog | 2 | 2050 | parts | KEEP-guide 2 |
| grill-restate | 1 | 1179 | page | KEEP-card 1 |
| grill-specify | 2 | 2138 | parts | CLI 1, DELETE-dup 1 |
| grill-critic | 1 | 1398 | page | KEEP-guide 1 |
| grill-critic-steps | 1 | 1460 | page | KEEP-guide 1 |
| where-cr-goes | 1 | 1462 | page | CLI 1 |
| grill-surface | 1 | 1072 | page | KEEP-card 1 |
| grill-outside-pr | 1 | 1416 | page | CLI 1 |
| ticket-summary | 2 | 2668 | parts | KEEP-guide 2 |
| ticket-summary-post | 2 | 2169 | parts | DELETE-stale 1, KEEP-card 1 |
| session-start | 1 | 1168 | page | CLI 1 |
| session-start-surface | 2 | 1720 | parts | CLI 1, DELETE-dup 1 |
| seat | 2 | 2546 | parts | CLI 2 |
| first-turn | 2 | 2367 | parts | KEEP-guide 1, DELETE-dup 1 |
| reload | 1 | 818 | page | CLI 1 |
| titles | 1 | 1503 | page | CLI 1 |
| writer | 1 | 1284 | page | KEEP-guide 1 |
| griller-worktree | 1 | 1195 | page | KEEP-guide 1 |
| griller-cost | 1 | 231 | page | DELETE-dup 1 |
| board | 2 | 1945 | parts | KEEP-guide 1, DELETE-dup 1 |
| board-lines | 1 | 1508 | page | DELETE-dup 1 |
| board-restart | 1 | 1455 | page | CLI 1 |
| watcher | 1 | 1503 | page | KEEP-guide 1 |
| watcher-lines | 2 | 1623 | parts | DELETE-dup 1, CLI 1 |
| watcher-events | 2 | 2250 | parts | CLI 1, DELETE-dup 1 |
| watcher-board | 2 | 1753 | parts | CLI 1, DELETE-inferable 1 |
| watcher-pull | 1 | 863 | page | CLI 1 |
| remote-login | 1 | 1037 | page | CLI 1 |
| allow-rules | 1 | 1356 | page | CLI 1 |
| allow-rules-more | 2 | 1883 | parts | CLI 1, DELETE-dup 1 |
| forge-permissions | 2 | 2714 | parts | CLI 2 |
| forge-permissions-say | 1 | 839 | page | CLI 1 |
| forge-permissions-gitlab | 1 | 861 | page | DELETE-stale 1 |
| config | 3 | 3652 | parts | CLI 2, DELETE-dup 1 |
| project-rules | 2 | 2285 | parts | CLI 2 |
| options | 1 | 1136 | page | DELETE-inferable 1 |
| refusals-to-say | 2 | 1846 | parts | CLI 2 |
| refusals-to-say-more | 1 | 1484 | page | CLI 1 |
| compacting | 2 | 1940 | parts | DELETE-inferable 2 |
| delivery-time | 2 | 2339 | parts | CLI 2 |
| batch-start | 13 | 14716 | aggregate | CLI 9, KEEP-guide 3, DELETE-stale 1 |
| trials | 2 | 1779 | parts | CLI 2 |
| batch-plan | 1 | 1502 | page | CLI 1 |
| batch-plan-show | 2 | 1826 | parts | CLI 2 |
| batch-plan-mode | 3 | 4032 | parts | KEEP-guide 1, CLI 2 |
| batch-plan-cut | 2 | 2304 | parts | KEEP-guide 2 |
| foreman-start | 2 | 2139 | parts | CLI 2 |
| foreman-start-more | 1 | 1134 | page | DELETE-stale 1 |
| steering | 25 | 25977 | aggregate | CLI 19, DELETE-dup 4, KEEP-guide 2 |
| steering-reports | 2 | 2146 | parts | CLI 2 |
| refused-push-chief | 2 | 2099 | parts | CLI 2 |
| refused-push-chief-more | 2 | 1679 | parts | KEEP-guide 1, DELETE-dup 1 |
| refused-rebase-chief | 1 | 1262 | page | CLI 1 |
| refused-forge-chain | 1 | 807 | page | DELETE-dup 1 |
| asks | 1 | 661 | page | DELETE-dup 1 |
| ready-asks | 1 | 367 | page | DELETE-dup 1 |
| ask-lines | 1 | 1022 | page | CLI 1 |
| order-verbs | 2 | 2057 | parts | CLI 2 |
| order-drop | 1 | 1150 | page | CLI 1 |
| cost | 1 | 295 | page | DELETE-dup 1 |
| chain-conflict | 1 | 1162 | page | CLI 1 |
| rounds-exception | 1 | 910 | page | KEEP-guide 1 |
| driver-question | 1 | 1340 | page | CLI 1 |
| ready-to-merge | 12 | 15427 | aggregate | CLI 9, KEEP-card 1, KEEP-guide 1, DELETE-stale 1 |
| merge-words | 2 | 1937 | parts | CLI 1, KEEP-card 1 |
| merge-gaps | 2 | 2858 | parts | CLI 1, KEEP-guide 1 |
| merge-recorded | 1 | 1353 | page | CLI 1 |
| merge-series-stack | 2 | 2696 | parts | CLI 2 |
| merge-stack-ready | 2 | 2966 | parts | CLI 2 |
| merge-stack-gitlab | 1 | 1285 | page | DELETE-stale 1 |
| stack-changes-chief | 2 | 2332 | parts | CLI 2 |
| batch-end | 10 | 11398 | aggregate | CLI 4, KEEP-guide 4, DELETE-dup 1, DELETE-stale 1 |
| batch-pause | 1 | 1402 | page | CLI 1 |
| retro-route | 2 | 2126 | parts | CLI 1, KEEP-guide 1 |
| retro-route-chantier | 2 | 1907 | parts | KEEP-guide 1, CLI 1 |
| batch-close | 2 | 2563 | parts | CLI 1, DELETE-dup 1 |
| batch-close-stopped | 2 | 1932 | parts | KEEP-guide 1, DELETE-stale 1 |
| recovery | 1 | 1468 | page | KEEP-guide 1 |
| direct | 12 | 12817 | aggregate | DELETE-dup 3, CLI 6, KEEP-guide 3 |
| direct-mode | 8 | 8812 | aggregate | DELETE-dup 2, CLI 4, KEEP-guide 2 |
| direct-mode-switch | 5 | 5594 | aggregate | CLI 3, KEEP-guide 2 |
| direct-mode-epoch | 2 | 1890 | parts | CLI 1, DELETE-dup 1 |
| direct-mode-accept | 2 | 2115 | parts | KEEP-guide 1, CLI 1 |
| release-procedure | 8 | 8607 | aggregate | KEEP-guide 4, CLI 4 |
| release-chief | 2 | 2753 | parts | KEEP-guide 1, CLI 1 |
| release-chief-approve | 2 | 1692 | parts | KEEP-guide 1, CLI 1 |
| release-chief-auto | 2 | 1867 | parts | CLI 1, KEEP-guide 1 |
| release-chief-after | 2 | 2295 | parts | KEEP-guide 1, CLI 1 |
| seat-handover | 1 | 1376 | page | KEEP-guide 1 |
| demo | 2 | 1782 | parts | KEEP-guide 1, DELETE-inferable 1 |
| pr-template-own | 1 | 312 | page | DELETE-inferable 1 |
| sync-offer | 2 | 2193 | parts | DELETE-inferable 2 |
| host-configuration | 2 | 2798 | aggregate | DELETE-dup 1, DELETE-stale 1 |
| host-allow-rules | 2 | 1895 | aggregate | DELETE-inferable 1, DELETE-stale 1 |
| host-allow-broad | 2 | 1728 | aggregate | CLI 1, DELETE-dup 1 |
| host-allow-extra | 2 | 1010 | aggregate | DELETE-stale 1, DELETE-dup 1 |
| host-allow-add | 2 | 1578 | aggregate | CLI 1, DELETE-dup 1 |
| host-allow-add-lines | 2 | 1756 | aggregate | CLI 1, DELETE-dup 1 |
| host-allow-not-add | 2 | 835 | aggregate | DELETE-stale 1, DELETE-dup 1 |
| host-refused | 2 | 1472 | aggregate | KEEP-guide 1, DELETE-dup 1 |
| host-auto-mode | 2 | 1657 | aggregate | DELETE-stale 1, DELETE-dup 1 |
| host-auto-mode-steering | 2 | 1740 | aggregate | DELETE-stale 1, DELETE-dup 1 |
| host-auto-mode-trials | 2 | 1778 | aggregate | DELETE-stale 1, DELETE-dup 1 |
| host-compact | 2 | 1683 | aggregate | KEEP-guide 1, DELETE-dup 1 |
| host-write-guard | 2 | 1422 | aggregate | DELETE-dup 2 |
| host-write-guard-shell | 2 | 1589 | aggregate | DELETE-dup 2 |
| host-sessions | 2 | 2105 | aggregate | CLI 1, DELETE-stale 1 |
| host-sessions-more | 2 | 1394 | aggregate | DELETE-stale 1, DELETE-dup 1 |
| host-remote | 2 | 1664 | aggregate | KEEP-guide 1, DELETE-dup 1 |
| host-surfaces | 2 | 1782 | aggregate | DELETE-inferable 1, DELETE-dup 1 |
| host-subagent-signs | 2 | 1545 | aggregate | KEEP-guide 1, DELETE-dup 1 |
| host-foreman-worktree | 2 | 864 | aggregate | DELETE-dup 2 |
| host-reuse-foreman | 2 | 1141 | aggregate | DELETE-inferable 1, DELETE-dup 1 |
| host-for-you | 2 | 1523 | aggregate | DELETE-inferable 1, DELETE-dup 1 |
| host-for-you-sessions | 2 | 1173 | aggregate | DELETE-inferable 1, DELETE-dup 1 |
| host-auto-fix | 2 | 1793 | aggregate | KEEP-guide 1, DELETE-dup 1 |
| host-turn-end | 2 | 1798 | aggregate | KEEP-guide 1, DELETE-dup 1 |
| host-driver-silence | 2 | 1528 | aggregate | KEEP-guide 1, DELETE-dup 1 |
| host-heartbeat | 2 | 2684 | aggregate | CLI 2 |
| init-checks | 1 | 1498 | page | KEEP-guide 1 |
| init-tools | 1 | 1492 | page | KEEP-guide 1 |
| release-evidence | 2 | 1879 | aggregate | KEEP-guide 1, DELETE-inferable 1 |
| status-notes | 2 | 2491 | aggregate | CLI 2 |

## D. Protective rules found in the pages (the checklist of plan sections 5 and 7)

As the four readers listed them, by slice; "exists?" and "not verified" are theirs.

### Slice A

- A CR found merged at hand-back: push, edit, retarget and turn nothing; note and end. (handback-refused) Enforceable: `push`, `ship` refuse on a merged CR (exists?).
- A CR that shows a `PR:` link at first take: never a second PR, never a new branch. (retake) Enforceable: `ship` refuses a second link for a CR.
- A release's new attempt starts in a new worktree, never `reset --hard` of the old one. (release-ship) Partly floor 5; not enforceable.
- Half-done irreversible release work: stop, say exactly what is out, never undo it alone. (release-ship) Not enforceable; card.
- The main-checkout release step (the tag) is never the release driver's. (release-merged) Enforceable by the write guard on `git -C <main checkout>` writes.
- Publication done by someone else: never run the publication command again; check read-only. (release-merged) Enforceable: `release go` answers no once `publication done:` is noted.
- Never rerun a creating forge command after a network error without checking it took effect. (trouble-remote) Not enforceable; guide.
- A forge refusal (4xx, protected branch, failed lease) is never retried as an infrastructure failure. (trouble-remote) Card line.
- Never read a verdict, pass or choice into an out-of-format reply, never fix it. (trouble-worker) Enforceable in part: `verdict`/`note approved` take the reply file and check its format.
- A second refused start of a worker is never retried without its model. (trouble-worker) No fallback (floor 3) covers it; drop.
- Driver and workers write nothing in `.git` (`info/exclude`, `config`, `hooks`). (trouble-git) Enforceable: write guard hook.
- The main checkout is never cleaned by force after a wrong-place git command. (trouble-git) Card line.
- A dropped CR's PR: close with no `--delete-branch`, no comment; a CR moved to backlog: draft only. (stack-changes) Enforceable: new `cancel`/`drop` does the forge step itself (needs an AGENTS.md forge exception).
- No forge branch protection is read; a push rejected as protected is never retried. (refused-push-steering) Enforceable: the steering push command.
- Steering push only for `chantier/*`, never the default branch, a user's yes included. (refused-push-steering; in both steering cards) Already `push.py` rails for Drivers; extend to steering.
- A leak found after an upload: replace, tell the user, nothing about it in the public PR. (pr-images) Not enforceable; guide.
- The user's own screenshot that fails the look is not uploaded or copied. (pr-images) Guide.
- A Driver never opens an image file. (pr-extras) Context protection, not a user protection; drop or one card line.
- Never use the live `$CHANTIER` line on a scratch project; `git init` it first. (verifier-scratch) Enforceable: CLI refuses when cwd is under `work/scratch` and the project resolves elsewhere.
- A too-long Windows path is a stop: no shorter folder outside `writes:`. (verifier-scratch) Write guard already refuses outside `writes:`.
- `--no-gate` replaces only the gate check, and quotes the rule. (cr-handback) Exists as a `handback` argument; the steering check stays a card line (foreman Never 2).
- Never skip a proof pass to save budget. (handback-other) Card line.
- A local gate failure leaves the would-be top a draft; change nothing for it. (stack-gate) Enforceable: `stack --out-of-draft` refuses without a pass (exists?).
- Never stop another CR's gate, nor yours because it is slow. (trouble-gate) First half exists (`--stop` refuses another CR's lock); second is card.
- An image upload in a release is irreversible: `release go` first. (release-evidence) Card line in release-driver.md.

### Slice B

- Check the forge shows the PR merged into the default branch before `order merged`; `not landed`/unconfirmed records nothing (wakes-forge). Enforceable: `order merged` could read the forge and refuse (needs a named forge read in AGENTS.md).
- The main-checkout fast-forward is only `merge --ff-only --no-overwrite-ignore`, never pull/reset/stash/clean/checkout; untracked files never touched; first no stops (main-checkout-p2). Enforceable: make it a CLI command (AGENTS.md already allows the CLI to fast-forward a clean main checkout).
- An Auto-fix event is no order: never merge the base in, never touch a PR whose Driver is live (host-auto-fix). Not enforceable; host row/card line.
- A host turn-end notice is no line and no ask: no tool call on it (host-turn-end). Not enforceable; card line (cost protection).
- Silence is never a reason to start a second Driver; restart only after a proof of death or its report (host-driver-silence, lost-silent). Partly enforceable: a take is refused while the lease is live (lease refusal).
- Never record a hand-back for a Driver yourself (lost-silent). Enforceable: `handback` requires the CR's lease (not verified).
- When you stop a Driver and do not restart at once, clear its id in the same turn, after a `stopped:` note (lost-outside). Enforceable: a `restart`/`stop` subcommand does both.
- A stopped-from-outside Driver is restarted with no ask, whatever the host says about "only if the user asks" (lost-outside). Card line (it overrides a host instruction; a model would otherwise obey the host).
- Steering rebase of a Driver's branch: only `git -C <worktree> rebase <base>` after the branch/base check; a conflict is left stopped, no `--abort`, no resolution (refused-rebase, -run). Enforceable: a CLI subcommand with rails, as `push`.
- Merge under grant on GitHub: with an open PR below in a native stack, no merge; a pending async merge is never PUT again; read state before any retry (merge-under-grant, merge-github). Enforceable in a `release merge` command.
- `--outside-stack` only on an open order carrying the user's word for that CR, never to pass a refusal (stack-outside). Already refused by `asks` without an order id (per its --help).
- Never take a held CR; neither it nor the release starts while a CR is held or parked (hold). Enforceable: `take` refusal (not verified it exists).
- A dropped CR's PR is closed with no `--delete-branch` and no comment; a trashed/backlog CR's worktree and branch are never removed by the Foreman (drop, cleanup). Second half is foreman Never 6; first: print the exact command.
- A local-gate ask goes only with `passed`; a hand-back claiming a waiver with no recorded order goes back with no ask (local-gate, long-gate-waiver). Enforceable: `judge` refuses (partly exists: `--local-gate`).
- `gate --first` only for the critical path or the user's next merge, never at a Driver's request (long-gate). Already in foreman.md "You own".
- Run a release step in the main checkout only when the Driver handed it back; refused: change nothing, never force (release-tag). Already foreman.md; keep.
- Chantier never removes or edits an allow rule of the user's; never arms/disarms the PR monitor; no `gh api` allow rule (host-allow-broad, host-auto-fix). One Chief of Staff card sentence.
- Never `rm -rf`/`Remove-Item -Recurse` on `.claude` or wildcard temp folders (host-refused). Hook deny possible.
- Stop a sync holder only if it is this session's own board/watcher, on the user's yes, by the host's task stop, never by PID (sync-offer). Covered by floor 10 + Chief of Staff "asks first 2".
- A chain: never chain a started CR; a shared file alone is no reason (chain). `order after` could refuse a started CR (not verified).
- A cancelled dependency never frees its CR: ask, do not start it (chain, orders-queue). `take` already refuses.
- The retro critic's verdicts are followed as given; its brief carries evidence, never the Foreman's argument (retro-critic, -write). Card/guide line.

### Slice C1

- A broad or stale allow rule of the user's is never removed or edited by the agent; the user removes it by hand. (allow-rules-more-p1) Enforceable: yes, if the settings write becomes a CLI command that only adds.
- Nothing but `permissions.allow` of `~/.claude/settings.json` is written: no project settings file, no deny or ask key. (allow-rules) The card has "nothing else there"; enforceable by the same CLI write.
- `close --stopped <agent>` only on the user's yes for each named agent, never to get past an unreadable transcript. (batch-close-stopped-p1) Partly: the CLI refuses a name that is not a running held agent; the yes cannot be checked by code.
- `asks --read all` is never used to clear the list: an ask stays unread until the user has heard it. (asks) Not enforceable; one card line.
- Never assume that stopping a session ended its Agent children: check each old Driver ended before restarting its CR. (direct-mode-switch-p2) Enforceable: `take` refuses on a live lease; a takeover command can refuse on a running transcript.
- Before a Foreman claims after a switch back, every Driver the Chief of Staff owns is stopped (no two Drivers on one CR). (direct-mode-back) Enforceable: `foreman set` refuses while another number's Driver leases are live (new rail).
- A Foreman session is stopped by the user, or by the Chief of Staff on the yes and only by the host's named means. (direct-mode-switch-p2) In the card (asks first, 2).
- A long-gate waiver is recorded with the user's own words (`order waive --note`), a follow-up CR filed first; never a note in a brief. (batch-plan-show-p2) Enforceable: `order waive` takes `--note` and `--follow-up` (stack form not verified).
- On a failed preflight condition: start nothing, offer no other way. (batch-plan) In the card.
- A forced steering mode is never swapped silently. (batch-plan-mode-p3) Enforceable: preflight refusal.
- Record every answer or decision in `02-answers.md` at once, with the date and the user's words; nothing waits in the conversation. (grill-backlog-p1) Not enforceable; a card line.
- Never decide alone that a CR is grilled enough; ask only after a full restatement. (grill-restate) Not enforceable; a card line.
- The spec critic never edits the specification and runs once, never in a loop. (grill-critic) Enforceable in part: its agent has no Write tool.
- A critic finding that touches behaviour, scope or risk is a question to the user, never fixed silently. (grill-critic-steps) Judgement; a guide line.
- An outside PR is archived only on the user's word, never from a forge read of the agent's own. (grill-outside-pr) Floor 7 covers it.
- Another project's CR: `file`'s "grill the CR here" is not followed; no launch (`order add`, `open`) even on "grill it here". (grill-surface) Enforceable: `order add`/`open` could refuse a CR of another project (not verified).
- A project's clone on a surface is touched only by `git -C <clone>`; a missing clone is cloned only on the user's word. (grill-surface) Partly enforceable (preflight names it).
- A Griller in a surface worktree commits nothing, opens no PR, runs no `triage` or `summary` there. (griller-worktree) Enforceable: those commands can refuse in a surface worktree.
- An install (`gh`, its extension) only on the user's yes; `gh auth login` stays the user's; chantier changes no forge setting. (init-tools) In the card.
- `long_gate` lines are written to `chantier.yaml` only on the user's yes. (init-checks) The card has "project file writes" under asks first.
- A demo fixture is prepared outside the repository's tracked files and removed at the end; a Chief of Staff's own subagent never commits, pushes or writes in a CR worktree. (demo-p1, demo-p2) Second half in the card; enforceable by the write guard (`writes:` line).
- The board is never stopped by the agent except by `serve --restart`, one yes per restart; a refused restart's stop command is printed, never run. (board-restart, board-lines) In the card and floor 10.
- A delivery time is never promised without the floor; none is stated when the gate's time is unknown; no gate is run to measure it. (delivery-time-p2) In the card; moot once the CLI prints `floor:` or `unknown`.
- A local gate `not run` or `failed` is quoted to the user before "can be merged"; merging anyway is the user's choice, never refused. (merge-gaps-p1) Enforceable: `judge` words it.

### Slice C2

- "You can merge it" is said only after the `ready-to-merge` / `stack-ready-to-merge` line reached you, never on a green CI or a draft (merge-words-p2). Partly enforceable: `judge`/`status` word a held state; the sentence itself is card text.
- A draft on another CR's branch is never called ready: merging it lands in that branch, not the default one (merge-words-p1). CLI: `label` already distinguishes; keep the word in `judge`'s output.
- An uploaded image that showed the username or home folder: tell the user the old attachment may stay reachable (merge-gaps-p2). Not enforceable; one guide line.
- A screenshot asked of the user uses made-up paths, no username or home folder (merge-gaps-p2). Extends floor 8 to the user's own screenshot; guide line.
- `publication done:` is recorded only from the user's own quoted words; never guessed from the forge or from silence (release-chief-after-p1). CLI could require the quoted form; else card (near ask-first 3).
- "auto" covers one release only: never the announcement, a fix's start or merge, `order confirm` or a budget raise (release-chief-auto-p2). `order grant` rails; the scope sentence stays in the guide.
- No grant lets a steering session merge a stack that holds the release PR; the user merges a stack (merge-series-stack-p2). A refusal in `release go` is possible; not verified.
- Never choose a dropped CR's destination for the user (order-drop). Enforced: `order drop` refuses without `--note` (per the page).
- A public chantier issue holds no project name, private path, code, CR number, batch id or person's data (retro-route-chantier-p1). A lint in a new `retro issue` command could catch patterns; judgement remains.
- A tracker comment holds no CR number, slug, batch, role, cost, private path or internal link; posted only on a recorded yes for that ticket, by the Chief of Staff only (ticket-summary-p1/p2). Card holds the core; a lint could enforce the patterns.
- A failed post is never retried another way; if an artifact fails, the comment is not posted (ticket-summary-post-p1). Floor 9 covers the first half.
- No agent closes or reopens an issue by hand; only the PR's closing line does (ticket-summary-post-p2). Already in the CoS and CR Driver cards.
- A refused push of a non-`chantier/*` or default branch is never pushed, even on a yes (refused-push-chief-p1). In the card rail; best as a refusal of a steering push command.
- A refused push or rebase: once, unchanged, never `--force`, never another form, never a change to the permission settings (refused-forge-chain, refused-push-chief-more-p2). "Never change the permission settings to get through" deserves one card line.
- The seat moves only on the user's word and the new session's explicit acknowledgement; a running Driver is never stopped or moved for it (seat-handover). Card has the first half.
- Two live Chiefs of Staff: do no Chief of Staff work until the user chooses (seat-p2). Whether commands refuse on a seat held by another session: not verified.
- The watcher and the board start only on the session's one yes; after a no, never start one; never stop another session's watcher (watcher). Guide line.
- The board's network exposure (`board.host: network`) only on the user's word (remote-login). One line.
- `cancel` only after a drop the user ordered, never to stop a CR that goes on (recovery). Already in the CoS card.
- The board's `running-batch` mark is a go only for a CR whose specification is final (watcher-board-p1). `order add` already refuses a CR with no specification.
- "Rescan" decides nothing: still ask before opening a batch (watcher-board-p2). Floor 7.
- A trial refusal is said at once with its exact text; a pass proves nothing for a Driver (trials-p2). Guide line.
- A `chantier.yaml` long-gate entry is written in the main checkout only on the user's yes (project-rules-p2). Card ask-first 1.
- Before proposing to move a session off a worktree, check nothing is left behind (session-start). `preflight` could print the two counts.
- Rounds exception: only for a red the batch caused, +1 per cause, never above `max_rounds` + 2; every other grant is the user's (rounds-exception). A cap rail on `order rounds` is easy; the cause stays judgement.

## E. Contradictions and stale text found

### Slice A

- cr-proof.md repeats its last line twice.
- verifier-images.md and pr-images.md hold the same definitions; they can drift.
- checkpoints.md and cr-ship.md both state the commit-message rule.
- ci.md says "a Monitor tool used from a subagent is unproved"; steering-messages.md and session-shell-p1 treat a host monitor as a normal background task.
- lease.md says a Driver "never reclaims"; lease-steering.md says a Driver settles `claim lost` "with `take --reclaim`'s output": unclear wording.
- handback-other.md justifies a rule by an incident ("a turn that ended to wait for a worker's reply had broken …"): history in a card.
- cr-driver.md says hand off at 115,000 "at the VERIFIED of the pushed head"; closing.md also hands off on `context: not measured`, while the card says `context: not measured`: go on.
- Marked unproved: ci-beside-gate (GitLab, Copilot, `glab ci status --live`), ci.md (Monitor from a subagent), conflicts.md (the forge's own rebase action), pr-gitlab.md (all three lines), release-merged (`glab release view`), release-notes (`glab mr update` file form), retake-notes (`folded:`, GitLab only), stack-make (GitLab chain checks, `glab mr update --ready`), refused-push-steering (GitLab protected-branch text), refused-push-gate (pipeline job as long gate on GitLab).
- cr-workers.md and cr-prompt.md describe prompt lines (`Note:`, `Needs:`, `Steering:`) around `brief`'s output; CR-510's known gaps say some of these sentences describe output the CLI no longer prints. Not checked here.
- session-shell and worker-shell exist as two pages (three files) for the same eight shell rules.
- The matrix probe (matrix.md, verifier-delta-matrix.md, cr-ship.md, inspector-audit.md, spec-writer-extras.md) is spread over five pages for a case concepts.md defines elsewhere.

### Slice B

- wakes-p1 says the watcher "outlives heartbeat and pause"; wakes-p2 and foreman.md say stop every background task before ending the heartbeat ("none outlives the heartbeat"). Already a known retro point.
- host-heartbeat: "A 55-minute wake is unproved"; lost-driver uses "55 minutes by default" as the suspect interval; the batch-31 handover says the host now caps a Monitor at 30 minutes.
- host-driver-silence says no `pong` can come from a Claude Driver; lost-silent builds the proof of death on a missing `pong`, and foreman.md lists `pong` as a byte-for-byte reply. The ping is near-useless on Claude Code.
- host-auto-mode and host-auto-mode-steering describe a Driver's raw `git -C <worktree> push --force-with-lease` and a `Rewrites:` prompt line (`concepts.md`, "A Driver's prompt"); Drivers now publish only by `chantier push`, and the prompt is a brief. Stale.
- refused-rebase step 2 and host-auto-mode-steering have the Foreman read P10's rule list and refuse to try (`push not tried: route rule missing`); floor 9 and the Chief of Staff card say run it and report a refusal. Two policies.
- merge-github is numbered "4." alone (a cut continuation of merge-under-grant): a byte-budget split artefact, like main-checkout-p1/p2, mode-switch-p1/p2, sync-offer-p1/p2, wakes-p1/p2, refused-rebase/-run.
- retro-lines' last bullet (an order that adds work; a batch born paused) repeats orders-queue and has nothing to do with the retro.
- release-tag is titled "the tag, a stale release, a fix" but holds only the tag; release-stale holds the rest.
- Marked unproved inside these pages: nearly every host-* page, GitLab stacks (conflict-check, stack-run, stack-merge, stack-checks), `glab mr update --draft` (drop), `glab ci status` (long-gate), the GitHub merge under grant "by an agent" (merge-under-grant), the Copilot heartbeat and everything Copilot.
- host-claude-only, host-allow-rules-copilot, host-compact-copilot, host-sessions-copilot, host-configuration-copilot exist only to say "nothing is known on Copilot".
- stack-run and qa-order restate foreman.md's "pass the `brief:` output unchanged": three copies.

### Slice C1

- **Unproved, by the pages' own words:** forge-permissions-gitlab ("All unproved"); batch-plan-mode-p1 (a stack on GitLab); grill-outside-pr (`glab mr view`); allow-rules (whether the running session picks up new rules); direct-mode-switch-p2 (stopping a session from the phone); foreman-start-p2 ("I have not tested this path"); board-lines (LAN reach untested); batch-close-stopped-p1/p2 (Copilot leases, "until the close end event lands").
- **Stale prompt form:** demo-p1 builds the demo-explorer's prompt by hand (a `Read <skill>/references/demo-explorer.md;` line, "the prompt of Starting an agent"); grill-specify-p1 and grill-critic-steps likewise ("its prompt names the card and the CR folder"), while the other roles start from `brief`.
- **foreman-start-p2** assembles the Foreman prompt by hand (`CLI:`, `Team:`, `Needs:`) though the prompt's own first step is `brief foreman`: two sources for one prompt.
- **board-p1 against the chief card:** the page gives `taskkill /PID <pid> /T /F` / `kill <pid>` to stop the board on the user's word; the card says "never by name, pattern or PID".
- **batch-close-p1 against AGENTS.md's spirit:** the Chief of Staff runs `git worktree remove --force` and `git branch -D` by hand; the CLI's own batch-end cleanup is "with no `--force`". Two cleanup paths, the agent's the more forceful.
- **direct-mode-switch-p4** ends by pointing at itself ("The switch to Foreman mode undoes it (`help direct-mode-switch`)"); the page meant is direct-mode-back.
- **first-turn-p1 against direct-mode-accept-p1:** the first says a CR joins a direct batch "once the others are handled and the batch is paused"; the second says a CR added while it runs "is queued by `order add` (taken when a slot frees)".
- **batch-plan-mode-p2:** `open` defaults to parallel while the page forbids ever taking the default.
- **direct-mode-epoch-p2:** the cost attribution depends on the agent writing four files with the Write/Edit tool and not a shell: a hidden coupling kept as an instruction.
- **Split residue:** cost (295 B), griller-cost (231 B), allow-rules-more-p2 (387 B), batch-close-stopped-p2 (498 B), direct-mode-p3 (538 B), board-p2 (531 B), demo-p2 (540 B): pointer or leftover pages made by the 1,500-byte page budget.
- **compacting-p1/p2 ("tips"):** a feature that lives only in card text (no trace of tips found in the CLI source by grep); 1.9 KB.
- **delivery-time-p1:** "The name in the card is this topic; no other word for it": residue of a naming dispute.

### Slice C2

- Marked unproved in the text: merge-stack-gitlab (whole page, merge train), ticket-summary-post-p1 (GitHub artifacts, GitLab, Jira: all three routes), options ("unproved from Remote Control"), steering-reports-p1 (the Foreman's error notice).
- refused-forge-chain, refused-push-chief-more-p2 and parts of refused-push-chief-p1/p2 repeat the Chief of Staff card's "Settles alone" block and rail nearly word for word.
- recovery repeats the card's `cancel` rule; ticket-summary-post-p2 repeats the card's issue rule; steering-reports-p1's turn-end notice repeats topics/host-turn-end.md.
- merge-recorded and watcher-events-p1 both give the "forge saw merged" procedure with different detail; merge-words-p2 and merge-recorded both say an early merge is recorded as any merge.
- rounds-exception and refusals-to-say-more row G state the same exception twice.
- release-chief-approve-p2 exists only to dodge a CLI quirk ("an `order note` on a ready CR is a take"): the text documents a tool defect.
- refused-push-chief-p2's "The route rule's P10 read is no step of yours" and `push not tried: route rule missing` read as residue of an earlier procedure.
- Watcher restarts are worded three ways: watcher-lines-p2 ("after a notification there is no restart; after an end, run the printed command"; and "2 h end with no batch: start it again at once"), watcher-events-p2 ("start an ended watcher again from its last line"). None knows the host's 30-minute Monitor cap the handover reports.
- project-rules-p1 and session-start both describe the session's first preflight (`preflight` against `preflight --direct`) and the first message; the first-turn pages (another slice) are likely a third copy.
- session-start-surface-p2 is chantier's own dev-mode rule (AGENTS.md), shipped to every project.
- CLI source, by grep only: no source string for `Destination:`, `Permission trials`, `rounds exception`, `publication done` or `chantier-issue`: these formats live only in cards, so the CLI neither writes nor checks them today. `partial stack mergeable` and `forge saw merged` are printed by the CLI.
