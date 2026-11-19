# Verify CR-381 (first verification)

Head: 22519166ff4d3c1ac13b156d1ce455c2de193cbb

All claims judged at 2251916 (pushed head, PR 346), base e33fb594. Raw logs in work/verifier/*.log.

1. `just docs` (sphinx-build -W --keep-going) at 2251916: exit 0, "build succeeded.", no warning line (the only
   "warning" substring is MyST's config echo). Log: work/verifier/docs.log. Built pages (21): index, installation,
   tutorials/{index,claude-code}, how-to/{index,agents-and-models,gates,release-process,use-cases,use-cases-direct,
   use-cases-foreman}, explanation/{index,batches-and-lifecycle,costs,planning-modes},
   reference/{index,boards,hosts,planning-folder,web-board,what-you-say}. All 13 old pages are present (none dropped).
2. Screenshots, from docs/_build/html with headless Chrome, in work/verifier/evidence/: home.png,
   tutorials-claude-code.png, how-to-gates.png, explanation-batches.png, reference-boards.png,
   web-board-on-a-phone.png. Each opened: furo, sidebar with the four sections, diagrams show; the phone section
   shows all 12 phone screenshots (the 8 new ones among them). Paths on screen are made up (/home/demo/...), no
   username. web-board-on-a-phone.png is of a scratch copy of the build whose CSS hides the page's other sections
   (a full-page capture was too tall); content and images are the built ones.
3. Link and image tests: `uv run --no-sync pytest tests/test_plugin_files.py tests/test_docs_site.py -k "links_resolve or docs_image"`
   -> "2 passed". Probe in a `git archive HEAD` copy under work/scratch (removed after): README line 54 URL
   renamed to planning-modezz.html -> AssertionError "README.md: https://chantier.readthedocs.io/en/latest/explanation/planning-modezz.html ... exists() False";
   docs/explanation/planning-modes.md image renamed to ../planning-modez.svg -> AssertionError "images no site page shows: ['planning-modes.svg']".
   The worktree itself was never edited (git status clean).
4. Startup bytes: `pytest -s tests/test_startup_manifest.py` at 2251916 and at base e33fb594 (detached worktree, removed):
   38 startup-bytes lines each; `diff startup-before.log startup-after.log` -> IDENTICAL. Max reload 12544
   (chief-of-staff, copilot) = STARTUP_LIMIT 12_544, none above. Files: work/verifier/startup-{before,after}.log.
5. Empty uv cache (UV_CACHE_DIR = new folder under work/scratch, outside the repo, removed after): `just tools` exit 0
   (tail: "ruff 0.17.5", "Version: 2.6.7"), then `just check` exit 0, ending "build succeeded." Logs: tools.log, check.log.
   Also `just test` earlier: 648 passed.
6. RTD recipe, tmp venv: `uv venv --python 3.13` (CPython 3.13.18), empty UV_CACHE_DIR,
   `UV_PROJECT_ENVIRONMENT=<venv> uv sync --locked --no-install-project --group docs`, then
   `python -m sphinx -T -W --keep-going -b html docs <tmp>/html` -> exit 0, "build succeeded." (rtd.log).
   Not proved: the `asdf install uv` steps (Linux-only, RTD image), RTD's own build.
7. PR description (`gh pr view 346 --json body`, work/verifier/pr-body-live.md) against `git diff --stat e33fb594 HEAD`:
   Summary, Deliverables, Changes match the 38 changed files (docs moves, conf.py, .readthedocs.yaml, pyproject/uv.lock,
   justfile, tests, path updates); renders (sections, fold). No images attached. Known gaps names the Factory mode
   absence, no RTD build, untested asdf lines. Items for the Driver at ship: replace `<sha7>` and tick the Test plan;
   the Known-gaps bullets "no screenshots yet of the built site / empty-cache run" are now done (this file), the README-on-GitHub
   screenshot remains not captured; README is 165 lines, sections short, all images kept (grep of README at head).
   Review box: not checked here (unchecked in the description).
8. Not provable here: `chantier rules` at the new paths (the CLI reads the main checkout; `$CHANTIER rules` run from
   here lists the old docs/use-cases-direct.md and docs/release-process.md). Instead at 2251916 CONTRIBUTING.md:30 links
   docs/how-to/use-cases-direct.md and :380 docs/how-to/release-process.md (grep), and `git grep` finds no old flat
   docs path left outside release notes and an old eval result. README rendered on GitHub and RTD's build: not available.
   Long gate: CI `just scenario (ubuntu)` green at this head per the brief (not re-run).

VERIFIED

## Description pass

Head: 22519166ff4d3c1ac13b156d1ce455c2de193cbb

Judged at 2251916 on `gh pr view 346 --json body` alone, against pr-template "The audit".
- Sections in order (Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps), one Details fold holding Changes, Human decisions, Impacts, Test plan, Internal references, nothing after it. Pass.
- Internal references: CR-381 appears only under Internal references; no role name as doer elsewhere. Pass.
- Images: the 3 attachments downloaded and opened; each is the built site at 2251916 (home, gates page, web board "On a phone"). No username (gaeta) and no home folder on screen; the only local path is the made-up /home/demo/planning-surface. Pass.
- Test plan: every proof names 2251916; Review box matches the Driver note "r1 approved at e33fb594, committed as 22519166" (`chantier log`). Pass.
- Known gaps: the UNVERIFIED claim (README on GitHub, first RTD build) has its bullets (no README screenshot, no RTD build); asdf lines and Factory mode gap also listed. Pass.

VERIFIED

## Second verification

Head: 105ad6680f5a867b2c58204ead5bdd65be93373f

Move 2251916..105ad66: restack onto the new base 0129b911 (CR-380) plus round-2 commit 105ad66. Raw logs: work/verifier/*2.log, startup2-*.log.

1. Docs build at 105ad66: `just docs` exit 0, "build succeeded.", 0 WARNING lines (docs2.log).
2. `just check` at 105ad66 (worktree clean): exit 0, ends "build succeeded." (check2.log).
3. Links: `git grep`/grep of docs/how-to/use-cases*.md: three Factory mode links, all https://github.com/gsemet/chantier#factory-mode; README.md:65 has `## Factory mode`. `pytest skills/chantier/scripts/cli/tests/test_docs_site.py test_plugin_files.py` -> 47 passed (the link test now lives in test_docs_site.py, `test_docs_site.py` + plugin files pass).
4. Startup sizes vs the new base 0129b911 (detached worktree, removed): `pytest -s test_startup_manifest.py` 30 passed; the 38 startup-bytes lines are IDENTICAL base vs head (diff), max reload within the limit (test passes).
5. Rebase: `git range-diff 5aca8256~1 5aca8256 5aca8256` shows the docs commit unchanged by itself; the base content changed under it (agents/cards/hooks path updates in the diff vs the old base), judged by 1-4.
6. Carried from 2251916: screenshots, empty-cache `just tools`, RTD recipe venv build, rules/CONTRIBUTING paths: the move touched no docs layout, conf.py or RTD config beyond the link edits.
7. PR description (`gh pr view 346`, head oid 105ad66) is STALE: its Test plan, evidence and Review lines name 2251916 (lines 74-78), and its Known gaps (line 43) still says the README "Factory mode" section and the use-cases link to it are "not carried over", which is false at 105ad66 (README:65 has the section, links added). Fails the description rule: NOT VERIFIED until the Driver updates the description to 105ad66 and drops/changes that gap.

NOT VERIFIED

## Description pass at 105ad66 (re-check)

Head: 105ad6680f5a867b2c58204ead5bdd65be93373f

8. PR description re-read (`gh pr view 346 --repo gsemet/chantier --json body,headRefOid`, oid 105ad6680f5a867b2c58204ead5bdd65be93373f):
   SHAs are 105ad66 or "carried from 2251916"; the Factory mode gap is gone (the section and its links exist:
   `grep -rn "factory-mode" docs` shows use-cases*.md link to https://github.com/gsemet/chantier#factory-mode);
   Summary, Deliverables and Changes match the diff (`git diff --stat 0129b911 HEAD`: docs/ moves, conf.py,
   .readthedocs.yaml, pyproject/uv.lock, justfile, cards, CONTRIBUTING, evals/README, release_notes.py, tests under
   skills/chantier/scripts/cli/tests/{docs_site,test_docs_site,test_plugin_files}.py; all named files exist).
   Known gaps cover the UNVERIFIED claim and the untested asdf lines. No STALE mark. No role name outside Internal references.
9. Images: all three URLs return 200 image/png (curl); opened each: home page (4 sections in Furo sidebar), gates
   page, web board "On a phone" section; each shows its claim; paths on screen are made up, no username or home folder.
10. Review box: `chantier log 381`: "r2 approved at 5aca825, committed as 105ad66" matches "approved at 105ad66".
11. CI: `gh pr checks 346`: check x3, eval-dry-run, scenario (ubuntu) pass. The "Verified at" box is left unchecked as instructed.

VERIFIED
