## Summary

The README had grown into a long reference that was hard to read in one go. It now opens with a clearer introduction (what a Change Request is, how work goes in batches, direct or Foreman mode, and that chantier respects the project's own rules), shows the "How chantier works" diagrams from the detailed view to the two simple ones, and keeps the detailed end (boards, gates, agents and models, the planning folder, hosts, costs) on pages under `docs/`, linked from a new "More" section. No text is lost: the moved blocks are verbatim.

## Deliverables

Where the detailed end of the README went:

| README section before | Now |
| --- | --- |
| The CR board, the remote board | `docs/boards.md` |
| Your gates | `docs/gates.md` |
| Your own agents, Models | `docs/agents-and-models.md` |
| Change Request lifecycle (the planning folder) | `docs/planning-folder.md` |
| Supported hosts | `docs/hosts.md` |
| Costs and budgets | `docs/costs.md` |

- The introduction holds five bullets: Change Requests beside your tracker, working in batches, one person to talk to, direct or Foreman (and why pick one), respect the project's rules.
- The three diagrams are in the order detailed, Foreman, direct; no SVG changed.
- Links that pointed at a moved section (the tutorial and three agent reference cards) now point at the new pages.

## Blast radius

Grade: 1. Documentation and link text only; a `git revert` restores the previous README.

## Autonomous decisions

- The README's line numbers in the specification were approximate against the current base, so the blocks were located by heading.

<details>
<summary>Details</summary>

## Changes

- `README.md`: new introduction, diagrams reordered with a new lead-in, six blocks removed, a "More" section, the gates link and the `docs/` line in "Repository layout" updated.
- Six new pages under `docs/`, each with a title, an opening line, heading levels lowered by one and relative links rewritten.
- `docs/tutorial-claude-code.md`, `skills/chantier/references/chief-of-staff.md`, `init.md` and `hosts/claude-code.md`: the reference to the moved README section now names the new page.

## Impacts

No behaviour change. Readers find the detail one click away from the README.

## Test plan

- [x] New or changed tests: No behaviour change
- [x] Local gates at `9baa081`: `just check`, `just scenario`
- [x] Evidence: no-content-lost check (217 non-blank lines compared, only the two replaced headings differ) and dangling-anchor search
- [x] Review: approved at `9baa081` (patch-identical to the reviewed round)
- [x] Verified at `9baa081`
- [x] CI green at `9baa081`

## Internal references

- CR-195 readme-reorg
</details>
