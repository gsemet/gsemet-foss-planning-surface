## Summary

Version 1.12.1 of Markdown OKF-Schema Studio. This pull request tops the stack that it releases (the raw-text opening fix below it); it carries the version commit, the changelog heading with the pull request of each line, and the release notes and announcement thread in `docs/releases-notes/2026-11-24-v1.12.1/`. The owner merges the whole stack with it, bottom up, by rebase.

## Deliverables

Release notes and announcement thread, rendered below. No images: a patch release, as 1.9.3.

## Changes

- `chore: version 1.12.1`: `package.json`, `package-lock.json`, the plugin manifests and the Copilot catalog.
- `CHANGELOG.md`: the `## 1.12.1 - 2026-11-24` heading; each line ends with its commit (when it is on `main`), pull request and issue.
- `docs/releases-notes/2026-11-24-v1.12.1/`: `release-notes.md` and `tweet.md`.

## Impacts

The merge starts the version push: heavy jobs, tag `v1.12.1`, GitHub release, Marketplace and Open VSX publications. The version is 1.12.1 although the stack carries a `feat` (the blank-line block per line, already on `main`), which Commitizen would number 1.13.0; the version is the owner's choice.

## Blast radius

Grade: **2**: the release publishes; a revert before the tag is a plain `git revert`, after it a new fix release.

## Test plan

- [x] New or changed tests (they fail on the previous code): none, release commit only
- [x] Requirements: No behaviour change
- [x] Changelog: the lines of the release moved under the 1.12.1 heading
- [x] Local gates: `just preflight` (static stage, passed)
- [ ] Review
- [x] CI green, and the heavy run (`integration` and `stress`) green on this head (run 45341630587)

---

# 📰 Release notes (rendered)

<h1 align="center">Markdown OKF-Schema Studio 1.12</h1>

<p align="center">
  <b>A Markdown file opens as text again, the blank-lines editor closes, each blank line is its own block.</b><br>
  <sub>21 changes since 1.12.0 · VS Code 1.95 or later · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from VS Code Marketplace</a> ·
  <a href="https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio">Install from Open VSX</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.12.1/CHANGELOG.md">Full changelog</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.0.0">1.0 showcase</a>
</p>

---

## 📄 A Markdown file opens as text again

Open With... > Text Editor stays a text editor, and a search result opens the text editor at the line again, as it did before 1.11.0. Studio no longer watches the files you open, so the settings `open.searchResultsInStudio` and `open.markdownFilesInStudio` are gone.

To open every Markdown file in Studio, associate `*.md` with Studio in `workbench.editorAssociations`. Where `open.markdownFilesInStudio` was on, the first activation sets that association for you. With it, a click in the Explorer opens Studio, and a jump to a line opens Studio at the top, without a marker in the side preview. Opening Studio at the line comes back in a later version.

## ⬜ One block for each blank line

Each extra blank line in edit mode now shows as its own blank-line block. Typing in one writes your text in place of that one blank line and keeps the others.

## 🛠 Smoother editing

- **Done closes the blank-lines editor.** It no longer stays on "Saving Markdown…".
- **Cancel and Escape always close a saving editor.** When a save fails, your text comes back in an editor you can save again.
- **Open Preview to Side and Refresh Preview finish again.** They complete once the page shows the document, as in 1.12.0, and so does a restored panel.

<details>
<summary><b>🔎 Details</b></summary>

- The side preview marks no line while a Markdown file is associated with Studio and you jump to a line: the jump opens Studio at the top.
- A search result or a jump with the default settings opens the text editor at the line.

</details>

<details>
<summary><b>🛠 For contributors</b></summary>

- The tests of Open Preview wait for the shown render before they read the preview counters, and the opening of a file is proven in a real window.
- The visual checks of the empty document and of six lines expect the blank-line block.
- Release pull requests can no longer carry merge commits, and each changelog line ends with its commit, pull request and issue.

</details>

---

# 🐦 Announcement thread (draft for the owner to post)

# Announcement thread for 1.12.1

## 1/

1.11 started opening every Markdown file in Studio, even when I picked Open With... > Text Editor, and a search result no longer landed on its line in the text editor. 1.12.1 takes that back: a Markdown file opens as text again, and you associate `*.md` with Studio yourself if you want every file in the page. It also closes the blank-lines editor after Done and gives each extra blank line its own block.

## 2/

The details are in the release notes:
https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.12.1

## 3/

Install or update it from the Marketplace, or from Open VSX for VSCodium and Cursor; it is free and MIT:
https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio
https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
