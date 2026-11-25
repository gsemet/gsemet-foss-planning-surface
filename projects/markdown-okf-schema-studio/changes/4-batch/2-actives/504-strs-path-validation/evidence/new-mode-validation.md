# CR-504: scratch validation in new mode

Command (run in the CR work folder `work/scratch`, round 3, after the fragment review and `just requirements-update`): `sh newmode.sh <worktree>`. It copies `requirements/` to `out/scratch504new/requirements` (ignored by git), sets `strs_test_coverage_mode: linked-swrs-and-acceptance-paths` there only, and runs `okfreq validate ... --check-links --project-root . --json`. The committed `config.yml` is unchanged (the mode switch is a later CR).

Summary line: `{'errors': 0, 'warnings': 121, 'infos': 0}` with warnings by code `{'W004': 95, 'W2': 26}`.

- 0 errors: every fragment names a declared scenario or path, every StRS marker is on the right bench.
- W004 (95): a StRS with no `@accepts_req` that counts ("has no acceptance test"); the new mode asks for one per StRS, walking each main path as `@accepts_req StRS-...#S<n>`. These StRS keep their SwRS tests and are the work of a following CR (the acceptance benches); `uncovered-scenarios.md` lists the paths with no marker.
- W2 (26): broken cross-links in the text of SwRS (`url`, `<url>` placeholders); they existed before this CR.
