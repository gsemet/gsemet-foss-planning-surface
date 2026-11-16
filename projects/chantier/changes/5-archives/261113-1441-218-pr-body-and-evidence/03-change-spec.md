# Change Specification: PR body says the gaps, keeps role names in place, and a board pane change shows a real screenshot

No tracker issue.

Source: `intake/request.md` (merged on 2026-11-13 from three batch-15 retro items:
`name-left-gaps-in-pr`, `pr-body-role-names`, `board-ui-screenshot`). The CR has no
`01-intent.md` and no `02-answers.md`: the user ordered it done from the request alone. Every
choice below that the request does not make is either one that changes nothing the user sees
(decided here, with its reason) or listed under "Open questions" with the default this
specification takes, so a Driver can implement the default and the Chief of Staff can confirm it.

## Goal, in the user's terms

When the user reads a PR that chantier says is ready, the PR tells them what it does not do:

1. A gap left on purpose (a cosmetic defect accepted, a claim not proven, evidence not captured,
   a part of the specification not done) is written in the PR body, and the "ready" line the user
   receives quotes it. Batch-15: PR 144 was reported "two cosmetic gaps left, the PR says so", and
   its body named none.
2. The PR body follows one clear rule on where an agent role name (Driver, Foreman, Verifier…) may
   appear, and the Driver checks the body against it before posting. Batch-15: CR-187, CR-203,
   CR-206, CR-213 and others failed the description pass on role names, some of them in PRs whose
   very subject was that role's card, which forced rewordings such as "the batch-steering card".
3. In this repository, a change to the CR board's pane carries one screenshot of the pane from a
   real Claude Code session. Batch-15: CR-202's Refresh button placement was "not provable
   without a real pane" and the PR merged with no image.

## What changes

### 1. Gaps left on purpose (`pr-template.md`, `driver.md`, `worker.md`, `foreman.md`, `chief-of-staff.md`)

**`skills/chantier/references/pr-template.md`**

- New visible section **Known gaps**, right after Autonomous decisions and before the
  `<details>` fold (default; see Open question 2). Layout rule becomes: Summary, Deliverables,
  Blast radius, Autonomous decisions and Known gaps visible, in that order; the fold unchanged.
- New rule bullet, "Known gaps": each gap the PR leaves on purpose, one bullet each, saying what
  is missing and why it was left (and, when known, what would close it). A gap is anything that
  is not done or not proven and that the PR knowingly ships that way: a part of the specification
  not delivered; a claim marked `**UNVERIFIED:**` (each such mark has its bullet here); evidence
  the plan named and the Verifier could not capture (`before-after.md` says why); a defect a
  review or the Verifier reported that the Driver accepted rather than fixed (a cosmetic defect
  included); a `STALE` proof is never a gap (it is fixed before the hand-back, as today). "None"
  when there is none; the section is never deleted. No internal reference in it.
- The template block gains the section, with its comment:
  `<!-- Each thing this PR leaves on purpose: not done, not proven, or a known defect accepted,
  one bullet with why; every UNVERIFIED claim has its bullet. Or "None". -->`
- The audit gains one numbered item (new item 10, or inserted after item 7 with the list
  renumbered; either, as the Coder judges): Known gaps is present, visible after Autonomous
  decisions; it has one bullet per `**UNVERIFIED:**` claim of the body and per gap the CR's notes
  record as left; "None" only when there is none. Audit item 1's section list and item 2's list
  of visible sections include it.

**`skills/chantier/references/driver.md`** (CR driver; the "Your end" bullet and the CR driver
section)

