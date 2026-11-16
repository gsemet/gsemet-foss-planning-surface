# Verification of CR-186 at 718c9ed

Verdict: VERIFIED.

## Evidence
- By hand: not run separately. The scenario's section 12b runs the same commands on a real scratch
  batch; its checks are the by-hand proof (evidence/scenario-12b-checks.txt): ready refusal naming
  `take --note ... then hand back again`; `order note` naming the `take`; `take --note` reopens to
  working with no round and the note/take event; commit with no `ship` refused alone, with and
  without `--no-gate`; after `ship` the gate and verdict are wanted; a full re-hand-back in the same
  round; a second blocked hand-back refused with the `take`. All `[x]` for github and gitlab.
- CI on PR 124 at 718c9ed: just check on ubuntu, macos, windows pass; just scenario (ubuntu) pass.

## Diff against the spec
1. handback ready/blocked refusal: matches the spec text, uses stored id, exit 2, other statuses unchanged.
2. Head check: matches (prefix compare, alone, release excluded, applies with --no-gate). It replaces the
   old mixed head line rather than adding one (disclosed); it sits after the `pr` check and before the
   dirty/gate checks. Scenario 12c updated to the new wording, not loosened.
3. order note line: matches.
4. foreman.md and 5. driver.md: all listed edits present (take-only rule, resume then new Driver, blocked
   keeps new Driver; Driver refusals, `taken back:` note, resumable end).
5. Scenario steps 1-7 present.

## Known deviations (in the PR body / accepted)
- `take` refuses a CR with an agent recorded, so card and scenario clear the agent first (card adds the
  `agents set <cr> - --epoch <n>` step before `take`). PR body "Autonomous decisions" mentions the ship
  SHA; the agent-clear deviation is in the commit, worth one line in the body.
- ship stores full SHAs (disclosed).

## Nits (non-blocking)
- driver.md: one line in "Your end" runs past the card width and a short wrapped line was left.
- foreman.md: the `order merged` bullet has a line over ~100 characters.
- The resume of the Driver is card behaviour, unproven until the eval run.
