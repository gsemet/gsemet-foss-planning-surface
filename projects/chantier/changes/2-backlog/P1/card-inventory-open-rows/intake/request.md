# Follow-up of the card rework: open rows and open points

## Resume here (written 2026-11-26, at batch-31's end)

Asked by the owner, verbatim: « Met tout ce qu'il faut pour reprendre en P1 » (put everything needed to resume in P1).

### Where batch-31 stands

- 40 CRs merged; main at 4d12a5b, CI green. The batch is paused, cost $492 of $800.
- It closes only on the owner's word: `close --batch batch-31`, then `--yes`, then the worktrees and branches that command lists. Archive the Foreman and Chief of Staff sessions after the close, not before (the close prices the Foreman's transcript).
- A copy of the batch's journal, which the close deletes and git does not hold: folder `chantier-batch-31-journal`, beside the main checkout on the owner's machine.
- Copied into this item: CR-510's and CR-511's known gaps, the retro points kept, the owed items and the leftovers. The other merged CRs' known gaps were not copied: 35 of the 40 CR folders hold them in `work/pr-body.md` (`4-batch/3-done` now, `5-archives` after the close); for CR-469, 475, 476, 502 and 507, which have no such file, read the PRs (#445, #451, #453, #484, #487 of gsemet/chantier).
- Decisions taken for the owner while they asked to be asked nothing are marked "to confirm by the owner" in the CRs' `02-answers.md` (5-archives after the close).

### What is in P1, in order (nothing starts without the owner's word)

1. `card-inventory-open-rows` (this item): "Do this first" below, cards and CLI usable. It is the first work of the next batch.
2. `simplify-cards-and-prompts`: the rework program and its answers.
3. `512-sc26-card-gates-pytest`, `513-sc27-card-gates-process`, `514-sc28-cards-real-run`: the parts of the program not done.
4. To specify again on the reworked base, their interview answers kept (all were in 3-ready): `415-eval-operator-from-phone`, `autonomy-command`, `batch-takeover`, `context-limits-of-the-drivers-configurab`, `docs-sphinx-rtd`, `docs-style-guide`, `evals-rework`, `shortcut-commands`, `surface-getting-started`, `test-ceiling-decision`. The owner, 2026-11-26, verbatim: « tu vas annuler les specs de tous les autres mais eviement pas perdre les reponses que j avais donnee en interview. Avec le rework en cours il faudra refaire la specification de tout, et on fera ca dans un batch 32. »
5. `tui-live-batch-kanban`: a new request, its second bullet unanswered.

Not moved: the other ideas of 1-inbox, among them `run-the-long-gate-on-main-after-v0-15-1`, the follow-up of CR-463's waived long gate.

## Do this first: make the cards and the CLI usable (added after batch-31's end, 2026-11-26)

Asked by the owner, verbatim: « Je veux savoir si tu as fini le rework demandé. S'il reste du travail on peut le mettre dans ce batch ou attendre de le clore et réouvrir un nouveau mais un faut que les cartes et les CLI soient utilisables » (is the rework finished; what remains can go in this batch or a new one, but the cards and the CLI must be usable). Chief of Staff's reading, to confirm by the owner: usable cards and CLI is the first requirement of the next batch.

1. **Blocker, other projects.** The version is still 0.15.1. uv's cached build of the main checkout (built 2026-11-25 22:38) lacks the card swap's source changes (commit 7714288e, 19 files) and still names removed card files: `driver.md` (commands/access.py, commands/facts.py), `foreman-stack.md` (stack_shape.py), `reload-rules.md` (status/ready_line.py), `startup-core.md` and `startup-manifest.json` (driver_prompt.py). Found by reading the cached files, not by running them; that uv reuses this build while `pyproject.toml` is unchanged is expected, not tested. Done when: the version is bumped and a project in plugin mode is shown to run on the new cards.
2. **Cards against CLI** (retro point 6 below). Seen again on 2026-11-26: `help <topic> --batch <batch>` is refused. The other cases were not re-checked.
3. **Real trial.** No batch has started from scratch on the new cards (CR-514, backlog P1).

Follow-up of CR-511 (batch-31): close the card inventory rows it leaves open.

Asked by the owner, 2026-11-26, verbatim: « Merci. Applique en coupant pour finaliser le batch rapidement quitte à corriger après » (apply it, cutting so the batch is finished quickly, even if things are fixed afterwards). Chief of Staff's reading, to confirm by the owner (CR-511, 02-answers.md 9; orders O-180 and O-181).

