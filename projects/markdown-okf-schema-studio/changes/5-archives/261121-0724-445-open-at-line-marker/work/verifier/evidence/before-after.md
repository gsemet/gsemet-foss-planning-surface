# Before and after

Before = base chantier/batch-07/cr-442-release-notes-highlights-text-first-pict (590b2c52). After = f61ac3a920146b83d5b3deaa56a1e3472b564481.

- Not captured as before images: the visual scenarios run on Linux CI only; at the base `previewRevealLine`
  does not exist (`git grep previewRevealLine origin/<base> -- src test` finds nothing), so the before is "no marker".
- After (CI run 44860928294, artifact e2e-visual-attempt-1, scratch only; made-up fixture text, no user path, no username):
  - v04-line-marker-code-line-light-900.png: arrow and band on one code line, light.
  - v10-line-marker-closed-dropdown-dark-900.png: a closed dropdown unfolded, arrow and band on the inner line, dark.
  - v11-line-marker-edit-mode-list-dark-900.png: edit mode, arrow left of the list handle, no overlap, dark.
  Reproduce: `gh run download 44860928294 -n e2e-visual-attempt-1`, folder e2e/screenshots/visual/lifecycle-sync/.
- Real VS Code screenshots (ta-*, tb-* in evidence/) are Coder trial captures, not re-captured here.
