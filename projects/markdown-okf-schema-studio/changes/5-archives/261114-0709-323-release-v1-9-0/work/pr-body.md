## Summary

Version 1.9.0 of Markdown OKF-Schema Studio. It ships the changes merged since 1.8.1: the floating
toolbar laid out as four rows of four, a grid of cards that stays whole inside a GitHub alert, two
click fixes for cards of a grid in a list item, and the first publication to Open VSX next to the
VS Code Marketplace.

## Deliverables

The release folder the owner reviews, committed with the version:

| File | Content |
| --- | --- |
| `docs/releases-notes/2026-11-14-v1.9.0/release-notes.md` | The GitHub release notes (rendered below) |
| `docs/releases-notes/2026-11-14-v1.9.0/tweet.md` | The three-post announcement thread (rendered below); posted by the owner only |
| `docs/releases-notes/2026-11-14-v1.9.0/floating-toolbar-four-by-four.png` | The hero picture of the notes and of post 1 |

## Changes

- `chore: version 1.9.0` from `just bump-version`: `package.json`, `package-lock.json`, the two
  plugin manifests and the GitHub Copilot catalog entry move from 1.8.1 to 1.9.0 (Commitizen
  computed 1.9.0 itself, from the `feat` of the toolbar).
- `CHANGELOG.md`: the four `## Unreleased` lines move under `## 1.9.0 - 2026-11-14`; nothing added.
- The release folder above.

## Impacts

No visual change in this commit: it only changes version numbers, the changelog heading and the
release folder. The merge publishes 1.9.0 (tag, GitHub release with these notes, VS Code
Marketplace, Open VSX for the first time, Pages) through the version push on `main`.

## Blast radius

Grade: 3

A release: once merged, CI tags v1.9.0 and publishes to the Marketplace and Open VSX. The extension
code is the one already on `main`; a bad release is fixed forward with a patch release.

## Test plan

- [x] New or changed tests (they fail on the previous code): no code change in this PR
- [x] Requirements: No behaviour change
- [x] Changelog: the version commit moves the `## Unreleased` lines under `## 1.9.0`; every `feat`
      and `fix` commit since v1.8.1 has its line
- [x] Local gates: `just release-notes-check` ok; `just preflight`: `ci-static` passed;
      `ci-visual` failed on one scenario (`v31-mark-editor-selection-light-900`, twice), an
      intermittent failure of this machine already seen before 1.8.1 and green in CI's `visual`
      job; the local real-window `ci-integration` failed at `tall-block-scroll` (this machine's
      window), so `ci-report` and `ci-gallery` did not pass; the heavy run below is the
      real-window proof
- [ ] Review: the owner reviews the release notes and the thread
- [x] CI green at this head, and the heavy run dispatched on this branch green at its exact head
      (run 43536948441: `integration` failed once at `real-input`, then green on the re-run of
      the failed jobs; attempt 2: `integration` success, `stress` success, `visual` success)

The heavy run of `main` 1191fb6c (run 43532691444) failed once at one `integration` step (`toc`:
the click on the Edit toggle never reached the page) and was green on its re-run of the failed
jobs (attempt 2: `integration` and `stress` success).

## Autonomous decisions

- The hero is a fresh capture of the 4 x 4 toolbar from the simulated visual suite (Cream theme,
  the capture made to check the toolbar change), cropped to a 4:3 frame; not a dedicated hero
  scenario. A dedicated one can replace it on request.
- The grid-in-alert fix is a highlight with a Markdown example and no picture (no capture of it
  exists; none is invented). The two list-item click fixes go in "All fixes".
- Open VSX is named in the notes (install link, one "Also on Open VSX" line) and in post 3 before
  its first publication. If the Open VSX step fails at the release, the "Also on Open VSX" line is
  removed from the published GitHub release by an edit, and post 3 keeps only the Marketplace link.

## Internal references

- Release change request: CR-323 release-v1-9-0 (batch-04).

---

# 📰 Release notes (rendered)

<h1 align="center">Markdown OKF-Schema Studio 1.9.0</h1>

<p align="center">
  <b>Reach every button in a compact square toolbar, keep a grid whole inside an alert, land on the card you click.</b><br>
  <sub>8 changes since 1.8.1 · VS Code 1.95 or later · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from VS Code Marketplace</a> ·
  <a href="https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio">Install from Open VSX</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.9.0/CHANGELOG.md">Full changelog</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.0.0">1.0 showcase</a>
</p>

---

## 🧭 The floating toolbar is four buttons wide

The floating toolbar now lays out its sixteen buttons on four rows of four, grouped by what they
do:

- Refresh, Edit, Export and the chevron that folds the toolbar;
- Anchor, Theme, Back and Next;
- Width, Fold, Zoom out and Zoom in;
- Table of contents, Side-by-side, Diff and Comments.

It keeps the same width as before, so it covers no more of the page, and it is one row shorter.

![The Cream theme with the floating toolbar open in the top right corner: four rows of four buttons next to a heading, a wide table and a diagram](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/f12ba53b38716231e07d5181786c04f83d487b20/docs/releases-notes/2026-11-14-v1.9.0/floating-toolbar-four-by-four.png)

Each row is one kind of action, so your hand finds the button without reading the icons.

## 🧩 A grid stays whole inside a GitHub alert

A grid of cards written inside a GitHub alert now stays inside it, with all its cards, and the
text after the alert is no longer swallowed into a code block:

```markdown
> [!TIP]
> ::::{grid} 2
> :::{card} Plan
> Write the steps first.
> :::
> :::{card} Review
> Read the diff side by side.
> :::
> ::::

The next paragraph stays a paragraph.
```

No new picture for this one: the alert simply looks as you wrote it.

You can put a set of options or next steps inside a callout and trust the page to show it whole.

## 🛠 Smoother editing

- **Also on Open VSX**: the extension is now published on
  [Open VSX](https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio) too, so
  VSCodium, Cursor and the other editors that use that registry can install and update it.

<details><summary><b>🐞 All fixes</b></summary>

- A click on a card of a grid written in a list item, whose content starts with a blank line, opens
  the editor on the card instead of the line above.
- A click on a card of a grid written in a list item whose marker is followed by a tab, or whose
  cards are indented with a tab, opens the editor on the card instead of the line above.

</details>

<details><summary><b>🛠 For contributors</b></summary>

- `just dev` is the first command in a new worktree or a clean checkout; the docs say so.
- The release workflow publishes to Open VSX with trusted publishing, after the Marketplace, with
  no stored token.

</details>

---

# 🐦 Announcement thread (rendered)

# Announcement thread for 1.9.0

## 1/

I keep the Studio preview open next to my coding agent all day, and the floating toolbar had grown
to five rows that I scanned icon by icon. It is now a square of four rows of four, one kind of
action per row, one row shorter and no wider. The same release keeps a
grid of cards whole when the agent writes it inside a GitHub alert, and a click on a card in a list
now opens the editor on that card.

Image: ![floating-toolbar-four-by-four.png](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/f12ba53b38716231e07d5181786c04f83d487b20/docs/releases-notes/2026-11-14-v1.9.0/floating-toolbar-four-by-four.png)

## 2/

The details are in the release notes:
https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.9.0

## 3/

Install or update it from the Marketplace, or from Open VSX for VSCodium and Cursor; it is free and
MIT:
https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio
https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
