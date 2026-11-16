# A text sent to the forge is written with the Write tool and posted from its file, never from a shell string

## Goal

In batch-14 a Driver built a PR body inside a PowerShell string. An escape sequence put a form
feed into the body, and two description passes failed before the body was posted again from a
file. The cards already show the file form (`--body-file`), but only as an example, and for
GitLab they give only the unsafe form (`--description` with the text as an argument).

After this CR the cards state it as a rule that every role reads. A multi-line text sent to the
forge is authored in a file with the host's Write tool, and the forge command takes it from that
file. Its text is never typed, built or escaped in a shell command, in any shell.

The CR has no tracker issue: no `issue:` line.

## Decisions carried from `02-answers.md`

1. **Scope of texts:** every multi-line text an agent sends to the forge. That covers a PR or MR
   body, a PR, MR or issue comment, and release notes, not only the PR body. The fault is the
   shell string, not the PR.
2. **One-line texts are not covered.** A single line with no Markdown, such as a PR title or a
   short `--note`, stays in the command.
3. **Commit messages are not covered** (out of scope).
4. **Any shell**, not PowerShell only. PowerShell's backtick is given as the example that
   happened. Bash is named too: quotes, `$`, and backticks as command substitution.
5. **The writing tool:** the host's Write tool, or Edit to change an existing file. Never a shell
   write: no redirection, here-string, `Out-File`, `Set-Content` or `echo > file`. A shell write
   brings back the same escapes, and on Windows PowerShell 5.1 a BOM as well.
6. **GitLab:** the same rule holds. The text is authored in the file with the Write tool, and the
   command only passes the file's content on, never text written in the command. Which `glab`
   form does that is for the Driver to settle and prove. The card marks the form **unproved**
   until a trial, as the host references do.
7. **Where the rule lives:** once, in `concepts.md` rule 9, next to the no-BOM sentence.
   `driver.md` turns its examples into "always from the file" and points to rule 9. The Chief of
   Staff's and the Release driver's posts are covered by rule 9 without a line of their own.
8. **No enforcement by the CLI or a test.** This is a card rule only. The CLI runs no forge
   command and knows no role, and the structure tests do not judge behaviour.
9. **No new Inspector check** for control characters in the description pass. The fix belongs at
   the source.
10. **Gates:** `just check` and `just scenario`, because this is a change to the cards.
11. **The Chief of Staff's `glab` example:** the one example in `chief-of-staff.md`,
    `glab issue note <id> --message …`, is replaced with a form that reads the file. It is marked
    unproved like the other `glab` forms. The Chief of Staff still gets no line of its own.

## What changes

Only three cards change: `skills/chantier/references/concepts.md`,
`skills/chantier/references/driver.md` and, for one example,
`skills/chantier/references/chief-of-staff.md`. Nothing changes in the CLI
(`skills/chantier/scripts/`), the agent files (`agents/`, `com.github.copilot/agents/`), the
hooks, the types, the scenario or the tests. The wording below is a target: the Driver may
tighten it, keeping every element named.

### 1. `concepts.md`, Rules, rule 9 ("Commands and files")

Rule 9 now ends with: "Every file you write, a PR body included, is UTF-8 without a byte-order
mark (on Windows PowerShell 5.1, `Out-File` and `Set-Content -Encoding utf8` add one)."

Directly after that sentence, add the rule. It must contain each of these elements:

- **What it covers:** a multi-line text sent to the forge. The examples are a PR or MR body, a
  PR, MR or issue comment, and release notes.
- **Where the text lives:** a file written with the host's Write tool (Edit to change it). The
  file goes in the work folder, or where the card or the project's procedure keeps it (for
  example `work/issue-comment.md` or a release's draft notes).
