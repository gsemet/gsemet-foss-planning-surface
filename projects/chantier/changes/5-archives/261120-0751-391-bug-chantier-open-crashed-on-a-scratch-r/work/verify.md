# Verify CR-391

Head: dc671de7be64a718d75c76422ca7cea932e51c7a

Judged at dc671de7 (base b76d037e = origin/main).

1. New tests fail on base, pass at head. Command (base, new test files copied in): `uv run --no-sync --project <base> pytest .../test_open_no_clone.py .../test_cli_units.py -q`
   output: `4 failed, 29 passed, 1 skipped` (before-tests.log). At head, same command: `33 passed, 1 skipped` (after-tests.log), incl. the 3 open cases (no-cr, factory, factory-configured-cell), test_preflight_names_the_missing_clone and test_git_in_a_missing_folder_is_a_refusal_naming_it. The cases assert exit EXIT_PRECONDITION, message with path, no Traceback, no batch.json, folder unchanged.
2. Manual, scratch external surface, no clone, `chantier --project <surf>/projects/demo open --factory --default-branch main`:
   head: `error: no clone of the project at .../projects/demo/.repo (remote https://example.com/demo.git): clone it there`, exit 2, no traceback; base: NotADirectoryError traceback, exit 1. See evidence/before-after.md.
   Planning folder after refusal: `find projects/demo/changes` -> only `.gitignore`, identical on base (written earlier by the batch lock; not this CR's).
3. With clone created (git init, origin remote, origin/HEAD), same command at head: `opened batch-01 on claude: no CR, paused, 4 slots, parallel, steering foreman, factory`, exit 0; batch.json and 5-archives/batches/batch-01.json exist.
4. P8 message unchanged: test_preflight_names_the_missing_clone passes on base (old code) and at head; the diff moves the text verbatim into Repo.missing_clone().
5. Matrix: default `.repo` cell proven by manual run and by the no-cr and factory tests; configured `repo: gone` cell by factory-configured-cell test (expected path = project/gone). Configured cell not run by hand (test only).
6. CI at dc671de7: `gh pr checks 360`: macos, ubuntu, windows `just check`, `just eval-dry-run`, `just scenario (ubuntu-latest)` all pass.
7. PR description (gh pr view 360): renders, sections match the diff (6 files: repo.py, opening_record.py, preflight.py, git.py, 2 test files); Known gaps None is consistent (no UNVERIFIED claim, all pairs captured). Review box `approved at dc671de (carried from 6cd45c2)`: `log` shows "r1 approved at 4fdf6fc9, committed as 6cd45c2b" and "rebase ... clean, patch unchanged, pushed dc671de". No images. Test-plan Evidence/Verified boxes are pending, to be ticked by the Driver.
8. Scope: no card, scenario, Repo.find or _external change in `git diff origin/main --stat`.

VERIFIED

Description pass at dc671de7be64a718d75c76422ca7cea932e51c7a: `gh pr view 360` body (headRefOid dc671de7) renders (sections, one Details fold with blank lines, nothing after it), Summary/Deliverables/Changes match `git diff main...HEAD` (6 files; Repo.missing_clone, open_settings EXIT_PRECONDITION refusal, git() ChantierError on missing cwd, tests), Known gaps None consistent, no images, no role names or internal refs outside Internal references, Test plan boxes name dc671de (carried from 6cd45c2 backed by the log note "r1 approved at 4fdf6fc9, committed as 6cd45c2b" and the clean-rebase note), CI claim per item 6. VERIFIED
