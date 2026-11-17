# T40 — Final verification, replay of every approved bug, RESULTS.md

| Field | Value |
| --- | --- |
| Fixes | Closure of all approved findings; QA-03 step 2 (agent visual review) |
| Depends on | T00–T39 `done` (or explicitly `blocked` with the user's agreement) |
| Gate | `unit types contracts full visual` |
| Risk | None (no product change expected) |
| Commit message | Only if documentation changed: `docs(vscode): record the deep UX fix campaign results` |

This task is run by the **orchestrator** with subagents. It is not a single implementer task:
it needs real VS Code exploration and multimodal screenshot review.

## Steps

1. **Gates.** Run `scripts/gate.sh T40 unit types contracts full visual`. Compare every failure
   with the T00 baseline. A new failure → stop and ask the user.
2. **Replay with the QA skill.** Spawn a `general-purpose` subagent (model `opus`) with the skill
   `.agents/skills/markdown-studio-exploratory-qa-claude/SKILL.md`. For **every approved bug sheet**
   (part 1, all `[x]`), it follows the sheet's "Steps to reproduce" on the same corpus, using real
   input. It records `fixed` / `partially fixed` / `not fixed`, with a screenshot path, in
   `PLAN/replay/<ID>.md`. It also replays the part-2 confirmations of UX-12 and UX-16 (aligned
   table, compact table, folded scalar, flow sequence). Frozen findings UX-22, UX-24 and UX-34 are
   replayed to confirm they are **unchanged**.
3. **Agent visual review (QA-03 step 2).** Follow `PLAN/visual-review.md`. Spawn one multimodal
   reviewer subagent per batch of about 20 screenshots, covering:
   - `test/visual/screenshots/*.png` with their `.txt` notes;
   - the latest `.artifacts/real-input-*/` captures.

   Each reviewer writes `PLAN/visual-review/batch-N.json`. Merge them into
   `PLAN/visual-review/review.json` and a `SUMMARY.md` that lists failures only.
4. **`PLAN/RESULTS.md`.** One row per approved finding: ID, status, commit SHA(s), the proving
   tests (unit and RI scenario names), replay evidence, and notes. Add rows confirming the frozen
   findings, and a section listing `followups.md` items that remain open.
5. **Docs consistency.** README sections touched by the plan read coherently. Spot-check that
   every README claim added by T07–T39 is true in the replay. Fix wording only, through one small
   implementer task (Sonnet, D-12) with review if needed.
6. Report to the user: a summary table, any `partially fixed` / `not fixed` items with evidence,
   the D-10 default actually shipped, and the open follow-ups.

## Done when

- Every approved finding is `fixed`, or explained with evidence and accepted by the user.
- `RESULTS.md`, `replay/`, and `visual-review/SUMMARY.md` exist.
