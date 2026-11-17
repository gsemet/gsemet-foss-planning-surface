# c2-1 — The Comments button does not hide review threads from the comments file

Severity Low · Confidence Reproduced (twice, second time on a clean fixture) · Area Review comments, toolbar · Modes side preview ·
Replay `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/c2-1-comments-toggle-keeps-threads.json` ·
Evidence [c2-1-comments-hidden-threads-visible.jpg](../../evidence/c2-1-comments-hidden-threads-visible.jpg)

**Steps.** Fixture `synth/review-threads.md` (with `review-threads.comments.json`, in assets/synth): open the side preview, open the
toolbar chevron, click the Comments button (it becomes "Show comments", `aria-pressed=false`).
**Expected / observed.** Expected: the author who hides comments no longer sees comment marks. Observed: the highlighted quotes
(`mark[data-okf-comment-thread]`), the badges and the "Orphaned comments" list stay fully visible; only the inline `<!-- comment -->` and
`<!-- THREAD` chips are hidden.
**Direction.** `src/core/preview/styles/commentStyles.ts` ~L535 hides only `.okf-comment` chips for `data-sphinx-preview-comments="off"`;
either extend it to `mark[data-okf-comment-thread]`, badges and the orphan list, or relabel the button. SwRS REVIEW-152 only speaks of chips, so
decide the intent first. Test to add: a scenario check on the mark background after the toggle.
