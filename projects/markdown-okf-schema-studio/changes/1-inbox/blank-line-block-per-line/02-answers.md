Short name: `blank-per-line`

Grilled as part of `blank-run-edit-stuck-saving` (short name `blank-save`) on 2026-11-23; the owner's
answers are recorded there and carried here. Its first specification's sections 1-4 and 6 (and the
critic's points 4 and 5) are this CR's starting point.

1. blank-per-line-Q1 (= blank-save-Q1): **One block per line**, replacing the CR-444 one-block-per-run
   design and its SwRS.
2. blank-per-line-Q2 (= blank-save-Q5): **Each extra line is a block.** Between two blocks the one
   separator line stays hidden: N blank lines give Nâˆ’1 blocks. At the end of the body and at the top
   of a file without frontmatter, every blank line is a block. Text typed in one replaces that one
   line (blank-save-Q2 restated per line); a blank line is added before or after only when Markdown
   needs one.
3. blank-per-line-Q3 (= blank-save-Q7): **Delete removes that one line**; the hidden separator always
   stays.
4. blank-per-line-Q4 (= blank-save-Q12): **Everywhere**: inside lists, quotes, admonitions,
   definitions and footnotes too; their indent and sibling rules stay.
5. blank-per-line-Q5 (= blank-save-Q13): **A body of only N blank lines after the frontmatter's
   closing `---` shows N blocks**, like the end of a file. Nothing inside the frontmatter changes.
6. blank-per-line-Q6 (= blank-save-Q8): **Stack order**: after `save-guard-never-hangs`, last of the
   three.
7. Spec critic: yes, on Fable (owner's rule): it changes what the writer sees and does in edit mode,
   and an existing design (CR-444). The first critic's points 4 and 5 are already settled.
8. blank-per-line-Q8 (spec critic, Fable, finding 5): **Amend StRS BLOCK-011.** Its text names the
   blank-line block's rule (text typed in one keeps the other blank lines around it), with the owner's
   re-approval of the new wording.
9. blank-per-line-Q9 (spec critic, finding 6): **After Delete on a blank-line block**, the selection
   goes to the blank-line block now at that place, else the blank-line block just above it in the same
   run; when the run has none left, nothing is selected, so one more Delete removes no text.

Destination: running batch-09
