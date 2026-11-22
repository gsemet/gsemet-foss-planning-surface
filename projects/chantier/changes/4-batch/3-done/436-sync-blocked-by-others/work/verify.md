# Verify CR-436

Head: c5af034bb5865f60832835e464cbb89b33b22666

All claims judged at c5af034 (the CR-436 commit only; base CR-428 commits not judged).

1. Tests at c5af034: `PYTHONPATH=<worktree>/skills/chantier/scripts/cli/src uv run --no-sync --project <main> pytest test_launch_modes.py test_allow_rules.py test_plugin_files.py -q`
   -> `51 passed in 16.70s`. (Without PYTHONPATH the main checkout's code is imported and collection fails; that is the environment, not the CR.)
   test_launch_modes.py covers the matrix cells: manifests claude/copilot/other-name/broken, surface chantier/studio, none, each with and without `.git`, for cli_command and sync_command.
2. Probe at c5af034 (a `.git` plugin root, cli_command/sync_command):
   - chantier Repo (manifest): `uv run --no-sync --project "<root>" chantier` | `uv sync --locked --project "<root>"`
   - other Repo: `uvx --from "<root>" chantier --skill "<root>/skills/chantier"` | `None`
3. The "`$CHANTIER` is the CLI, one launch in two modes" paragraph, md5 of the 4 SKILL.md lines: all `24e59376b8adaa7239ed53c19978ace8`; it holds the second condition, "another project, even with the plugin loaded from chantier's checkout", and the path sentence.
4. Q12 sentence ("run that build and serve every project of the surface") count 1 in each of AGENTS.md, CONTRIBUTING.md, session-start.md; phrase "when the session's project is chantier" present in AGENTS.md, CONTRIBUTING.md, session-start.md, concepts.md, hosts/claude-code.md (6).
5. permissions.py: `grep is_dev_checkout` returns nothing; `_dev_mode(repo)` is the single mode test.
6. Gate: work/gates/20261121-213952.log first line `gate CR-436 ... head c5af034bb5865f60832835e464cbb89b33b22666`, last line `result: pass at c5af034bb5865f60832835e464cbb89b33b22666`.
7. PR 405 description: head c5af034 matches; sections render; Summary/Deliverables/Changes match the diff (20 files); Known gaps names the card-behaviour, Q12 and scenario gaps. Test plan boxes still hold `<sha7>` placeholders (the Driver fills them at hand-back; noted, not a failure of the change). No images.

Not run by me: just check / just eval-dry-run (Driver's gates), CI.

VERIFIED

## Description pass at c5af034bb5865f60832835e464cbb89b33b22666

Posted PR 405 body (gh pr view 405) read against `git show c5af034`: table, helper, Changes, Known gaps match the diff; placeholders now filled with c5af034; review box "approved at c5af034 (carried from 14160a6)" proved by log note "r1 approved at 14160a65..., committed as c5af034b". No images.

VERIFIED

## Move c5af034 -> 9bff328 (clean restack)

Head: 9bff328e1999e223638b0b26fc12b9190325b8cb

- Tests at 9bff328: `PYTHONPATH=src uv run --no-sync --project <main> pytest tests/test_launch_modes.py tests/test_allow_rules.py tests/test_plugin_files.py -q` -> `51 passed in 10.23s`.
- Base changes since touch only board files (crs.py, times.py, web client js, docs/web-board.md, board tests) per `git diff --name-only origin/main HEAD~1`; none touch launch.py, permissions.py, plugin_files.py or the cards this CR changes. Claims 2-5 carried from c5af034: patch unchanged (same patch-id), base brought no change to what they run.
- CI at 9bff328 (`gh pr checks 405`): check ubuntu pass; macos, windows, eval-dry-run, scenario pending.
- Description pass: pr-body.md lines 61-65 still name c5af034 (see report); Known gaps has no stacked-base/draft line.

VERIFIED
