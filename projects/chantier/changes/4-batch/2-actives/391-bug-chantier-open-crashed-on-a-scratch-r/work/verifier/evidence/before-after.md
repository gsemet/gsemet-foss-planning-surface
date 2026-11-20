# Before / after, CR-391

Before: base b76d037e (detached worktree). After: head dc671de7be64a718d75c76422ca7cea932e51c7a.
Paths below are made up (`/scratch/surf`).

## Pair 1: new tests (before-tests.log, after-tests.log)
Reproduce: copy tests/test_open_no_clone.py and tests/test_cli_units.py of the head into the base, run
`pytest skills/chantier/scripts/cli/tests/test_open_no_clone.py skills/chantier/scripts/cli/tests/test_cli_units.py`.
- before: 4 failed, 29 passed, 1 skipped (3 open cases and the git() unit case fail; the preflight P8 test passes: P8 text unchanged)
- after: 33 passed, 1 skipped

## Pair 2: manual, `open --factory` on an external scratch surface with no clone
Reproduce: git init a surface with projects/demo/{checkout.yml,project.md,changes/}; run
`chantier --project <surf>/projects/demo open --factory --default-branch main`.
- before (base):
  NotADirectoryError: [WinError 267] (traceback ends here), exit 1
- after (head):
  error: no clone of the project at /scratch/surf/projects/demo/.repo (remote https://example.com/demo.git): clone it there
  exit 2
- after, clone created (git init at projects/demo/.repo, origin remote, origin/HEAD):
  opened batch-01 on claude: no CR, paused, 4 slots, parallel, steering foreman, factory   (exit 0)
Note: both before and after leave only changes/.gitignore (written by the batch lock before open_settings; unchanged behaviour); no batch.json, no record.
