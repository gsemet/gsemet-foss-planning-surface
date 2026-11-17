# 01: XState v6 beta on the board's PRs feed

Assessment of `xstate@6.0.0-beta.3` (published 2026-11-15; `latest` is still 5.33.4) for the
user's request of 2026-11-17 (`intake/request.md`). The code is on the branch
`poc/xstate-board-feeds` of chantier, in a draft PR that is not to be merged: https://github.com/gsemet/chantier/pull/281.

## 1. What XState is, and what v6 changes

XState is a zero-dependency, MIT library for state machines, statecharts and actors in
JavaScript/TypeScript: a machine names its states and the events each one accepts; actors run
machines and async work, own their timers and children, and stop them all when stopped. It solves
the "boolean soup" of hand-written async UI and workflow code: flags such as `busy`, `stopped`,
`loaded` whose combinations are not all valid, timers and requests that outlive their owner, races
between a slow answer and a newer state.

v6 (beta since 2026-11-05) narrows the authoring surface: a transition is a plain object
(`{ target }`) or one function `(args, enq) => ({ target, context })`; guards are plain `if`s;
effects are queued with `enq.*`; `assign`, `raise`, `sendTo`, the guard combinators, string
targets and `interpret` are gone; `schemas` (Standard Schema, or `types<T>()`) replace `types`
and typegen. New: typestates, state input, choice and route states, state `timeout`, a
data-only CLI (`xstate inspect | validate | simulate | test | replay | diff`) over JSON
definitions, an experimental durable execution, and the docs shipped inside the package
(`node_modules/xstate/docs/`, with an `agents.md`).

## 2. The gnarliest problem it could help with

chantier's real state machines (the CR lifecycle, the batch, the rails) are Python: XState cannot
reach them. Its JavaScript is the web board (plain ES modules, no build) and the pane
(`hooks/register.tsx`, which imports only `claude-code`). On the board, the gnarliest state is in
its two pollers; `views/prs-feed.js` is the worse of the two: a read every 10 s while the page is
visible and a PR is not done, paused when hidden, restarted when a CR gets a PR the last read did
not ask for, one read at a time, no answer written after the view or the project changed, and the
last good answer kept beside a failed one. That is four flags and three event sources
(`setInterval`, `visibilitychange`, the store) in 68 lines. The proof of concept rewrites it.

## 3. The proof of concept

- `board/web/js/views/prs-feed-machine.js`: the rules, as a machine with two states (`reading`,
  `waiting`) and no DOM, store or clock of its own; the forge read is an injected actor.
- `board/web/js/views/prs-feed.js`: the adapter, same export (`startFeed`), feeds the machine the
  page's facts (`shown`, `hidden`, `links`) and writes what it emits (`prs`) in the store.
- `board/web/js/vendor/xstate.js`: XState bundled into one minified ES module (94 kB, 30 kB
  gzipped), its MIT notice on top, by `poc-xstate/vendor.mjs`.
- `biome.json`: the vendored file is left out of Biome.
- `poc-xstate/`: the evidence (tests, type probes, the browser check), not shipped.

One behaviour moves: the 10 s are now counted from the end of the last read, not from the view's
opening (no read can be skipped because the previous one was still running).

## 4. Verification

| Check | Result |
| --- | --- |
| `just check` (ruff, mypy, Biome, 382 pytest tests, release notes) on the branch | pass |
| `just scenario` on the branch | pass: every unit ok, 399 s wall time (local, Windows) |
| `node --test poc-xstate/prs-feed.test.mjs`: 8 tests of the machine, simulated clock, reads answered by hand | 8 pass, 140 ms |
| Mutation check: 3 mutants of the machine | 2 killed; the third showed the timer's re-arming was dead logic, now removed |
| `poc-xstate/browser_check.py`: the worktree's `chantier board` on a copy of `docs/demo/`, Chromium, Playwright's clock, made-up forge answers (no `gh`, no network): 9 time windows (open PRs visible/hidden/shown again, every PR done, the view left) | the XState version and `main`'s version give the same reads in all 9 windows; no page error |
| The board's "self-contained frame" test (`test_code_targets.py`) | failed on the first bundle: XState's error messages link to GitHub; `vendor.mjs` points them at the package's bundled `errors.md` |

Not covered: a CR getting a new PR while the page is open is tested on the machine only, not in
the browser; the old and new code were not run against a real forge.

## 5. Grades (each out of 5, 5 the best)

