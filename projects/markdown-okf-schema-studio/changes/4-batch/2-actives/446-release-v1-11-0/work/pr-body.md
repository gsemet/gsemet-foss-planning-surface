## Summary

Release 1.11.0: the version commit (bump, changelog heading, release notes folder with its three cropped pictures). It is a minor release because the stack under it ships features: the Delete block button, the blank-lines block, and Studio opening at a searched line. It is based on the top branch of the stack, so it stays a draft until the stack merges.

## Deliverables

The release notes and the announcement thread are rendered below, from the files in `docs/releases-notes/2026-11-21-v1.11.0/`. The three pictures are cropped from the captures of the merged changes to the place where each change happens. Nothing is tagged or published by this PR: the owner merges it, and the tag, the GitHub release and the Marketplace publication follow only on the owner's word.

## Changes

- `chore: version 1.11.0`: `package.json`, `package-lock.json`, `plugin.json`, `.claude-plugin/plugin.json`, `.github/plugin/marketplace.json`.
- `CHANGELOG.md`: the `## Unreleased` lines moved under `## 1.11.0 - 2026-11-21`.
- `docs/releases-notes/2026-11-21-v1.11.0/`: `release-notes.md`, `tweet.md` and the pictures.

## Impacts

No visual change in the extension by itself. It publishes the changes of the stack below it.

## Blast radius

Grade: 3

Release: the merge starts the tag and the publication. Nothing is published before the owner's word; rollback after the tag is a new patch version.

## Test plan

- [x] New or changed tests: none, a version commit
- [x] Requirements: No behaviour change
- [x] Changelog: the lines of the stack moved under 1.11.0
- [x] Local gates: `just release-notes-check` ok; `just preflight` (static stage on Windows) run through the project's gate
- [ ] Review
- [ ] CI green: the heavy run (`integration`, `stress`) is dispatched on this branch

---

# 📰 Release notes (rendered)

<h1 align="center">Markdown OKF-Schema Studio 1.11</h1>

<p align="center">
  <b>Edit CRLF files without getting stuck, delete blocks, open Studio at the line you searched.</b><br>
  <sub>21 changes since 1.10.0 · VS Code 1.95 or later · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from VS Code Marketplace</a> ·
  <a href="https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio">Install from Open VSX</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.11.0/CHANGELOG.md">Full changelog</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.0.0">1.0 showcase</a>
</p>

---

## 💾 Edit a file with CR LF line endings

The block editor of a file with CR LF line endings no longer stays stuck on "Saving Markdown..." when you leave it without a change. A block you edit keeps the line endings of its file.

## 🗑️ Delete a block

![A block in edit mode with its bar below it: insert, move up, move down and a delete button](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/81f62b6fec41c79eea133094bd6fc0196f3c6a95/docs/releases-notes/2026-11-21-v1.11.0/delete-block-button.png)

Each block's bar has a Delete block button (x), and <kbd>Delete</kbd> or <kbd>Backspace</kbd> on a selected block deletes it. Emptying a block and pressing Done removes the block instead of leaving blank lines.

## ⬜ Reach and remove blank lines

![A run of three blank lines shown as a dashed blank-lines block between two paragraphs](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/81f62b6fec41c79eea133094bd6fc0196f3c6a95/docs/releases-notes/2026-11-21-v1.11.0/blank-lines-block.png)

In edit mode, two or more blank lines between blocks, at the start or at the end of a document show as a blank-lines block. Reach it with the arrow keys, click or press <kbd>Enter</kbd> on it to write a block in its place, or remove it with <kbd>Delete</kbd>.

## 🔎 Open Studio at the line you searched

![A code block with a blue arrow in the margin at line 15](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/81f62b6fec41c79eea133094bd6fc0196f3c6a95/docs/releases-notes/2026-11-21-v1.11.0/line-marker-arrow.png)

A search result, a Quick Open `file.md:40` or a link to a line opens Studio at that line, with an arrow in the margin. The setting `markdownOkfSchemaStudio.open.searchResultsInStudio` is on by default; the new setting `markdownOkfSchemaStudio.open.markdownFilesInStudio` opens every Markdown file in Studio, and **Open as Text** reads the raw text of one file.

## 🛠 Smoother editing

- **A new block starts clean.** It no longer keeps its leading blank lines, and one inserted after a list gets one blank line before it.
- **The line arrow stays clear of list handles** in edit mode.
- **Requirement pages on the website** draw each use case as one joined map, smaller and readable, and show table scenarios instead of empty columns.

<details><summary><b>🔎 Details</b></summary>

- The setting `markdownOkfSchemaStudio.open.markdownFilesInStudio` replaces the `workbench.editorAssociations` entry for Markdown files; an existing entry is migrated.
- Removing a blank-lines block keeps one blank line.
- On the requirement map, states shared by several paths are drawn once, each path keeps its colour, and Play walks the path in its colour.

</details>

<details><summary><b>🛠 For contributors</b></summary>

- Test fixtures with CR LF line endings stay CR LF, and the save tests cover CR LF, LF and mixed files.
- The use case map tests run in their own CI job.
- Release notes highlights start with text; their pictures are cropped on the change.
- Requirement pages get one share card per feature category.

</details>

---

# 🐦 Announcement thread (rendered, a draft the owner posts themselves)

# Announcement thread for 1.11.0

## 1/

I opened a Markdown file written on Windows in the Studio editor, left a block without changing anything, and the page stayed on "Saving Markdown..." for good. In 1.11 that is fixed and your file keeps its own line endings. You can also delete a block with one button, reach and remove blank lines between blocks, and open Studio right at the line a search result points to.

Image: ![line-marker-arrow.png](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/81f62b6fec41c79eea133094bd6fc0196f3c6a95/docs/releases-notes/2026-11-21-v1.11.0/line-marker-arrow.png)

## 2/

The details are in the release notes:
https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.11.0

## 3/

Install or update it from the Marketplace, or from Open VSX for VSCodium and Cursor; it is free and MIT:
https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio
https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
