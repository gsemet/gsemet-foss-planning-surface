# A PR says on the forge when it is not ready to merge

## Problem

A CR's PR is open and mergeable as soon as it exists, whatever its CI, its evidence or its base. The
user merged PR 55 and PR 57, both green, into another CR's branch. The forge says nothing against
that merge, and the cards do not say who opens a PR while a stack is not ordered.

## Change

**Ready, defined.** A PR is ready to merge when its CR is handed back `ready` and its base is the
default branch. Any other PR is not ready, and says so on the forge.

**The cards** (`driver.md`, with `foreman.md`, `chief-of-staff.md` and `concepts.md` where they say
the same thing):

- The CR Driver always opens its CR's PR, on the `base` that `take` printed, as a draft
  (`gh pr create --draft`, `glab mr create --draft`). The stack driver never opens one: it retargets
  and restacks.
- At `handback ready`, the CR Driver turns the PR ready (`gh pr ready`, `glab mr update --ready`)
  if its base is the default branch; otherwise it leaves the draft and says so in its hand-back.
- The stack driver keeps this true for each PR it moves: a PR on the default branch whose CR is
  ready turns ready; a PR on another base turns draft (`gh pr ready --undo`, `glab mr update
  --draft`). After a partial merge, the new first PR turns ready once it is retargeted and green.
- A send-back to a Driver turns its PR back to a draft.
- **The project's rules rank first.** A project that says how a PR shows it is not ready (a label, a
  title prefix, no draft at all) is followed as written, on both the opening and the turning ready.
- **No fallback.** A forge or plan that refuses a draft is a stop for that step: the Driver reports
  the exact text to its parent and the Chief of Staff tells the user. It picks no look-alike.

**The report.** In a Progress report, 🔵 to review is a ready PR only; a CR ready on a base other
than the default branch says what it waits for.

**The CLI** gains no forge command. The scenario's fakes (`scenario/fake_gh.py`, `fake_glab.py`)
accept the new calls if the scenario's run needs them.

## Out of scope

`rails.py` refusing a PR by its base, and any check of the PR's state by the CLI.

## Done when

- The cards say all of the above, on GitHub and GitLab alike, and do not contradict each other.
- `agents/` and `com.github.copilot/agents/` keep identical bodies, if touched.
- `just check` and `just scenario` pass.
