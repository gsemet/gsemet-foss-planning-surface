# Follow-up of the card rework: open rows and open points

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
- CR-511's own Known gaps: to add from its PR at its hand-back.

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
