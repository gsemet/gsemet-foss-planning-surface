## Summary

The release guideline asked for the same feature-release shape whatever shipped: a short version in
the title, a subtitle of verbs and headings saying "what you can now do". A reader of a fix release
could not tell it was one, and a removed setting could sit inside a paragraph. The guideline now asks
for the release's kind first, in short plain text, with bad news on its own labelled line.

## Deliverables

One file changes, `.agents/guidelines/release-process.guidelines.md`:

| In the release notes | Before | After |
| --- | --- | --- |
| Title | `X.Y` | `X.Y.Z` |
| Subtitle | two or three changes as verbs | the kind first, at most 16 words |
| Highlight heading | "what you can now do" | in the kind's words ("Fixed: ...") |
| Removal, changed behaviour, known issue | no rule | a `Removed:`, `Changed:` or `Known issue:` line in the visible part |
| Length | no budget | 16, 20, 40 words; visible part 120 or 250 |
| Pictures | cropped | only visible changes, cropped, 900 to 1200 px wide, at most 600 px high |
| Before the version pull request | nothing | a ten-question self-check, answered by the agent |

The values follow the shared release template of the tool that runs this project's releases (its
section on the notes and its section on release pictures). Each rule against the guideline:

<details>
<summary>Rule by rule, with the guideline's line</summary>

| Rule | Lines | Shared template | This guideline | Same |
| --- | --- | --- | --- | --- |
| Written for the user: a maintainer's plain words, no ticket number, internal term or implementation | 242-244 | yes | same, kept from before | yes |
| Kinds, decided before writing | 220-226 | feature, fix, restore, breaking, internal | same five, same definitions | yes |
| Subtitle names the kind | 228-230, 291-292 | first words; no "you can now" in a fix | same | yes |
| Several kinds | 232-233 | breaking, feature, restore, fix, internal | same | yes |
| Version against kind | 235-238 | the pull request says so; the version is never changed alone | same; the owner decides | yes |
| Title | 290 | full `X.Y.Z` | same | yes |
| Header and links | 289-301 | subtitle, `<sub>` line, links | same; `<sub>` line and links unchanged | yes |
| Highlights | 249-255, 302-304 | two to four, heading by kind, two sentences, picture | same | yes |
| Picture that shows the whole change | 337-338 | no text | same | yes |
| Smaller changes | 305-308 | one line each | one line each; heading `Smoother editing` in a feature release, `Other fixes` in a fix release | **differs**: the project keeps its own heading |
| Folded sections, each changelog line once | 309-317 | once | same | yes |
| One sentence, `Fixed:` and `Restored:` | 256-259 | consequence, not mechanism | same | yes |
| Bad news | 260-264, 307-308, 313-314 | three labelled lines in the visible part | same | yes |
| Banned constructions | 272-283 | seven rows | same seven rows, plus the earlier bans | yes |
| Setting named as a setting | 268-269 | name, default, where to turn it on | same | yes |
| Word budgets | 319-324 | 16, 20, 40, 120, 250; a judgement, not a check | same | yes |
| One picture per visible change | 328 | yes | same | yes |
| Crop | 329-332 | cropped to the change | the changed element; a gesture keeps its target | **differs**: a feature clip's GIF is not cropped (342-344), because it shows the whole filmed window and its zoom stands in for the crop |
| Size | 333 | 900 to 1200 px wide, at most 600 px high | same, for still pictures | **differs**: a feature clip's GIF is exempt (342-344), because it films the whole window, as it is already exempt from cropping |
| Before and after | 334-336 | one joined image, same region and scale | same | yes |
| Alt text | 339 | the caption, no caption line | same | yes |
| Missing picture | 340-341 | the notes say nothing; the pull request's known gaps name it | the notes say nothing; the version pull request's body names it | **differs**: where it is named, because this project's release is reviewed on the version pull request |
| Hero image | 402-404 | not covered | announcement thread only; the first highlight takes its own picture | **differs**: a project picture the new size would not allow in the notes |
| Self-check | 359-375, 58-59 | ten questions, before the notes are final | same ten, before the version pull request opens and before its body is regenerated | **differs**: when it runs, because this project's notes are reviewed on the version pull request and its body is regenerated after remarks |
| Capture a missing picture; read each picture before keeping it; name a picture without a Markdown link; upload | none | release mechanics | not carried | **differs**: only the writing and picture rules are taken, because this change leaves how a release is run to the project's own steps |