- The ready line quotes the gaps: when Known gaps is not "None", `handback <cr> ready <link>`
  is followed by `gaps: <gap>; <gap>`, each gap the bullet's first sentence as written in the
  posted body, in the body's order. With a draft: `handback <cr> ready <link> draft on <base>:
  waits for <what>; gaps: …`. No gap in the line that the body does not name, and the reverse.
- A Driver that judges something "left" (in a note, a hand-back, a reply to the steering session)
  writes it in Known gaps of `pr-body.md` first; a gap said anywhere else and absent from the body
  is a defect of the body.
- No CLI change: `handback` already accepts free text after the link
  (`skills/chantier/scripts/cli/src/chantier/commands.py`, `handback`, the `note` joined from
  `args.note`), and prints it in the `[driver <cr>→foreman] hand-back ready …` line. Decided here:
  this keeps the CLI out of a judgment it cannot make (what a gap is), per AGENTS.md's CLI scope.

**`skills/chantier/references/worker.md`**

- Inspector: no new text beyond the audit (it audits `pr-body.md` against the audit list, which
  now holds the Known gaps item).
- Verifier, the description paragraph: the posted description's Known gaps is one of the claims:
  each `**UNVERIFIED:**` claim, each evidence pair `before-after.md` says was not captured, and
  each claim of `verify.md` that failed and was accepted rather than fixed has its bullet; a
  missing one, or a Known gaps that says "None" while one exists, is `NOT VERIFIED`.

**`skills/chantier/references/foreman.md`** ("The user's boundaries" and the `asks` line list)

- The `ready` ask carries the Driver's gap text as the hand-back wrote it: `ready <cr> <link>
  gaps: …` (after `no long gate: <reason>` or the draft text when present). In a stack batch, the
  `stack-ready` ask carries each CR's gaps after its link: `<cr>=<link> gaps: …`. The Foreman
  invents none and drops none; a gap the Foreman itself sees and the body lacks sends the CR back
  to a Driver (`take <cr> --note "gaps: <what is missing from Known gaps>"`), with no ask.

**`skills/chantier/references/chief-of-staff.md`** (where it tells the user a CR or a stack is
ready: the series and stack bullets, and the plain `ready` ask)

- When it tells the user a PR or a stack is ready, it quotes each gap of the ask, in the user's
  language, next to the PR's link; with none, it says nothing about gaps.

`docs/use-cases.md` (line 134-138, the template's sections) names the new visible section.
`scenario/run_scenario.py` `BODY` gains `## Known gaps\n\nNone.\n\n` after Autonomous decisions,
so the scripted Driver's body follows the template (the scenario does not audit it; this keeps
it a faithful example).

### 2. Where role names may appear (`pr-template.md`, `driver.md`, `worker.md`)

**`skills/chantier/references/pr-template.md`**, the "No internal reference" rule and audit
item 3 (default; see Open question 1):

- An agent role of chantier (Chief of Staff, Foreman, Griller, Driver, Coder, Inspector,
  Verifier, Investigator, Debugger, Conflict resolver, Spec-writer, Demo explorer) is an internal
  reference when it names who did the work or how the PR was made ("the Verifier checked…",
  "the Driver chose…"): then it goes in Internal references only.
- A role name may appear in any section when it is a term of the project's own product: the
  diff changes that role's behaviour, card or agent file (as in chantier's own repository, where
  the roles are what the cards define). It is then a project term, defined on first use as the
  existing rule asks ("Define a project term on first use"). In a project whose product defines
  no such role, this never applies.
- A file path the diff changes (for instance `skills/chantier/references/driver.md`) may be
  named in Changes whatever its name.
- The template's first comment says the same in one line. Audit item 3 says: no CR name, batch,
  round or `.agents/changes/` path outside Internal references; no role name as the doer of the
  work outside it; a role name elsewhere only as a product term of a change to that role.

**`skills/chantier/references/driver.md`**, CR driver (the Push bullet where `pr-body.md` is
written and posted, and the CR driver section):

- Before each post of the body (`gh pr create --body-file`, `gh pr edit --body-file`, `glab mr
  create`/`update` with the file form), the Driver reads `pr-body.md` once against the audit
  list of the template in use, items on internal references (role names included) and Known gaps
  first, and fixes `pr-body.md` itself before posting. This is not a round and not a review: it
  does not replace the Inspector's audit or the Verifier's description pass. A failure the
  Verifier's description pass still finds is fixed as today.
- Decided here: a card rule, not a CLI check. The CLI cannot tell a role used as a product term
  from a role used as the doer (a judgment), and AGENTS.md admits a new CLI tool only from
  measured token cost; the failed description passes are counted in the retro but not measured.

**`skills/chantier/references/worker.md`**: Verifier, description pass: judges role names by the
same rule (a product term of a change to that role is not a failure).

### 3. A board pane change shows one real screenshot (this repository's rules)

