# Intent: AGENTS.md names the forge calls the CLI makes

Sources: `intake/request.md` (2026-11-20), and the parent CR `take-base-from-forge`
(`5-archives/261121-0330-422-take-base-from-forge/02-answers.md`, Q11: "`agents-md-names-cli-forge-reads`
(AGENTS.md's network sentence does not name the forge reads `ship`, `take`, `handoff` and
`forge-stack` already make with `gh` or `glab`) ... the second is a rule's wording, the user's").

No grill was held: on 2026-11-21 the user delegated the night's spec questions ("plus de
question"). The choices left open are written as numbered questions in `03-change-spec.md`, each
with a recommendation, and the specification is written on the recommended options.

## What the user wants

The project's rules and the CLI's code agree on when the CLI talks to the forge. Today AGENTS.md
says the CLI needs no network once uv's cache holds its packages, except three named parts (the
server's read of a batch's PRs, the forge hub, the surface server's writer), and its scope bullet
says "the agents do the work, git and the forge included". The CLI makes more forge calls than
that, with the user's own `gh` or `glab`:

- `ship` reads the PR's base branch and draft state;
- `take`, `round` and `handoff` read the base branch of a stacked CR's PR (the request names
  `take` and `handoff`; the code shows `round` does it too);
- `forge-stack` reads, and writes, the stack on the forge (it creates and dissolves stacks and
  retargets PR bases).

Either the rule names them, or the CLI stops making them. The request asks for no code change:
it is a decision on a project rule's wording.

## Why

The parent CR had to settle whether `take` could add a forge read, and found the rule silent on
the ones already there. A rule that does not say what the code does misleads every agent and
reviewer that reads it (a Driver would refuse, or a critic would flag, a read the CLI already
makes).

## Done when

AGENTS.md (and the same sentences where CONTRIBUTING.md and README.md repeat them) name every
forge call the CLI makes, and no sentence there says the CLI makes none.
