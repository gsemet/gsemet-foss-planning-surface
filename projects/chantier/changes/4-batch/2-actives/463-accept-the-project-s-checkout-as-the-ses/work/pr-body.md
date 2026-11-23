## Summary

When a project plans in a separate planning surface, a session started in the project's own checkout (its clone) failed preflight checks P6 and P7, with a false "linked worktree" message, so no batch could open from it. Preflight now accepts the main checkout of either the surface or the project's clone, and still refuses a linked worktree of either. The surface's branch check (P11), the forge-remote reads and the settings files of the permissions check (P10) now read the folder they concern instead of whichever folder the session runs in.

## Deliverables

Session folder, before and after:

| Session folder | Before | After |
| --- | --- | --- |
| surface's main checkout | P6 ok, P7 ok | P6 ok, P7 ok |
| project's clone (nested or beside the surface) | P6 FAIL, P7 FAIL ("linked worktree") | P6 ok, P7 ok |
| linked worktree of the surface | P7 FAIL | P7 FAIL, with a message naming the surface |
| linked worktree of the clone | P6 FAIL, P7 FAIL | P7 FAIL, with a message naming the clone |
| another repository | P6 FAIL | P6 FAIL, naming both accepted folders |

```python
class SessionCheckout(NamedTuple):
    top: Path | None   # the cwd's top-level folder
    linked: bool       # a linked worktree
    owner: str         # "surface" | "clone" | "project" | "other" | "none"
    main: Path         # the main checkout the session should be in

Repo.session_checkout(cwd=None) -> SessionCheckout
```

Choices: the session folder is read from the process's real folder, never from an environment override; `init` refuses only a linked worktree, with P7's text.

## Blast radius

Grade: **1**. The change is confined to preflight, `init`'s worktree refusal and two permission reads; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- None beyond the specification.

## Known gaps

- The CLI still does not read the project's planning pointer line, and does not refuse a run without `--project`; the cards ask the session to pass it.
- No long gate was run locally (waived by the user); CI runs what it runs.

<details>
<summary>Details</summary>

## Changes

- `core/repo.py`: `session_checkout`, one `git rev-parse` of the cwd.
- `commands/preflight.py`: P6, P7 messages per owner; P11 reads the surface's branch.
- `commands/intake.py`: `init` refuses only a linked worktree.
- `commands/permissions.py`: remote reads run in the project's repository; settings are read from the session's folder.
- Cards: session start, both host references, the Chief of Staff and Foreman cards say what the code does.
- Tests: `test_session_folder.py`.

## Human decisions

- Option A: P6 and P7 accept both main checkouts, each refusal with its own message.
- The surface is found by the session from the project's `AGENTS.md` pointer and kept; the CLI's git reads run on the folder they concern.
- No long gate and no eval for this fix.

## Impacts

No visual change. A session in the project's clone can now open a batch.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test_session_folder.py`
- [ ] Local gates at `9bb9c9b`: `just check` (2157 passed, 20 skipped), `just eval-dry-run` (19 of 19)
- [ ] Evidence: none; tests are the proof
- [ ] Review: approved at `9bb9c9b`
- [ ] Verified at `9bb9c9b`
- [ ] CI green at `9bb9c9b`

## Internal references

CR-463 session-folder, batch-31.

</details>
