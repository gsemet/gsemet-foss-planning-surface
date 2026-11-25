## Summary

The OKF documentation page explains that Studio turns frontmatter into a properties table, but it shows nothing of it. This adds a 12 second silent feature clip of a note in an OKF Schema bundle: a typed table with a Description column and type icons, an invalid `status` value flagged by the title badge, a pick from a select of the schema's values, a save, and the error gone. The clip plays on the OKF page of the docs site.

## Deliverables

The clip, taken in a real VS Code window with the extension's packaged build:

![The OKF Schema bundle frontmatter clip](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/635f1ba09e6511333ac80ebe30e97678ec1fce24/docs/demo-video/clips/okf-schema-bundle-frontmatter/okf-schema-bundle-frontmatter.gif)

- MP4: [okf-schema-bundle-frontmatter.mp4](https://github.com/gsemet/markdown-okf-schema-studio/blob/635f1ba09e6511333ac80ebe30e97678ec1fce24/docs/demo-video/clips/okf-schema-bundle-frontmatter/okf-schema-bundle-frontmatter.mp4)
- WebM: [okf-schema-bundle-frontmatter.webm](https://github.com/gsemet/markdown-okf-schema-studio/blob/635f1ba09e6511333ac80ebe30e97678ec1fce24/docs/demo-video/clips/okf-schema-bundle-frontmatter/okf-schema-bundle-frontmatter.webm)
- Storyboard: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/635f1ba09e6511333ac80ebe30e97678ec1fce24/docs/demo-video/clips/okf-schema-bundle-frontmatter/clip.md)

Choices: it is the sibling of the standard frontmatter clip (same page, same `status` field, same click, save chord and marks); only `type: note` and a `_schema/` folder are added, so what differs on screen is what the schema brings. The control filmed is the enum select, picked with two ArrowDown keys and saved with Ctrl+Enter.

Deviation from the feature clip process: the storyboard review is the owner's, on this pull request, so it stays a draft until approved. Also, the storyboard first said the `status` row is red at frame 0. The trial take showed Studio paints no colour on a field row in error (the `okf-error` style exists only on the info row), so the only error signal on screen is the title badge reading 1 error. The clip shows what exists: every "red row" wording was changed to the badge, in the storyboard, the scenario comments and the OKF page alt text. No `src/` change.

## Blast radius

Grade: **1**. Documentation, a clip folder and tests only; a plain `git revert` restores the previous page.

## Autonomous decisions

- The error signal is shown as the title badge only, because the field row has no error colour; the missing row style is a possible bug filed apart, not fixed here.
- The select is changed with ArrowDown and saved with the save chord; the trial showed no native popup, so no Escape was needed.

## Known gaps

- Motion, rhythm and the loop as watched are not checked by the author; the owner reviews them on this pull request.
- A field row in error has no colour of its own (existing behaviour, not changed here).

<details>
<summary>Details</summary>

## Changes

- `docs/demo-video/clips/okf-schema-bundle-frontmatter/`: storyboard, scenario, stage (`_schema/note.schema.yaml` and `notes/release-note.md`), frames, MP4, WebM, GIF, poster and the check report.
- `docs/user/okf.md`: the clip under the introduction.
- `docs/demo-video/clip-kit/lib/*.test.mjs`: the clip's scenario checks and storyboard are covered.
- `test/site/siteClips.test.ts`: the OKF page plays the clip as a video.

## Impacts

The OKF page of the docs site shows the clip; the frames above show frame 0 and the picked value. No product behaviour change.

## Test plan

- [x] New or changed tests (`test/site/siteClips.test.ts`, the clip kit tests) <!-- they cover the new clip -->
- [x] Local gates at `635f1ba`: `just check` pass, `just clip-kit-test` pass (37 tests), clip render and check pass
- [x] Evidence: the clip and its frames, taken at `635f1ba`
- [ ] Review: approved at `635f1ba`
- [ ] Verified at `635f1ba`
- [ ] CI green at `635f1ba`

## Internal references

CR-499 okf-schema-bundle-frontmatter, batch-09, second clip stack.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
