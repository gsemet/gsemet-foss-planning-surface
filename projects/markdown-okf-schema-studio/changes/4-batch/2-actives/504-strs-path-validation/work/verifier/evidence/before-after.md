# CR-504: requirements viewer, before and after

- Before: base `4a47151e8d055b7f096b69b1fca2d9bf9636f863` (base requirements report from okf-schema
  0.17.0, base viewer sources).
- After: pushed head `afbb55c527217ec66537dff308bbcfb5d05b25c8` (head report and trace from the
  worktree, head viewer sources).
- Capture: `verifier/buildsite.cjs` builds each site, `verifier/shots.cjs` takes the screenshots
  (Playwright Chromium, 1280 px, light theme). Both sites were built in the scratch folder from
  `git archive` copies and transpiled viewer sources, not in a detached base worktree.

| State | Before | After |
| --- | --- | --- |
| Home figures and area table | before-home-figures.png | after-home-figures.png |
| Use case page, paths (LIFE-023) | before-life023.png (top of the page: no path rows) | after-life023.png |
| Use case page, one path (CODE-004) | before-code004.png | after-code004.png |
| Behaviour page, scenarios (CORE-082) | before-swrs.png | after-swrs.png |
| Behaviour page, scenario without a test (PALETTE-001) | none: the base viewer marks no scenario | after-swrs-missing.png |

Observation (cosmetic, head): the "Tested by" block of a scenario card has no horizontal padding;
its label and file rows touch the card border (after-swrs.png, after-swrs-missing.png).
