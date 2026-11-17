# The Foreman plans the release

Owner's request (2026-11-04), from the P1 backlog item `release-stability-heavy-runs-before-version`:
the real VS Code jobs stay on `main`, with no heavy jobs on pull requests and no nightly run. Stacking
the release commit on top of development is the mistake: the Foreman takes part in the release, starts
the release driver once the stack is merged, and handles the small problems.
