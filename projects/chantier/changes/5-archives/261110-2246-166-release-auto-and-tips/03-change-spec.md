# Change Specification: release "auto" and contextual tips

## Goal

The user does not know what chantier can do. Two changes make the Chief of Staff show it at the
right moments, without noise:

1. **Release "auto".** While a release runs, the Chief of Staff offers: say "auto" to switch this
   release to auto. In auto, the version PR is merged, the tag pushed and the GitHub release
   published without asking the user. Announcements (posts) stay drafts for the user.
2. **Contextual tips.** One short tip line at four key moments: first use, after a `status`, at
   the end of a batch, during a release. At most one tip per moment and per session. "plus de
   conseils" (no more tips) turns them off for the session.

## Decisions carried from `02-answers.md`

| # | Decision (grill of 2026-11-10) | Where it lands below |
| --- | --- | --- |
| 1 | "auto" covers merge of the version PR, tag and publication of the GitHub release, without asking; announcements stay drafts for the user | Area A |
| 2 | Key moments: first use, after a `status`, end of a batch, during a release; one short line, at most once per moment and per session; "plus de conseils" turns them off for the session | Area B |

Nothing else was decided; the points left open are in "Open questions" at the end. Where this
specification needs an answer to one of them to be complete, it states the recommended answer and
marks it **(pending Q<n>)**: the Driver implements the recommendation unless the user's answer,
recorded in `02-answers.md` before the batch, says otherwise.

## Area A: release "auto"

### What exists today (no change needed in the CLI)

The CLI already holds the mechanics "auto" needs; this CR adds **no CLI code** (AGENTS.md: a new
CLI tool comes only from measured token cost).

- `order grant <release-cr> --note "releases=<n> fixes=on|off budget=<usd>"`
  (`skills/chantier/scripts/cli/src/chantier/commands.py`, `order` kind `grant`;
  `rails.py` `parse_grant`, `check_grant`).
- `release go <cr> --note "<action>"` (`rails.py` `release_go`) answers `go` without an approval
  while `grant["autonomous"] > grant["published"]`; `release published` raises `published` by one
  and ends that allowance ("the grant ends with its number of releases", scenario §14).
- `check_grant` refuses autonomy without a batch budget ("a release grant needs a batch budget").
- `handoff <release-cr>` prints `grant: up to <n> releases without asking (<k> published); …`
  (`commands.py` `grant_line`), which gives `<k>`.
- The Foreman merges the release PR after `release go … "merge <pr>"` says `go` (foreman.md), and
  sends a blocked release CR back to a Driver once an order (a grant included) lifts its block.
- The Release driver card (`driver.md`, "Release driver") already says the announcement thread is
  never posted by an agent: it stays a draft (`note --draft <path>`) for the user.

So "auto" for this release is: `order grant <release-cr> --note "releases=<k+1>"`, `<k>` being the
releases already published in this batch, read from `handoff <release-cr>`. Fixes are not part of
it: `fixes=` is left as it is (decision 1 names merge, tag, publication only).

### Changes in `skills/chantier/references/chief-of-staff.md`, section "Releases"

Add a paragraph after the grant sentence ("The grant is the user's: …"):

- **The offer.** While the release runs (from the start of the Release driver, after `order
  confirm`, or at once for a release alone in its batch, until `release published` or the CR
  ends), the Chief of Staff offers "auto" as the "during a release" tip (Area B): one line, the
  exact word to say, e.g. "💡 Say "auto" to let this release merge its version PR, tag and
  publish the GitHub release without asking; the announcement stays a draft for you."
- **On an approval ask** (`ask … blocked <release-cr> approval: <action>`): the question to the
  user lists "auto" as one of its answers, beside approving the one action (`order approve`).
  This is part of the question, not a tip line, so it holds even when tips are off and does not
  break "a message that asks a question carries no tip" **(pending Q1)**.
- **On "auto"** (the user's own word, any language, e.g. "auto", "passe en auto"):
  1. `$CHANTIER handoff <release-cr>`; read `<k>` from its `grant:` line.
  2. If the batch has no budget, ask the user for one, with a recommended figure, since the CLI
     refuses autonomy without it **(pending Q2)**; send nothing before the answer.
  3. `$CHANTIER order grant <release-cr> --note "releases=<k+1>[ budget=<usd>]"`, and record the
     user's word in the release CR's `02-answers.md` with the date ("Record at once").
  4. Send the order's line to the Foreman (direct mode: act on it yourself; a release CR blocked
     on an approval goes back to a Driver with `--note "auto: <the grant line>"`).
  5. Tell the user in one line what auto now does (merge, tag, publish, this release only) and
     what stays theirs (the announcement, posted by them; a fix, unless they grant it).
- "auto" covers **this release only**: the next release of the batch asks again. It never covers
  posting an announcement, starting or merging a fix (`fixes=` unchanged), the `order confirm`
  word, or a raise of the budget.
- Add one row to the "Entry points" table: `"auto" during a release` → `order grant <release-cr>
  --note "releases=<k+1>"`, budget first if none → Releases.

### Changes in `skills/chantier/references/driver.md`, section "Release driver"

One sentence, so the Driver's behaviour under auto is explicit and nothing new is posted:
"Under a grant ("auto"), `release go` answers `go` for the merge, the tag and the publication; the
announcement thread stays a draft, never posted." No other change: the Driver already calls
`release go` before each irreversible action, and the Foreman merges the release PR.

`agents/release-driver.md` and `com.github.copilot/agents/chantier-release-driver.agent.md` are
not changed (the contract lives in the card).

## Area B: contextual tips

### The rule (replaces the current Tips rule)

