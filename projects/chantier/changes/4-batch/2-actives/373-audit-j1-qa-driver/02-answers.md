Short name: `audit-qa`

# Answers

No user answer: the user asks no questions on this CR (the Chief of Staff, 2026-11-18). The
request's scope stands as written; behaviour questions go back to the Chief of Staff (settled
below).

## Settled by the spec-writer (2026-11-18)

Points of implementation that change no user-visible behaviour of chantier (the cards, the CLI,
the plugin); each only makes the audit read what the cards already say.

1. **The form.** `audit.py` accepts the QA driver's first line only for the role `qa-driver`:
   `chantier qa-driver for <folder> of batch <batch>, in the project <root>.`. Its `role` is
   `qa-driver`, its `what` is `<folder>` as written. Another role with a folder in that place
   (`chantier coder for <folder> of batch ...`) is still no recognised form and still fails J1.
   The batch named in the line is not compared with the audited batch (no check does that for
   the other forms either).
2. **Its card and rules line.** As every Driver: its prompt names `references/driver.md` and
   holds `$CHANTIER rules` (the skeleton `order qa` prints, `driver_prompt.py`'s
   `driver_prompt_lines`, gives both). Nothing new is asked of it.
3. **Its worktree.** `driver.md`, "QA driver", tells it to create a detached worktree of its own
   (`git worktree add --detach <repo>.worktrees/<folder name> <remote>/<default branch>`). The
   audit's J3 check "creates no worktree", which lists `qa-driver` since before that card changed
   (commit e33084a0), accepts a detached `git worktree add` from a QA driver, as it does the
   Verifier's; a non-detached one still fails J3.
4. **Its own files.** The card sends everything to its QA folder (`04-result.md`, `evidence/`,
   long tests). J3's "writes no code itself" counts a QA driver's write inside the folder its
   first line names as its own, like `/work/` and `/evidence/`; a write elsewhere still fails J3.
5. **The proof.** One dry-run case, `audit-qa-prompt`, whose first line is read from the shipped
   agent file (`agents/qa-driver.md`, its "Prompt starts with:"), with planted breaches that must
   still fail.
6. **No scorecard change.** `evals/SCORECARD.md`'s J1, J2, J3 and J4 wordings hold: J3's "no
   worker creates a worktree (except the Verifier's detached one)" is about workers, and the QA
   driver is a Driver.

## Settled by the Chief of Staff (2026-11-18, the user asks no questions)
- In direct mode the audit also checks a QA driver the Chief of Staff starts in the batch, as a Driver of the batch (one line in `load_agents`, one more dry-run variant).

