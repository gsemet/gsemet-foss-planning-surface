# CR-170 investigation: current text and line map (worktree batch-09-CR-170, base origin/main)

Paths below are under `skills/chantier/references/` unless stated.

## Places to change (spec line numbers are off in two spots)

| Area | File:lines (actual) | Current text |
| --- | --- | --- |
| 1 | chief-of-staff.md:319-331 | One bullet "A refused force push": runs the push (exception to "do no Driver's work"), from the main checkout, `git push --force-with-lease=<branch>:<expected> <remote> <local sha>:refs/heads/<branch>`; check first (CR from branch name, `$CHANTIER handoff <cr>`, `worktree: ... branch` line must match, never the default branch) else `push refused <branch>: not a branch of this batch`; failed lease -> `push failed <branch> <git's text>`; done -> `pushed <branch>`; all to the Foreman; own push refused -> show exact text, `push refused <branch>: <exact text>`, retry nothing, never change permissions. No judgement step, no "not a question for the user", nothing about what the user hears. |
| 2 | chief-of-staff.md:466-469 (spec said ~457) | "Nothing is sent to yourself ... A Driver's refused force push is run by you, as above; the Driver hears the result as a note." |
| never list | chief-of-staff.md:622-623 (spec said ~604) | "In Foreman mode, message a Driver or do the Foreman's or a Driver's work (but the refused force push above)". Stays as is. |
| 3 | driver.md:93-100 (spec ~93 ok) | "A force push the host refuses (any Driver that pushes): the Chief of Staff runs it for you." then the push line, wait, "The steering session tells you the result", failed lease, `push refused` -> `handback blocked refused <exact text>`. Lines 138 and 174 ("a refused one goes up as written above / as above") need no change. |
| 3 | foreman.md:125-132 (spec said ~116; line 116 is a different bullet) | The sentence is at 131: "A push the host refuses the Chief of Staff too is the user's, shown by it; the Driver hears `push refused <branch>: <exact text>` and hands back." The Foreman passes the line as is, not through `asks`, and tells the Driver `note push <branch>: <the answer>`. |
| 4 | hosts/claude-code.md:200-201 (spec ~200 ok) | "A refusal is reported with its exact text (concepts rule 7). A refused force push takes the route already written (`driver.md`, `foreman.md`: Driver -> Foreman -> Chief of Staff)." Allow-rules table rows 109-110 and JSON lines 127-130 stay (checked by a test, see below). |
| 5 | status-layout.md:53 (spec ~51) | Progress: line 53 is the chain-line sentence ("When a CR is chained ... your next report has a line with the chain and its reason."). Add the pushed-for-the-Driver line next to it. Lines 46-47: the **For you:** last line. |

Other mentions, no contradiction found:
- routing.md:11: Foreman -> Chief of Staff `push <branch> <expected remote sha> <local sha>` "a Driver's refused force push, passed as it came". Nothing says the user is asked; no change. The answers `pushed`, `push failed`, `push refused` are not listed as messages in routing.md (only the push line), so "no new message" holds.
- chief-of-staff.md:160: "never a force push" is about the setup/clone sync (a rebase on a rejected push); unrelated, keep. Could confuse a reader only slightly; leave.
- driver.md:39: `git push --force-with-lease -u <remote> <branch>` only for a rewrite; unrelated.
- concepts.md:258, 261: `--force-with-lease` after a rewrite; no mention of refusal or the route. No contradiction.
- hosts/claude-code.md:109-110, 127-130: permission rules; unchanged.
- hosts/copilot.md: no force push text (confirmed by grep).
- Code: commands.py:171-172 (RECOMMENDED_ALLOW), commands.py:1691 message. Unchanged.
- docs/, README.md, agents/, com.github.copilot/, scenario/: no force push text (grep of "force", "pushed", "push failed", "push refused" found only unrelated "pushed head" wording).
- Chief of Staff's "do no Driver's work" exception wording is in the bullet at 319-320 and the never list at 622; "Foreman's card" has no "do no Driver's work" text to change.

