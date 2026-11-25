# Getting started: chantier on a new, empty planning surface

Priority P3, later. The user, 2026-11-20, on CR-404's decision (a surface whose origin/HEAD is unset is refused with the fix `git remote set-head origin -a`, no guessed default branch).

1. **Getting-started guide.** A guide to turn chantier on for a new project on a new, empty planning surface: create the surface repository, its first commit and push, set the default branch, the project's folder and its `chantier.yaml`, the `planning:` line in the code repository's AGENTS.md, start the surface server (`chantier board --seat`) and check its `writer:` line, and what the first `open` needs.

2. **Where the surface's branch comes from.** Besides origin/HEAD, the branch the surface server writes to can be stated explicitly, in the surface's AGENTS.md (or its `chantier.yaml`), or read from the checkout's tracked branch (its upstream). These are explicit sources, not a fallback: with none of them set, the refusal stays and its message names all three ways to fix it. The guide shows them.
