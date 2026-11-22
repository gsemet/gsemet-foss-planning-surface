# Diagnosis: serve_and_webui (CR-456)

Cause: scenario/run_scenario.py `serve_and_webui` (l.2699-2703) builds `sw` and `sw2` (SurfaceWorld.build)
but never runs `sw.chantier("init")`, so `projects/demo/changes` does not exist. Every other
surface-board case that starts a server calls init first (e.g. outside_poller l.2769).
`serve` then refuses: "error: board not started: no planning folder at <surface>/projects/demo/changes"
(board/command.py check_planning). Consequences:
- `first` BoardProc prints no start line (error on stderr) -> `Link(None).ok` False -> the case prints
  "default port 8765 is held" (wrong guess) and skips the second-surface step.
- `webui` finds no server, spawns `<cli> serve --stop-idle` detached (stdout/stderr devnull); it dies on
  the same error; webui waits 20 s -> exit 4 "did not start within 20 s" (commands/webui.py:46-47).
- Then the later steps fail; the final 10049 OSError is a follow-on of the empty link.

Proof: fresh scratch surface without `changes/`: `uv run --no-sync --project <wt> chantier --project demo serve --port 0 --seat s`
-> "board not started: no planning folder at ...\changes". With the folder present, the exact spawned
command (`uvx --from <wt> chantier --skill ... --project ... serve --stop-idle`) starts in about 1 s and takes a
free port when 8765 is held (checked with CHANTIER_WRITER_TEST_TIMES set and a live-pid writer entry).
Locally 8765 is also held by the user's real boards (netstat: pids 5276, 19868), a second, separate issue.

Fix: in serve_and_webui, after the `build()` loop add `each.chantier("init")` for sw and sw2 (SurfaceWorld.chantier
runs writer_up first, as outside_poller does).
Second risk: `first` uses `--port DEFAULT_PORT` explicitly, so no election happens (command.py `_listen`: default only
when args.port is None); if 8765 is held (a real board here, or a parallel unit on CI), it refuses and the second-surface
step is skipped (handled, not failing). Optional: leave as is.
