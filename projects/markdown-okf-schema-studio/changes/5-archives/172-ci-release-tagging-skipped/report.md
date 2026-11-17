# 172 — CI: release tagging skipped since the heavy split — report

Landed 2026-10-28. PR https://github.com/gsemet/markdown-okf-schema-studio/pull/186 (auto-merge by
the user). Normal CI green; heavy not needed (no heavy job changed).

- `tag-release`: `!cancelled() && needs.checks.result == 'success' && push && main`.
- `release`, `pages`: `!cancelled() && needs.tag-release.result == 'success' && tag != ''`.
- `gallery` unchanged (only runs with `inputs.heavy`, so its ancestors ran).
- `test/build/test_workflows.py`: +4 cases (4 failed on the old ci.yml, 18 pass on the fix).
- `scripts/version.py` `tag_release()` is a no-op when the tag already exists (hand v1.0.0 safe).
- New SwRS-MDOKFSTUDIO-CORE-076 (proposed). `okfreq update-coverage` added one generated
  `derived_by` line to the LOCKED StRS-MDOKFSTUDIO-CORE-001 (needed for `just check`; reported to
  the Chief of Staff).
- Inspector (opus) APPROVE; optional nits for a follow-up: `!cancelled()` jobs treated as never
  skippable in the test helper; `"inputs.heavy" in condition` is a substring test; PyYAML not a
  direct dependency of the test.
- Note: release.yml and pages.yml also trigger on `push: tags: v*.*.*`.
