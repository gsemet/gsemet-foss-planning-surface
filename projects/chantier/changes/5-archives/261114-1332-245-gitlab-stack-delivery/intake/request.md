Define and prove how chantier delivers a stack on GitLab, so "a stack on GitHub and GitLab" is true.

The user (2026-11-14): chantier must deliver stacks "dans une variété de cas", on GitHub and GitLab, with the skill and the CLI given the tools to do it.

Found by the critic's review (Fable, 2026-11-14):
- `forge-stack` refuses any non-GitHub link, `show` included (`commands/forge_stack.py:18-21, 46-51`), so the five checks cannot run (`foreman.md:181-182`, "GitHub only").
- `driver.md:435-437`: on GitLab the stack stays a chain, the first MR ready and the others drafts; "stack-ready" is undefined there, there is no one-action merge, and each merge forces a full restack (`driver.md:454-460`).
- Every GitLab form is "unproved" (`chief-of-staff.md:336`, `driver.md:155-157`).

Wanted:
- what a ready stack is on GitLab: the chain's checks (each MR's target is the branch below, the first on the default branch, CI green at the top, the order of `take stack`), read by `forge-stack show` on GitLab too;
- the merge sequence the user follows (or a merge train when the project has one), and what chantier does after each merge (retarget, restack), written in the cards;
- one real run on a GitLab project, recorded, before the GitLab forms lose "unproved".
## The user's word (2026-11-14)

"GitLab, on testera plus tard. Fais au mieux." Design GitLab's stack delivery as well as can be done from the docs and the existing GitLab forms, with no real run for now; the forms stay marked "unproved" until a real GitLab run, done later. Lowered to P2.