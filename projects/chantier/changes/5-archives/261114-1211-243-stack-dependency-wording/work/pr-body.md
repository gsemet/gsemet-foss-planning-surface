## Summary

Two sentences of the concepts card said that, in a parallel batch and in a stack, every change request (CR) starts at once. The CLI does not do that: `take` refuses a queued CR until each CR it depends on is `ready` or `merged`, in every mode. The two sentences are rewritten to say what the CLI does, so the card and the rails agree.

## Deliverables

Before and after, for the batch modes paragraph of `skills/chantier/references/concepts.md`:

| Mode | Before | After |
| --- | --- | --- |
| Parallel | every CR starts from the default branch at once | every CR with no open dependency starts at once; a CR with a dependency starts once that dependency is `ready`, on the branch of its last open dependency (else the default branch), its PR a draft until the dependency merges |
| Stack | every CR starts at once, on the default branch or on its last open dependency | every CR with no open dependency starts at once; a CR with a dependency starts once that dependency is `ready`, on the branch of its last open dependency (else the default branch) |

The Series sentence and the Dependencies paragraph, which already said it right, are unchanged.

## Blast radius

Grade: **1**

A wording change in one card, no code. A plain `git revert` restores the previous text.

## Autonomous decisions

None

## Known gaps

- The local long gate (`just scenario`) was not run: it is waived for this batch and CI at the head replaces it.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/concepts.md`: the Parallel and Stack sentences of the batch modes paragraph, as above.
- `foreman.md`, `driver.md` and `chief-of-staff.md` were checked for the same wording and already agree; they are unchanged.

## Impacts

No visual change. Agents reading the card now get the same rule as the CLI enforces.

## Test plan

- [x] No behaviour change (cards only)
- [x] Local gates at `b24f7c2` (the tree reviewed, before the commit): `just check` passed (mypy, `uv lock --check`, 63 tests); a search for `last open dependency|every CR starts` in `skills/chantier/references` finds nothing. No local long gate (waived for this batch; CI replaces it).
- [x] Evidence: reading pass, the new Parallel and Stack sentences and Dependencies say the same; `foreman.md`, `driver.md`, `chief-of-staff.md` checked, no contradicting wording
- [x] Review: approved at `b24f7c2`, committed as `c4e3cae`
- [x] Verified at `c4e3cae`
- [x] CI green at `c4e3cae`: `gh pr checks 185` shows check x3, eval-dry-run and scenario pass

## Internal references

CR-243 stack-dependency-wording.

</details>
