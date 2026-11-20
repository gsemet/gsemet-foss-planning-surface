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

---

# 📰 Release notes (rendered)

<h1 align="center">Markdown OKF-Schema Studio 1.10</h1>

<p align="center">
  <b>Drag a list item into place, edit one item at a time, list items in the outline.</b><br>
  <sub>30 changes since 1.9.3 · VS Code 1.95 or later · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from VS Code Marketplace</a> ·
  <a href="https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio">Install from Open VSX</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.10.0/CHANGELOG.md">Full changelog</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.0.0">1.0 showcase</a>
</p>

---

## ↕️ Drag a list item to move it

![A bullet list in edit mode with a handle left of each item; one item is held down, dimmed, and a line shows where it will drop](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/b59ef32699f2b19de3949dbdf4718b888dfcd995/docs/releases-notes/2026-11-20-v1.10.0/list-item-handles-drag.png)

In edit mode, each list item has a handle on its left, as table rows do. Drag it, or focus it and
press <kbd>Alt</kbd>+<kbd>Up</kbd> or <kbd>Alt</kbd>+<kbd>Down</kbd>: the item moves with its
sub-items in one edit.

## ✏️ Edit one list item, not the whole list

![Left, a click on a list item opens the whole list in the editor; right, the same click opens only that item](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/b59ef32699f2b19de3949dbdf4718b888dfcd995/docs/releases-notes/2026-11-20-v1.10.0/edit-one-list-item.png)

A click on the list itself, outside its items, still edits the whole list.

## 🧭 List items in the table of contents

![The table of contents with the items of a top-level list shown under the heading before them](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/b59ef32699f2b19de3949dbdf4718b888dfcd995/docs/releases-notes/2026-11-20-v1.10.0/list-items-in-toc.png)

Turn on the setting `markdownOkfSchemaStudio.preview.listItemsInToc` (off by default) in the VS Code
settings to list the items of top-level lists in the table of contents, by their first line. A
document that writes each requirement as a list item gets a usable outline.

<details><summary><b>🐞 All fixes</b></summary>

- When a render fails without a message, the preview shows "The render failed." (or "The latest
  render failed." over the kept page) instead of "undefined" or an empty message.

</details>

<details><summary><b>🔎 Details</b></summary>

- From the keyboard, <kbd>Enter</kbd> on an item, or on a block inside an item, reached with
  <kbd>Right</kbd> as before, edits that item or that block only.
- An ordered list keeps its numbers in order when an item moves.
- The lists of alerts and admonitions get their handles left of the box.
- The table of contents leaves out the items of a `[TOC]` list, of the footnotes and of tables.

</details>

<details><summary><b>🛠 For contributors</b></summary>

- The requirements of rendering, diagrams, trust, MyST, code blocks and GitHub Markdown are traced
  to their code and tests, with a use case diagram each; the requirements lint fails on a diagram
  that does not parse.
- Every heavy CI dispatch builds the gallery and the site.
- The table breakout width tests run on Linux in the visual job, with one bundled font.
- Three real-window tests and a build queue test no longer fail at random.
- The release notes are short and demo-first; the release guideline says how.

</details>

---

# 🐦 Announcement thread (rendered)

_A draft: the owner posts it; no agent posts it._

# Announcement thread for 1.10.0

## 1/

My coding agent writes plans as long lists, and reviewing one in the Studio preview meant opening
the whole list to fix a single step, then cutting and pasting lines to put the steps in order. In
1.10 a click on a list item edits that item only, and each item has a handle: drag it, or press
Alt+Up or Alt+Down, and it moves with its sub-items. There is also a setting to list the items in
the table of contents, for documents that write one requirement per item.

Image: ![list-item-handles-drag.png](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/b59ef32699f2b19de3949dbdf4718b888dfcd995/docs/releases-notes/2026-11-20-v1.10.0/list-item-handles-drag.png)

## 2/

The details are in the release notes:
https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.10.0

## 3/

Install or update it from the Marketplace, or from Open VSX for VSCodium and Cursor; it is free and
MIT:
https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio
https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
