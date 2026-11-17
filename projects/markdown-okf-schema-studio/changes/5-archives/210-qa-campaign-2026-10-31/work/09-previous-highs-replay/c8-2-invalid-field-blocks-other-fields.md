# c8-2 — A rejected frontmatter value still blocks every other field (previous UX-38; same defect family as c6-1)

Severity High · Confidence Reproduced (twice) · Area Frontmatter · Modes side preview ·
Replay `scenarios/ux-38-invalid-field-does-not-block-others.json` · Evidence none (DOM check)

**Steps.** `synth/frontmatter-edit.md` (frontmatter-edge.md), edit mode, click `priority`, Cmd+A, type `9`, Enter (validation error), click the `reviewed_on` value.
**Expected / observed.** Expected: the second editor opens, or the invalid one is reverted with a message. Observed: no editor opens, nothing visible happens; the buffer is unchanged.
**Relation to c6-1.** Same defect family and probably the same root cause (the save path of `frontmatterValueEditor.ts` returns after a rejected save with the editor left open and `activeElement` moved off the control). c6-1 records the focus and Escape symptoms (and that clicking `title` does nothing, which is the UX-38 symptom); c8-2 records the cross-field symptom reported in UX-38. One fix covers both; suggest merging them under c6-1.
**Direction.** Revert or close the invalid editor when another field is clicked, and refocus the control after a rejection.

**Coordinator triage (2026-10-31).** Merged into QA210-01
([c6-1](../06-frontmatter/c6-1-rejected-commit-strands-editor.md)), which takes this High severity.
Replayed in a fresh session: still present.
