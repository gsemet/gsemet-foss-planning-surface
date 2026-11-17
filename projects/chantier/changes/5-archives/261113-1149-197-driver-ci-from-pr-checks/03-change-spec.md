# A Driver's claim about CI comes from the forge's checks at the pushed head

## Goal

A Driver never again says "no CI" while a check runs. In real-direct run 1 (2026-11-12, PR 137;
`evals/results/real-direct-2026-11-12-run1.md`, finding 1) three Drivers wrote "no CI" in their
hand-backs and PR bodies while a `test` check ran green on every PR. The claim came from
somewhere other than the forge, most likely from a look taken before the forge had registered the
checks. After this change, every claim a Driver makes about CI (running, green, red, or none)
comes from the forge's list of checks for the PR, read at the head the Driver pushed, and "no CI"
needs a second empty look taken a minute after the push.

This is a card change only: no CLI change, no agent file change.

## What changes

### 1. `skills/chantier/references/driver.md`, "Your means", the `CI:` bullet (lines 109-120 today)

The bullet keeps everything it says today (do the work that needs no CI first, one long wait with
the forge's watch in a background shell, no look in between, how a result is judged, the flake
note, the 3-hour limit). It gains the rule below, written in the card's style (short sentences,
plain words). Because it sits in "Your means", it binds every Driver that pushes: CR, stack and
release Drivers alike. For a stack driver, which opens no PR, "the PR" is the PR whose branch it
pushed (the top of the stack, where the heavy CI runs).

The rule, in substance:

- **The only source.** Any claim about CI (running, green, red, or none) comes from the forge's
  list of checks for the PR at the pushed head: `gh pr checks <pr>`, `glab ci list`, or the
  forge's equivalent. The project's files (a workflow folder or its absence), its rules, an
  earlier Driver's note and a guess are not a source.
- **The project's rules do not replace the look.** Even when the project's rules say the project
  has no CI, the claim comes from the forge's list; the rules only say how to judge what the list
  shows. A list that contradicts the rules (a check listed where the rules say none, or none where
  the rules say some) is said in a `note`.
