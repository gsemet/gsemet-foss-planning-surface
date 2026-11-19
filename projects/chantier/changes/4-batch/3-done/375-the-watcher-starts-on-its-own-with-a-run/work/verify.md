Head: fe2c215e81c641c9449155b5b2e5c7c26f0b48ab

NOT VERIFIED

Second verification. Previous: 4b111a1c (VERIFIED). Move 4b111a1..fe2c215: a restack onto CR-370's
branch b2ae16d3. `git range-diff 4b111a1...fe2c215` shows the CR's one commit changed (hunks in
chief-of-staff.md, foreman.md, batch_status.py, orders.py, run_scenario.py follow the base); the base
brought 7ee43d0d..b2ae16d3 changes to batch_status.py, orders.py, the cards, scenario (git diff
--name-only). So claims 1, 2, 4, 6 are judged again; 3 and 5 carried.

Claims.

1. Watcher lock, lines, outputs, cut, structure, now with the empty-batch and factory tests of the
   new base. Judged at fe2c215e. Command (cli folder, PYTHONPATH=src):
   `python -m pytest tests/test_watcher_autostart.py tests/test_watcher_step.py tests/test_forge_hub.py tests/test_startup_manifest.py tests/test_plugin_files.py tests/test_open_empty_batch.py tests/test_factory.py -q`
   Output: `122 passed in 25.16s`.
2. CI at fe2c215e: `gh pr checks 341`: just check (macos, ubuntu, windows) pass; just eval-dry-run
   (ubuntu) pass; just scenario (ubuntu-latest) pass (2m40s). The Driver's log (note 23:59:36)
   says the same. Judged at fe2c215e. Local `just scenario` on Windows and `chantier gate`: not run
   by me; the ship event says no long gate passed at fe2c215 (Driver's).
3. Startup limit unchanged. carried from 4b111a1: the move did not touch startup-manifest.json or
   the test; `git diff main...HEAD --stat -- skills/chantier/scripts/cli/tests/test_startup_manifest.py startup-manifest.json`
   at fe2c215e is empty, and test_startup_manifest.py passes in claim 1.
4. Cards: `grep -n "watch" chief-of-staff.md | grep "\-\-batch"` at fe2c215e: empty. The range-diff
   shows only the Entry points row context and the foreman.md context changed (CR-370's rows);
   the CR's own lines are intact; test_plugin_files and the manifest test pass (claim 1).
5. Docs (AGENTS.md, CONTRIBUTING.md, hub/__init__.py). carried from 4b111a1: no range-diff hunk
   in them.
6. Known gap "open with no CR prints no line" now testable; I tried it, a real flow on a scratch
   git repo (removed after), CLAUDE_CODE_SESSION_ID=s-probe, `chantier open --remote origin --default-branch master`:
   output `opened batch-01 on claude: no CR, paused, 4 slots, parallel, steering foreman, factory`
   then `next: complete the brief ...`; no `watch:` line. `chantier status` then: `batch-01 paused ...
   no CR yet`, `no CR yet: ...`, `last closed: none`; no `watch:` line. So the case is as the spec
   says (paused batch, no line), but no test in the suite asserts it
   (test_some_outputs_print_no_line covers take, order add, status of a paused batch with CRs only).
   Judged at fe2c215e, by hand probe only.
7. PR description (gh pr view 341 --json body, at fe2c215e): FAILS. Sections render, no images, the
   Summary and Deliverables match the diff, but: (a) Test plan lines name `4b111a1` for local gates,
   Review, Verified and CI, a SHA not in fe2c215's history and not a clean carry (the patch changed,
   ship refused the carry); (b) Known gaps still says the empty-batch change "is not below this
   one", which is false at this base (f0f8d4b7 and b2ae16d3 are below), and the one-line gap
   should say instead that no test asserts the no-line open (claim 6). Driver: fix the SHAs
   to fe2c215 (or the evidence of this pass), reword that gap, then a description-only pass.
Review box: the note "r1 approved at 4e0de99c" exists; at fe2c215 the Review box must cite a note
of a pass at that head or carry with a reason; none is logged yet for the restack beyond the Driver's
"judged" note (23:59:12).

Not run by me: full `just scenario` (CI green at head cited above); Windows local gate (Driver's).

## Description-only pass at fe2c215e81c641c9449155b5b2e5c7c26f0b48ab (code claims carried from the run above)

Command: `gh pr view 341 --json body,headRefOid`; `chantier log CR-375`; `gh pr view 341 --json statusCheckRollup`.
- SHAs: headRefOid = fe2c215e81c641c9449155b5b2e5c7c26f0b48ab. Test plan: local gates at `4b111a1` (log: "before first PR at 4b111a1: just check: pass; just eval-dry-run: pass") with CI at fe2c215 (check x3, scenario, eval-dry-run all SUCCESS); Verified and CI at fe2c215. Pass.
- Review box: "approved at 4e0de99, carried to fe2c215"; log has "r1 body re-inspection approved at 4e0de99c" and "move b2ae16d-restack: 4b111a1..fe2c215 judged: clean rebase, no conflict, hunks follow CR-370's changes". Pass.
- Known gaps: the empty-batch gap now says it holds by hand at fe2c215 and has no test (matches claim 6 above); the scenario-units gap stands. Pass.
- Renders, no images, no username, no role name misuse. Pass.

VERIFIED
