# CR-504: requirements viewer, before and after

- Before: base `17b779d502b9633fd42dd275986067397db5c4aa` (report from okf-schema 0.17.0, base viewer
  sources).
- After: pushed head `2f3c629acdec1f49ca94aa0809506dc4e0f93325` (report and trace from okf-schema
  0.18.1, head viewer sources).
- All pairs were captured again after the restack and rounds 6 to 9 (the requirement data changed).
- How to reproduce: `git archive` each revision into an empty folder with its own `git init`; in it,
  run `okfreq generate-report requirements --output-json
  out/reports/requirements/requirements-report.json` and `okfreq trace requirements --json >
  out/reports/requirements/requirements-trace.json` with the okf-schema version of that revision;
  transpile `test/**/*.ts` and `src/**/*.ts` to `out/` with `verifier/transpile.cjs` (esbuild, CommonJS); build each site with
  `verifier/buildsite.cjs` into `site-base` and `site-head`; take the screenshots with
  `verifier/shots.cjs <folder> <evidence>` (Playwright Chromium, 1280 px, light theme). No detached
  base worktree was used.

| State | Before | After | What it shows |
| --- | --- | --- | --- |
| Home figures and area table | before-home-figures.png | after-home-figures.png | before: card "23 of 95 StRS with a stakeholder validation test", no path columns; after: 6/156 paths tested, 17/156 accepted, 1/95 StRS covered, 1911/2633 scenarios tested, two area columns |
| Use case page, paths (LIFE-023) | before-life023.png (top of the page: no path rows) | after-life023.png | four paths, none tested or accepted |
| Use case page, one path (CODE-004) | before-code004.png | after-code004.png | the path list with "Tested by" and "Accepted by", both empty |
| Behaviour page, scenarios (CORE-082) | before-swrs.png | after-swrs.png | scenario ids, test files per scenario, "missing" on S2 |
| Behaviour page, scenario without a test (PALETTE-001) | none: the base viewer marks no scenario | after-swrs-missing.png | "missing" tag and "Tested by: None." |

Checked in each image: no user name and no home folder path. The broken logo picture is the local
build, which does not copy the site images.

Observation (cosmetic, head): the "Tested by" block of a scenario card has no horizontal padding;
its label and file rows touch the card border (after-swrs.png, after-swrs-missing.png).