This is a rule of chantier's own repository, not of the plugin: it goes in the project's rules,
which rank above the cards for chantier's own CRs, and changes nothing for a user's project.

- **`AGENTS.md`**: one bullet: a change to what the CR board pane draws (`hooks/register.tsx`'s
  pane, or `status.py`'s `STATUS.json` fields the pane shows) carries, in its PR's Deliverables,
  one screenshot of the pane from a real Claude Code session running the PR's head, captioned
  with the head's SHA (seven characters). Until the screenshot is there, the PR's Known gaps
  names it ("no screenshot of the pane from a real session"), so the ready line quotes it.
- **`CONTRIBUTING.md`** line 193-195 ("they do not draw a real pane, so open the board in a
  session once after a change"): says the same and points to the AGENTS.md rule, with how a
  session runs the PR's head (the means the Investigator proves; see below).
- Who takes it and when: default in Open question 3. With that default, the Chief of Staff, on a
  `ready` ask whose gaps name the missing screenshot, asks the user for one screenshot of the
  pane from a session running the PR's branch; on the user's file, it sends the CR back
  (`order note <cr> --note "evidence: <path of the image>"`, which the Foreman turns into `take
  <cr> --note …`); a Driver attaches it in Deliverables (`gh pr edit --attach`, as driver.md's
  evidence bullet says), removes the gap, runs the description pass and hands back ready.
- The Investigator settles, read-only, how a real session runs the PR's head without moving the
  main checkout (AGENTS.md: the main checkout does not change during work; a worktree's edit
  loads once merged), for instance a session started with the plugin loaded from the CR's
  worktree. What it finds goes in CONTRIBUTING.md; a means it cannot prove is said there as
  unproved, never guessed.

## Out of scope

- Any CLI change: no new command, no new check in `handback`, `ship` or elsewhere.
- `hooks/`, `types/`, the board itself: no change (so no `just mod`).
- The release PR's form and the stack driver's PRs (they keep their form, as today); the gaps
  rule covers a CR's PR.
- A project's own PR template: it ranks above `pr-template.md` as today; Known gaps and the role
  rule fill only where it is silent.
- Agent files (`agents/`, `com.github.copilot/agents/`): no change; the cards carry the rules.
- An automated screenshot of the pane by an agent (computer use or a harness): not added.
- The other batch-15 retro items.

## Evidence

- `just check` passes (structure tests: agents' bodies still identical, references present).
- `just scenario` passes (cards and scenario changed).
- Read-back of the cards: `pr-template.md` has the Known gaps section in the rules, the layout,
  the template block and the audit; the role-name rule in the rules, the template comment and
  audit item 3; `driver.md` has the `gaps:` text of the ready line and the check before each
  post; `worker.md`'s Verifier judges Known gaps and role names by the new rules; `foreman.md`
  carries `gaps:` in the `ready` and `stack-ready` asks; `chief-of-staff.md` quotes them to the
  user; `AGENTS.md` and `CONTRIBUTING.md` hold the board screenshot rule.
- A grep of the cards for "Known gaps" and "gaps:" shows each place above, consistent wording.
- This CR's own PR body follows the new template (Known gaps present; role names only as product
  terms of the cards it changes): it is the first example, checked by the Inspector and the
  Verifier.
- No visual change: no screenshot needed (the board is not touched).

## Open questions (behaviour the user sees)

1. **Where role names may appear.** Default taken: anywhere when the role is a product term of a
   change to that role (chantier's own card changes), never as the doer of the work, and file
   paths of the diff in Changes; otherwise Internal references only. Alternative: role names only
   in Changes (inside the fold) and Internal references, whatever the change. Which?
2. **Where the gaps go in the body.** Default taken: a new visible section "Known gaps" after
   Autonomous decisions, "None" when empty. Alternative: bullets inside Autonomous decisions
   (leaving a gap is a decision taken without the user), no new section. Which?
3. **Who takes the board screenshot, and when.** The agents cannot see the pane. Default taken:
   the user, before the merge, from a session running the PR's branch, on the Chief of Staff's
   ask; the PR names the missing screenshot as a gap until then and a Driver attaches it.
   Alternatives: the user takes it after the merge from the main checkout and attaches it to the
   merged PR (the PR merges with the gap named); or the missing screenshot stays a named gap and
   no one is asked. Which?
