Short name: `font-hang`

# Answers (owner, 2026-11-20, Chief of Staff grill)

- No grill question: the request is clear (close Chromium on the font-load error path so the run fails instead of hanging).

- Open question 1 (chartPage.ts openChartPage has the same leak between chromium.launch and its return): include it in this CR, same try/close/rethrow pattern, with its own regression check. Decided by the Chief of Staff under the owner's standing autonomy grant ('arrete tes questrion soitr autonome'): same small test-only fix, same file family.
