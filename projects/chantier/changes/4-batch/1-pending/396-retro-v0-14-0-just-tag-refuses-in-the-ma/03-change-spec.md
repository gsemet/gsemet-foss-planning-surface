# `just tag` fast-forwards the main checkout before it tags

## Goal

After the user merges a version PR, `just tag` runs from the main checkout and works there, even
when that checkout is still on the previous version. In v0.14.0 (CR-388), the main checkout was
still at v0.13.0 after the merge of PR #356. `check-tag` reads the local version, so it refused,
and the Driver ran `just tag` from the release worktree instead.

From now on the `tag` recipe fast-forwards the main checkout to `origin/main` first. It never
forces anything. When it cannot fast-forward, it stops and says what to do. After the
fast-forward, `check-tag` and `show` read the local version as they do today, and that version is
now origin/main's.

## What changes

### 1. `scripts/version.py`: a new `ff-main` subcommand

Add a function `ff_main(root: Path = ROOT) -> int` and a subcommand `ff-main` (help: "fast-forward
the main checkout to origin/main; refuse when not on main, with tracked changes, or when it is not a
fast-forward"). Every git call is `subprocess.run([...], cwd=root, capture_output=True, text=True,
encoding="utf-8", check=False)`, the same way `check_tag` calls git. Writing it in Python keeps the
recipe portable: the justfile runs PowerShell on Windows and sh elsewhere, so the logic cannot go in
shell.

The steps, in this order. The first refusal stops the run: it prints one line on stderr that starts
`just tag:` and returns 1, and nothing in the checkout has changed.

1. `git symbolic-ref --quiet --short HEAD` must print `main`. Refusals:
   - another branch: `just tag: the checkout is on <branch>, not main: run just tag from the main checkout, on main`;
   - a detached HEAD (non-zero exit): `just tag: detached HEAD, not main: run just tag from the main checkout, on main`.

   A linked worktree (a release worktree) is on its own branch, so this step refuses it too.
2. `git status --porcelain --untracked-files=no` must print nothing. Otherwise: `just tag: the main
   checkout has tracked changes (<up to three paths>): commit or set them aside yourself, then run
   just tag again`. Untracked files are never listed, read, moved or deleted.
3. `git fetch origin main`. If it fails: `just tag: fetch failed: <git's stderr, first line>`.
4. Record `git rev-parse HEAD` as `<before>`. Then run `git merge --ff-only --no-overwrite-ignore
   origin/main`, in exactly this form. Never `pull`, `reset`, `rebase`, `stash`, `clean`,
   `checkout`, `switch`, `--force`, or a merge missing either flag. This is the same form as
   foreman.md's "The main checkout after a merge". `--no-overwrite-ignore` matters: without it, git
   overwrites an ignored file that the incoming commits add. If git refuses: `just tag: main cannot
   fast-forward to origin/main (<git's reason, first line>): nothing was changed; settle main by hand,
   then run just tag again`. No retry, and no other way is tried.
5. On success, print one line on stdout: `main checkout: fast-forwarded to <sha7>`, or `main
   checkout: already at <sha7>` when `<before>` equals the new HEAD. When `git diff --quiet <before>
   HEAD -- uv.lock` exits 1, add `; uv.lock changed: sync pending` to the same line. A version
   commit always changes `uv.lock`, because the chantier entry carries the version. This tool never
   runs `uv sync`. Return 0.

The remote (`origin`) and the branch (`main`) stay hard-coded, as they already are in `check-tag`
and in the recipe. Update the module docstring's usage block with the new subcommand.

### 2. `justfile`: the `tag` recipe

Replace the recipe's `git fetch origin main` line with the fast-forward, so it reads:

```
# After the release PR is merged, from the main checkout: fast-forward main, tag the version on origin/main and push the tag
tag:
    uv run --script scripts/version.py ff-main
    uv run --script scripts/version.py check-tag
    git tag "v$(uv run --script scripts/version.py show)" origin/main
    git push origin "v$(uv run --script scripts/version.py show)"
```

`check-tag` itself does not change: it reads the local version, which now equals origin/main's. A
non-zero exit from `ff-main` stops the recipe before the tag on all three systems. Both `sh` and
`powershell.exe -Command` (the `windows-shell`) report a failing native command's exit code to
`just`, as `check-tag` already depends on today. Since `version.py` locates `ROOT` from its own
path, `just --justfile <main checkout>/justfile tag`, run from any folder, acts on the main
checkout.

### 3. CONTRIBUTING.md "Release", step 4

Rewrite step 4 to say:

- It runs from the main checkout, on `main` (`just tag`, or `just --justfile <main checkout>/justfile tag`).
- `just tag` first fast-forwards the main checkout to `origin/main`, and never by force. It refuses,
  changing nothing, in four cases: the checkout is not on `main`, it has tracked changes, the fetch
  fails, or main cannot fast-forward. Each refusal says what to do; the user settles the checkout by
  hand and runs `just tag` again.
- It then refuses unless origin/main's head is the `release: vX.Y.Z` commit of the local version
  (the existing sentence, kept), so a commit pushed after the merge never gets the tag.
- Its `main checkout: ...` line says when `uv.lock` changed. In chantier's own checkout, the sync
  then follows (the moment AGENTS.md names: "after a merge that changes `uv.lock`").

Leave steps 1 to 3, 5 and 6 unchanged.

### 4. The cards: the Release driver hands `just tag` to the steering session

No Driver moves the main checkout, and that rule stays as it is. Two passages are **not** changed:

- `driver.md`, the bullet "Every git command a Driver runs names its worktree" ("The main checkout
  is read-only for a Driver");
- `concepts.md` rule 8 ("The main checkout moves only by the steering session's `merge --ff-only
  --no-overwrite-ignore` after a merge it records, and only when clean").

The recipe's fast-forward is the steering session's own. It runs after the release merge that the
steering session recorded, with the same command, and refuses unless the checkout is clean.
`ff-main` stays in the recipe as the guard. The steering session's post-merge fast-forward
(foreman.md, "The main checkout after a merge") has normally already run by then, so `ff-main`
prints `already at`.

There is no `release-driver.md` card: the Release driver is the `## Release driver` section of
`skills/chantier/references/driver.md`. The steering session is the Foreman, or the Chief of Staff in
direct mode, who does the Foreman's work by `foreman.md`.

Below, "the main-checkout step" means a step of the project's release procedure that runs in the
main checkout. For chantier, that is CONTRIBUTING.md "Release" step 4, `just tag`. With a planning
surface, the step runs in the project's clone that `take` names, the same checkout the post-merge
fast-forward uses.

**`driver.md`, `## Release driver`, the bullet "A release PR merged ...": one new sub-bullet.**

- The main-checkout step is never the Driver's. The Driver never runs it, neither in the main
  checkout nor in its worktree.
- When the procedure reaches that step, the existing approval rule applies first, unchanged: a held
  step with no approval gets `handback blocked approval: <step>`.
- Once the step is approved, the Driver writes a `note` that names the steps already run. Then it
  hands back `handback blocked waits: the steering session runs <the step> in the main checkout`,
  quoting the step as the procedure writes it (for chantier, `just tag`).
- A take note that starts `tag done:` means the steering session ran the step. The Driver goes on
  from the procedure's next step and never runs that step again.
- The Driver checks the step's result read-only, where it can (for chantier, `git -C <worktree>
  ls-remote --tags origin v<X.Y.Z>`). If the tag is missing, it hands back `handback blocked
  question:` and names the missing tag.
- The existing bullet that ends "name in a `note` the steps of the procedure already run (for
  chantier, `just tag`)" stays. The steps already run now include the steering session's `tag
  done:`.

**`foreman.md`, the bullet "A Release driver takes the release CR ...": new sentences right after
the `publication done:` take-back.**

- A release handed back `blocked waits: the steering session runs <step> in the main checkout` is
  yours to run at once. Run it in the checkout the post-merge fast-forward uses: the main checkout,
  or with a planning surface the project's clone. For chantier that is `just --justfile <that
  checkout>/justfile tag`, as one command with nothing chained. Your own post-merge fast-forward
  has already run; the recipe fast-forwards again as its guard.
- It succeeds:
  - copy the recipe's `main checkout:` line word for word into `$CHANTIER note <release-cr> "<the
    line>"`. A `uv.lock changed: sync pending` in it reaches the Chief of Staff, who syncs, as after
    your own fast-forward;
  - then take the CR back by the usual take-back path (`agents set <cr> -` first when the id is
    still recorded): `take <release-cr> --note "tag done: steering session, <YYYY-MM-DD>: v<X.Y.Z>
    pushed"`.
- It refuses (a `just tag:` line), or the host refuses the command:
  - change nothing, try no other way, never force;
  - send it to the Chief of Staff: `[foreman→chief-of-staff] release <cr>: <step> refused: <the
    exact line>`;
  - in direct mode you are the Chief of Staff, and take it to the user yourself, as
    `chief-of-staff.md` says below.
- The step's approval is the user's word, which the Driver checked before its hand-back. You run
  nothing the Driver did not hand back.

**`chief-of-staff.md`, the release section, next to "The publication refused by the host": one new
paragraph.**

- It covers a refused main-checkout step: the line `release <cr>: <step> refused: <line>` from the
  Foreman, or the refusal seen by you in direct mode.
- Give the user a **For you** line with the refusal and what it says to do. For example: "the main
  checkout has tracked changes (...): commit or set them aside, then tell me to run `just tag`
  again". You never settle the checkout yourself.
- When the user says to run it again:
  - in Foreman mode, send `[chief-of-staff→foreman] release <cr>: run <step> again`, and the Foreman
    runs it as above;
  - in direct mode, run it yourself, as above.
- The ready ask's naming of the approved steps (CONTRIBUTING.md step 4, `just tag`) is unchanged.

Nothing else changes:

- No change to `agents/` or `com.github.copilot/agents/`.
- No change to the CLI's `src/`. The hand-back reason is free text, and a `waits:` reason already
  prints "the Foreman takes it back when that lands".
- If any edited text is in a startup core, keep the startup-size test (`STARTUP_LIMIT` in
  `skills/chantier/scripts/cli/tests/test_plugin_files.py`) passing.

## Decisions carried from 02-answers.md

1. The fast-forward (`git fetch`, then `git merge --ff-only origin/main`, refusing if the checkout
   is dirty or not on main) lives in the `tag` recipe, through `version.py ff-main`, so no agent
   has to remember it. `check-tag` keeps reading the local version: section 1, section 2.
2. Never a forced update. A refusal stops the step and says what to do: section 1, steps 1 to 4;
   section 4, the refusal paths.
3. CONTRIBUTING.md "Release" and the cards that name the release steps are updated: section 3,
   section 4.
4. Linux, macOS and Windows: the logic is in Python, and the recipe's lines are plain commands that
   both shells run: section 2.
5. The read-only main checkout stays whole: no Driver moves it. The Release driver hands `just tag`
   to the steering session (the Foreman, or the Chief of Staff in direct mode), which runs it in the
   main checkout. `ff-main` stays in the recipe as the guard. `driver.md` and `concepts.md` rule 8
   get no exception: section 4.

## Out of scope

- Making `check-tag` read the version at `origin/main` instead of the local one (the intent's other
  option, set aside by decision 1).
- The steering session's post-merge fast-forward (foreman.md): unchanged. Both may run, and the
  second one prints `already at`.
- Any remote or default branch other than `origin`/`main`.
- Refusing a linked worktree that has `main` checked out: git does not allow two checkouts of one
  branch, so step 1 already covers this case.
- `just release`, and steps 1 to 3, 5 and 6 of the procedure. Step 5, the publication, stays the
  Release driver's, as today.
- Running `uv sync` from the recipe.
- A new allow rule for `just tag`: the host card's release-grant row already names it "the
  project's own, no rule offered".

## Evidence

- `just check` passes on the PR's head (Linux, macOS and Windows in CI).
- One new test in `skills/chantier/scripts/cli/tests/test_plugin_files.py`:
  - It loads the shipped `scripts/version.py` through `_version_script()` (the repository's file at
    the head under test) and calls `ff_main(root)`.
  - It is parametrized over git repositories prepared in `tmp_path`: a bare `origin`, plus a clone
    with `main` checked out (git's identity set locally for the commits).
  - Each case asserts the return code, the first words of the stderr or stdout line, and `git
    rev-parse HEAD` before and after:
    - behind origin/main by one commit that touches `uv.lock`: returns 0, `fast-forwarded to`, `uv.lock changed: sync pending`, HEAD equals origin/main;
    - already at origin/main: returns 0, `already at`;
    - on another branch: returns 1, `is on`, HEAD unchanged;
    - a tracked file modified: returns 1, `tracked changes`, the file's content unchanged;
    - diverged (one local commit not on origin): returns 1, `cannot fast-forward`, HEAD unchanged;
    - an untracked file present while behind: returns 0, and the untracked file is still there.
  - The prepared repositories are cases the shipped checkout cannot hold (refusals, a divergence),
    and are named as such. The shipped file itself is what runs.
- A structure assertion on the shipped `justfile`: the `tag` recipe's first command line is `uv run
  --script scripts/version.py ff-main`, and it comes before `check-tag`.
- A structure assertion on the shipped cards, read from the repository at the head under test:
  - `driver.md`'s Release driver section holds the hand-back `blocked waits: the steering session
    runs`;
  - `foreman.md` holds the matching take-back `tag done: steering session`.

  The test checks both phrases together, so renaming one in a single card fails it.
- `just tag` itself is not run in CI, because it pushes a tag. The steering session's hand-off is
  first proved at the next release. The PR's Known gaps names both.
- Host matrix: none. The recipe and the hand-off act the same whatever the host (Claude Code or
  Copilot) and whatever the configuration.
- The Driver also runs `just scenario`, since the CR changes cards (AGENTS.md, the long gate).

## Open questions

None.
