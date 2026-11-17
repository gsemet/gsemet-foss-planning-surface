## Summary

GitHub answers a stack's unstack call with a 2xx and an empty body. `forge-stack rebuild` tried to parse that body as JSON, failed with `not JSON:` and stopped half done: the pull requests were unstacked and no stack was left on the forge. An empty body on a 2xx unstack reply is now a success and `rebuild` goes on (retarget, create, read the stack back). When a `rebuild` fails after the unstack, its last line now says what to run next, so an agent no longer has to work the state out.

## Deliverables

The last line of a refused `rebuild` now depends on what the run did:

| Failure | New last line |
|---|---|
| Before the unstack phase ends (read, refused POST, read-back, stack still open after 5 tries) | none, as today |
| `retarget` failed, or the forge refused the create call, after this run unstacked a stack | `stack #<n> is dissolved and no stack replaces it yet: run `forge-stack create`` (`stacks #<a> #<b> are dissolved … them yet …` for several) |
| The create call was accepted but its reply cannot be read | `the forge accepted the create call but its reply cannot be read, so the stack's state is unknown: run `forge-stack show`` |

```python
def gh(args, host, *, empty_ok: bool = False): ...   # 2xx + empty body -> None when empty_ok
class Unreadable(ChantierError): ...                  # accepted call, unreadable reply (exit 4)
```

The stack driver runs `forge-stack create` itself after the dissolved line; the Chief of Staff runs the command the line names on the user's yes. The unknown-state line stays an `anomaly` for the stack driver, which may quote a `forge-stack show` read.

## Blast radius

Grade: **1**. The change is confined to `forge-stack` (GitHub), two card sentences and the scenario's fake forge; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

None.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `forge_stack_gh.py`: new `Unreadable` error (exit 4, same text as before); `gh(..., empty_ok=True)` returns `None` on an empty 2xx body; `unstack` passes `empty_ok=True` and still decides by reading the stacks back.
- `forge_stack.py`: `_make` raises `Unreadable` when the reply has no stack number; `_rebuild` tracks the stacks it unstacked and appends the dissolved or unknown-state line as above.
- `skills/chantier/references/driver.md` and `chief-of-staff.md`: one sentence each, for the stack driver and the Chief of Staff.
- `scenario/fake_gh.py`: flags `unstack_empty` and `create_unreadable`; `scenario/run_scenario.py`: steps 3, 3b changed, 3c and 3d added; `scenario/README.md` updated.
- `test_cli_units.py`: one parametrized test (six rows) of `gh`'s reply parsing.

## Impacts

No visual change. A `rebuild` on an empty unstack reply completes; a refused one tells the operator the next command.

## Test plan

- [x] New or changed tests (they fail on the previous code): the six-row `gh` reply test and scenario steps 3, 3b, 3c, 3d
- [x] Local gates at judged before the restacks, carried over clean restacks to `e594c4a`: `just test` 375 passed, `just scenario --unit stack --forge github` exit 0
- [x] Evidence: no visual change; the scenario's stack steps 3, 3b, 3c and 3d show the new lines (run before the restacks, carried to `e594c4a`)
- [x] Review: approved before the restacks, carried over clean restacks to `e594c4a`
- [x] Verified before the restacks, carried over clean restacks to `e594c4a`
- [x] CI green at `e594c4a`: all 5 jobs pass, `just scenario (ubuntu-latest)` included, `just scenario (ubuntu-latest)` included

## Internal references

- CR-313 forge-stack-rebuild-empty-unstack

</details>