CR-511 restores only the serious lost rules. To do afterwards:

- every inventory row left open in the list CR-511 commits (at its round 1: 332 rows with no compliant home, 57 of kind a, 139 inferable without a quiz case, 136 others; its work/r1-worklist.md), then drop the list the inventory test accepts;
- the quiz cases not written;
- card budget overruns and raised brief-byte ceilings CR-511 names;
- the non-blocking Known gaps of the PRs of CR-510 and CR-511.

CR-512, CR-513 and CR-514 are separate items, already in the backlog (P1). Not grilled.

## Added on 2026-11-26: every open point, in one CR treated at the end

Asked by the owner, verbatim: « J'ai mergé car tu m'as dit qu'elle était prête à merger. Fini rapidement le reste du batch / Tes points met les dans une CR que l'on traite à la fin » (I merged because you told me it was ready to merge; finish the rest of the batch quickly; put your points in one CR that we treat at the end). Chief of Staff's reading, to confirm by the owner: one follow-up CR, after batch-31, not added to the running batch.

### Points the Chief of Staff raised

- A CR that must not merge alone was announced with "ready to merge" next to "do not merge", and the owner merged it (CR-510). Wanted: while a CR of a stack waits for the others, neither the CLI's line nor the steering session's message reads "ready to merge"; the user gets one instruction.
- The board runs a cached build of the CLI that has no `brief` command, while the new cards call it (newer cached builds have it). Check that another project's sessions, in plugin mode, always get a CLI that matches the cards they read from chantier's checkout. Not verified.
- A running Driver blocks the main checkout's fast-forward when a lower CR of the stack is merged early (its cards and CLI are read live from that checkout).
- CR-511's own Known gaps: below, added at its hand-back.

### CR-510's Known gaps (https://github.com/gsemet/chantier/pull/488), as posted

