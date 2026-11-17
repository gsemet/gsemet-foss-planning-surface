# c8-1 — Escape in an inline block editor still discards text already autosaved to the buffer (previous UX-01)

Severity High · Confidence Reproduced (twice, from a clean revert) · Area Inline editing · Modes side preview ·
Replay `scenarios/ux-01-escape-keeps-typed-text.json` · Evidence none (buffer diff)

**Steps.** `book/chapters/02-foundations.md`, preview to the side, edit mode, click the paragraph "Training and deploying an LLM", End, type ` KEEP ME PLEASE.`, Escape.
**Expected / observed.** Expected: text kept or a confirmation. Observed: the buffer diff against the mark holds the text before Escape (check 10 passes) and is empty after Escape; the autosaved text is silently reverted, as in the original UX-01.
**Direction.** Escape should close without reverting the autosaved text, or the revert should be announced; see the original sheet `04-archives/001-deep-UX-analysis/01-inline-block-editing/UX-01-escape-discards-autosaved-text.md`.

**Coordinator triage (2026-10-31).** Replayed in a fresh session: same result. The behaviour is now
specified by SwRS-MDOKFSTUDIO-BLOCK-053 ("Cancel and Escape restore the saved text": after an autosave,
Escape posts `previewEditCancel` and the host writes the original block text back). Listed as a design
decision for the owner (QA210-D1), not as a defect.
