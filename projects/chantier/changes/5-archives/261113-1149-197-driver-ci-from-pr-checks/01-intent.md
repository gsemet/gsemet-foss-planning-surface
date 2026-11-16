# A Driver's claim about CI comes from the forge's checks at the pushed head

## The problem

In real-direct run 1 (2026-11-12, PR 137) three Drivers reported "no CI" while a `test` check ran
on every PR. The claim came from somewhere other than the forge (the project's files, a guess, a
look taken before the checks were registered), and nothing in the Driver card says where a claim
about CI must come from.

## Where it shows

- `skills/chantier/references/driver.md`, "Your means", the `CI:` bullet: it says how to wait
  (`gh pr checks <pr> --watch`, `glab ci status --live`) and how to judge a result, but it has no
  word on the case "no CI", so a Driver is free to conclude it from anything.
- On a PR with no check registered yet, `gh pr checks` answers that no check is reported and the
  watch ends at once: a look taken right after the push reads as "no CI" when CI is only late.
- `skills/chantier/references/pr-template.md`, Test plan, `CI green at <sha7>`: the box has no
  form for a project without CI, so the Driver improvises it.
- The Driver's `note` on CI ("Say what CI showed in a `note`") then carries the wrong fact to the
  steering session and to the report.

## What would fix it

In the `CI:` bullet of the Driver card:

- The forge's list of checks for the PR at the pushed head (`gh pr checks <pr>`, `glab ci list`,
  or the forge's equivalent) is the only source for any claim about CI: running, green, red, or
  none. The project's files, its rules and an earlier Driver's note are not a source.
- "No CI" is said only when that list holds no check after the push, on a look taken once the
  forge has had time to register them, and with the PR's head equal to the pushed head.
- The note that says what CI showed names the command and the head; the PR body's CI box says the
  same thing in the template's words.

The rule sits in "Your means", so it holds for every Driver that pushes (CR, stack, release).

## Out of scope

- Any CLI change: the CLI runs no forge command, and `handback` keeps checking the gate and the
  verdict only.
- How a result is judged (skipped, red on the default branch, flake, the 3-hour limit): unchanged.
- The agent files of both hosts: the contract lives in the card.
- An automated audit of the claim in the eval kit.
