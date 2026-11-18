Head: 4fa7952f0a714746afa52304272f990a3a212462

All claims judged at 4fa7952f.

1. Tests pass: `pytest tests/test_cli_stop.py tests/test_startup_manifest.py tests/test_plugin_files.py -s -q` -> `67 passed`.
2. Budget (reload bytes, from -s): router claude 12496 / copilot 12502; chief-of-staff claude 12538 / copilot 12544; griller 12219 / 12225; status 12314 / 12320. All <= 12544, matching the PR table. Limit is 12544 in startup-manifest.json, test_startup_manifest.py, test_plugin_files.py (grep).
3. startup-core.md (git diff) holds: both modes and any call, exact error and stop, no seat, nothing written in planning folder, no upgrade/reinstall/repair/relaunch/other source, one retry on transient network error only, cannot-run scope with refusal/error exit/permission denial kept, CLI never a tool a role works without, steering tells user / started agent ends turn with plain-text error.
4. The 4 SKILL.md hold "Any failure of the sync or of `$CHANTIER`, in either mode, at any call, follows `startup-core.md`" (diff + test).
5. Exclusion clause present in concepts.md (lines 453, 645), chief-of-staff.md (53, 182), driver.md (95) and the 8 worker cards; `grep -rniE "not a stop|without it|part without"` finds no other uncovered missing skill/tool line (remaining hits are "without its/it" unrelated).
6. Tests fail on base: test_cli_stop.py copied into a detached worktree of origin/main -> `16 failed`. Worktree removed.
7. PR body matches diff (files, figures, trims, 16 cases); CI `gh pr checks 328`: check x3, eval-dry-run, scenario (ubuntu-latest) all pass.
8. Known gap in the body (fragment "The plugin root (...)") is disclosed. Test plan boxes are the Driver's to tick.

VERIFIED
