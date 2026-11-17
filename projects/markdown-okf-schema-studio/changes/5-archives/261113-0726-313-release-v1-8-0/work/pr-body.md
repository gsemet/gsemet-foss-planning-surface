## Summary

Version 1.8.0 of Markdown OKF-Schema Studio. It ships the changes merged since 1.7.1: save with
Cmd+S (Ctrl+S) from the preview, GitHub alerts that keep their title when they start with a
heading, a sticky heading band that keeps each level on one line, an HTML export that keeps an
edit in progress, and a click fix for cards of a grid inside a quote.

## Deliverables

The release folder the owner reviews, committed with the version:

| File | Content |
| --- | --- |
| `docs/releases-notes/2026-11-13-v1.8.0/release-notes.md` | The GitHub release notes (rendered below) |
| `docs/releases-notes/2026-11-13-v1.8.0/tweet.md` | The three-post announcement thread (rendered below); posted by the owner only |
| `docs/releases-notes/2026-11-13-v1.8.0/sticky-heading-one-line.png` | The picture of the notes and of post 1 |

## Changes

- `chore: version 1.8.0` from `just bump-version`: `package.json`, `package-lock.json`, the two
  plugin manifests and the GitHub Copilot catalog entry move from 1.7.1 to 1.8.0.
- `CHANGELOG.md`: the `## Unreleased` lines move under `## 1.8.0 - 2026-11-13`; nothing added.
- The release folder above.

## Impacts

No visual change in this commit: it only changes version numbers, the changelog heading and the
release folder. The merge publishes 1.8.0 (tag, GitHub release with these notes, Marketplace,
Pages) through the version push on `main`.

## Blast radius

Grade: 3

A release: once merged, CI tags v1.8.0 and publishes to the Marketplace. The extension code is the
one already on `main`; a bad release is fixed forward with a patch release.

## Test plan

- [x] New or changed tests (they fail on the previous code): no code change in this PR
- [x] Requirements: No behaviour change
- [x] Changelog: the version commit moves the `## Unreleased` lines under `## 1.8.0`; every `feat`
      and `fix` commit since v1.7.1 has its line
- [x] Local gates: `just release-notes-check` ok; `just preflight`: `ci-static` and `ci-visual`
      passed, the local real-window `ci-integration` failed on one step (`tall-block-scroll`) of
      this machine's VS Code window, so `ci-report` and `ci-gallery` did not pass; the heavy run
      below is the real-window proof
- [ ] Review: the owner reviews the release notes and the thread
- [x] CI green at this head, and the heavy run dispatched on this branch green at its exact head
      (`integration` success, `stress` success; run 43377939225)

## Autonomous decisions

- The picture is an existing capture of the sticky band from the visual suite, cropped to a
  landscape frame, not a dedicated hero scenario: the guideline accepts an existing capture for a
  small release. A dedicated hero image (a real document with the sticky band or an alert) can
  replace it on request.
- "Export keeps your edit in progress" goes in "Smoother editing" and the grid-in-quote click fix
  in "All fixes"; the three headline changes have their own sections.

## Internal references

- Release change request: CR-313 release-v1-8-0 (batch-02).

---

# 📰 Release notes (rendered)

<h1 align="center">Markdown OKF-Schema Studio 1.8.0</h1>

<p align="center">
  <b>Save from the preview, keep a GitHub alert's title, read a long heading on one line.</b><br>
  <sub>12 changes since 1.7.1 · VS Code 1.95 or later · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from the Marketplace</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.8.0/CHANGELOG.md">Full changelog</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.0.0">1.0 showcase</a>
</p>

---

## 💾 Save from the preview with <kbd>Cmd</kbd>+<kbd>S</kbd>

<kbd>Cmd</kbd>+<kbd>S</kbd> (<kbd>Ctrl</kbd>+<kbd>S</kbd> on Windows and Linux) now saves the
document while the focus is in the preview, with no detour through the source editor. It works
even while you are editing a block, a table cell or a frontmatter field: the text typed so far is
written first, the text box stays open with its caret, and a frontmatter field closes.

You can keep your hands where you are working and save as often as you like.

## 📣 GitHub alerts keep their title

A GitHub alert whose first line is a heading or a bold line now keeps its title ("Note", or the
text after the marker) and shows that heading or bold line in its body, as GitHub does:

```markdown
> [!NOTE]
> ## Before you migrate
> Back up the database first.
```

MyST admonitions and Quarto callouts still take their title from a leading heading or bold line.

The preview now shows the same alert as GitHub, so what you read is what your readers get.

## 📌 A long heading stays on one line in the sticky band

The sticky band at the top of the preview shows each heading level on one line, cut with an
ellipsis when it is too long. It no longer grows at a high zoom, and no longer covers the first
line of the section below.

![The sticky band of a page zoomed in: the long title of the document on one line, cut with an ellipsis, above the same title in full and the first section](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/39d4a51e41ce92366dec3ea9fcb45097612664a3/docs/releases-notes/2026-11-13-v1.8.0/sticky-heading-one-line.png)

The band tells you where you are without hiding what you are reading.

## 🛠 Smoother editing

- **Export keeps your edit in progress**: Export to HTML keeps the content of a table cell or a
  front matter field that is being edited, as last saved; the editor stays open and is not in the
  file.

<details><summary><b>🐞 All fixes</b></summary>

- A click on a card of a grid written inside a quote, whose content starts with a blank quoted
  line, opens the editor on the card instead of the line above.

</details>

<details><summary><b>🛠 For contributors</b></summary>

- `ci-integration` stops at once on a locked screen and names the cause and both ways out;
  `just preflight` says why the report and gallery stages did not run.
- The e2e report names each failed visual check (`<page>: <detail>`) instead of printing
  `[object Object]`.
- Each pull request with a `feat` or `fix` commit now adds its own line to the changelog.

</details>

---

# 🐦 Announcement thread (rendered)

# Announcement thread for 1.8.0

## 1/

I review what my coding agent writes in the Studio preview, and I fix things right there: a
sentence in a block, a cell in a table. Then I had to click back into the source just to save.
Now Cmd+S saves from the preview, even with the text box still open. Two smaller things came
with it: a GitHub alert that starts with a heading keeps its title, as on GitHub, and a long
heading in the sticky band stays on one line.

Image: ![sticky-heading-one-line.png](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/39d4a51e41ce92366dec3ea9fcb45097612664a3/docs/releases-notes/2026-11-13-v1.8.0/sticky-heading-one-line.png)

## 2/

The details are in the release notes:
https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.8.0

## 3/

Install or update it from the Marketplace, it is free and MIT:
https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
