## Summary

In a recent batch the cards already said what each worker's reply must look like, and replies still broke their format: a verdict given in prose, a proof with no command, a worker resumed by message instead of started again. This PR replaces the pile of specific rules with one: a reply that breaks its format is a failed worker, which the Driver starts once more with the same brief, never reads meaning into and never resumes by message. Two smaller rules come with it: the conflict resolver's `conflicts.md` names the fast gate it ran and its result, and a forge 5xx or network failure re-runs the same command once, then ends as `blocked infra:`.

## Deliverables

Card text only, so the before/after is the diff. The rules, by card:

| Card | What it now says |
| --- | --- |
| `driver.md`, "Your means" | A reply is checked against its worker's format (Inspector JSON alone, Verifier proof with SHA, command and output, `conflicts.md`, output files). Out of format: `restart: reply out of format: <what is missing>` and one new start with the same brief. A second one: next round for a Coder, `blocked question:` for another role, an `anomaly` for the stack driver. No resume by message. |
| `driver.md`, "Your means" | A remote command failing on an HTTP 5xx or a network failure runs once more at once (after checking the first attempt did not take effect, for a command that creates or moves something), then `blocked infra:` (an `anomaly` for the stack driver). A refusal keeps its own routes. |
| `driver.md`, "CR driver" | A rebase during which a conflict resolver ran always gets an Inspector before the next push, recorded `move <old7>..<new7> (conflict) inspector approved at <head>`. |
| `worker.md` | The shared paragraph says a reply out of format is a failed worker; the Verifier's proof rule holds for a refusal or any negative claim; `conflicts.md` holds the fast gate's command and result. |
| `concepts.md` | `reply out of format: <what is missing>` joins the restart causes. |

## Blast radius

Grade: 1. Text of three cards, no code. A plain `git revert` restores the previous cards.

## Autonomous decisions

- The specification's mention of `SendMessage` is written as "a message to its agent": a structure test forbids host tool names in the cards.
- The remote-command bullet sits just before the Push bullet rather than inside it, so the Push bullet stays whole.

## Known gaps

- No scenario check or eval row covers the new card text: left out on purpose, tests stay few and the cards' diff is the evidence.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: reply-out-of-format bullet, remote-command re-run bullet, clarified paragraph on the Inspector after a resolved conflict.
- `skills/chantier/references/worker.md`: shared paragraph, Verifier, Conflict resolver.
- `skills/chantier/references/concepts.md`: one restart cause.

## Human decisions

- One Driver-side rule for a reply out of format, instead of one rule per failure.
- The whole proposal is in scope, including the infra re-run and the fast gate line in `conflicts.md`.

## Impacts

No visual change. Drivers and workers follow the new rules from the next session that reads the cards.

## Test plan

- [x] New or changed tests (they fail on the previous code): No behaviour change (card text)
- [x] Local gates at `8d9efdb`: `just check` and `just scenario` pass
- [x] Evidence: the cards' diff, no before/after run
- [x] Review: approved at `8d9efdb` (carried from `b3cc2be` over two clean rebases)
- [x] Verified at `8d9efdb`
- [x] CI green at `8d9efdb`: `gh pr checks 168`, all five checks pass

## Internal references

- CR-230 worker-reply-contract (batch-17), from the retro of batch-16.

</details>
