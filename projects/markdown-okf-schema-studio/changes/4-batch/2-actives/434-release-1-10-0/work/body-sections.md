## Summary

Release 1.10.0 of Markdown OKF-Schema Studio. In edit mode you can now edit one list item at a time
and move a list item with a handle, and a new setting lists the items of top-level lists in the
table of contents. It is a minor version: two `feat` commits and a new setting since 1.9.3.

## Deliverables

The release folder `docs/releases-notes/2026-11-20-v1.10.0/`, reviewed here and published as it is
by CI after the merge:

| File | Content |
| --- | --- |
| `release-notes.md` | The GitHub release notes (rendered below) |
| `tweet.md` | The announcement thread, three posts, for the owner to post (rendered below) |
| `list-item-handles-drag.png` | First highlight and post 1: a list item held by its handle, the drop line under the target |
| `edit-one-list-item.png` | Second highlight: before (whole list in the editor) and after (only the clicked item), joined side by side with Pillow from the dark 460 px captures of the item editing change |
| `list-items-in-toc.png` | Third highlight: the table of contents with the setting on |

## Changes

- `package.json`, `package-lock.json`, `plugin.json`, `.claude-plugin/plugin.json` and
  `.github/plugin/marketplace.json` at 1.10.0 (`just bump-version`; Commitizen picked the minor
  bump from the `feat` commits).
- `CHANGELOG.md`: the `## Unreleased` lines move under `## 1.10.0 - 2026-11-20`.
- The release folder above.

## Impacts

The merge publishes 1.10.0: CI tags the version commit once its heavy jobs are green, then the
Release VSIX run publishes to the VS Code Marketplace, the GitHub release and Open VSX. The
pictures are in the notes below.

## Blast radius

Grade: 3. A release reaches every user through both registries. A bad release is rolled back by
publishing a fix version; the tag and the published versions are not taken back.

## Test plan

- [x] New or changed tests: none, a version change
- [x] Requirements: No behaviour change
- [x] Changelog: the `## Unreleased` lines moved under the version heading; every `feat` and `fix`
      commit since `v1.9.3` has its line (the two fixes repair the unreleased item editing and
      share its line)
- [ ] Local gates: `just release-notes-check` ok; `just preflight` (Windows: static stage)
- [x] Heavy run of `main` HEAD `049b543` green before the version commit (run 44764608171:
      integration, stress, checks, visual, static, static-windows)
- [ ] Review
- [ ] CI green

## Autonomous decisions

- The notes have no "Smoother editing" section: every changelog line is in a highlight or in a
  folded section, so it would be empty.
- No dedicated hero image: the drag capture serves the first highlight and post 1.
- The version commit has no `Signed-off-by` trailer, as the release guideline says; `CONTRIBUTING.md`
  "How to Release" step 3 still shows `git commit --amend --no-edit -s`.