- Quiz of the roles on the new cards, not run: skipped on the owner's word, 2026-11-26: `just quiz coder conflict-resolver cr-driver debugger demo-explorer release-driver stack-driver verifier --max-usd 40` and `just quiz chief-of-staff foreman griller --model claude-sonnet-5-5 --max-usd 45` (only the free `--plan` form was run).
- Old-card quiz baseline to compare against, not run: skipped on the owner's word, 2026-11-26: the same two commands with `--cards ea11a9e0` (the last head with the old set), then each new run with `--against <that results file>`.
- No transcript of a real Claude Code session showing the reload message after `/compact`: only the hook's own tests ran.
- Unproved in a real Copilot session: briefs build for every role on that host, its host rows stay untested, and it has no hook, so the reload message and the write guard are inert there.
- On Claude Code, a worker configured with a generic agent gets a brief with its card and the floor but without the extra generic-agent contract lines, which are printed only where chantier itself starts a role generic; this change does not alter that, and no test covers that Claude Code case.
- Real run not done: no real batch has run on these cards.
- Launcher not switched: it leaves the CLI running after its stop on Windows.
- The board Griller does not read the floor.
- Some new cards still describe output the CLI no longer prints (a worker's opening lines, the worker `writes:` line, the prompt skeleton of `take` and `order qa`): `topics/cr-workers.md`, `concepts.md` ("The prompt" and its template), `topics/trouble-worker.md`, `foreman.md`, `topics/direct-mode-p2.md`, `topics/direct-mode-switch-p4.md`, `topics/qa-order.md`, `topics/order-verbs-p1.md`, `topics/stack-run.md`, `topics/wakes-p1.md`. Card content was not rewritten here; these sentences should be fixed before a real batch runs on these cards.
- The new refusal paragraph of the worker agent files was not tried with a real agent.
- A worker started with a prompt that names its card and no brief is accepted, but two sentences of its agent file, about the brief that the prompt names, do not read true for it.
- The test that ties that paragraph to the short prompt of `brief` was only seen passing: it was not made to fail on a changed brief name.
- `AGENTS.md` says `brief` reads the record and the planning folder only; it now also reads the project's instructions for the review steps. `AGENTS.md` is unchanged here.
- Review steps are read when `brief` runs, while two docs pages say a running batch keeps the team it started with.
- The generic agent's contract heading still says "after the opening lines", though it is now in the worker's brief.
- Cards over their size target, in bytes (target): `release-driver.md` 3,809 (3,072), `spec-writer.md` 1,667 (1,500), `coder.md` 1,603 (1,500), `verifier.md` 3,112 (3,000), `demo-explorer.md` 1,612 (1,500), `spec-critic.md` 1,572 (1,500), `retro-critic.md` 1,565 (1,500).
- Nine host topics are over the 1,500-byte target since the added link line, in bytes: `host-turn-end.md` 1,578, `host-auto-fix.md` 1,571, `host-surfaces.md` 1,561, `host-auto-mode-trials.md` 1,558, `host-allow-add-lines.md` 1,540, `host-configuration.md` 1,524, `host-allow-rules.md` 1,522, `host-auto-mode-steering.md` 1,520, `host-allow-broad.md` 1,509.
- The Drivers' briefs are over their start targets: CR 9,773 (6 KB), stack 9,179 (6 KB), release 9,531 (5 KB), QA 6,032 (4 KB).
- Two data files kept byte-identical still hold removed file names: `hosts/claude-code.json` (`driver.md`, `session-start.md`) and `hosts/copilot.json` (`session-start.md`, `foreman-lost-driver.md`).
- Wording of the old set not found in the new one: some sentences of the sync offer, "A release with no PR yet is no anomaly", the Foreman's pointer to `help session-shell`; "say it once to the user as printed" became "offer the restart once".
- Stale text left as found: some evaluation scorecard rows cite the host card for rules that now live in rows or topics, one sentence of the Claude Code tutorial, `AGENTS.md`'s mention of a removed card, the direct-mode runbook's "unproved" list; some evaluation links now go to topics that do not keep the old section titles.
- A `foreman:`, `chief-of-staff:` or `griller:` entry in the project's `## chantier` section would print as a review step, though only a name that is no built-in role should.
- The CR Driver's brief size budget in its test is 9,900 bytes, where rounding the measured 9,773 up gives 9,800.
- One sentence of `evals/README.md` still names a removed test.
- The new hook test case reads only the test's own constants; the cases next to it tie them to what the hook sends.
- The type checker's warnings on `hooks/register.tsx` were there before.
- The new tests were not run against the previous code.
- `docs/proofs/claude-code.md` still holds a local home path, as it did before this change.
- `just test` was already far above the time budget of `AGENTS.md` before this change.
- **UNVERIFIED:** the test suite's added time stays within the expected 3 seconds: one pair of runs on the same machine gives 165.0 to 167.2 seconds of wall time (157.8 to 162.5 as the test runner counts), while runs of the new head span 139 to 265 seconds.

### CR-511's Known gaps (https://github.com/gsemet/chantier/pull/489), as posted at its hand-back

- 329 rows stay open (62 of kind a, 139 inferable with no quiz case, 128 others), listed in
  `docs/proofs/cards-inventory-open.tsv`. The goal that every row has a resolving home is not met.
  Only serious lost rules were restored, on the owner's choice to finish quickly.
- The 62 open kind-a rows were read one by one against the new cards; the other 267 open rows were
  judged from their wording, not searched one by one.
- A sample suggests up to about one in ten automatically mapped homes of non-protective rows may not
  hold its rule; no test can see this.
- Reported by review on an earlier state and not changed since: some homes point at text that does
  not state the rule (W-001, W-038, W-076, W-108, W-156, W-238, W-283, H-119, H-120, C-1220, C-1223,
  C-1535, C-1536, FM-474, FM-475); H-173 and H-217 resolve only in code docstrings; the trigger
  `none (rare)` was set from the home, so the rare-rule test cannot fail on those 129 rows; the role
  column mixes spellings.
- The stack driver card's context hand-back points to a host means that names direct mode only (it
  already did for another line), and its answer-every-message line names only one of the two message
  tags the topics use.
- The 539 kind-a rows that have a home are checked by quote only (the text is still where the row
  says), with no behaviour check yet; the other 62 are open. The owner lists (601 kind-a rows) are in
  the inventory and are not repeated here. Rows homed in the incidents file: H-439, H-989, H-1040,
  H-1041, H-1059, H-1069, H-1191, H-1192, H-1203, H-1212, H-1306, H-1551; no row is homed as
  inferable.
