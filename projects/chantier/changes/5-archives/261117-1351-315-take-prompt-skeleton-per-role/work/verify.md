# Verify CR-315

Head: 5c36b06aa36882f31ec9bb49e801626922163a76

Judged at 5c36b06 (all claims). Rules read (`$CHANTIER rules`): AGENTS.md, CONTRIBUTING.md and the cards; nothing beyond AGENTS.md touches this task.

## Evidence 1: structure test

- Command (worktree, 5c36b06): `uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/test_driver_prompt.py skills/chantier/scripts/cli/tests/test_cli_runs.py skills/chantier/scripts/cli/tests/test_plugin_files.py -q`
- Output: `66 passed in 10.02s`
- `test_the_drivers_prompt_table_names_each_driver_card_and_start_once[claude|copilot]` (in `tests/test_driver_prompt.py`, not in `test_plugin_files.py` as the spec suggested; it imports that file's helpers) checks: the table parses, each role has an agent file on both hosts with `Started by the steering session` and `Prompt starts with: chantier <role> for `, each card exists, `change`/`fix`/`release` each named once, `take stack` and `order qa` once. Deviation of location only; behaviour covered.

## Evidence 2: CLI tests

- Same run, 5c36b06: `test_the_commands_print_each_drivers_prompt_skeleton_without_a_writes_line_for_most[change|release|stack|qa]` and `test_a_driver_role_with_no_agent_file_is_refused_before_anything_is_recorded[qa-driver|cr-driver]` passed (exit 2, error names the role and "out of step", record and inbox unchanged); `test_an_external_surface_...` asserts `writes: <folder>; <absolute archive>` ending with the `archive:` path; `test_a_direct_batch_...` asserts `  Steering: the Chief of Staff`. A `--note` shows on `Note:` (change, release, stack, qa cases).
- Whole suite, 5c36b06: `uv run --no-sync --project . pytest -q -n auto` -> `390 passed in 21.33s` (within the 18.5 s + 30 s budget).

## Evidence 3: scenario

- `git diff HEAD~1 HEAD -- scenario/run_scenario.py` read: `check_driver_skeleton` runs after each `Foreman.take` (release/stack: no `writes:`, stack rows in the block; other CRs: one `writes:` line, folder first, absolute archive path when `archive:` printed); `qa_on_head` checks the qa-driver block after `QA folder:` with no `writes:`.
- Long gate: `gh pr checks 270 -R gsemet/chantier` at head 5c36b06: `just scenario (ubuntu-latest)  pass 2m51s`; `just check` on macos, ubuntu, windows: pass; `just eval-dry-run`: pass. I did not run `just scenario` locally (no pass exists on Windows for this head; the AGENTS.md Windows run belongs to the stack's top CR).

## Evidence 4: reading proof

- Captured at 5c36b06 from a scratch project (`C:/cvscratch/acme`, a 2-CR stack batch, CR-102 recorded as kind release; never the real batch-23 record), with the username and home folder replaced by made-up values (`/home/user`): `evidence/take-skeletons.txt` in the CR folder.
- Commands: `take CR-101 --note ...`, `take CR-102 --note ...`, `take stack --note ...`, `order qa --note "try the export on a phone"`.
- `grep -n "^  writes:\|^  Steering\|^  Team\|^  Note"` on the file: one `  writes: <folder>` (CR-101 block only); the release block (line 123) has Steering and Note, no writes, no Team; stack block has Steering, Team, Note, no writes, and holds the chain line and both CR rows; qa block has `QA folder: ...; order O-1`, `default branch: main`, Steering, `Note: try the export on a phone`, no writes, no Team. Headings of the release, stack and qa blocks say `no writes: line`.
- `grep -ic "gaeta\|Users"` on the saved file: `0`. No archive path in that run (no external surface), so the absolute-archive case rests on Evidence 2's test.
- Observation: `Steering:` and the CR/stack `Team:` stay `<...>` placeholders, as the spec says; the stack `Team:` stayed a placeholder because the scratch playbook configures no roles.

## Part 2: PR description (`gh pr view 270 -R gsemet/chantier --json body`, head 5c36b06)

- Renders clean (sections, table, code fence, fold); no images.
- Summary, Deliverables and Changes match the diff `HEAD~1..HEAD` (table in `concepts.md`, `driver_prompt.py`, `driver.py`, `orders.py`, `cli.py` order-qa no-cut, cards, tests, scenario checks); claims on exit 2 before recording and on `default branch:` failing rather than assuming `main` match `orders.py` (`_qa_row`). Not mentioned but small: `cli.py`'s output-limit change is in "order qa joins the commands..."; `test_playbook_config.py` is named.
- Known gaps bullets (worker opening lines twice; no real Driver started) are true to the evidence above (the opening lines do appear twice in the cr-driver block).
- Note for the Driver, not a failure: the Test plan boxes are unchecked and still hold `<sha7>` placeholders; fill them at the ready line with 5c36b06 (or the head then) and, for Review, a Driver note of the pass (`$CHANTIER log`). No role name outside Internal references.

## Cleanup

- I could not remove the scratch folder `C:/cvscratch` (outside my `writes:`); it holds no user data and should be deleted by the Driver.

VERIFIED

## Description pass

Head: 5c36b06aa36882f31ec9bb49e801626922163a76

Judged at 5c36b06: posted body (`gh pr view 270 -R gsemet/chantier --json body`) against `git diff --stat HEAD~1 HEAD` (13 files: cards, driver_prompt.py, driver.py, orders.py, cli.py, tests, scenario). The branch-vs-origin-CR-314 stat also shows forge_stack/facts files, which belong to the base commits (ef1041d, 1fab261), not this patch.
- Renders: sections, table, fold, code block fine; no images, so no username/home look needed.
- Summary, Deliverables, Changes match the patch; nothing claimed is missing, nothing delivered is unmentioned.
- Known gaps lists the two unverified points; no "None".
- Review box: `$CHANTIER log CR-315` has "r1 approved at 42d9718" (line 12/13), matches the box.
- Proofs name 5c36b06; no STALE mark. Role names are product terms of this change.

VERIFIED
