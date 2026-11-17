## Summary

Release 1.7.1. Everything merged since 1.7.0 is on the published site: the requirements viewer with
the map of each use case, the main paths of the use cases, one cream look for the whole site and
the share picture cards. The site is published only on a version tag, so this release is what puts
those pages online. The extension itself does not change.

## Deliverables

```text
docs/releases-notes/2026-11-12-v1.7.1/
├── release-notes.md              the GitHub release notes (rendered below)
├── tweet.md                      the three-post announcement thread (rendered below)
├── requirements-viewer-map.png   hero: the map of a use case in the requirements viewer
└── share-card-gallery.png        the share card of the screenshot gallery
```

## Changes

- `just version 1.7.1`: `package.json`, `package-lock.json`, `plugin.json`,
  `.claude-plugin/plugin.json`, `.github/plugin/marketplace.json`.
- `CHANGELOG.md`: the `## 1.7.1 - 2026-11-12` section. Its lines are written in this commit rather
  than in the merged pull requests, on the owner's decision for this release (documentation only,
  so no new heavy run of `main` was needed).
- The release notes folder above. The hero is a capture of the site built from the reports of the
  heavy run of `main` (`just site-from-run 43262188098`), the exact site this tag publishes.

## Impacts

No change to the extension. On merge, CI tags `v1.7.1`, publishes the extension to the
Marketplace, creates the GitHub release with these notes, and deploys the site to GitHub Pages.

## Blast radius

Grade: 3. A release: tag, Marketplace publication and Pages deploy. Before the merge, closing the
PR undoes everything; after it, a fix ships as a new version.

## Test plan

- [x] New or changed tests: none, a release
- [x] Requirements: no behaviour change
- [x] Local gates: `just preflight` at this head: `ci-static` (with the release notes check) and
      `ci-visual` passed; the real VS Code stage could not run on the locked screen of the machine,
      so `ci-integration`, then `ci-report` and `ci-gallery`, failed. Its proof is the heavy run
      dispatched on this branch, below.
- [x] Heavy run on this branch's head `786fe7b0`: run 43275294730, `integration` and `stress`
      success, the whole run green
- [x] Heavy run green on `main` HEAD `cf51f12f` (run 43262188098: `integration` and `stress` success)
- [ ] Review: the owner reviews the notes and the thread
- [x] CI green (pull request run 43275285258)

## Internal references

- Change request CR-304 release-v1-7-1 of batch-01; the merged changes are PRs #371 to #374.

---

# 📰 Release notes (rendered)

<h1 align="center">Markdown OKF-Schema Studio 1.7.1</h1>

<p align="center">
  <b>Browse the requirements as a map, read the whole site in one cream look, share a page with a picture card.</b><br>
  <sub>27 changes since 1.7.0 · VS Code 1.95 or later · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from the Marketplace</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.7.1/CHANGELOG.md">Full changelog</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.0.0">1.0 showcase</a>
</p>

---

This release is about the
[published site](https://gsemet.github.io/markdown-okf-schema-studio/). The extension itself
works as in 1.7.0.

## 🗺️ Browse the requirements as a map

The [Requirements](https://gsemet.github.io/markdown-okf-schema-studio/requirements/) page is now
a viewer you move through one level at a time: the 16 areas of Studio, the use cases of an area,
one use case, and one behaviour with its rule, scenarios, source files and tests. Search works on
every page, and the pages read without JavaScript.

Almost every use case now has its main paths written down step by step, and the viewer draws them as a
map: each circle is a state the user reaches, each label is the behaviour that takes them on, with
the number of tests that check it. Play path walks you through one path.

![The map of the use case "A writer edits a table cell in place and never loses the text": two paths of states, each step labelled with its behaviour and its number of tests, and the other outcomes on dashed lines](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/786fe7b0fad3a686d34f527a663d9462fa7d5c36/docs/releases-notes/2026-11-12-v1.7.1/requirements-viewer-map.png)

The figures of the page are right again: the old page counted every requirement as "unknown", and
the old `requirements.html` link still works.

You can see what Studio promises, and how each promise is tested, without reading the code.

## 🎨 One cream look, and a picture when you share a page

Every page of the site, and the requirements viewer, now has the look of the extension's Cream
theme: the same colours, fonts and header everywhere, with no dark mode.

A link to the home, Contributing, How we ship, Gallery or requirements pages, shared on X or any
site that reads Open Graph, now shows a large picture card. The gallery card shows the live number
of captures.

![The share card of the screenshot gallery: "542 screenshots" in cream, with three captures of the extension in VS Code](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/786fe7b0fad3a686d34f527a663d9462fa7d5c36/docs/releases-notes/2026-11-12-v1.7.1/share-card-gallery.png)

A shared link now says what it leads to before anyone clicks it.

<details><summary><b>🐞 All fixes</b></summary>

- On the site, the requirements breadcrumb shows the full current page on its own row, and wide
  code blocks and tables scroll inside themselves instead of widening the page on a small screen.
- Without JavaScript, the requirements viewer hides its search and play buttons, which need it.
- The requirements viewer passes the accessibility checks.

</details>

<details><summary><b>🛠 For contributors</b></summary>

- A check, run by `just requirements-lint`, fails when the main paths of a use case cite a
  behaviour that does not exist, is not active, or belongs to another use case.

</details>

---

# 🐦 Announcement thread (rendered)

# Announcement thread for 1.7.1

## 1/

When a coding agent changes Studio, I want to see what the change touches: which promise to the
user, and which tests hold it. That was a long page of IDs. Now almost every use case is written as the
path a user walks, and the site draws it as a map: each step, the behaviour behind it, and how many
tests check it. The whole site also got the cream look of the extension.

Image: ![requirements-viewer-map.png](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/786fe7b0fad3a686d34f527a663d9462fa7d5c36/docs/releases-notes/2026-11-12-v1.7.1/requirements-viewer-map.png)

## 2/

The details are in the release notes:
https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.7.1

## 3/

Install or update it from the Marketplace, it is free and MIT:
https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
