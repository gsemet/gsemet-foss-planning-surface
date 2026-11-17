## Summary

After a compaction of a chantier session on Claude Code, the plugin added a line that sent the model to a reference file, and the role's own skill was never loaded again, so the compacted session worked from the summary's memory of it. The message now names the session's role and tells the model to call its chantier skill again with the argument `reload`. The skills honour that argument and, when the seat says the session holds another role, load that role's skill instead.

## Deliverables

The compaction message, by role (the last role skill loaded in the session):

| Session | Message added after a compaction |
| --- | --- |
| Chief of Staff | `You are the Chief of Staff in a chantier session; after this compaction, call your chantier skill again with the argument reload.` |
| Griller | `You are the Griller in a chantier session; after this compaction, call your chantier skill again with the argument reload.` |
| Router only | `You are in a chantier session; after this compaction, call your chantier skill again with the argument reload.` |

```ts
const reloadLine = (role: string) =>
  `You are ${role in WHO ? `${WHO[role]} in` : 'in'} a chantier session; after this compaction, call your chantier skill again with the argument reload.`
// skill.prompt: the loaded role moves to the end of the list
update($, roles, list => [...list.filter(n => n !== name), name])
```

Choices: the message names no skill; the role is the last one loaded; the reload reads the seat first and follows it when it disagrees with the message; no pane change.

## Blast radius

Grade: **1**. A hook message and the reload cards and skill text; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The reload byte limit of the startup manifest (12288) left no room for the specified wording: the reload sentences are shorter than the specification's, the "5. Reload" step drops the explicit rename and "take no seat" clauses, and some existing prose of the four thin skill files (the sync-failure parenthesis, the "Nothing to install" paragraphs, part of the Chief of Staff's description) was trimmed to fit. The alternative was raising the limit, which is the user's call.
- The role-choice test is three generated tests instead of one parametrized test, because each case needs a fresh session.

## Known gaps

- The automatic reload is not seen in a real session: which skill the model calls on the message (the role's or the router), and that the seat hop and the router's delegation load the right one, are unproved until the trial in the host reference.
- The argument `reload` of the Chief of Staff and Griller skills is unproved until that trial.
- The pane goes back to its first page after a reload, as on any skill load (the engine's skill event carries no argument).
- The reload wording is shorter than specified and some existing skill prose was trimmed (see Autonomous decisions).

<details>
<summary>Details</summary>

## Changes

- `hooks/register.tsx`: `reloadLine(role)` replaces the fixed line; the roles list keeps load order (a re-load moves a role to the end); the compaction hook sends the line of the last role that is not the router.
- `skills/chief-of-staff/SKILL.md`, `skills/griller/SKILL.md`, `skills/chantier/SKILL.md`: the argument `reload` follows "5. Reload"; the router delegates to the session's role skill.
- `skills/chantier/references/session-start.md`: "5. Reload" reads the seat first.
- `skills/chantier/references/hosts/claude-code.md`, `skills/chantier/references/hosts/copilot.md` and the root `README.md`: the new message, the manual reload lines and the trial.
- `skills/status/SKILL.md` and `types/index.d.ts`: the sync-failure wording of the thin skill is shortened to fit the reload limit, and the `roles` comment says "the reload message".
- `hooks/register.test.tsx`: the expected lines and the role choice.

## Impacts

No visual change. A compacted session calls its skill again.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `6cb7984` (carried from 6cb7984): `just check` pass (455 passed), `just mod` pass (65 pass)
- [x] Evidence: none, no visible change
- [x] Review: approved at `47abe26`, committed as `6cb7984` (carried from 6cb7984)
- [x] Verified at `6cb7984` (carried from 6cb7984)
- [x] CI green at `796686b`

## Internal references

- CR-334 compaction-reload-loads-skill

</details>
