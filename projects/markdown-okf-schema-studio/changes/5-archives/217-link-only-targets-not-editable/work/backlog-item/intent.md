# In edit mode a click on a link jumps to another file, and the next keys edit that file

Severity High · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-BLOCK-014 (proposed, to change), SwRS-MDOKFSTUDIO-BLOCK-258 · Area Inline editing · Side preview · QA210-02, QA215-01 · Replay `scenarios/c1-1-link-card-not-editable.json`, `scenarios/c3-1-link-card-footer-click-navigates.json` · P1

> [!IMPORTANT]
> **Owner decision, 2026-10-31 (replaces the earlier "margin click" decision).** In edit mode, a click on a
> link opens the block's editor, and Cmd/Ctrl+click follows the link. In reading mode nothing changes: a
> click follows the link. This is the rule BLOCK-014 already applies to a linked image, extended to every
> link.

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![Link card: double-click navigates to the target](evidence/currently.jpg) | ![Link card outlined: a block editor should open](evidence/expected.jpg) |
| ![Link-only paragraph: click navigates](evidence/currently-paragraph.jpg) | ![Link-only paragraph outlined: a click should open the editor](evidence/expected-paragraph.jpg) |
| ![Link card footer: click navigates, typing lands in targets/alpha.md](evidence/currently-footer.jpg) | *Expected: the card's editor opens; `targets/alpha.md` is never opened, so no key reaches it.* |
| *Currently, edit mode: a click on a `:link:` card (title, body, footer) or on `*Next: [Related](related-target.md)*` opens the link target and no editor (replays `c1-1`, `c0-1`, `c3-1`).* | *Expected (annotated copies of the before-shots): each click opens the block's editor; Cmd/Ctrl+click still follows the link.* |

The Currently shots are the before-shots the fix PR must reproduce.

## Why this is wrong

In edit mode a click on text means "edit this", and every other block opens its editor on a click. A
link breaks that: a `:link:` grid card, a paragraph made only of a link (the `*Next: […]*` line that
closes every chapter) and any link inside a paragraph jump to the target instead. The worst case is
QA215-01: after a click on a link card's footer, the author's next keys (" F") go into the front-matter
editor of `targets/alpha.md`, whose buffer becomes dirty (`--- F` on line 1). A file the author never
meant to open is changed without warning. Editors that mix reading and editing (Word, Google Docs, VS
Code's own Markdown links) follow a link on Cmd/Ctrl+click and edit on a plain click; the preview already
does this for a linked image (BLOCK-014, "A linked image").

## The rule

| Input, **edit mode on** | Effect |
| --- | --- |
| Click on a link: inside a paragraph, a link-only paragraph, a `:link:` card (title, body, footer), a linked image | The block's editor opens; the link is not followed |
| Enter or Space on a focused link | Same as a click: the block's editor opens |
| Cmd/Ctrl+click on a link | The link is followed; no editor opens |
| Cmd/Ctrl+Enter on a focused link | The link is followed |
| **Edit mode off** (reading) | Unchanged: a click, Enter or Space follows the link |

The editor opens on the source lines of the block that holds the link. A `:link:` card has no source
mapping today (BLOCK-258): the fix maps the card the way a non-linked card is mapped, so the editor opens
on its directive or option line.

Uncheck to disagree: [x]

## Hover hint

In edit mode, hovering a link shows a short hint, "Cmd/Ctrl+click to follow" (Ctrl on Windows and Linux),
so the author knows how to navigate. No hint in reading mode.

Uncheck to disagree: [x]

## Requirement to write or change

Change SwRS-MDOKFSTUDIO-BLOCK-014 (lifecycle proposed, so no approval record is needed):

- the row "click, Enter or Space on a link inside a paragraph, edit mode on → the link is followed and no
  editor opens" becomes "→ the block's editor opens; Cmd/Ctrl+click or Cmd/Ctrl+Enter follows the link";
- the row "click on a mapped block that is itself inside a link → no editor opens" becomes "the block's
  editor opens";
- generalise the "A linked image" scenario to every link: paragraph links, link-only paragraphs, `:link:`
  cards, linked images; add the hover hint.

Update BLOCK-258 so a `:link:` card keeps a source mapping. Update the tests that assert the old rule
(`test/page/blockReq.requirements.test.ts`: "a click on a link inside a paragraph follows the link and
opens no editor", "Enter or Space on a link inside a paragraph opens no editor").

Uncheck to disagree: [x]

## Test to add

Real-input E2E, edit mode on: a click on the link-only paragraph and a click on a `:link:` card's footer
each open a block editor and leave the active file unchanged; a Cmd/Ctrl+click on the same link navigates
to the target. Then type a key after the footer click and assert `targets/alpha.md` is not dirty. It
earns a test because the old failure silently changed another file.

Uncheck to disagree: [x]

## Steps to reproduce

1. Fixture `fixtures-visual/46-grid-cards.md` ("Linked card"), preview to the side, edit mode on. Click
   the title, the body or the footer "Footer of the card": the editor group switches to
   `targets/alpha.md`, no textarea opens. Type " F": the target's front matter changes.
2. Fixture `synth/linkonly.md`, preview to the side, edit mode on; click the middle of the "Next: Related"
   line: the preview navigates, no editor opens.

```markdown
# Link only

Some intro paragraph.

*Next: [Related](related-target.md)*

Tail paragraph.
```

## Where it comes from

`src/page/features/pageInput.ts` skips links on purpose (around lines 197 and 244–246); the linked-image
case is the one place that already prevents the default and opens the editor. `:link:` cards are left
unmapped by design (#236, BLOCK-258); the card title is an `a.myst-grid-card-link[data-sphinx-preview-navigation]`
stretched over the card.

## Done when

- [ ] In edit mode a click, Enter or Space on any link opens the block's editor; Cmd/Ctrl+click and
      Cmd/Ctrl+Enter follow it; reading mode is unchanged.
- [ ] The hover hint shows in edit mode only.
- [ ] Replays `c1-1`, `c0-1` and `c3-1` pass with the new expectation.

Sources: sheet [c1-1](../../../210-qa-campaign-2026-10-31/work/01-myst-cards-tabs/c1-1-link-card-not-editable.md),
sheet [c0-1](../../../210-qa-campaign-2026-10-31/work/10-noop-sweeps/c0-1-link-only-paragraph-not-editable.md),
sheet [QA215-01](../../../215-qa-campaign-2026-10-31/work/02-grid-cards/c3-1-link-card-footer-click-navigates.md),
replays [c1-1](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c1-1-link-card-not-editable.json)
and [c0-1](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c0-1-link-only-paragraph-navigates.json),
[campaign 210 index](../../../210-qa-campaign-2026-10-31/work/00-index.md),
[campaign 215 index](../../../215-qa-campaign-2026-10-31/work/00-index.md).
