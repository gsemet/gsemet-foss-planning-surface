# A PR body is written with the Write tool and posted from its file, never from a shell string

## The request

Batch-14's retro: a Driver built a PR body inside a PowerShell string; an escape sequence put a
form feed into the body, and two description passes failed before the body was posted again from
a file. The request: the cards say the PR body is always written with the Write tool and posted
with `--body-file`, never built in a PowerShell string.

## The problem

- The cards already show the right way, but only as an example. `driver.md` (Push) gives
  `gh pr create --draft --body-file <work folder>/pr-body.md` and `gh pr edit --body-file`, and
  `concepts.md` rule 9 says a PR body is UTF-8 without a BOM. No line says "never another way",
  so a Driver in a hurry types the text in the command.
- A shell string is not a safe carrier for Markdown: PowerShell reads the backtick as its escape
  character (`` `f `` is a form feed, `` `n `` a newline, `` `t `` a tab), and Markdown is full of
  backticks. Quotes and `$` break the same way, and Bash has its own cases.
- For GitLab the card gives `glab mr create --draft` with `--description`, which takes the text
  as an argument: the card leaves that host with the unsafe form only.
- The cost: two failed description passes of the Inspector and a re-post, on a fault that is
  not about the change at all.

## What would fix it

The cards state the rule as a rule: a text sent to the forge (a PR or MR body first) is a file
written with the Write tool in the work folder, and the forge command takes it from that file;
its content is never typed, built or escaped in a shell command. `concepts.md` rule 9 holds the
rule for everyone, `driver.md` (Push, and the places that edit the description) says "always",
and the GitLab form is given so that the text still comes from the file.

## Out of scope

- A CLI command that posts the body, or a CLI refusal: the CLI runs no forge command.
- A new check of control characters in the Inspector's description pass: the pass caught the
  fault as it is.
- Commit messages and one-line texts (a PR title): no fault measured.
- The content and template of the PR body (`pr-template.md`).
