## Summary

A session driven by Remote Control could not start another session (a batch's Foreman, a Griller), and the docs said so. In use, Remote Control refuses a start in another place (a `cwd`, or a saved `preset`), not every start. A start with no `cwd`, no `preset` and `use_worktree: false` works and lands in the steering session's own folder. This PR writes that rule in the Claude Code host reference, the cards and the docs, so the creation of a sub-session works from Remote Control.

## Deliverables

The rule, before and after, as the docs and cards state it:

| | Before | After |
| --- | --- | --- |
| Remote Control, `start_session` with a `cwd` or a `preset` | stated as "refused" for every start | refused (proved 2026-11-20) |
| Remote Control, `start_session` with no `cwd`, no `preset`, `use_worktree: false` | "cannot start outside a worktree", "nested sessions are a problem" | works; the session lands in the steering session's own folder (proved 2026-11-20) |
| Remote Control, forced `foreman` | reuse only, refused with no Foreman to reuse | a new Foreman in the Chief of Staff's folder, or the reuse |
| Remote Control, no argument | direct | direct (unchanged) |
| Steering folder | the planning surface's checkout | that checkout, or the project's main checkout with the surface added as a working directory |

Choices made: a session started that way must land on a main checkout (a worktree session is unfit); what lies outside its folder reaches it by absolute paths in its prompt; a move with `change_directory` inside a trusted folder works but does not reload project instructions; clearing another session is denied by the auto mode classifier, and no route uses it.

## Blast radius

Grade: **1**. Prose in cards, docs, one SVG; no code. A plain `git revert` restores the previous wording.

## Autonomous decisions

- The two wrapped old wordings (README.md, docs/planning-modes.md) were rewritten as a whole paragraph rather than word by word, since the rule they stated is gone.
- `docs/tutorial-claude-code.md`, `init.md` and the mode and fork lines of `session-start.md` were re-read and left unchanged: nothing in them is false.

## Known gaps

- No new trial: the 2026-11-20 sessions (a Foreman and two Grillers started with no `cwd` in the Studio project, and a Foreman started the same way in chantier's own checkout) are the proof; a session the user creates from the remote client's own New session on a chosen folder stays unproved, and a trial from the phone is a separate change.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/hosts/claude-code.md`: the rule stated once; the Foreman-start row; the move with `change_directory`; the Remote Control and planning-surface rows of the classes table; the remote paragraph; the settled trial; the surfaces and options table and the "For you" blocks.
- `skills/chantier/references/chief-of-staff.md`: a forced `foreman` under Remote Control starts a new Foreman or reuses one; the switch to Foreman mode no longer needs a Foreman to reuse.
- `skills/chantier/references/session-start.md`: the main checkout may be the project's own with the surface added as a working directory.
- `README.md`, `docs/planning-modes.md`, `docs/planning-modes-texts.md`, `docs/planning-modes.svg`, `docs/use-cases.md`, `docs/use-cases-direct.md`, `docs/use-cases-foreman.md`, `docs/hosts.md`: the same rule in their own words; the SVG text kept identical to the texts file.

## Human decisions

- With no argument, a batch planned under Remote Control stays direct, as today; only the docs stop saying a Foreman cannot start there.
- A forced `foreman` under Remote Control starts a new Foreman with no `cwd`, instead of only reusing the last one; reusing stays offered.
- Starting an eval's operator from the phone, and Foreman campaigns from the phone, are left to a separate change.
- Proof for this change is the 2026-11-20 trials already made; no new trial before the PR is ready.

## Impacts

No visual change beyond the planning-modes figure's Remote panel text. Documentation only.

## Test plan

- [x] No behaviour change; no new test (the existing check that keeps host tools out of the cards covers the cards).
- [ ] Local gates at `<sha7>`: `just check` in the worktree, pass; stale-wording search below.
- [x] Evidence: stale wording search at base `d7b5a01` and head, below.
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

Search (`grep -rnF "<pattern>" skills docs README.md --include=*.md --include=*.svg`), matches at base `d7b5a01` then at the head (all 0 at the head):

| Pattern | Base | Head |
| --- | --- | --- |
| `no: refused, the message must be typed` | 1 | 0 |
| `Foreman to reuse, else` | 2 | 0 |
| `Remote Control with no Foreman to reuse` | 1 | 0 |
| `with no Foreman to reuse` | 2 | 0 |
| `nested sessions are a problem` | 1 | 0 |
| `cannot start outside a worktree` | 5 | 0 |
| `only by reusing a Foreman` | 1 | 0 |
| ``start_session` is refused (classes table)`` | 1 | 0 |
| `start a session: proved in use` | 1 | 0 |

## Internal references

- The 2026-11-20 sessions: the Studio's batch-07 Foreman and two Grillers, and chantier's batch-29 Foreman.
- The wrapped old wordings (README.md, docs/planning-modes.md) were checked by reading: the rewritten paragraphs no longer state the old rule.
- CR-414 sessions start from Remote Control with no cwd (part A of the request; the eval operator from the phone is a separate change).

</details>
