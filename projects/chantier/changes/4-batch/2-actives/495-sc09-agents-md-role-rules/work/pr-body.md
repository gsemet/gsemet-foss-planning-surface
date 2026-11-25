## Summary

Two steps in one PR, in this order. First, `AGENTS.md` states that the CLI reads roles as data, advises with `next`, refuses with its rails and never decides a merge or a take-back. Second, a new `chantier brief <role> [<unit>]` command writes a role's whole start brief (its card, the floor, its unit's facts, its host rows) in the git folder and prints the short prompt that points at it, so an agent starts from one short prompt and one file.

## Deliverables

One bullet of `AGENTS.md` is rewritten (roles are data; the CLI refuses, advises and never decides a merge; `judge` only words the ask; the user's yes merges), and the CLI gains `brief`.

```
chantier brief <role> [<unit>] [--lease N] [--epoch N] [--cards <folder>]
  -> <git folder>/chantier/briefs/<project>/<batch>/<unit>-<role>.md   (card, floor, facts, host rows, closing line)
  -> stdout: first line, `writes:` and `worktree:` lines when due, `Read <brief file> whole, first.`
```

Choices: the brief is byte-stable (no clock-relative value); it never renews a lease; it reads the record and the planning folder only; the project name is the first folder under `briefs/` so two projects on a shared surface never collide. `take`, `take stack`, `round`, `handoff` and `order qa` print the same bytes as before. `just test`: 113.62 s at the base, 114.09 s at the head on the same machine (+0.5 s, 26 new cases).

## Blast radius

Grade: 1. A new command and a new data file; the only touched existing code is extractions of prompt builders with unchanged output. A plain revert restores the previous state.

## Autonomous decisions

- The role table is a function `roles()` rather than a tuple: the four Drivers' card and writes are read from `concepts.md` at run time, not copied.
- Host row ids per role are a mapping of the host capability ids (Drivers: steering, start, ending, compacting, write guard; workers: ending; board Griller: none).
- Wrapper helpers live in a new `role_wrappers.py` to keep `plugin_files.py` under the file-size limit; `brief` is added to the epoch-command list; `floor.md` gets an LF entry in `.gitattributes`.
- Four open choices took their proposed defaults (`--cards` naming for the two skill roles, project folder under `briefs/`, so the path is `chantier/briefs/<project>/<batch>/<unit>-<role>.md` rather than the specification's `chantier/briefs/<batch>/...`, briefs never cleaned, `brief` allowed through a profile).

## Known gaps

- Until the later steps land (`next`, `help --for`, `msg steering`, `judge`, `roles.yaml`, and the switch of `take`, `round` and `handoff` to `brief`), `AGENTS.md` names commands and a file that do not exist yet at this head.
- `CONTRIBUTING.md` still says "The CLI knows no role"; left out on purpose, as this change is scoped to `AGENTS.md`.
- Copilot: the `writes:` line is inert (no hook) and the Copilot host rows are unproved in a real session.

<details>
<summary>Details</summary>

## Changes

- `AGENTS.md`: role bullet; git-folder sentence; a `brief` exception line. `docs/planning-folder.md`: one line.
- New: `references/floor.md`, `brief_roles.py`, `role_wrappers.py`, `commands/brief.py`, `declare/brief.py`, `tests/test_brief.py`.
- Extractions with no output change: `driver_prompt.py`, `commands/driver.py`, `commands/orders.py`, `commands/facts.py`.
- Hook test case, scenario check and Coverage bullet, eval dry-run case `quiz-folder` made positive.

## Human decisions

- `next` is advice for the choice of the change and the wording; safety steps are refusals, not advice; the CLI words the ask to the user and the steering session may add one sentence.
- One change before the brief change rewrites the four role sentences of `AGENTS.md`: roles are data the CLI reads; the CLI advises, refuses with its rails and never decides a merge or a take-back; `judge` only words the ask.

## Impacts

No visual change. Grep of the old role wording at the base (`git grep -n -i "knows no role\|role's contract lives\|says what it refuses\|what the role judges"`): `AGENTS.md:43-46` and `:134`, `CONTRIBUTING.md:100` and `:122`, `docs/proofs/claude-code.md:361`, `references/hosts/claude-code.md:630`, docstrings in `commands/__init__.py:14`, `driver_prompt.py:149`, `plugin_files.py:174,276,385`; none under `tests/`.

## Test plan

- [x] New or changed tests (they fail on the previous code): `tests/test_brief.py`, hook case, scenario check
- [x] Local gates at `d2c55f0`: `just check`, `just eval-dry-run`, `just mod` pass; `just scenario` passed locally on the pre-rebase tree (ac03671); at this head the pipeline's `just scenario (ubuntu-latest)` job passed
- [x] Evidence: none beyond the tests above
- [x] Review: approved at `ac03671` (carried to `d2c55f0`: a rebase onto main and a one-character `;` in `scenario/README.md`)
- [x] Verified at `d2c55f0`
- [x] CI green at `d2c55f0`

## Internal references

CR-495 (children 9 and 10 of the simplify-cards program).

</details>
