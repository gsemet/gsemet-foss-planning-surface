# CR-218 map (read-only, worktree batch-16-CR-218, base 7705f00)

Line numbers are from the worktree files.

## 1. Places to change

pr-template.md (skills/chantier/references/)
- 5-9 scope; 31-34 "No internal reference" rule (role names named there: "no agent role (Driver, Coder, Inspector...)"); 51-56 layout rule (Summary..Autonomous decisions visible); 77-84 UNVERIFIED rule (new Known-gaps tie-in); 92-94 Autonomous decisions bullet (put Known gaps after it); 102-108 first template comment (role-name line); 136-138 Autonomous decisions block (add `## Known gaps` before `<details>` at 140); 179-206 audit: item 1 (183-185 section list), item 2 (186-190 visible list), item 3 (191-192 internal refs), item 7 (198-199); last item is 9 (202-203), so "item 10" is free.

driver.md
- 71-90 Push bullet (pr-body.md written/posted: `gh pr create/edit --body-file`, `glab mr` at 80-81): add the pre-post check there.
- 111-115 evidence bullet (`gh pr edit --attach`; used by the screenshot flow).
- 166-181 "Your end" bullet: ready line; 177-178 is the draft text `handback <cr> ready <link> draft on <base>: waits for <what>`: add `gaps: ...`.
- 222-245 CR driver section: 225-229 pr-body.md rounds; 239-243 UNVERIFIED and description pass; add the pre-post read and "gap said elsewhere goes in pr-body.md first".
- Also ready-line mentions to keep consistent: 279-282 (taken back, re-ready), 330 (stack `[stack->foreman] hand-back ready`), 418, 432 (`handback ready <pr link>`).

worker.md
- 68-72 Inspector (pr-body.md audit; no new text).
- 99-107 Verifier description paragraph: add Known gaps claims and the role-name rule here (line 104 UNVERIFIED sentence is the anchor).

foreman.md
- 39-45 `ready <cr> <link>` ask (+ `no long gate:`, draft text); add `gaps:`. 151-160 stack-ready flow; 171-173 asks line list (`ready`, `blocked`, `released`, `stack-ready <stack link> <cr>=<link>...`). 233 mentions /reload-plugins (cards load).

chief-of-staff.md
- 412-416 series bullet (each `ready` ask); 417-424 stack bullet (`stack-ready`); add gap quoting. 36 table row, 623-629 mentions stack-ready; no change needed there.

Other places that list the sections / ready line / asks
- docs/use-cases.md 132-140 (sections list; line 138-140 also says "name no CR, batch, round or agent").
- skills/chantier/references/routing.md 11 (Foreman to CoS asks), 16 (Driver to Foreman `hand-back ready <link> [<text>]`), 18 (stack driver). Text is generic: add "gaps" mention only if wanted; consistent with "text".
- skills/chantier/references/concepts.md 22 ("no CR, batch, agent role or cost"), 72 (Internal references only in a CR's PR): the role-name rule is stated here too; check they stay consistent with the new exception.
- scenario/run_scenario.py 49-53 (BODY: `## Autonomous decisions\n\nNone.\n\n<details>...` at line 51; add Known gaps before it), used at 187, 509, 3887 (written to work/pr-body.md; never audited).
- AGENTS.md (38 lines; add one bullet; the plugin-in-place bullet is lines 30-32). CONTRIBUTING.md 153-159 (plugin read live from main checkout, /reload-plugins) and 193-195 (the "no real pane" sentence to rewrite).
- CLI: commands.py `handback` ~1721-1734 (free note text after the link, no change); cli.py 154 help string "a Driver's end: ready <link> or blocked <reason>" (spec says no CLI change; leave). commands.py 783 has an unrelated "- Autonomous decisions:" line in a generated file (STATUS/handoff template, not the PR body): do not touch.
- Agents' bodies (agents/, com.github.copilot/agents/): grep finds no template-section or ready-line text. No change.
- Tests: skills/chantier/scripts/cli/tests/test_structure.py (NOT tests/): no match for pr-template, Autonomous, Known, handback or ready text; it checks links resolve (177), card presence (222-240), host card (373). No test pins the card text. Adding `Known gaps` needs no test edit. Any relative link added in a card must resolve (test 177).
- evals/ not searched in depth (excluded as out of scope); no evidence it lists the template sections.

## 2. Running a PR's head in a real session

Proved (read-only):
- A claude binary exists: C:\Users\gaeta\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\claude-code\2.1.321\d0e23af87588\claude.exe (the Desktop process CLAUDE_PID=30172; not on PATH). `claude --version` = 2.1.321.
- `claude --help` lists `--plugin-dir <path>`: "Load a plugin from a directory or .zip ... (repeatable)". It is a per-invocation flag, so it loads a worktree path without touching the main checkout or the installed plugin. `claude plugin validate <path>` and `claude plugin test [dir]` take a path too.
- Project setting (.claude/settings.json) enables `chantier@chantier`; the installed one is read live from the main checkout (CONTRIBUTING 153-159).
- `/reload-plugins` reloads what is already registered (the main checkout); it cannot point at a worktree. Not a means for a PR head.

Unproved:
- Whether `--plugin-dir <worktree>` overrides the installed `chantier@chantier` (same plugin name) or loads beside it / is ignored on a name clash. Also whether hooks/register.tsx (the board pane) is loaded and drawn from `--plugin-dir`. Not run: it needs an interactive session and would be a new session, so it cannot be proved read-only. The help text does not say.
- Whether Claude Desktop (not the CLI) accepts `--plugin-dir`; only the CLI binary's help was read. A terminal session with the exe above is the one proved to have the flag.
- Whether the user's own machine has the same binary path.

Wording for CONTRIBUTING: "start a session with `claude --plugin-dir <worktree of the PR's branch>` (flag in `claude --help`, 2.1.321); that it replaces the installed copy of the same name, and that the board pane draws from it, is unproved: check the pane's behaviour (a change visible in the PR's head, absent on main) in the screenshot itself." Do not say `/reload-plugins` for it.

## 3. Evidence plan
1. `just check`, then `just scenario` (CLI/cards/scenario changed); no `just mod` (hooks/types untouched).
2. grep the cards for "Known gaps" and "gaps:": expect pr-template (rules 4 places: rule, layout, template block, audit items 1/2/new), driver (ready line, pre-post check), worker (Verifier), foreman (ready, stack-ready), chief-of-staff (series and stack bullets), use-cases.md, scenario BODY, AGENTS.md, CONTRIBUTING.md.
3. Read-back of the audit numbering (new item 10 or renumbered) and that the template comment and item 3 say the same role-name rule.
4. Check the CR's own PR body: Known gaps present, role names only as product terms (this CR changes the role cards), nothing as "the Driver chose".
5. Check scenario BODY still satisfies `chantier` CLI flows (it is not audited).
6. No screenshot (board untouched); the Known gaps of this PR should name that the `--plugin-dir` override of an installed plugin is unproved (if the CONTRIBUTING text says so).
