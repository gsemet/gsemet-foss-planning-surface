## Summary

A batch could only be a stack (the default) or independent pull requests (`--parallel`), and a stack started all its CRs at once, which read as "not in series". This change gives a batch three explicit modes: **parallel** (the default: every CR starts from the default branch, and after each merge every open PR is rebased and checked again), **series** (one CR after the other, each starting from the previous one's pushed branch once it is ready, as a draft, rebased onto the default branch after the previous merge) and **stack** (every CR at once, PRs each on the previous one, kept up to date automatically (restacked after a change)). A series can switch to a stack on request.

## Deliverables

A new diagram of the three modes, `docs/batch-modes.svg` (texts in `docs/batch-modes-texts.md`), shown in a new "Batch modes" README section.

![The three batch modes](https://github.com/user-attachments/assets/571694a6-ce84-4ea1-b9e5-6a8a1245961e)

```text
chantier open <folders...> [--mode parallel|series|stack]     # default: parallel
chantier order mode --note stack                            # series -> stack only
```

| Mode | Each CR starts from | PR base | After a merge |
| --- | --- | --- | --- |
| parallel (default) | the default branch | the default branch | every open PR rebased and checked again |
| series | the previous CR's branch, once it is ready | the previous CR's branch, as a draft | the next one is rebased onto the default branch and turns ready |
| stack | the default branch (or its last open dependency) | the CR under it | the stack is restacked |

## Blast radius

Grade: 2. `open --parallel` is removed (no alias) and the default mode changes from stack to parallel, so batches opened by habit now get independent CRs. The series rules touch `take`, `status` and the start base. Rollback is a revert of the change.

## Autonomous decisions

- Stack keeps today's mechanics (each CR starts on the default branch or its last open dependency, the PRs are stacked afterwards): the least disruptive reading, since the request was ambiguous.
- A series batch gets no demo offer, as before for non-stacks: the same reading.
- A CR blocked with a PR is rebased too after a merge in a parallel batch: the same reading.
- Invalid `order mode` and invalid series order exit with code 2 (the CLI's precondition code), since 1 is the usage code in this CLI.

<details>
<summary>Details</summary>

## Changes

- CLI: `open --mode` replaces `--parallel`; `open` refuses a series whose order puts a CR before its dependency; in a series a queued CR also waits for its predecessor (`take` refuses it, `status` shows it), and its start base is the predecessor's branch until that one merges; new order `order mode --note stack` switches a series to a stack.
- Agent guidance (the reference docs for planning, batch steering and PR work) describes the three modes, the rebase after each merge by mode, and the generalised `rebase:` note.
- Docs: new batch-modes diagram and texts, README section, use-cases for batch steering and direct mode.
- Scenario: `--parallel` removed, stack sections open with `--mode stack`, a new section covers the three modes and the switch.

## Human decisions

- Parallel is the default; series or stack only when asked or when a CR depends on another.
- In a series the next CR starts only once the previous one is handed back ready, and is rebased when the previous one changes during review.
- A series switches to a stack on request, every remaining CR starting at once.
- After each merge in a parallel batch every open PR is rebased and its checks run again.

## Impacts

Users who relied on the stack default must now ask for `--mode stack`. The README and the docs describe the three modes.

## Test plan

- [x] New or changed tests (they fail on the previous code): scenario section for the three modes and the switch
- [x] Local gates: `just check`, `just scenario`
- [x] Evidence: the diagram in Deliverables; CLI output of the mode scenarios
- [x] Review
- [ ] CI green

## Internal references

- CR-167 batch-modes-redefine
- `.agents/changes/4-batch/2-actives/167-batch-modes-redefine/03-change-spec.md`

</details>

