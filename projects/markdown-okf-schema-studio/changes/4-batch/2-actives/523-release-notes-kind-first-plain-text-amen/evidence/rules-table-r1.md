# Card rules against the guideline (round 1)

Guideline lines of `.agents/guidelines/release-process.guidelines.md` in the worktree, round 1
(uncommitted, on base b9b29c5a; check the numbers again at the PR head).

| Rule (card "The notes" and release pictures) | Lines | Card value | Guideline value | Match |
| --- | --- | --- | --- | --- |
| Kinds, decided before writing | 220-226 | feature, fix, restore, breaking, internal | same five, same definitions | yes |
| Subtitle names the kind | 228-230, 291-292 | first words; no "you can now" in a fix | same | yes |
| Several kinds | 232-233 | breaking, feature, restore, fix, internal | same | yes |
| Kind against version | 235-238 | PR says so; the agent never changes the version | version PR body says so; the owner decides | yes (role words differ) |
| Title | 290 | full `X.Y.Z`, never `X.Y` | `X.Y.Z` (the full version) | yes |
| Header and links | 291-301 | subtitle, `<sub>` line, links | same; `<sub>` and links unchanged | yes |
| Highlights | 302-304, 249-255 | two to four; heading by kind; two sentences; picture | same; keeps "Nothing comes under the picture" | yes |
| Smaller changes | 305-308 | one line each | one line each, bold lead kept; `Smoother editing` in a feature release, `Other fixes` in a fix | difference: project heading |
| Folded sections, every line once | 309-317 | each changelog line once | same | yes |
| One sentence, labelled lines | 256-259 | one sentence; "Fixed:", "Restored:"; consequence | same | yes |
| Bad news | 260-264, 307-308, 313-314 | `Removed:`, `Changed:`, `Known issue:`, visible part | same | yes |
| Banned constructions | 272-283 | seven rows | same seven rows, plus the existing items | yes |
| Setting named as a setting | 268-269 | name, default, where | same | yes |
| Budgets | 319-324 | 16, 20, 40, 120, 250; judgement, not a check | same | yes |
| Only visible changes | 328 | one image per change | same | yes |
| Crop | 329-332 | cropped to the change, never the whole window | changed element; a gesture keeps its target | difference: clip GIF (342-344); hero image, used by the thread only (400-408, 422-423) |
| Size | 333 | 900-1200 px wide, at most 600 px high | same, still pictures | difference: clip GIF exempt |
| Before and after | 334-336 | one joined image, same region and scale | same | yes |
| Alt text | 339 | the caption; no caption line | same | yes |
| Missing picture | 340-341 | silent notes; "Known gaps" names it | silent notes; the version PR body names `no picture for <change>: <why>` | difference: where it is named (spec) |
| Self-check | 359-375 | ten questions, before the notes are final | same ten; before the version PR opens and before its body is regenerated; pointer at 58-59 | difference: timing words (spec) |

Not carried (the specification does not list them): capturing a missing image with the project's own
means, reading each image before keeping it, naming an image without a Markdown link, and the upload
step.
