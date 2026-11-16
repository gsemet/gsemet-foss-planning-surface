# A refused force push goes up to the Chief of Staff

When the host refuses a Driver `git push --force-with-lease`, the Chief of Staff runs the push: the
stack no longer waits for the user. This CR changes the cards; the CLI gets no new command.

## The route

- `driver.md`: a plain push when the remote branch is an ancestor of the local one, force only for
  a rewrite. On a refused force push, the Driver has its work committed and sends the Foreman the
  branch, the remote head it expects and the local head, then waits.
- `foreman.md`: it passes that line to the Chief of Staff, and tells the Driver once it is done.
- `chief-of-staff.md`: on that line it runs, from the main checkout, without changing its branch,
  `git push --force-with-lease=<branch>:<expected> <remote> <local head>:refs/heads/<branch>`.
  This is the one exception to "do no Driver's work". It answers the Foreman with the result.
- `routing.md` shows the route; both hosts' agent files follow only if they name it.

## Limits

- Only a branch the batch's state names for one of its CRs, never the default branch.
- A failed lease is not retried: the remote moved, and the Driver looks at why.
- If the Chief of Staff's own push is refused, it stops and shows the user the exact text, as for
  any `refused`. No other way around, and it never touches permission settings.

## Done when

- The cards say this, and `refused` for any other action still goes to the user as today.
- `just check` and `just scenario` pass.