- 20 of the 36 hand-over checklist items end as known gaps, each with its reason in the inventory,
  among them: the scorecard rails J11 and J22 are not reconciled with the new wording, one sentence
  of CONTRIBUTING.md is not aligned, and no new quiz case was written.
- H-1360 (a rule dropped by default, pending the owner's confirmation) needs that confirmation.
- Card size targets exceeded by this change, in LF bytes (before to now, target): cr-driver 3749 to
  5066 (4096), stack-driver 3783 to 4821 (4096), release-driver 3809 to 4685 (3072, already over),
  foreman 3997 to 4426 (4000), conflict-resolver 1494 to 1535 (1500). Already over and unchanged,
  their sizes not listed here: coder, demo-explorer, retro-critic, spec-critic, spec-writer,
  verifier.
- Brief byte ceilings raised in `test_brief_bytes.py`: cr-driver 9900 to 11100, release-driver 9600
  to 10500, stack-driver 9200 to 10300, qa-driver 6100 to 6300, foreman 22200 to 22600.
- Not run: skipped on the owner's word, 2026-11-26: `just quiz <role> --plan --max-usd 10`,
  `just quiz <role> --cards f08cf41f2c80e2e4f7ab834adc3dc06820ae7f93 --max-usd 10 --save old-<role>`
  and `just quiz <role> --max-usd 10 --against <the saved old results>`, for each role under
  `evals/quiz/` (the session roles add `--model`). So no result shows the new cards answer as well
  as the old ones.
- Real run not done (a later, separate campaign).
- The seconds the new test adds to `just test` were not measured as two runs before and after; the
  test file alone took 2.8 s of pytest wall time at an earlier state.

## Batch-31's retro, the points its critic kept (not filed one by one)

- [project] Flaky tests: `test_serve_webui` failed its port walk in macOS CI on CR-491, CR-492 and CR-493, and the board-griller moved-folder test failed once on CR-481: fix or isolate them.
- [chantier] Card rewrite CRs far past their budget (CR-507 15 rounds and $135.54, CR-510 $54.57, CR-511 $28.98; CR-505 and CR-507 spent their 3 rounds before the last part; batch budget raised 400, 600, 800; CR-512..514 dropped to the backlog): the specification splits such a CR into parts that each fit the round limit.
- [chantier] PR descriptions repeatedly came back NOT VERIFIED, many on the description alone (CR-467, 473, 480, 490, 507, 510, 511), each costing another Verifier run: the CLI writes the body's factual parts (gates, heads, gaps) from the record.
- [chantier] Workers or Drivers acted outside their role or folder (stray files outside `writes:` on CR-474, Verifiers changing into the CR folder on CR-507 and CR-510, a Driver editing code with no Coder on CR-477 and CR-497): enforce it by the write guard and a CLI rail, not card lines.
- [chantier] CRs labelled ready to merge while their own gaps said not to merge them alone (CR-505, 507, 510), and the owner merged CR-510 while CR-511 still worked, against the order that every Driver finish first: the CLI words a held state instead of ready to merge.
- [chantier] Cards and CLI disagree after the swap (`help <topic>` refuses the `--batch` of the brief's CLI line; `next` asks for a stack ask while `judge` words an alone ask; `push`'s `next:` line and the card order differ on the gate; the watcher outlives the heartbeat in `wakes-p1` and is stopped by `wakes-p2` and the Foreman card; the PR template's "nothing follows </details>" clashes with the host's attribution line; `ship` and closing disagree on a description-only NOT VERIFIED; stale sentences quoting removed CLI output, O-175 and O-176): tests that tie card sentences to the CLI's output.

The dropped points: `retro-dropped.md` beside this file.

## Still owed from batch-31

- H-1360: a rule dropped by default, waiting for the owner's confirmation.
- Screenshots of the board pane from a real session for CR-481, CR-482, CR-483 and CR-486 (the Foreman's final report).
- Quizzes and evaluation campaign: the owner runs them later.

## Housekeeping (counted on 2026-11-26; delete nothing without the owner's word, and check first for unsaved work)

- 48 git worktrees besides the main checkout (24 of batch-29), 2 of them removed by batch-31's close.
- 50 local branches whose remote branch is gone; 3 stashes.
- 3 old draft pull requests: #386, #347, #346.
- Untracked in the main checkout: `commands.py`, `concepts.md`, `state.py`, `test.md`, `.agents/`.
- The evaluation campaign's folder and plugin entries set up on 2026-11-26.
