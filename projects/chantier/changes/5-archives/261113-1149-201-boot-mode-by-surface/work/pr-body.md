## Summary

`/chantier:chief-of-staff` used to run batches in Foreman mode or direct mode depending on the session, and proposed direct mode in the plan. The mode now follows the surface: with no argument, a local session at the desktop uses a Foreman, and a session under Remote Control, a terminal or VS Code (anywhere a Foreman cannot start) uses direct mode. A first word `foreman` or `direct` forces one for the session, and the plan says which mode is used and why, with no separate question. The README is also reworked around this single entry point, and the Claude Code CR board gets a real docs page with screenshots.

## Deliverables

- The mode rule, in the Chief of Staff card's "Starting a batch":

| Situation | Mode |
|---|---|
| first word `foreman` or `direct` | forced for the session (`foreman` is refused where no Foreman can start) |
| no argument, Remote Control notice present | direct |
| no argument, host cannot start a Foreman | direct |
| no argument otherwise | Foreman |

- The CR board in the README, after the change (at `dce25c9`):

![The CR board of a batch just opened](https://raw.githubusercontent.com/gsemet/chantier/dce25c92c0d1ac373e819936cc39bae8398d5ca4/docs/board-mod-batch.png)

- README: one boot skill, the CR board section with a screenshot, a direct-mode session screenshot, Releases with an example procedure; "What is Chantier?" and "Repository layout" moved to `CONTRIBUTING.md`.
- `docs/boards.md`: what the board is, how to open it, how to read it, and five screenshots of a batch from start to done. A cost report screenshot is added to the tutorial and `docs/costs.md`.
- The two simple diagrams show the new entry lines (desk or foreman, remote or direct).

## Blast radius

Grade: 1. Documentation, cards and eval runbooks only; no code, CLI or hooks change. A `git revert` restores the previous behaviour.

## Autonomous decisions

- The CR board section of `docs/boards.md` is split into subsections, the last one holding the mod's guard paragraph unchanged.
- The `claude-code` card keeps the argument's handling marked unproved, as no eval report was checked for proof.

<details>
<summary>Details</summary>

## Changes

- Cards: `chief-of-staff` and `chantier` skills, `chief-of-staff.md`, `session-start.md`, `init.md`, `hosts/claude-code.md`, `hosts/copilot.md`.
- `README.md`, `CONTRIBUTING.md`, `docs/` pages, seven screenshots, two simple SVGs and their texts.
- `evals/real-foreman/RUNBOOK.md` and `evals/full/RUNBOOK.md` start with `foreman`.

## Human decisions

- The mode follows the surface unless forced; the plan states it and the go is the yes.
- A forced `foreman` where none can start is refused, never swapped silently.
- The README drops "What is Chantier?" and "Repository layout"; the board is shown with the user's screenshots.

## Impacts

The README and the board page now show the screenshots; the plan names the mode and why.

## Test plan

- [x] New or changed tests: No behaviour change in code
- [x] Local gates at `dce25c9`: `just check` (58 passed), `just scenario` carried from `6f9a236`: patch unchanged; the long gate runs once at the top of the stack, PR 152 (github 586/586, gitlab 586/586 at `6f9a236`)
- [x] Evidence: the two simple diagrams rendered (carried from `6f9a236`), the seven screenshots hash-identical to their sources, judged again at `dce25c9`
- [x] Review: approved at `6f9a236` (carried to `dce25c9`: patch unchanged by the restack)
- [x] Verified at `dce25c9`
- [x] CI green at `dce25c9`

## Internal references

CR-201 boot-mode-by-surface

</details>
