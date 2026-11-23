Short name: `blank-save`

1. blank-save-Q1: **One block per line** (owner, 2026-11-23, option B). A run of blank lines no longer
   shows as one blank-lines block: each blank line shows as its own block. This changes the CR-444
   design (`blank-runs`, PR #453) and its SwRS.
2. blank-save-Q2: **Text replaces the run** (owner, option A, answered before Q1 B was known: to be
   restated per line, see Q5).
3. blank-save-Q3: Owner's words: "That means this is not tested as side case". Read as: the hang
   shows the edge case has no test; the guard question is put again (Q6).
4. blank-save-Q4: **Running batch-09** (owner, option A).
5. blank-save-Q5: **Each extra line is a block** (owner, option A). Between two blocks, the one blank
   line that separates them in Markdown stays hidden: N blank lines give N−1 blank-line blocks. At the
   end of the body, and at the top of a file without frontmatter, every blank line is a block (the
   issue's 6 lines give 6 blocks). Text typed in one of them replaces that one line (this restates Q2
   per line); a blank line is added before or after only when Markdown needs one to keep the text a
   block of its own.
6. blank-save-Q6: **Tests and a guard** (owner, option A). Tests for the edge cases the issue lists:
   segmentation of N blank lines, typing in a blank-line block, the save always ending. And a general
   guard: every save ends in success or in a shown error (with a timeout); Cancel always closes the
   editor.
7. blank-save-Q7: **Delete removes that one line** (owner, option A). Delete or Backspace on a
   selected blank-line block, or its Delete block button, removes that blank line only; the hidden
   separator always stays, so two blocks are never glued together.
8. Spec critic: yes, on Fable (owner's rule): it changes what the writer sees and does in edit mode,
   and an existing design (CR-444).
9. Grilled enough: decided by the Chief of Staff (owner's autonomy rule on rounds), 2026-11-23.

Spec critic (Fable), 2026-11-23: 7 points, 3 fixes applied by the spec-writer without the owner,
4 questions; the spec's own 3 open questions asked with them.

10. blank-save-Q8: **Three CRs, one stack** (owner, option A). (A) the #485 hang fix first (closes the
    issue), then (B) the general save guard, then (C) one block per blank line; all in batch-09's stack.
11. blank-save-Q9: **The frontmatter time limit stops when the editor closes or an error shows**
    (owner, option A): "Saved. Refreshing preview…" is bounded too.
12. blank-save-Q10: **Neutral timeout message** (owner, option A): "No answer yet; your text may
    already be saved", Done to retry, Cancel to close; a stale refusal on the retry reads as already
    saved or changed, close the editor.
13. blank-save-Q11: Owner's words: "Je ne comprends pas les new line dans le frontmatter ça ne devrait
    pas être dans le scope". The question was about blank lines in the body right after the
    frontmatter, not inside it; asked again as Q13.

Destination: running batch-09
