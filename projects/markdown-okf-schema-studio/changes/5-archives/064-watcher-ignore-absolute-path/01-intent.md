# A workspace below a folder named out, tmp, dist… never refreshes on file changes

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P2.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS LIFE-045.

- The ignore list (tmp, out, output, public, dist) is matched against every segment of the absolute
  path, so a workspace stored under such a folder never refreshes on included-file, image or
  sibling-file changes.
- Expected: match the path relative to the watched root; unit test with a root under /…/out/.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
