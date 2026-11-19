# Retro: release 1.9.2

- Cost: the heavy run of `main` HEAD needed a re-run of `integration` (about 25 minutes).
  Root cause: `stepSchemaOrderAndBadge` in `test/integration/previewEditing.test.ts` counts the
  highlighted cell, then reads it again, while `pageInput.ts` removes the highlight after 1.5 s;
  a slow runner reads it after it is gone. Process fix: file a test fix that reads the field in the
  same evaluation as the count (not done in this release).
- Cost: the version was first proposed as having no `feat` since 1.9.1; one `feat` (requirements
  site only) existed. Fix: always run the `git log ... | grep -E '(feat|fix)'` check of CONTRIBUTING
  step 2 before proposing a version to the owner.
