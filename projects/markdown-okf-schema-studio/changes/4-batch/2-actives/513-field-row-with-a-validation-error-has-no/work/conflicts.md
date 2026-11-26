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

# CR-513, second rebase, onto CR-505's branch (copied from the resolver's reply)

- Old head 0c9cab313d0b388ce982d1cb9d4147fc3c52d3a0 (on 89cae5ff), new head
  1fa9587eb1f6a5e53ef5bce5269d292bc2517859 (on 9d7e788a); commits 91e5b23a, 1fa9587e, messages
  unchanged, no merge commit, tree clean.

## Conflicted hunks

1. requirements/tiers/log.md, section 2026-11-26, first commit: the CR-513 entry kept first, then
   both CR-505 entries and the older ones; no line removed or reworded. The second commit applied
   cleanly with its own edit of the CR-513 entry.

Auto-merged and checked: test/visual/scenarioDefinitions2.ts keeps the base's TRUST-001 marker
change and this change's v32 to v35. The base changed none of this change's requirement files.

## Gates at the new head

- just preflight: pass (unit 5371 tests, 5363 pass, 0 fail, 8 skipped; other node runs 56/56 and
  116/116; Sphinx 4 passed; no merge commit since origin/main)
- just requirements-update: pass, no file changed
- uv run --no-sync --group requirements okfreq validate --check-links --project-root .: pass
  (1228 requirements, 0 errors, 26 warnings)
- visual:render and capture.py --group frontmatter-schema: pass (35 scenarios, 28 screenshots)
- just dev not run: uv.lock and package-lock.json unchanged between 89cae5ff and 9d7e788a

Not run: any app-window test.

# CR-513, third rebase, onto CR-511's branch (copied from the resolver's reply)

- Old head 1fa9587eb1f6a5e53ef5bce5269d292bc2517859 (on 9d7e788a), new head
  7e7022822b1a25ced9d2f7383652f4b1cff35456 (on 928ebd7e); commits 552cfac4, 7e702282, messages
  unchanged, no merge commit, tree clean.

## Conflicted hunks

1. requirements/tiers/log.md, section 2026-11-26, first commit: all entries kept unchanged, order
   CR-513, CR-511, CR-512. The second commit applied cleanly.

## Gates at the new head

- just preflight: pass (ci-static passed; static stage only on Windows)
- just requirements-update: pass, no file changed
- uv run --no-sync --group requirements okfreq validate --check-links --project-root .: pass
  (1228 requirements, 0 errors, 26 warnings)
- just dev not run: no lock file or package manifest changed
