# Verify CR-476

Head: 8f0f54d8e14f98861cbb1ebe8c6c8dfb2fb05a72

Gate: `work/gates/20261124-142244.log`, first line `gate CR-476 branch chantier/batch-31/cr-476-watcher-runs-through-several-events-inst head 8f0f54d8e14f98861cbb1ebe8c6c8dfb2fb05a72`, last `result: pass at 8f0f54d8e14f98861cbb1ebe8c6c8dfb2fb05a72`.

Each claim judged at 8f0f54d8.

1. Tests (stream, idle rows, autostart host forms, hub paused-batch, waits): `uv run --no-sync python -m pytest tests/test_watch_stream.py tests/test_watch_events.py tests/test_watcher_autostart.py tests/test_forge_hub.py tests/test_forge_hub_waits.py -q` in the worktree's cli folder -> `127 passed in 35.31s`.
2. `--stream` refused with `--once`: `python -m chantier --project <surface> watch --stream --once --after 0` -> `error: watch: --stream and --once do not go together`, exit 1 (EXIT_USAGE = 1 in core/errors.py).
3. Watch.poll/tell/_idle: read in `git diff origin/main...HEAD -- hub/watch.py`: STREAM_TOLD block then `told_at` reset, idle counted from max(start, woke_at, flight_at), batch read every SEAT_CHECK_S via `batch_prs.followed_batch`, SEAT/END unchanged.
4. Host form: `watch_command` appends ` --stream` for `claude` only; test `test_the_watcher_command_streams_on_claude_code_only` passes (claim 1); scenario transcript shows `watch --after 12 --stream` in the not-running line.
5. `followed_batch` (running, or paused with `to_read`) replaces `running_batch` in batch_prs, waits, lines; `grep -rn running_batch skills scenario tests docs AGENTS.md` shows only the unrelated `lifecycle/running_batch` module.
6. Scenario step 16d at this head (gate log's run, `scenario/results/scenario-20261124-144800-29504.md` lines 28995-29012): stream watcher first and second block with `still watching`, still alive; paused with PR open runs past idle end; hub's third block; seat take ends it with the seat line; all `[x]`.
7. AGENTS.md, hosts cards, copilot card, session-start card, concepts, docs/web-board.md, defaults comment: diffs read against the spec's section 3-5 text; match (hub sentence, watcher sentence, interests sentence, rows 39/55/56, copilot "no --stream here", web-board lines 228 and 238).
8. CI at 8f0f54d: `gh pr checks 453` -> all five jobs pass (check macos/ubuntu/windows, eval-dry-run, scenario).
9. PR body: `gh pr view 453` body equals pr-body.md (trailing blank line only); Summary/Deliverables match the diff; Known gaps lists the unproved Monitor start, no Copilot stream, `just test` duration; no internal ids beyond the Internal references section; no images. Review box `approved at a94085d, committed as 8f0f54d` matches the Driver's notes in `chantier log CR-476` (13:10:31Z). Unchecked boxes (evidence, verified, CI) are for this pass and CI; evidence is in verifier/evidence/before-after.md.
10. Evidence: verifier/evidence/before-after.md (before = a94085d, after = head).

Not run by me: `just check` / `just eval-dry-run` (cited from the Driver's notes at 8f0f54d, and CI green); the unproved real-session Monitor trial is a stated Known gap.

VERIFIED
