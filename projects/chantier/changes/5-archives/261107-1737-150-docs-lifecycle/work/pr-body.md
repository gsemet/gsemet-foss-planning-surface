## Summary

The docs still described the old batch ("land", a Foreman as the only steering) and lacked what shipped recently. They now say what Chantier does today: a batch is running, then paused, then closed on your word, steered by a Foreman or, in direct mode, by the Chief of Staff itself.

## Deliverables

New and changed diagrams, plus one use-case document per configuration:

| Before | After |
| --- | --- |
| `docs/use-cases.md` (one page) | `use-cases.md` (common), `use-cases-foreman.md`, `use-cases-direct.md` |
| no batch-lifecycle diagram | `docs/batch-lifecycle.svg` (running, paused, closed) |
| Foreman path only in `how-chantier-works*.svg` | Foreman and direct-mode paths, spec-writer shown |

## Changes

- `docs/batch-lifecycle.svg` is new; `how-chantier-works`, `how-chantier-works-simple`, `cr-lifecycle` and `cr-lifecycle-simple` SVGs updated, with their `-texts.md` companions (one new for the simple diagram).
- README: both steerings, spec-writer, PR template, board slots, hosts for direct mode, costs; the use-case links.
- Tutorial: init, grill and restatement, twelve agents, direct mode pointer.
- Use cases split by configuration.

## Impacts

Documentation only. The SVGs are the ones approved as prototypes, copied unchanged.

## Blast radius

Grade: 1. Docs and diagrams only; a plain `git revert` restores them.

## Test plan

- [x] New or changed tests (they fail on the previous code) No behaviour change
- [x] Local gates: `just check` passes; SVGs parse as XML; every relative link resolves; descriptions equal companions
- [x] Evidence: no visual change beyond the approved diagrams
- [x] Review
- [x] CI green

## Autonomous decisions

- The five SVGs are delivered byte for byte as approved; none needed a text change.

## Internal references

CR-150 docs-lifecycle

