# Round 2 triage (written by scratch/merge/triage.py)

Test (orders O-179, O-180): without the rule, a session could act irreversibly or outward
without the user's yes, pass over a refusal or safety stop, lose work, or leave a batch
unable to run. `held`: the rule's text was at the base; `restored`: absent at the base,
written this CR. File:line is where the cited span (or floor rule, topic reading) starts.
Depth: the kind-a open rows were read against head one by one; the other open rows
(inferable and other kinds) were judged from their listed behaviour, not searched one by
one at head.

Rows: 438. By verdict and serious: held/no 48, held/yes 24, open/no 329, restored/no 6, restored/yes 31.

## Sentences CR-510's PR left out

| sentence | serious | verdict | reason |
|---|---|---|---|
| "A release with no PR yet is no anomaly" (X-004) | yes | restored at skills/chantier/references/stack-driver.md:10 | without it the stack driver treats the release CR as broken |
| the Foreman's pointer to `help session-shell` | no | restored at skills/chantier/references/foreman.md:39 | a pointer |
| the sync offer | no | held at skills/chantier/references/sync-checkout.md:13 | also topics/sync-offer-p1.md; it still asks the user's yes |
| "say it once to the user as printed" | no | restored at skills/chantier/references/topics/board-restart.md:3 | wording of a report to the user |

## Rows

