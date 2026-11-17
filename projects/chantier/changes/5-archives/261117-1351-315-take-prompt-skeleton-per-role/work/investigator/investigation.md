# CR-315 investigation (round 0)

Paths are under `skills/chantier/scripts/cli/` unless marked. The tests live in `tests/` there, not in a repo-root `tests/` as the spec names.

## Files and entry points
- `src/chantier/plugin_files.py`: `skill_dir()`, `_agent_files(host)` (agent folder and files; an empty list when there is no plugin root), `worker_prompt_lines` (its regex `WORKER_FIRST_LINE` matches only `for <cr> "<title>" of batch <batch>, in the project <root>.`), `contract_lines(role, text, resolved)` (generic start gives a heading plus the body, 2-space indent; its heading says "after the opening lines"), `archive_path(repo, c)` (relative `.agents/changes/5-archives/<stamp>-<name>/`, None unless external and archive_in_pr), `cli_command(repo)`.
  - The Driver first lines are NOT one shape: cr-driver and release-driver `for <cr> "<title>" of batch <batch>`; stack-driver `for the stack of batch <batch>`; qa-driver `for <folder> of batch <batch>`. Use one regex over `Prompt starts with: \`(chantier <role> for .*)\``, then fill `<cr> <title> <folder> <batch> <root>`. All four descriptions say "Started by the steering session (...)".
  - No helper builds `Needs:`. `playbook --batch` prints `needs: <role>: skills a, b; tools c` (playbook/lines.py ~l.105); the template wants `Needs: skills <..>; tools <..>`. The new function must reformat from `resolved["roles"][role]` (`skills`, `tools`), not copy the `needs:` line.
- `src/chantier/commands/driver.py`: `take` (return at l.117: `took`, `reopened`, `facts`, `fresh`) and `_take_stack` (l.61-76, returns `head, reopened, rows`; the caller appends `fresh`). Insert the block after `facts` / after `rows`, before `fresh`. In reach: `args.note`, `d.steering` (foreman/direct), `d.playbook`, `d.host`, `c.kind`, `c.worktree`. The kind/role check must run before any mutation (`_reopen`, `b.touch`, `start_cr`, `work(...).mkdir`): `RenderedBatch` writes on exit, so look the row up before `check_take`'s mutations.
- `src/chantier/commands/facts.py`: `cr_facts` (shared with `round` and `handoff`: leave it untouched), `stack_lines(repo, batch, d)` (reuse as is for the stack block rows).
- `src/chantier/commands/orders.py`, `order()` l.169-218: the QA branch makes the inbox folder with `_qa_folder` (after `check_budget` and `check_slot`; `new_request` writes files), then `apply_order` -> `orders_apply._qa` (l.345, prints `QA folder: ...`), then `_record_order`. Return is `[order line, *effect, *fresh]`; put the block between `effect` and `fresh`, for `qa` and not `own` only. The missing-role check must run before `_qa_folder` and `_reopen`. The order id is `req.oid` (`O-{n+1}`); `<folder>` is `cr` after `_qa_folder`. `default branch:` is `repo.config["default_branch"]`; it comes from `opening_record.py` (`core/git.default_branch`) and may be None: then fall back to `git.default_branch(repo.root, repo.config["remote"])`, else a CLI error, never a silent "main".
- `scenario/run_scenario.py`: `Foreman.take` l.476 (`self.facts`, then `start_driver`); stack take ~l.4476 (`stacked[1..3]` index the rows); `order qa` run l.6138 (`out[1]` is the `QA folder:` line). Release runs are the `release*` units.
- Cards: `references/concepts.md` l.425-439 (template; l.434 writes comment, l.436 Team comment), l.441-455 prose, l.465 first-lines table, l.389-390 the ten-line exceptions list (`order qa` joins it); `foreman.md` l.169-171 (take bullet) and l.185-191 (order qa); `chief-of-staff.md` l.30 (table row), ~l.934 (Steering), l.1408-1418 (The Drivers); `driver.md` l.73-75; `hosts/claude-code.md` l.494-495. `hosts/copilot.md`: grep it for the archive-path rule before editing (not read here).

## Smallest change
1. `concepts.md`: add `### A Driver's prompt` with the table and rules after the template (spec section 1); edit the l.434 and l.436 comments; add `order qa` to the l.389 list.
2. `plugin_files.py`: `driver_prompt_lines(...)` plus a small `driver_row(...)` that parses the table from `skill_dir()/references/concepts.md`, picks the row by "Started after" (`take <cr>` with the kind in the cell, `take stack`, `order qa`) and checks the role's agent file on the host. Callers run `driver_row` first (before state changes), then build the lines. Errors: `ChantierError` with `EXIT_USAGE` (confirm it is 2 in `core/errors.py`) naming the role or kind.
3. Three call sites: `driver.take`, `driver._take_stack`, `orders.order` (qa).
4. Cards as the spec's section 4.
5. Tests and scenario checks (below). No change to `cr_facts`, agent files or `hooks/`.

