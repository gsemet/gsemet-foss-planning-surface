# What main already has (2026-11-10, main at de9ea80)

Checked by the Chief of Staff when the item was filed, after pulling main.

- **Rule 5, draft until mergeable: mostly there.**
  - `concepts.md` "Ready to merge": a CR's PR whose CR was handed back `ready` on the default branch; any other is a draft.
  - `driver.md`: a CR Driver opens its PR as a draft, turns it ready at hand-back, and back to a draft when the CR returns to a Driver.
  - Missing: in a stack, a PR on another base stays a draft (`driver.md`, stack driver). The issue wants each stacked PR to turn ready on its own once mergeable.
- **Rules 1 to 4 (tracker comments, links both ways, closing keyword, "Released in"): not there.**
  - No `issue:` line, no closing keyword in `pr-template.md`, no tracker comment by the Chief of Staff.
  - `session-start.md` only says a CR is one level over the tracker's issues.
- **`tracker-grill-summary`**, the planning item the issue says it replaces, was found neither in this repository nor in the planning surface.