| id | serious | verdict | reason |
|---|---|---|---|
| C-003 | no | open | no home found at the head; seed: card chief-of-staff.md:22 |
| C-007 | no | held at skills/chantier/references/topics/session-start.md:1 | format, pointer, output size or procedure, held or re-homed |
| C-008 | no | open | inferable: no quiz case names it |
| C-010 | no | open | inferable: no quiz case names it |
| C-011 | no | open | no home found at the head; seed: topic first-turn |
| C-014 | no | open | no home found at the head; seed: topic batch-plan |
| C-017 | yes | held at skills/chantier/references/floor.md:14 | unwanted act, refusal passed over, lost work or stuck batch |
| C-021 | no | held at skills/chantier/references/chief-of-staff.md:25 | format, pointer, output size or procedure, held or re-homed |
| C-023 | no | open | no home found at the head; seed: topic watcher; no rule: an entry-point table row |
| C-024 | no | open | no home found at the head; seed: topic pr-template-own |
| C-027 | no | open | no home found at the head; seed: topic config; the rule it applies: card chief-of-staff.md:13 |
| C-034 | no | open | no home found at the head; seed: topic board-restart; no rule: a fact about the CLI, the host or the forge |
| C-046 | no | open | inferable: no quiz case names it |
| C-052 | yes | held at skills/chantier/references/floor.md:7 | unwanted act, refusal passed over, lost work or stuck batch |
| C-098 | no | open | host row; no rule: wording of a message or report |
| C-1014 | no | open | no home found at the head; seed: topic grill-backlog; the rule it applies: card chief-of-staff.md:26 |
| C-1020 | no | held at skills/chantier/references/topics/where-cr-goes.md:1 | format, pointer, output size or procedure, held or re-homed |
| C-1027 | no | open | inferable: no quiz case names it |
| C-1039 | no | open | no home found at the head; seed: topic grill-surface |
| C-1047 | no | open | no home found at the head; seed: topic grill-series |
| C-1048 | no | open | inferable: no quiz case names it |
| C-1053 | no | open | no home found at the head; seed: topic grill-series |
| C-1059 | no | open | inferable: no quiz case names it |
| C-1065 | no | open | no home found at the head; seed: topic grill-series; no rule: wording of a message or report |
| C-1079 | no | open | inferable: no quiz case names it |
| C-1082 | no | open | inferable: no quiz case names it |
| C-1084 | no | open | inferable: no quiz case names it |
| C-1087 | no | open | inferable: no quiz case names it |
| C-1090 | no | open | inferable: no quiz case names it |
| C-1095 | no | open | inferable: no quiz case names it |
| C-1097 | no | open | inferable: no quiz case names it |
| C-1101 | no | open | inferable: no quiz case names it |
| C-1105 | no | open | inferable: no quiz case names it |
| C-1106 | no | open | inferable: no quiz case names it |
| C-1143 | no | open | no home found at the head; seed: topic where-cr-goes |
| C-1157 | no | open | no home found at the head; seed: topic grill-backlog |
| C-1161 | no | open | named by the Inspector; ask a pasted image as a file, not in floor or card; floor 8 holds |
| C-1164 | no | open | inferable: no quiz case names it |
| C-1196 | no | open | inferable: no quiz case names it |
| C-1203 | no | open | inferable: no quiz case names it |
| C-1238 | no | open | no home found at the head; seed: topic grill-critic-steps |
| C-1244 | no | open | no home found at the head; seed: topic grill-series |
| C-1254 | no | open | inferable: no quiz case names it |
| C-1292 | no | open | duplicate: the card's pointers and `help` |
| C-1295 | no | open | inferable: no quiz case names it |
| C-1309 | no | open | no home found at the head; seed: topic release-chief-after |
| C-1312 | no | open | no home found at the head; seed: topic grill-backlog |
| C-1412 | no | open | inferable: no quiz case names it |
| C-1413 | no | open | inferable: no quiz case names it |
| C-1414 | no | held at skills/chantier/references/topics/session-start.md:1 | format, pointer, output size or procedure, held or re-homed |
| C-1416 | no | held at skills/chantier/references/topics/titles.md:1 | format, pointer, output size or procedure, held or re-homed |
| C-1442 | no | open | no home found at the head; seed: topic allow-rules |
| C-1443 | no | open | no home found at the head; seed: topic forge-permissions |
| C-1473 | no | held at skills/chantier/references/topics/seat-p1.md:1 | format, pointer, output size or procedure, held or re-homed |
| C-1479 | no | open | inferable: no quiz case names it |
| C-1513 | yes | held at skills/chantier/references/chief-of-staff.md:20 | unwanted act, refusal passed over, lost work or stuck batch |
| C-1516 | no | held at skills/chantier/references/topics/session-start.md:1 | format, pointer, output size or procedure, held or re-homed |
| C-154 | no | open | no home found at the head; seed: card chief-of-staff.md:41 |
| C-1542 | no | open | no home found at the head; seed: topic board-lines |
| C-155 | no | open | pointer to a removed old reading, no single head home |
| C-156 | no | open | no home found at the head; seed: card chief-of-staff.md:41; no rule: a pointer |
| C-158 | no | held at skills/chantier/references/topics/steering-reports-p1.md:1 | format, pointer, output size or procedure, held or re-homed |
| C-1585 | no | held at skills/chantier/references/topics/titles.md:1 | format, pointer, output size or procedure, held or re-homed |
| C-1602 | no | open | no home found at the head; seed: card ticket-summary-example.md:1; no rule: the sample's provenance, dropped |
| C-1603 | no | open | no home found at the head; seed: card ticket-summary-example.md:3 |
| C-1606 | no | open | no home found at the head; seed: card ticket-summary-example.md:9 |
| C-1607 | no | open | inferable: no quiz case names it |
| C-161 | no | open | no home found at the head; seed: card chief-of-staff.md:35; no rule: a pointer |
| C-1610 | no | open | inferable: no quiz case names it |
| C-1613 | no | open | inferable: no quiz case names it |
| C-1614 | no | open | inferable: no quiz case names it |
| C-1616 | no | open | inferable: no quiz case names it |
| C-1617 | no | open | inferable: no quiz case names it |
| C-165 | no | open | no home found at the head; seed: card chief-of-staff.md:35; no rule: a pointer |
| C-190 | no | open | inferable: no quiz case names it |
| C-255 | no | open | no home found at the head; seed: topic first-turn |
| C-286 | no | open | host row (unproved bookkeeping dropped from the topic) |
| C-315 | no | open | no home found at the head; seed: topic compacting |
| C-345 | no | open | inferable: no quiz case names it |
| C-375 | no | open | inferable: no quiz case names it |
| C-472 | no | open | host row (unproved bookkeeping dropped from the topic) |
| C-495 | no | open | no home found at the head; seed: card chief-of-staff.md:39 |
| C-625 | no | open | no home found at the head; seed: topic seat; the rule it applies: card chief-of-staff.md:3 |
| C-643 | no | open | no home found at the head; seed: topic watcher-lines |
| C-659 | no | open | no home found at the head; seed: topic watcher-events |
| C-669 | no | open | no home found at the head; seed: topic watcher-board; topic watcher-events |
| C-697 | no | open | no home found at the head; seed: topic merge-words; the rule it applies: floor 1 |
| C-748 | no | open | no home found at the head; seed: topic merge-series-stack; no rule: procedure |
| C-902 | no | open | no home found at the head; seed: topic direct-mode |
| C-932 | no | held at skills/chantier/references/concepts.md:93 | format, pointer, output size or procedure, held or re-homed |
| D-006 | no | restored at skills/chantier/references/cr-driver.md:16 | part of the context rules O-158 restores |
| D-009 | no | open | inferable: no quiz case names it |
| D-010 | no | open | reading discipline, no effect a refusal does not catch |
| D-011 | no | open | token economy of reading, topics only |
| D-012 | no | open | token economy of reading, topics only |
| D-013 | no | open | token economy of reading, topics only |
| D-014 | yes | restored at skills/chantier/references/cr-driver.md:12 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| D-016 | no | open | worker replies and outputs, topics only |
| D-017 | yes | held at skills/chantier/scripts/cli/src/chantier/rails.py:313 | unwanted act, refusal passed over, lost work or stuck batch |
| D-018 | no | open | named by the Inspector; worker model as printed, concepts.md only; floor 3 forbids a look-alike |
| D-019 | no | open | worker replies and outputs, topics only |
| D-020 | no | open | worker replies and outputs, topics only |
| D-021 | no | open | named by the Inspector; the worker prompt lines, concepts.md only; `brief` and `take` print them |
| D-024 | yes | restored at skills/chantier/references/cr-driver.md:12 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| D-025 | no | open | raw-log place, topic cr-prompt only |
| D-026 | yes | restored at skills/chantier/references/cr-driver.md:15 | unwanted act, refusal passed over, lost work or stuck batch |
| D-027 | no | restored at skills/chantier/references/cr-driver.md:15 | part of the context rules O-158 restores |
| D-028 | yes | restored at skills/chantier/references/cr-driver.md:16 | unwanted act, refusal passed over, lost work or stuck batch |
| D-030 | yes | restored at skills/chantier/references/cr-driver.md:16 | unwanted act, refusal passed over, lost work or stuck batch |
| D-031 | no | open | named by the Inspector; section pointer, its rules in topic handback-other |
| D-032 | no | restored at skills/chantier/references/cr-driver.md:16 | part of the context rules O-158 restores |
| D-035 | yes | restored at skills/chantier/references/cr-driver.md:23 | unwanted act, refusal passed over, lost work or stuck batch |
| D-036 | no | open | background tasks: the card's end line stops them |
| D-037 | no | open | background tasks: the card's end line stops them |
| D-038 | no | held at skills/chantier/scripts/cli/src/chantier/commands/crs.py:50 | format, pointer, output size or procedure, held or re-homed |
| D-039 | no | open | output economy of git listings, topic only |
| D-040 | no | open | rebase-first order, topic cr-ship; floor 10 holds the process rule |
| D-041 | yes | restored at skills/chantier/references/cr-driver.md:10 | unwanted act, refusal passed over, lost work or stuck batch |
| D-044 | no | held at skills/chantier/references/topics/conflicts-early-push.md:1 | format, pointer, output size or procedure, held or re-homed |
| D-045 | yes | restored at skills/chantier/references/cr-driver.md:10 | unwanted act, refusal passed over, lost work or stuck batch |
| D-047 | yes | restored at skills/chantier/references/cr-driver.md:23 | unwanted act, refusal passed over, lost work or stuck batch |
| D-048 | no | restored at skills/chantier/references/cr-driver.md:16 | part of the context rules O-158 restores |
| D-050 | yes | restored at skills/chantier/references/cr-driver.md:11 | unwanted act, refusal passed over, lost work or stuck batch |
| D-051 | yes | restored at skills/chantier/references/cr-driver.md:11 | unwanted act, refusal passed over, lost work or stuck batch |
| D-052 | yes | restored at skills/chantier/references/cr-driver.md:11 | unwanted act, refusal passed over, lost work or stuck batch |
| D-053 | no | open | CI procedure, topics; the card holds what makes CI green |
| D-054 | no | open | CI procedure, topics; the card holds what makes CI green |
| D-055 | no | restored at skills/chantier/references/cr-driver.md:16 | part of the context rules O-158 restores |
| D-056 | no | open | CI procedure, topics; the card holds what makes CI green |
| D-058 | no | open | commit message style, topic cr-ship only |
| D-064 | no | open | hand-back reasons and closing steps, topics; `handback` refuses |
| D-065 | no | open | named by the Inspector; wait types, refused hand-backs: CLI, topic handback-other |
| D-066 | no | open | round and ship order, topics; `ship` and `handback` refuse |
| D-068 | no | open | round and ship order, topics; `ship` and `handback` refuse |
| D-070 | no | open | hand-back reasons and closing steps, topics; `handback` refuses |
| D-077 | yes | restored at skills/chantier/references/stack-driver.md:21 | unwanted act, refusal passed over, lost work or stuck batch |
| D-078 | no | open | restack reading order, topic stack-restack; `ship` refuses a break |
| D-080 | no | open | restack reading order, topic stack-restack; `ship` refuses a break |
| D-082 | yes | restored at skills/chantier/references/qa-driver.md:15 | unwanted act, refusal passed over, lost work or stuck batch |
| D-084 | yes | restored at skills/chantier/references/release-driver.md:17 | unwanted act, refusal passed over, lost work or stuck batch |
| D-090 | no | open | release notes choice, topic release-notes only |
| FM-004 | no | held at skills/chantier/references/foreman.md:10 | format, pointer, output size or procedure, held or re-homed |
| FM-005 | no | open | no home found at the head; seed: card foreman.md:6 |
| FM-008 | no | held at skills/chantier/references/foreman.md:10 | format, pointer, output size or procedure, held or re-homed |
| FM-010 | no | open | no home found at the head; seed: card foreman.md:3 |
| FM-012 | no | open | no home found at the head; seed: card foreman.md:3 |
| FM-017 | no | held at skills/chantier/references/foreman.md:32 | format, pointer, output size or procedure, held or re-homed |
| FM-034 | no | open | pointer to a removed old reading, no single head home |
| FM-035 | no | open | pointer to a removed old reading, no single head home |
| FM-036 | no | held at skills/chantier/references/topics/hold.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-037 | no | held at skills/chantier/references/topics/lost-driver.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-038 | no | held at skills/chantier/references/topics/mode-switch-p1.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-039 | no | held at skills/chantier/references/topics/lost-context.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-040 | no | held at skills/chantier/references/topics/escalation.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-041 | no | held at skills/chantier/references/topics/conflict-check.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-042 | no | held at skills/chantier/references/topics/release-take.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-043 | no | held at skills/chantier/references/topics/refused-push-route.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-044 | no | held at skills/chantier/references/topics/retro.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-045 | no | held at skills/chantier/references/topics/stack.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-046 | no | open | pointer to a removed old reading, no single head home |
| FM-047 | no | open | pointer to a removed old reading, no single head home |
| FM-048 | no | open | pointer to a removed old reading, no single head home |
| FM-050 | no | open | inferable: no quiz case names it |
| FM-051 | no | held at skills/chantier/references/foreman.md:13 | format, pointer, output size or procedure, held or re-homed |
| FM-062 | no | open | superseded: `brief` writes the whole Driver prompt (CR-510) |
| FM-064 | no | open | no home found at the head; seed: card foreman.md:13 ("copy whole the prompt"); card concepts.md:105 |
| FM-093 | no | held at skills/chantier/references/topics/stack.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-101 | no | open | no home found at the head; seed: card foreman.md:38 |
| FM-115 | no | open | inferable: no quiz case names it |
| FM-129 | no | open | inferable: no quiz case names it |
| FM-163 | no | open | pointer to a removed old reading, no single head home |
| FM-164 | no | held at skills/chantier/references/topics/stack.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-165 | no | held at skills/chantier/references/topics/stack.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-168 | no | open | inferable: no quiz case names it |
| FM-263 | no | open | inferable: no quiz case names it |
| FM-264 | no | open | inferable: no quiz case names it |
| FM-281 | no | held at skills/chantier/references/topics/stack-merge.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-291 | no | open | inferable: no quiz case names it |
| FM-292 | no | open | inferable: no quiz case names it |
| FM-312 | no | open | inferable: no quiz case names it |
| FM-313 | no | open | inferable: no quiz case names it |
| FM-315 | no | open | inferable: no quiz case names it |
| FM-316 | no | open | inferable: no quiz case names it |
| FM-334 | no | open | inferable: no quiz case names it |
| FM-335 | no | open | inferable: no quiz case names it |
| FM-349 | no | open | inferable: no quiz case names it |
| FM-393 | no | open | inferable: no quiz case names it |
| FM-404 | no | open | no home found at the head; seed: topic lost-driver |
| FM-436 | no | open | inferable: no quiz case names it |
| FM-473 | no | held at skills/chantier/references/topics/conflict-check.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-476 | no | held at skills/chantier/references/topics/conflict-check.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-486 | no | open | inferable: no quiz case names it |
| FM-489 | no | open | host row (Copilot reference: `hosts/copilot.md`) |
| FM-492 | no | open | inferable: no quiz case names it |
| FM-494 | yes | restored at skills/chantier/references/foreman.md:18 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| FM-495 | yes | restored at skills/chantier/references/foreman.md:18 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| FM-507 | yes | restored at skills/chantier/references/foreman.md:18 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| FM-508 | yes | restored at skills/chantier/references/foreman.md:18 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| FM-513 | no | held at skills/chantier/references/topics/release-take.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-541 | yes | restored at skills/chantier/references/foreman.md:23 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| FM-548 | no | held at skills/chantier/references/topics/refused-push-route.md:1 | format, pointer, output size or procedure, held or re-homed |
| FM-552 | no | open | no home found at the head; seed: topic refused-push-route |
| FM-558 | yes | restored at skills/chantier/references/foreman.md:23 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| FM-577 | no | open | named by the Inspector; record each refusal once, not in floor or card |
| FM-578 | no | open | named by the Inspector; record each refusal once, not in floor or card |
| FM-582 | yes | held at skills/chantier/references/foreman.md:23 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| FM-584 | yes | restored at skills/chantier/references/foreman.md:23 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| FM-586 | no | open | named by the Inspector; P10 rebase rule read first, topic only; a miss is a host refusal |
| FM-595 | no | open | named by the Inspector; record each refusal once, not in floor or card |
| FM-B006 | no | held at skills/chantier/references/foreman.md:15 | named by the Inspector; format, pointer, output size or procedure, held or re-homed |
| FM-B012 | no | open | dropped (unproved bookkeeping, kind d; no host row holds it) |
| FM-B017 | no | open | dropped (unproved bookkeeping, kind d; no host row holds it) |
| FM-B037 | no | held at skills/chantier/scripts/cli/src/chantier/rails.py:62 | format, pointer, output size or procedure, held or re-homed |
| FM-B039 | no | open | inferable: no quiz case names it |
| FM-B047 | no | open | inferable: no quiz case names it |
| FM-B053 | no | held at skills/chantier/references/foreman.md:25 | format, pointer, output size or procedure, held or re-homed |
| G-005 | no | held at skills/chantier/references/topics/titles.md:1 | format, pointer, output size or procedure, held or re-homed |
| G-009 | no | open | no home found at the head; seed: topic grill-restate; topic grill-critic-steps |
| G-010 | no | open | inferable: no quiz case names it |
| G-017 | no | open | no home found at the head; seed: topic first-turn; the rule it applies: card griller-skill.md:5 |
| G-050 | no | open | no home found at the head; seed: topic titles |
| H-001 | no | open | inferable: no quiz case names it |
| H-002 | no | open | inferable: no quiz case names it |
| H-003 | no | open | inferable: no quiz case names it |
| H-004 | no | open | inferable: no quiz case names it |
| H-005 | no | open | inferable: no quiz case names it |
| H-006 | no | open | inferable: no quiz case names it |
| H-007 | no | open | inferable: no quiz case names it |
| H-008 | no | open | inferable: no quiz case names it |
| H-009 | no | open | inferable: no quiz case names it |
| H-010 | no | open | inferable: no quiz case names it |
| H-042 | no | open | no home found at the head; seed: card concepts.md:14 |
| H-050 | no | open | no home found at the head; seed: card concepts.md:41 |
| H-071 | no | open | inferable: no quiz case names it |
| H-075 | no | open | inferable: no quiz case names it |
| H-076 | no | open | inferable: no quiz case names it |
| H-077 | no | open | inferable: no quiz case names it |
| H-081 | no | open | inferable: no quiz case names it |
| H-090 | no | open | inferable: no quiz case names it |
| H-1002 | no | open | no home found at the head; seed: topic host-auto-fix |
| H-1006 | no | open | inferable: no quiz case names it |
| H-1010 | no | open | inferable: no quiz case names it |
| H-1011 | no | open | no home found at the head; seed: topic host-auto-fix |
| H-1014 | no | open | inferable: no quiz case names it |
| H-1015 | no | open | no home found at the head; seed: topic host-auto-fix |
| H-1025 | no | open | no home found at the head; seed: topic host-turn-end |
| H-1033 | no | open | no home found at the head; seed: topic host-turn-end |
| H-1070 | no | open | inferable: no quiz case names it |
| H-1071 | no | open | inferable: no quiz case names it |
| H-1073 | no | open | inferable: no quiz case names it |
| H-1080 | no | open | inferable: no quiz case names it |
| H-1105 | no | open | no home found at the head; seed: card hosts/claude-code.md:24 |
| H-111 | no | open | no home found at the head; seed: card concepts.md:43 |
| H-1120 | no | open | no home found at the head; seed: card hosts/claude-code.md:39 |
| H-1123 | no | open | no home found at the head; seed: card hosts/claude-code.md:42 |
| H-1124 | no | open | no home found at the head; seed: card hosts/claude-code.md:43 |
| H-1129 | no | open | no home found at the head; seed: card hosts/claude-code.md:48 |
| H-113 | no | open | a remark on the old text, no single head home |
| H-1130 | no | open | no home found at the head; seed: card hosts/claude-code.md:49 |
| H-1131 | no | open | no home found at the head; seed: card hosts/claude-code.md:50 |
| H-1134 | no | open | no home found at the head; seed: card hosts/claude-code.md:53 |
| H-115 | no | open | no home found at the head; seed: card concepts.md:55 |
| H-1175 | no | open | inferable: no quiz case names it |
| H-1181 | no | open | no home found at the head; seed: topic host-refused |
| H-1187 | no | open | no home found at the head; seed: topic host-auto-mode |
| H-1215 | no | open | no home found at the head; seed: topic host-auto-mode-trials |
| H-1233 | no | open | no home found at the head; seed: topic host-auto-mode-trials; no rule: a measurement, not carried |
| H-1252 | no | open | inferable: no quiz case names it |
| H-1254 | no | open | no home found at the head; seed: topic host-compact |
| H-1260 | no | open | inferable: no quiz case names it |
| H-1265 | no | open | no home found at the head; seed: topic host-compact |
| H-1285 | no | open | inferable: no quiz case names it |
| H-1293 | no | open | inferable: no quiz case names it |
| H-1295 | no | open | no home found at the head; seed: topic host-sessions |
| H-1340 | no | open | no home found at the head; seed: topic host-surfaces |
| H-1341 | no | open | no home found at the head; seed: topic host-surfaces |
| H-1344 | no | open | no home found at the head; seed: topic host-surfaces |
| H-1346 | no | open | no home found at the head; seed: topic host-surfaces |
| H-1360 | no | open | dropped by sc21-Q1, owner to confirm; the card bars widening a grant |
| H-1391 | no | open | no home found at the head; seed: topic host-for-you |
| H-1421 | yes | held at skills/chantier/references/chief-of-staff.md:13 | unwanted act, refusal passed over, lost work or stuck batch |
| H-1429 | no | open | inferable: no quiz case names it |
| H-1430 | no | open | no home found at the head; seed: topic host-for-you |
| H-1437 | no | open | no home found at the head; seed: topic host-allow-add |
| H-145 | no | open | no home found at the head; seed: topic stack-grows |
| H-1453 | no | open | inferable: no quiz case names it |
| H-1454 | no | open | inferable: no quiz case names it |
| H-1455 | no | open | inferable: no quiz case names it |
| H-1456 | no | open | inferable: no quiz case names it |
| H-1461 | no | open | inferable: no quiz case names it |
| H-1521 | no | held at skills/chantier/references/topics/worker-shell.md:1 | format, pointer, output size or procedure, held or re-homed |
| H-1526 | no | open | no home found at the head; seed: topic host-compact |
| H-1535 | no | held at skills/chantier/references/status-layout.md:5 | format, pointer, output size or procedure, held or re-homed |
| H-1542 | no | open | no home found at the head; seed: card skills/chantier-SKILL.md:23 |
| H-1546 | yes | held at skills/chantier/references/floor.md:5 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| H-1547 | no | open | inferable: no quiz case names it |
| H-1549 | no | open | inferable: no quiz case names it |
| H-1552 | no | open | inferable: no quiz case names it |
| H-1553 | no | open | inferable: no quiz case names it |
| H-1554 | no | open | inferable: no quiz case names it |
| H-1556 | no | open | inferable: no quiz case names it |
| H-1577 | no | open | held in the skill's SKILL.md launch paragraph, not a role card |
| H-1590 | no | open | inferable: no quiz case names it |
| H-1599 | yes | held at skills/chantier/references/chief-of-staff.md:14 | unwanted act, refusal passed over, lost work or stuck batch |
| H-1607 | no | held at skills/chantier/references/chief-of-staff.md:3 | format, pointer, output size or procedure, held or re-homed |
| H-1612 | no | open | no home found at the head; seed: card skills/chief-of-staff-SKILL.md:35 |
| H-1621 | no | open | held in the skill's SKILL.md launch paragraph, not a role card |
| H-1641 | no | open | held in the skill's SKILL.md launch paragraph, not a role card |
| H-1649 | no | open | held at skills/status/SKILL.md:19, the status skill's file, not a role card |
| H-1650 | no | open | inferable: no quiz case names it |
| H-166 | no | held at skills/chantier/references/topics/stack-changes.md:1 | format, pointer, output size or procedure, held or re-homed |
| H-1695 | yes | held at skills/chantier/references/foreman.md:23 | unwanted act, refusal passed over, lost work or stuck batch |
| H-1737 | no | open | held in the copilot host row; floor 3 forbids a look-alike model |
| H-1751 | yes | held at skills/chantier/references/foreman.md:23 | unwanted act, refusal passed over, lost work or stuck batch |
| H-201 | no | open | inferable: no quiz case names it |
| H-207 | no | open | inferable: no quiz case names it |
| H-223 | no | open | no home found at the head; seed: topic release-ship |
| H-243 | no | open | inferable: no quiz case names it |
| H-287 | no | held at skills/chantier/references/foreman.md:13 | named by the Inspector; format, pointer, output size or procedure, held or re-homed |
| H-299 | yes | held at skills/chantier/references/floor.md:7 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| H-301 | no | open | named by the Inspector; work without a missing skill or tool, in concepts.md and worker-shell |
| H-304 | no | open | no home found at the head; seed: card concepts.md:87 |
| H-305 | no | open | superseded: `brief` writes a worker's prompt (CR-510) |
| H-309 | no | held at skills/chantier/references/concepts.md:95 | format, pointer, output size or procedure, held or re-homed |
| H-313 | no | open | no home found at the head; seed: card concepts.md:99 |
| H-314 | no | open | inferable: no quiz case names it |
| H-315 | no | open | no home found at the head; seed: card concepts.md:107 |
| H-318 | no | open | no home found at the head; seed: card concepts.md:107 |
| H-320 | no | open | inferable: no quiz case names it |
| H-330 | no | open | no home found at the head; seed: card concepts.md:119 |
| H-331 | no | open | no home found at the head; seed: card concepts.md:119 |
| H-344 | yes | held at skills/chantier/references/cr-driver.md:27 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| H-356 | no | open | no home found at the head; seed: card concepts.md:129 |
| H-357 | no | open | no home found at the head; seed: card concepts.md:129 |
| H-373 | no | open | named by the Inspector; model escalation wording, concepts.md only; floor 3 forbids a look-alike |
| H-379 | no | open | no home found at the head; seed: card concepts.md:140 |
| H-387 | no | open | inferable: no quiz case names it |
| H-390 | no | held at skills/chantier/references/topics/escalation.md:1 | format, pointer, output size or procedure, held or re-homed |
| H-391 | yes | held at skills/chantier/scripts/cli/src/chantier/rails.py:313 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| H-401 | no | open | inferable: no quiz case names it |
| H-402 | no | open | named by the Inspector; work without a missing skill or tool, in concepts.md and worker-shell |
| H-425 | yes | restored at skills/chantier/references/cr-driver.md:22 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| H-433 | no | open | inferable: no quiz case names it |
| H-440 | no | open | inferable: no quiz case names it |
| H-441 | no | open | inferable: no quiz case names it |
| H-446 | no | open | inferable: no quiz case names it |
| H-449 | no | open | no home found at the head; seed: topic session-shell |
| H-459 | no | open | no home found at the head; seed: card pr-template.md:12 |
| H-470 | no | open | no home found at the head; seed: card pr-template.md:15 |
| H-473 | no | open | no home found at the head; seed: card pr-template.md:16 |
| H-491 | no | open | no home found at the head; seed: card pr-template.md:20 |
| H-503 | no | open | no home found at the head; seed: card pr-template.md:22 |
| H-507 | no | open | no home found at the head; seed: card pr-template.md:22 |
| H-527 | no | open | inferable: no quiz case names it |
| H-528 | no | open | inferable: no quiz case names it |
| H-581 | no | open | no home found at the head; seed: card release-template.md:44 |
| H-582 | no | open | no home found at the head; seed: card release-template.md:45 |
| H-584 | no | open | no home found at the head; seed: card release-template.md:46 |
| H-706 | no | open | the sync-pending report item, topic only; the offer still asks a yes |
| H-750 | no | open | no home found at the head; seed: topic compacting |
| H-774 | yes | held at skills/chantier/references/chief-of-staff.md:13 | unwanted act, refusal passed over, lost work or stuck batch |
| H-778 | yes | held at skills/chantier/references/chief-of-staff.md:13 | unwanted act, refusal passed over, lost work or stuck batch |
| H-779 | yes | held at skills/chantier/references/chief-of-staff.md:13 | unwanted act, refusal passed over, lost work or stuck batch |
| H-808 | yes | held at skills/chantier/references/chief-of-staff.md:13 | unwanted act, refusal passed over, lost work or stuck batch |
| H-832 | yes | held at skills/chantier/references/chief-of-staff.md:13 | unwanted act, refusal passed over, lost work or stuck batch |
| H-833 | no | open | init's forge-tool recommendation, topic only |
| H-848 | no | open | no home found at the head; seed: card review-step.md:3 |
| H-850 | no | open | inferable: no quiz case names it |
| H-853 | no | open | inferable: no quiz case names it |
| H-854 | no | open | inferable: no quiz case names it |
| H-855 | no | open | held at review-step.md, the added review step's card, not a roles.yaml card |
| H-856 | no | open | held at review-step.md, the added review step's card, not a roles.yaml card |
| H-858 | no | open | inferable: no quiz case names it |
| H-860 | no | open | held at review-step.md, the added review step's card, not a roles.yaml card |
| H-863 | no | open | held at review-step.md, the added review step's card, not a roles.yaml card |
| H-864 | no | open | held at review-step.md, the added review step's card, not a roles.yaml card |
| H-865 | no | open | held at review-step.md, the added review step's card, not a roles.yaml card |
| H-878 | no | open | no home found at the head; seed: card review-step.md:9 |
| H-881 | no | open | inferable: no quiz case names it |
| H-885 | no | open | no home found at the head; seed: card review-step.md:17 |
| H-889 | no | open | inferable: no quiz case names it |
| H-895 | no | open | held at sync-checkout.md and topic sync-offer-p1, not a role card |
| H-897 | no | open | held at sync-checkout.md and topic sync-offer-p1, not a role card |
| H-899 | no | open | held at sync-checkout.md and topic sync-offer-p1, not a role card |
| H-905 | no | open | held at sync-checkout.md and topic sync-offer-p1, not a role card |
| H-907 | no | open | held at sync-checkout.md and topic sync-offer-p1, not a role card |
| H-929 | no | open | inferable: no quiz case names it |
| H-930 | no | open | inferable: no quiz case names it |
| H-931 | no | open | inferable: no quiz case names it |
| H-932 | no | open | inferable: no quiz case names it |
| H-938 | no | open | inferable: no quiz case names it |
| P-001 | yes | restored at skills/chantier/references/cr-driver.md:12 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| P-002 | no | open | named by the Inspector; lease renewal, held by the CLI's commands and topic lease |
| P-003 | no | open | checkpoint message, topic checkpoints only |
| P-005 | yes | held at skills/chantier/references/cr-driver.md:20 | unwanted act, refusal passed over, lost work or stuck batch |
| P-006 | no | open | named by the Inspector; pointer to the re-take notes, topic restart |
| P-007 | no | open | re-take inside a stack, topic retake-stack only |
| P-008 | no | open | named by the Inspector; matrix probe, topic matrix only |
| P-009 | no | held at skills/chantier/references/cr-driver.md:5 | named by the Inspector; format, pointer, output size or procedure, held or re-homed |
| P-010 | no | open | named by the Inspector; remote failures, topic trouble-remote only |
| P-011 | no | restored at skills/chantier/references/cr-driver.md:16 | part of the context rules O-158 restores |
| P-013 | no | open | named by the Inspector; carry and conflict, topic conflicts only |
| P-014 | no | open | named by the Inspector; unusual hand-backs, topic handback-other only |
| P-015 | yes | held at skills/chantier/references/floor.md:12 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| P-016 | yes | restored at skills/chantier/references/stack-driver.md:21 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| P-017 | yes | restored at skills/chantier/references/stack-driver.md:10 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| P-018 | yes | restored at skills/chantier/references/stack-driver.md:21 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| P-019 | yes | held at skills/chantier/references/stack-driver.md:5 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| P-020 | yes | held at skills/chantier/references/release-driver.md:26 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| P-022 | yes | held at skills/chantier/references/release-driver.md:7 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| P-023 | yes | held at skills/chantier/references/release-driver.md:7 | named by the Inspector; unwanted act, refusal passed over, lost work or stuck batch |
| W-010 | no | open | inferable: no quiz case names it |
| W-025 | no | open | inferable: no quiz case names it |
| W-047 | no | open | inferable: no quiz case names it |
| W-052 | yes | restored at skills/chantier/references/conflict-resolver.md:17 | unwanted act, refusal passed over, lost work or stuck batch |
| W-062 | yes | restored at skills/chantier/references/conflict-resolver.md:10 | unwanted act, refusal passed over, lost work or stuck batch |
| W-085 | no | open | inferable: no quiz case names it |
| W-117 | no | open | inferable: no quiz case names it |
| W-144 | no | open | inferable: no quiz case names it |
| W-157 | no | open | inferable: no quiz case names it |
| W-200 | no | open | inferable: no quiz case names it |
| W-206 | no | open | inferable: no quiz case names it |
| W-220 | no | open | inferable: no quiz case names it |
| W-243 | no | open | inferable: no quiz case names it |
| W-254 | no | open | inferable: no quiz case names it |
| W-263 | no | open | inferable: no quiz case names it |
| W-271 | no | open | inferable: no quiz case names it |
| W-292 | no | open | inferable: no quiz case names it |
| W-307 | no | open | inferable: no quiz case names it |
| W-319 | no | held at skills/chantier/references/verifier.md:21 | format, pointer, output size or procedure, held or re-homed |
| W-323 | no | open | no home found at the head; seed: card verifier.md (Cite the gate pass by its log's first line and `handoff`); refusal: `handback` without a gate pass |
| W-362 | no | open | inferable: no quiz case names it |
| W-367 | no | held at skills/chantier/references/griller.md:16 | format, pointer, output size or procedure, held or re-homed |
| X-003 | no | open | topic cr-workers |
| X-004 | yes | restored at skills/chantier/references/stack-driver.md:10 | unwanted act, refusal passed over, lost work or stuck batch |
| X-005 | yes | restored at skills/chantier/references/stack-driver.md:10 | unwanted act, refusal passed over, lost work or stuck batch |
| X-006 | no | open | topic stack-record |
| X-008 | no | open | pointer to a removed old reading, no single head home |
