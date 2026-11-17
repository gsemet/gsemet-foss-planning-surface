# Behaviour note: Replace all and a link target that repeats the query

## Today

The find bar counts 4 matches for `needle` in `assets/synth/find-list-b.md`. Replace all replaces 2:
the list item and the link label stay `needle`, and only after the click does the note say "2 matches
cannot be replaced from the preview". Before the click the note is empty.

Cause (read in the code, matches the QA replay `c4-1`): the page sends each match with "occurrence k of
n of this text in the rendered block". The source block is the whole list; it holds 3 occurrences (the
two visible ones plus the URL `https://example.com/needle`), the page shows 2. The planner
(`planFindReplace` in `src/core/edits/findReplace.ts`) refuses any block whose counts disagree, so the
whole list is skipped. The page's pre-click count (`unreplaceableCount` in `src/page/modules/findBar.ts`)
only knows blocks with no source mapping, never the host-side refusals.

## After (proposal)

1. The planner leaves out the text a reader cannot see in the source block: link and image targets and
   titles (`](url "title")`), and reference definitions (`[label]: url`). In the fixture all 4 visible
   matches are replaced and the URL stays `https://example.com/needle`. Autolinks (`<https://…needle>`)
   stay counted: their URL is the visible text.
2. While the replace row is open, the page asks the host to plan the replacement without applying it
   (a dry run, debounced after each search), and the note says before the click: "N matches cannot be
   replaced from the preview". This covers the cases that stay skipped (a formula, an admonition title,
   markup inside the match). The after-click note is unchanged.

## Requirements touched

- SwRS-MDOKFSTUDIO-TOOLBAR-012 (draft): the boundary row "a match in a link label whose target repeats
  the text: skipped" becomes "replaced; the target is kept".
- New SwRS (proposed, next free id SwRS-MDOKFSTUDIO-TOOLBAR-131): "Replace all announces the matches it
  will skip", derived from StRS-MDOKFSTUDIO-TOOLBAR-003 (draft).
- No approved requirement changes.

## Choices left open

- A. Pre-click announcement (part 2): recommended yes (the intent's requirement section asks for it).
  Alternative: only part 1, and the new SwRS covers the link-target case only.
- B. When the dry run runs: recommended only while the replace row is open (a reader who only searches
  causes no host traffic); debounce 150 ms.
- C. Image alt text `![alt needle](…)`: the page does not see alt text, so today such a block is skipped.
  Recommended: leave the whole image out of the source count too (alt text is not replaced).
- D. Wording: keep the existing "N matches cannot be replaced from the preview" for the pre-click note.

## Shots

- /private/tmp/claude-502/cr225-driver/shots/before-replace-all-skips-list.png (the QA replay shot in
  the real VS Code window: 4 matches before, 2 left after Replace all).
