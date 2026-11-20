Short name: `relnotes-style`

# Answers (owner, 2026-11-20, Chief of Staff grill)

- Owner's words: 'trop verbeux. Je voudrais plus privilégier des démos et screenshots et se concentrer sur ce que la release APPORTE à l'utilisateur vs ce qu'elle est (qui reste en détail)'.
- Rejected tries: a bare minimum (the reader cannot tell what was there before); "Before: / Now:" labels in the notes ('c'est lourd'; they stay in PRs); an invented scene with punchy bullets ('pile ce qu'il ne faut pas faire').
- Feedback on try D: a change of visible behaviour shows the before and after pictures joined into one image; when the picture shows the whole change, the picture alone is enough; a setting must be named so the reader understands it is a setting.
- Approved: the writing prompt below, and try E written from it without retouch.
- 'chantier ne sera pas mis à jour au moment de la release': the Studio guideline carries every rule itself. The generic part is sent to chantier for its release template; Studio may trim its copy once chantier ships it.
- The PR guideline already asks for before/after in PRs: unchanged.

## Approved writing prompt

> Write like a maintainer telling a colleague what changed. Use short, complete sentences, plain verbs, and "you". Write for the user: no ticket numbers, no internal terms, no implementation.
> Structure: a title; one line naming the two or three main changes, as verbs; two to four highlights; the smaller changes, one line each; every fix and detail in folded sections.
> Each highlight is a heading that says what you can now do, then a picture, then at most two sentences.
> - When the change replaces a behaviour you can see, the picture puts the before and the after side by side in one image, and the text does not describe the before again.
> - When the picture shows the whole change, write no text under it.
> - Name a setting as a setting: "the setting `full.name`", with its default value and where to turn it on.
> Never use: "Before:" or "Now:" labels; invented scenes; punchy fragments; praise words (seamless, powerful, effortless, easily); a closing "why it matters" line.
> Coverage: every changelog line appears once, visible or folded.

## Approved try E (shape reference, images as placeholders)

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
