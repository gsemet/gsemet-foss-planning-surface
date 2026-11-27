# CR-504: scratch validation in new mode (round 4)

`new-mode-validation.md` (round 3) is superseded: its method checked no marker. okfreq 0.18.1 scans the markers in the directory that contains the bundle (`project_path` in `okfreq/core.py` returns `root.parent`; `--project-root` only serves `--check-links`). A copy of `requirements/` alone under `out/scratch504new/` therefore has no source and no test next to it: its "0 errors" proved nothing about fragments or benches, and W004 (95) was every live StRS.

Command (round 4): `sh work/scratch/newmode-full.sh <worktree> [head]`. It copies the whole repository (the tracked files of the working tree, or the committed HEAD with `head`) to the git-ignored `out/newmode504/`, sets `strs_test_coverage_mode: linked-swrs-and-acceptance-paths` in the copy only, then runs `okfreq validate out/newmode504/requirements --check-links --project-root out/newmode504 --json` and `okfreq trace` on the same copy to show that markers were found. The committed `config.yml` is unchanged. The copy is removed after the run.

| Tree | errors | W004 | W2 | scenario_markers found |
| --- | --- | --- | --- | --- |
| HEAD 77a8d074 | 0 | 38 | 26 | 3724 |
| working tree of round 4 | 0 | 38 | 26 | 3735 |

Logs: `work/gates/r4-newmode-full-head.log`, `work/gates/r4-newmode-full.log`.
