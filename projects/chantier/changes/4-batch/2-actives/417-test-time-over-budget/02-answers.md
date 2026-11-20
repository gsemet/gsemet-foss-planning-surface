# Answers: just test and the scenario units over their time budgets

The user asks no questions on this CR (2026-11-20: "tu es maintenant autonome. plus de question.
tu grilles tout seul"). Each point below was open in `intake/request.md` and is settled here from
the request, the code at main (`4ed0d56c`) and the project's rules, by the narrowest choice that
meets the request.

## A1. Is the AGENTS.md ceiling changed?

No. The ceiling stays as AGENTS.md and CONTRIBUTING.md write it: `just test` at most 30 s above
its 18.5 s of 2026-11-14 on the user's Windows machine, so 48.5 s. This CR brings the suite under
it. If the measurement proves it cannot be met without losing coverage, the Driver stops there,
delivers the gain it has, names the gap in the PR's Known gaps with the figures, and the change of
the ceiling goes to the user as a new CR: it is a project rule, not this CR's to change.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the request says
"bring `just test` back under the ceiling", and a rule change is the user's.

## A2. What counts as the measure of `just test`?

The time pytest prints on its last line (`N passed, M skipped in X s`) for a plain `just test`
(`pytest -q -n auto`, no other argument), on the user's Windows machine, idle: no other `just
test`, `just scenario`, `chantier gate` or eval running on it. Three runs in a row; the suite is
under the ceiling when each of the three is at most 48.5 s. The same three runs are taken first at
main's head, as the baseline, in the same sitting.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the request asks
for a baseline on an idle machine; three runs each under the ceiling is the plainest proof, with no
statistics to argue about.

## A3. What if the machine cannot be idle while a batch runs?

The Driver waits for a moment when no other test, scenario, gate or eval runs, and takes its runs
then. If it cannot get one, it records its runs as loaded, with what else was running, and the PR's
Known gaps says "no idle measure of `just test`". A loaded measure proves nothing against the
ceiling, in either direction.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the batch has
other Drivers on the same machine; the evidence must say under which load it was taken.

## A4. Which ways of saving time are allowed?

Only those that keep every assertion:

- a prepared state built once (per session or per module) and copied for each test, as
  `repo_template` and `surface_template` already do in `conftest.py`;
- fewer git processes for the same state (one command in place of several, a state written to disk
  in place of a sequence of commands that builds it), when git's own behaviour is not what the
  test checks;
- tests that build the same state merged into one test or one parametrized test, each assertion
  kept with its message;
- a duplicate removed: a test whose every assertion is made by another test, named in the PR;
- pytest's and xdist's own settings (how the tests are spread over the workers), when no test
  leaves the default run.

Not allowed: a skip, a marker or an option that takes a test out of the plain `just test`; a fake
in place of real git where real git is what the test checks (the writer's rebase, conflict, stash
and push in `test_writer_cycle.py` and `test_writer_edges.py`, the carry's patch comparison in
`test_carry_ship.py`, the fast-forward in `test_release_tag.py`); a weaker assertion; a refusal no
longer checked.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the project's rule
is "few, parametrized and fast", and the brief's is never to lower a check's strength to save time.

## A5. Do tests move from pytest to the scenario?

No. No check moves to `scenario/run_scenario.py` in this CR. The request notes that the workflow
belongs to the scenario, but three units are already over their budgets, and a moved check would
make the re-measure a moving target.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: narrowest choice;
the scenario's units are measured as they are.

## A6. Does the CLI's source change?

No. The change is in the tests' folder (`skills/chantier/scripts/cli/tests/`), in the `UNITS`
literals of `scenario/run_scenario.py` and in `scenario/README.md`. Nothing under
`skills/chantier/scripts/cli/src/` changes. A saving that would need a change of the CLI (a git
process the CLI runs twice, for instance) is not made: the Driver names it in its hand-back, as an
idea for the inbox.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the request is
about the tests' time; a CLI change is another risk and another gate.

## A7. How is "no coverage lost" proved?

By an inventory. The list of test ids (`pytest --collect-only -q`) is taken at main's head and at
the CR's head. Each id that is gone or renamed is listed in the PR with where each of its
assertions now lives (the test id that holds it). An id with no destination is a refusal of the PR.
The scenario README's coverage list names tests by `(test: <file>::<test>)`: each renamed or merged
test is renamed there too, and `test_scenario_coverage.py` stays green.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: a time saved by a
dropped check must be visible to the Verifier without rereading every test.

## A8. Scenario units: sped up, or their budgets re-set?

Their budgets are re-set from a new measure; no case is sped up, moved or removed. The request
says "re-measure the scenario units' budgets". A budget only warns, so a higher one drops no
check.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the request's own
words; speeding the units up is a larger work, not asked.

## A9. How is a unit's budget set from the measure?

Two full runs of `just scenario` (both forges, `--jobs 4`, the default) at the CR's head, on the
user's Windows machine, idle as in A2. Each unit's budget is the slower of its two times plus 25
percent, rounded up to the next 5 s. The rule is applied to the nine units alike, upward or
downward: `parallel`, `stack`, `release`, `gates`, `series-deps`, `direct`, `surface-board`,
`qa-driver`, `gitlab`. The README says that the measure is an idle one, and that under load a unit
may warn.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the README's own
rule is "the `--jobs 4` time plus about 25 percent"; the request asks for an idle machine; one rule
for the nine units leaves no literal unexplained.

## A10. What is refreshed in the scenario README?

The measured section of `scenario/README.md` (from "Measured on 2026-11-15" to the paragraph
ending "lower the budgets"): the date, the machine, the load, one table with the nine units, their
budget as `UNITS` holds it and the two runs' times, the wall time and the sum of the units. The
stale figures go (`direct` 125 where `UNITS` says 135, `surface-board` 300 where it says 700, the
`stack` paragraph's older runs). The sentence saying that under 300 s on a quiet Linux machine is
not proven stays, unless the PR's own CI run of `just scenario (ubuntu-latest)` gives the figure,
in which case the README quotes it with its date.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the request asks
for the stale measured columns to be refreshed with the re-measure, and nothing more.

## A11. Is a guard added (a test that fails when `just test` is slow, or when the README's budget column differs from `UNITS`)?

No. Neither is asked. A time guard would be flaky on a loaded machine; the budget column guard is
a new check of its own.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: narrowest choice;
both are named out of scope in the specification.

## A12. Where does the work start, and when does it stop?

It starts with the files that cost the most, from a `--durations` profile taken with the baseline.
At main `4ed0d56c` on 2026-11-20 (1405 passed, 14 skipped, 89.0 s on a loaded machine, so not a
reference), the calls and setups of 0.8 s or more summed to: `test_writer_cycle.py` 66 s,
`test_carry_ship.py` 64 s, `test_writer_edges.py` 47 s, `test_release_tag.py` 13 s,
`test_store_command_table.py` 12 s, `test_surface_writes.py` 10 s. It stops when the three idle
runs of A2 are each at most 48.5 s, or at the end of the CR's third round with A1's hand-back.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the CR must fit in
one batch CR of at most three rounds; the request already names the slowest files, the profile
confirms them and adds the writer's.
