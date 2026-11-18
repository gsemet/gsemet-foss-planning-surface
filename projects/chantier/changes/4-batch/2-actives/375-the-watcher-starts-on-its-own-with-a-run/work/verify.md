Head: 4b111a1c7630c04066e73148bf06328cfd0ee06b

VERIFIED

Claims, all judged at 4b111a1c.

1. Watcher lock, the lines, outputs (open, take, order qa, foreman transcript, status), end line, cut, structure test.
   Command (worktree, its src on PYTHONPATH):
   `python -m pytest tests/test_watcher_autostart.py tests/test_watcher_step.py tests/test_forge_hub.py tests/test_startup_manifest.py tests/test_plugin_files.py -q`
   Output: `95 passed in 16.34s`. (Without PYTHONPATH the main checkout's older install is imported and the new tests fail to collect: not the CR's.)
2. Whole suite at head: work/check.log (just check) ends `663 passed in 34.82s`; the Driver's log: `just check: pass; just eval-dry-run: pass`; `gh pr checks 341` at 4b111a1: all pass including scenario (ubuntu-latest).
3. Startup limit unchanged: `git diff main...HEAD --stat -- startup-manifest.json test_startup_manifest.py` is empty; manifest `"limit": 12544`; the measures test passes (claim 1).
4. Cards: grep shows the Startup core line (SKILL.md:35), Entry points row (chief-of-staff.md:33), step `5. **Start the watcher.**` (868), The watcher (1241-1249), direct-mode step (1689), seat hand-over, session-start.md:104, foreman.md:774, both host rows. No `--batch` watch command left in chief-of-staff.md (grep empty).
5. Docs: diff of AGENTS.md (both places), CONTRIBUTING.md, hub/__init__.py names `chantier/watch-<project>/<session>.lock`.
6. PR description (posted body equals work/pr-body.md, one blank-line difference): sections render, Summary/Deliverables/Changes match the diff (27 files incl. autostart.py, lines.py, lock.py, watch.py, cards, scenario); no images; Known gaps names the untested no-CR open case and the scenario/Windows long gate; Review box `4e0de99` carried: driver note "r1 approved at 4e0de99c" and the rebase note "patch unchanged" at 4b111a1c. No role-name misuse found. Unchecked Verified/CI boxes are expected before this pass.
Not run by me: full `just scenario` (CI green at head cited above); Windows local gate is the Driver's.
