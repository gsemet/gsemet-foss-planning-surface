# Verify CR-369

Head: 19085335ea6c9eca23c41f808429109bf51cd806

All claims judged at 19085335 (first verification). CLI run from the worktree's code against scratch repositories (scratch removed at the end).

## Claims

1. `open` with no CR is born paused (19085335). `chantier open --default-branch main --slots 2 --budget 30`:
   `opened batch-01 on claude: no CR, paused, 2 slots, parallel, steering foreman` / `next: complete the brief ..., then \`order add --note <folder> --batch batch-01\` for each CR, then start the Foreman`, exit 0. batch.json: status paused, crs [], spent_usd null, paused set, summary ["Spent: none yet (no CR)"], foreman_transcript null. events.jsonl: `open` (crs []) then `pause` trigger "open, no CR". brief.md: `- CRs, in order: none yet (born paused; \`order add\` joins them)`. Direct mode (`open --direct`, own repo): second line ends `claim the batch, then \`take\``.
2. Refusals with no CR (19085335): `open --release 1` -> `--release N names the release CR among the CRs given, and none is given: add it later with \`order add --note <folder> --release\` (then \`order grant\`)` (exit 1 = usage); `--grant-fixes` and `--autonomous-releases 1` -> `--autonomous-releases and --grant-fixes need --release`; nothing written (no .agents folder after the three).
3. Second `open` (with item `1-inbox/first-thing`) -> `error: batch-01 is not closed (a paused batch stays until \`close\`): \`order add\` joins new work to it`, exit 2.
4. `status` on the empty batch: `batch-01 paused ... spent none yet of $30 (paused, cost to date), no CR yet` then ``no CR yet: `order add --note <folder> --batch batch-01` joins one``. 4-batch/STATUS.md header `spent none yet`, `## Paused` holds `- No CR yet.`. `pause` on it refused (needs epoch; paused already, as today).
5. STATUS.json: index schema 3 unchanged, batch entry `crs_total: 0` and after `order add` `crs_total: 1`; 4-batch/STATUS.json `crs: []`, `state: paused`, `crs_total: 0`.
6. `order add --note 1-inbox/first-thing --batch batch-01`: `batch-01 stays paused: the first \`take\` sets it running again` / `added CR-101, queued`; status then `spent unknown` (with a CR, as today). `foreman set local_foreman_t --epoch 1 --batch batch-01` then `take CR-101 --epoch 1 --batch batch-01`: `batch-01 was paused: running again`.
7. `close` of an empty never-steered direct batch (own repo): preview `0 CRs move from 3-done to 5-archives: none`, `Total: none: no session steered it`, `Foreman or steering: none: no session steered it`; `close --yes`: `closed batch-01: ... 0 CRs archived`. batch-01.md: `This batch held no CR.`, Total/Foreman lines `none: no session steered it`, `No retro was written: no CR.`. batch-01.json: `crs: []`, `cost_usd: null`, `cost_cause: "none: no session steered it"`, receipt steering `none`. The Chief of Staff outside-the-budget lines remain priced as today ($0.06 etc.), as the spec keeps them.
8. Refusal kept for a batch that held a CR with no steering transcript: could not be reached with the CLI alone (close of a queued CR is refused first: `cannot close batch-01, something still runs: CR-101 is queued`); proven by the in-process test `test_close_still_refuses_a_batch_that_held_a_cr_with_no_steering_transcript`: `uv run pytest skills/chantier/scripts/cli/tests/test_open_empty_batch.py` -> 12 passed (and `-k "empty or no_cr or born or never_steered"` -> 20 passed).
9. Pane and types: `just mod` at 19085335 -> `85 pass 0 fail`, including `a paused batch with crs_total 0 says no CR yet on its title line` and `a paused batch with crs_total 2 does not say no CR yet on its title line`. Diff of hooks/register.tsx and types/index.d.ts read: `crs_total?: number`, title `<batch>  none yet<budget> · paused, no CR yet`, body `No CR yet.` dimmed, no gauge when spent null.
10. Web board: diff read at the head: `batch.no_cr_yet` and `batch.spent_none_yet` in en-batch.js and fr-batch.js with the spec's wording; `noCrYet` in semantics.js; batch.js shows `empty(t('batch.no_cr_yet'))`; home-batch.js replaces the bar by one line, Spent `none yet` with no meter, sign `—` not late; DESIGN.md updated; test_the_board_words_of_a_batch_with_no_cr_are_shipped passes. Not rendered in a browser (no capture).
11. Cards and docs: grep at the head finds the empty-batch wording in concepts.md (l.271), foreman.md (l.776 heartbeat), hosts/claude-code.md (l.79), hosts/copilot.md (l.60), chief-of-staff.md (`none yet: no CR`, `open [<prepared-folder>…]`), docs/batch-lifecycle-texts.md and the SVG. Agent files untouched (not in the diff).
12. Scenario leg: in the diff (scenario/run_scenario.py +36); proven by the pipeline scenario job, green at the head per the Driver's brief (not re-run by me).
13. PR 335 description (read with gh at the head 19085335, base CR-374's branch): renders, Summary/Deliverables/Changes match the diff against the base branch (32 files), Known gaps names the pane screenshot and the unrun local scenario leg. No image attached. Role names: none outside Internal references. The Test plan boxes still hold `<sha7>` placeholders for gates, Review, Verified and CI: left for the Driver at hand-back, not judged a failure now. Review note: `r2 approved at 7bf2bb0` and `move 7bf2bb0..487447a (conflict) inspector approved at 19085335...` found in `log CR-369`.

## Verdict
14. Description pass at 19085335 (gh pr view 335 body): Summary, Deliverables, Changes match the 32-file diff (crs_total, cost_cause, record_born_paused, none yet found in the diff); Test plan SHAs 1908533 right; `gh pr checks 335`: 5 pass; Review note `inspector approved at 19085335` in log; Known gaps complete (pane screenshot, local scenario, no-transcript close); no internal reference outside Internal references. Clean.

## Verdict

VERIFIED
