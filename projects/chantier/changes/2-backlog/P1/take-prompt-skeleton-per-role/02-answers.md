# Answers

## take-skeleton-Q1: what `take` prints

2026-11-17, the user chose the recommended answer: `take` prints the whole prompt skeleton for the CR's Driver role (its first line, the card to name, and, for a release, stack or QA CR, no `writes:` line), ready to give to the Driver.

Spec critic: yes, it changes what `take` prints and how every Driver is started.

## Spec questions (2026-11-17)

- take-skeleton-Q2 (archive path on `writes:`): the skeleton prints the archive as an absolute path, `<worktree>/<archive path>`; the CLI test checks it; `driver.md` and `hosts/claude-code.md` say "absolute".
- take-skeleton-Q3 (stack driver skeleton): the stack-driver block has its own shape; it carries the stack rows as printed; its `Team:` is filled from `playbook --batch`.
- take-skeleton-Q4 (QA driver): yes, `order qa` also prints the `qa-driver` skeleton.
