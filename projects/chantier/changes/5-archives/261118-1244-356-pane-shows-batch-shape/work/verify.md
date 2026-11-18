# Verify CR-356

Head: 2ad1d97b694744b6f18a73f494afe7c813733500

Judged at 2ad1d97b694744b6f18a73f494afe7c813733500 unless stated.

1. Pane words (spec section 3, Evidence "Pane"). Command: `uv run --no-project python scripts/mod.py` in the worktree.
   Output: "(pass) a batch header ends its slots line with the batch shape, and says unknown when it is null or odd", "(pass) a batch header shows its slots, and nothing when the index has none", "79 pass / 0 fail". The test covers parallel, series, stack, null -> unknown, odd -> unknown, mode with no slots (word alone), slots with no mode (`Slots 0/3, 3 free`, no `free ·`). Diff of hooks/register.tsx read: the word rule is stack|series|parallel else unknown. VERIFIED.
2. Index carries `mode` (section 1), scratch project (own git repo under work/scratch, every call run from it, no --project; CLI code from the worktree): after `open --mode parallel --slots 3 --direct`, then `order mode --note stack`: index `batches` = `[('batch-01', {'taken': 0, 'total': 3}, 'stack')]`; after `order mode --note series`: `[('batch-01', 'series')]`; after `--note parallel`: `[('batch-01', 'parallel')]`; `schema` printed 3. The index follows a live switch; schema unchanged. VERIFIED. (Scratch removed.)
3. Type: `types/index.d.ts` diff adds `mode?: string | null` beside `slots?`; `scripts/mod.py` (validate and tests) passed (claim 1). VERIFIED.
4. Docs: `git diff origin/main...HEAD -- docs/boards.md` shows "its slots and its shape (`Slots 3/3, 0 free · parallel`)". VERIFIED.
5. Scenario checks added (index mode equals the batch's STATUS.json mode; index "stack" after `order mode --note stack`): present in the diff of scenario/run_scenario.py; `gh pr checks 321` per the Driver's brief: scenario (ubuntu) green at this head. Not re-run by me. VERIFIED on CI.
6. PR description (posted via `gh pr view 321 --json body`, equal to work/pr-body.md): renders, no images, Summary/Deliverables/Changes match the diff; Known gaps names the missing screenshot. The Test plan boxes (Review, Verified, CI) are still unchecked placeholders for the Driver. VERIFIED.
7. Screenshot of the pane from a real session: not captured (not possible here); named in Known gaps. Not a verdict change.

VERIFIED
