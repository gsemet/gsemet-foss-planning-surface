---
title: Harden the cell inline Markdown shown after Tab
description: Non-blocking findings of the CR 268 review (PR #337), deferred by the owner to a later CR.
status: inbox
date: 2026-11-10
---

# Harden the cell inline Markdown shown after Tab

PR [#337](https://github.com/gsemet/markdown-okf-schema-studio/pull/337) (CR 268, issue #335) added
`src/page/modules/cellInlineMarkdown.ts`: the cell left with Tab or an arrow key shows its typed text
as inline Markdown until the next render. The Inspector approved it with four findings, deferred by the
owner (2026-11-10) to a later CR:

| # | Finding | Proposed fix |
| --- | --- | --- |
| 1 | The module has no direct unit test: the link allowlist (`javascript:` and `data:` dropped), backslash escapes and `<br>` are not asserted. | A new test file with `@tests_req SwRS-MDOKFSTUDIO-TABLE-035` (`runtimeTableCellEditor.test.ts` is at 1490 of 1500 lines). |
| 2 | `SAFE_HREF` admits protocol-relative `//host/path`. | Tighten to `\/(?!\/)`. |
| 3 | `_` and `*` open emphasis inside words: `snake_case_name`, `2 * 3 * 4` flash as emphasis. | Follow the CommonMark flanking rules, at least no intraword `_`. |
| 4 | Only ArrowRight is tested; the scenario names the four arrows. | Loop the test over the four keys. |
