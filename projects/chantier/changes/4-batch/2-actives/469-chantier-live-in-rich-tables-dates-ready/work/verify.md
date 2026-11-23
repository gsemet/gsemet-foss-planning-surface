# Verify CR-469

Head: 56385daa44e5b66e3b29758eee66998fd21035bb

Verdict: VERIFIED (Evidence 12, the Windows Terminal hand check, is UNVERIFIED and is a Known gap in the PR description).

Claims, each judged at 56385daa (the pushed head):

1. Evidence 1-9 (since, zone, Agents, Ready, screen plain, interactive OSC 8 and SGR colours, keys, tokens.css colours, `--once` deadline) and 10 (real server `--once`, both transports):
   `uv run --no-sync python -m pytest tests/test_live_model.py tests/test_live_ready.py tests/test_live_link.py -q -x` (in `skills/chantier/scripts/cli`) -> `105 passed in 36.99s`.
   Test names read: `test_since_rounds_down...`, `test_every_time_is_drawn_in_the_local_zone...`, `test_agents_lists...`, `test_wanted_names_the_batch...`, `test_ready_draws_each_state_word...`, `test_ready_follows_the_merge_order...`, `test_the_interactive_screen_links_the_pr...`, `test_the_state_colours_are_the_boards`, `test_once_prints_with_the_prs_not_read...`; keys cases `["t"]`, `["t","t"]`, `["/","t","enter"]`, `["?","t"]` and the footer `? keys  / filter  t time  q quit` are in `test_live_model.py` lines 132-136; `test_live_link.py` lines 166-167 assert the Agents and Ready titles and the `\d{2}-\d{2} \d{2}:\d{2}:\d{2}` time.
2. Scope: `git diff --name-only origin/main...HEAD` lists no `pyproject.toml`, `uv.lock`, web client or server file; only `clients/tui/*`, `commands/live.py`, tests, `docs/boards.md`, `docs/server-api.md`, `scenario/*`. The `docs/server-api.md` paragraph names the `prs` watch and the `merged@1` line as the spec's section 7 says.
3. Gates: `gh pr checks 445` -> `just check` ubuntu, macos, windows pass; `just eval-dry-run` pass; `just scenario (ubuntu-latest)` pass, run at head 56385daa (PR headRefOid equals it).
4. PR description: `gh pr view 445 --json body` equals `pr-body.md` (only a trailing newline differs). It renders (sections, fold, a text capture, no image), the Summary, Deliverables and Changes match the diff (the new `times.py`, `ready.py`, `parts.py`, `live_world.py`, `test_live_ready.py` are mentioned), no username or home path in the capture (`/work/demo`). Known gaps lists the one UNVERIFIED claim (no hand check in Windows Terminal), the prepared-events capture and the cut Ready title. Test plan boxes pending are not claims at the head.
5. Evidence 12 (Windows Terminal: boxes, colours, `t`, click on a PR number): UNVERIFIED, an agent cannot do it; recorded in Known gaps.
6. The long gate `scenario` was not run locally (port 8765 held by the user's board, never stopped); the CI `scenario` pass at this head is cited above.

## Description pass (posted body, at 56385daa)

NOT VERIFIED: `gh pr view 445 --json body` Changes lists docs/boards.md, docs/server-api.md, scenario/README.md but not scenario/run_scenario.py (`git diff origin/main...HEAD --stat` shows it changed: live_once now expects the Tasks State word first). A delivered change is unmentioned. Everything else checked out: Review note "r2 approved at e833bc8e, committed as 56385daa" in `chantier log`, CI all five checks SUCCESS at 56385daa, Known gaps match.

## Description pass at 56385daa44e5b66e3b29758eee66998fd21035bb

Command: gh pr view 445 --repo gsemet/chantier --json body; git diff --stat origin/main...HEAD (15 files); chantier log CR-469.
- Renders: sections, fold, one text capture, no images, no username or home path (made-up /work/demo). Pass.
- Consistent: Changes lists model/times, screen/parts/ready, view, commands/live, docs, scenario/README and scenario/run_scenario.py, which match the diff; tests are named in Autonomous decisions and Test plan. Pass.
- Known gaps holds the one UNVERIFIED (Windows Terminal hand check) and the skipped local long gate. Pass.
- Review box: log has "r2 approved at e833bc8e..., committed as 56385daa" matching 56385da. Pass.
- Verdict for the description: VERIFIED
