## Summary

In the Auto width mode, a wide table, figure, image, code block or Mermaid diagram widens past the
text column only when it sits at the top level of the page. Inside a list item, admonition, block
quote, tab set, dropdown or card it keeps its Margin layout, but the requirements listed this as a
known issue. They now state it as the rule. The extension behaves as before.

## Deliverables

The requirement for Auto width now says what the page does:

| Wide block in Auto | Requirement before | Requirement after |
| --- | --- | --- |
| Top-level table, figure, image, code block or Mermaid diagram | Widens (top level not stated) | Widens; "a direct child of the page content" |
| Image alone in a top-level paragraph | Widens (said only in the known issue) | Widens, stated in the rule; the exceptions below are a known issue |
| Linked image alone in a top-level paragraph | Not stated | Known issue: not widened |
| Block inside a list item, admonition, block quote, tab set, dropdown or card | Known issue | Specified: keeps the layout it has in Margin |

## Changes

- `SwRS-MDOKFSTUDIO-LAYOUT-023`: the normative text and `description:` limit widening to top-level
  blocks; a new refusal scenario covers nested blocks; the list-item case moves into it; the
  known issue on nested blocks is removed and one is added on images in a top-level paragraph; the
  verification notes follow, and their criteria say which of those images are measured.
- `test/page/runtimePageControls.test.ts`: a new unit test, `a wide block nested in a container is
  not measured` (a table, an image in a paragraph and a code block, each inside a container).
- `test/page/codeBlockBreakout.test.ts`: requirement markers only.
- The generated requirements index and a dated entry in `requirements/tiers/log.md`.

## Impacts

No visual change: no file under `src/` changes.

## Blast radius

- **1**: local and isolated; a plain `git revert` restores the previous behaviour.

Grade: 1. Requirements text, one unit test and test markers; nothing shipped to users changes.

## Autonomous decisions

- The new unit test gives its fake image the two members an image has in a browser (its natural
  width and its attribute lookup), so that a wrong widening rule fails it on an assertion rather
  than on a missing member of the fake page.
- No changelog line: the change has nothing a user would notice.
- The requirement records two image cases as a known issue, because requirements here state what
  the extension does today and "an image alone in a top-level paragraph" does not hold for them
  (see Known gaps). The wording of the rule itself is unchanged by them.

## Known gaps

- In a real browser, only the list-item case of a nested block is checked. The new unit test fakes
  an admonition, a block quote and a card by their element tags, and no test builds a tab set or a
  dropdown; the widening rule looks only at a block's parent.
- A linked image alone in a top-level paragraph is not widened, and a paragraph holding no text
  and several images, at least one of them not wrapped in another element, is measured as a whole
  from its first image. The requirement records both as a known issue; no test checks them, and
  changing the page is left to a later change.

## Test plan

- [ ] New or changed tests (they fail on the previous code): no behaviour change. The new unit test
      passes on the current code and fails (`AssertionError: TABLE`) when the widening rule is
      temporarily changed to accept any element, and (`AssertionError: P`) when only the check that
      an image's paragraph is at the top level is removed.
- [ ] Requirements: `SwRS-MDOKFSTUDIO-LAYOUT-023` changed (one scenario added), source
      `src/page/modules/widthMode.ts` (unchanged), tests `test/page/runtimePageControls.test.ts`
      and `test/page/codeBlockBreakout.test.ts`; `just requirements-update` run
- [ ] Changelog: no user-facing change
- [ ] Local gates:
- [ ] Review
- [ ] CI green

## Internal references

- CR-511 nested-code-blocks-do-not-widen-in-auto. The added scenario is S9; the list-item row
  moved from S8 to S9.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
