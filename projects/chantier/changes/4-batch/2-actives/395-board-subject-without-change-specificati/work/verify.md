Head: fb41759dd7b54c5e242bd2af9aa5a9c87f56085a

Claims, all judged at fb41759 (CR patch = git diff ce7a7ef3..HEAD, 14 files).

1. Title tests pass at fb41759.
   `PYTHONPATH=<worktree>/skills/chantier/scripts/cli/src python -m pytest tests/test_titles.py tests/test_board_prs_batches.py -q`
   -> `36 passed in 3.81s`. (Without PYTHONPATH the project venv imports the main checkout and fails; not the CR's.)

2. `just lint` at fb41759: ruff format/check, mypy (258 files), uv lock --check, biome (148 files) all pass.

3. Root fix: a request whose spec heading is "# Change Specification: Fix it" joins a batch with the plain title.
   Scratch project, `chantier open --default-branch master 3-ready/1-fix` ->
   `CR-101 Fix it: 3-ready/1-fix -> 4-batch/1-pending/101-fix`; batch.json, STATUS.json, events.jsonl hold `"title": "Fix it"`.

4. Old record shown plain by the board server. Edited the scratch batch.json title to "Change Specification: Fix it",
   ran `chantier board --host 127.0.0.1 --port 0`, `GET /api/projects/proj/state` -> `"title":"Fix it"`.
   (`/prs` rows were empty: no PR in the scratch record, so the PRs rows' server strip is covered by the test file, claim 1.)

5. Page JavaScript `title()` (format.js), executed with node 24 (uvx nodejs-wheel):
   "Change Specification: Fix it" -> "Fix it"; "change specification : Fix it" -> "Fix it";
   "# Change Specification: Fix it" -> "Fix it"; BOM + "# ..." -> "Fix it"; "Intent: Fix it" -> "Fix it";
   "Fix the Change Specification: lead" -> unchanged; null -> "".
   Call sites (prs-row, home-prs, batch-pr-card, overview) read in the diff: each wraps the title in `title(...)`.
   Limit: no browser render of the PRs page was done (no browser tool, no PR in the scratch record); the function and call sites are proved, the pixels are not.

6. PR description (gh pr view 364 body at head fb41759): renders, equals work/pr-body.md; Summary/Deliverables/Changes match the diff
   (files.py subject, backlog import, stages.py, status/views.py, prs.py, state.py, format.js and its four views). Known gaps names both
   UNVERIFIED items (page stripping, pane screenshot). Test plan boxes are the template's unchecked ones, to be filled at hand-off. No image, no role name misuse.
   The JS-stripping gap is now partly settled by claim 5 (function proved, no browser render); the Driver may keep or narrow its bullet.

Gate: no gate run by me; CI is green at the head per the brief.

VERIFIED
