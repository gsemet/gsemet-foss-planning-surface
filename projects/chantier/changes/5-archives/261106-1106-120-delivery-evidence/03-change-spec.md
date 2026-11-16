# A CR leaves before and after evidence of what it delivers

Each CR plans what proves its change and leaves that evidence beside its verdict. The cards change;
the CLI does not. A chantier project needs no setup: with no rule written, the Driver judges.

## What the project says

The project's rules rank first: its own `AGENTS.md` and what it links may say what evidence a kind
of change needs and how to capture it, for example with its e2e environment. That is the project's
ordinary text: chantier adds no key, no section and no file for it. Nothing written leaves the
choice to the plan below, never a question to the user.

## The plan

`worker.md`, Investigator: its report before the first round ends with an evidence plan: the kind of
change, what shows it before and after (a screenshot, a command's output, a log, a generated file),
the technique, reusing the project's e2e or test environment when it has one, and what cannot be
shown. A change with nothing to see says so in one line.

`driver.md`, CR Driver: it validates the plan, corrects it if needed, passes it to the Verifier, and
stays responsible for it. A stack Driver's CRs each keep their own.

## The capture

`worker.md`, Verifier: at the end, with the same technique, it captures the before on a detached
worktree of the CR's base, and the after on the pushed head, so the two compare. It removes that
worktree at its end. The files go to `work/verifier/evidence/`, with a `before-after.md` listing
each pair, what it shows and how to reproduce it.

Evidence that cannot be captured: the Verifier writes why in `before-after.md`, and this alone does
not change its verdict. If the project's rules require that evidence, its absence is NOT VERIFIED.

## In the PR or MR

`driver.md`: the Driver, who owns the PR or MR, puts the evidence in its description, before and
after side by side, as the forge's own CLI uploads images and videos (`gh pr edit --attach` on
GitHub, as of `gh` 2.103). The card names no other forge's flag: the Driver reads its CLI's help. A
file that its CLI cannot upload stays in `work/` and the description names it.

## Out of scope

- A new role, and any change to the CLI, the Inspector or the Coder.

## Done when

- `worker.md` and `driver.md` say this.
- `just check` and `just scenario` pass.