</details>

## Changes

- "Release notes" of the guideline: a new "The kind" part, rewritten "Writing" and "Structure"
  parts, an "Images" part that gathers the picture rules, and a new "Self-check".
- A performance gain the user can see is a highlight with figures.
- The hero image now serves the announcement thread only.
- No script changes: the rules are read by whoever writes the notes. Published notes are not
  rewritten.

## Impacts

No visual change: a contributor guideline only; the extension and the published notes are unchanged.

The next release notes are written to these rules. A dry run of the self-check on the 1.12.1 note,
as it stands, shows the faults it would have caught:

| # | Question (short) | Answer | Why (line of the note) |
| --- | --- | --- | --- |
| 1 | Subtitle names the kind first | no | line 4 names no kind |
| 2 | Title carries `X.Y.Z` | no | line 1 says `1.12` |
| 3 | Tone of the kind everywhere | no | feature headings (18, 24); `Smoother editing` in a patch (28) |
| 4 | Every fix starts "Fixed:" | no | none does (30-32) |
| 5 | Every restore owns the earlier break | no | "as it did before 1.11.0" (20), "as in 1.12.0" (32) do not say a release broke it |
| 6 | Bad news on labelled lines | no | two removed settings and a postponed ability sit in paragraphs (20, 22) |
| 7 | One sentence per line, budgets kept | no | bold lead plus a second sentence (30-32); subtitle 18 words for 16; longer highlight, lines and visible part than allowed |
| 8 | Consequence, no banned construction | no | "Studio no longer watches the files you open" (20) is mechanism; bad news is buried |
| 9 | Pictures within bounds, none apologised for | yes | no picture, and no sentence about it |
| 10 | Version matches the kind, or the pull request says it is probably wrong | no | a patch that removes two settings; its pull request calls the number the owner's choice, never probably wrong |

## Blast radius

- **1**: local and isolated; a plain `git revert` restores the previous behaviour.

Grade: 1. One guideline file; no code, script, workflow or published note changes.

## Test plan

- [x] New or changed tests: none, a documentation change
- [x] Requirements: No behaviour change
- [x] Changelog: No user-facing change
- [ ] "what you can now do" appears in the guideline only as the feature kind's heading
- [ ] Local gates: `just release-notes-check`, `just check`, `just preflight`
- [ ] Review
- [ ] CI green

## Human decisions

- A fix release keeps today's structure; only the tone of its headings and lines follows its kind.
- No new script check: the rules are a self-check read by the writer.
- A feature clip's GIF is exempt from the new picture sizes.
- The published 1.12.1 note is not rewritten.
- A visible performance gain is a highlight with figures.
- The hero image serves the first post of the announcement thread only.

## Autonomous decisions

- In a fix release the smaller changes are headed "Other fixes", to match the kind's tone.
- The two older picture rules about the text next to a picture moved to "Images" with their bullets,
  so each rule is written once.
- "A fix says what works now" is written in "Writing" too, as the self-check asks it.

## Known gaps

- The opening of "Release notes" and "Structure" still speak of a picture for each highlight, while a
  change with nothing visible, or no picture within the sizes, now gets none.
- The heading of the smaller changes is not given for a breaking release.
- The smaller changes keep their bold lead; how it combines with a line starting `Fixed:` or
  `Removed:` is not said.
- The part on the version pull request body does not say where the "version is probably wrong" and
  "no picture" statements go, so a regenerated body needs them added again.
- The number of highlights for an internal or a one-fix release is not said.
- A removal told as a highlight and again on its `Removed:` line sits against "every changelog line
  appears once".
- A performance figure shown as a chart is not a crop of a changed element.

## Internal references

- CR-523 notes-kind

🤖 Generated with [Claude Code](https://claude.com/claude-code)