## What tests check (skills/chantier/scripts/cli/tests/test_structure.py)
- No test holds any push text (grep for "push" finds none on cards).
- test_each_host_has_its_reference_and_the_cards_hold_no_host_tool (l.206-219): the cards chief-of-staff, foreman, driver, worker, concepts, griller, session-start, status-layout must not contain the strings SendMessage, send_message, write_agent, TaskStop, ScheduleWakeup, start_session, create_session, get_session, /every, /loop, /compact, /autocompact, CLAUDE_CODE_SESSION_ID, COPILOT_AGENT_SESSION_ID outside lines containing "hosts/". The new text must avoid these (the spec's "`order note` or the host's message" is fine; do not name a tool).
- test_skill_and_references_links_resolve (l.154): markdown links in the cards must resolve; any new link (e.g. to status-layout.md) must be a real path.
- test_every_role_has_its_section_in_its_card (l.196): the `## <Role>` headings must stay; do not rename sections.
- test_the_allow_rules_json_block_lists_exactly_what_preflight_checks (l.335): the JSON block in hosts/claude-code.md "### Allow rules" must equal RECOMMENDED_ALLOW; keep the heading and block untouched (the Auto mode text at 200 is after it; check the split on "### Allow rules\n" still picks the first json block, which it does if no json block is added before it).

## Notes on the spec
- Spec line numbers to correct: direct mode ~457 is 466-469; never list ~604 is 622-623; foreman ~116 is 131; status-layout ~51 is 53.
- Area 1 asks for a read-only judgement from "the main checkout or `git -C <worktree>`". The existing bullet already uses `$CHANTIER handoff <cr>`; spec's gate check reads the `gate` event with `result` and `head` in `events.jsonl`. I did not verify the event's field names; the implementer must check them in commands.py (grep `"gate"`) before the card names them. Also the card says no hand-edit of `events.jsonl` (never list, line 55), reading is fine.
- Open questions 1-3 of the spec change the card's text (missing gate pass sent back to the Driver vs asked; failed lease: tell user without wait; own push refused: give the command). The Area 1 draft already follows the recommended answers for 2 and 3; question 1 is left open in item 3/5 (a missing gate pass is not listed under "ask"), so settle it before writing.
- Area 1 item 3 keeps the card bullet long (about 30 lines vs 13); consider making it a short sub-list to stay readable. The line length convention is about 100 columns.

## Evidence plan
1. `just check` passes (runs test_structure.py: the host-tool ban, link resolution, section headings, the allow-rules block).
2. At the PR head, Verifier read-through with `git grep -n` on the cards:
   - `git grep -n -i "not a question for the user" -- skills/chantier/references/chief-of-staff.md` finds the sentence in "A refused force push".
   - The same bullet holds the unchanged branch check (`not a branch of this batch`) and the unchanged push command (`--force-with-lease=<branch>:<expected>`).
   - The judgement's three points are present: committed head, remote work rebased onto the `base` that `handoff` prints, gate passed at the local head.
   - The three ask/tell cases each state what the user hears: judged not legitimate, failed lease, own push refused.
   - `git grep -n "without asking the user" -- skills/chantier/references/chief-of-staff.md` hits the direct-mode line (466-469 region).
   - driver.md ("judges it and runs it", the Driver keeps waiting while the steering session asks), foreman.md (the Chief of Staff may ask the user first; wait for its answer), hosts/claude-code.md Auto mode (classifier "Git Destructive" cause, proved 2026-11-11 batch-09), status-layout.md (the report line for a pushed branch) carry Areas 3-5.
   - `git grep -n -i "force push\|force-with-lease" -- skills/chantier/references/` and read each hit against the new rule: no hit says the user is asked in every case, or that the Chief of Staff always asks (current hits: chief-of-staff 160, 319, 468; concepts 258, 261; driver 39, 93, 138, 174; foreman 131; routing 11; hosts/claude-code 109-110, 127-130, 200).
   - `git diff origin/main --stat` shows only the five cards (chief-of-staff, driver, foreman, hosts/claude-code, status-layout), no CLI, agent file, routing.md or copilot.md.
   - Agents untouched: `agents/` and `com.github.copilot/agents/` need no pairing change.
3. Scenario: `just scenario` is run by the PR as AGENTS.md asks for a change to cards; it does not run the refused-push route (the scenario's Driver pushes itself), so no behaviour proof is expected from it. The rule itself is proved by reading only; its first live use is the next batch where a host refuses a Driver's force push (state it as unproved in the PR until then).
