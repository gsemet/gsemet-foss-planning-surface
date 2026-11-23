Short name: `save-guard`

Grilled as part of `blank-run-edit-stuck-saving` (short name `blank-save`) on 2026-11-23; the owner's
answers are recorded there and carried here. Its first specification's section 5 (and the critic's
points 2, 3, 6 and 7) is this CR's starting point.

1. save-guard-Q1 (= blank-save-Q6): **Tests and a guard.** Every save ends in success or in a shown
   error (with a time limit); Cancel always closes the editor.
2. save-guard-Q2 (= blank-save-Q9): **The frontmatter time limit stops when the editor closes or an
   error shows**: "Saved. Refreshing preview…" is bounded too.
3. save-guard-Q3 (= blank-save-Q10): **Neutral timeout message**: "No answer yet; your text may
   already be saved", Done to retry, Cancel to close; a stale refusal on the retry reads as already
   saved or changed, close the editor.
4. save-guard-Q4 (= blank-save-Q14): **Cancel during "Saving…" closes the editor and the save goes
   on**; the text is kept.
5. save-guard-Q5 (= blank-save-Q15): **10 seconds, checked by a measure**: save-to-render time on the
   largest fixture; back to the owner through the Chief of Staff if the slowest is over half the limit.
6. save-guard-Q6 (= blank-save-Q8): **Stack order**: after `blank-run-edit-stuck-saving`, before
   `blank-line-block-per-line`.
7. Spec critic: yes, on Fable (owner's rule): it changes what the writer sees on every save, and a
   refusal scenario of an SwRS (BLOCK-053).

Destination: running batch-09
