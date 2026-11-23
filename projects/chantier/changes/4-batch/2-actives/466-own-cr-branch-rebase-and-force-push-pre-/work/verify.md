Head: e17cd34ba18773aa1f73c0be0b74d33d093e7c9a

VERIFIED

Claims, each judged at e17cd34b:

1. `just check` (lint, tests, release-notes) passes: `2288 passed, 20 skipped in 115.18s`,
   `release-notes: ... ok`. Includes the new `test_rebase_rules.py` and `test_driver_prompt.py`.
2. `just eval-dry-run` at e17cd34b: `dry run: 19 of 19 cases as expected`, exit 0.
3. Code (`git diff origin/main...HEAD`): 13 rebase samples in `allow_samples.py`, shared
   `project_remote` and ` origin/` fill in `permissions.py`, `Rewrites:` line between `writes:` and
   `Steering:` in `driver_prompt.py` (none for `none`), scenario step and README updated.
4. Cards: `foreman.md` "A Driver's refused rebase", `chief-of-staff.md` "A refused rebase",
   `driver.md` "Means: a rebase the host refuses", `concepts.md` `Rewrites:` column and rule 8,
   `routing.md`, `hosts/claude-code.md` rows and the 2026-11-23 mark (grep at the head).
5. Spec deviations (the `--exec` ban not in driver.md; preflight asserts in test_rebase_rules.py) are
   named in the description's Known gaps. The long gate is waived by the user (O-20).
6. PR 443 description (read with `gh pr view 443` at headRefOid e17cd34b): Test plan cites e17cd34,
   matches the diff, Known gaps current, no stale claim, no images.
