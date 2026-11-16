# Build the eval sandbox project

First of two CRs (the user, 2026-11-12: "fais 1 puis 2"); `reproducible-evals` follows it and
builds the campaigns on it. The grill's answers for both CRs are in
`reproducible-evals/02-answers.md` (2026-11-12): this CR follows them as written.

## The request

The eval campaigns get a frozen project to run on, the public repository
https://github.com/gsemet/chantier-eval-sandbox, created by the user ("fais-en ce que tu veux").
This CR builds that project in a clear, clean, working state, so that every eval starts from one
known SHA-1.

## What the project is (from the answers)

- A Python project managed with uv, with GitHub Actions CI, and the CI is fast (a minute or two,
  not ten).
- A small web application served by a Python backend; the HTML is written by hand. No Node, no
  front-end build: only uv and hand-written HTML (and CSS).
- It exists and works before any eval: tests pass, CI is green, the app runs locally with one
  documented command.
- It is shaped so the CRs that evals run on it are real coding without being long: a few
  modules, clear seams, room for small features (a page, a route, a filter, a validation, an
  export) that touch the backend, the HTML and the tests.
- It carries what a chantier user's project carries: an `AGENTS.md` (how it builds, tests, runs,
  ships and releases, its long gate), a release procedure (version bump, notes, tag, GitHub
  release) so a batch can end with a release on it.

## Where it lives

- Its source and the way its initial commit is produced belong to chantier's eval kit (under
  `evals/kit/`), so the base SHA-1 is known and reproducible: the same kit, run twice, produces
  the same commit (fixed author, committer and dates), and the kit records that SHA-1.
- The sandbox's `main` today holds only the README commit made at its creation, so putting the
  project there replaces `main`: a force push. The answers say a force push on the sandbox lives
  only in a clearly defined, reviewed kit command, never an ad-hoc command. The Chief of Staff
  places that command in this CR: the kit's reset of the sandbox to the initial commit is how the
  project first reaches the sandbox, and the same command resets it before each eval
  (`reproducible-evals` then uses it). It resets `main` to the initial commit and removes what
  evals leave: open PRs closed, branches other than `main` deleted, tags and GitHub releases
  deleted (evals merge PRs and make releases there). Merged PRs may stay. It never touches any
  repository other than the sandbox, and says what it is about to do before it does it.
- This CR ends with the project published on the sandbox at the recorded SHA-1, its CI green
  there.

## Out of scope

The frozen CRs, the hidden tests, the campaigns and their runbooks, the audit's changes: all in
`reproducible-evals`.
