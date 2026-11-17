## Summary

A Claude eval campaign's operator session could not be started from the phone: a new workspace folder needs the Claude Desktop app's trust step, which the app shows only at the desk, never under Remote Control. The first campaigns of v0.11.0 could not start for that reason. This PR has the user pick one eval root folder and trust it once at the desk. The eval kit then creates every workspace inside it, and refuses any other. chantier never writes or edits a trust or security setting: only the user grants trust.

Only the campaigns with no Foreman can start away from the desk. A Foreman campaign still needs the desk, to start the Foreman and type the go, because a session driven under Remote Control cannot start another session.

## Deliverables

The campaigns, and where each starts:

| Campaign | Foreman | Away from the desk |
|---|---|---|
| `real-direct` | no | yes |
| `ticket-summary` | no | yes |
| `claude-planted` | no | yes (its operator) |
| `real-foreman` | yes | no: the desk, to start the Foreman and type the go |
| `full` | yes | no: the desk, to start the Foreman and type the go |
| `copilot` | - | out of scope (the Copilot app's trust) |

The setup refusal, as `evals/kit/setup.py` now behaves:

```text
setup.py <campaign> <workspace>
  read evals/kit/eval-root.local.json   -> {"root": "<absolute folder>"}
  no file or malformed file             -> refused, names the file (and the line to write)
  workspace not strictly inside root    -> refused, precondition exit code, nothing created
  workspace inside root                 -> setup goes on as before
```

- Impactful choice: the eval root file is the user's, git-ignored, and holds a path only; it grants nothing.
- Impactful choice: the claim that a workspace inside a trusted folder skips the trust step is **unproved** until the user's trial reports; the README and the hosts card say so, and say what to withdraw if the trial fails.

## Blast radius

Grade: 1. Only the eval kit, its README and runbooks, and one row of the hosts card change; the CLI, the scenario and the agents do not. A `git revert` restores the previous behaviour.

## Autonomous decisions

- The setup rows of the `copilot` and `claude-planted` runbooks also say the workspace is a new folder inside the eval root, so that the two runbooks do not contradict setup's refusal.

## Known gaps

- The trust inheritance is unproved: it needs the user's trial after the merge (the first `real-direct` run, started from the phone under Remote Control), which no CI can run.

<details>
<summary>Details</summary>

## Changes

- `evals/kit/setup.py`: reads the eval root file and refuses a workspace outside the root, with no file, or with a malformed file, before any campaign runs; the docstring and the printed summary name the root and the file.
- `evals/kit/dry_run.py`: every setup case points the root constant at a temporary file; a new `eval-root` case covers the four outcomes (outside, no file, malformed, inside with the same allow rules and no trust entry).
- `evals/README.md`: Prerequisites name the eval root and say a Foreman campaign still needs the desk; the setup step, "The operator" (a third, away-from-the-desk start, marked unproved), the staged campaign example and "The host's limits" follow.
- The Claude sandbox runbooks' Start paragraphs and Setup rows: the Foreman campaigns say they need the desk.
- `skills/chantier/references/hosts/claude-code.md`: one host-fact row, "Trust of a workspace inside a trusted folder", marked unproved.
- `.gitignore`: `evals/kit/eval-root.local.json`.

## Human decisions

- One eval root folder, trusted once by the user at the desk; every run creates its workspace inside it. chantier never writes, edits or automates a trust or security setting.
- A git-ignored local file, `evals/kit/eval-root.local.json`, names the root; setup refuses a workspace outside it, and refuses when the file is missing.
- Only the campaigns with no Foreman start away from the desk; the docs say plainly that a Foreman campaign still needs the desk.
- The trial checks the phone-started session is on the workspace's main checkout (not a worktree) and records how the session was created.

## Impacts

No visual change. A person running a campaign now writes `evals/kit/eval-root.local.json` once and keeps workspaces inside it.

## Test plan

- [x] New or changed tests (they fail on the previous code): the dry run's new `eval-root` case
- [x] Local gates at `60da054`, carried to `81039ce` by a clean rebase: `just check` (369 passed), `just eval-dry-run` (17 of 17 cases as expected)
- [x] Evidence: no before/after: no visual change
- [x] Review: approved at `3df17b9`, committed as `8b6ee60` (carried from `8b6ee60`: rebased to `81039ce`, patch unchanged)
- [x] Verified at `60da054` (carried from `60da054`, patch unchanged at `81039ce`; setup refusals run by hand: outside, root itself, no file and malformed file each exit 2 and create nothing)
- [x] CI green at `81039ce`: `gh pr checks 266`, 5 checks pass

## Internal references

- CR-312 "Change Specification: evals that start away from the desk", batch-23.
- Order with the pending `evals-rework` change (the specification's section 6): it is not merged, so this change merges first and `evals-rework` carries the eval-root text onto the renamed runbooks.

</details>
