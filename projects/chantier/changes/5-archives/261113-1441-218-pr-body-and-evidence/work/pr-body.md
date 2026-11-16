## Summary

A PR that says it is ready used to hide what it did not do. A known defect accepted, a claim
not proven, a part left out: none had a place in the body, and the ready message quoted none of
them. Agent role names in the body also caused repeated rewrites, even where the PR's subject
was that role's own card. This change makes the body name its gaps, fixes one rule for role
names, and asks for a real screenshot when this repository's board pane changes.

## Deliverables

- **Known gaps**: a new visible section after Autonomous decisions in the PR template, with its
  rule and its audit item. Each `UNVERIFIED` claim, each evidence pair not captured and each
  accepted defect has its bullet; "None" when there is none.
- **The ready line quotes the gaps**: `handback <cr> ready <link> gaps: <gap>; <gap>`, carried by
  the Foreman's ready asks and quoted by the Chief of Staff to the user next to the link.
- **One rule for role names**: a role name is an internal reference when it says who did the work;
  it may appear anywhere when it is a term of the product the diff changes (a change to that
  role's card). The Driver reads the body against the audit once before each post.
- **Board pane screenshot, for this repository**: a change to what the CR board pane draws
  carries one screenshot from a real Claude Code session, captioned with the head SHA; until then
  Known gaps names it and the Chief of Staff asks the user for one.

```text
gap in pr-body.md  ->  handback ... gaps: ...  ->  Foreman ask  ->  Chief of Staff -> the user
```

## Blast radius

Grade: **1**. Cards and docs only, no CLI, hook or agent-file change; a `git revert` restores
the previous behaviour.

## Autonomous decisions

- The three open questions took the specification's defaults (role names as product terms,
  a visible Known gaps section, the user takes the screenshot).
- The audit item for Known gaps is added as item 10 rather than renumbering the list.
- The role-name check before each post is a card rule, not a CLI check: the CLI cannot tell a
  product term from the doer of the work.
- The `--plugin-dir` means for running a PR's head is written from the read-only investigation
  and marked unproved where it is.

## Known gaps

- **The `--plugin-dir` means is unproved**: that it replaces the installed copy of the same name,
  that the board pane draws from it, and that Claude Desktop accepts the flag. It needs an
  interactive session; `CONTRIBUTING.md` says so.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/pr-template.md`: Known gaps rule, section and audit item 10; the
  role-name rule, template comment and audit item 3.
- `skills/chantier/references/driver.md`: `gaps:` on the ready line, the read of the body before
  each post, the `evidence:` note.
- `skills/chantier/references/worker.md`: the Verifier's description pass judges Known gaps and
  role names.
- `skills/chantier/references/foreman.md`, `chief-of-staff.md`: the asks carry the gaps; the
  screenshot flow.
- `AGENTS.md`, `CONTRIBUTING.md`: the board pane screenshot rule and how a session runs a
  head.
- `docs/use-cases.md`, `scenario/run_scenario.py`: the template's sections and the scripted body.

## Impacts

No visual change: the board is not touched.

## Test plan

- [x] No behaviour change in code; the cards are text <!-- structure tests unchanged -->
- [x] Local gates at `ef20ec7`: `just check` and `just scenario` pass
- [x] Evidence: No visual change, no before/after
- [x] Review: approved at `ef20ec7`
- [x] Verified at `ef20ec7`
- [x] CI green at `ef20ec7`: `gh pr checks 160`, 5 checks pass

## Internal references

CR-218 pr-body-and-evidence (batch-16). Source: three batch-15 retro items
(`name-left-gaps-in-pr`, `pr-body-role-names`, `board-ui-screenshot`).

</details>