- **The head first.** Before it reads the checks, the Driver confirms that the PR's head on the
  forge is the head it pushed (`gh pr view <pr> --json headRefOid`, or the forge's equivalent).
  Checks listed for an older commit prove nothing about the pushed one.
- **"No CI" needs two looks.** An empty first look, or a watch that ends at once because no check
  is reported yet, is not a conclusion: a forge registers its checks a few seconds after the push.
  "No CI" is said only when a second look, taken a minute or more after the push, still lists no
  check at the same head. The minute is filled with the work that needs no CI result
  (`pr-body.md`, the archive's `delivery.md`, the notes), which the bullet already puts first.
- **The one bounded wait.** When that work ends before a minute has passed since the push, the
  Driver runs one bounded wait, once, until a minute after the push (for instance a single `sleep`
  of the seconds that remain), then takes the second look. The card names this as the exception
  to rule 8 of `concepts.md` ("No `sleep`, no polling loop"): at most once per pushed head, never
  a loop. A second empty look concludes "No CI"; a second look that lists checks leads to the
  normal long wait.
- **What the note says.** The `note` that says what CI showed ("Say what CI showed in a `note`",
  already in the bullet) names the command it ran and the head (seven characters) it read at, for
  instance `CI: gh pr checks 12 at abc1234: test pass` or `CI: no check listed at abc1234 (gh pr
  checks 12, two looks, the second a minute after the push)`.
- **What the PR body says.** The PR body's CI box says the same thing in the template's words
  (section 3 below).

Keep the bullet's existing ban on looks during the long wait ("no `gh pr checks` or `glab ci`
look in between"): the two looks of the "no CI" rule happen before the long wait starts, or
instead of it when no check is listed; the Driver writes the text so the two do not read as a
contradiction.

### 2. `skills/chantier/references/concepts.md`, "Rules", rule 8

Rule 8 says "No `sleep`, no polling loop: a wait is the forge's own watch, in a background shell."
It gains a short pointer to the one exception, in substance: "except the one bounded wait before
a second CI look that [driver](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/driver.md), `CI:`, names". Nothing else in the rule changes.

### 3. `skills/chantier/references/pr-template.md`, the template's Test plan

The last Test plan item, today `- [ ] CI green at \`<sha7>\``, gets the form for a PR whose forge
lists no check:

- When the forge lists no check at the head (after the two looks of section 1), the box stays,
  checked, and reads `No CI: no check listed at <sha7>`.
- It is never deleted and never written "CI green" in that case.

Put this in the item's HTML comment in the template (as the other items carry their alternatives,
e.g. `<!-- or "No CI: no check listed at <sha7>" when the forge lists no check at the head -->`),
and, if the Driver judges it reads better, one line in "The rules" next to the rule that each
proof names its SHA. The Inspector's audit list ("The audit") is unchanged.

### 4. `evals/SCORECARD.md`, one new row

Add one row after J24, with the next free id, `J25`, marked by hand (no automated audit):

| id | rail | from | where seen | how marked |
| --- | --- | --- | --- | --- |
| J25 | a Driver's claim about CI comes from the forge's list of checks at the pushed head: a "no CI" follows a checks call made after the push, at the PR's head, with a second look a minute after the push still empty (one bounded wait at most, never a loop); the note and the PR body's CI box name that head | driver.md, pr-template.md, concepts.md rule 8 | full, real-foreman, real-direct, claude-planted | by hand |

`evals/kit/audit.py` is not changed: it reads the rows at run time and a `by hand` row needs no
check there.

## Decisions carried from the answers

1. The forge's list at the pushed head is the only source, even when the project's rules say the
   project has no CI; the rules say how to judge the list; a list that contradicts them is said in
   a `note` (section 1).
2. "No CI" only after a second look, taken about a minute after the push, still lists no check;
   an empty first look or a watch that ends at once is no conclusion (section 1).
3. The Driver confirms the PR's head on the forge equals the head it pushed before reading the
   checks, and its note names that head (section 1).
4. The rule binds every Driver that pushes (CR, stack, release), by sitting in the common `CI:`
   bullet (section 1).
5. With no check listed, the PR body's CI box stays, checked, and reads
   `No CI: no check listed at <sha7>`; never deleted, never "CI green" (section 3).
6. The Verifier's card (`skills/chantier/references/worker.md`, "Verifier") does not change: the
   CI line of the description is already a claim it judges, reading the forge's list itself, and a
   claim with no proof is already `NOT VERIFIED`.
7. The CLI does not refuse a `handback ready` with no CI reading: it runs no forge command and
   knows no role.
8. The eval part is one `by hand` row in `evals/SCORECARD.md`, no automated audit (section 4).
9. When the Driver's other work ends in under a minute after an empty first look: one bounded
   wait, once, until a minute after the push, then the second look; a named exception in the
   `CI:` bullet, which rule 8 of `concepts.md` points to; never a loop; a second empty look
   concludes "No CI" (sections 1 and 2).

## Out of scope

- Any CLI change (`skills/chantier/scripts/cli/`): `handback` keeps checking the gate and the
  verdict only; the preflight allow list in `commands.py` is not touched.
- How a CI result is judged (a skipped job, a job red on the default branch, an infrastructure
  re-run, a flake, the 3-hour limit): unchanged.
- The Verifier's card and the Inspector's audit in `pr-template.md`.
- The agent files of both hosts (`agents/`, `com.github.copilot/agents/`): the contract lives in
  the card.
- An automated audit of the claim in `evals/kit/audit.py`.
- The host cards (`skills/chantier/references/hosts/*.md`).
- Any other change to rule 8 than the pointer.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes: the change touches cards (AGENTS.md: a change to the cards passes it
  before its PR).
- A read of the diff shows, in `driver.md`'s `CI:` bullet: the only-source rule, the
  rules-do-not-replace-the-look rule with its `note`, the head check before the read, the two
  looks with the second a minute after the push, the one bounded wait named as the exception to
  rule 8 (once, never a loop), and the note naming the command and the head; nothing of the
  bullet's existing text removed.
- `concepts.md` rule 8 carries the pointer to that exception and nothing else new.
- `pr-template.md`'s Test plan carries `No CI: no check listed at <sha7>` as the form of the CI
  item when no check is listed.
- `evals/SCORECARD.md` has the row J25, `by hand`, and the kit's audit (run as
  `evals/README.md` says) still reads the scorecard without an "UNKNOWN RAIL" or a missing-row
  error.
- No file under `agents/`, `com.github.copilot/agents/`, `skills/chantier/scripts/` or
  `evals/kit/` changes.
