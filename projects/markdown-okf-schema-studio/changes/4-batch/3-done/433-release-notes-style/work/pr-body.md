## Summary

The release notes had grown verbose: each highlight explained the feature in a paragraph and ended
with a "why it matters" sentence. This PR rewrites the "Release notes" section of the release
guideline so the notes show what a release brings the user, mostly through pictures, and fold the
detail. The guideline carries every rule itself, starting with the next release.

## Deliverables

A new "Writing" subsection states the tone and the banned forms in one place:

> Write like a maintainer telling a colleague what changed. Use short, complete sentences, plain
> verbs, and "you". [...] Each highlight is a heading that says what you can now do, then a
> picture, then at most two sentences.
>
> Never use: "Before:" or "Now:" labels; invented scenes; punchy fragments; praise words
> (seamless, powerful, effortless, easily); a closing "why it matters" line.

The highlight shape it yields (images as placeholders):

```markdown
## ✏️ Edit a single list item
[image: before | after, side by side]
To edit the whole list, click beside the items.

## ↕️ Drag list items to reorder them
[GIF]

## 📑 Show list items in the table of contents
[capture]
Turn on the setting `markdownOkfSchemaStudio.preview.listItemsInToc` (off by default) in the VS Code
settings: the items of top-level lists then appear in the table of contents, under the heading above
them.

<details><summary><b>🐞 Fixes</b></summary> … </details>
<details><summary><b>🔎 Details</b></summary> … </details>
```

| Part of the notes | Before | After |
| --- | --- | --- |
| Highlight | paragraph, optional example, picture, "why it matters" sentence | picture, at most two sentences; a syntax may add a short example |
| Changed visible behaviour | one picture or a light and dark pair | one joined before / after image |
| Settings | no rule | "the setting `markdownOkfSchemaStudio.…`", its default, where to turn it on |
| Smaller changes | one bullet each | one line per bullet, bold lead kept |
| Folded sections | All fixes, For contributors | All fixes, Details (keyboard, defaults, limits), For contributors |

## Changes

- `.agents/guidelines/release-process.guidelines.md`, "Release notes": new "Writing" subsection;
  "Structure" keeps the centred header, the bold line of verbs, the `<sub>` line, the links line
  and the rule; highlights lose the explanatory paragraph and the closing sentence; a folded
  "Details" section is added; the coverage rule counts any folded section.
- "Images": the joined before / after image is one file in the notes folder, made from the
  before and after captures of the merged changes, with any tool the version PR names.
- Announcement thread: its tone rule also bans the forms listed in "Writing". The hero image is
  unchanged.

## Impacts

No visual change: this PR changes a contributor guideline only; the extension and the published
notes of earlier releases are untouched.

## Blast radius

Grade: 1. One guideline section; a `git revert` restores the previous release-notes rules. The
release-notes check script reads only the title and the images, which this PR does not change.

## Test plan

- [x] New or changed tests: none, documentation only
- [x] Requirements: No behaviour change
- [x] Changelog: No user-facing change
- [x] Local gates: `just check` and `just release-notes-check` pass at a719e64 (the 1.9.3 notes
      still pass)
- [x] Review: approved, committed as a719e64
- [x] CI green at a719e64: checks, report, static, static-windows and visual pass; the heavy
      jobs (integration, stress, release) are skipped on a pull request, as the CI rules say for a
      documentation change

## Autonomous decisions

None.

## Known gaps

None.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
