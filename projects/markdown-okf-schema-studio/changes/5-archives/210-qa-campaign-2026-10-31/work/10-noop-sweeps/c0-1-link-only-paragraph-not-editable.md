# c0-1 — A paragraph made only of a link cannot be opened for editing by clicking its text

Severity Low · Confidence Reproduced · Area Inline editing · Modes side preview ·
Replay `scenarios/c0-1-link-only-paragraph-navigates.json` · Evidence none (check output)

**Steps.** Fixture `synth/linkonly.md` (line 5: `*Next: [Related](related-target.md)*`). Open the
side preview, switch edit mode on, click the middle of the "Next: Related" line.
**Expected / observed.** Expected: the paragraph opens in the inline editor, like any other block.
Observed: the click lands on the link, the preview navigates to the target document, no editor opens,
buffer unchanged. This is the closing line of every book chapter (`*Next: [Glossary](16-glossary.md)*`),
so the last paragraph of each chapter can only be edited by clicking beside the text.
**Direction.** Links are skipped on purpose in `src/page/features/pageInput.ts` (lines 197, 244-246);
in edit mode, require Cmd/Ctrl-click to follow a link, or open the editor on a plain click and follow
only on modified click.

**Fixture** `synth/linkonly.md` (create it in the workspace before replay):

```markdown
# Link only

Some intro paragraph.

*Next: [Related](related-target.md)*

Tail paragraph.
```

**Coordinator triage (2026-10-31).** Same root as QA210-02
([c1-1](../01-myst-cards-tabs/c1-1-link-card-not-editable.md)): in edit mode a click on a link
follows it, so a target made only of a link has no edit path. Merged into QA210-02.