- **How it reaches the forge:** the forge command takes the text from that file (`--body-file`,
  `--notes-file`, or the forge CLI's equivalent).
- **What is forbidden:** the text is never typed, built or escaped in a shell command, in any
  shell. The file is never written by the shell (a redirection, a here-string, `Out-File`,
  `Set-Content`).
- **Why:** a shell string mangles Markdown. In PowerShell the backtick is the escape character
  (`` `f `` is a form feed: the batch-14 fault). In Bash, `$` and backticks expand, and quotes
  break.
- **What it does not cover:** a one-line text with no Markdown (a PR title, a `--note`) and a
  commit message.

Suggested wording:

> A multi-line text sent to the forge (a PR or MR body, a PR, MR or issue comment, release notes)
> is a file written with the host's Write tool (Edit to change it), in the work folder or where
> your card or the project's procedure keeps it, and the forge command takes it from that file
> (`--body-file`, `--notes-file`, or the forge CLI's equivalent). Its text is never typed, built
> or escaped in a shell command, in any shell, and the file is never written by the shell (a
> redirection, a here-string, `Out-File`, `Set-Content`): PowerShell reads a backtick as an escape
> (`` `f `` is a form feed), Bash expands `$` and backticks, and Markdown is full of both. A
> one-line text with no Markdown (a PR title, a `--note`) and a commit message are not covered.

Constraint from `tests/test_structure.py`
(`test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`): `concepts.md`,
`driver.md` and `chief-of-staff.md` must not contain any name in `HOST_TOOLS` (`SendMessage`,
`send_message`, `write_agent`, `TaskStop`, `ScheduleWakeup`, `start_session`, `create_session`,
`get_session`, `/every`, `/loop`, `/compact`, `/autocompact`, `CLAUDE_CODE_SESSION_ID`,
`COPILOT_AGENT_SESSION_ID`). "Write" and "Edit" are not on that list, and `concepts.md` already
names them.

### 2. `driver.md`: every forge-text example becomes "always from the file"

Each place below gets the file form. The GitLab forms are no longer given as text in an argument.

- **Section "All drivers" (or the shared list above "CR driver"), the "Push" bullet (now lines
  62–67).**
  - Say that a CR Driver **always** opens and edits the PR from `<work folder>/pr-body.md`,
    written with the Write tool as in [concepts](concepts.md), rule 9. Keep
    `gh pr create --draft --body-file <work folder>/pr-body.md` and `gh pr edit --body-file`.
  - Replace `glab mr update --description` and the sentence "`glab mr create --draft` takes the
    body with `--description`" with the GitLab form that passes the file's content, for
    `glab mr create --draft` and for `glab mr update`.
  - Settle that form from `glab`'s own help (for example `glab mr create --help`). If `glab` is
    not installed, write the form generically ("`glab`'s option that reads the description from
    the file").
  - Mark it **unproved** in the card, with the trial that settles it, in the style of
    `hosts/claude-code.md` (an "unproved; trial: …" clause). For example: "unproved; trial: a
    GitLab MR opened and edited from `pr-body.md` whose body holds backticks, `$` and quotes, and
    whose description on the forge matches the file byte for byte".
  - Never give a form whose text is substituted by the shell (such as `"$(cat file)"`) as proved.
    Whatever form the Driver writes stays marked unproved until the trial runs.
- **Section "CR driver" (now line 192):** "`gh pr edit --body-file` again" stays. Add nothing
  else, or a short "(from the file, rule 9)" if the sentence reads better with it.
- **Section "Stack driver" (now line 247):** "`gh pr edit --body-file` / `glab mr update
  --description`". Replace the GitLab half with the same file-based GitLab form as in the Push
  bullet, carrying the same unproved mark (or a pointer to the Push bullet).
- **Section "Release driver", the bullet "The files are the source and the body a copy" (now
  line 305):** "`gh pr edit --body-file`, `glab mr update --description`, or the equivalent for
  another forge". Replace the GitLab form the same way. The bullet already says the body is
  written from the files. Add only the pointer to rule 9 if needed, no new rule (decision 7).
- **The retargeting and draft forms** (`glab mr update --target-branch`, `--draft`, `--ready`)
  carry no text and stay as they are.

### 3. `chief-of-staff.md`, bullet "How to post" (now lines 195–197): one example

- Keep `gh issue comment <link> --body-file <file>` as it is.
- Replace `glab issue note <id> --message …` with the `glab` form that passes the content of the
  file (`work/issue-comment.md`) on, with no text written in the command (decision 11).
- Settle that form from `glab`'s own help, as for the forms in `driver.md`. If `glab` is not
  installed, write it generically.
- Mark it **unproved**, with its trial. For example: "unproved; trial: an issue note posted from
  a file whose text holds backticks, `$` and quotes, and that matches the file on the forge".
- Keep "read the CLI's help for the exact form" and the rest of the bullet.
- Add no other line for the Chief of Staff: rule 9 covers it (decision 7).

### 4. What stays as it is

- `pr-template.md`, `worker.md` (the Inspector's description pass), `release-template.md`, the
  host references, the CLI, the scenario and the tests.

## Out of scope

- A CLI command that posts a body, or a CLI refusal. The CLI runs no forge command and knows no
  role.
- A test that enforces the rule. The structure tests do not judge behaviour.
- A control-character check in the Inspector's description pass.
- Commit messages, and one-line texts with no Markdown (a PR title, a `--note`).
- The content and template of the PR body (`pr-template.md`).
- The eval kit and scorecard (`evals/`). A docs or eval-kit change would be its own item.

## Evidence

At the PR's pushed head:

1. `just check` passes, on the Windows checkout at least. CI covers Linux and macOS.
2. `just scenario` passes, for both forges (`--forge github`, then `--forge gitlab`), unchanged.
   The scenario already opens its PR with `--body-file` (`scenario/run_scenario.py`, `open_pr`).
3. Text checks, each command run with its output in the evidence:
   - `concepts.md` rule 9 holds the new rule, directly after the no-BOM sentence. Show the rule 9
     block (for example
     `git grep -n -A12 "^9\. \*\*Commands and files" -- skills/chantier/references/concepts.md`).
   - No forge-text example in `driver.md` passes the text as an argument any more:
     `git grep -n -e "--description" -e "--message" -e "--body " -e "--notes " -- skills/chantier/references/driver.md`
     returns only the file-based GitLab form, marked unproved, or nothing.
   - The GitLab form in `driver.md` carries the word `unproved` and a trial:
     `git grep -n -e "unproved" -- skills/chantier/references/driver.md`.
   - `driver.md` points to rule 9 from its Push bullet:
     `git grep -n "rule 9" -- skills/chantier/references/driver.md`.
   - `chief-of-staff.md` no longer gives `--message` with the text, and its `glab` form is marked
     unproved:
     `git grep -n -e "glab issue note" -e "unproved" -- skills/chantier/references/chief-of-staff.md`.
4. The diff touches only `skills/chantier/references/concepts.md`,
   `skills/chantier/references/driver.md` and `skills/chantier/references/chief-of-staff.md`
   (plus the cleaned archive, if `take` prints one): `git diff --stat origin/main...HEAD`.

There is no live forge trial of the GitLab forms in this CR: the cards mark them unproved
(decisions 6 and 11).

## Open questions

None.