**5a. API nuance (more is worse): 2/5.** v6 removed a lot (no guard combinators, no `assign`, no
string targets, one transition form for conditions), but the root module still exports 55 names
and the subpaths about 30 more, and most needs have several spellings: a delay is `after`, a state
`timeout`/`onTimeout`, an invoke `timeout`, or `enq.raise(..., { delay })`; async work is
`invoke`, `enq.spawn`, a context-initializer `spawn`, or one of five `create*Logic`; a condition is
an inline `if`, a named guard, `always`, or a `choice` state; a message is `enq.emit`,
`enq.sendTo`, `enq.listen` or `enq.subscribeTo`. A two-state feed already used nine concepts
(`setup`, `createMachine`, `createAsyncLogic`, `createActor`, `provide`, `invoke`, `after`,
`always`, `enq.emit`). The shipped `agents.md` helps an agent choose; it does not remove choices.

**5b. Type safety: 4/5 in TypeScript, 0/5 on the board as it is.** A typed twin of the machine
(`poc-xstate/types-probe/`, `types<T>()` schemas, `tsc --strict`) caught 7 of 8 seeded mistakes:
a target typo, a wrong event field, a wrong emitted event, a wrong context value, an unknown actor,
a missing actor input, a wrong invoke input. It missed an unknown context key added through a
spread (a TypeScript limit). The target typo is reported at the `createMachine` call, not at the
typo, as "not assignable to parameter of type 'never'": found, but hard to place. The board is
plain JavaScript with no type check: none of this applies until it moves to TypeScript or
`checkJs`, which needs a Node tool in `just check`.

**5c. Testability: 4/5.** The best part: transitions are pure functions, `provide()` swaps the
forge read, `SimulatedClock` drives the timers; 8 tests run in 140 ms with no DOM, and the mutants
found dead code. Against it: v6's headline model tooling does not apply to idiomatic v6 code.
`xstate inspect` on the machine's JSON answers `EVALUATOR_REQUIRED` for all 10 transitions,
because every conditional transition is a function; `simulate`, `test` and `replay` need
data-only definitions. The two v6 features pull against each other.

**5d. Cyclomatic complexity: 2/5.** ESLint's `complexity`, per function:

| | Functions | Sum | Max | Code lines |
| --- | --- | --- | --- | --- |
| `prs-feed.js` on `main` | 13 | 29 | 4 | 50 |
| machine + adapter | 25 | 39 | 4 | 103 |

The flags (`busy`, `stopped`, `here()`) are gone and every rule is named in one place, but the
explicit complexity grows by a third, the code doubles, and the implicit complexity moves into
94 kB of library semantics (run-to-completion steps, `always` re-evaluation, invoke lifecycles)
that a reader must know.

**5e. Docs: 4/5.** 71 Markdown pages (about 79,000 words) ship inside the package and match the
installed version exactly, with a cheatsheet, a v5 migration guide with a codemod, an agent guide
and an export stability manifest; reading them offline was enough to write the machine first
time. Against it: it is a beta (after 73 alphas), the production build's errors are codes
(`XState error E<n>`) to look up, and the TypeScript errors (5b) are not documented away.

**5f. Deployment changes: 1/5 (heavy for chantier).** The board has no build and no npm, and
chantier's rule is that `uv` is the only tool to install. Adopting XState there means:

- a vendored, minified third-party file (94 kB) in the package, rebuilt by a Node script run
  through `uvx --from nodejs-wheel`, and a way to keep it on a pinned version through a beta's
  churn;
- an exception in Biome, and a rewrite of the bundle to keep the board's "names no other origin"
  rule (or a change of the rule);
- JavaScript tests wired into `just check` (none exist today: the board is tested from Python), or
  the machines stay untested by CI;
- the MIT notice kept in the shipped file;
- nothing for the pane (`hooks/register.tsx` imports only `claude-code`) nor for the Python CLI.

## 6. Recommendation

Do not adopt XState in chantier now. It works, and it makes a poller's rules explicit and very
easy to test, but chantier's gnarly state is in Python where it cannot go, and the board's state
is small enough that a third-party bundle, a Node toolchain in the checks and a beta's churn cost
more than the four flags they remove. Keep the board's hand-written pollers.

Two things are worth taking without the library:

- the shape: a pure "what to read next" function, separate from the DOM and the store, tested
  with a fake clock; `prs-feed.js` and `refresh.js` could take it in plain JavaScript;
- a mutation pass: three mutants found dead logic in the machine; the same cheap exercise on the
  current pollers may find some there.

Revisit if the board moves to TypeScript with a build, or grows a real multi-step flow (an edit
with a conflict and a retry, a wizard) where statecharts pay for themselves.