## Risks and points to settle (the Driver decides; none needs the user)
- Spec inconsistency: the 2a template shows `Team: <the team: lines above, as printed, then the review steps>`, but 2d says the CR Driver's `Team:` content stays `<…>` and a CR Driver still copies the workers' lines from its own prompt. Smallest reading, matching the CLI test (it needs only a `  Team:` line): print `  Team: <the team: lines above, as printed, then the review steps>` as a placeholder.
- Stack driver `Team:` "one line holding the `team:` lines": say how they join (suggest strip each `team: ` prefix and join with `; `). With no playbook configured `team_lines` is empty: print the placeholder rather than omit the line (the test conditions its check on a configured playbook).
- Generic Driver: contract lines go after the rules line and before `CLI ($CHANTIER):`. `test_a_copilot_batch_records_a_generic_start_and_take_prints_its_contract` (tests/test_playbook_config.py l.323) makes only the coder generic and asserts that coder heading is the only "contract (a generic agent" in `took`: still true unless a Driver is made generic there.
- Archive path: `c.worktree` may hold backslashes on Windows: build with `Path(c.worktree, archive).as_posix()` and re-append the trailing `/` that `Path` drops (the test checks the path ends with the `archive:` line's path, which ends in `/`).
- Heading text must match the spec's test prefix exactly: `release-driver prompt (no writes: line `.
- CR `kind` is a free string in the code (no enum found): a hand-edited record with an unnamed kind is the real "no row" error case.
- The table in `concepts.md` is parsed by the CLI and by the structure test: same headers. `test_startup_manifest.py` slices sections by title and may budget bytes: check `startup-manifest.json` for a size on concepts' "Starting an agent" before finalising (`just test` shows it).
- Cards must hold no host tool name (`HOST_TOOLS`, tests/test_plugin_files.py l.340): keep `Steering:` means as `<…>`; never name a send tool in concepts, foreman or chief-of-staff outside a `hosts/` line. Relative links in edited cards must resolve (the links test, l.300; absolute https links are skipped).
- `order qa` output passes ten lines: edit the concepts exceptions list; grep tests for "ten lines" before.
- `order qa` is accepted in direct mode only when paused: there `Steering: the Chief of Staff`.

## Existing tests that could break
No test asserts the exact full output of `take`, `take stack` or `order qa`. Care points, all safe if the block is appended after the facts, the stack rows and the `QA folder:` line:
- `tests/test_cli_runs.py::_worker_opening_lines` (l.63): finds lines containing ` prompt, opening lines (copy them`; the Driver heading (`cr-driver prompt (copy it whole`) does not match.
- `tests/test_playbook_config.py`: `team()` filters `startswith("team:")`; the block's `  Team:` has two leading spaces and a capital: safe. l.343-348 relies on `took[at-1]` starting `  the project's rules rank above it`; the Driver line says "above them": safe.
- `tests/test_rail_refusals.py::test_order_qa_...` (l.188) reads `out[0]` and `out[1]` only; `tests/test_spend_check.py` checks codes and spend: safe (they only pay the table parse).
- Scenario: `fm.facts` is indexed from the Verifier heading (l.870-880); stack `stacked[1..3]` and QA `out[1]`: safe.
- `test_plugin_files.py` l.340 (host tools) and l.300 (links): new card text must pass them.
- `tests/conftest.py` sets `CHANTIER_PLUGIN_ROOT` to the real plugin, so the agent files exist in every existing run.

## Questions only the user can answer
None.

## Evidence plan
Kind: CLI output change plus cards text; no UI (the board pane is untouched, so no screenshot).
- Before and after: the text of `take <change CR>`, `take <release CR>`, `take stack` and `order qa --note ...`, taken once on the base (no block) and once at the head. Technique: the scenario's own runs (the `release*` units, the stack unit at ~l.4458, the QA unit at l.6125) with the new checks; save the four outputs as plain text in `evidence/take-skeletons.txt`. Scrub made-up and real paths, the username and the home folder before keeping the file (rule of the latest commit).
- Tests (all in `skills/chantier/scripts/cli/tests/`): structure test in `test_plugin_files.py` (parametrized over roles and hosts, the table once); CLI tests in `test_cli_runs.py`: change CR with and without an archive (the external-surface test at l.125 prints `archive: in the PR at`), release CR, `take stack` (reuse `open_batch` in `batch_helpers.py` with `--mode stack`), `order qa --note`, direct batch Steering, `--note` on take, and the missing-agent refusal (set `CHANTIER_PLUGIN_ROOT` and `CHANTIER_SKILL_DIR` to a tmp tree with the agents folders and `concepts.md`, remove one agent file; assert exit 2 and the record and inbox unchanged). Parametrize to stay within the `just test` budget; report its time against 18.5 s.
- Gates: `just check`; `just scenario` (CI ubuntu job at the head; `chantier gate` locally on Windows for the top CR of the batch).
- Cannot be shown: a real Driver started from the skeleton on a real host (batch-22's refusal is not reproduced); the fix rests on the printed text and on the write-guard rule in `hosts/claude-code.md`, which `hooks/` tests cover and this CR does not touch (`just mod` not needed).
