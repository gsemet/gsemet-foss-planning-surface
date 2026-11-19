# Verify CR-386

Head: e0f6e1fcde315394cfa54dd03dc470cf6a714965

Claims, all judged at e0f6e1f.

1. Spec sections 1-4 and the Evidence tests list (e0f6e1f). Command:
   `uv run --no-sync python -m pytest test_board_running.py test_forge_hub.py test_surface_server.py test_scenario_coverage.py test_watch_events.py test_event_audience.py test_watcher_autostart.py test_board_journal.py` (in skills/chantier/scripts/cli/tests)
   Output: `125 passed in 21.34s`. Covered: migration cases (migrate-live-older, migrate-key-only, same/other-version/silent/dead),
   `--new-key` keeps entries and a refused write gives `board not started: <path>: ... write lock`
   (test_board_running.py:182), forge-hub lock election with no server / live server / yield / re-elect
   (test_one_watcher_holds_the_hub_lock...[no-server|live-server]), hub entry write retried at next cycle,
   two writers of server.json lose neither entry, the server's hub thread elects/cycles/releases,
   status line in three forms (`none running`, `the surface server`, `a watcher`; test_forge_hub.py:253-258).
2. Section 5 text (e0f6e1f): `grep` shows AGENTS.md names `chantier/server.json` + `server.json.lock`, "Two named" exceptions
   with the surface server, "two named git exceptions"; docs/web-board.md:176 names server.json; session-start.md diff adds the
   forge-read ask and "a watcher started while the board runs is not the hub". chief-of-staff.md / foreman.md unchanged (kept true).
3. Out of scope kept (e0f6e1f): `git diff --name-only HEAD~1 -- agents com.github.copilot hooks types .../board/web` prints nothing.
4. Remaining `board.json`/`hub.json` mentions in src are only the migration code of hub/state.py.
5. CI at e0f6e1f: `gh pr checks 354`: check macos/ubuntu/windows pass, eval-dry-run pass, `just scenario (ubuntu-latest)` pass
   (covers the surface-board scenario steps 1-7). Coder also ran surface-board on Windows (262/262) - not re-run by me.
6. PR description (e0f6e1f): renders, Summary/Deliverables/Changes match the diff, no images, Known gaps names the missing real run.

UNVERIFIED: the Windows real run on the user's machine (spec "Real run", 4 steps). Also not done by me: a live `chantier board`
+ `status` run in scratch (a foreground-only rule leaves no way to run the server and status together); the scenario covers it in CI.

VERIFIED

## Description pass (e0f6e1fcde315394cfa54dd03dc470cf6a714965)

Command: `gh pr view 354 --json body`, read against `git diff --stat HEAD~1 HEAD` (base = CR-385 branch, 27 files) and `02-answers.md`.
Output: sections in order, fold with blank lines and nothing after `</details>`, no images, no internal reference outside Internal references, no role name.
Deliverables names (`server.json`, status line forms) match hub/state.py and hub/lines.py diff; budget 300 to 500 s matches run_scenario.py diff.
Human decisions match answers 1, 3/16, 4/11, 12, 13. Test plan SHAs e0f6e1f; review box matches log note "r2 approved at f9fb169, committed as e0f6e1f";
`gh pr checks 354`: five jobs pass. Known gaps covers the unverified real run and the Linux/macOS note.

VERIFIED