In `skills/chantier/references/chief-of-staff.md`, bullet **Tips** of "While it runs", and in
`skills/chantier/references/status-layout.md`, section "Tips", state the same rule:

- **When:** only at four key moments **(pending Q3)**:
  1. **First use:** the first-turn introduction (`session-start.md` §4), or the end of the `init`
     tour (`init.md` §5) when the session starts with it.
  2. **After a status:** a Progress report given on "status?", `/chantier:status`, or a report on
     a CR ready or merged.
  3. **End of a batch:** the Completion report at the pause, or the bilan of `close`.
  4. **During a release:** a report or answer while a release CR runs (Area A's "auto" offer).
- **How much:** one tip, one short line, starting with 💡, in the user's language, with the exact
  words to type; the last line of the message, after the **For you:** line. At most once per key
  moment and per session: a moment that already had its tip in this session gets none again. (This
  replaces "one or two tips" and "the end of a piece of work, a report, a quiet turn".)
- **Kept as they are:** a message that asks a question or reports a blocker carries none; a tip
  names only what chantier really answers, never a command the host refuses in this session, nor
  what the user cannot take from where they are ("Offering options"); a tip given and not used is
  not repeated in the session; the compact command advice follows its own Compacting rule and is
  not a tip.
- **Off:** "plus de conseils" (or the same in any language: "no more tips") turns tips off for the
  rest of the session; the Chief of Staff acknowledges in one line and gives no tip line after it.
  A new session starts with tips on. Area A's "auto" answer in an approval question is not a tip
  and stays **(pending Q1)**.

### The tips, by moment (examples, judged freely)

Replace the current examples list in `chief-of-staff.md` with one list per moment. Each names
only what exists today; the Chief of Staff picks the one that fits, or another true one.

- **First use:** "init" for a guided tour (the existing "new here? say init for a guided tour"
  line of `session-start.md` §4 is this moment's tip when the project has no planning folder);
  "file this: …"; "which agents and models?"; "use my agent X as the coder".
- **After a status:** "what did it cost?" (once a CR has spent); `/chantier:status` from any
  session, for the table at once; `/chantier-board` to show or hide the CR board (Claude Code only,
  never on Copilot); "I merged #<n>"; "more rounds for CR-<n>"; "run a QA on <what>" (`order qa`).
- **End of a batch:** "close the batch"; "add <slug> to this batch"; "why did it cost that?"
  (`cost --explain`); "release v<x.y.z>"; "run what is in 3-ready", when that folder holds CRs.
- **During a release:** "auto" (Area A); the draft's link to review as soon as `status` shows it.

### Other cards

- `skills/chantier/references/session-start.md` §4: one sentence saying the introduction's last
  line ("new here? say init…") counts as the first-use tip, and that tips follow the Tips rule of
  the Chief of Staff's card.
- `skills/chantier/references/init.md` §5: after "Phrases to say", one sentence: the tour's end is
  the first-use moment; its phrases stand for that moment's tip, so no 💡 line is added there.
- `skills/status/SKILL.md`: no change; it reads `status-layout.md`, which carries the rule.
- The cards keep naming no host tool (`test_structure.py`,
  `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`): the compact command is still
  named only through the host's reference.

## Out of scope

- Any CLI change (`rails.py`, `commands.py`, `cli.py`): the grant exists.
- A persistent "auto" across releases or batches, or a project setting for it (the user's
  `AGENTS.md` may still say what it wants; the project's rules rank above the cards).
- Posting the announcement thread: only the user posts.
- Fixes under the grant (`fixes=on`), the budget raise, the `order confirm` word: unchanged.
- Remembering "plus de conseils" beyond the session, or a per-user record of tips given.
- Changing the agent files of any role, the hooks, or the board.

## Evidence

- `just check` passes (Linux, macOS, Windows): structure tests, including the no-host-tool check
  on the edited cards.
- `just scenario` passes before the PR (cards changed, per AGENTS.md). Its §14 already proves the
  mechanics "auto" relies on: a grant without a budget is refused; `releases=1 … budget=5` lets
  `release go` answer "without asking"; the Foreman merges the release PR under the grant; the
  grant ends at its number of releases. Add one check in `scenario/run_scenario.py` §14 only if
  the Driver finds a gap: "auto" mid-release on a CR blocked on `approval:` — `order grant <rel>
  --note "releases=<k+1>"` sends the blocked release back to a Driver and the next `release go`
  answers `go`.
- A reading of the diff against this specification: the four moments, "one line, once per moment
  and per session", "plus de conseils", "auto" = merge, tag, publish for this release only,
  announcement draft, are each written in `chief-of-staff.md` and, for tips, in
  `status-layout.md`.
- PR description: the cards changed and the scenario result.

## Open questions

1. **Q1, "auto" in an approval question.** Tips are banned from a message that asks a question,
   yet the approval ask is the moment "auto" matters most. Recommended: list "auto" as one of the
   question's answers (not a tip line), and keep it there even after "plus de conseils". Agree?
2. **Q2, no budget.** The CLI refuses a release grant without a batch budget. When the user says
   "auto" and the batch has none, recommended: the Chief of Staff asks for one with a proposed
   figure before sending the grant. Agree, or should "auto" be offered only when a budget exists?
3. **Q3, only four moments.** The current card also gives tips at "the end of a piece of work, a
   quiet turn" (e.g. "file this" when an idea comes up in passing). Recommended: tips only at the
   four key moments; those others disappear. Agree?
4. **Q4, "publication" for other projects.** Decision 1 names the GitHub release. For a project
   whose procedure also publishes a package (npm, PyPI), recommended: "auto" covers every
   publication step of the project's procedure, announcement posts excluded. Agree, or GitHub
   release only?
