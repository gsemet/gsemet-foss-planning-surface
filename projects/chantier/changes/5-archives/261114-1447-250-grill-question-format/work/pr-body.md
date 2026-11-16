## Summary

A grill asks the user a series of independent questions, but jumping from one subject to the next is hard: the question tool is small, has no formatting and shows little context. This change gives every grill and specification question a reference, a short context, concrete examples for each option and a recommendation. The text written before the question tool and the tool itself now show the same questions, in the same order, each option starting with the same words.

## Deliverables

The text before a call and the tool's form mirror each other (new worked example in `skills/chantier/references/chief-of-staff.md`):

| | Text before the call (full) | Question tool (short mirror) |
|---|---|---|
| Question | `grill-format-Q1`, the question, 2-3 lines of context | `grill-format-Q1` + the question |
| Options | `A.` to `D.`, each with a concrete example | `A. <same words> (recommended)`, `B.` ... |
| Recommendation | always option `A.`, with its reason | `A.` marked "(recommended)" |

Choices made:

- A reference `<short name>-Q<n>` on each question; the short name is picked once per item and kept at the head of its answers file; numbers keep counting across series.
- One item per call of the question tool; independent questions only; at most 5 per series, the host's own limit in its reference (4 on Claude Code, 5 on Copilot, both unproved until a trial); at most 4 options per question.
- The text before the tool is written before every call, without exception, remote sessions included.

## Blast radius

Grade: **1**. Wording of cards only (no code, hook, agent file or test); a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The Copilot row says "the host's question tool": the tool's name is recorded nowhere in the repository, so none is invented.
- The Copilot tools table has no mark column, so the mark (the user's statement, unproved, and its trial) sits inside the row.

## Known gaps

- No local long gate ran: the user waived it for this batch; GitHub CI at the head replaces it.
- The question limits (4 questions on Claude Code including Remote Control, 5 on Copilot) are the user's statements, unproved until the trials named in each host reference.
- Copilot's question tool name and whether it has its own free answer are not recorded.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/chief-of-staff.md`: "Backlog and grill" gets the subsection "Asking the user: a series" (who follows it, one asker per item, one item per call, the series, the short name, the reference, the text first, the options, the same on both sides, no question tool, the record, "grilled enough?", a worked example); "Shared understanding" points to it.
- `skills/chantier/references/griller.md`: a mention of the series shape, and which answers file a Griller in a worktree reads and writes.
- `skills/chantier/references/hosts/claude-code.md` and `hosts/copilot.md`: a Tools row for the question tool with the host's figures and their mark; the Copilot preamble admits this one dated exception.

## Human decisions

- Chief of Staff and Griller follow the format for every grill and specification question; the Release driver's yes/no confirmations keep their shape.
- Reference `<short name>-Q<n>`, always the short name, never the CR number.
- One CR or backlog item per call of the question tool; independent questions, at most 5.
- At most 4 options, the recommended one always first (`A.`); the tool's free answer covers the rest.
- The text is written before every call; the form is its short mirror.
- "Grilled enough?" follows the same format.
- Each recorded answer starts with its reference.

## Impacts

No visual change. Grill sessions will show their questions in the new format on both hosts.

## Test plan

- [x] No behaviour change (cards only)
- [x] Local gates (at the pre-restack head, carried): `just check` passes (waived long gate: user waiver for the batch)
- [x] Evidence: none (wording of cards)
- [x] Review: approved at the pre-restack head, carried to c60029e (diff unchanged; see the restack note)
- [ ] Verified at `c60029e` (pending)
- [ ] CI green at `c60029e` (pending)

## Internal references

CR-250 grill-question-format.

</details>
