# Answers: ci-artifacts-out-of-plan

## 2026-11-20, grilled by the Chief of Staff alone

Every answer below: Settled by the Chief of Staff (2026-11-20, the user asks no questions).

Q1. Which pattern does the managed `.gitignore` gain?

`**/work/**/artifacts-*/`, the request's own, and nothing wider (not `**/artifacts-*/`).
Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the request names
it; a wider pattern would hide a folder a user means to publish outside `work/`.

Q2. The CLI's own reading of the ignore patterns (`store/base.py`, `_matches`) takes a `**` only
at a pattern's start. Does it learn the middle `**`?

Yes: a `**` name inside a pattern matches zero or more folders, as git reads it, so `published`
and git agree on the new line. Settled by the Chief of Staff (2026-11-20, the user asks no
questions). Reason: the store's rule is that it agrees with the `.gitignore` it writes; without
it `work/artifacts-1/` and `work/a/b/artifacts-1/` would be ignored by git and called published
by the CLI.

Q3. Where do the cards send a downloaded CI artifact?

`<CR folder>/work/scratch/artifacts-<run id>/`, for the Driver, the debugger and the verifier;
what proves a claim is copied from there, small, into `evidence/`. The failed-jobs log keeps its
place (`<work folder>/ci-<run>.log`, already ignored). Settled by the Chief of Staff (2026-11-20,
the user asks no questions). Reason: the request names the three roles and `work/scratch/`; the
log rule already keeps logs out.

Q4. Which cards change?

`driver.md`, `debugger.md`, `verifier.md`, and the two sentences of `concepts.md` that list what
the `.gitignore` keeps out; `docs/planning-folder.md` and `docs/planning-modes.md` list the same.
The investigator, the coder and the inspector are not changed. Settled by the Chief of Staff
(2026-11-20, the user asks no questions). Reason: the request names three roles; the ignore line
covers an agent that misses the rule.

Q5. How does the writer say a path is too long?

Its own blocked reason, `path-too-long`, with the path's length and its start in the text and the
rule in the way out (move it under the CR's `work/scratch/`, where downloaded CI artifacts go, or
shorten it). It is a failed git step like `git-error`: blocked at the second cycle in a row, one
`sync-blocked@1` per episode, `sync-resumed@1` when a cycle completes. Settled by the Chief of
Staff (2026-11-20, the user asks no questions). Reason: the text is cut at 200 characters and the
way out is chosen by the reason; a 358-character path and the rule do not fit in a `git-error`
text.

Q6. How does the writer know the file?

From git's own message for the failed `git add` (`Filename too long` on Windows, `File name too
long` elsewhere, with the path git quotes). A message with neither, or with no path to read,
stays a `git-error` with git's text, as today. The writer does not measure paths itself before
`git add`. Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: git
decides what is too long (it depends on `core.longpaths` and the system); a limit of the CLI's
own would be a guess.

Q7. Does chantier set `core.longpaths`, untrack artifacts already committed, or move folders?

No. It writes no git configuration, and the writer's git commands stay the list in `AGENTS.md`;
a surface that already committed such a folder, or holds one outside `work/scratch/`, is repaired
by hand (the ignore line then keeps an untracked one out). Settled by the Chief of Staff
(2026-11-20, the user asks no questions). Reason: `AGENTS.md` names the writer's git commands and
where chantier writes; no fallback.

Q8. Does an existing planning folder get the new line?

Yes, by the existing means: `ensure_gitignore` completes a `.gitignore` that lacks a line, at the
next command that writes there. Studio's line in `.git/info/exclude` can then go, by hand.
Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: it is what the
code does today for every new line.

Q9. Is anything split out?

No. Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the request
fits one CR: one ignore line, one matcher case, one blocked reason, three cards.
