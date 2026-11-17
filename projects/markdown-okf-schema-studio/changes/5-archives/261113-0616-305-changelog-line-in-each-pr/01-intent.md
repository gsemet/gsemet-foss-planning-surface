# Intent: release process fixes from the v1.7.1 retro

From the v1.7.1 retro, three fixes to the release process documents:

1. Each change of a batch adds its `## Unreleased` line to `CHANGELOG.md` in its own PR, as step 2
   of the release procedure asks; in 1.7.1 the lines were written late, in the version commit.
2. Step 6 names the Marketplace check of record (the gallery `vspackage` URL of the version) and
   the delay before the listing page shows the new version.
3. Step 8: an empty list of closed issues ends the step with one line in `report.md`, with no
   owner approval.
