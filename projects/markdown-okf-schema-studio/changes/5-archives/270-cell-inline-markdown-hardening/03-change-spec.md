---
title: "CR 270: harden the cell inline Markdown shown after Tab"
description: Test and tighten the inline Markdown a table cell shows after Tab, until the next render.
status: open
date: 2026-11-10
---

# CR 270: harden the cell inline Markdown shown after Tab

> [!NOTE]
> Intent: `01-intent.md` (the four Inspector findings of CR 268, PR #337). Base: `origin/main` at `293366d0`.

## Owner's decisions (2026-11-10)

| Question | Decision |
| --- | --- |
| Scope | The four findings of `01-intent.md`: a direct unit test of `src/page/modules/cellInlineMarkdown.ts`, no protocol-relative `//host` links, no intraword `_` emphasis (CommonMark flanking rules as far as is simple), the four arrow keys in the TABLE-035 test. |
| Priority | P1, small. Short spec, the owner does not review it before coding. |
| Approved requirements | None changed: `SwRS-MDOKFSTUDIO-TABLE-035` is `proposed`. |

## Done when

- A new test file asserts the link allowlist (`javascript:`, `data:`, `//host` dropped; `https:`,
  `mailto:`, `#`, relative kept), backslash escapes, `<br>`, and that `snake_case_name` and `2 * 3 * 4`
  stay plain text, with `@tests_req SwRS-MDOKFSTUDIO-TABLE-035`. The link and emphasis cases fail on the unchanged code.
- The TABLE-035 "cell left shows its new text" test covers the four arrow keys.
- A `CHANGELOG.md` `## Unreleased` line only if the visible behaviour changes (the emphasis case does).
