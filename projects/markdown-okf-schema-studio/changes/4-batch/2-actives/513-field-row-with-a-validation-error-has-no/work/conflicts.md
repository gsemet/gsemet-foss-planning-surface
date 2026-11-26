# CR-513, rebase onto the moved base (copied from the resolver's reply)

- Old head 79aa5698d9a74ac4053f28737d0603e1b2084274 (on 8df99ce), new head
  1a48862d4da583420fe57aa1db4d01bea95416f3 (on 89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4).
- One CR commit, message unchanged.

## Conflicted hunks

1. requirements/tiers/log.md, section 2026-11-26: the base's two CR-504 entries and the CR-513
   entry collided. All three kept unchanged, CR-513 first (newest first).
2. SwRS-MDOKFSTUDIO-FMSCHEMA-023.md, generated tested_in_files: base side taken, then
   regenerated (adds fieldIssueStyles.test.ts and frontmatterIssueRowScenarios.ts; the base had
   moved a marker off previewEditing.test.ts).
3. SwRS-MDOKFSTUDIO-FMSCHEMA-084.md, generated tested_in_files: same.

Auto-merged and checked: test/visual/scenarioAssertions.ts, scenarioDefinitions1.ts;
e2eGroups.test.ts count 527 passes; fixtures 98, 99 and ids v32 to v35 free on 89cae5f.

## Gates at the new head

- just dev: completed (okf-schema 0.17.0 to 0.18.1)
- just requirements-update: pass (2 files updated; W002, W2 warnings only)
- uv run --no-sync --group requirements okfreq validate --check-links --project-root .: pass
  (1228 requirements, 0 errors, 26 warnings)
- just preflight: pass, ci-static passed; unit 5339 tests, 5331 pass, 0 fail, 8 skipped.

Not run: visual captures on the new base; any app-window test.
